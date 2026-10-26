#!/usr/bin/env python3
"""แปลงไฟล์รายงานที่ export จาก FusionSolar ให้เป็น data/solar.json

วางไฟล์ .xlsx ไว้ในโฟลเดอร์ data/solar/reports/ (ชื่อไฟล์อะไรก็ได้) รองรับ 4 แบบ
- Plant Report รายวัน    → แถวละ 1 ชั่วโมง  (ผลิต, ส่งออก, ซื้อเข้า)          ใช้ทำกราฟรายชั่วโมง
- Plant Report รายเดือน  → แถวละ 1 วัน     (ผลิต, ใช้ไฟ, ใช้เอง, กำลังสูงสุด, CO₂) ใช้ทำกราฟรายวัน/รายเดือน
- Inverter Report รายวัน  → ผลิต/สะสม/กำลังสูงสุด ของแต่ละเครื่อง  (วันที่จากชื่อไฟล์ เช่น _16-10-2026)
- Inverter Report รายเดือน → ผลิตของแต่ละเครื่องในเดือนนั้น         (เดือนจากชื่อไฟล์ เช่น _04-2026)

สคริปต์อ่านทุกไฟล์ใหม่ทุกครั้ง ถ้าข้อมูลวันเดียวกันมาจากหลายไฟล์ จะใช้ชุดที่ครบกว่า ไม่ต้องลบไฟล์เก่า

    pip install openpyxl
    python3 scripts/import_solar_reports.py
"""
import calendar
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


def r2(x):
    return None if x is None else round(x, 2)


def norm(h):
    return re.sub(r"[^a-z0-9]", "", str(h or "").lower())


def rows_of(path):
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True).worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def find_header(rows, must, limit=10):
    for i, r in enumerate(rows[:limit]):
        keys = [norm(c) for c in r]
        if all(any(k.startswith(m) for k in keys) for m in must):
            return i, keys
    return None, None


def col(keys, *names):
    for n in names:
        for i, k in enumerate(keys):
            if k.startswith(n):
                return i
    return None


def getter(row, keys):
    def g(*names):
        c = col(keys, *names)
        return num(row[c]) if c is not None and c < len(row) else None
    return g


def parse_time(v):
    if isinstance(v, datetime):
        return v, len(str(v)) > 10
    s = str(v or "").strip()
    for fmt, hourly in (("%Y-%m-%d %H:%M:%S", True), ("%Y-%m-%d %H:%M", True), ("%Y-%m-%d", False)):
        try:
            return datetime.strptime(s, fmt), hourly
        except ValueError:
            pass
    return None, None


def parse_plant(rows):
    """คืน (hourly_days, daily_rows) — hourly_days: {date: {HH:00: {...}}}, daily_rows: {date: {...}}"""
    i, keys = find_header(rows, ["statisticalperiod", "pvyield"])
    if i is None:
        return None
    c_t = col(keys, "statisticalperiod")
    hourly, daily = defaultdict(dict), {}
    for r in rows[i + 1:]:
        dt, is_hour = parse_time(r[c_t] if c_t < len(r) else None)
        if dt is None:
            continue
        g = getter(r, keys)
        pv = g("pvyield")
        if pv is None:
            pv = g("inverteryield")
        rec = {"pv_kwh": pv, "export_kwh": g("export"), "import_kwh": g("import"), "revenue": g("revenue")}
        if is_hour:
            hourly[dt.strftime("%Y-%m-%d")][dt.strftime("%H:00")] = rec
        else:
            rec.update({"use_kwh": g("consumption"), "self_kwh": g("selfconsumptionkwh"),
                        "peak_kw": g("peakpower"), "co2_t": g("co2avoided", "coavoided"), "total_kwh": g("totalyield"),
                        "irradiation": g("globalirradiation")})
            if pv is not None or rec["use_kwh"] is not None:
                daily[dt.strftime("%Y-%m-%d")] = rec
    return hourly, daily


def parse_inverters(rows):
    i, keys = find_header(rows, ["devicename", "yield"])
    if i is None:
        return None
    c_n = col(keys, "devicename")
    out = []
    for r in rows[i + 1:]:
        if c_n >= len(r) or not r[c_n]:
            continue
        g = getter(r, keys)
        out.append({"name": str(r[c_n]).strip(), "kwh": g("yield"), "total_kwh": g("totalyield"),
                    "peak_kw": g("peakacpower"), "hours": g("gridconnectionduration")})
    return out


