#!/usr/bin/env python3
"""ดึงข้อมูลโซลาร์เซลล์จาก Huawei FusionSolar (Northbound API) แล้วเขียนลง data/solar.json

ใช้ได้ทั้งจาก GitHub Actions และรันเองในเครื่อง:
    FUSIONSOLAR_USER=... FUSIONSOLAR_SYSTEM_CODE=... python3 scripts/fetch_solar.py

ตัวแปรสภาพแวดล้อม
    FUSIONSOLAR_USER         ชื่อผู้ใช้ Northbound (ไม่ใช่บัญชีล็อกอินหน้าเว็บ)
    FUSIONSOLAR_SYSTEM_CODE  รหัสผ่านของผู้ใช้ Northbound
    FUSIONSOLAR_BASE         โดเมน API (ค่าเริ่มต้น https://intl.fusionsolar.huawei.com)
    FUSIONSOLAR_STATION      รหัสสถานี (ค่าเริ่มต้น NE=76434926 จากลิงก์ของ รพ.)

ไม่ต้องติดตั้งไลบรารีเพิ่ม ใช้แค่ Python มาตรฐาน
ถ้าเรียก API ส่วนไหนไม่สำเร็จ (เช่น เกินโควตา) จะเก็บค่าเดิมในไฟล์ไว้ ไม่ทำให้หน้าเว็บว่าง
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BKK = timezone(timedelta(hours=7))
OUT = Path(__file__).resolve().parent.parent / "data" / "solar.json"

# ใช้ `or` เพื่อให้ค่าว่างจาก GitHub vars ที่ยังไม่ได้ตั้ง กลับไปใช้ค่าเริ่มต้น
BASE = (os.environ.get("FUSIONSOLAR_BASE") or "https://intl.fusionsolar.huawei.com").rstrip("/")
STATION = os.environ.get("FUSIONSOLAR_STATION") or "NE=76434926"
USER = os.environ.get("FUSIONSOLAR_USER", "")
CODE = os.environ.get("FUSIONSOLAR_SYSTEM_CODE", "")


class Api:
    def __init__(self):
        self.token = None

    def _post(self, path, body):
        req = urllib.request.Request(
            BASE + path,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", **({"XSRF-TOKEN": self.token} if self.token else {})},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.loads(r.read().decode() or "{}")
            return r.headers, payload

    def login(self):
        headers, data = self._post("/thirdData/login", {"userName": USER, "systemCode": CODE})
        if not data.get("success"):
            raise RuntimeError(f"login failed: failCode={data.get('failCode')} message={data.get('message')}")
        self.token = headers.get("xsrf-token") or headers.get("XSRF-TOKEN")
        if not self.token:
            raise RuntimeError("login ok but no xsrf-token header returned")

    def call(self, path, body):
        _, data = self._post(path, body)
        if not data.get("success"):
            raise RuntimeError(f"{path}: failCode={data.get('failCode')} message={data.get('message')}")
        return data.get("data")


def num(v):
    try:
        return round(float(v), 2)
    except (TypeError, ValueError):
        return None


def ms(dt):
    return int(dt.timestamp() * 1000)


def main():
    if not USER or not CODE:
        # ยังไม่มีบัญชี API — ใช้วิธีอัปโหลดรายงาน (import_solar_reports.py) แทน จึงจบเฉย ๆ ไม่ให้ workflow ขึ้นว่าล้มเหลว
        print("ยังไม่ได้ตั้งค่า FUSIONSOLAR_USER / FUSIONSOLAR_SYSTEM_CODE — ข้ามการดึงผ่าน API")
        return

    old = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
        except ValueError:
            old = {}
    out = {k: v for k, v in old.items() if k != "sample"}
    errors = []

    api = Api()
    api.login()
    now = datetime.now(BKK)

    # 1) ภาพรวมวันนี้/เดือนนี้/สะสม
    try:
        rows = api.call("/thirdData/getStationRealKpi", {"stationCodes": STATION}) or []
        m = rows[0]["dataItemMap"] if rows else {}
        out["realtime"] = {
            "day_kwh": num(m.get("day_power")),
            "month_kwh": num(m.get("month_power")),
            "total_kwh": num(m.get("total_power")),
            "day_income": num(m.get("day_income")),
            "total_income": num(m.get("total_income")),
            "health": m.get("real_health_state"),  # 1 ตัดการเชื่อมต่อ, 2 ผิดปกติ, 3 ปกติ
        }
    except Exception as e:  # noqa: BLE001
        errors.append(str(e))

    # 2) รายชั่วโมงของวันนี้ (ผลิต / ใช้ไฟ ถ้ามีมิเตอร์)
    try:
        rows = api.call("/thirdData/getKpiStationHour", {"stationCodes": STATION, "collectTime": ms(now)}) or []
        hourly = []
        for r in sorted(rows, key=lambda x: x.get("collectTime", 0)):
            t = datetime.fromtimestamp(r["collectTime"] / 1000, BKK)
            d = r.get("dataItemMap", {})
            hourly.append({
                "h": t.strftime("%H:00"),
                "pv_kwh": num(d.get("inverter_power")),
                "use_kwh": num(d.get("use_power")),
                "grid_kwh": num(d.get("ongrid_power")),
                "radiation": num(d.get("radiation_intensity")),
            })
        out["hourly"] = hourly
        out["hourly_date"] = now.strftime("%Y-%m-%d")
    except Exception as e:  # noqa: BLE001
        errors.append(str(e))

    # 3) รายเดือนของปีนี้
    try:
        rows = api.call("/thirdData/getKpiStationMonth", {"stationCodes": STATION, "collectTime": ms(now)}) or []
        monthly = []
        for r in sorted(rows, key=lambda x: x.get("collectTime", 0)):
            t = datetime.fromtimestamp(r["collectTime"] / 1000, BKK)
            d = r.get("dataItemMap", {})
            monthly.append({
                "m": t.strftime("%Y-%m"),
                "pv_kwh": num(d.get("inverter_power")),
                "use_kwh": num(d.get("use_power")),
                "income": num(d.get("power_profit")),
                "co2_t": num(d.get("reduction_total_co2")),
            })
        out["monthly"] = monthly
    except Exception as e:  # noqa: BLE001
        errors.append(str(e))

    # 4) อินเวอร์เตอร์: กำลังผลิตขณะนี้และสถานะ
    try:
        devs = api.call("/thirdData/getDevList", {"stationCodes": STATION}) or []
        inv = [d for d in devs if d.get("devTypeId") == 1]
        if inv:
            rows = api.call("/thirdData/getDevRealKpi", {"devIds": ",".join(str(d["id"]) for d in inv), "devTypeId": 1}) or []
            names = {d["id"]: d.get("devName") for d in inv}
            out["inverters"] = [{
                "name": names.get(r.get("devId"), str(r.get("devId"))),
                "kw": num(r.get("dataItemMap", {}).get("active_power")),
                "on": r.get("dataItemMap", {}).get("run_state") == 1,
            } for r in rows]
            out["power_kw"] = round(sum(i["kw"] or 0 for i in out["inverters"]), 2)
    except Exception as e:  # noqa: BLE001
        errors.append(str(e))

    out["station"] = STATION
    out["updated"] = now.isoformat(timespec="minutes")
    out["errors"] = errors
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(errors)} error(s))")
    for e in errors:
        print("  -", e)


if __name__ == "__main__":
    main()
