#!/usr/bin/env python3
"""แปลงไฟล์รายงานที่ export จาก FusionSolar ให้เป็น data/solar.json

วางไฟล์ .xlsx ไว้ในโฟลเดอร์ data/solar/reports/ (ชื่อไฟล์อะไรก็ได้)
- Plant Report รายวัน   → ข้อมูลรายชั่วโมง: ผลิต (PV Yield), ส่งออก (Export), ซื้อเข้า (Import), รายได้
- Inverter Report รายวัน → ผลิตวันนี้ / สะสม / กำลังสูงสุด ของแต่ละอินเวอร์เตอร์ (วันที่อ่านจากชื่อไฟล์ เช่น _16-10-2026)

สคริปต์อ่านทุกไฟล์ใหม่ทุกครั้ง ถ้าวันเดียวกันมีหลายไฟล์ (เช่น export ตอนสายแล้ว export ซ้ำตอนเย็น)
จะใช้ไฟล์ที่มีข้อมูลครบกว่า ไม่ต้องลบไฟล์เก่า

    pip install openpyxl
    python3 scripts/import_solar_reports.py
"""
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "data" / "solar" / "reports"
OUT = ROOT / "data" / "solar.json"
BKK = timezone(timedelta(hours=7))


def num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def norm(h):
    return re.sub(r"[^a-z0-9]", "", str(h or "").lower())


def rows_of(path):
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True).worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def find_header(rows, must):
    for i, r in enumerate(rows[:10]):
        keys = [norm(c) for c in r]
        if all(any(m in k for k in keys) for m in must):
            return i, keys
    return None, None


def col(keys, *names):
    for n in names:
        for i, k in enumerate(keys):
            if k.startswith(n):
                return i
    return None


def parse_plant(rows):
    """คืน {date: {"hours": {hh: {...}}}}"""
    i, keys = find_header(rows, ["statisticalperiod", "pvyield"])
    if i is None:
        return None
    c_t = col(keys, "statisticalperiod")
    c_pv = col(keys, "pvyield")
    c_inv = col(keys, "inverteryield")
    c_exp = col(keys, "export")
    c_imp = col(keys, "import")
    c_rev = col(keys, "revenue")
    c_rad = col(keys, "globalirradiation")
    days = defaultdict(dict)
    for r in rows[i + 1:]:
        t = r[c_t] if c_t is not None and c_t < len(r) else None
        if isinstance(t, datetime):
            dt = t
        else:
            try:
                dt = datetime.strptime(str(t).strip()[:16], "%Y-%m-%d %H:%M")
            except ValueError:
                continue
        get = lambda c: num(r[c]) if c is not None and c < len(r) else None  # noqa: E731
        pv = get(c_pv)
        if pv is None:
            pv = get(c_inv)
        days[dt.strftime("%Y-%m-%d")][dt.strftime("%H:00")] = {
            "pv_kwh": pv, "export_kwh": get(c_exp), "import_kwh": get(c_imp),
            "revenue": get(c_rev), "radiation": get(c_rad),
        }
    return days


def parse_inverters(rows):
    i, keys = find_header(rows, ["devicename", "totalyield"])
    if i is None:
        return None
    c_n, c_y, c_t = col(keys, "devicename"), col(keys, "yield"), col(keys, "totalyield")
    c_p, c_h, c_cap = col(keys, "peakacpower"), col(keys, "gridconnectionduration"), col(keys, "totalstringcapacity")
    out = []
    for r in rows[i + 1:]:
        if c_n is None or c_n >= len(r) or not r[c_n]:
            continue
        g = lambda c: num(r[c]) if c is not None and c < len(r) else None  # noqa: E731
        out.append({"name": str(r[c_n]).strip(), "day_kwh": g(c_y), "total_kwh": g(c_t),
                    "peak_kw": g(c_p), "hours": g(c_h), "capacity_kwp": g(c_cap)})
    return out


def date_from_name(name):
    m = re.search(r"(\d{1,2})-(\d{1,2})-(\d{4})", name)
    if m:
        d, mo, y = map(int, m.groups())
        return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return "-".join(m.groups()) if m else None


def filled(hours):
    return sum(1 for h in hours.values() if h.get("pv_kwh") is not None or h.get("import_kwh") is not None)


def r2(x):
    return None if x is None else round(x, 2)


