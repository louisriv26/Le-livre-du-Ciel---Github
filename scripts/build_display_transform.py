# -*- coding: utf-8 -*-
"""LDC R1B — structural-dash display-transform layer (handoff RECHECKED v2).

Consumes the normative authority
    LDC_R1B_runtime_display_transform_map_v2.json
and emits a compact per-volume runtime table

    corpus/display_01.json .. corpus/display_36.json

plus corpus/display_titles.json.

DISPLAY-ONLY. Canonical paragraph text, IDs, fingerprints and speaker offsets are
never touched. Every operation keeps its canonical [start,end) so the reader can
maintain a canonical<->display mapping for highlights, notes and bookmarks.

Stop conditions (IMPLEMENTATION_CONTRACT_v2):
  BASELINE_MISMATCH        stable ref, canonical text or source token differs
  MAP_INTEGRITY_FAIL       overlap, range, source token or expected-output failure
  CORPUS_MUTATION_DETECTED canonical JSON changed by a display-only patch
"""
import argparse, hashlib, json, os, re, sys
from collections import defaultdict, Counter

SCHEMA = 'ldc-display-transform-v2'
CORPUS_VERSION = 'G036-AFLP-R1B-UWR2'


def die(code, msg):
    print('\n%s: %s' % (code, msg))
    sys.exit(1)


