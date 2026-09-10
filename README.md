# Arecibo Observatory Planetary Radar Object Catalog

Data repository backing the interactive dashboard cataloging every solar system object detected by the Arecibo Observatory's planetary radar system between 1978 and 2020 — 1,036 objects spanning near-Earth asteroids, potentially hazardous asteroids, main-belt asteroids, comets, planets, moons, rings, and spacecraft.

**Live dashboard:** https://luchananda.github.io/LPI-Arecibo-data/dashboard.html

**All-attempts catalog:** https://luchananda.github.io/LPI-Arecibo-data/dashboard_all.html — the same catalog expanded to 1,356 objects, adding every object that was *attempted* at Arecibo but not confirmed detected. See below for what's different.

## What's in this repository

- `dashboard.html` — the self-contained interactive dashboard (also mirrored to a Claude Artifact for preview, but this GitHub Pages copy is the canonical, fully-working version — Claude's Artifact hosting blocks external images, so this is the one to share)
- `dashboard_all.html` — a companion catalog covering every object ever attempted at Arecibo (1,356), not just the 1,036 confirmed detections. Adds a **Detection** status column (Detected / Not detected / Unclear), a **Notes** column (comments and clues gathered from the underlying processing-log workbook, on every object where something was found), and a **Re-check** filter for objects flagged during cross-checking as needing manual review. The **H (mag)** column header notes that non-detection values come from JPL SBDB rather than the team's own physical-data sources.
- `TeamRadar-Revision.html` — a separate, experimental interactive page for FSI/Arecibo team members to review and submit corrections on individual catalog objects (comments, "I have data" flags, reference approve/reject, new references, Re-visit flags). It does **not** replace or link from the live dashboard above; reviewed input is merged in by hand later. Currently covers only the 1,036 detected objects in `dashboard.html`, not the all-attempts catalog. See [`TeamRadar-Revision/README.md`](TeamRadar-Revision/) for what it is, why it exists, and how it was built.
- `Data_sheets2compare/` — documentation of the source spreadsheets behind the catalog (see [`Readme_Data_Sources.md`](Data_sheets2compare/Readme_Data_Sources.md)), plus derived data products such as `Data_Project_brain.cell.killer_extracted.xlsx` — a flat per-object/per-date extraction of the Arecibo processing-log workbook's CW/delay-Doppler file records and cross-sheet notes, with a "Re-check" sheet flagging detection-status conflicts found by cross-checking it against the live catalog
- `curated/` — hand-picked public-domain/Creative-Commons images (NASA, NRAO) used for objects that don't have their own LPI radar imagery, mainly the planets, the Moon, and Saturn's rings
- All other folders (`Continuous Wave/`, `Delay Doppler/`, etc.) — compressed radar product images harvested from the [LPI Asteroids Radar Archive](https://www.lpi.usra.edu/resources/asteroids/), organized by product type and object designation

## Data sources

Every object's catalog entry is cross-checked against the JPL Small-Body Database, the Lunar and Planetary Institute's Asteroids Radar Archive, Johnston's Archive, and the Pravec/Ondřejov binary asteroid database. Every value shown on an object's card in the dashboard carries a hover citation showing exactly which of these it came from.

Observation history (which years an object was observed, how many distinct days, and in which mode — CW, DD, or both, down to the DD baud/resolution code) is tracked separately in an Arecibo processing-log spreadsheet, shown as a per-year table on each object's card. That log only covers a subset of objects/years, so a blank Mode/resolution cell means "not confirmed," not "not observed" — the Years Observed count itself comes from the broader historical record. Objects that aren't in the processing log at all get no per-year table, and their Years Observed hover says so explicitly rather than implying a source it doesn't have.

## Filtering the catalog

Beyond the category chips (NEA, PHA, MBA, Comet, Moons, Planets, Spacecraft) and free-text search, the table can be filtered by detection status, presence of a matched reference, "With product" (has a downloadable CW/delay-Doppler product in this repository), binary/multiple systems, observing **Mode** (CW / DD / CW+DD), and **DD resolution** (the processing-log baud codes: p05, p1, p2, p5, u1, u2, u4, other). A live "Objects matching selection" count next to the search box reflects the combined effect of every active filter.

## How the dashboard is built

The dashboard is generated from a set of Python scripts (not included in this repo — they live in the main project directory) that merge several source spreadsheets and API-based literature searches (OpenAlex, Crossref, NASA ADS) into one master catalog, then render a single self-contained HTML file referencing the images in this repository by URL.

## List of Revisions submitted from TeamRadar members

Every submission made through [`TeamRadar-Revision.html`](TeamRadar-Revision.html) lands as its own row in a shared spreadsheet — one row per object edited, with real columns (object, comment, have-data flag, Re-visit flag, reference approvals, new references submitted).

**[Open the submissions table →](https://docs.google.com/spreadsheets/d/1cJbV9h_u0ngABVx5Y31ugmUpYn2v9S80ThVLG6TUplI/edit)** (access request required)
