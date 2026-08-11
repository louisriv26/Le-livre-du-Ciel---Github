# -*- coding: utf-8 -*-
"""Export reports/cross_fragment_speech_run_links.csv (instruction v2 §7.4).

This is a PORT of LDCSpeechModel.buildParagraphSpeechModel + linkFlowRuns +
LDCDisplayMap.projectParagraph as they run in the browser. A port can drift from
the code it mirrors, so the script does not ask to be trusted: it prints the
SHA-256 of the CSV it produces, which must equal the hash the running app
computes over the same ledger. Mismatch = the port is wrong, not the app.
"""
import argparse, hashlib, json, os, re, sys
from collections import defaultdict

STYLED = {'JESUS': 'jesus', 'MARIE': 'marie', 'MARY': 'marie'}
LEXICAL = re.compile(r'[0-9A-Za-zÀ-ɏ]')
SECT_STRIP = re.compile(r'^\s*\(\d+\)\s*')
ATTRIB_END = re.compile(r'[:：]\s*["\'«“„]?\s*$')


def norm_speaker(s):
    return STYLED.get(s)


def build_model(text, segments):
    """Port of buildParagraphSpeechModel."""
    sorted_segs = sorted(segments, key=lambda s: (s['start_char'], s['end_char']))
    prev_end = -1
    for s in sorted_segs:
        if not (0 <= s['start_char'] < s['end_char'] <= len(text)):
            return None
        if s['start_char'] < prev_end:
            return None
        prev_end = s['end_char']

    intervals, cur = [], 0
    for s in sorted_segs:
        if s['start_char'] > cur:
            intervals.append({'start': cur, 'end': s['start_char'],
                              'text': text[cur:s['start_char']], 'speaker': None, 'styled': False})
        intervals.append({'start': s['start_char'], 'end': s['end_char'],
                          'text': text[s['start_char']:s['end_char']],
                          'speaker': s['speaker'], 'styled': s['speaker'] in STYLED})
        cur = s['end_char']
    if cur < len(text):
        intervals.append({'start': cur, 'end': len(text), 'text': text[cur:],
                          'speaker': None, 'styled': False})

    runs = []
    j = 0
    while j < len(intervals):
        iv = intervals[j]
        last = runs[-1] if runs else None
        if last and last['styled'] and iv['styled'] and \
           norm_speaker(last['speaker']) == norm_speaker(iv['speaker']) and last['end'] == iv['start']:
            last['end'] = iv['end']; last['text'] += iv['text']; j += 1; continue
        if last and last['styled'] and not iv['styled'] and j + 1 < len(intervals):
            nxt = intervals[j + 1]
            if nxt['styled'] and norm_speaker(last['speaker']) == norm_speaker(nxt['speaker']) and \
               last['end'] == iv['start'] and iv['end'] == nxt['start'] and not LEXICAL.search(iv['text']):
                last['end'] = nxt['end']; last['text'] += iv['text'] + nxt['text']; j += 2; continue
        runs.append({'start': iv['start'], 'end': iv['end'], 'text': iv['text'],
                     'speaker': iv['speaker'], 'styled': iv['styled'],
                     'runId': None, 'isContinuation': False})
        j += 1

    for r in runs:
        if not r['styled']:
            r['presentation'] = 'narrative'; continue
        before = SECT_STRIP.sub('', text[:r['start']])
        r['presentation'] = 'block' if (before.strip() == '' or ATTRIB_END.search(before)) else 'inline'
    return {'ok': True, 'runs': runs}


def project(text, ops):
    """Port of projectParagraph -> atoms."""
    if not ops:
        return None
    ops = sorted(ops, key=lambda o: (o['s'], o['e']))
    prev = -1
    for o in ops:
        if not (0 <= o['s'] <= o['e'] <= len(text)) or o['s'] < prev or text[o['s']:o['e']] != o['t']:
            return None
        prev = o['e']
    atoms, cur = [], 0
    for o in ops:
        if o['s'] > cur:
            atoms.append({'cs': cur, 'ce': o['s'], 'text': text[cur:o['s']], 'kind': 'canonical'})
        atoms.append({'cs': o['s'], 'ce': o['e'], 'text': o['r'],
                      'kind': 'suppressed' if o['r'] == '' else 'replaced'})
        cur = o['e']
    if cur < len(text):
        atoms.append({'cs': cur, 'ce': len(text), 'text': text[cur:], 'kind': 'canonical'})
    return atoms


def visible_len(atoms, frm, to):
    if atoms is None:
        return max(0, to - frm)
    n = 0
    for a in atoms:
        if a['ce'] <= frm or a['cs'] >= to:
            continue
        if a['kind'] == 'canonical':
            n += min(a['ce'], to) - max(a['cs'], frm)
        else:
            n += len(a['text'])
    return n