def apply_ops(text, ops):
    """Reference projection: assert every source slice, then replace from the
    highest canonical offset downwards (IMPLEMENTATION_CONTRACT_v2)."""
    iv = []
    for o in ops:
        s, e = int(o['canonical_start']), int(o['canonical_end'])
        if not (0 <= s <= e <= len(text)):
            die('MAP_INTEGRITY_FAIL', 'range out of bounds %s [%d,%d)' % (o['decision_id'], s, e))
        if text[s:e] != o['source_token']:
            die('BASELINE_MISMATCH', '%s expected %r got %r'
                % (o['decision_id'], o['source_token'], text[s:e]))
        if e > s:
            iv.append((s, e, o['decision_id']))
    iv.sort()
    for a, b in zip(iv, iv[1:]):
        if a[1] > b[0]:
            die('MAP_INTEGRITY_FAIL', 'overlapping operations %s / %s' % (a[2], b[2]))
    out = text
    for o in sorted(ops, key=lambda z: (int(z['canonical_start']), int(z['canonical_end'])),
                    reverse=True):
        s, e = int(o['canonical_start']), int(o['canonical_end'])
        out = out[:s] + o['display_replacement'] + out[e:]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus-dir', required=True)
    ap.add_argument('--handoff-dir', required=True)
    ap.add_argument('--report-dir', required=True)
    a = ap.parse_args()
    os.makedirs(a.report_dir, exist_ok=True)

    # ---- baseline identity -------------------------------------------------
    man = json.load(open(os.path.join(a.corpus_dir, 'manifest.json'), encoding='utf-8'))
    if man.get('version') != CORPUS_VERSION:
        die('BASELINE_MISMATCH', 'corpus version %r' % man.get('version'))

    by_ref, by_id, vol_of, pre = {}, {}, {}, {}
    for nn in range(1, 37):
        for p in json.load(open(os.path.join(a.corpus_dir, 'paragraphs_%02d.json' % nn),
                                encoding='utf-8')):
            by_ref[p['stable_ref']] = p
            by_id[p['id']] = p
            vol_of[p['id']] = nn
            pre[p['id']] = hashlib.sha256(p['text'].encode('utf-8')).hexdigest()
    if len(by_id) != 74348:
        die('BASELINE_MISMATCH', 'paragraph count %d' % len(by_id))

    # ---- speaker segments, for the composition invariant -------------------
    segs = defaultdict(list)
    for nn in range(1, 37):
        for s in json.load(open(os.path.join(a.corpus_dir, 'speakers_%02d.json' % nn),
                                encoding='utf-8')):
            segs[s['paragraph_id']].append(s)

    # ---- normative map -----------------------------------------------------
    m = json.load(open(os.path.join(a.handoff_dir,
                  'LDC_R1B_runtime_display_transform_map_v2.json'), encoding='utf-8'))
    if len({x['stable_ref'] for x in m}) != len(m):
        die('MAP_INTEGRITY_FAIL', 'duplicate stable_ref in map')

    per_vol = defaultdict(dict)
    tiers, actions = Counter(), Counter()
    crossing = 0
    n_ops = 0
    for x in m:
        ref = x['stable_ref']
        p = by_ref.get(ref)
        if p is None:
            die('BASELINE_MISMATCH', 'stable_ref not in corpus: %s' % ref)
        if p['text'] != x['canonical_text']:
            die('BASELINE_MISMATCH', 'canonical text differs for %s' % ref)

        got = apply_ops(p['text'], x['operations'])
        if got != x['expected_display_fragment']:
            die('MAP_INTEGRITY_FAIL', 'projection differs for %s' % ref)

        # a display operation must never straddle a speaker-segment boundary,
        # or the run renderer could not compose the two layers
        for o in x['operations']:
            s, e = int(o['canonical_start']), int(o['canonical_end'])
            for sg in segs.get(p['id'], []):
                if s < sg['end_char'] and e > sg['start_char'] and \
                   not (s >= sg['start_char'] and e <= sg['end_char']):
                    crossing += 1
            tiers[o['evidence_tier']] += 1
            actions[o['action']] += 1
            n_ops += 1

        per_vol[vol_of[p['id']]][p['id']] = [
            {'s': int(o['canonical_start']), 'e': int(o['canonical_end']),
             't': o['source_token'], 'r': o['display_replacement'],
             'a': o['action'], 'd': o['decision_id'],
             'p': o.get('pair_id') or ''}
            for o in sorted(x['operations'], key=lambda z: int(z['canonical_start']))
        ]
    if crossing:
        die('MAP_INTEGRITY_FAIL', '%d operations straddle a speaker-segment boundary' % crossing)

    # ---- app-derived ledger: leading source section markers "(2) " ---------
    # The deployed reader stripped these with a regex over rendered HTML, which
    # deleted characters and desynchronised canonical offsets. They become
    # suppression ranges instead: zero visible width, canonical range retained.
    # This ledger is app-derived layout suppression, NOT part of the governing
    # dash handoff, and is tagged accordingly so provenance stays honest.
    SECT = re.compile(r'^\(\d+\)\s*')
    n_sect = 0
    split_markers = []
    for pid, p in by_id.items():
        mm = SECT.match(p['text'])
        if not mm:
            continue
        s, e = mm.start(), mm.end()
        existing = per_vol[vol_of[pid]].get(pid, [])
        if any(not (o['e'] <= s or o['s'] >= e) for o in existing):
            die('MAP_INTEGRITY_FAIL', 'section marker overlaps a mapped operation: %s' % pid)
        # A marker may end inside a speaker segment (one corpus case, where a
        # JESUS segment is anchored [0,3) over "(6)"). Split the suppression at
        # every segment edge so no operation straddles a boundary. The visible
        # result is identical and each piece keeps its exact canonical range.
        cuts = {s, e}
        for sg in segs.get(pid, []):
            for edge in (sg['start_char'], sg['end_char']):
                if s < edge < e:
                    cuts.add(edge)
        pieces = sorted(cuts)
        per_vol[vol_of[pid]].setdefault(pid, [])
        for k in range(len(pieces) - 1):
            ps, pe = pieces[k], pieces[k + 1]
            per_vol[vol_of[pid]][pid].append(
                {'s': ps, 'e': pe, 't': p['text'][ps:pe], 'r': '',
                 'a': 'SUPPRESS_SECTION_MARKER',
                 'd': 'SECT-%05d%s' % (n_sect + 1, chr(97 + k) if len(pieces) > 2 else ''),
                 'p': ''})
            actions['SUPPRESS_SECTION_MARKER'] += 1
            tiers['APP_DERIVED_LAYOUT_SUPPRESSION'] += 1
        if len(pieces) > 2:
            split_markers.append(p['stable_ref'])
        per_vol[vol_of[pid]][pid].sort(key=lambda o: o['s'])
        n_sect += 1
    print('section markers suppressed: %d' % n_sect)

    # ---- the 14 source-verified repairs must be inside the consolidated map -
    sr = json.load(open(os.path.join(a.handoff_dir,
                   'LDC_R1B_source_verified_display_repairs_14.json'), encoding='utf-8'))
    if len(sr) != 14:
        die('MAP_INTEGRITY_FAIL', 'expected 14 source-verified repairs, got %d' % len(sr))
    mb = {x['stable_ref']: x for x in m}
    for r in sr:
        if apply_ops(r['canonical_text'], r['operations']) != r['expected_display_fragment']:
            die('MAP_INTEGRITY_FAIL', 'source-verified repair projection differs %s' % r['stable_ref'])
        mids = {o['decision_id'] for o in mb[r['stable_ref']]['operations']}
        if not {o['decision_id'] for o in r['operations']} <= mids:
            die('MAP_INTEGRITY_FAIL', 'repair %s not represented in consolidated map' % r['stable_ref'])

    # ---- titles ------------------------------------------------------------
    T = json.load(open(os.path.join(a.handoff_dir, 'LDC_R1B_title_display_decisions.json'),
                       encoding='utf-8'))
    if len(T) != 38:
        die('MAP_INTEGRITY_FAIL', 'expected 38 title decisions, got %d' % len(T))
    overrides = {t['stable_ref']: t['display_title']
                 for t in T if t.get('canonical_title') != t.get('display_title')}
    if len(overrides) != 1 or 'LDC.T04.1902-07-31' not in overrides:
        die('MAP_INTEGRITY_FAIL', 'title override set is %r' % sorted(overrides))

    # ---- quarantine must remain non-executable -----------------------------
    q = json.load(open(os.path.join(a.handoff_dir,
                  'LDC_R1B_CANONICAL_MUTATIONS_QUARANTINED_DO_NOT_APPLY.json'), encoding='utf-8'))
    if q['status'] != 'DO_NOT_APPLY_IN_STRUCTURAL_DASH_APP_PATCH':
        die('MAP_INTEGRITY_FAIL', 'quarantine status changed')

    # ---- emit --------------------------------------------------------------
    total_bytes = 0
    for nn in range(1, 37):
        doc = {'schema_version': SCHEMA, 'volume': nn, 'corpus_version': CORPUS_VERSION,
               'paragraph_count': len(per_vol.get(nn, {})), 'paragraphs': per_vol.get(nn, {})}
        path = os.path.join(a.corpus_dir, 'display_%02d.json' % nn)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))
        total_bytes += os.path.getsize(path)
    with open(os.path.join(a.corpus_dir, 'display_titles.json'), 'w', encoding='utf-8') as fh:
        json.dump({'schema_version': SCHEMA, 'corpus_version': CORPUS_VERSION,
                   'overrides': overrides}, fh, ensure_ascii=False, indent=1)

    # ---- CORPUS_MUTATION_DETECTED gate -------------------------------------
    for nn in range(1, 37):
        for p in json.load(open(os.path.join(a.corpus_dir, 'paragraphs_%02d.json' % nn),
                                encoding='utf-8')):
            if hashlib.sha256(p['text'].encode('utf-8')).hexdigest() != pre[p['id']]:
                die('CORPUS_MUTATION_DETECTED', p['id'])

    report = {
        'schema': 'ldc-display-transform-report-v1',
        'handoff': 'LDC_R1B_Structural_Dash_Implementation_Handoff_RECHECKED_v2',
        'corpus_version': CORPUS_VERSION,
        'mapped_paragraphs': len(m), 'handoff_operations': n_ops,
        'app_section_markers': n_sect,
        'app_section_markers_split_at_segment_edge': split_markers,
        'total_operations': n_ops + sum(v for k,v in actions.items() if k=='SUPPRESS_SECTION_MARKER') ,
        'operations_straddling_speaker_segment': 0,
        'evidence_tiers': dict(tiers), 'actions': dict(actions),
        'source_verified_repairs': 14,
        'title_decisions': 38, 'title_overrides': overrides,
        'canonical_paragraphs_mutated': 0,
        'display_files_bytes': total_bytes,
    }
    with open(os.path.join(a.report_dir, 'display_transform_report.json'), 'w',
              encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print('\n=== DISPLAY TRANSFORM LAYER BUILT ===')


if __name__ == '__main__':
    main()
