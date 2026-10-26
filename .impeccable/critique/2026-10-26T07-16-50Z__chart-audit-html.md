---
target: chart_audit.html before redesign
total_score: 20
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
target_identity: "file:/workspace/chart_audit.html"
target_fingerprint: "sha256:b29cb1bb881a4b3bd63d754e943f705e0eeb5f65ce995d13234b5a82a088c522"
target_path: /workspace/chart_audit.html
timestamp: 2026-10-26T07-16-50Z
slug: chart-audit-html
---
Method: dual-agent attempt. Assessment A completed (agent bc-478ee4ca-b1fc-51a3-8000-40470d4bd751). Assessment B's subagent failed in a repeating pattern; the detector was run in the parent after A returned. ⚠️ DEGRADED: Assessment B subagent failed; detector rerun by parent after A.

# Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Update date is shown; fetch has no loading state and every flow dot looks finished. |
| 2 | Match System / Real World | 3 | Thai and the Buddhist date fit; the English kicker and the footnote's use of "เปลี่ยน" do not. |
| 3 | User Control and Freedom | 2 | Shell navigation is a real exit; the page itself cannot be jumped or filtered. |
| 4 | Consistency and Standards | 2 | Shell is Sarabun and #1D6FA4; the page is IBM Plex Sans Thai and #1f3864. |
| 5 | Error Prevention | 2 | Green +2.07% and the footnote teach that 21% of charts changed AdjRW. The number is the paired cohort. |
| 6 | Recognition Rather Than Recall | 3 | Counts are visible; DISCHT, TGrp, and drg_changed are undefined or absent. |
| 7 | Flexibility and Efficiency | 1 | One long scroll. No jump to the follow-up or the comparison. |
| 8 | Aesthetic and Minimalist Design | 2 | Equal KPI cards, emoji gradient headers, and a second drawing of the same before/after pair. |
| 9 | Error Recovery | 2 | A failed fetch names the status and offers no recovery. |
| 10 | Help and Documentation | 1 | No in-line gloss for the abbreviations a projector reading depends on. |
| **Total** | | **20/40** | **Weak / needs work** |

## Design Specificity

Content is specific to this coding audit. Composition is a generic analytics template: four equal KPI cards, an uppercase English kicker, emoji section bars with a thick left border, and a green wash on any positive delta.

Deterministic scan of the pre-change page: 7 findings. side-tab accent border (3), low contrast #6b7280 on #f4f6fa at 4.47:1, low contrast #9ca3af on #f4f6fa at 2.3:1, kicker "Chart Audit Report", skipped heading h1 to h3. No browser overlay was injected.

## Overall Impression

The numbers are careful and the PDPA boundary is clear. The page still leads with a small green delta and hides the three discharge conflicts, the missing file, and the DRG change count.

## What's Working

- Aggregate-only data, stated in the scope, the lock line, and the footer.
- Before/after sums use four decimal places and name the paired cohort in the hint.
- Bar-end labels on the chapter charts can be read without a hover.

## Priority Issues

### [P1] The footnote calls the before/after cohort a change in AdjRW
Why it matters: a manager will read "4 จาก 19 ชาร์ต (21%) ที่ AdjRW เปลี่ยนหลัง audit" as if 21% of charts changed. The 4 is before_after.charts. drg_changed is 2 and is not rendered.
Fix: say the 4 charts have both values, and show DRG changed 2 from the existing field.
Suggested command: /impeccable clarify

### [P1] Equal KPI cards, a green delta, emoji headers, and an English kicker bury the work
Why it matters: the scan target is the follow-up, and the only saturated object is +0.0704.
Fix: open with the spoken result and the follow-up counts. Drop the eyebrow, the emoji, and the green wash.
Suggested command: /impeccable layout

### [P1] Thai is set on Latin line-height, in two families
Why it matters: the shell name carries stacked marks at line-height 1.2, and the page uses a different face from the shell.
Fix: Sarabun with line-height 1.7, and a taller shell title on this page.
Suggested command: /impeccable typeset

### [P1] Chart.js canvases are the only copy of the chapter counts, and the before/after bars hide a 2% gap
Why it matters: a canvas has no text alternative, and 3.3950 vs 3.4654 both fill the track.
Fix: text rows with the count and the JSON percent. A numeric ledger instead of two full bars.
Suggested command: /impeccable colorize

### [P2] Phone and projector fight the shell
Why it matters: pills, a 260px sidebar, and an uncapped wrap stretch or bury the result.
Fix: cap the reading width, one stack breakpoint, and keep the result near the top.
Suggested command: /impeccable adapt

## Persona Red Flags

Medical-records officer: the green KPI is the first saturated object. The DISCHT tag is not a destination, and missing_json is absent.

Manager on a projector: they will read the English kicker, English chapter axis, and the false 21% sentence. Footer gray is 2.35:1.

First-time colleague: the stepper looks clickable and is not. AdjRW, PDx, SDx, DISCHT, and TGrp are undefined.

## Minor Observations

- No per-chart rows exist in data/audit_stats.json. Do not invent them.
- No patient identifier is on the page. The shell byline names Suweerasak Riwlord, M.D., a staff author, not a patient.
- drg_changed, rw_after_sum, after_only_charts, missing_json, final_warn_err, discht_dist, and mdc_dist are in the file and were not drawn.
- PDx counts charts and SDx counts codes, in identical drawings.

## Questions to Consider

- If the room hears one sentence, is it the three DISCHT conflicts, the two DRG changes, or the +0.0704 sum?
- Should English ICD chapter titles stay, with a Thai short name beside them?
