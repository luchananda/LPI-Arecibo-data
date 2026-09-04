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
    '<div class="tr-banner">PREVIEW BUILD &mdash; this is a staging version for team data review, '
    'not the live dashboard. Nothing you submit here is saved anywhere yet (the shared-spreadsheet '
    'connection is being set up); reviewed input will eventually flow into the main catalog above.</div>',
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

html = html.replace(
    '<h2 class="ao-h2-lg">Objects by category</h2>',
    TEAM_PANEL.strip('\n') + '\n\n    <h2 class="ao-h2-lg">Objects by category</h2>',
    1)

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
.tr-modal-quick .tr-field { margin-bottom: 4px; }
.tr-modal-quick .tr-field label { font-size: 10px; margin-bottom: 2px; }
.tr-modal-quick textarea { font-size: 11px; padding: 4px 6px; min-height: 24px; }
.tr-modal-quick label { display: inline-block; margin-right: 14px; font-size: 11px; }
.tr-modal-section { margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--grid); }
.tr-modal-section h4 { font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: var(--text-secondary); margin: 0 0 8px; }
.tr-ref-row { display: flex; align-items: flex-start; gap: 8px; font-size: 12px; margin-bottom: 6px; }
.tr-newref-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px; }
.tr-newref-grid input { padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border); font-size: 12px; grid-column: span 1; }
'''
html = html.replace('</style>', TEAM_CSS + '</style>', 1)

TEAM_DATA_INIT = '''  var teamData = {};
  function td(target) { if (!teamData[target]) teamData[target] = {selected:false, comment:'', hasData:false, revisit:false, refApprovals:{}, newRefs:[]}; return teamData[target]; }
