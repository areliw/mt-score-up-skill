# Design drafts — ระบบที่กำลังออกแบบ (ยังไม่ implement)

> เอกสารในโฟลเดอร์นี้ = **ดราฟต์การออกแบบ** ของระบบที่จะทำให้คลังสกิล *วัดผลได้ + ดูแลตัวเอง*.
> **ยังไม่ถูก implement** — track ไว้เพื่อความโปร่งใส + iterate. สถานะคุณภาพจริงของสกิลตอนนี้ยังใช้ 3-tier (`draft`/`semi-stable`/`stable`) ตาม [`../../CHANGELOG.md`](../../CHANGELOG.md)

| ไฟล์ | คือ | สถานะ |
|---|---|---|
| [maturity-ladder.md](./maturity-ladder.md) | 10-tier วัดคุณภาพสกิล (hash-currency gate) | design |
| [contribution-credit.md](./contribution-credit.md) | นับ "ภูมิที่เก็บได้" (U) เป็น north-star tier | design |
| [roadmap.md](./roadmap.md) | wave W0–W5 ที่จะทำ | living |
| [catalog-steward.md](./catalog-steward.md) | loop ดูแลคลังตัวเอง (detect→propose→gate→apply) | design |

ออกแบบ 2026-06-15. ดู [`roadmap.md`](./roadmap.md) สำหรับลำดับ wave + dependency. ข้อเสนอ/ติชม → เปิด issue ได้
