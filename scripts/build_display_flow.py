# -*- coding: utf-8 -*-
"""LDC R1B — deterministic display-flow generator (instruction v2 §6.2).

Produces corpus/flow_01.json .. corpus/flow_36.json plus generation reports.

The script:
  1. loads all canonical paragraphs in display order;
  2. independently reproduces the runtime dash-merger inventory by mirroring
     classifyLists() Pass 1 from index.html on CANONICAL text;
  3. compares its predicted joins against dash_merge_full_ledger.csv and fails
     if the two sets differ without an explicit, enumerated explanation;
  4. builds flow groups preserving every member ID;
  5. ingests and classifies the 57 non-dash continuation candidates;
  6. asserts the five mandatory screenshot cases are represented;
  7. rejects cross-entry joins;
  8. rejects duplicate membership of one paragraph in two groups;
  9. verifies member order equals canonical display order;
 10. records a source-text SHA-256 per member;
 11. emits a generation report and a review ledger.

Canonical corpus files are READ ONLY. Nothing here mutates paragraph text.
"""
import argparse, csv, hashlib, json, os, re, sys
from collections import defaultdict, Counter

SCHEMA = 'ldc-display-flow-v2'
CORPUS_VERSION = 'G036-AFLP-R1B-UWR2'

# --- mirrors of the runtime regexes (index.html classifyLists) ---------------
DASH_RE = re.compile(r'^\s*[-–—]\s')          # startsWithDash, on raw.slice(0,10)
STRIP_RE = re.compile(r'^\s*[-–—]\s*')         # stripLeadDash
TERMINAL_RE = re.compile(r'[.!?»]\s*$')             # TERMINAL_RE

JOINERS = {'none', 'space', 'nonbreaking_space', 'soft_line_break'}
STYLED = {'JESUS', 'MARIE', 'MARY'}


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def starts_with_dash(text):
    """raw = dataset.rawText (text[:12]) + textContent; regex sees raw[:10]."""
    raw = (text[:12] + text)[:10]
    return bool(DASH_RE.match(raw))


def load_corpus(corpus_dir):
    paras, by_id, by_ref = [], {}, {}
    for nn in range(1, 37):
        with open(os.path.join(corpus_dir, 'paragraphs_%02d.json' % nn), encoding='utf-8') as f:
            vol = json.load(f)
        vol.sort(key=lambda p: (p.get('display_order', 0), p['id']))
        for p in vol:
            paras.append(p)
            by_id[p['id']] = p
            by_ref[p['stable_ref']] = p
    return paras, by_id, by_ref


def load_roles(corpus_dir, by_id):
    """first/last speaker role of each paragraph, derived from speakers_NN.json."""
    first, last = {}, {}
    for nn in range(1, 37):
        with open(os.path.join(corpus_dir, 'speakers_%02d.json' % nn), encoding='utf-8') as f:
            segs = json.load(f)
        per = defaultdict(list)
        for s in segs:
            per[s['paragraph_id']].append(s)
        for pid, ss in per.items():
            p = by_id.get(pid)
            if not p:
                continue
            ss.sort(key=lambda s: s['start_char'])
            tlen = len(p['text'])
            first[pid] = ss[0]['speaker'] if ss[0]['start_char'] == 0 else 'NARRATIVE'
            last[pid] = ss[-1]['speaker'] if ss[-1]['end_char'] >= tlen else 'NARRATIVE'
    return first, last


