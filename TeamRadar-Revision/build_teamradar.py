#!/usr/bin/env python3
"""Build TeamRadar-Revision.html: a PREVIEW of the interactive team-review
page, built by post-processing the already-built dashboard.html (reuses its
object data/table/grid/modal wholesale, adds a team-input layer on top).

This is a local preview only - the Submit button is a stub. Nothing is wired
to a real backend yet (that happens once the Google Form exists and its
field IDs are known)."""

PROJ = '/Users/floridaspaceinstitute/Documents/Radar/Catalogue4Webpage'
html = open(f'{PROJ}/dashboard.html', encoding='utf-8').read()

# 1) title + banner
html = html.replace(
    '<meta charset="utf-8">',
    '<meta charset="utf-8">\n<title>TeamRadar-Revision</title>',
    1)
html = html.replace(
    '<h1>Arecibo Observatory &mdash; Planetary Radar Object Catalog</h1>',
    '<h1>TeamRadar-Revision</h1>\n'
    '<div class="tr-banner">TEAM REVIEW BUILD &mdash; this is a staging version for team data review, '
    'separate from the live dashboard above. Submissions here ARE saved live to a shared Google Sheet '
    '(ask apophis@ucf.edu for access). They do not update the catalog automatically &mdash; a person '
    'reviews the sheet and applies accepted changes to the main catalog by hand.</div>',
    1)

# 2) contact box: 2pt bigger, centered
html = html.replace(
    '<div class="ao-contact">Have questions',
    '<div class="ao-contact" style="font-size:15px;text-align:center;">Have questions',
    1)

# 3) table header: add a select checkbox column
html = html.replace(
    '<th data-k="num">Number</th>',
    '<th style="width:30px;"><input type="checkbox" id="tr-select-all" title="Select all on this page"></th>\n            <th data-k="num">Number</th>',
    1)

# 4) row template: add a select checkbox cell per row
html = html.replace(
    "return '<tr' + trAttrs + '><td>' + esc(r.num) + '</td><td>' + nameCell",
    "return '<tr' + trAttrs + '><td><input type=\"checkbox\" class=\"tr-row-select\" data-target=\"' + esc(r.target) + '\" onclick=\"event.stopPropagation()\" ' + (teamData[r.target] && teamData[r.target].selected ? 'checked' : '') + '></td><td>' + esc(r.num) + '</td><td>' + nameCell",
    1)
html = html.replace(
    "var trAttrs = ' class=\"ao-row-click\" data-target=\"' + esc(r.target) + '\" tabindex=\"0\"';",
    "var _trTd = teamData[r.target];\n"
    "      var _trMarked = _trTd && (_trTd.comment || _trTd.hasData || _trTd.revisit || Object.keys(_trTd.refApprovals || {}).length || (_trTd.newRefs || []).length);\n"
    "      var _trSelected = _trTd && _trTd.selected;\n"
    "      var trAttrs = ' class=\"ao-row-click' + (_trMarked ? ' tr-marked' : '') + (_trSelected ? ' tr-selected' : '') + '\" data-target=\"' + esc(r.target) + '\" tabindex=\"0\"';",
    1)