def parse_ami(rows):
    """มิเตอร์ AMI ของการไฟฟ้า (Billing Monthly kWh Report) → {(date, HH:MM): (kwh, is_peak)} ช่วงละ 15 นาที"""
    head = " ".join(str(c) for r in rows[:12] for c in r if c)
    i, keys = find_header(rows, ["time", "ratea", "total"], limit=60)
    if i is None:
        return None
    info = {"meter": None, "tariff": None}
    for r in rows[:i]:
        cells = [str(c).strip() if c is not None else "" for c in r]
        for j, c in enumerate(cells):
            nxt = next((x for x in cells[j + 1:] if x), None)
            if c.startswith("Meter No") and nxt:
                info["meter"] = nxt
            if c.startswith("Tariff") and nxt:
                info["tariff"] = nxt
    c_t, c_a, c_tot = col(keys, "time"), col(keys, "ratea"), col(keys, "total")
    out = {}
    for r in rows[i + 1:]:
        t = str(r[c_t] or "").strip()
        mt = re.match(r"(\d{2})/(\d{2})/(\d{4}) (\d{2})[.:](\d{2})", t)
        if not mt:
            continue
        v = num(r[c_tot]) if c_tot < len(r) else None
        if v is None:
            continue
        d, mo, y, hh, mm = map(int, mt.groups())
        end = datetime(y, mo, d) + timedelta(hours=hh, minutes=mm)   # เวลาสิ้นสุดช่วง 15 นาที
        start = end - timedelta(minutes=15)
        out[(start.strftime("%Y-%m-%d"), start.strftime("%H:%M"))] = (v, num(r[c_a]) is not None if c_a < len(r) else False)
    return info, out if "Metering" in head or out else None


def period_from_name(name):
    """('day', 'YYYY-MM-DD') หรือ ('month', 'YYYY-MM') จากชื่อไฟล์"""
    m = re.search(r"(?<!\d)(\d{1,2})-(\d{1,2})-(\d{4})(?!\d)", name)
    if m:
        d, mo, y = map(int, m.groups())
        return "day", f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"(?<!\d)(\d{1,2})-(\d{4})(?!\d)", name)
    if m:
        mo, y = map(int, m.groups())
        return "month", f"{y:04d}-{mo:02d}"
    return None, None


def filled(hours):
    return sum(1 for h in hours.values() if h.get("pv_kwh") is not None or h.get("import_kwh") is not None)


def day_from_hours(hs):
    pv = sum(h["pv_kwh"] or 0 for h in hs.values())
    meter = any(h["import_kwh"] is not None or h["export_kwh"] is not None for h in hs.values())
    exp = sum(h["export_kwh"] or 0 for h in hs.values())
    imp = sum(h["import_kwh"] or 0 for h in hs.values())
    last = max((k for k, v in hs.items() if v.get("pv_kwh") is not None or v.get("import_kwh") is not None), default=None)
    return {
        "pv_kwh": pv, "export_kwh": exp if meter else None, "import_kwh": imp if meter else None,
        "use_kwh": pv - exp + imp if meter else None, "self_kwh": pv - exp if meter else None,
        "revenue": sum(h["revenue"] or 0 for h in hs.values()), "last_hour": last, "complete": last == "23:00",
    }


