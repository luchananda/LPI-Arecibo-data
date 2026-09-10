# TeamRadar-Revision

An experimental, interactive companion page for FSI/Arecibo team members to review individual catalog objects and submit corrections — without needing edit access to the main catalog or its underlying data files.

**Live page:** https://luchananda.github.io/LPI-Arecibo-data/TeamRadar-Revision.html

**Submissions table (Google Sheet, access request required):** https://docs.google.com/spreadsheets/d/1cJbV9h_u0ngABVx5Y31ugmUpYn2v9S80ThVLG6TUplI/edit

**Google Form backing it:** https://docs.google.com/forms/d/1HOx_QFzDlwBLChJzIx4teYQr7765MJBS5sB9qHENZMY/edit

## What this is, and what it isn't

This is a **separate, preview page** — it does not replace, link from, or automatically update [`dashboard.html`](../dashboard.html), the live public dashboard. It's a review layer for collecting team feedback that gets merged into the main catalog by hand later, once reviewed. It currently covers only the 1,036 confirmed-detection objects in `dashboard.html`; there's no review companion yet for [`dashboard_all.html`](../dashboard_all.html), the 1,356-object all-attempts catalog.

## What it lets a reviewer do

- Identify themselves by initials (required) and, optionally, an email for one-time updates — initials typed via "my initials aren't listed" are added to the dropdown for the rest of the session
- Mark an object "Selected for review" directly from its own card (in addition to the checkbox column in the table), and see a live "saved in this browser tab" status as soon as any field on that card is touched
- Leave a comment on one object, or select several at once (across pages — selection isn't limited to the current 25-row page) and apply the same comment to all of them
- Flag "I have data for this object", "add to Re-visit list", suggest a corrected Qcode (1–5), or approve/reject references — all editable directly on an object's own card, no separate save step
- The bulk toolbar buttons (Mark has-data, Flag revisit, Approve all references) are toggles: pressing one applies it to the current selection and lights up the button; pressing again undoes it. Selected and edited rows stay visibly highlighted in the table so it's clear what's queued
- A "Clear selection" button on the review panel deselects everything at once, without touching any comments or flags already entered
- Approve or reject each of an object's existing references, either from that object's own detail card (checkboxes added right onto the same numbered, linked reference list the public dashboard shows), or from a pop-out panel listing several selected objects' references side by side
- Submit a new reference for an object (DOI preferred, falling back to first author + year, or a topic/title if that's all that's known)
- Report a separate list of objects they have for cross-referencing, with an optional link, or a note to email it in directly
- Work is autosaved to this browser's local storage every few seconds and restored if the tab is closed or reloaded before submitting — it's still only sent to the shared Sheet when Submit is clicked. After a successful submit, the form resets (comments, flags, selections) but keeps your initials and email for the next round

## How it was built

`build_teamradar.py` (in this folder) doesn't rebuild the catalog from scratch — it **post-processes the already-built `dashboard.html`** (a single string-replace pass), so it inherits the exact same object data, grid, table, search, and detail-card modal as the live dashboard for free. On top of that it injects:

- A top "Add your review" panel (initials/email, comment + bulk-apply toolbar, the cross-referencing-list question, Preview/Submit)
- A checkbox "select" column in the object table, wired to the bulk toolbar
- Inside each object's detail popup: a "Select for review" button and live save-status line, a compact "quick review" strip (comment, have-data, Re-visit, Qcode) placed right under the image/data row, plus approve/reject checkboxes injected directly onto the object's existing numbered reference list (same [N] numbering, link, and full citation as the public dashboard - no separate re-listing), and an add-new-reference form further down
- The multi-object "Review references for selected…" pop-out, sharing the same approve/reject logic and the same in-memory `teamData` store as the per-object popup, so edits made either way stay in sync

### Where submissions go

GitHub Pages is a static site — it can't safely receive or store form submissions (doing that from client-side JavaScript would mean embedding a write-access credential directly in the page's source, visible to anyone). Instead, the page's Submit button sends a background `POST` straight to a dedicated Google Form's public submission endpoint (a standard, credential-free technique; Google Forms are designed to accept this). Each Form question maps to one column in the linked Google Sheet.

Because one session can touch several objects, the page submits **one Form response per object edited** (not one blob for the whole session), so the Sheet reads as an actual table — Object, Comment, Have data, Re-visit, References, New references — rather than a single JSON cell per submission. The initials/email/cross-referencing-list answers are repeated on every row from the same session.

### What happens after a submission

Nothing, automatically. The Sheet is the raw intake — reviewing it and folding accepted changes back into `FINAL_TABLE.json` (and rebuilding `dashboard.html`) is a manual step for later.
