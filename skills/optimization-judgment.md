---
skill: optimization-judgment
title: โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง (Optimization Judgment)
type: ADVISE               # ช่วยตัดสินใจ formulate/เลือกวิธี ไม่ใช่ตำรา Simplex
needs: any                 # ใช้ได้กับ AI ทุกตัว
author: "Phanuphong Tameesak - MT Score UP!"
last_edited: 2026-06-04
status: draft
disclaimer: "ช่วยคิดเลือกวิธี optimize + เลี่ยงกับดัก เพื่อการศึกษา ไม่ใช่คำสั่งทางการ — ผลต้องตรวจกับเงื่อนไขจริงและทดสอบก่อนใช้ตัดสินใจจริง (เช่นจัดเวร/จัดสรรทรัพยากร) · ผู้นำไปใช้รับผิดชอบการตัดสินใจที่นำไปใช้จริง · ผู้สร้างไม่รับผิดต่อความเสียหายจากการนำไปใช้"
---

# โค้ช Optimization/OR — เลือกวิธีให้ถูก + คำตอบใช้ได้จริง

มีปัญหาแบบ "หาค่าที่ดีที่สุดภายใต้เงื่อนไข" (จัดเวร, จัดสรรเครื่อง/คน/น้ำยา, เส้นทาง) → โค้ชนี้ช่วย **เลือกวิธี + เลี่ยงกับดักที่ทำให้คำตอบใช้จริงไม่ได้**

> **กฎ #1 (เลือกวิธี):** เชิงเส้น + แน่นอน (deterministic) + เล็ก-กลาง → ใช้ **LP/MIP** เสมอ (รับประกัน optimal) — อย่าเพิ่งหยิบ GA/PSO. ไป metaheuristic เฉพาะตอน nonlinear/combinatorial/ใหญ่มาก, ไป simulation เฉพาะตอนมี randomness/คิว. **หยิบ GA ทั้งที่ LP แก้ได้ = over-engineer ผิด.**
> **กับดัก #1 (คำตอบพัง):** **ลืม constraint** → optimal สวยแต่ละเมิดเงื่อนไขจริง = ใช้ไม่ได้. ก่อน solve ต้อง formulate ครบ 3 ชิ้น (objective · decision vars · constraints) แล้ว **ไล่ constraint จากโจทย์คำต่อคำ** (รวม ≥0, integer, capacity).
> งานเลข Simplex/PSO อย่าให้ AI กะในหัว → ใช้ solver (ดู `offload-to-automation`)

## ใช้เมื่อ
- ตั้งโจทย์ optimization / เลือก solver-method / ทำ sensitivity analysis
- "ใช้ LP หรือ heuristic", "จัดเวร/จัดสรรยังไงให้ดีสุด", "อ่าน shadow price ยังไง"

## วิธีใช้
วาง skill นี้ + เล่าปัญหา → AI บังคับ formulate ก่อน แล้วชี้วิธี + กับดัก

---

## วิธีเลือก (AI: ทำตามนี้) — forks

### 1. exact (LP/MIP) vs metaheuristic (GA/PSO) vs simulation — ข้อใหญ่สุด
- **เชิงเส้น + deterministic + เล็ก-กลาง** → **LP/Simplex/MIP** (Excel Solver, OR-Tools, GUROBI) — รับประกัน optimal = **default**
- **nonlinear / combinatorial / ใหญ่มาก (NP-Hard เช่น จัดเวร, VRP, TSP)** → **metaheuristic (GA/PSO/ACO)** — ได้ "ดีพอ" ไม่รับประกัน optimal
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
- **Binding** (slack=0) → SP>0 → เพิ่มทรัพยากรช่วยได้ (ลงทุนถ้าราคา < SP) · **Non-binding** (มี slack) → SP=0 → เพิ่มไม่ช่วย อย่าซื้อ
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
