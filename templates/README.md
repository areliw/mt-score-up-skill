# Templates

เก็บ **.docx templates** สำหรับ WI ตาม hospital-specific format

## ที่ต้องเพิ่ม (ผู้สร้างกรอกเอง — ลบข้อมูล identifying ก่อน)

| File | สำหรับ | สถานะ |
|---|---|---|
| `generic-iso15189.docx` | ทั่วไป ISO 15189:2022 + ISO 15190:2020 (header/footer สำเนา ลายเซ็น) | ⏳ TODO |
| `hospital-b-bloodbank.docx` | รพ.ตัวอย่าง B Blood Bank | ⏳ TODO |
| `hospital-b-microbiology.docx` | รพ.ตัวอย่าง B Micro | ⏳ TODO |
| `hospital-c-bloodbank.docx` | รพ.ตัวอย่าง C Blood Bank | ⏳ TODO |
| `hospital-c-microbiology.docx` | รพ.ตัวอย่าง C Micro | ⏳ TODO |

## วิธีเตรียม template

1. **เอา WI จริง 1 ตัว** ที่ approve แล้ว
2. **ลบข้อมูล identifying:**
   - ชื่อคนไข้ / HN / MRN
   - ชื่อบุคลากรเฉพาะเจาะจง (เปลี่ยนเป็น `{{author_name}}`, `{{reviewer_name}}`)
   - หมายเลขเอกสารเฉพาะ (เปลี่ยนเป็น `{{doc_number}}`)
3. **เก็บแค่ structure + header/footer + signature box**
4. **Save เป็น .docx** ใน folder นี้

## ใช้ template ยังไง

หลัง paste system prompt ใน Claude.ai → upload .docx template → AI จะ match format

## Contribution

ถ้าคุณมี template โรงพยาบาลอื่น → fork repo + เพิ่ม → submit PR
