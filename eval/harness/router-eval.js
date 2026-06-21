// Router-accuracy eval — measures whether the triage catalog routes a natural
// problem-description to the CORRECT skill. The A/B harness tests a skill once
// it's already chosen; THIS tests the choosing step (the 94-skill bet's blind spot).
//
// Run via Claude Code Workflow (NOT node):
//   Workflow({ scriptPath: 'eval/harness/router-eval.js', args: { names: ["skill-a", ...] } })
//   optional: { names:[...], routeModel:'haiku', genModel:'opus' }
//
// Method:
//   1) GEN  (Opus, per skill): read the skill file, write 1 realistic Thai MT
//      problem a confused person would actually type — symptoms/situation, NOT
//      the skill's title keywords (else routing is trivially easy). Ground-truth
//      label = that skill.
//   2) ROUTE (Haiku = realistic "user pasted triage.md into a chat"): read
//      prompts/triage.md catalog + the problem → top-3 skill ids, ranked.
//   3) SCORE (mechanical): top1 = picks[0]==target · top3 = target ∈ picks.
//   4) ADJUDICATE (Opus, top3-misses only): is picks[0] an ACCEPTABLE alternative
//      for this problem (soft miss = legit overlap/boundary) or a HARD miss
//      (routed somewhere unrelated)? + which skill it got confused with.
//
// Output: top1/top3 accuracy + hardMiss/softMiss lists + confusion pairs.
// Mis-routing within a known cluster (soft) validates the "overlap" concern;
// hard misses are the real routing failures to fix in the catalog descriptions.

export const meta = {
  name: 'router-eval',
  description: 'Router-accuracy eval — does triage.md route a problem to the right skill?',
  phases: [
    { title: 'Gen', detail: 'Opus writes one natural problem per skill (no title keywords)' },
    { title: 'Route', detail: 'Haiku routes each problem via triage catalog → top-3' },
    { title: 'Adjudicate', detail: 'Opus judges top3-misses: soft (overlap) vs hard' },
  ],
}

const PROBLEM = { type:'object', properties:{ problem:{type:'string'} }, required:['problem'], additionalProperties:false }
const PICKS = { type:'object', properties:{ picks:{type:'array', items:{type:'string'}}, reason:{type:'string'} }, required:['picks'], additionalProperties:false }
const ADJ = { type:'object', properties:{ acceptable:{type:'boolean'}, confusedWith:{type:'string'}, why:{type:'string'} }, required:['acceptable','confusedWith','why'], additionalProperties:false }

function cfg(a){
  if (typeof a === 'string'){ try { a = JSON.parse(a) } catch { a = {} } }
  if (Array.isArray(a)) return { names:a, routeModel:'haiku', genModel:'opus', batch:10 }
  return { names:(a&&a.names)||[], routeModel:(a&&a.routeModel)||'haiku', genModel:(a&&a.genModel)||'opus', batch:Number(a&&a.batch)>0?Number(a.batch):10 }
}
const C = cfg(args)
const NAMES = C.names
if (!NAMES.length){ log('router-eval: no names — pass { names:[...] }'); return { error:'no names' } }
log(`router-eval: ${NAMES.length} skills · route=${C.routeModel} · gen=${C.genModel}`)

const VOCAB = NAMES.join(', ')

