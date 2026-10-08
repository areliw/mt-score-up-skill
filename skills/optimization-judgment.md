---
skill: optimization-judgment
title: โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง (Optimization Judgment)
type: ADVISE               # ช่วยตัดสินใจ formulate/เลือกวิธี ไม่ใช่ตำรา Simplex
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-10-08
status: draft
disclaimer: "ช่วยคิดเลือกวิธี optimize + เลี่ยงกับดัก เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ผลต้องตรวจกับเงื่อนไขจริงและทดสอบก่อนใช้ตัดสินใจจริง (เช่นจัดเวร/จัดสรรทรัพยากร) · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง

มีปัญหาแบบ "หาค่าที่ดีที่สุดภายใต้เงื่อนไข" (จัดเวร, จัดสรรเครื่อง/คน/น้ำยา, เส้นทาง) → โค้ชนี้ช่วย **เลือกวิธี + เลี่ยงกับดักที่ทำให้คำตอบใช้จริงไม่ได้**

> **กฎ #1 (เลือกวิธี):** เชิงเส้น + แน่นอน (deterministic) + เล็ก-กลาง → ใช้ **LP/MIP** เสมอ (รับประกัน optimal) — อย่าเพิ่งหยิบ GA/PSO. ไป metaheuristic เฉพาะตอน nonlinear/combinatorial/ใหญ่มาก, ไป simulation เฉพาะตอนมี randomness/คิว. **หยิบ GA ทั้งที่ LP แก้ได้ = over-engineer ผิด.**
> **กับดัก #1 (คำตอบพัง):** **ลืม constraint** → optimal สวยแต่ละเมิดเงื่อนไขจริง = ใช้ไม่ได้. ก่อน solve ต้อง formulate ครบ 3 ชิ้น (objective · decision vars · constraints) แล้ว **ไล่ constraint จากโจทย์คำต่อคำ** (รวม ≥0, integer, capacity).
> งานเลข Simplex/PSO อย่าให้ AI กะในหัว → ใช้ solver (ดู `offload-to-automation`)

