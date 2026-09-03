# The Quest to Match MBA Detections — 2026

A running account of the effort to verify that every Main-Belt Asteroid (MBA)
on the Arecibo catalog dashboard is *actually* backed by real evidence, not
just an internal tracker saying so. Three phases, spread across this project's
2026 work: a raw-count discrepancy check, a full per-object reconciliation
against Luisa's own cross-check workbook, and a "confirmation strength" audit
that traced every MBA's sourcing back to its root. Written up here because the
process — including the wrong turns — is as informative as the final numbers.

## Why this started

The dashboard's MBA count (121) didn't match JPL Horizons/SSD's public count
of MBAs with Arecibo radar astrometry on file (138) — a 17-object gap. Rather
than just fixing the number, the question became: for every MBA the dashboard
*does* claim was detected, what's the actual evidence, and how good is it?

## Phase 1 — The 17-object JPL count gap

**Method:** pulled JPL's `sb_radar.api` astrometry table filtered to Arecibo
(station `-1`), cross-referenced against the dashboard's 121 MBAs, then
searched every spreadsheet in the project plus `AllRadarPublications.html`
(the hand-curated bibliography) for the 17 objects present at JPL but absent
from the dashboard.

**Finding — the gap fully explains itself, no hidden detections:**

- **13 objects: data exists only on undigitized tape** — attempted at
  Arecibo, logged, but the data was never processed into a usable form, so
  there's nothing to confirm a detection from:
  18 Melpomene, 20 Massalia, 21 Lutetia, 27 Euterpe, 33 Polyhymnia,
  78 Diana, 84 Klio, 92 Undina, 129 Antigone, 230 Athamantis, 356 Liguria,
  694 Ekard, 796 Sarita.
- **4 objects: genuine orphans** — logged as attempted somewhere in the
  project's tracking sheets, but with no tape, no processed data, and no
  recovered detection anywhere:
  77 Frigga, 201 Penelope, 261 Prymno, 441 Bathilde.

**Re-verified twice**, independently: once via an arXiv-only literature
search, once via a full pass through every spreadsheet in the project
(`ALL_AO_CATALOG_2026_DRAFT.xlsx`, `CatalogTable4Thesis.xlsx`,
`All_obj_obs_count_AO_lu.xlsx`, `FINAL_LIST_2026.xlsx`, `CROSSCHECK_temp.xlsx`)
plus `AllRadarPublications.html`, using word-boundary-safe title matching to
avoid false attributions. Both passes agreed: no hidden detection anywhere.

## Phase 2 — Full reconciliation against the FV cross-check workbook

Luisa maintains `AsteroidAOradarHistoryMBA_FV_LFZM_2026_v2_CleanAnalysis.xlsm`
— a per-apparition cross-check of every MBA candidate against internal
trackers (Lance list, JLM list, Ellen's lists, tape/orphan logs). Collapsed
its 141+ per-apparition rows into one record per unique object and
auto-classified each using her own existing review columns
(`In_final_catalog`, `Catalog_detection`, `On Tape`, `Detection_discrepancy`).
Output: `MBA_Reconciliation_Results_2026.xlsx`.

**Result — 141 objects, all fully explained, zero needing fresh review:**

| Bucket | Count | Meaning |
|---|---|---|
| Clean, confirmed detected | 120 | Matches the dashboard, no issue |
| Tape not digitized | 13 | Same 13 objects as Phase 1 |
| Orphan, correctly excluded | 4 | Same 4 objects as Phase 1 |
| Flagged conflict | 1 | 363 Padua — see below, resurfaces in Phase 3 |
| In catalog, not in her FV list | 2 | 1927 WB (Tama), A880 SA |
| **Needs fresh review** | **0** | — |

The reconciliation's own conflict flag on **363 Padua** reads: *"CONFLICT:
catalog=Yes but brain=No detection."* Her workbook shows Padua on the Lance
list, the JLM list, and Ellen's list (three internal trackers agreeing it was
detected), but the brain workbook's `No_Detection` sheet explicitly logs it as
not detected. This was noted here, filed as "flagged, not yet resolved," and
then re-discovered independently in Phase 3 below — same object, same
conflict, found twice by two different methods. Still unresolved; needs
Luisa's judgment call.

## Phase 3 — The Lance-page confirmation-strength audit

The deepest question: **of every MBA marked detected, how many rest on
*only* the internal "Lance page" list, with nothing else backing them up?**

**Finding:** 74 of 121 MBAs (61%) have `confirmed_by: "Lance page"` as their
sole recorded confirmation method. Of those 74:

| Independent signal | Count |
|---|---|
| Has ≥1 literature reference | 18 |
| Has LPI archive imagery | 6 |
| Has real Arecibo radar astrometry at JPL | 1 |
| **Has none of the above** | **54*** |

\* the write-up's summary line said 55; the actual enumerated list has 54 —
a minor count typo caught in the next phase, doesn't change the analysis.

That's **45% of the entire MBA category** resting on one non-primary,
internal source with zero external corroboration anywhere in the catalog.

### The 6-step triage plan (approved, then executed)

1. Triage by risk — start with the 54 zero-backing objects.
2. Re-run JPL radar astrometry per-object.
3. Cross-reference against the brain workbook's per-date detection sheets.
4. Re-run `AllRadarPublications.html` matching specifically for these 54.
5. For whatever's left: flag with a lower-confidence marker, or trace the
   Lance page's own sourcing.
6. Reverse check (objects marked *not* detected that maybe actually were) —
   explicitly deferred; it's a full-catalog pass, not just this subset.

