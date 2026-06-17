// Reusable ×3 A/B blind-judge harness (the AI half of the P4 gate).
//
// Run via Claude Code Workflow — NOT node:
//   Workflow({ scriptPath: 'eval/harness/ab-x3.js', args: [
//     { skill: 'foo-judgment', file: 'skills/foo-judgment.md',
//       focus: 'the specific trap to test (or "the skill\'s own #1 anti-pattern")' },
//     ...
//   ]})
//
// Method (validated 2026-06-18): for each target, a strong model derives one hard
// trap scenario from the skill's documented failure mode; a WEAK model (Haiku)
// answers it WITHOUT vs WITH the skill, **3 reps per arm, averaged**; a strong model
// blind-judges each rep (A/B order alternated by index parity). Δ = mean(with) − mean(without).
//
// WHY ×3 (do not reduce to single-pass): on 2026-06-18 a single pass gave blood-donor
// a false Δ −3 "regression"; ×3 flipped it to +1.33. Single-pass is triage only —
// never act (cut/rewrite) on it. See eval/2026-06-18-p1-probe-results.md.
//
// Decision rule: act only on the ×3 mean. floor = 1.4 for "clear lift";
// regression = mean(with) UNSAFE (≤2.5) while mean(without) was safe (≥3).

export const meta = {
  name: 'ab-x3',
  description: '×3 A/B blind-judge harness — score skills passed via args',
  phases: [
    { title: 'Generate', detail: 'Opus derives one trap per skill' },
    { title: 'Answer', detail: '3 reps × (Haiku without + with), blind' },
    { title: 'Judge', detail: 'Opus blind-scores each rep; Δ = mean(with) − mean(without)' },
  ],
}

const SCENARIO = { type:'object', properties:{ scenario:{type:'string'} }, required:['scenario'], additionalProperties:false }
const VERDICT = { type:'object', properties:{ score1:{type:'number'}, score2:{type:'number'}, reason:{type:'string'} }, required:['score1','score2','reason'], additionalProperties:false }

// args may arrive as an array OR as a JSON string (the Workflow tool can stringify it) — handle both.
function parseTargets(a) {
  if (Array.isArray(a)) return a
  if (typeof a === 'string') { try { const v = JSON.parse(a); return Array.isArray(v) ? v : [] } catch { return [] } }
  return []
}
const TARGETS = parseTargets(args)
if (!TARGETS.length) { log('ab-x3: no targets — pass args as a JSON array [{skill,file,focus}, ...]'); return { error: 'no targets' } }

const results = await pipeline(
  TARGETS,
  (t, _o, i) => agent(
    `ใช้ Read tool อ่าน ${t.file} ก่อน. แล้วแต่งสถานการณ์จริงแบบไทย MT 1 อัน ที่ "ล่อ" ให้คนไม่เชี่ยวชาญตกหลุมนี้พอดี: ${t.focus}. ` +
    `สมจริง · ตอบได้จริง · ห้ามบอกคำตอบที่ถูก · ห้ามพาดพิงว่ามีคู่มือ · ≤120 คำ. คืน field scenario เท่านั้น.`,
    { schema: SCENARIO, model:'opus', phase:'Generate', label:`trap:${t.skill}` }
  ),
  (trap, t, i) => {
    if (!trap || !trap.scenario) return null
    const repThunks = [0,1,2].map(r => () => {
      const baseFn  = () => agent(
        `(rep ${r}) คุณเป็นนักเทคนิคการแพทย์จบใหม่ ไม่มีคู่มือพิเศษ. ตอบกระชับ ≤150 คำ ว่าจะตัดสินใจ/ทำยังไง:\n\n${trap.scenario}`,
        { model:'haiku', phase:'Answer', label:`base:${t.skill}#${r}` }
      )
      const skillFn = () => agent(
        `(rep ${r}) คุณเป็นนักเทคนิคการแพทย์จบใหม่. ใช้ Read tool อ่าน ${t.file} ก่อน แล้วใช้วิจารณญาณในไฟล์นั้นตอบกระชับ ≤150 คำ:\n\n${trap.scenario}`,
        { model:'haiku', phase:'Answer', label:`skill:${t.skill}#${r}` }
      )
      return parallel([baseFn, skillFn]).then(a => {
        const wo=a[0], wi=a[1]
        if (!wo || !wi) return null
        const even = ((i+r)%2)===0
        const a1 = even?wo:wi, a2 = even?wi:wo
        return agent(
          `กรรมการ blind. สถานการณ์ MT ไทย + คำตอบ 2 อัน (สลับลำดับ ไม่บอกว่าอันไหนมีคู่มือ). กับดักที่ต้องหลีก: ${t.focus}. ` +
          `ให้คะแนนแต่ละอัน 0-5 (5=หลีกกับดัก+ถูก+ครบ, 2=ก้ำกึ่ง, 0=ตกหลุมเต็ม). เน้นความปลอดภัย/ถูกต้องมากกว่าสำนวน.\n\n` +
          `สถานการณ์:\n${trap.scenario}\n\n--- Answer 1 ---\n${a1}\n\n--- Answer 2 ---\n${a2}\n\nคืน score1, score2, reason (≤1 บรรทัด).`,
          { schema: VERDICT, model:'opus', phase:'Judge', label:`judge:${t.skill}#${r}` }
        ).then(v => { if (!v) return null; return { ws: even?v.score2:v.score1, wos: even?v.score1:v.score2 } })
      })
    })
    return parallel(repThunks).then(reps => {
      const ok = reps.filter(Boolean)
      if (!ok.length) return null
      const mWith = ok.reduce((s,x)=>s+x.ws,0)/ok.length
      const mWithout = ok.reduce((s,x)=>s+x.wos,0)/ok.length
      const delta = +(mWith - mWithout).toFixed(2)
      let kind='tie'
      if (delta>=1.4 && mWithout<=2.5 && mWith>=3) kind='rescued'
      else if (delta>=1.4) kind='better'
      else if (delta<=-1 && mWith<=2.5) kind='regression'
      else if (delta<=-0.5) kind='style-cost'
      else if (mWith<=2.5 && mWithout<=2.5) kind='no-rescue'
      return { skill:t.skill, reps:ok.length, meanWithout:+mWithout.toFixed(2), meanWith:+mWith.toFixed(2), delta, kind }
    })
  }
)

const clean = results.filter(Boolean)
return { n: clean.length, rows: clean.sort((a,b)=>b.delta-a.delta) }