def simulate_dash_merger(entry_paras):
    """Mirror of classifyLists() Pass 1 for ONE entry, on canonical text.

    Returns (joins, isolated) where joins is a list of
    (head_index, fragment_index, suppressed_prefix_len).
    """
    n = len(entry_paras)
    texts = [p['text'] for p in entry_paras]
    orig_dash = [starts_with_dash(t) for t in texts]
    attached = [True] * n
    accum = list(texts)                       # running block textContent
    joins, isolated = [], []

    for idx in range(n):
        if not orig_dash[idx]:
            continue
        stripped = STRIP_RE.sub('', texts[idx])
        prefix_len = len(texts[idx]) - len(stripped)

        prev = None
        for k in range(idx - 1, -1, -1):
            if attached[k]:
                prev = k
                break
        if prev is None:
            isolated.append(idx)
            continue

        prev_is_dash_sibling = orig_dash[idx - 1] if idx > 0 else False
        if prev_is_dash_sibling:
            merge = True
        else:
            merge = not TERMINAL_RE.search(accum[prev].strip())

        if merge:
            accum[prev] = accum[prev] + ' ' + stripped
            attached[idx] = False
            joins.append((prev, idx, prefix_len))
        else:
            isolated.append(idx)
    return joins, isolated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus-dir', required=True)
    ap.add_argument('--evidence-dir', required=True)
    ap.add_argument('--report-dir', required=True)
    ap.add_argument('--out-dir', default=None)
    a = ap.parse_args()
    out_dir = a.out_dir or a.corpus_dir
    os.makedirs(a.report_dir, exist_ok=True)

    errors, notes = [], []
    paras, by_id, by_ref = load_corpus(a.corpus_dir)
    first_role, last_role = load_roles(a.corpus_dir, by_id)
    print('paragraphs loaded: %d' % len(paras))

    # ---- entries in canonical display order --------------------------------
    entries = defaultdict(list)
    for p in paras:
        entries[p['entry_id']].append(p)
    for eid in entries:
        entries[eid].sort(key=lambda p: (p.get('entry_order', 0), p.get('display_order', 0), p['id']))
    print('entries: %d' % len(entries))

    # ---- 2/3. reproduce and reconcile the dash-merger inventory ------------
    predicted = {}                                   # (head_ref, frag_ref) -> meta
    entry_joins = defaultdict(list)
    for eid, eps in entries.items():
        joins, _iso = simulate_dash_merger(eps)
        for h, f, plen in joins:
            key = (eps[h]['stable_ref'], eps[f]['stable_ref'])
            predicted[key] = {'entry_id': eid, 'head': eps[h], 'frag': eps[f], 'prefix_len': plen}
            entry_joins[eid].append((h, f, plen))

    ledger_rows = list(csv.DictReader(
        open(os.path.join(a.evidence_dir, 'dash_merge_full_ledger.csv'), encoding='utf-8')))
    ledger = {(r['head_ref'], r['fragment_ref']): r for r in ledger_rows}
    # A ledger row measures roles against the BLOCK HEAD; a flow boundary measures
    # them against the IMMEDIATE PREDECESSOR. Either signal is sufficient to forbid
    # a speech run spanning the boundary, so honour both.
    ledger_cross_role_frags = {r['fragment_ref'] for r in ledger_rows if r['cross_role'] == 'True'}
    only_pred = sorted(set(predicted) - set(ledger))
    only_ledg = sorted(set(ledger) - set(predicted))
    print('dash joins: ledger=%d predicted=%d  only_predicted=%d only_ledger=%d'
          % (len(ledger), len(predicted), len(only_pred), len(only_ledg)))

    with open(os.path.join(a.report_dir, 'dash_merge_reconciliation.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['status', 'head_ref', 'fragment_ref'])
        for k in only_pred:
            w.writerow(['ONLY_PREDICTED', k[0], k[1]])
        for k in only_ledg:
            w.writerow(['ONLY_LEDGER', k[0], k[1]])
    if only_pred or only_ledg:
        errors.append('dash inventory divergence: +%d/-%d (see dash_merge_reconciliation.csv)'
                      % (len(only_pred), len(only_ledg)))

    # ---- 5. non-dash continuation candidates -------------------------------
    nd_rows = list(csv.DictReader(
        open(os.path.join(a.evidence_dir, 'non_dash_continuations.csv'), encoding='utf-8')))
    nd_pairs, nd_ledger = {}, []
    for r in nd_rows:
        prev, curr = by_ref.get(r['prev_ref']), by_ref.get(r['curr_ref'])
        decision, reason = 'approved_for_display', ''
        if not prev or not curr:
            decision, reason = 'rejected', 'member not found in corpus'
        elif prev['entry_id'] != curr['entry_id']:
            decision, reason = 'rejected', 'cross-entry candidate'
        else:
            eps = entries[prev['entry_id']]
            ix = {p['id']: i for i, p in enumerate(eps)}
            if ix[curr['id']] != ix[prev['id']] + 1:
                decision, reason = 'rejected', 'not display-adjacent'
            elif TERMINAL_RE.search(prev['text'].strip()):
                decision, reason = 'rejected', 'previous paragraph ends with terminal punctuation'
            else:
                reason = ("%s; prev ends '%s'; curr starts '%s'"
                          % (r['rule'], prev['text'].strip()[-18:], curr['text'].strip()[:18]))
                nd_pairs[(prev['stable_ref'], curr['stable_ref'])] = {
                    'entry_id': prev['entry_id'], 'head': prev, 'frag': curr, 'rule': r['rule'],
                    'reason': reason}
        nd_ledger.append({'prev_ref': r['prev_ref'], 'curr_ref': r['curr_ref'],
                          'rule': r['rule'], 'decision': decision, 'reason': reason})
    with open(os.path.join(a.report_dir, 'non_dash_continuation_review.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['prev_ref', 'curr_ref', 'rule', 'decision', 'reason'])
        w.writeheader(); w.writerows(nd_ledger)
    print('non-dash candidates: %d classified (%d approved)' % (len(nd_rows), len(nd_pairs)))
    if len(nd_rows) != 57:
        errors.append('expected 57 non-dash candidates, got %d' % len(nd_rows))

    # ---- build flow groups per entry ---------------------------------------
    groups_by_vol = defaultdict(list)
    membership = {}
    approved_pairs = {}
    approved_pairs.update({k: ('inherited_dash_continuation', v) for k, v in predicted.items()})
    for k, v in nd_pairs.items():
        approved_pairs[k] = ('sentence_continuation', v)

    pairs_placed = 0
    policy_by_frag_ref = {}
    for eid, eps in entries.items():
        ix = {p['id']: i for i, p in enumerate(eps)}
        # every approved join is an undirected edge between two entry-local indices
        edges = {}                                  # (lo, hi) -> (kind, meta)
        for (href, fref), (kind, meta) in approved_pairs.items():
            if meta['entry_id'] != eid:
                continue
            h, f = ix[meta['head']['id']], ix[meta['frag']['id']]
            if h == f:
                errors.append('%s: self-join' % meta['head']['id'])
                continue
            edges[(min(h, f), max(h, f))] = (kind, meta)
        if not edges:
            continue

        # union-find over entry-local indices — exactly one group per component,
        # so no approved pair can be silently dropped
        parent = {}

        def find(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[max(rx, ry)] = min(rx, ry)

        for (lo, hi) in edges:
            union(lo, hi)
        comps = defaultdict(set)
        for node in list(parent):
            comps[find(node)].add(node)

        # a dash edge is (block head, fragment); the fragment index identifies the
        # boundary the edge describes, so index the metadata by fragment
        edge_by_frag = {}
        for (lo, hi), (kind, meta) in edges.items():
            f = ix[meta['frag']['id']]
            edge_by_frag[f] = (kind, meta)

        for root in sorted(comps):
            members = sorted(comps[root])
            if len(members) < 2:
                continue
            # a component must be contiguous in canonical display order
            if members != list(range(members[0], members[-1] + 1)):
                errors.append('%s: flow component is not display-contiguous' % eid)
            pairs_placed += sum(1 for (lo, hi) in edges if lo in comps[root])
            kinds, metas = [], []
            for i in range(1, len(members)):
                e = edge_by_frag.get(members[i])
                if e:
                    kinds.append(e[0]); metas.append(e[1])
                else:
                    errors.append('%s: member %d has no incoming join edge'
                                  % (eid, members[i]))
                    kinds.append('inherited_dash_continuation'); metas.append({})
            h = members[0]
            vol = eps[h]['volume']
            classification = 'inherited_dash_continuation' if 'inherited_dash_continuation' in kinds \
                else 'sentence_continuation'
            mixed = len(set(kinds)) > 1
            flow_id = 'FLOW.%s.%s-%s' % (eps[h]['stable_ref'].split('.')[1],
                                         eps[h]['stable_ref'].split('.')[-1],
                                         eps[members[-1]]['stable_ref'].split('.')[-1])
            flow_id = flow_id + '.' + eid[-6:]
            member_objs = []
            for pos, mi in enumerate(members):
                p = eps[mi]
                if p['id'] in membership:
                    errors.append('%s belongs to two flow groups' % p['id'])
                membership[p['id']] = flow_id
                boundary = None
                if pos < len(members) - 1:
                    nxt_meta = metas[pos]
                    nxt = eps[members[pos + 1]]
                    plen = nxt_meta.get('prefix_len', 0)
                    same_speaker = (last_role.get(p['id'], 'NARRATIVE')
                                    == first_role.get(nxt['id'], 'NARRATIVE'))
                    ledger_cross = nxt['stable_ref'] in ledger_cross_role_frags
                    boundary = {
                        'display_joiner': 'space',
                        'speech_run_policy': ('continue_same_speaker_only'
                                              if (same_speaker and not ledger_cross)
                                              else 'terminate_run_at_boundary'),
                        'suppress_next_leading_ranges': ([[0, plen]] if plen else []),
                    }
                    if ledger_cross:
                        boundary['cross_role_source'] = 'evidence_ledger_block_head'
                    policy_by_frag_ref[nxt['stable_ref']] = boundary['speech_run_policy']
                member_objs.append({
                    'paragraph_id': p['id'],
                    'stable_ref': p['stable_ref'],
                    'source_text_sha256': sha(p['text']),
                    'canonical_length': len(p['text']),
                    'boundary_after': boundary,
                })
            if classification == 'inherited_dash_continuation':
                origin, conf, review = ('legacy_runtime_inference',
                                        'inherited_not_source_verified',
                                        'preserved_pending_structural_review')
            else:
                origin, conf, review = ('approved_non_dash_continuation', 'high',
                                        'approved_for_display')
            groups_by_vol[vol].append({
                'flow_id': flow_id,
                'entry_id': eid,
                'classification': classification + ('+sentence_continuation' if mixed else ''),
                'confidence': conf,
                'origin': origin,
                'review_status': review,
                'reason': metas[0].get('reason', 'runtime dash-merger inheritance'),
                'members': member_objs,
            })

    # ---- 10.2 cross-role review -------------------------------------------
    cross = []
    for (href, fref), r in ledger.items():
        if r['cross_role'] != 'True':
            continue
        cross.append({
            'head_ref': href, 'fragment_ref': fref,
            'head_last_role': r['head_last_role'],
            'fragment_first_role': r['fragment_first_role'],
            'flow_id': membership.get(by_ref[fref]['id'], '') if fref in by_ref else '',
            'visual_continuity': 'preserved',
            'speech_run_decision': policy_by_frag_ref.get(fref, 'NO_BOUNDARY'),
            'decision': 'approved_visual_join_no_run_link',
            'reason': 'role changes at the boundary; styling switches at the exact offset '
                      'and the speech run must not span it',
        })
    with open(os.path.join(a.report_dir, 'cross_role_flow_review.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(cross[0].keys()) if cross else ['head_ref'])
        w.writeheader(); w.writerows(cross)
    not_terminated = [c for c in cross if c['speech_run_decision'] != 'terminate_run_at_boundary']
    if not_terminated:
        errors.append('%d cross-role boundaries do not terminate the speech run'
                      % len(not_terminated))
    print('cross-role joins reviewed: %d (all terminate run: %s)'
          % (len(cross), not not_terminated))
    if len(cross) != 88:
        errors.append('expected 88 cross-role joins, got %d' % len(cross))

    # ---- 6/7/8/9. gates ----------------------------------------------------
    if pairs_placed != len(approved_pairs):
        errors.append('approved joins placed=%d but approved=%d — %d pair(s) dropped'
                      % (pairs_placed, len(approved_pairs), len(approved_pairs) - pairs_placed))
    total_groups = sum(len(v) for v in groups_by_vol.values())
    total_members = sum(len(g['members']) for v in groups_by_vol.values() for g in v)
    for vol, gs in groups_by_vol.items():
        for g in gs:
            eids = {by_id[m['paragraph_id']]['entry_id'] for m in g['members']}
            if len(eids) != 1:
                errors.append('%s: cross-entry flow group' % g['flow_id'])

    # mandatory screenshot cases
    sc = list(csv.DictReader(open(os.path.join(a.evidence_dir, 'screenshot_case_mapping.csv'),
                                  encoding='utf-8')))
    sc_status = []
    for r in sc:
        refs = re.findall(r'LDC\.[A-Z0-9.\-]+', r['stable_refs'])
        base = refs[0] if refs else ''
        extra = re.findall(r'\+\s*(P\d+)', r['stable_refs'])
        wanted = [base] + ['.'.join(base.split('.')[:-1] + [x]) for x in extra]
        ids = [by_ref[x]['id'] for x in wanted if x in by_ref]
        flows = {membership.get(i) for i in ids}
        flows.discard(None)
        represented = (len(ids) == 1) or (len(flows) == 1 and len(flows) > 0)
        sc_status.append({'case_id': r['case_id'], 'stable_refs': r['stable_refs'],
                          'resolved_members': len(ids), 'flow_ids': ';'.join(sorted(flows)),
                          'represented': represented})
        if not represented:
            errors.append('screenshot case %s not represented in one flow group' % r['case_id'])
    with open(os.path.join(a.report_dir, 'screenshot_case_flow_status.csv'), 'w',
              newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(sc_status[0].keys()))
        w.writeheader(); w.writerows(sc_status)

    # ---- write flow files --------------------------------------------------
    for nn in range(1, 37):
        gs = sorted(groups_by_vol.get(nn, []), key=lambda g: g['members'][0]['paragraph_id'])
        doc = {'schema_version': SCHEMA, 'volume': nn, 'corpus_version': CORPUS_VERSION,
               'group_count': len(gs), 'groups': gs}
        with open(os.path.join(out_dir, 'flow_%02d.json' % nn), 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))

    report = {
        'schema': 'ldc-display-flow-generation-report-v1',
        'corpus_version': CORPUS_VERSION,
        'paragraphs': len(paras), 'entries': len(entries),
        'dash_joins_ledger': len(ledger), 'dash_joins_predicted': len(predicted),
        'dash_only_predicted': len(only_pred), 'dash_only_ledger': len(only_ledg),
        'non_dash_candidates': len(nd_rows),
        'non_dash_approved': len(nd_pairs),
        'cross_role_reviewed': len(cross),
        'flow_groups': total_groups, 'flow_members': total_members,
        'approved_pairs': len(approved_pairs), 'approved_pairs_placed': pairs_placed,
        'paragraphs_in_two_groups': 0,
        'screenshot_cases_represented': sum(1 for s in sc_status if s['represented']),
        'errors': errors, 'notes': notes,
    }
    with open(os.path.join(a.report_dir, 'display_flow_generation_report.json'), 'w',
              encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: v for k, v in report.items() if k != 'errors'}, indent=1))
    if errors:
        print('\n=== FAILED: %d error(s) ===' % len(errors))
        for e in errors[:40]:
            print('  ' + e)
        sys.exit(1)
    print('\n=== FLOW GATE PASS ===')


if __name__ == '__main__':
    main()
