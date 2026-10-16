# 🏥 Hospital Dashboard

Dashboard ภาพรวมโรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา พร้อมลิงก์ข้อมูลจังหวัดนครราชสีมา
https://suvoak-web.github.io/hospital-dashboard/
## ข้อมูลที่แสดง

- **ผู้ป่วย** — OPD / IPD รายวัน แยกตามแผนก
- **เตียง** — สถานะว่าง/เต็ม แยกตามวอร์ด
- **บุคลากร** — แพทย์ พยาบาล เจ้าหน้าที่ที่ปฏิบัติงานวันนี้
- **ระยะเวลารอคอย** — แยกตามแผนก พร้อมสีเตือน
- **การเงิน** — รายรับ/รายจ่าย เงินพึงรับ/พึงจ่าย ระหว่างโรงพยาบาล
- **อายุลูกหนี้** (`ar_aging.html`) — ลูกหนี้ค่ารักษาแยกอายุ/สิทธิ เทียบ รพ.ในจังหวัด อัปเดตโดยลากไฟล์ Excel อายุลูกหนี้ภาพจังหวัดมาวางในหน้า (อ่านในเบราว์เซอร์ ไม่ส่งไฟล์ออกไปไหน)

## ลิงก์จังหวัดนครราชสีมา

| ระบบ | URL |
|------|-----|
| ตัวชี้วัดสาธารณสุข | https://apikorat.moph.go.th/home/dashboard |
| ระยะเวลารอคอย R9 | https://www.r9health.net/servicetime/ |

## วิธีใช้งาน

เปิดไฟล์ `index.html` ได้เลย ไม่ต้องติดตั้งอะไรเพิ่ม

## Deploy ด้วย GitHub Pages

1. Push โค้ดขึ้น GitHub
2. ไปที่ Settings → Pages
3. เลือก Source: `main` branch, folder `/root`
4. Save → รอสักครู่ ได้ URL สาธารณะ

## ☀️ พลังงานแสงอาทิตย์ (`solar_dashboard.html`)

ดึงข้อมูลจาก Huawei FusionSolar อัตโนมัติทุกชั่วโมง 06:00–19:00 ผ่าน GitHub Actions (`.github/workflows/solar.yml` → `scripts/fetch_solar.py` → `data/solar.json`)
จนกว่าจะตั้งค่าเสร็จ หน้าเว็บจะแสดงข้อมูลตัวอย่างพร้อมป้ายบอก

**ตั้งค่าครั้งแรก**
1. ล็อกอิน FusionSolar ด้วยบัญชีผู้ดูแลบริษัท → System → Company Management → Northbound Management → Add
   ตั้งชื่อผู้ใช้ (ต้องไม่ซ้ำบัญชีเว็บ) และรหัสผ่าน เปิด Basic APIs และเลือกสถานีของ รพ.
2. GitHub repo → Settings → Secrets and variables → Actions → New repository secret
   - `FUSIONSOLAR_USER` = ชื่อผู้ใช้ Northbound
   - `FUSIONSOLAR_SYSTEM_CODE` = รหัสผ่าน Northbound
3. (ถ้าจำเป็น) แท็บ Variables: `FUSIONSOLAR_BASE` ถ้าบัญชีอยู่โดเมนอื่น (ค่าเริ่มต้น `https://intl.fusionsolar.huawei.com`), `FUSIONSOLAR_STATION` (ค่าเริ่มต้น `NE=76434926`)
4. Actions → "อัปเดตข้อมูลโซลาร์" → Run workflow เพื่อทดสอบ

ค่าไฟต่อหน่วย (`TARIFF`) และค่า CO₂ (`EF`) แก้ได้ที่ต้นสคริปต์ใน `solar_dashboard.html` (และ `TARIFF` ใน `index.html`)
หมายเหตุ: กราฟเทียบ "ไฟที่ รพ. ใช้" จะแสดงเมื่อมีมิเตอร์วัดไฟเชื่อมกับ FusionSolar เท่านั้น