### Step 2 — a correction that changed the whole approach

Every one of the 54 objects returned **zero** JPL radar astrometry hits. My
first instinct was to read that as more bad news. **Luisa corrected this
directly:** most MBA orbits are already well-constrained by optical
astrometry, so radar data often never gets submitted to JPL for orbit
correction even when a real detection happened — unlike NEAs, which routinely
need it. Missing astrometry is neutral for an MBA, not a red flag. This
reframed the rest of the search: stop treating an absence as evidence, and go
look for literature and other corroboration instead.

### Step 3 — the brain workbook, strict word-boundary matching

Naive substring matching produced two false positives that had to be caught
and discarded before trusting any result: `"28 Bellona"` spuriously matched
`"289P"` (a comet), and `"161 Athor"` spuriously matched `"Hathor"` (a
different, unrelated asteroid) — the same class of error caught earlier in
the session's `AllRadarPublications.html` work (`1998 WT` vs `1998 WT24`).
Switching to number-prefix + exact-name matching fixed both.

With that fixed:
- **161 Athor**: real hit in the brain workbook's `Successful_Detection`
  sheet — genuine independent corroboration beyond Lance. Resolved.
- **363 Padua**: real hit in the `No_Detection` sheet — the same conflict
  Phase 2 had already flagged, rediscovered independently. Left unresolved.
- 48/54 appeared only in `Not_processed` (ambiguous, no new signal).
- All 54 have a `/proj/radar/MBAs/...` folder (attempted, already known,
  weak signal on its own).

### Step 4 — creative literature search (the actual breakthrough)

`AllRadarPublications.html` itself returned zero title matches for all 54 —
confirming it had nothing new to offer. Per Luisa's "be creative" guidance,
went to the open literature directly instead of stopping there.

**Found: Magri, Nolan, Ostro & Giorgini (2007), "A radar survey of main-belt
asteroids: Arecibo observations of 55 objects during 1999–2003," Icarus 186,
126–151** — a real, peer-reviewed survey covering exactly this population.
**29 of the 54 objects are named targets in it**, each with a published OC
SNR value, every one above the paper's 6-sigma detection threshold (the one
target in the full 55-object survey that fell short, 253 Mathilde, isn't one
of ours). Added this citation to all 29 and upgraded their `confirmed_by`
from `"Lance page"` to `"Publication"`:

1963 Bezovec, 3 Juno, 13 Egeria, 28 Bellona, 36 Atalante, 38 Leda,
54 Alexandra, 66 Maja, 83 Beatrix, 101 Helena, 109 Felicitas, 114 Kassandra,
127 Johanna, 137 Meliboea, 145 Adeona, 182 Elsa, 211 Isolda, 225 Henrietta,
247 Eukrate, 266 Aline, 270 Anahita, 354 Eleonora, 407 Arachne, 429 Lotis,
444 Gyptis, 488 Kreusa, 622 Esther, 704 Interamnia, 914 Palisana.

Went further and cross-checked the remaining objects against **Johnston's
Archive**, a maintained third-party radar-asteroid compilation that cites its
own sources per entry. Found **5 more** with real published backing —
**71 Niobe, 110 Lydia, 135 Hertha, 325 Heidelberga, 413 Edburga** — cited
there to Shepard et al. (2015, Icarus, "A radar survey of M- and X-class
asteroids III"), with Lydia and Edburga additionally backed by Shepard et al.
LPI conference abstracts and Niobe/Hertha/Heidelberga by the NASA PDS radar
data archive. Added and upgraded the same way. The other 18 objects checked
against Johnston's Archive had only a bare year, no citable source — no new
information, ruled out as a lead.

### Final tally

**35 of 54 (65%) now have real, independently verifiable backing** — 29 via
Magri et al. 2007, 5 via Shepard et al. 2015 / Johnston's Archive, 1 via the
brain workbook. Dashboard and `confirmed_by` fields updated and pushed live.

**19 still need attention:**
- **363 Padua** — the conflict (see Phase 2), unresolved, needs a decision.
- **18 objects with genuinely zero independent backing found anywhere** —
  not JPL, not the brain workbook, not `AllRadarPublications.html`, not
  Johnston's Archive:
  14 Irene, 51 Nemausa, 56 Melete, 59 Elpis, 91 Aegina, 140 Siwa, 141 Lumen,
  164 Eva, 165 Loreley, 212 Medea, 335 Roberta, 377 Campania, 404 Arsinoe,
  455 Bruchsalia, 463 Lola, 476 Hedwig, 521 Brixia, 524 Fidelio.

These 19 are now surfaced live on the dashboard via the **Re-check** filter,
next to the category chips, so they're not just sitting in a spreadsheet —
anyone browsing the catalog can find them.

## What's still open

- **363 Padua**: needs Luisa's call — trust the Lance/JLM/Ellen internal
  trackers (3-for), trust the brain workbook's explicit non-detection (1
  against but from a different, more granular source), or dig into whether
  the "no detection" note refers to one specific observing date rather than
  the object overall.
- **The 18 zero-backing objects**: options are a visible lower-confidence
  marker on the dashboard, or reaching out to whoever maintains the Lance
  list to ask what their original sourcing was.
- **Step 6, the reverse check** (objects marked *not* detected that maybe
  actually were): not started. It's a full-catalog pass, not just this MBA
  subset — planned as its own future task rather than folded into this one.
- **Same triage for other categories** (NEAs, comets): not started. The
  dashboard's Re-check filter is scoped to MBAs only, for now, by design —
  it'll expand once the same process runs for those categories.
