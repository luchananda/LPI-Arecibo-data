# TeamRadar-Revision

An experimental, interactive companion page for FSI/Arecibo team members to review individual catalog objects and submit corrections — without needing edit access to the main catalog or its underlying data files.

**Live page:** https://luchananda.github.io/LPI-Arecibo-data/TeamRadar-Revision.html
**Submissions table (Google Sheet, access request required):** https://docs.google.com/spreadsheets/d/1cJbV9h_u0ngABVx5Y31ugmUpYn2v9S80ThVLG6TUplI/edit
**Google Form backing it:** https://docs.google.com/forms/d/1HOx_QFzDlwBLChJzIx4teYQr7765MJBS5sB9qHENZMY/edit

## What this is, and what it isn't

This is a **separate, preview page** — it does not replace, link from, or automatically update [`dashboard.html`](../dashboard.html), the live public dashboard. It's a review layer for collecting team feedback that gets merged into the main catalog by hand later, once reviewed.

## What it lets a reviewer do

- Identify themselves by initials (required) and, optionally, an email for one-time updates
- Leave a comment on one object, or select several at once and apply the same comment to all of them
- Flag "I have data for this object" or "add to Re-visit list", single or multi-select
- Approve or reject each of an object's existing references, either from that object's own detail card, or from a pop-out panel that lists several selected objects' references side by side (so a reviewer isn't stuck reviewing one object at a time)
- Submit a new reference for an object (DOI preferred, falling back to first author + year, or a topic/title if that's all that's known)
- Report a separate list of objects they have for cross-referencing, with an optional link, or a note to email it in directly

## How it was built

`build_teamradar.py` (in this folder) doesn't rebuild the catalog from scratch — it **post-processes the already-built `dashboard.html`** (a single string-replace pass), so it inherits the exact same object data, grid, table, search, and detail-card modal as the live dashboard for free. On top of that it injects:

- A top "Add your review" panel (initials/email, comment + bulk-apply toolbar, the cross-referencing-list question, Preview/Submit)
- A checkbox "select" column in the object table, wired to the bulk toolbar
- Inside each object's detail popup: a compact "quick review" strip (comment, have-data, Re-visit) placed right under the image/data row, plus a fuller "Reference verification" section (approve/reject per reference, add-new-reference form) further down
- The multi-object "Review references for selected…" pop-out, sharing the same approve/reject logic and the same in-memory `teamData` store as the per-object popup, so edits made either way stay in sync

### Where submissions go

GitHub Pages is a static site — it can't safely receive or store form submissions (doing that from client-side JavaScript would mean embedding a write-access credential directly in the page's source, visible to anyone). Instead, the page's Submit button sends a background `POST` straight to a dedicated Google Form's public submission endpoint (a standard, credential-free technique; Google Forms are designed to accept this). Each Form question maps to one column in the linked Google Sheet.

Because one session can touch several objects, the page submits **one Form response per object edited** (not one blob for the whole session), so the Sheet reads as an actual table — Object, Comment, Have data, Re-visit, References, New references — rather than a single JSON cell per submission. The initials/email/cross-referencing-list answers are repeated on every row from the same session.

### What happens after a submission

Nothing, automatically. The Sheet is the raw intake — reviewing it and folding accepted changes back into `FINAL_TABLE.json` (and rebuilding `dashboard.html`) is a manual step for later.
