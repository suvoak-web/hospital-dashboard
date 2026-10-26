---
name: Chart audit sheet
description: Cool-paper screening sheet for the aggregate chart audit. Applies to chart_audit.html only.
colors:
  cool-paper: "#f4f7f9"
  ink: "#142433"
  muted: "#3c5160"
  line: "#d5e0e8"
  blue: "#0e4f78"
  bar: "#1a6ea3"
  track: "#e3eef4"
  warn: "#6e3d0c"
  warn-bg: "#fff5e8"
  focus: "#0b5cad"
  selection: "#c5dff0"
  error: "#7f1d1d"
  error-bg: "#fdecec"
typography:
  display:
    fontFamily: "Sarabun, \"Noto Sans Thai\", Tahoma, sans-serif"
    fontSize: "4.25rem"
    fontWeight: 700
    lineHeight: 1.05
    fontFeature: "tabular-nums"
  headline:
    fontFamily: "Sarabun, \"Noto Sans Thai\", Tahoma, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 600
    lineHeight: 1.65
  title:
    fontFamily: "Sarabun, \"Noto Sans Thai\", Tahoma, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.45
    letterSpacing: "0"
  body:
    fontFamily: "Sarabun, \"Noto Sans Thai\", Tahoma, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Sarabun, \"Noto Sans Thai\", Tahoma, sans-serif"
    fontSize: "0.92rem"
    fontWeight: 600
    lineHeight: 1.5
rounded:
  none: "0"
  sm: "2px"
  pill: "99px"
spacing:
  hair: "4px"
  tight: "8px"
  row: "12px"
  pair: "18px"
  sheet: "28px"
  section: "2rem"
components:
  spoken-sentence:
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    padding: "0"
  follow-up-count:
    textColor: "{colors.blue}"
    typography: "{typography.display}"
    rounded: "{rounded.none}"
    padding: "0 10px"
  follow-up-alert:
    backgroundColor: "{colors.warn-bg}"
    textColor: "{colors.warn}"
    typography: "{typography.display}"
    rounded: "{rounded.none}"
    padding: "8px 0"
  ledger:
    textColor: "{colors.ink}"
    padding: "12px 12px 4px 0"
  text-bar:
    backgroundColor: "{colors.bar}"
    rounded: "{rounded.pill}"
    height: "8px"
  text-bar-peak:
    backgroundColor: "{colors.blue}"
    rounded: "{rounded.pill}"
    height: "8px"
  text-bar-track:
    backgroundColor: "{colors.track}"
    rounded: "{rounded.pill}"
    height: "8px"
  procedure-table:
    textColor: "{colors.ink}"
    padding: "10px 12px 10px 0"
  section-jump:
    textColor: "{colors.blue}"
    height: "44px"
  disclosure:
    textColor: "{colors.blue}"
    height: "44px"
    padding: "8px 0 0"
  error-status:
    backgroundColor: "{colors.error-bg}"
    textColor: "{colors.error}"
    rounded: "{rounded.sm}"
    padding: "12px 14px"
  source-step:
    textColor: "{colors.ink}"
    padding: "10px 0"
---

# Design System: Chart audit sheet

## Overview

**Creative North Star: "The Posted Screening Sheet"**

The chart audit is a notice posted on cool fluorescent paper. The first line is a sentence a manager can read aloud. Under it, the counts that still need a person sit in a box, larger than every other figure. The sheet then gives the numeric ledger, the code distributions, and the procedure table. It refuses an equal-card dashboard.

This system is the audit sheet in `chart_audit.html` only. Other pages in the repository are not this world. The page is drawn inside the shared hospital shell, and that shell keeps its own header and sidebar. The sheet does not retokenize that chrome. On the sheet itself, one Thai text face carries the tone marks, posted blue is the result, and amber is spent only when a person still has to act.

The material is flat paper. Separation is a hairline, a 1px box, an amber wash, or the single rule under the spoken sentence. The only motion is that rule drawing once from the left.

**Key Characteristics:**