'''
html = html.replace(
    "var state = { q: '', cat: 'All', lpiOnly: false, det: 'All', recheckOnly: false, hasRef: 'All', sortKey: null, sortDir: 1, page: 0 };",
    "var state = { q: '', cat: 'All', lpiOnly: false, det: 'All', recheckOnly: false, hasRef: 'All', sortKey: null, sortDir: 1, page: 0 };\n" + TEAM_DATA_INIT,
    1)

TEAM_JS = '''
  document.getElementById('tr-initials').addEventListener('change', function(e) {
    document.getElementById('tr-initials-other').style.display = e.target.value === '__other' ? 'block' : 'none';
  });
  document.getElementById('tr-haslist-yes').addEventListener('change', function() { document.getElementById('tr-haslist-yes-box').style.display = 'block'; });
  document.getElementById('tr-haslist-no').addEventListener('change', function() { document.getElementById('tr-haslist-yes-box').style.display = 'none'; });

  function selectedTargets() {
    return Array.prototype.slice.call(document.querySelectorAll('.tr-row-select:checked')).map(function(cb) { return cb.getAttribute('data-target'); });
  }
  function updateSelCount() {
    document.getElementById('tr-sel-count').textContent = selectedTargets().length + ' objects selected';
  }
  document.getElementById('ao-tbody').addEventListener('change', function(e) {
    if (!e.target.classList.contains('tr-row-select')) return;
    td(e.target.getAttribute('data-target')).selected = e.target.checked;
    updateSelCount();
  });
  document.getElementById('tr-select-all').addEventListener('change', function(e) {
    document.querySelectorAll('.tr-row-select').forEach(function(cb) { cb.checked = e.target.checked; td(cb.getAttribute('data-target')).selected = e.target.checked; });
    updateSelCount();
  });
  document.getElementById('tr-apply-comment').addEventListener('click', function() {
    var c = document.getElementById('tr-comment').value.trim();
    if (!c) { alert('Type a comment first.'); return; }
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first (checkbox column on the left of the table).'); return; }
    sel.forEach(function(t) { td(t).comment = c; });
    alert('Comment applied to ' + sel.length + ' object(s).');
  });
  document.getElementById('tr-apply-hasdata').addEventListener('click', function() {
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first.'); return; }
    sel.forEach(function(t) { td(t).hasData = true; });
    alert('Marked ' + sel.length + ' object(s) as "I have data for this object".');
  });
  document.getElementById('tr-apply-revisit').addEventListener('click', function() {
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first.'); return; }
    sel.forEach(function(t) { td(t).revisit = true; });
    alert('Flagged ' + sel.length + ' object(s) for Re-visit.');
  });
  document.getElementById('tr-apply-approve-refs').addEventListener('click', function() {
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first.'); return; }
    var refCount = 0;
    sel.forEach(function(t) {
      var row = DATA.filter(function(r) { return r.target === t; })[0] || {};
      (row.refsFull || []).forEach(function(rf, i) { td(t).refApprovals[i] = true; refCount++; });
    });
    alert('Approved ' + refCount + ' reference(s) across ' + sel.length + ' object(s).');
  });

  // Shared reference approve/reject markup + wiring - used both by the
  // per-object modal and the multi-object "Review references" pop-out, so
  // the checkboxes behave identically (and write into the same teamData
  // store) no matter which surface you check them from.
  function refsHtmlFor(target) {
    var row = DATA.filter(function(r) { return r.target === target; })[0] || {};
    var d = td(target);
    if (!(row.refsFull || []).length) return '<div class="tr-hint">No references listed for this object yet.</div>';
    return row.refsFull.map(function(rf, i) {
      var checked = d.refApprovals[i];
      return '<div class="tr-ref-row"><label><input type="checkbox" class="tr-ref-approve" data-target="' + esc(target) + '" data-i="' + i + '" ' + (checked === true ? 'checked' : '') + '> approve</label>' +
        '<label><input type="checkbox" class="tr-ref-reject" data-target="' + esc(target) + '" data-i="' + i + '" ' + (checked === false ? 'checked' : '') + '> reject</label>' +
        '<span class="fl-help" tabindex="0" data-tip="Approve if this reference correctly applies to this object; reject if it looks wrong.">i</span>' +
        '<span>' + esc(rf.citation || rf.url || 'reference ' + (i + 1)).slice(0, 90) + '</span></div>';
    }).join('');
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
    if (panel.style.display !== 'none') { panel.style.display = 'none'; return; }
    var sel = selectedTargets();
    if (!sel.length) { alert('Select at least one object first (checkbox column on the left of the table).'); return; }
    panel.innerHTML = sel.map(function(t) {
      var row = DATA.filter(function(r) { return r.target === t; })[0] || {};
      var title = (row.num ? row.num + ' ' : '') + (row.name || t);
      return '<div class="tr-multiref-obj"><h5>' + esc(title) + '</h5>' + refsHtmlFor(t) + '</div>';
    }).join('');
    wireRefCheckboxes(panel);
    panel.style.display = 'block';
  });

  function collectSubmission() {
    var initialsSel = document.getElementById('tr-initials').value;
    var initials = initialsSel === '__other' ? document.getElementById('tr-initials-other').value.trim() : initialsSel;
    var haslist = (document.querySelector('input[name="tr-haslist"]:checked') || {}).value || null;
    var perObject = Object.keys(teamData).filter(function(t) {
      var d = teamData[t];
      return d.comment || d.hasData || d.revisit || Object.keys(d.refApprovals).length || d.newRefs.length;
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
      html += '<table class="ao-table" style="margin-top:10px;"><thead><tr><th>Object</th><th>Comment</th><th>Have data</th><th>Re-visit</th><th>References</th></tr></thead><tbody>' +
        s.objects.map(function(o) {
          return '<tr><td>' + esc(o.target) + '</td><td>' + (o.comment ? esc(o.comment) : '&mdash;') + '</td><td>' + (o.hasData ? 'Yes' : '&mdash;') +
            '</td><td>' + (o.revisit ? 'Yes' : '&mdash;') + '</td><td>' + refSummary(o) + '</td></tr>';
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
  };
  function refsPlainText(o) {
    var app = Object.keys(o.refApprovals).filter(function(i) { return o.refApprovals[i] === true; }).length;
    var rej = Object.keys(o.refApprovals).filter(function(i) { return o.refApprovals[i] === false; }).length;
    var parts = [];
    if (app) parts.push(app + ' approved');
    if (rej) parts.push(rej + ' rejected');
    return parts.join(', ');
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
      return fetch(GFORM_URL, {method: 'POST', mode: 'no-cors', body: body});
    })).then(function() { status.textContent = 'Submitted ' + rows.length + ' row(s) – thank you! You can keep editing and submit again any time.'; })
      .catch(function() { status.textContent = 'Submission failed – check your connection and try again.'; });
  });

  // -- per-object Team Review section, appended into the existing object modal --
  var _origOpenModal = openModal;
  openModal = function(target) {
    _origOpenModal(target);
    var d = td(target);
    var refsHtml = refsHtmlFor(target);

    var body = document.getElementById('ao-modal-body');

    // Compact quick-review strip, placed right under the top image/data row
    // (not at the very bottom) so a one-object review doesn't need scrolling
    // past the full reference list just to leave a comment or flag it.
    var quickHtml = '<div class="tr-modal-quick">' +
      '<div class="tr-field"><label>Comment <span class="fl-help" tabindex="0" data-tip="Add here any comments about the data">i</span></label>' +
      '<textarea id="tr-modal-comment" rows="1">' + esc(d.comment) + '</textarea></div>' +
      '<label><input type="checkbox" id="tr-modal-hasdata" ' + (d.hasData ? 'checked' : '') + '> I have data for this object</label>' +
      '<label><input type="checkbox" id="tr-modal-revisit" ' + (d.revisit ? 'checked' : '') + '> Add to Re-visit list</label>' +
      '</div>';
    var modalTop = body.querySelector('.ao-modal-top');
    if (modalTop) { modalTop.insertAdjacentHTML('afterend', quickHtml); } else { body.innerHTML += quickHtml; }

    body.innerHTML += '<div class="tr-modal-section">' +
      '<h4>Reference verification</h4>' + refsHtml +
      '<div style="margin-top:8px;"><span class="fl-help term-help" tabindex="0" data-tip="Preferred: a DOI. If you don\\u2019t have one, the first author\\u2019s last name, publication year if known, or a topic/title so we can find it.">Add a new reference</span>' +
      '<div class="tr-newref-grid">' +
      '<input type="text" id="tr-newref-doi" placeholder="DOI (preferred)">' +
      '<input type="text" id="tr-newref-author" placeholder="First author last name">' +
      '<input type="text" id="tr-newref-year" placeholder="Year (if known)">' +
      '<input type="text" id="tr-newref-topic" placeholder="Topic / title (if no DOI/author)">' +
      '</div><button class="toggle-btn" id="tr-add-newref" style="margin-top:8px;">Add reference to this object\\u2019s card</button>' +
      '<div id="tr-newref-list" style="margin-top:6px;font-size:12px;"></div></div>' +
      '</div>';

    document.getElementById('tr-modal-comment').addEventListener('input', function(e) { d.comment = e.target.value; });
    document.getElementById('tr-modal-hasdata').addEventListener('change', function(e) { d.hasData = e.target.checked; });
    document.getElementById('tr-modal-revisit').addEventListener('change', function(e) { d.revisit = e.target.checked; });
    wireRefCheckboxes(body);
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
    });
  };
'''
html = html.replace('})();', TEAM_JS + '\n})();', 1)

open(f'{PROJ}/TeamRadar-Revision.html', 'w', encoding='utf-8').write(html)
print(f'Saved TeamRadar-Revision.html: {len(html):,} bytes')