def main():
    files = sorted(REPORTS.glob("*.xlsx")) if REPORTS.exists() else []
    if not files:
        sys.exit(f"ไม่พบไฟล์ .xlsx ใน {REPORTS}")

    plant = {}      # date -> hours
    invs = {}       # date -> list
    skipped = []
    for f in files:
        try:
            rows = rows_of(f)
        except Exception as e:  # noqa: BLE001
            skipped.append(f"{f.name}: เปิดไม่ได้ ({e})")
            continue
        p = parse_plant(rows)
        if p:
            for d, hours in p.items():
                old = plant.get(d)
                if old is None or (filled(hours), sum(h["pv_kwh"] or 0 for h in hours.values())) >= \
                        (filled(old), sum(h["pv_kwh"] or 0 for h in old.values())):
                    plant[d] = hours
            continue
        inv = parse_inverters(rows)
        if inv:
            d = date_from_name(f.name)
            if not d:
                skipped.append(f"{f.name}: Inverter Report แต่หาวันที่จากชื่อไฟล์ไม่เจอ")
                continue
            tot = sum(x["total_kwh"] or 0 for x in inv)
            if d not in invs or tot >= sum(x["total_kwh"] or 0 for x in invs[d]):
                invs[d] = inv
            continue
        skipped.append(f"{f.name}: ไม่รู้จักรูปแบบไฟล์ (ต้องเป็น Plant Report หรือ Inverter Report)")

    if not plant and not invs:
        sys.exit("ไม่มีไฟล์ที่อ่านได้:\n  " + "\n  ".join(skipped))

    # สรุปรายวัน
    daily = []
    for d in sorted(plant):
        hs = plant[d]
        pv = sum(h["pv_kwh"] or 0 for h in hs.values())
        exp = sum(h["export_kwh"] or 0 for h in hs.values())
        imp = sum(h["import_kwh"] or 0 for h in hs.values())
        has_meter = any(h["import_kwh"] is not None or h["export_kwh"] is not None for h in hs.values())
        last = max((h for h, v in hs.items() if v.get("pv_kwh") is not None or v.get("import_kwh") is not None), default=None)
        daily.append({
            "d": d, "pv_kwh": r2(pv), "export_kwh": r2(exp) if has_meter else None,
            "import_kwh": r2(imp) if has_meter else None,
            "use_kwh": r2(pv - exp + imp) if has_meter else None,
            "revenue": r2(sum(h["revenue"] or 0 for h in hs.values())),
            "last_hour": last, "complete": last == "23:00",
        })

    latest = max(list(plant) + list(invs))
    hs = plant.get(latest, {})
    hourly = []
    for h in sorted(hs):
        v = hs[h]
        meter = v["import_kwh"] is not None or v["export_kwh"] is not None
        pv = v["pv_kwh"] or 0
        hourly.append({
            "h": h, "pv_kwh": r2(v["pv_kwh"]),
            "use_kwh": r2(pv - (v["export_kwh"] or 0) + (v["import_kwh"] or 0)) if meter else None,
            "grid_kwh": r2(v["export_kwh"]), "import_kwh": r2(v["import_kwh"]),
        })
    # ตัดชั่วโมงท้ายที่ยังไม่มีข้อมูล (export ระหว่างวัน)
    while hourly and hourly[-1]["pv_kwh"] is None and hourly[-1]["import_kwh"] is None:
        hourly.pop()

    monthly = defaultdict(lambda: {"pv_kwh": 0, "days": 0})
    for r in daily:
        m = monthly[r["d"][:7]]
        m["pv_kwh"] += r["pv_kwh"] or 0
        m["days"] += 1

    today = next((r for r in daily if r["d"] == latest), None)
    inv_latest = invs.get(latest) or (invs[max(invs)] if invs else [])
    month_key = latest[:7]

    out = {
        "source": "report",
        "sample": False,
        "plant": "รพ.พระทองคำ",
        "report_date": latest,
        "report_complete": bool(today and today["complete"]),
        "report_last_hour": today["last_hour"] if today else None,
        "updated": datetime.now(BKK).isoformat(timespec="minutes"),
        "peak_kw": r2(sum(x["peak_kw"] or 0 for x in inv_latest)) if inv_latest else None,
        "realtime": {
            "day_kwh": today["pv_kwh"] if today else r2(sum(x["day_kwh"] or 0 for x in inv_latest)),
            "month_kwh": r2(monthly[month_key]["pv_kwh"]) if month_key in monthly else None,
            "month_days": monthly[month_key]["days"] if month_key in monthly else 0,
            "total_kwh": r2(sum(x["total_kwh"] or 0 for x in inv_latest)) if inv_latest else None,
            "day_export_kwh": today["export_kwh"] if today else None,
            "day_income": today["revenue"] if today else None,
        },
        "hourly_date": latest,
        "hourly": hourly,
        "daily": daily[-62:],
        "monthly": [{"m": k, "pv_kwh": r2(v["pv_kwh"]), "days": v["days"]} for k, v in sorted(monthly.items())],
        "inverters": [{"name": x["name"], "day_kwh": r2(x["day_kwh"]), "total_kwh": r2(x["total_kwh"]),
                       "peak_kw": r2(x["peak_kw"]), "hours": r2(x["hours"])} for x in inv_latest],
        "errors": skipped,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(daily)} วัน, รายงานล่าสุด {latest}"
          + (f" (ถึง {out['report_last_hour']})" if out["report_last_hour"] else ""))
    for s in skipped:
        print("  ข้าม:", s)


if __name__ == "__main__":
    main()
