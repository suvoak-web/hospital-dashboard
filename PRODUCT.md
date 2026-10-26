# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Inferred from the task brief, after a localhost decision page received no answer: primary users are medical-records staff (เวชระเบียน) and their managers at โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา. They read an aggregate inpatient chart-audit result at a desk, aloud from a projector, and on a phone.

Repository evidence for the hospital name: `credit.js` and `README.md`.

## Product Purpose

Show the aggregate result of an inpatient chart audit: charts audited, AdjRW before and after, mean AdjRW for this set, DRG changes, coding follow-ups, and diagnosis and procedure distributions. Success means a coder or a manager can say the result correctly, including which charts were actually compared.

## Positioning

The page is a de-identified aggregate. It does not list charts or patients. Other dashboards in this repository cover operations, finance, or hospital KPI; this one is only the coding-audit rollup.

## Operating Context

Static HTML on GitHub Pages. `credit.js` supplies the shared hospital header, sidebar, and page links. The page fetches `data/audit_stats.json`. The file on hand covers 19 charts, scope “เริ่ม ตุลาคม 2569”, updated “14 ต.ค. 2569”.

## Capabilities and Constraints

- Static page. No build step. Do not change data values, calculations, or `data/audit_stats.json`.
- Keep every metric the current page already shows.
- Do not add patient identifiers. The data file has no per-chart rows. Do not invent rows.
- UI text is Thai. Tone marks must render. Sarabun is the shared shell face and a brief-allowed Thai face.
- The page must work at phone width and on a projector.
- Two formulas already on the page stay as they are: delta percent = diff / sum_before × 100, two decimals; paired share = paired charts / total × 100, zero decimals; money-like weights use `toFixed(4)`.
- Inferred display choice: fields the page already loads but did not draw (`drg_changed`, `after_only_charts`, `missing_json`, `rw_after_sum`, `final_warn_err`, `discht_dist`, `tgrp_code_adjustments`, `mdc_dist`, `pdx_by_block3`, `skipped_summaries`, `audit_note_unknown`) are shown as stored, because the brief asks for DRG and a complete reading of this file. No new arithmetic.

## Brand Commitments

The shared shell uses Sarabun and `#1D6FA4`. This page should read as part of that hospital system. Voice is plain Thai, with the English abbreviations coders already use (AdjRW, DRG, PDx, SDx, DISCHT, TGrp) defined in the sentence around them.

## Evidence on Hand

- `chart_audit.html`
- `data/audit_stats.json` (aggregate only; rule string says no AN/HN/name/DOB)
- `credit.js` shell
- No per-chart rows, testimonials, or benchmarks. Do not fabricate them.

## Product Principles

- The sentence a manager reads aloud has to be true.
- Follow-up work outranks a small positive delta.
- Every number on screen is a JSON field or one of the two formulas already on the page.
- The page is a report inside the hospital shell, readable up close and from a projector.

## Accessibility & Inclusion

Thai readers, including tone marks and under-vowels. Text contrast at WCAG AA. Results in text, not only on a canvas. Phone and projector are both required.

## Inference

The decision page was served only on localhost and was not answered. Facts above that are not in the repository are inferred from the task brief and marked as such.