function chunks(a, n){ const o=[]; for (let i=0;i<a.length;i+=n) o.push(a.slice(i,i+n)); return o }
const BATCH = Number(C.batch) > 0 ? Number(C.batch) : 10
let rows = []
let _bi = 0
const _parts = chunks(NAMES, BATCH)
for (const _part of _parts) {
  _bi++
  log(`batch ${_bi}/${_parts.length} — ${_part.length} skills (gentle on rate-limit)`)
  const _r = await pipeline(
  _part,
  // 1) GEN ground-truth problem
  (name) => agent(
    `ใช้ Read tool อ่าน skills/${name}.md ก่อน. แล้วสมมติว่าคุณเป็นคน (นักเทคนิคการแพทย์/นักศึกษา MT/คนทำงานแล็บ) ที่กำลังเจอสถานการณ์ซึ่ง **สกิลนี้ถูกออกแบบมาช่วยพอดี**. ` +
    `เขียน "ข้อความที่เขาจะพิมพ์ถามจริงๆ" 1 อัน (ภาษาไทย, 2-4 ประโยค) — เล่าเป็น **อาการ/สถานการณ์/ความอึดอัดจริง** ไม่ใช่ศัพท์เทคนิค. ` +
    `**ห้ามใช้คำที่อยู่ในชื่อสกิล (${name}) หรือ title ของไฟล์** และห้ามบอกชื่อสกิล — ให้ router ต้องเดาเอาเองจากเนื้อปัญหา. คืน field problem เท่านั้น.`,
    { schema: PROBLEM, model: C.genModel, phase:'Gen', label:`gen:${name}` }
  ),
  // 2) ROUTE via catalog
  (gen, name, i) => {
    if (!gen || !gen.problem) return null
    return agent(
      `ใช้ Read tool อ่าน prompts/triage.md ก่อน (เป็น catalog ของสกิลทั้งหมด). ` +
      `ผู้ใช้พิมพ์ปัญหานี้มา:\n\n"${gen.problem}"\n\n` +
      `เลือกสกิลที่ "ตรงสุด" 3 ตัวจาก catalog เรียงจากตรงสุด→รองลงมา. ` +
      `คืน picks เป็น array ของ **id สกิลเป๊ะ** (เลือกจากรายการนี้เท่านั้น ห้ามแต่งใหม่/ห้ามสะกดเพี้ยน): ${VOCAB}. ` +
      `+ reason ≤1 บรรทัด.`,
      { schema: PICKS, model: C.routeModel, phase:'Route', label:`route:${name}` }
    ).then(r => {
      if (!r || !Array.isArray(r.picks)) return { target:name, problem:gen.problem, picks:[], top1:false, top3:false, err:true }
      const picks = r.picks.map(s => String(s).trim()).filter(Boolean)
      return { target:name, problem:gen.problem, picks, reason:r.reason||'',
               top1: picks[0]===name, top3: picks.slice(0,3).includes(name) }
    })
  }
  )
  rows = rows.concat(_r)
}

const clean = rows.filter(Boolean)
const scored = clean.filter(r => !r.err)
const n = scored.length
const top1 = scored.filter(r=>r.top1).length
const top3 = scored.filter(r=>r.top3).length
const misses = scored.filter(r=>!r.top3)

// 3) ADJUDICATE top3-misses (barrier: need the full miss set; each judged independently)
const adjudicated = await parallel(misses.map(m => () =>
  agent(
    `ปัญหาที่ผู้ใช้พิมพ์:\n"${m.problem}"\n\n` +
    `สกิลที่ "ควรจะใช่" (ground-truth) = ${m.target}\n` +
    `router กลับเลือก (อันดับ 1) = ${m.picks[0]||'(ไม่มี)'} · ทั้ง 3 อันดับ = ${m.picks.join(', ')||'(ว่าง)'}\n\n` +
    `ตัดสิน: สกิลที่ router เลือกอันดับ 1 ("${m.picks[0]||''}") เป็น **ทางเลือกที่ยอมรับได้** สำหรับปัญหานี้ไหม ` +
    `(acceptable=true ถ้ามันคาบเกี่ยว/เป็น boundary ใกล้กันจน routing ไปตัวนั้นก็ช่วยผู้ใช้ได้จริง · acceptable=false ถ้าไปคนละเรื่อง=หลงทางจริง). ` +
    `confusedWith = id สกิลที่มันสับสนไปเลือก. why ≤1 บรรทัด.`,
    { schema: ADJ, model:'opus', phase:'Adjudicate', label:`adj:${m.target}` }
  ).then(v => ({ ...m, adj: v }))
))
const adj = adjudicated.filter(Boolean)
const soft = adj.filter(x => x.adj && x.adj.acceptable)
const hard = adj.filter(x => x.adj && !x.adj.acceptable)

return {
  n, errors: clean.length - n,
  top1Acc: +(top1/n).toFixed(3), top3Acc: +(top3/n).toFixed(3),
  softMissN: soft.length, hardMissN: hard.length,
  hardMiss: hard.map(x=>({ target:x.target, got:x.picks[0]||'', picks:x.picks.slice(0,3), why:x.adj.why, problem:x.problem })),
  softMiss: soft.map(x=>({ target:x.target, got:x.picks[0]||'', why:x.adj.why })),
  top1Misses: scored.filter(r=>!r.top1 && r.top3).map(r=>({ target:r.target, got:r.picks[0], picks:r.picks.slice(0,3) })),
}
