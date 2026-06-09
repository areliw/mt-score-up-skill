/**
 * MT Score UP! — สร้าง "Google Form ส่งความรู้เข้าคลังสกิล" อัตโนมัติ
 * ------------------------------------------------------------------
 * ฟอร์มนี้คือ no-GitHub contribution lane ที่อ้างถึงใน CONTRIBUTING.md / README.md
 * (ฟิลด์ตรงกับ "ตัวช่วยร่างด้วย AI" — เรื่อง / สถานการณ์ / ตัวเลือก / กับดัก + privacy gate)
 *
 * วิธีใช้ (ครั้งเดียว ~30 วินาที):
 *   1. เปิด  https://script.google.com  → New project
 *   2. ลบโค้ดเดิม → วางไฟล์นี้ทั้งหมด → กด Save (💾)
 *   3. กด Run ▶ (ฟังก์ชัน createContributionForm) → Google ถาม authorize → Allow
 *   4. ดูแท็บ "Execution log" ด้านล่าง → คัดลอก  FORM_URL (responder)  มาให้ผมเสียบเข้า repo
 *      (EDIT_URL เก็บไว้แก้ฟอร์มเองทีหลัง)
 *
 * ไม่ต้อง login เพื่อตอบ · ไม่เก็บอีเมลอัตโนมัติ (มีช่องอีเมลให้กรอกเองแบบไม่บังคับ)
 */
function createContributionForm() {
  var form = FormApp.create('MT Score UP! — ส่งความรู้/วิจารณญาณเข้าคลังสกิล');

  form.setDescription(
    '📚 แชร์ "วิจารณญาณหน้างาน" ของคุณเข้าคลังสกิล MT Score UP! — ไม่ต้องเขียนให้สวย ' +
    'แค่บอก "เลือกอะไรเมื่อไหร่ + กับดักที่คนพลาด" มา เดี๋ยว maintainer + AI เรียบเรียงเป็น skill ให้ (มี credit ชื่อคุณ)\n\n' +
    '⚠️ เพื่อการศึกษา/ช่วยคิดเท่านั้น — ไม่ใช่คำสั่งวินิจฉัย/รักษา\n' +
    '🔒 สำคัญ: ลบข้อมูลคนไข้ / HN / ชื่อเฉพาะบุคคล / ความลับ รพ. ออกให้หมดก่อนส่ง (ส่งเฉพาะ generic procedure)'
  );

  // ไม่บังคับ login / ไม่เก็บอีเมลอัตโนมัติ (กันคนไม่มีบัญชี Google ตอบไม่ได้)
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  try { form.setRequireLogin(false); } catch (e) { /* consumer account: no-op */ }

  // --- ข้อมูลผู้ส่ง (ไม่บังคับ) ---
  form.addTextItem()
      .setTitle('ชื่อ (สำหรับ credit)')
      .setHelpText('อยากให้ลงชื่อใน CONTRIBUTORS.md ว่าอะไร — เว้นว่างได้ถ้าอยากไม่ระบุชื่อ');

  form.addTextItem()
      .setTitle('โรงพยาบาล / สังกัด')
      .setHelpText('ไม่บังคับ');

  form.addTextItem()
      .setTitle('อีเมลติดต่อกลับ')
      .setHelpText('ไม่บังคับ — ใส่ถ้าอยากให้ maintainer ติดต่อถามต่อ/แจ้งเมื่อขึ้นคลัง');

  // --- เนื้อหาสกิล (บังคับ) ---
  form.addTextItem()
      .setTitle('หัวข้อ / เรื่องของสกิล')
      .setHelpText('เช่น "อ่าน ABO discrepancy", "เลือก media เพาะเชื้อ", "QC reject เมื่อไหร่"')
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('สถานการณ์ที่ต้องตัดสินใจหน้างาน')
      .setHelpText('เล่าเคส/จังหวะที่ MT ต้องตัดสินใจ — สถานการณ์สมมุติได้ ห้ามมีข้อมูลคนไข้จริง')
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('ตัวเลือก & เลือกอันไหนเมื่อไหร่')
      .setHelpText('มีทางเลือกอะไรบ้าง และ "เลือกอันไหน เมื่อเงื่อนไขแบบไหน"')
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('กับดักที่คนพลาดบ่อย')
      .setHelpText('สิ่งที่ผู้เชี่ยวชาญรู้แต่มือใหม่ไม่รู้ — จุดที่พลาดแล้วเสียหาย')
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('References / แหล่งอ้างอิง (ถ้ามี)')
      .setHelpText('AABB / CLSI / ISO / guideline / paper — ไม่บังคับ แต่ช่วย verify');

  // --- Privacy gate (บังคับติ๊ก) ---
  var privacy = form.addCheckboxItem();
  privacy.setTitle('ยืนยันก่อนส่ง')
         .setRequired(true)
         .setChoices([
           privacy.createChoice('ฉันได้ลบข้อมูลคนไข้ / HN / ชื่อเฉพาะบุคคล / ความลับโรงพยาบาล ออกหมดแล้ว')
         ]);

  var responderUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();
  var shortUrl = FormApp.openByUrl(editUrl).shortenFormUrl(responderUrl);

  Logger.log('=================================================');
  Logger.log('✅ สร้างฟอร์มสำเร็จ');
  Logger.log('FORM_URL (เอาอันนี้ไปแทนใน 3 จุดของ repo):');
  Logger.log('   ' + responderUrl);
  Logger.log('FORM_URL (แบบสั้น): ' + shortUrl);
  Logger.log('EDIT_URL (เก็บไว้แก้ฟอร์มเอง): ' + editUrl);
  Logger.log('=================================================');

  return { responderUrl: responderUrl, shortUrl: shortUrl, editUrl: editUrl };
}