def build_grid(ami, info, solar_daily):
    """สรุปมิเตอร์หลักของ รพ. รวมกับไฟโซลาร์ → ไฟทั้งโรงพยาบาล"""
    first_pv = min(solar_daily) if solar_daily else "0000"
    days = defaultdict(lambda: {"kwh": 0.0, "peak_kwh": 0.0, "n": 0, "max15": 0.0, "max_at": None, "hours": [0.0] * 24})
    for (d, hm), (v, peak) in ami.items():
        x = days[d]
        x["kwh"] += v
        x["n"] += 1
        if peak:
            x["peak_kwh"] += v
        x["hours"][int(hm[:2])] += v
        if v > x["max15"]:
            x["max15"], x["max_at"] = v, hm
    daily = []
    for d in sorted(days):
        x = days[d]
        sd = solar_daily.get(d, {})
        complete = x["n"] >= 96
        rec = {"d": d, "kwh": r2(x["kwh"]), "peak_kwh": r2(x["peak_kwh"]), "off_kwh": r2(x["kwh"] - x["peak_kwh"]),
               "max_kw": r2(x["max15"] * 4), "max_at": x["max_at"], "workday": x["peak_kwh"] > 0, "complete": complete,
               "pv_kwh": r2(sd.get("pv_kwh")) if sd.get("complete") else None, "hours": [r2(h) for h in x["hours"]]}
        rec["total_kwh"] = r2(x["kwh"] + rec["pv_kwh"]) if complete and rec["pv_kwh"] is not None else None
        daily.append(rec)
    months = []
    for m in sorted({x["d"][:7] for x in daily}):
        ds = [x for x in daily if x["d"].startswith(m)]
        both = [x for x in ds if x["total_kwh"] is not None]
        mx = max(ds, key=lambda x: x["max_kw"] or 0)
        months.append({
            "m": m, "days": sum(1 for x in ds if x["complete"]),
            "kwh": r2(sum(x["kwh"] for x in ds)), "peak_kwh": r2(sum(x["peak_kwh"] for x in ds)),
            "off_kwh": r2(sum(x["off_kwh"] for x in ds)), "max_kw": mx["max_kw"], "max_at": f"{mx['d']} {mx['max_at']}",
            "both_days": len(both), "both_grid_kwh": r2(sum(x["kwh"] for x in both)), "both_pv_kwh": r2(sum(x["pv_kwh"] for x in both)),
        })
    def profile(sel):
        ds = [x for x in daily if x["complete"] and sel(x)]
        return [r2(sum(x["hours"][h] for x in ds) / len(ds)) for h in range(24)] if ds else None
    lowest = min(((x["d"], h, x["hours"][h]) for x in daily if x["complete"] for h in range(9, 16)), key=lambda t: t[2], default=None)
    return {
        "meter": info.get("meter"), "tariff": info.get("tariff"),
        "first_date": daily[0]["d"], "last_date": daily[-1]["d"],
        "daily": daily[-400:], "monthly": months,
        "profile_workday": profile(lambda x: x["workday"]), "profile_holiday": profile(lambda x: not x["workday"]),
        "min_midday_kwh_per_h": r2(lowest[2]) if lowest else None,
        "min_15min_kwh": r2(min(v for v, _ in ami.values())),
        # ช่วง 15 นาทีกลางวันที่มิเตอร์หลักแทบเป็นศูนย์ = โซลาร์มากกว่าไฟที่ทั้ง รพ. ใช้ อาจมีไฟไหลออกไปการไฟฟ้า
        "zero_intervals": sum(1 for (d, hm), (v, _) in ami.items() if v <= 0.5 and 8 <= int(hm[:2]) < 17 and d >= first_pv),
        "zero_days": len({d for (d, hm), (v, _) in ami.items() if v <= 0.5 and 8 <= int(hm[:2]) < 17 and d >= first_pv}),
    }