- Cool paper as the page field, with a transparent report so the sheet is not a card
- One spoken sentence, with a 3px rule under it
- Follow-up counts in a 1px box, larger than the ledger
- Amber only when a count needs a person
- A numeric ledger, text bars, and a procedure table in the same ink
- Sarabun, with Noto Sans Thai behind it, and reading text at line-height 1.65–1.7

## Colors

Ink, two blues, and one amber on cool paper. The paper is the body field.

### Primary

- **Posted Blue** (`colors.blue`): the result ink. Boxed counts that do not need a new decision, in-page jumps, the disclosure summary, step numbers, the word สูงสุด, and the peak bar.
- **Rule Blue** (`colors.bar`): the 3px rule under the spoken sentence, and every distribution bar that is not the peak. The sheet’s direction spoke of one blue ink; the build splits result ink from the rule and the ordinary bar, and the build stands.
- **Focus Blue** (`colors.focus`): the keyboard ring, 3px solid, offset 3px on the sheet.

### Secondary

- **Follow-up Amber** (`colors.warn`): the box border, the boxed figure, and the row label when that count needs a person.
- **Amber Wash** (`colors.warn-bg`): the full row behind that alert. It is a wash, not a card.

### Tertiary

- **Load Error** (`colors.error`) on **Error Wash** (`colors.error-bg`): the failed fetch only. A 2px corner, padding 12px 14px. It names the failure and the retry.

### Neutral

- **Cool Paper** (`colors.cool-paper`): the page background. The report is transparent, so this is the sheet.
- **Ledger Ink** (`colors.ink`): body text, the spoken sentence, ledger figures, and procedure names. Selection keeps this ink.
- **Caption Slate** (`colors.muted`): scope, hints, column headers, English chapter lines, fact notes, and the footer.
- **Hairline** (`colors.line`): the 1px row and cell rules.
- **Bar Track** (`colors.track`): the 8px trough behind a distribution bar.
- **Selection Wash** (`colors.selection`): text selection, with ledger ink on top.

### Named Rules

**The Amber-Is-Work Rule.** Amber ink on the amber wash is only for a follow-up count that needs a person. A positive AdjRW delta stays ledger ink. The sheet has no green result.

**The Two Blues Rule.** Posted blue is the result. Rule blue is the spoken underline and the ordinary bar. Peak bars step back to posted blue. Neither blue replaces the shared hospital header, and the header color is not a token of this sheet.

## Typography

**Display Font:** Sarabun (with Noto Sans Thai, then Tahoma, then sans-serif)
**Body Font:** Sarabun (with Noto Sans Thai, then Tahoma, then sans-serif)

**Character:** One Thai text face for prose, figures, and procedure codes. Sarabun is loaded at 400, 500, 600, and 700; Noto Sans Thai is the fallback at 400, 600, and 700. Weight and size make the hierarchy. Figures that are counts or weights use tabular numerals. Letter-spacing stays at 0 where it is set. There is no monospace costume and no display face.

### Hierarchy

- **Display** (700, 4.25rem, line-height 1.05, tabular numerals): the boxed follow-up count. Under 720px the same role is 2.65rem.
- **Sheet name** (700, 1.7rem, line-height 1.45, letter-spacing 0): the single page title. Under 720px it is 1.55rem. It is not a second display face.
- **Headline** (600, 1.4rem, line-height 1.65): the spoken sentence, width at most 40em. From 1100px it is 1.65rem. Under 720px it is 1.12rem at line-height 1.6.
- **Title** (700, 1.35rem, line-height 1.45, letter-spacing 0): section headings.
- **Ledger figure** (700, 1.7rem, line-height 1.25, tabular numerals): the before, after, and delta. From 720px the figure is 2.15rem. The percent under the delta is 0.9rem, weight 600, caption slate.
- **Fact figure** (700, 1.45rem, line-height 1.35, tabular numerals): the supporting totals. The note under a fact is 0.92rem, weight 500, caption slate.
- **Body** (400, 1rem, line-height 1.7): hints, notes, the de-identification line, and step text. The root is 16px, and 17.5px from 1100px, so this rem step grows on a projector. Supporting labels (scope, the count’s title, the ledger caption) are 1.05rem.
- **Label** (600, 0.92rem, line-height 1.5, caption slate): English chapter lines, procedure headers, and the small tables. Ledger column headers are the same role at 0.95rem and line-height 1.5. The peak word is 0.78rem, weight 700, posted blue.

