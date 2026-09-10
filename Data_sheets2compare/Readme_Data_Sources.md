# Data Sources

Inventory of the source spreadsheets behind the catalog, and specifically behind
`dashboard_all.html` (the "all attempts" catalog, which adds objects that were
attempted but not detected to the main 1,036-object `dashboard.html`). The
spreadsheets themselves aren't in this repo yet — this documents what's in each
one now, ahead of uploading them here later.

A note on authorship metadata: every file's embedded "creator" field just says
"openpyxl" (the Python library that last wrote it), not the original human
author. Where Excel/Sheets recorded a "last modified by," it's listed below;
otherwise authorship is inferred from content (initials in notes, filenames)
and marked as such, not asserted as fact.

## The "Verified_Catalog" lineage — 4 versions of the same union catalog

These four files share the same base structure (a reconciled union of the
older working lists below) and the same 1,360-row core, refined over time.
**`ALL_AO_CATALOG_2026_DRAFT.xlsx` is the one the 321 not-detected objects in
`dashboard_all.html` were extracted from** — not `BUILD`, which has the same
row set but a merge-key bug (see CHANGELOG below) and packs H/diameter/
rotation/albedo into one unparsed text field instead of separate columns.

| File | Last modified by | Last updated | Sheets |
|---|---|---|---|
| `ALL_AO_CATALOG_2026_BUILD.xlsx` | *(not recorded)* | 2026-07-08 21:15 | Verified_Catalog, Counts_Comparison, Discrepancies, Diff_vs_Run1 |
| `ALL_AO_CATALOG_2026_DRAFT_LFZM.xlsx` | Luisa Fernanda Zambrano Marin | 2026-07-08 21:03 | Verified_Catalog, Counts_Comparison, Discrepancies, Diff_vs_Run1 |
| `ALL_AO_CATALOG_2026_DRAFT.xlsx` | Luisa Fernanda Zambrano Marin | 2026-07-09 05:43 | Verified_Catalog, Discrepancies, Counts_Comparison, Diff_vs_Run1, **CrossCheck**, References_split, CHANGELOG |
| `ALL_AO_CATALOG_2026_calude_v1.xlsx` | Luisa Fernanda Zambrano Marin | 2026-08-13 12:54 | Verified_Catalog, **Final_List**, **References**, Discrepancies, Counts_Comparison, Diff_vs_Run1, CrossCheck, CHANGELOG |

### Sheets in this lineage

- **Verified_Catalog** (all 4 files) — one row per object, detected or not.
  Number/Name/Designation, Category, H/Diameter/Rotation/Albedo, `Count as
  Detection` (Yes / No / Duplicate / blank / N/A), `Comment - NOTE`, JPL SBDB
  link, logsheet/datapath. **Source of the 321 not-detected objects and their
  Notes column** in `dashboard_all.html` (via DRAFT specifically).
- **CrossCheck** (DRAFT + calude_v1 only) — per-object validation against live
  JPL SSD: identity, category, orbit family, H, diameter, rotation, albedo,
  binarity. **Used to independently verify the category of all 321
  not-detected objects** — caught 23 miscategorizations (mostly missing PHA
  tags), all fixed by preferring the SBDB-informed `Category tags` field over
  the coarser `Category (orig)` field.
- **Discrepancies** — 45-46 rows, one per resolved cross-source conflict, with
  `Fix` / `Fix_Status` / `Fix_how2` columns. Skimmed, not directly used.
- **CHANGELOG** (DRAFT + calude_v1) — human-written log of what changed in
  that pass. Read in full for DRAFT; this is how the Bennu/2010 SV3 merge-key
  bug fix (present in DRAFT, not BUILD) was found, confirming DRAFT as the
  better source.
- **Counts_Comparison / Diff_vs_Run1** — object-count reconciliation between
  MASTER/FINAL declared counts and independent recounts. Not used.
- **Final_List / References** (calude_v1 only) — dedicated APA-citation
  columns (`Title/Citation (APA)`, `URL/doi`) with 8 ready-made references for
  not-detected objects. **Flagged as candidates, not yet imported** — at least
  one (attached to object "2006AN") looks like a possible mismatch (a
  Didymos/DART paper) and needs verification against the project's
  [reference-matching methodology](../REFERENCE_MATCHING_METHODOLOGY.md)
  before being trusted.

## Independent validation files

| File | Last modified by | Last updated | What it tracks |
|---|---|---|---|
| `MBA_Reconciliation_Results_2026.xlsx` | *(not recorded)* | 2026-08-31 21:08 | One sheet, `MBA_Reconciliation` — 142 MBAs bucketed (clean-detected / orphan-excluded / tape-not-digitized / resolved-conflict) against the live catalog. **Used to verify all 13 "tape not digitized" MBAs and all 4 "orphan, correctly excluded" MBAs** in the not-detected list — 100% match after fixing an extraction bug that was dropping object numbers for numbered+named asteroids (e.g. "92 Undina (A867 NA)"). |
| `CROSSCHECK_temp.xlsx` | *(not recorded)* | 2026-07-08 12:56 | Sheets: CrossCheck, References_split, Summary — appears to be a scratch/staging copy of the same CrossCheck process as DRAFT's own CrossCheck sheet. Not used (DRAFT's CrossCheck was used directly instead). |