TEAM_PANEL = '''
    <div class="ao-panel tr-panel">
      <h2 class="ao-h2-lg">Add your review</h2>
      <div class="tr-grid">
        <div class="tr-field">
          <label>Your initials <span class="tr-req">*</span></label>
          <select id="tr-initials">
            <option value="">Select&hellip;</option>
            <option>LFZM</option>
            <option value="__other">My initials aren&rsquo;t listed</option>
          </select>
          <input id="tr-initials-other" type="text" placeholder="Type your initials" style="display:none;margin-top:6px;">
        </div>
        <div class="tr-field">
          <label>Your email <span class="tr-hint">(only needed the first time, so we can send you updates)</span></label>
          <input id="tr-email" type="email" placeholder="you@example.com">
        </div>
      </div>
      <div class="tr-field" style="margin-top:14px;">
        <label>Comment <span class="fl-help" tabindex="0" data-tip="Add here any comments about the data">i</span></label>
        <textarea id="tr-comment" rows="2" placeholder="Type a comment, select one or more objects in the table below (checkbox column), then click Apply."></textarea>
      </div>
      <div class="tr-toolbar">
        <span id="tr-sel-count">0 objects selected</span>
        <button class="toggle-btn" id="tr-apply-comment">Apply comment to selected</button>
        <button class="toggle-btn" id="tr-apply-hasdata">Mark selected: &ldquo;I have data for this object&rdquo;</button>
        <button class="toggle-btn" id="tr-apply-revisit">Flag selected for Re-visit</button>
        <button class="toggle-btn" id="tr-apply-approve-refs">Approve all listed references for selected</button>
        <button class="toggle-btn" id="tr-review-refs-btn">Review references for selected&hellip;</button>
        <button class="toggle-btn" id="tr-clear-selection">Clear selection</button>
        <span class="tr-hint" id="tr-bulk-status"></span>
      </div>
      <div id="tr-multiref-panel" style="display:none;"></div>
      <div class="tr-field" style="margin-top:16px;">
        <label>Do you have a list of objects to add for cross-referencing, not included here?</label>
        <div class="tr-radio-row">
          <label><input type="radio" name="tr-haslist" value="yes" id="tr-haslist-yes"> Yes! I have a list to add</label>
          <label><input type="radio" name="tr-haslist" value="no" id="tr-haslist-no"> No, I don&rsquo;t have anything else</label>
        </div>
        <div id="tr-haslist-yes-box" style="display:none;margin-top:8px;">
          <div class="tr-hint">If you can, please send us an email with the file to <a href="mailto:apophis@ucf.edu">apophis@ucf.edu</a>, or include a link to it below.</div>
          <input id="tr-haslist-url" type="url" placeholder="https://&hellip; (optional link to your list)" style="margin-top:6px;">
        </div>
      </div>
      <div class="tr-toolbar" style="margin-top:16px;border-top:1px solid var(--border);padding-top:14px;">
        <button class="toggle-btn" id="tr-preview-btn">Preview my submissions</button>
        <button class="toggle-btn" id="tr-submit-btn">Submit</button>
        <span class="tr-hint" id="tr-submit-status">Submit sends everything above, plus any per-object edits made in each object&rsquo;s detail popup, to the shared spreadsheet.</span>
      </div>
      <div id="tr-preview-out" style="display:none;"></div>
    </div>
'''

_panel_anchor = '<div class="ao-panel">\n    <div class="ao-panel-head-row">\n      <h2 style="margin:0;">Browse the catalog</h2>'
assert html.count(_panel_anchor) == 1, 'Browse-the-catalog panel anchor not found exactly once - update it'
html = html.replace(_panel_anchor, TEAM_PANEL.strip('\n') + '\n\n  ' + _panel_anchor, 1)

TEAM_CSS = '''
.tr-banner { background: #fff3cd; border: 1px solid #e6c766; color: #6b5300; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 8px; margin: 4px 0 16px; }
.tr-panel { border: 2px solid var(--gold); }
.tr-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.tr-field label { display: block; font-size: 12px; font-weight: 700; color: var(--text-secondary); margin-bottom: 4px; }
.tr-field select, .tr-field input[type="text"], .tr-field input[type="email"], .tr-field input[type="url"], .tr-field textarea {
  width: 100%; padding: 7px 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface-1); color: var(--text-primary); font-size: 13px; font-family: inherit;
}
.tr-req { color: #b00020; }
.tr-hint { font-size: 11px; font-weight: 400; color: var(--muted); }
.tr-toolbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
.tr-radio-row { display: flex; gap: 18px; font-size: 13px; margin-top: 4px; }
#tr-preview-out { background: var(--page); border: 1px solid var(--border); border-radius: 8px; padding: 10px; font-size: 12px; max-height: 320px; overflow: auto; margin-top: 10px; }
#tr-preview-out table td, #tr-preview-out table th { padding: 5px 8px; }
#tr-multiref-panel { margin-top: 10px; padding: 10px 12px; border: 1px dashed var(--gold); border-radius: 8px; background: var(--page); max-height: 360px; overflow: auto; }
.tr-multiref-obj { margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.tr-multiref-obj:last-child { margin-bottom: 0; border-bottom: none; padding-bottom: 0; }
.tr-multiref-obj h5 { font-size: 12px; font-weight: 700; margin: 0 0 6px; }
.tr-modal-quick { margin-top: 10px; padding: 8px 10px; border: 1px dashed var(--gold); border-radius: 8px; background: var(--page); font-size: 11px; }
.tr-modal-statusrow { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.tr-modal-quick .tr-field { margin-bottom: 4px; }
.tr-modal-quick .tr-field label { font-size: 10px; margin-bottom: 2px; }
.tr-modal-quick textarea { font-size: 11px; padding: 4px 6px; min-height: 24px; }
.tr-modal-quick label { display: inline-block; margin-right: 14px; font-size: 11px; }
.tr-modal-section { margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--grid); }
.tr-modal-section h4 { font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: var(--text-secondary); margin: 0 0 8px; }
.tr-ref-row { display: flex; align-items: flex-start; gap: 8px; font-size: 12px; margin-bottom: 6px; }
.tr-ref-inline { display: inline-flex; align-items: center; gap: 8px; margin-left: 10px; font-size: 11px; color: var(--text-secondary); }
.tr-ref-inline label { display: inline-flex; align-items: center; gap: 3px; }
.pub-list li[data-ref-i] { display: flex; flex-wrap: wrap; align-items: center; gap: 2px; }
.pub-list li[data-ref-i] .ref-full { flex-basis: 100%; }
.tr-newref-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px; }
.tr-newref-grid input { padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border); font-size: 12px; grid-column: span 1; }
tr.tr-selected td { background: #e3f2fd; }
tr.tr-marked td { background: #fff8e1 !important; }
tr.tr-marked td:first-child { box-shadow: inset 3px 0 0 var(--gold); }
'''
html = html.replace('</style>', TEAM_CSS + '</style>', 1)

