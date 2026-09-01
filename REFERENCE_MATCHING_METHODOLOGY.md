# How references get matched to objects (and how we avoid false attributions)

This applies to every literature-matching pass on this catalog: the original
OpenAlex/Crossref/ADS searches (`scripts/crossref_lit_search.py`,
`scripts/ads_lit_search.py`, `scripts/deep_lit_search.py`) and the more recent
cross-check against `AllRadarPublications.html`
(`scripts/crosscheck_allradarpubs.py`).

## The rule: title match only, precision over recall

A publication is attributed to a specific catalog object **only when that
object's actual designation, number, or an unambiguous name appears explicitly
in the paper's title** — never from a topical/abstract-only association, and
never because a paper is "about the kind of object this is."

- Matching uses each object's `target`, `name`, `designation`, and `number`
  fields, normalized (uppercased, non-alphanumerics stripped) before
  comparison.
- Short or generic designations are matched with word-boundary-aware patterns,
  not raw substring search. This caught a real collision during the
  AllRadarPublications.html pass: naive substring matching would have
  attributed a paper about "1998 WT24" to the unrelated object "1998 WT" — the
  shorter designation is a literal substring of the longer one. Fixed before
  anything was written.
- General survey papers that don't name a specific object in the title (e.g.
  "A Radar Survey of M- and X-Class Asteroids," "Radar Observations of
  Near-Earth and Main-Belt Asteroids") are **not** attributed to any
  individual object, even though they likely discuss dozens of them by name
  in the body text. The risk of guessing wrong outweighs the citation gained.
  This is a known, intentional gap — see "What this doesn't catch" below.

## Before adding, check for duplicates

Every candidate reference is checked against the object's *existing*
`references` array before being added:
1. First by URL/DOI match (normalized: protocol/trailing-slash/case
   stripped) — the same paper often has a DOI link in one source and an ADS
   link in another.
2. If URLs don't match, by fuzzy title/first-author/year — to catch the same
   paper indexed slightly differently across OpenAlex, Crossref, ADS, and the
   hand-curated publication list.

If an object already has the reference but with no URL, only the URL is
filled in — nothing else about the existing entry is touched.

## Verification, not just automation

A sample of new matches is always spot-checked by hand before being treated
as final (title, authors, and object designation read together to confirm
the match is real, not a string coincidence).

## What this doesn't catch (known, intentional gaps)

- **Survey papers**: a paper's *title* not naming an object doesn't mean the
  paper doesn't discuss it — many radar surveys report results for dozens of
  objects in tables/figures without naming them all in the title. These are
  real references we're not capturing under this rule. Revisiting this would
  mean parsing abstracts/full text per object, a materially bigger and
  riskier task (worth doing deliberately, not as a byproduct of a title-match
  pass).
- **Abstract-level detection confirmation**: matching a title to an object
  confirms the paper is *about* that object, not that the paper's actual
  result was a positive detection (vs. a non-detection, an upper limit, or a
  reanalysis of someone else's data). That is a separate check — see the
  ongoing detection-reconciliation work for whether abstracts should be
  pulled and read for that signal on a case-by-case basis.