def link_flow_runs(members):
    """Port of linkFlowRuns — all seven §7.4 conditions."""
    links = []
    for k in range(len(members) - 1):
        cur, nxt = members[k], members[k + 1]
        b = cur.get('boundaryAfter')
        if not b or b.get('speech_run_policy') != 'continue_same_speaker_only':
            continue
        if not cur['model'] or not nxt['model']:
            continue
        cr = cur['model']['runs'][-1] if cur['model']['runs'] else None
        nr = nxt['model']['runs'][0] if nxt['model']['runs'] else None
        if not cr or not nr or not cr['styled'] or not nr['styled']:
            continue
        if norm_speaker(cr['speaker']) != norm_speaker(nr['speaker']):
            continue
        if visible_len(cur['atoms'], cr['end'], len(cur['text'])) != 0:
            continue
        if visible_len(nxt['atoms'], 0, nr['start']) != 0:
            continue
        if nr['start'] > 0:
            supp = b.get('suppress_next_leading_ranges') or []
            if not (any(r[0] == 0 and r[1] >= nr['start'] for r in supp)
                    or visible_len(nxt['atoms'], 0, nr['start']) == 0):
                continue
        if not b.get('display_joiner'):
            continue
        run_id = cr['runId'] or (cur['paraId'] + '#R' + str(len(cur['model']['runs']) - 1))
        cr['runId'] = run_id; nr['runId'] = run_id; nr['isContinuation'] = True
        links.append((run_id, cur['paraId'], nxt['paraId'], norm_speaker(cr['speaker']),
                      b['display_joiner'],
                      json.dumps(b.get('suppress_next_leading_ranges') or [], separators=(',', ''))))
    return links


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus-dir', required=True)
    ap.add_argument('--report-dir', required=True)
    ap.add_argument('--expect-sha256', default=None,
                    help='SHA-256 the running app computed for this ledger')
    a = ap.parse_args()
    os.makedirs(a.report_dir, exist_ok=True)

    rows = ['run_id,from_paragraph,to_paragraph,speaker,joiner,suppressed_leading']
    styled_local = all_local = 0
    for nn in range(1, 37):
        paras = json.load(open(os.path.join(a.corpus_dir, 'paragraphs_%02d.json' % nn), encoding='utf-8'))
        segs = json.load(open(os.path.join(a.corpus_dir, 'speakers_%02d.json' % nn), encoding='utf-8'))
        disp = json.load(open(os.path.join(a.corpus_dir, 'display_%02d.json' % nn), encoding='utf-8'))['paragraphs']
        flow = json.load(open(os.path.join(a.corpus_dir, 'flow_%02d.json' % nn), encoding='utf-8'))['groups']
        P = {p['id']: p for p in paras}
        S = defaultdict(list)
        for s in segs:
            S[s['paragraph_id']].append(s)

        def build(pid):
            p = P[pid]
            return {'paraId': pid, 'text': p['text'], 'atoms': project(p['text'], disp.get(pid)),
                    'model': build_model(p['text'], S.get(pid, []))}

        in_group = set()
        for g in flow:
            mem = []
            for m in g['members']:
                in_group.add(m['paragraph_id'])
                b = build(m['paragraph_id']); b['boundaryAfter'] = m['boundary_after']; mem.append(b)
            for m in mem:
                if m['model']:
                    all_local += len(m['model']['runs'])
                    styled_local += sum(1 for r in m['model']['runs'] if r['styled'])
            for L in link_flow_runs(mem):
                rows.append('%s,%s,%s,%s,%s,"%s"' % L)
        for p in paras:
            if p['id'] not in in_group:
                b = build(p['id'])
                if b['model']:
                    all_local += len(b['model']['runs'])
                    styled_local += sum(1 for r in b['model']['runs'] if r['styled'])

    csv_text = '\n'.join(rows)
    out = os.path.join(a.report_dir, 'cross_fragment_speech_run_links.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        fh.write(csv_text)
    digest = hashlib.sha256(csv_text.encode('utf-8')).hexdigest()

    print('paragraph-local STYLED runs before cross-fragment linking = %d' % styled_local)
    print('paragraph-local ALL runs before cross-fragment linking    = %d' % all_local)
    print('approved cross-fragment run links                         = %d' % (len(rows) - 1))
    print('final flow-level displayed STYLED runs                    = %d' % (styled_local - (len(rows) - 1)))
    print('csv bytes = %d  sha256 = %s' % (len(csv_text.encode('utf-8')), digest))
    if a.expect_sha256:
        ok = digest == a.expect_sha256
        print('app ledger sha256 = %s' % a.expect_sha256)
        print('PORT FIDELITY: %s' % ('BYTE-IDENTICAL TO THE RUNNING APP' if ok else 'MISMATCH — port is wrong'))
        if not ok:
            sys.exit(1)


if __name__ == '__main__':
    main()