def main():
    files = sorted(REPORTS.glob("*.xlsx")) if REPORTS.exists() else []
    if not files:
        sys.exit(f"ไม่พบไฟล์ .xlsx ใน {REPORTS}")

    hourly_days = {}            # date -> {hour: rec}
    daily_rows = {}             # date -> rec (จากรายงานรายเดือน)
    inv_day = {}                # date -> [..]
    inv_month = {}              # YYYY-MM -> [..]
    ami = {}                    # (date, HH:MM) -> (kwh, is_peak)
    ami_info = {}
    skipped = []
    for f in files:
        try:
            rows = rows_of(f)
        except Exception as e:  # noqa: BLE001
            skipped.append(f"{f.name}: เปิดไม่ได้ ({e})")
            continue
        p = parse_plant(rows)
        if p:
            hours, days = p
            for d, hs in hours.items():
                if d not in hourly_days or filled(hs) >= filled(hourly_days[d]):
                    hourly_days[d] = hs
            daily_rows.update(days)
            continue
        a = parse_ami(rows)
        if a and a[1]:
            ami_info.update({k: v for k, v in a[0].items() if v})
            ami.update(a[1])
            continue
        inv = parse_inverters(rows)
        if inv:
            kind, key = period_from_name(f.name)
            if kind == "day":
                if key not in inv_day or sum(x["kwh"] or 0 for x in inv) >= sum(x["kwh"] or 0 for x in inv_day[key]):
                    inv_day[key] = inv
            elif kind == "month":
                inv_month[key] = inv
            else:
                skipped.append(f"{f.name}: Inverter Report แต่หาวันที่/เดือนจากชื่อไฟล์ไม่เจอ")
            continue
        skipped.append(f"{f.name}: ไม่รู้จักรูปแบบไฟล์ (ต้องเป็น Plant Report, Inverter Report หรือรายงาน AMI ของการไฟฟ้า)")

    if not (hourly_days or daily_rows or inv_day or inv_month):
        sys.exit("ไม่มีไฟล์ที่อ่านได้:\n  " + "\n  ".join(skipped))

    # รวมข้อมูลรายวัน: แถวจากรายงานรายเดือน (สรุปทั้งวัน) มาก่อน ยกเว้นรายงานรายชั่วโมงของวันนั้นครบวัน
    daily = {}
    for d, hs in hourly_days.items():
        daily[d] = day_from_hours(hs)
    today_bkk = datetime.now(BKK).strftime("%Y-%m-%d")
    for d, rec in daily_rows.items():
        if d in daily and daily[d]["complete"]:
            daily[d].update({k: v for k, v in rec.items() if v is not None and k not in daily[d]})
            continue
        hourly_part = daily.get(d)
        if hourly_part and (rec.get("pv_kwh") or 0) < (hourly_part["pv_kwh"] or 0):
            continue  # รายงานรายชั่วโมงของวันนี้ใหม่กว่าแถวในรายงานรายเดือน
        # แถวของวันนี้ในรายงานรายเดือน (export ระหว่างวัน) ยังไม่ครบวัน
        partial = d == today_bkk or (hourly_part is not None and not hourly_part["complete"])
        base = {"last_hour": None if partial else "23:00", "complete": not partial}
        base.update(rec)
        if base.get("self_kwh") is None and base.get("pv_kwh") is not None and base.get("export_kwh") is not None:
            base["self_kwh"] = base["pv_kwh"] - base["export_kwh"]
        daily[d] = base

    # วันที่มีแค่ Inverter Report รายวัน (ไม่มี Plant Report): รู้ยอดผลิต แต่ไม่รู้การใช้ไฟ/ส่งออก
    for d, inv in inv_day.items():
        if d not in daily:
            hrs = max((x["hours"] or 0 for x in inv), default=0)
            daily[d] = {"pv_kwh": sum(x["kwh"] or 0 for x in inv), "export_kwh": None, "import_kwh": None,
                        "use_kwh": None, "self_kwh": None, "peak_kw": sum(x["peak_kw"] or 0 for x in inv) or None,
                        "last_hour": None, "complete": hrs >= 10 or d < datetime.now(BKK).strftime("%Y-%m-%d"),
                        "inverter_only": True}
    dates = sorted(daily)
    latest = max(dates + list(inv_day)) if (dates or inv_day) else None

    # รายเดือน: ต่อเนื่องตั้งแต่เดือนแรกถึงเดือนล่าสุด เดือนที่ไม่มีรายงานเป็น null
    months = sorted({d[:7] for d in dates} | set(inv_month))
    monthly = []
    if months:
        y, m = map(int, months[0].split("-"))
        ly, lm = map(int, months[-1].split("-"))
        while (y, m) <= (ly, lm):
            key = f"{y:04d}-{m:02d}"
            ds = [daily[d] for d in dates if d.startswith(key)]
            rec = {"m": key, "days": len(ds), "days_in_month": calendar.monthrange(y, m)[1]}
            if ds:
                s = lambda k: r2(sum(x.get(k) or 0 for x in ds)) if any(x.get(k) is not None for x in ds) else None  # noqa: E731
                rec.update({"pv_kwh": s("pv_kwh"), "use_kwh": s("use_kwh"), "self_kwh": s("self_kwh"),
                            "export_kwh": s("export_kwh"), "import_kwh": s("import_kwh"), "co2_t": s("co2_t"),
                            "peak_kw": r2(max((x.get("peak_kw") or 0 for x in ds), default=0)) or None})
            elif key in inv_month:
                rec.update({"pv_kwh": r2(sum(x["kwh"] or 0 for x in inv_month[key])), "days": None})
            else:
                rec["pv_kwh"] = None
            monthly.append(rec)
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)

    # รายชั่วโมงของวันล่าสุดที่มีรายงานรายชั่วโมง
    hdate = max(hourly_days) if hourly_days else None
    hourly = []
    for h in sorted(hourly_days.get(hdate, {})):
        v = hourly_days[hdate][h]
        meter = v["import_kwh"] is not None or v["export_kwh"] is not None
        hourly.append({
            "h": h, "pv_kwh": r2(v["pv_kwh"]),
            "use_kwh": r2((v["pv_kwh"] or 0) - (v["export_kwh"] or 0) + (v["import_kwh"] or 0)) if meter else None,
            "grid_kwh": r2(v["export_kwh"]), "import_kwh": r2(v["import_kwh"]),
        })
    while hourly and hourly[-1]["pv_kwh"] is None and hourly[-1]["import_kwh"] is None:
        hourly.pop()

    today = daily.get(latest, {})
    inv_latest = inv_day.get(latest) or (inv_day[max(inv_day)] if inv_day else [])
    total_inv = sum(x["total_kwh"] or 0 for x in inv_latest) if inv_latest and all(x["total_kwh"] is not None for x in inv_latest) else None
    total_plant = max((daily[d].get("total_kwh") or 0 for d in dates), default=0) or None
    total_sum = sum(daily[d].get("pv_kwh") or 0 for d in dates)
    total_kwh = max(v for v in (total_inv, total_plant, total_sum) if v is not None)
    mkey = latest[:7] if latest else None
    mrec = next((x for x in monthly if x["m"] == mkey), {})

    out = {
        "source": "report",
        "sample": False,
        "plant": "รพ.พระทองคำ",
        "first_date": dates[0] if dates else None,
        "report_date": latest,
        "report_complete": bool(today.get("complete")),
        "report_last_hour": today.get("last_hour"),
        "updated": datetime.now(BKK).isoformat(timespec="minutes"),
        "peak_kw": r2(today.get("peak_kw") or (sum(x["peak_kw"] or 0 for x in inv_latest) if inv_latest else None)),
        "realtime": {
            "day_kwh": r2(today.get("pv_kwh")),
            "day_export_kwh": r2(today.get("export_kwh")),
            "day_use_kwh": r2(today.get("use_kwh")),
            "month_kwh": mrec.get("pv_kwh"),
            "month_days": mrec.get("days"),
            "total_kwh": r2(total_kwh),
        },
        "summary": {  # รวมเฉพาะวันที่มีรายงานรายวัน/รายเดือน
            "days": len(dates),
            **{k: r2(sum(daily[d].get(k) or 0 for d in dates))
               for k in ("pv_kwh", "use_kwh", "self_kwh", "export_kwh", "import_kwh")},
            "co2_t": r2(sum(daily[d].get("co2_t") or 0 for d in dates)),
            "pv_meter_kwh": r2(sum(daily[d].get("pv_kwh") or 0 for d in dates if daily[d].get("use_kwh") is not None)),
            "inverter_only_days": [d for d in dates if daily[d].get("inverter_only")],
            "missing_months": [x["m"] for x in monthly if not x.get("pv_kwh")],
        },
        "hourly_date": hdate,
        "hourly": hourly,
        "daily": [dict({"d": d}, **{k: r2(v) if isinstance(v, float) else v for k, v in daily[d].items()
                                     if k in ("pv_kwh", "use_kwh", "self_kwh", "export_kwh", "import_kwh", "peak_kw", "complete", "inverter_only", "last_hour")})
                  for d in dates[-400:]],
        "monthly": monthly,
        "inverters": [{"name": x["name"], "day_kwh": r2(x["kwh"]), "total_kwh": r2(x["total_kwh"]),
                       "peak_kw": r2(x["peak_kw"]), "hours": r2(x["hours"])} for x in inv_latest],
        "inverter_monthly": [{"m": k, "items": [{"name": x["name"], "kwh": r2(x["kwh"]), "peak_kw": r2(x["peak_kw"]),
                                                "hours": r2(x["hours"])} for x in v]} for k, v in sorted(inv_month.items())],
        "errors": skipped,
    }
    out["grid"] = build_grid(ami, ami_info, daily) if ami else None
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    have = [x["m"] for x in monthly if x["pv_kwh"] is not None]
    print(f"wrote {OUT}: {len(dates)} วัน, เดือนที่มีข้อมูล {', '.join(have)}, ล่าสุด {latest}")
    for s in skipped:
        print("  ข้าม:", s)


if __name__ == "__main__":
    main()