## เครื่องมือ (รันก่อนคิดเลข)
มีโมเดล LP/IP/assignment เล็กๆ หรือมี "คำตอบ" ที่จะเชื่อ → **รันสคริปต์ก่อน แล้วค่อยตัดสินด้วย fork/กับดักข้างล่าง** (อย่ากะ Simplex หรือไล่ constraint ด้วยตา) · รัน `--help` ก่อน ไม่ต้องอ่านซอร์ส · ไฟล์อยู่ใน `scripts/` ของโฟลเดอร์ skill (ใน repo: `skills/optimization-judgment/scripts/`) · โมเดลเขียนเป็น JSON (`sense`, `vars`, `c`, `constraints[{name,a,op,b}]`, ทุกตัวแปร ≥ 0) ดูตัวอย่างใน `data/`
- `python scripts/lp_check.py solve data/wyndor.json --delta 6` → สถานะ **OPTIMAL / INFEASIBLE / UNBOUNDED** (เลขเศษส่วนแท้ ไม่ปัด) · ค่าตัวแปร + objective · ตาราง constraint: LHS, RHS, slack, **binding**, shadow price ต่อ +1 RHS · `--delta D` เทียบการเปลี่ยนจริงกับ shadow price × D ถ้าไม่ตรงจะพิมพ์ `OUTSIDE allowable range` (กับดัก "ใช้ shadow price นอกช่วง")
- `python scripts/lp_check.py solve data/reddy_mikks.json --integer all` → branch-and-bound + ผลของ "ปัดเศษคำตอบ LP" (ได้ 3, 2 = infeasible; integer optimum จริงได้ค่าต่างจาก LP) · `--integer x1,x2` เลือกเฉพาะตัวแปรที่ต้องเป็นจำนวนเต็ม
- `python scripts/lp_check.py check data/wyndor.json --x 4 6` → ไล่ **ทุก constraint คำต่อคำ** + ≥ 0 + จำนวนเต็ม ของคำตอบที่ใครเสนอมา · exit 1 ถ้าไม่ feasible (กับดัก #1 "ลืม constraint": solve โมเดลที่ขาด plant3 ได้ 42 ซึ่งสวยกว่า 36 แต่ `check` จับว่าผิด)
- `python scripts/lp_check.py assign data/machineco.csv [--max]` → assignment (Hungarian) จากตารางต้นทุนจัตุรัส ไม่มี header
- ขอบเขต: vertex enumeration แม่นแต่โตแบบ exponential → ~4 ตัวแปร / ~12 constraint (เกินจะปฏิเสธ) · งานจริงใช้ Excel Solver / OR-Tools / GUROBI (ดู `offload-to-automation`) · **ไม่มี tool** สำหรับ GA/PSO/Pareto/simulation เพราะผลสุ่มและไม่มีเลขที่ตรวจซ้ำแบบแน่นอนได้ · ทุก output มีบรรทัด `ADVISORY` — เป็นตัวช่วยตรวจ ไม่ใช่ผู้ตัดสิน
- ทดสอบแล้ว: `evals/test_lp_check.py` (19 ข้อ เทียบ Wyndor ของ Hillier-Lieberman (2,6)/36 + dual (0, 3/2, 1), Reddy Mikks ของ Taha (3, 1.5)/21, Machineco ของ Winston = 15, และตัวอย่างใน digest 261475: 122/78/66,100, shadow price S2 = 16.67, unbounded case · Hungarian เทียบ brute force 25 เมทริกซ์สุ่ม · must-fail control 3 ตัว: ลืม constraint · ปัดเศษแทน integer · ขยาย shadow price นอกช่วง → ต้องแดง)

## ใช้เมื่อ
- ตั้งโจทย์ optimization / เลือก solver-method / ทำ sensitivity analysis
- "ใช้ LP หรือ heuristic", "จัดเวร/จัดสรรยังไงให้ดีสุด", "อ่าน shadow price ยังไง"

## วิธีใช้
วาง skill นี้ + เล่าปัญหา → AI บังคับ formulate ก่อน แล้วชี้วิธี + กับดัก

---

## วิธีเลือก (AI: ทำตามนี้) — forks

### 1. exact (LP/MIP) vs metaheuristic (GA/PSO) vs simulation — ข้อใหญ่สุด
- **เชิงเส้น + deterministic + เล็ก-กลาง** → **LP/Simplex/MIP** (Excel Solver, OR-Tools, GUROBI) — รับประกัน optimal (MIP: เมื่อ **พิสูจน์ optimality/gap=0** ไม่ใช่แค่ solver หยุด/timeout — ดู Fork 7) = **default**
- **nonlinear / combinatorial / ใหญ่จน exact ช้าเกิน (NP-Hard เช่น จัดเวร, VRP, TSP)** → **metaheuristic (GA/PSO/ACO)** — ได้ "ดีพอ" ไม่รับประกัน optimal · ⚠️ NP-hard *เล็ก ๆ* ก็ solve exact ได้ — เลือก metaheuristic เพราะ **ขนาด/เวลา** ไม่ใช่เพราะเป็น NP-hard เอง
- **มี randomness/queue/เวลา แก้เป็นสมการไม่ได้** (คิวคนไข้, โหลดเครื่อง) → **simulation (Monte Carlo/DES)** — ได้การกระจาย (utilization, waiting time)
- ✅ test: เขียน objective+constraint เป็นสมการเชิงเส้นได้ครบ → อย่าใช้ GA (over-engineer); เขียนไม่ได้เพราะมี randomness → อย่าใช้ LP

### 2. GA vs PSO (ในกลุ่ม metaheuristic)
- อยาก converge เร็ว, พารามิเตอร์น้อย, ตัวแปร **ต่อเนื่อง** → **PSO**
- มีโครงสร้าง **combinatorial / encode เป็น gene ได้ / ต้อง explore กว้าง** → **GA**

### 3. single vs multi-objective (Pareto)
- objective เดียว → optimize ตรงๆ
- หลาย objective ขัดกัน (max คุณภาพ vs min cost) → รู้ weight ชัด → **Weighted Sum** (ได้ 1 จุด); อยากเห็น trade-off ทั้งชุด → **Pareto front (NSGA-II)** แล้วค่อยเลือก
- ✅ อย่ายัด weight มั่วถ้ายังไม่รู้ trade-off — หา Pareto ก่อน

### 4. network model (เมื่อปัญหาเป็น node + arc)
ส่งตรง min cost → **Transportation** · จับคู่ 1:1 → **Assignment** · ผ่าน node กลาง → **Transshipment** · เส้นสั้นสุด → **Shortest Path** · flow สูงสุด (arc มี capacity) → **Maximal Flow** · เชื่อมทุก node ถูกสุด → **Min Spanning Tree**

### 5. formulation ต้องครบ 3 ชิ้นก่อนแตะ solver
Decision Variables + Objective (ในรูป vars) + Constraints (สมการ/อสมการ) · LP ได้ก็ต่อเมื่อ ต่อเนื่อง + ไม่มี xi·xj + ไม่มี x² + deterministic — ผิดข้อใด = ไม่ใช่ LP

### 6. sensitivity: shadow price ("คุ้มจะเพิ่มทรัพยากรไหม")
- **Shadow price** = objective เปลี่ยนเท่าไรต่อการเพิ่ม RHS ของ constraint 1 หน่วย = ยอมจ่ายเพิ่มได้สูงสุดเท่าไรต่อ 1 หน่วย
- **Binding** (slack=0) → SP≥0 (ปกติ >0; เครื่องหมายขึ้นกับ min/max + ทิศ constraint ≤/≥) → เพิ่มทรัพยากรช่วยได้ (ลงทุนถ้าราคา < SP) · ⚠️ **degenerate** อาจ SP=0 แม้ binding · **Non-binding** (มี slack) → SP=0 → เพิ่มไม่ช่วย อย่าซื้อ
- Δobjective = SP × ΔRHS **เฉพาะใน allowable range**

### 7. MIP solve ช้า/ไม่จบ — ทำไงก่อนทิ้ง exact
อย่าเด้งไป GA ทันทีเมื่อ MIP ช้า — ลองตามลำดับ: (1) **ใส่ time-limit + รับ MIP gap** (เช่น 1-2% มักดีพอใช้งานจริง) — solver คืนคำตอบที่ดีที่สุดที่เจอ + การันตีว่าห่าง optimal ไม่เกิน gap (2) **LP relaxation** เป็น bound + reality-check ว่าโจทย์สมเหตุผล (3) **warm-start** ด้วยคำตอบ heuristic (4) กระชับ formulation (tighten bound, ตัด symmetry). ทิ้ง exact ไป metaheuristic **เฉพาะตอน gap ยังกว้างหลังทำครบ** — ตอนนั้นยอมเสีย "การันตี optimal" แลกความเร็ว

---

## กับดัก (Anti-patterns)
- **ลืม constraint → solution ใช้จริงไม่ได้** (#1) — optimal สวยแต่ละเมิดเงื่อนไขที่ไม่ได้เขียน (ลืม ≥0, capacity, ต้องบริการครบ) → เช็คทุก constraint จากโจทย์คำต่อคำก่อน solve
- **ลืม integer constraint** — ต้องเป็นจำนวนเต็ม (รถ/คน/เครื่อง) แต่ solve เป็น LP ต่อเนื่อง → ได้ 2.7 = ใช้ไม่ได้ → ใช้ **MIP**
- **อ่าน Infeasible vs Unbounded ผิด** — Infeasible = constraint ขัดกัน (ผ่อน constraint) · Unbounded = มักแปลว่า **ลืม constraint** (วนกลับข้อแรก)
- **greedy/local search ติด local optimum** — GA ต้องมี mutation, PSO ต้อง diversity; รันรอบเดียวแล้วเชื่อ = พลาด → รันหลาย seed
- **over-model** — ยัด GA/nonlinear ทั้งที่ LP เล็กแก้ได้ใน 1 วิ; เริ่มจากโมเดลง่ายสุดที่ตอบโจทย์
- **simulation รันน้อย → CI กว้าง สรุปมั่ว** — เพิ่ม replication จน CI แคบพอ
- **GIGO** — input/distribution ผิด → optimal ก็ไร้ค่า; ตรวจ assumption ก่อนเชื่อ
- **ใช้ shadow price นอก allowable range / ของ non-binding** → ตัดสินใจลงทุนผิด
- **ตัวแปรคูณกัน/มี x² แล้วยังเรียก LP** → nonlinear, Simplex ใช้ไม่ได้

---

## ช่องสำหรับผู้เชี่ยวชาญเติม
> เติมเคสจริง เช่น:
> - *"(MT) จัดเวร/จัดสรรเครื่องในแล็บ ผมใช้... เพราะ constraint จริงคือ..."*
> - *"ปัญหาที่ดูเหมือน LP แต่จริงๆ มี randomness ต้องใช้ simulation คือ..."*

---
*ช่วยคิดเลือกวิธี optimize + เลี่ยงกับดัก เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ผลต้องตรวจกับเงื่อนไขจริงและทดสอบก่อนใช้ตัดสินใจจริง · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้*
