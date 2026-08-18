# Arecibo Observatory Planetary Radar Object Catalog

Data repository backing the interactive dashboard cataloging every solar system object detected by the Arecibo Observatory's planetary radar system between 1978 and 2020 — 1,039 objects spanning near-Earth asteroids, potentially hazardous asteroids, main-belt asteroids, comets, planets, moons, rings, and spacecraft.

**Live dashboard:** https://luchananda.github.io/LPI-Arecibo-data/dashboard.html

## What's in this repository

- `dashboard.html` — the self-contained interactive dashboard (also mirrored to a Claude Artifact for preview, but this GitHub Pages copy is the canonical, fully-working version — Claude's Artifact hosting blocks external images, so this is the one to share)
- `curated/` — hand-picked public-domain/Creative-Commons images (NASA, NRAO) used for objects that don't have their own LPI radar imagery, mainly the planets, the Moon, and Saturn's rings
- All other folders (`Continuous Wave/`, `Delay Doppler/`, etc.) — compressed radar product images harvested from the [LPI Asteroids Radar Archive](https://www.lpi.usra.edu/resources/asteroids/), organized by product type and object designation

## Data sources

Every object's catalog entry is cross-checked against the JPL Small-Body Database, the Lunar and Planetary Institute's Asteroids Radar Archive, Johnston's Archive, and the Pravec/Ondřejov binary asteroid database. Every value shown on an object's card in the dashboard carries a hover citation showing exactly which of these it came from.

## How the dashboard is built

The dashboard is generated from a set of Python scripts (not included in this repo — they live in the main project directory) that merge several source spreadsheets and API-based literature searches (OpenAlex, Crossref, NASA ADS) into one master catalog, then render a single self-contained HTML file referencing the images in this repository by URL.
