/* ============================================================================
   LDC R1B — Stage B: pure paragraph-local speech model builder
   ----------------------------------------------------------------------------
   buildParagraphSpeechModel(text, segments) -> model

   Pure function. No DOM, no mutation of inputs, no string deletion.
   Every canonical character of `text` appears exactly once across model.intervals.

   Governing rules (instruction v2 §7.1–7.3, §7.5, §7.7):
     - validate segments; never silently "repair" them
     - cover the paragraph with atomic intervals (narrative | speech)
     - merge adjacent styled segments ONLY when:
         same normalised speaker, truly adjacent in the FULL segment order,
         and the bridge between them contains no letter or digit
       The bridge characters are KEPT inside the run (never discarded).
     - internal quotation marks are ordinary characters of the run and must
       never terminate it
     - block/inline is decided per RUN, never per source segment
   ========================================================================== */
(function (root) {
  'use strict';

  var STYLED = { JESUS: 'jesus', MARIE: 'marie', MARY: 'marie' };

  // A bridge is "non-lexical" if it contains no letter or digit. Accents included.
  var LEXICAL = /[0-9A-Za-zÀ-ɏ]/;

  function normSpeaker(s) { return STYLED[s] || null; }
  function isStyled(s) { return !!STYLED[s]; }
  var CONF_RANK = { low: 0, medium: 1, high: 2 };
  function mergeConfidence(a, b) {
    if (!a) return b || null;
    if (!b) return a || null;
    return (CONF_RANK[a] <= CONF_RANK[b]) ? a : b;
  }

  /* -- validation: report, never mutate ----------------------------------- */
  function validateSegments(text, segments) {
    var errs = [];
    var sorted = segments.slice().sort(function (a, b) {
      return a.start_char - b.start_char || a.end_char - b.end_char;
    });
    for (var i = 0; i < sorted.length; i++) {
      var s = sorted[i];
      if (!(s.start_char >= 0 && s.start_char < s.end_char && s.end_char <= text.length)) {
        errs.push({ code: 'INVALID_RANGE', segment_id: s.segment_id,
                    start: s.start_char, end: s.end_char, len: text.length });
      }
      if (i > 0 && s.start_char < sorted[i - 1].end_char) {
        errs.push({ code: 'OVERLAP', segment_id: s.segment_id,
                    prev_segment_id: sorted[i - 1].segment_id });
      }
    }
    return { sorted: sorted, errors: errs };
  }

  /* -- main ---------------------------------------------------------------- */
  function buildParagraphSpeechModel(text, segments, opts) {
    opts = opts || {};
    var v = validateSegments(text, segments || []);
    if (v.errors.length && !opts.tolerateInvalid) {
      return { ok: false, errors: v.errors, intervals: [], runs: [] };
    }
    var sorted = v.sorted;

    /* 1 — atomic intervals covering the paragraph exactly once */
    var intervals = [], cur = 0;
    for (var i = 0; i < sorted.length; i++) {
      var s = sorted[i];
      if (s.start_char > cur) {
        intervals.push({ start: cur, end: s.start_char, text: text.slice(cur, s.start_char),
                         role: 'NARRATIVE', speaker: null, styled: false,
                         confidence: null, segment_ids: [] });
      }
      intervals.push({ start: s.start_char, end: s.end_char,
                       text: text.slice(s.start_char, s.end_char),
                       role: s.speaker, speaker: s.speaker,
                       styled: isStyled(s.speaker),
                       confidence: s.confidence || null,
                       segment_ids: [s.segment_id] });
      cur = s.end_char;
    }
    if (cur < text.length) {
      intervals.push({ start: cur, end: text.length, text: text.slice(cur),
                       role: 'NARRATIVE', speaker: null, styled: false,
                       confidence: null, segment_ids: [] });
    }

    /* 2 — controlled coalescence into paragraph-local runs.
           Adjacency is evaluated on the FULL interval sequence: a NARRATIVE
           interval between two styled intervals means they are NOT adjacent,
           which is exactly what excludes the 99 intervening-role pairs. */
    var runs = [], merges = [];
    for (var j = 0; j < intervals.length; j++) {
      var iv = intervals[j];
      var last = runs.length ? runs[runs.length - 1] : null;
      if (last && last.styled && iv.styled &&
          normSpeaker(last.speaker) === normSpeaker(iv.speaker) &&
          last.end === iv.start) {
        // directly abutting styled intervals of the same speaker
        last.end = iv.end;
        last.text += iv.text;
        last.segment_ids = last.segment_ids.concat(iv.segment_ids);
        last.confidence = mergeConfidence(last.confidence, iv.confidence);
        merges.push({ at: iv.start, kind: 'abut', bridge: '' });
        continue;
      }
      if (last && last.styled && iv.styled === false && j + 1 < intervals.length) {
        var nxt = intervals[j + 1];
        if (nxt.styled && normSpeaker(last.speaker) === normSpeaker(nxt.speaker) &&
            last.end === iv.start && iv.end === nxt.start &&
            !LEXICAL.test(iv.text)) {
          // NON-LEXICAL BRIDGE: keep the bridge characters inside the run
          last.end = nxt.end;
          last.text += iv.text + nxt.text;
          last.segment_ids = last.segment_ids.concat(nxt.segment_ids);
          last.confidence = mergeConfidence(last.confidence, nxt.confidence);
          merges.push({ at: iv.start, kind: 'non_lexical_bridge', bridge: iv.text });
          j++; // consume nxt
          continue;
        }
      }
      runs.push({ start: iv.start, end: iv.end, text: iv.text,
                  role: iv.role, speaker: iv.speaker, styled: iv.styled,
                  confidence: iv.confidence, segment_ids: iv.segment_ids.slice(),
                  presentation: null });
    }

    /* 3 — block vs inline, decided per RUN (§7.7) */
    for (var k = 0; k < runs.length; k++) {
      var r = runs[k];
      if (!r.styled) { r.presentation = 'narrative'; continue; }
      var before = text.slice(0, r.start);
      // strip a leading source section marker such as "(2) "
      var beforeCore = before.replace(/^\s*\(\d+\)\s*/, '');
      if (/^\s*$/.test(beforeCore)) { r.presentation = 'block'; continue; }
      // explicit narrative attribution ending in a colon
      if (/[:：]\s*["'«“„]?\s*$/.test(beforeCore)) { r.presentation = 'block'; continue; }
      r.presentation = 'inline';
    }

    return { ok: true, errors: [], intervals: intervals, runs: runs, merges: merges };
  }

  /* -- reconstruction proof helper ---------------------------------------- */
  function reconstruct(model) {
    var out = '';
    for (var i = 0; i < model.intervals.length; i++) out += model.intervals[i].text;
    return out;
  }

  /* -- §7.4 link same-speaker runs across approved flow boundaries ---------
     members: [{ paraId, text, model, atoms, boundaryAfter }] in display order.
     A link is created ONLY when all seven conditions hold. Sharing a speaker is
     never sufficient — the flow decision and its boundary metadata are
     mandatory. Mutates member models in place and returns the link ledger. */
  function linkFlowRuns(members) {
    var links = [];
    // display-visible length of a canonical range, so an approved suppressed
    // extraction dash does not stop a run from counting as fragment-initial
    function visibleLen(atoms, from, to) {
      if (!atoms) return Math.max(0, to - from);
      var n = 0;
      for (var i = 0; i < atoms.length; i++) {
        var a = atoms[i];
        if (a.ce <= from || a.cs >= to) continue;
        if (a.kind === 'canonical') n += Math.min(a.ce, to) - Math.max(a.cs, from);
        else n += a.text.length;
      }
      return n;
    }
    for (var k = 0; k < members.length - 1; k++) {
      var cur = members[k], nxt = members[k + 1];
      var b = cur.boundaryAfter;
      // (1)+(2) same approved group, boundary permits continuation
      if (!b || b.speech_run_policy !== 'continue_same_speaker_only') continue;
      if (!cur.model || !cur.model.ok || !nxt.model || !nxt.model.ok) continue;
      var cr = cur.model.runs[cur.model.runs.length - 1];
      var nr = nxt.model.runs[0];
      if (!cr || !nr || !cr.styled || !nr.styled) continue;
      // (3) identical normalised speaker
      if (normSpeaker(cr.speaker) !== normSpeaker(nr.speaker)) continue;
      // (4) nothing may intervene: the run must reach the visible end of its
      // fragment, and the next run must start at the visible start of its own
      if (visibleLen(cur.atoms, cr.end, cur.text.length) !== 0) continue;
      if (visibleLen(nxt.atoms, 0, nr.start) !== 0) continue;
      // (5) a leading extraction dash must be an approved suppressed range
      if (nr.start > 0) {
        var supp = (b.suppress_next_leading_ranges || []);
        var covered = supp.some(function (r) { return r[0] === 0 && r[1] >= nr.start; }) ||
                      visibleLen(nxt.atoms, 0, nr.start) === 0;
        if (!covered) continue;
      }
      // (6) the joiner must be explicit
      if (!b.display_joiner) continue;
      // (7) the continuation inherits the logical run id
      var runId = cr.runId || (cur.paraId + '#R' + (cur.model.runs.length - 1));
      cr.runId = runId;
      nr.runId = runId;
      nr.isContinuation = true;
      links.push({ run_id: runId, from_paragraph: cur.paraId, to_paragraph: nxt.paraId,
                   speaker: normSpeaker(cr.speaker), joiner: b.display_joiner,
                   suppressed_leading: JSON.stringify(b.suppress_next_leading_ranges || []) });
    }
    return links;
  }

  root.LDCSpeechModel = {
    buildParagraphSpeechModel: buildParagraphSpeechModel,
    reconstruct: reconstruct,
    validateSegments: validateSegments,
    normSpeaker: normSpeaker,
    isStyled: isStyled,
    linkFlowRuns: linkFlowRuns
  };
})(typeof window !== 'undefined' ? window : globalThis);

/* ============================================================================
   Stage C — renderSpeechModel(model, opts) -> HTML string
   ----------------------------------------------------------------------------
   Emits ONE styled element per RUN (never per source segment) and ONE speaker
   label per run. Performs NO string deletion: every canonical character is
   emitted. An outer direct-speech delimiter is wrapped in
   <span class="speech-outer-delimiter"> so it can be visually suppressed by CSS
   while remaining present in the DOM with its canonical offsets.
   ========================================================================== */
(function (root) {
  'use strict';
  var M = root.LDCSpeechModel;

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  var OPEN = '«“„"';
  var CLOSE = '»”"';

  // Split a run into [openDelim, core, closeDelim] without dropping anything.
  function splitOuterDelimiters(t) {
    var a = 0, b = t.length;
    var lead = '', trail = '';
    while (a < b && /\s/.test(t[a])) a++;
    if (a < b && OPEN.indexOf(t[a]) !== -1) { lead = t.slice(0, a + 1); a = a + 1; }
    else { lead = ''; a = 0; }
    var e = b;
    while (e > a && /\s/.test(t[e - 1])) e--;
    if (e > a && CLOSE.indexOf(t[e - 1]) !== -1) { trail = t.slice(e - 1); b = e - 1; }
    else { trail = ''; b = t.length; }
    return { lead: lead, core: t.slice(a, b), trail: trail };
  }

  /* Emit a canonical range as DISPLAY text (structural-dash handoff v2).
     Suppressed and replaced tokens become spans carrying their canonical
     [cs,ce), so nothing downstream has to re-derive offsets from rendered text.
     `lead`/`trail` are display-space lengths of an outer speech delimiter. */
  function emitRange(atoms, start, end, lead, trail) {
    var DM = root.LDCDisplayMap;
    if (!DM || !atoms) {                       // no map loaded — canonical passthrough
      return null;
    }
    var ra = DM.atomsForRange(atoms, start, end);
    var total = 0, i;
    for (i = 0; i < ra.length; i++) total += ra[i].text.length;
    lead = lead || 0; trail = trail || 0;
    var out = '', d = 0;
    for (i = 0; i < ra.length; i++) {
      var a = ra[i];
      if (a.kind !== 'canonical') {
        out += '<span class="dtok dtok-' + (a.kind === 'suppressed' ? 'suppressed' : 'replaced') +
               '" data-cs="' + a.cs + '" data-ce="' + a.ce + '"' +
               (a.kind === 'suppressed' ? ' aria-hidden="true"' : '') +
               ' data-decision="' + esc(a.decision_id || '') + '">' + esc(a.text) + '</span>';
        d += a.text.length;
        continue;
      }
      // split this canonical atom across the lead / core / trail zones
      var txt = a.text, base = d, off = 0;
      while (off < txt.length) {
        var pos = base + off, zoneEnd;
        if (pos < lead)                 zoneEnd = Math.min(txt.length, lead - base);
        else if (pos >= total - trail)  zoneEnd = txt.length;
        else                            zoneEnd = Math.min(txt.length, (total - trail) - base);
        var chunk = txt.slice(off, zoneEnd);
        if (pos < lead || pos >= total - trail) {
          out += '<span class="speech-outer-delimiter" aria-hidden="true">' + esc(chunk) + '</span>';
        } else {
          out += esc(chunk);
        }
        off = zoneEnd;
      }
      d += txt.length;
    }
    return out;
  }

  function renderSpeechModel(model, opts) {
    opts = opts || {};
    var showLabels = !!opts.showLabels;         // labels emitted; Repères CSS controls visibility
    var hideOuter  = opts.hideOuterDelimiters !== false;
    var paraId     = opts.paraId || '';
    var atoms      = opts.atoms || null;        // display projection, may be absent
    var DM         = root.LDCDisplayMap;
    var html = '';
    for (var i = 0; i < model.runs.length; i++) {
      var r = model.runs[i];
      if (!r.styled) {
        var nar = atoms ? emitRange(atoms, r.start, r.end, 0, 0) : null;
        html += (nar === null ? esc(r.text) : nar);
        continue;
      }
      var cls = M.normSpeaker(r.speaker) === 'marie' ? 'speech-marie' : 'speech-jesus';
      var label = M.normSpeaker(r.speaker) === 'marie' ? 'Marie' : 'Jésus';
      // A run linked across a flow boundary keeps ONE logical id; only its first
      // fragment emits the speaker label and block-start spacing (§6.4).
      var runId = r.runId || (paraId + '#R' + i);
      var isCont = !!r.isContinuation;
      // outer delimiters are decided on the DISPLAY text, since a mapped token
      // may change what the run visually starts or ends with
      var runDisplay = r.text;
      if (atoms && DM) {
        var ra = DM.atomsForRange(atoms, r.start, r.end);
        runDisplay = '';
        for (var q = 0; q < ra.length; q++) runDisplay += ra[q].text;
      }
      var parts = splitOuterDelimiters(runDisplay);
      var inner = null;
      if (atoms) {
        inner = emitRange(atoms, r.start, r.end,
                          hideOuter ? parts.lead.length : 0,
                          hideOuter ? parts.trail.length : 0);
      }
      if (inner === null) {
        inner = '';
        if (parts.lead)  inner += '<span class="speech-outer-delimiter"' +
                                  (hideOuter ? ' aria-hidden="true"' : '') + '>' + esc(parts.lead) + '</span>';
        inner += esc(parts.core);
        if (parts.trail) inner += '<span class="speech-outer-delimiter"' +
                                  (hideOuter ? ' aria-hidden="true"' : '') + '>' + esc(parts.trail) + '</span>';
      }
      html += '<span class="' + cls + ' speech-run speech-' +
              (isCont ? 'inline speech-run-continuation' : r.presentation) + '"' +
              ' data-speech-run-id="' + esc(runId) + '"' +
              (isCont ? ' data-run-continuation="1"' : '') +
              ' data-run-start="' + r.start + '" data-run-end="' + r.end + '">' +
              (showLabels && !isCont ? '<span class="speech-label lbl-' +
                 (M.normSpeaker(r.speaker) === 'marie' ? 'marie' : 'jesus') + '">' + label + '</span>' +
                 (r.confidence ? '<span class="speech-conf" data-confidence="' + esc(r.confidence) + '">' +
                   (r.confidence === 'high' ? 'confiance élevée' : r.confidence === 'medium' ? 'confiance moyenne' : 'confiance faible') +
                  '</span>' : '') : '') +
              inner + '</span>';
    }
    return html;
  }

  M.renderSpeechModel = renderSpeechModel;
  M.splitOuterDelimiters = splitOuterDelimiters;
  M.escapeForRender = esc;
})(typeof window !== 'undefined' ? window : globalThis);