### Named Rules

**The Reading Line Rule.** Prose that a person reads across is line-height 1.65 to 1.7: the spoken sentence at 1.65, and hints, notes, and body at 1.7. The phone size of the spoken sentence is 1.6. Counts and ledger figures tighten to 1.05–1.35 and use tabular numerals.

**The One Face Rule.** Procedure codes, step numbers, and the boxed counts use Sarabun with Noto Sans Thai behind it. Do not swap in a monospace face to make a code look technical.

## Layout

The sheet is one reading column, max-width 1080px, margin 8px auto 40px, padding 8px 28px 36px. Under 720px the padding is 12px 16px 28px and the bottom margin is 24px. Sections start 2rem below the previous block. The follow-up block sits closer, 1.15rem under the spoken sentence.

The spoken sentence comes before the boxed counts, and the ledger sits immediately under that work. Distributions, the procedure table, and the source trail start below the first screen. Hints and notes measure 68ch. The de-identification note measures 62ch. The spoken sentence measures at most 40em.

The repeated rhythm is 4px inside tight stacks, 8px under a caption or between a bar and its track, 12px for row padding and the gap in a count row, 18px between a count’s words and its box, and 28px for the sheet’s side padding and the gap between the two chapter columns. From 720px the fact list is two columns, with 22px on the trailing side of each odd cell, and the two chapter lists sit side by side. From 1100px the root is 17.5px and the spoken sentence steps up to 1.65rem.

In-page jumps wrap, with a 4px by 18px gap, each link at least 44px tall. The disclosure summary is the same 44px target.

### Named Rules

**The First Viewport Rule.** The first screen is the sheet name, the spoken sentence, and the boxed follow-up counts, then the ledger. Chapter bars and the procedure table stay below that. Do not pull the distributions up beside the sentence.

## Elevation & Depth

The sheet is flat. It has no drop shadow, no raised card, and no side stripe. Depth is tonal and linear: the hairline between rows, the 1px border of a count, the amber wash on an alert row, and the 3px rule under the spoken sentence. The hospital header’s shadow belongs to the shared shell, not to this sheet.

### Named Rules

**The Flat Sheet Rule.** Surfaces sit on cool paper. Do not put the report in a card, and do not add a shadow to a count, a bar, or a table.

## Shapes

Corners on the sheet are square: the count box, the rows, the tables, and the error status’s near-square 2px radius. The only capsule is the distribution track, 8px tall with a 99px radius, clipped so the fill follows the same capsule. Borders that structure the sheet are 1px hairlines. The count box is a 1px border in posted blue, or in follow-up amber when the row is an alert. The spoken rule is 3px tall and the width of the sentence, not a full-bleed divider.

### Named Rules

**The Square Sheet Rule.** Counts, tables, and rows stay square. The distribution track is the only pill. Do not round the count into a badge.

## Components

### Spoken sentence

The sentence a manager reads aloud. It is the headline step, ink on cool paper, fit to its own width up to 40em. A 3px rule in rule blue sits 12px below the words and spans that width. It draws once from the left (0.55s, cubic-bezier(0.16, 1, 0.3, 1)) and is already fully drawn when reduced motion is requested. The sentence is not a control, so it has no hover.

### Follow-up counts

A two-column row: the label on the left, the figure on the right. The figure is the display step, tabular, centered, with at least 1.6ch of width, padding 0 10px, and a 1px border. Rows are separated by a hairline, with 8px vertical padding and an 18px gap before the box. The label is 1.05rem, weight 700, line-height 1.55.

A count that needs a person paints the whole row with the amber wash, and the box, the figure, and the label switch to follow-up amber. Other counts keep ledger ink on the label and posted blue on the box. Nothing here hovers.

