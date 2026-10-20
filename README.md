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

## ☀️ Solar PV อาคารอุบัติเหตุและฉุกเฉิน (`solar_dashboard.html`)

ข้อมูลมาจากรายงานที่ export จาก Huawei FusionSolar (ใช้สิทธิ์ผู้ใช้ทั่วไปได้ ไม่ต้องเป็นผู้ดูแล)

**อัปเดตข้อมูลประจำวัน (ประมาณ 1 นาที)**
1. ใน FusionSolar export **Plant Report** และ **Inverter Report** แบบรายวัน เป็น .xlsx — แนะนำให้ export หลังแดดหมด (ประมาณ 19:00 น.) จะได้ข้อมูลครบวัน
2. กดปุ่ม **อัปโหลดรายงาน Excel** บนหน้าโซลาร์ (หรือเปิดโฟลเดอร์ [`data/solar/reports`](data/solar/reports) → **Add file → Upload files**) → ลากไฟล์มาวาง → **Commit changes**
3. รอ 1–2 นาที ระบบ (`.github/workflows/solar_reports.yml`) จะแปลงไฟล์เป็น `data/solar.json` ให้เอง แล้วหน้าเว็บจะแสดงข้อมูลใหม่

ถ้าส่งแค่ Inverter Report ระบบจะนับยอดผลิตให้ แต่ไฟที่อาคารใช้/ส่งไปอาคารอื่นต้องมาจาก Plant Report · ไม่ต้องเปลี่ยนชื่อไฟล์ และไม่ต้องลบไฟล์เก่า (ถ้าวันเดียวกันมีหลายไฟล์ จะใช้ไฟล์ที่ข้อมูลครบกว่า) วันที่ของ Inverter Report อ่านจากชื่อไฟล์ เช่น `_16-10-2026`
แปลงเองในเครื่องได้ด้วย `pip install openpyxl && python3 scripts/import_solar_reports.py`

**มิเตอร์หลักของการไฟฟ้า (AMI)** — export "Billing Monthly kWh Report" รายเดือนจากระบบ AMI ของ PEA (.xlsx ข้อมูลทุก 15 นาที) แล้วอัปโหลดเข้าโฟลเดอร์เดียวกัน หน้าเว็บจะแสดงส่วน "ไฟฟ้าทั้งโรงพยาบาล": ไฟที่ใช้ทั้ง รพ. (= ซื้อจาก PEA + โซลาร์), สัดส่วนที่โซลาร์ช่วย, Peak/Off-Peak, ความต้องการไฟสูงสุด และรูปแบบการซื้อไฟรายชั่วโมง

**ตัวเลขที่คำนวณ**
- ไฟที่อาคารใช้ = PV Yield − Export + Import (รายชั่วโมงจาก Plant Report)
- ค่าไฟที่ประหยัด = PV Yield ทั้งหมด × `TARIFF` (มิเตอร์หลักไม่เคยลดถึงศูนย์ ไฟที่อาคาร ER "Export" จึงถูกอาคารอื่นใน รพ. ใช้ต่อ ไม่ได้ขายคืนการไฟฟ้า)
- CO₂ = พลังงานสะสม (Total Yield ของอินเวอร์เตอร์) × `EF`

แก้ `TARIFF` (บาท/kWh) และ `EF` ได้ที่ต้นสคริปต์ใน `solar_dashboard.html` (และ `TARIFF` ใน `index.html`)

**ทางเลือก: ดึงอัตโนมัติผ่าน API** — ถ้าผู้ดูแลระบบ FusionSolar สร้างบัญชี Northbound ให้ (System → Company Management → Northbound Management)
ใส่ secrets `FUSIONSOLAR_USER` / `FUSIONSOLAR_SYSTEM_CODE` แล้ว `.github/workflows/solar.yml` จะดึงข้อมูลเองวันละครั้ง (19:35 น.) โดยไม่ต้องอัปโหลดไฟล์ ถ้ายังไม่ใส่ secrets workflow นี้จะข้ามไปเฉย ๆ