TEAM_DATA_INIT = '''  var teamData = {};
  function td(target) { if (!teamData[target]) teamData[target] = {selected:false, comment:'', hasData:false, revisit:false, qcode:'', refApprovals:{}, newRefs:[]}; return teamData[target]; }
'''
_state_anchor = "sortDir: 1, page: 0 };"
assert html.count(_state_anchor) == 1, 'state-object anchor not found exactly once in dashboard.html - update it'
html = html.replace(_state_anchor, _state_anchor + "\n" + TEAM_DATA_INIT, 1)

TEAM_JS = '''
  // Everything typed into the review form (comments, Qcode, flags, ref
  // approvals, initials/email) lives ONLY in this browser tab's memory
  // until you click the main Submit button, which is what actually sends
  // it to the shared Google Sheet. To avoid losing work if the tab is
  // accidentally closed or reloaded before submitting, autosave a copy to
  // this browser's local storage (this device/browser only, not shared)
  // and restore it on load.
  var TR_STORAGE_KEY = 'teamradar_data_v1';
  function trPersist() {
    try {
      localStorage.setItem(TR_STORAGE_KEY, JSON.stringify({
        teamData: teamData,
        initials: document.getElementById('tr-initials').value,
        initialsOther: document.getElementById('tr-initials-other').value,
        email: document.getElementById('tr-email').value,
      }));
    } catch (e) {}
  }
  function trRestore() {
    var saved;
    try { saved = JSON.parse(localStorage.getItem(TR_STORAGE_KEY) || 'null'); } catch (e) { saved = null; }
    if (!saved) return;
    if (saved.teamData) { Object.keys(saved.teamData).forEach(function(t) { teamData[t] = saved.teamData[t]; }); }
    if (saved.initials) {
      var sel = document.getElementById('tr-initials');
      var exists = Array.prototype.some.call(sel.options, function(o) { return o.value === saved.initials; });
      if (!exists && saved.initials !== '__other') {
        var opt = document.createElement('option');
        opt.value = saved.initials; opt.textContent = saved.initials;
        sel.insertBefore(opt, sel.querySelector('option[value="__other"]'));
      }
      sel.value = saved.initials;
    }
    if (saved.email) document.getElementById('tr-email').value = saved.email;
  }
  trRestore();
  setInterval(trPersist, 3000);
  window.addEventListener('beforeunload', trPersist);
  render();
  updateSelCount();

  document.getElementById('tr-initials').addEventListener('change', function(e) {
    document.getElementById('tr-initials-other').style.display = e.target.value === '__other' ? 'block' : 'none';
  });
  document.getElementById('tr-initials-other').addEventListener('blur', function(e) {
    var v = e.target.value.trim();
    if (!v) return;
    var sel = document.getElementById('tr-initials');
    var exists = Array.prototype.some.call(sel.options, function(o) { return o.value.toLowerCase() === v.toLowerCase() && o.value !== '__other'; });
    if (!exists) {
      var opt = document.createElement('option');
      opt.value = v; opt.textContent = v;
      sel.insertBefore(opt, sel.querySelector('option[value="__other"]'));
    }
    sel.value = v;
    e.target.style.display = 'none';
  });
  document.getElementById('tr-haslist-yes').addEventListener('change', function() { document.getElementById('tr-haslist-yes-box').style.display = 'block'; });
  document.getElementById('tr-haslist-no').addEventListener('change', function() { document.getElementById('tr-haslist-yes-box').style.display = 'none'; });

  function selectedTargets() {
    return Object.keys(teamData).filter(function(t) { return teamData[t].selected; });
  }
  function updateSelCount() {
    document.getElementById('tr-sel-count').textContent = selectedTargets().length + ' objects selected';
  }
  document.getElementById('ao-tbody').addEventListener('change', function(e) {
    if (!e.target.classList.contains('tr-row-select')) return;
    td(e.target.getAttribute('data-target')).selected = e.target.checked;
    e.target.closest('tr').classList.toggle('tr-selected', e.target.checked);
    updateSelCount();
  });
  document.getElementById('tr-select-all').addEventListener('change', function(e) {
    document.querySelectorAll('.tr-row-select').forEach(function(cb) {
      cb.checked = e.target.checked;
      td(cb.getAttribute('data-target')).selected = e.target.checked;
      cb.closest('tr').classList.toggle('tr-selected', e.target.checked);
    });
    updateSelCount();
  });
  document.getElementById('tr-clear-selection').addEventListener('click', function() {
    // Selection can span pages, so clear it in teamData directly - not
    // just the checkboxes currently visible on this page.
    selectedTargets().forEach(function(t) { td(t).selected = false; });
    document.getElementById('tr-select-all').checked = false;
    document.getElementById('tr-bulk-status').textContent = 'Selection cleared.';
    render();
    updateSelCount();
  });
  document.getElementById('tr-apply-comment').addEventListener('click', function() {
    var c = document.getElementById('tr-comment').value.trim();
    if (!c) { alert('Type a comment first.'); return; }
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first (checkbox column on the left of the table).'); return; }
    sel.forEach(function(t) {
      var d = td(t);
      // Don't clobber a comment already typed on the object's own card -
      // append instead, unless this exact text is already there (so
      // re-clicking Apply on the same selection doesn't duplicate it).
      if (d.comment && d.comment.indexOf(c) === -1) { d.comment = d.comment + '\\n' + c; }
      else if (!d.comment) { d.comment = c; }
    });
    document.getElementById('tr-bulk-status').textContent = 'Comment applied to ' + sel.length + ' object(s) - highlighted below.';
    var btn = this;
    btn.classList.add('active');
    setTimeout(function() { btn.classList.remove('active'); }, 1200);
    render();
  });
  // Toggle buttons: click turns the flag ON for the current selection and
  // presses the button; click again turns it back OFF (removes the flag)
  // and un-presses it. The button's pressed state is independent of
  // selection - it just remembers which way it last applied.
  function wireToggleBtn(id, onToggle) {
    var btn = document.getElementById(id);
    btn.addEventListener('click', function() {
      var sel = selectedTargets();
      if (!sel.length) { alert('Select at least one object first.'); return; }
      var nowActive = !btn.classList.contains('active');
      btn.classList.toggle('active', nowActive);
      onToggle(sel, nowActive);
      render();
    });
  }
  wireToggleBtn('tr-apply-hasdata', function(sel, on) {
    sel.forEach(function(t) { td(t).hasData = on; });
    document.getElementById('tr-bulk-status').textContent = (on ? 'Marked ' : 'Unmarked ') + sel.length + ' object(s) as having data - highlighted below.';
  });
  wireToggleBtn('tr-apply-revisit', function(sel, on) {
    sel.forEach(function(t) { td(t).revisit = on; });
    document.getElementById('tr-bulk-status').textContent = (on ? 'Flagged ' : 'Unflagged ') + sel.length + ' object(s) for Re-visit - highlighted below.';
  });
  wireToggleBtn('tr-apply-approve-refs', function(sel, on) {
    var refCount = 0;
    sel.forEach(function(t) {
      var row = DATA.filter(function(r) { return r.target === t; })[0] || {};
      (row.refsFull || []).forEach(function(rf, i) { if (on) { td(t).refApprovals[i] = true; } else { delete td(t).refApprovals[i]; } refCount++; });
    });
    document.getElementById('tr-bulk-status').textContent = (on ? 'Approved ' : 'Un-approved ') + refCount + ' reference(s) across ' + sel.length + ' object(s) - highlighted below.';
  });

  // Shared reference approve/reject markup + wiring - used both by the
  // per-object modal and the multi-object "Review references" pop-out, so
  // the checkboxes behave identically (and write into the same teamData
  // store) no matter which surface you check them from.
  function refsHtmlFor(target) {
    var row = DATA.filter(function(r) { return r.target === target; })[0] || {};
    var d = td(target);
    var refsFull = row.refsFull || [];
    if (!refsFull.length) return '<div class="tr-hint">No references listed for this object yet.</div>';
    var combined = (row.refs || []).map(function(rf, i) { return {label: rf.label, url: rf.url, year: rf.year, citation: (refsFull[i] || {}).citation || null, i: i}; });
    // Chronological order, SBDB pinned first - same rule the object's own
    // card and the public dashboard use, so [N] means the same reference
    // no matter which of the three views a reviewer is looking at.
    combined.sort(function(a, b) {
      var ay = a.year ? parseInt(a.year, 10) : Infinity, by = b.year ? parseInt(b.year, 10) : Infinity;
      return ay - by;
    });
    var numbered = (row.link ? [{sbdb: true, label: 'JPL SBDB', url: row.link}] : []).concat(combined);
    return '<ul class="pub-list">' + numbered.map(function(ref, idx) {
      var num = '[' + (idx + 1) + '] ';
      if (ref.sbdb) {
        return '<li>' + num + '<a href="' + esc(ref.url) + '" target="_blank" rel="noopener">' + esc(ref.label) + '</a></li>';
      }
      var checked = d.refApprovals[ref.i];
      var labelHtml = ref.url ? '<a href="' + esc(ref.url) + '" target="_blank" rel="noopener">' + esc(ref.label) + '</a>' : esc(ref.label);
      var urlLine = ref.url ? ' <a href="' + esc(ref.url) + '" target="_blank" rel="noopener">' + esc(ref.url) + '</a>' : '';
      var arrow = ref.citation ? ' <span class="ref-expand open" tabindex="0" role="button" aria-label="Show full reference">▾</span><div class="ref-full open">' + esc(ref.citation) + urlLine + '</div>' : '';
      return '<li data-ref-i="' + ref.i + '">' + num + labelHtml + arrow +
        '<span class="tr-ref-inline"><label><input type="checkbox" class="tr-ref-approve" data-target="' + esc(target) + '" data-i="' + ref.i + '" ' + (checked === true ? 'checked' : '') + '> approve</label>' +
        '<label><input type="checkbox" class="tr-ref-reject" data-target="' + esc(target) + '" data-i="' + ref.i + '" ' + (checked === false ? 'checked' : '') + '> reject</label></span></li>';
    }).join('') + '</ul>';
  }
  function wireRefCheckboxes(container) {
    container.querySelectorAll('.tr-ref-approve').forEach(function(cb) {
      cb.addEventListener('change', function(e) {
        var t = e.target.getAttribute('data-target'), i = e.target.getAttribute('data-i');
        if (!e.target.checked) return;
        td(t).refApprovals[i] = true;
        var rej = container.querySelector('.tr-ref-reject[data-target="' + t + '"][data-i="' + i + '"]');
        if (rej) rej.checked = false;
      });
    });
    container.querySelectorAll('.tr-ref-reject').forEach(function(cb) {
      cb.addEventListener('change', function(e) {
        var t = e.target.getAttribute('data-target'), i = e.target.getAttribute('data-i');
        if (!e.target.checked) return;
        td(t).refApprovals[i] = false;
        var app = container.querySelector('.tr-ref-approve[data-target="' + t + '"][data-i="' + i + '"]');
        if (app) app.checked = false;
      });
    });
  }
  document.getElementById('tr-review-refs-btn').addEventListener('click', function() {
    var panel = document.getElementById('tr-multiref-panel');
    if (panel.style.display !== 'none') { panel.style.display = 'none'; this.classList.remove('active'); return; }
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first (checkbox column on the left of the table).'); return; }
    panel.innerHTML = sel.map(function(t) {
      var row = DATA.filter(function(r) { return r.target === t; })[0] || {};
      var title = (row.num ? row.num + ' ' : '') + (row.name || t);
      return '<div class="tr-multiref-obj"><h5>' + esc(title) + '</h5>' + refsHtmlFor(t) + '</div>';
    }).join('');
    wireRefCheckboxes(panel);
    panel.style.display = 'block';
    this.classList.add('active');
  });

  function collectSubmission() {
    var initialsSel = document.getElementById('tr-initials').value;
    var initials = initialsSel === '__other' ? document.getElementById('tr-initials-other').value.trim() : initialsSel;
    var haslist = (document.querySelector('input[name="tr-haslist"]:checked') || {}).value || null;
    var perObject = Object.keys(teamData).filter(function(t) {
      var d = teamData[t];
      return d.comment || d.hasData || d.revisit || d.qcode || Object.keys(d.refApprovals).length || d.newRefs.length;
    }).map(function(t) { return Object.assign({target: t}, teamData[t]); });
    return {
      initials: initials, email: document.getElementById('tr-email').value.trim(),
      hasAdditionalList: haslist, additionalListUrl: document.getElementById('tr-haslist-url').value.trim(),
      objects: perObject,
    };
  }
  function refSummary(d) {
    var app = Object.keys(d.refApprovals).filter(function(i) { return d.refApprovals[i] === true; }).length;
    var rej = Object.keys(d.refApprovals).filter(function(i) { return d.refApprovals[i] === false; }).length;
    var parts = [];
    if (app) parts.push(app + ' approved');
    if (rej) parts.push(rej + ' rejected');
    if (d.newRefs.length) parts.push(d.newRefs.length + ' new');
    return parts.join(', ') || '&mdash;';
  }
  document.getElementById('tr-preview-btn').addEventListener('click', function() {
    var out = document.getElementById('tr-preview-out');
    var s = collectSubmission();
    out.style.display = 'block';
    var html = '<table class="ao-table"><tbody>' +
      '<tr><td><b>Initials</b></td><td>' + esc(s.initials || '(missing - required)') + '</td></tr>' +
      '<tr><td><b>Email</b></td><td>' + (s.email ? esc(s.email) : '&mdash;') + '</td></tr>' +
      '<tr><td><b>Additional list?</b></td><td>' + esc(s.hasAdditionalList || '(not answered)') + (s.additionalListUrl ? ' &mdash; ' + esc(s.additionalListUrl) : '') + '</td></tr>' +
      '</tbody></table>';
    if (s.objects.length) {
      html += '<table class="ao-table" style="margin-top:10px;"><thead><tr><th>Object</th><th>Comment</th><th>Have data</th><th>Re-visit</th><th>Qcode</th><th>References</th></tr></thead><tbody>' +
        s.objects.map(function(o) {
          return '<tr><td>' + esc(o.target) + '</td><td>' + (o.comment ? esc(o.comment) : '&mdash;') + '</td><td>' + (o.hasData ? 'Yes' : '&mdash;') +
            '</td><td>' + (o.revisit ? 'Yes' : '&mdash;') + '</td><td>' + (o.qcode ? esc(o.qcode) : '&mdash;') + '</td><td>' + refSummary(o) + '</td></tr>';
        }).join('') + '</tbody></table>';
    } else {
      html += '<div class="tr-hint" style="margin-top:10px;">No per-object edits yet &mdash; click into an object to add comments, mark data, or review references.</div>';
    }
    out.innerHTML = html;
  });

  // -- real submission, POSTed to the TeamRadar-Revision Submissions Google Form --
  // One Form submission = one Sheet row. Since a session can touch several
  // objects, we submit one row PER OBJECT edited (all sharing the same
  // initials/email/list-answer columns) so the Sheet reads as a real table -
  // Object/Comment/Have data/Re-visit/References as actual columns, not one
  // JSON blob per session.
  var GFORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSeFvyoNg7sQvdZ6CuD10oW07DDTPIRMdhrDx1oRRUc9q2PTiw/formResponse';
  var GFORM_ENTRIES = {
    initials: 'entry.1519103522',
    email: 'entry.1826505028',
    hasAdditionalList: 'entry.1132650262',
    additionalListUrl: 'entry.77071328',
    object: 'entry.796976015',
    comment: 'entry.624306432',
    hasData: 'entry.233549053',
    revisit: 'entry.1209227406',
    references: 'entry.1438340613',
    newRefs: 'entry.819246442',
    qcode: 'entry.1407087598',
  };
  function refsPlainText(o) {
    // Log which references, not just a count - a count alone isn't enough
    // to apply these decisions back to the catalog later without reopening
    // every object's card to guess which reference the reviewer meant.
    var row = DATA.filter(function(r) { return r.target === o.target; })[0] || {};
    var refs = row.refs || [];
    var approved = [], rejected = [];
    Object.keys(o.refApprovals).forEach(function(i) {
      var label = (refs[i] || {}).label || ('reference ' + (parseInt(i, 10) + 1));
      if (o.refApprovals[i] === true) approved.push(label);
      else if (o.refApprovals[i] === false) rejected.push(label);
    });
    var parts = [];
    if (approved.length) parts.push('Approved: ' + approved.join('; '));
    if (rejected.length) parts.push('Rejected: ' + rejected.join('; '));
    return parts.join(' | ');
  }
  function newRefsPlainText(o) {
    return (o.newRefs || []).map(function(r) {
      return [r.doi, r.author, r.year, r.topic].filter(Boolean).join(' / ');
    }).join(' | ');
  }
  document.getElementById('tr-submit-btn').addEventListener('click', function() {
    var s = collectSubmission();
    if (!s.initials) { alert('Your initials are required before submitting.'); return; }
    var status = document.getElementById('tr-submit-status');
    var rows = s.objects.length ? s.objects : [null];
    status.textContent = 'Submitting…';
    Promise.all(rows.map(function(o) {
      var body = new URLSearchParams();
      body.set(GFORM_ENTRIES.initials, s.initials);
      body.set(GFORM_ENTRIES.email, s.email);
      body.set(GFORM_ENTRIES.hasAdditionalList, s.hasAdditionalList || '');
      body.set(GFORM_ENTRIES.additionalListUrl, s.additionalListUrl);
      body.set(GFORM_ENTRIES.object, o ? o.target : '(session only - no object edits)');
      body.set(GFORM_ENTRIES.comment, o ? (o.comment || '') : '');
      body.set(GFORM_ENTRIES.hasData, o && o.hasData ? 'Yes' : '');
      body.set(GFORM_ENTRIES.revisit, o && o.revisit ? 'Yes' : '');
      body.set(GFORM_ENTRIES.references, o ? refsPlainText(o) : '');
      body.set(GFORM_ENTRIES.newRefs, o ? newRefsPlainText(o) : '');
      body.set(GFORM_ENTRIES.qcode, o ? (o.qcode || '') : '');
      return fetch(GFORM_URL, {method: 'POST', mode: 'no-cors', body: body});
    })).then(function() {
      status.textContent = 'Submitted ' + rows.length + ' row(s) – thank you! Form is reset and ready for your next search (initials/email kept).';
      Object.keys(teamData).forEach(function(t) { delete teamData[t]; });
      document.getElementById('tr-comment').value = '';
      document.querySelectorAll('input[name="tr-haslist"]').forEach(function(r) { r.checked = false; });
      document.getElementById('tr-haslist-yes-box').style.display = 'none';
      document.getElementById('tr-haslist-url').value = '';
      document.getElementById('tr-multiref-panel').style.display = 'none';
      document.getElementById('tr-preview-out').style.display = 'none';
      document.getElementById('tr-bulk-status').textContent = '';
      ['tr-apply-hasdata', 'tr-apply-revisit', 'tr-apply-approve-refs', 'tr-review-refs-btn'].forEach(function(id) { document.getElementById(id).classList.remove('active'); });
      try { localStorage.removeItem(TR_STORAGE_KEY); } catch (e) {}
      render();
      updateSelCount();
    }).catch(function() { status.textContent = 'Submission failed – check your connection and try again.'; });
  });

  // Instead of re-listing an object's references in a second, separate
  // block, inject approve/reject controls directly onto the numbered
  // reference list the dashboard's own openModal already renders (each
  // <li> carries data-ref-i pointing back to its index in refsFull; the
  // pinned SBDB entry is data-ref-i="-1" and is skipped, since it isn't a
  // matched reference to approve/reject). Keeps the same [N] numbering,
  // link, and expand-arrow the public dashboard uses - only the checkboxes
  // are new.
  function augmentRefList(target, body) {
    var d = td(target);
    var items = body.querySelectorAll('.pub-list li[data-ref-i]');
    items.forEach(function(li) {
      var i = li.getAttribute('data-ref-i');
      if (i === '-1') return;
      var checked = d.refApprovals[i];
      var span = document.createElement('span');
      span.className = 'tr-ref-inline';
      span.innerHTML =
        ' <label><input type="checkbox" class="tr-ref-approve" data-target="' + esc(target) + '" data-i="' + i + '" ' + (checked === true ? 'checked' : '') + '> approve</label>' +
        '<label><input type="checkbox" class="tr-ref-reject" data-target="' + esc(target) + '" data-i="' + i + '" ' + (checked === false ? 'checked' : '') + '> reject</label>' +
        '<span class="fl-help" tabindex="0" data-tip="Approve if this reference correctly applies to this object; reject if it looks wrong.">i</span>';
      li.appendChild(span);
      // In review mode, show the full citation right away - no click needed
      // to verify a reference actually applies to the object.
      var expandIcon = li.querySelector('.ref-expand'), fullDiv = li.querySelector('.ref-full');
      if (expandIcon) expandIcon.classList.add('open');
      if (fullDiv) fullDiv.classList.add('open');
    });
    wireRefCheckboxes(body);
  }

  // -- per-object Team Review section, appended into the existing object modal --
  var _origOpenModal = openModal;
  openModal = function(target) {
    _origOpenModal(target);
    var d = td(target);

    var body = document.getElementById('ao-modal-body');

    // Compact quick-review strip, placed right under the top image/data row
    // (not at the very bottom) so a one-object review doesn't need scrolling
    // past the full reference list just to leave a comment or flag it.
    var quickHtml = '<div class="tr-modal-quick">' +
      '<div class="tr-modal-statusrow"><button class="toggle-btn' + (d.selected ? ' active' : '') + '" id="tr-modal-select">' + (d.selected ? '✓ Selected for review' : 'Select this object for review') + '</button>' +
      '<span id="tr-modal-status" class="tr-hint"></span></div>' +
      '<div class="tr-field"><label>Comment <span class="fl-help" tabindex="0" data-tip="Add here any comments about the data">i</span></label>' +
      '<textarea id="tr-modal-comment" rows="1">' + esc(d.comment) + '</textarea></div>' +
      '<label><input type="checkbox" id="tr-modal-hasdata" ' + (d.hasData ? 'checked' : '') + '> I have data for this object</label>' +
      '<label><input type="checkbox" id="tr-modal-revisit" ' + (d.revisit ? 'checked' : '') + '> Add to Re-visit list</label>' +
      '<label>Qcode <span class="fl-help" tabindex="0" data-tip="Suggest a corrected quality code, 1 (poor) to 5 (excellent)">i</span> ' +
      '<select id="tr-modal-qcode" style="width:auto;display:inline-block;padding:2px 6px;">' +
      '<option value="">&ndash;</option>' + [1, 2, 3, 4, 5].map(function(n) { return '<option value="' + n + '" ' + (String(d.qcode) === String(n) ? 'selected' : '') + '>' + n + '</option>'; }).join('') +
      '</select></label>' +
      '</div>';
    var modalTop = body.querySelector('.ao-modal-top');
    if (modalTop) { modalTop.insertAdjacentHTML('afterend', quickHtml); } else { body.insertAdjacentHTML('beforeend', quickHtml); }

    // Live status line: makes it explicit that field edits are captured
    // in this browser tab as soon as they're typed/checked (no separate
    // save button - same as the comment box always worked), and exactly
    // what will go out when the main Submit button is clicked.
    function updateCardStatus() {
      var touched = d.comment || d.hasData || d.revisit || d.qcode || Object.keys(d.refApprovals).length || d.newRefs.length;
      document.getElementById('tr-modal-status').innerHTML = touched
        ? '✓ Saved in this browser tab &mdash; will be sent to the shared Sheet when you click <b>Submit</b> below.'
        : 'No edits yet for this object.';
    }
    updateCardStatus();
    document.getElementById('tr-modal-select').addEventListener('click', function() {
      d.selected = !d.selected;
      this.classList.toggle('active', d.selected);
      this.textContent = d.selected ? '✓ Selected for review' : 'Select this object for review';
      var tableCb = document.querySelector('.tr-row-select[data-target="' + CSS.escape(target) + '"]');
      if (tableCb) { tableCb.checked = d.selected; tableCb.closest('tr').classList.toggle('tr-selected', d.selected); }
      updateSelCount();
    });

    augmentRefList(target, body);

    // insertAdjacentHTML (not body.innerHTML +=) - the += form re-parses the
    // ENTIRE body, silently destroying every listener attached to existing
    // children (the Select button above, and the reference approve/reject
    // checkboxes from augmentRefList) even though they keep looking correct
    // afterward, since serialized HTML round-trips structure but not
    // listeners. This was a real, previously-undetected bug.
    body.insertAdjacentHTML('beforeend', '<div class="tr-modal-section">' +
      '<span class="fl-help term-help" tabindex="0" data-tip="Preferred: a DOI. If you don\\u2019t have one, the first author\\u2019s last name, publication year if known, or a topic/title so we can find it.">Add a new reference</span>' +
      '<div class="tr-newref-grid">' +
      '<input type="text" id="tr-newref-doi" placeholder="DOI (preferred)">' +
      '<input type="text" id="tr-newref-author" placeholder="First author last name">' +
      '<input type="text" id="tr-newref-year" placeholder="Year (if known)">' +
      '<input type="text" id="tr-newref-topic" placeholder="Topic / title (if no DOI/author)">' +
      '</div><button class="toggle-btn" id="tr-add-newref" style="margin-top:8px;">Add reference to this object\\u2019s card</button>' +
      '<div id="tr-newref-list" style="margin-top:6px;font-size:12px;"></div>' +
      '</div>');

    document.getElementById('tr-modal-comment').addEventListener('input', function(e) { d.comment = e.target.value; updateCardStatus(); });
    document.getElementById('tr-modal-hasdata').addEventListener('change', function(e) { d.hasData = e.target.checked; updateCardStatus(); });
    document.getElementById('tr-modal-revisit').addEventListener('change', function(e) { d.revisit = e.target.checked; updateCardStatus(); });
    document.getElementById('tr-modal-qcode').addEventListener('change', function(e) { d.qcode = e.target.value; updateCardStatus(); });
    body.addEventListener('change', function(e) {
      if (e.target.classList.contains('tr-ref-approve') || e.target.classList.contains('tr-ref-reject')) updateCardStatus();
    });
    document.getElementById('tr-add-newref').addEventListener('click', function() {
      var ref = {
        doi: document.getElementById('tr-newref-doi').value.trim(),
        author: document.getElementById('tr-newref-author').value.trim(),
        year: document.getElementById('tr-newref-year').value.trim(),
        topic: document.getElementById('tr-newref-topic').value.trim(),
      };
      if (!ref.doi && !ref.author && !ref.topic) { alert('Add at least a DOI, author, or topic/title.'); return; }
      d.newRefs.push(ref);
      document.getElementById('tr-newref-list').textContent = d.newRefs.length + ' new reference(s) queued for this object.';
      ['doi', 'author', 'year', 'topic'].forEach(function(f) { document.getElementById('tr-newref-' + f).value = ''; });
      updateCardStatus();
    });
  };
'''
html = html.replace('})();', TEAM_JS + '\n})();', 1)

open(f'{PROJ}/TeamRadar-Revision.html', 'w', encoding='utf-8').write(html)
print(f'Saved TeamRadar-Revision.html: {len(html):,} bytes')