### Numeric ledger

A three-column table for before, after, and the delta. The caption is 1.05rem, weight 700, above the table. Headers are caption slate, weight 600, about 0.95rem. Figures are 1.7rem (2.15rem from 720px), weight 700, tabular, aligned to the baseline, with a hairline on top of the row and padding 12px 12px 4px 0. The delta’s percent is a second line in caption slate. The supporting fact list under the ledger is a stack of term and figure, hairline on top, two columns from 720px. Figures there are 1.45rem. There is no card around either block.

### Text bars

Each chapter is a text row, not a canvas. The Thai short name is weight 700. The English chapter line is the label step, in caption slate, and is marked as English. The count, the unit, and the JSON percent are tabular and right-aligned; the percent is caption slate. If the row is a maximum, the word สูงสุด follows in posted blue at 0.78rem. An 8px track in bar-track color sits 6px under the words. The fill is rule blue, or posted blue when the row is a maximum. Both track and fill are capsules. Several tied maxima are all posted blue. An empty distribution is one caption-slate line.

### Procedure table

Aggregate ICD-9-CM rows in a full-width table: order, code, name, count. A hairline tops each row. Padding is 10px 12px 10px 0, line-height 1.55, and long names may break anywhere. Codes use Sarabun at weight 700 with tabular numerals, not a monospace face. Counts are right-aligned and tabular, prefixed with a times sign. The maximum count carries the same สูงสุด word as the bars. The caption is weight 700, above the table. The smaller code tables inside the disclosure use the same hairline, right-aligned numbers, and 0.92rem headers.

### Jumps, disclosure, and errors

Jumps are posted-blue, weight 700, underlined, offset 4px, at least 44px tall. Hover thickens the underline from 1px to 2px. The disclosure summary is the same blue and the same 44px target; hover underlines it, offset 3px. A failed load replaces the quiet status line with load-error ink on the error wash. An empty list is caption slate. Keyboard focus is a 3px focus-blue ring, offset 3px. On this page the same ring is offset 2px on the shell’s own controls.

The source trail is an ordered list. The number is generated, tabular, weight 700, posted blue, in a 2.2rem column. The step title is weight 700; the Thai line under it is caption slate. A hairline tops each step. The sequence is the procedure, so the numbers stay.

### Named Rules

**The Boxed Count Rule.** A follow-up count is a 1px box in the display size, larger than the ledger. Alert boxes use follow-up amber on the amber wash. Every other box uses posted blue on the paper.

**The Spoken Rule.** One 3px rule in rule blue sits under the spoken sentence and is only as wide as that sentence. It draws once from the left, and reduced motion leaves it in place.

## Do's and Don'ts

### Do:

- **Do** paint the page with cool paper and keep the report transparent, so the sheet is the page.
- **Do** box follow-up counts with a 1px border and keep them larger than the ledger figures.
- **Do** put one 3px rule-blue line under the spoken sentence, the width of that sentence.
- **Do** render distributions as text rows (Thai name, English chapter, count, percent) with an 8px capsule track, and mark a maximum in posted blue with the word สูงสุด.
- **Do** keep procedure codes in Sarabun, right-align counts, and set figures in tabular numerals.
- **Do** keep reading line-height at 1.65–1.7, and use a 3px focus-blue ring.
- **Do** leave the shared hospital header and sidebar on the shell. This page may keep the legibility overrides it already ships there (a taller header title, no uppercase tracking on sidebar groups, and the shared focus ring).

### Don't:

- **Don't** color a positive delta green, and don't spend amber on anything except a count that needs a person.
- **Don't** put the audit in a sheet card, a side stripe, or a shadow.
- **Don't** add a kicker or an eyebrow above the sheet name, and don't use emoji as icons.
- **Don't** set procedure codes in a monospace face.
- **Don't** recolor the shared hospital header with posted blue, or import the header color onto the sheet.
- **Don't** add a per-chart or patient table. The procedure table is the aggregate ICD-9-CM list.
