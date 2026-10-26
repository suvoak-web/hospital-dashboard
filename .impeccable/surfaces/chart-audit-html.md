---
version: 1
slug: "chart-audit-html"
primary_target: "chart_audit.html"
related_targets: []
---

# Chart audit

Mode: operate

Audience: medical-records staff and managers at โรงพยาบาลพระทองคำเฉลิมพระเกียรติ 80 พรรษา, reading an aggregate audit on a phone and a projector.

Job: say the audit result correctly and see which follow-ups need a person.

Constraints: static HTML, do not change JSON values or the two existing formulas, no per-chart rows, no patient identifiers, Thai UI in Sarabun.

## Direction contract

THESIS: A posted screening sheet whose first line a manager can read aloud. It refuses the equal KPI-card dashboard.

OWN-WORLD: Cool fluorescent paper, Sarabun, blue ink for the result, amber only on counts that need a person. Follow-up counts sit in a 1px box, larger than the ledger. One blue rule under the spoken sentence. No sheet-card, no emoji, no side-tab.

STORY: The visitor hears how many charts were compared, the AdjRW delta, how many DRGs changed, and which conflicts remain. Then they can read the code distributions.

FIRST VIEWPORT: Shared hospital shell, then the Thai title, the spoken sentence, and the boxed follow-up counts. The ledger sits immediately under that. Distributions start below the first screen. Signature: the boxed count, the way a posted screening sheet circles the abnormal number.

FORM: Candidate 6 of the grounded list, a clinic-wall screening summary. Seed 970f5349. Raises kept from declined challengers: specimen scale contrast, j-card right-aligned counts, video-feed first screen, zoo flat colour instead of a floating card.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