## Legacy input files

Per calude_v1's own README cell, these are already absorbed into
Verified_Catalog: *"Union of: MASTER LIST + FINAL_LIST_2023 + FSIWebpage2024
(All_obj_obs_count_AO_lu.xlsx), thesis FinalTable (CatalogTable4Thesis.xlsx),
live FSI webpage."* They were spot-checked for content that might be missing
from Verified_Catalog's notes, not used as a primary source.

| File | Last modified by | Last updated | Notes |
|---|---|---|---|
| `All_obj_obs_count_AO_lu.xlsx` | Luisa Fernanda Zambrano Marin | 2026-08-26 12:06 | Personal working copy, **43 sheets** (MASTER LIST, LuisaStats, NEA-problematic, Orphans(TAPES), REFSCHECKworkspace, ELLENs LISTS, Beths tabulations, JLM list, and many scratch/intermediate sheets). Spot-checked `NEA-problematic` in full, plus a name-search across all 43 sheets for a random sample of not-detected objects - no content found that's missing from Verified_Catalog's notes. |
| `All_obj_obs_count_AO.xlsx` | *(not recorded)* | 2026-07-06 14:03 | Same 43-sheet structure as the `_lu` version, apparently an earlier or shared copy. Same spot-check, same result. |
| `CatalogTable4Thesis.xlsx` | *(not recorded)* | 2026-07-07 06:48 | Sheets: FinalTable, Orphans - thesis export. Name-searched, not individually read in full. |
| `Data_Project_brain.cell.killer.xlsx` | *(not recorded)* | 2026-07-09 10:20 | **20 sheets** - the Arecibo processing-log source. Already used elsewhere for the observation-mode/Year-Days-Mode table feature on every object's card (both `dashboard.html` and `dashboard_all.html`). Also has detection-status working sheets (`Not_processed`, `No Data FoundNo Folder`, `Re-check`, `No_Detection`) that were spot-checked against the Notes column - e.g. confirmed that "2000 RD53" looking absent from the not-detected list was correct: this file's `Re-check` sheet called it tentative, but Verified_Catalog's later reconciliation confirmed it as a real detection via astrometry, correctly superseding the earlier note. Since then, fully extracted end-to-end - see `Data_Project_brain.cell.killer_extracted.xlsx` below. |

### Derived: `Data_Project_brain.cell.killer_extracted.xlsx`

A flat, per-object/per-date extraction of `Data_Project_brain.cell.killer.xlsx`'s CW/delay-Doppler
records (Object, Year, Date, CW yes/no + files, Delay-Doppler yes/no + setup + files), built by
`extract_braincell_detections.py`. 4,047 object-date rows across 1,357 objects, after deduping 118
rows found to be exact-duplicate blocks already present in the source sheets (copy-paste artifacts,
not real repeat observations - see the `Detections` sheet's row-level `sheet` column for provenance).

The **Notes** column on each row merges three sources, each tagged so it can be traced back: real
Excel cell-comment text (669 found workbook-wide, 653 attributed to a specific object via row
position), status/comment columns from the workbook's other tracking sheets (`Not_processed`,
`No_Detection`, `Compare`, `Objects with data`, `Successful_Detection`, `ALL OBJECTS THAT HAVE A
FOLDER`, `Re-check`, `MISSING`), and - once cross-checked against the live catalog - a summary of
any detection-status conflict found.

A **"Re-check (detection flag)"** sheet lists the 118 objects currently marked "Detected" on the
live catalog where this workbook's own tracking disagrees (either its Compare/No_Detection sheets
say "no detection," or no CW/delay-Doppler file is ever marked available) - each with a blank
Resolution column for manual triage. The same 118 flags are also pushed into `dashboard_all.html`'s
existing "Re-check" filter (`review_flag` field) and appended to each object's Notes.

## What hasn't been exhaustively checked

Every cell of every sheet in the 43-sheet files (`All_obj_obs_count_AO_lu.xlsx`,
`All_obj_obs_count_AO.xlsx`) has not been read line by line - those were spot-checked by
name-searching a random sample of objects, not exhaustively audited.
`Data_Project_brain.cell.killer.xlsx`'s year-range/Comets/"Named objects" sheets, by contrast,
*have* now been read in full (see the derived workbook above) - the remaining gap there is that
the extraction hasn't yet been re-verified against a second independent pass. If a specific sheet
in the 43-sheet files needs a full audit, that's a targeted follow-up, not something this pass
covered.
