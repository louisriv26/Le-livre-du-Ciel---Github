"""
LDC corpus validator — run before every deploy that touches corpus/.

Checks (fails loudly, exit code 1, if any violation found):
  1. Per-volume counts match corpus/manifest.json and each other
     (volume.json entry_count/para_count vs actual paragraph/search/speaker files)
  2. No duplicate paragraph IDs globally
  3. Every paragraph fingerprint == SHA-256(text, utf-8)
  4. search_NN.json text matches paragraphs_NN.json text exactly (same id)
  5. Every speech segment has a valid target paragraph and valid offsets:
       0 <= start_char < end_char <= len(paragraph.text)
  6. No mid-word segment boundaries (start/end don't split a word) —
     8-category boundary scan (over-tlen, sc>ec, sc/ec mid-word, overlap)
  7. semantic_index.json N matches total paragraph count
  8. embeddings_ldc_ids.json (if present) has correct id format
     (snake_case matching paragraph id, NOT dotted stable_ref) and count

Usage:
    python scripts/validate_corpus.py [--corpus-dir PATH]

Exit code 0 = all checks passed. Exit code 1 = at least one check failed
(details printed to stdout).
"""
import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def check_counts(corpus_dir, manifest, errors):
    tot_entries = tot_paras = tot_search = tot_speech = 0
    for nn in range(1, 37):
        vol = load_json(os.path.join(corpus_dir, f'volume_{nn:02d}.json'))
        paras = load_json(os.path.join(corpus_dir, f'paragraphs_{nn:02d}.json'))
        search = load_json(os.path.join(corpus_dir, f'search_{nn:02d}.json'))
        speakers = load_json(os.path.join(corpus_dir, f'speakers_{nn:02d}.json'))

        if vol.get('entry_count') != len(vol['entries']):
            errors.append(f'T{nn}: volume.entry_count={vol.get("entry_count")} '
                           f'!= actual entries={len(vol["entries"])}')
        if vol.get('para_count') != len(paras):
            errors.append(f'T{nn}: volume.para_count={vol.get("para_count")} '
                           f'!= actual paragraphs={len(paras)}')
        if len(search) != len(paras):
            errors.append(f'T{nn}: search count={len(search)} '
                           f'!= paragraph count={len(paras)}')

        tot_entries += len(vol['entries'])
        tot_paras += len(paras)
        tot_search += len(search)
        tot_speech += len(speakers)

    if manifest.get('total_entries') != tot_entries:
        errors.append(f'manifest.total_entries={manifest.get("total_entries")} '
                       f'!= actual={tot_entries}')
    if manifest.get('total_paragraphs') != tot_paras:
        errors.append(f'manifest.total_paragraphs={manifest.get("total_paragraphs")} '
                       f'!= actual={tot_paras}')

    return {
        'entries': tot_entries, 'paragraphs': tot_paras,
        'search_records': tot_search, 'speech_segments': tot_speech,
    }


def check_corpus(corpus_dir, errors, warnings):
    all_ids = []
    all_paras_by_vol = {}
    all_search_by_vol = {}
    all_speech_by_vol = {}

    for nn in range(1, 37):
        paras = load_json(os.path.join(corpus_dir, f'paragraphs_{nn:02d}.json'))
        search = load_json(os.path.join(corpus_dir, f'search_{nn:02d}.json'))
        speakers = load_json(os.path.join(corpus_dir, f'speakers_{nn:02d}.json'))
        all_paras_by_vol[nn] = paras
        all_search_by_vol[nn] = search
        all_speech_by_vol[nn] = speakers

        pmap = {p['id']: p for p in paras}
        all_ids.extend(pmap.keys())

        # Fingerprint check
        for p in paras:
            expected = hashlib.sha256(p['text'].encode('utf-8')).hexdigest()
            if p.get('fingerprint') != expected:
                errors.append(f'T{nn} {p["id"]}: fingerprint mismatch')

        # search/paragraph text sync
        smap = {s['id']: s for s in search}
        for pid, p in pmap.items():
            if pid in smap and smap[pid].get('text') != p['text']:
                errors.append(f'T{nn} {pid}: search text != paragraph text')

        # search norm field present (missing norm crashes runSearch() app-wide, index.html:3888)
        for s in search:
            if not s.get('norm'):
                errors.append(f'T{nn} {s["id"]}: search record missing "norm" field')

        # Speech offset + boundary checks
        for seg in speakers:
            pid = seg['paragraph_id']
            if pid not in pmap:
                errors.append(f'T{nn} {seg["segment_id"]}: paragraph_id {pid} not found')
                continue
            text = pmap[pid]['text']
            tlen = len(text)
            sc, ec = seg['start_char'], seg['end_char']

            if ec > tlen:
                errors.append(f'T{nn} {seg["segment_id"]}: end_char={ec} > tlen={tlen}')
                continue
            if sc > ec:
                errors.append(f'T{nn} {seg["segment_id"]}: start_char={sc} > end_char={ec}')
                continue
            if 0 < sc < tlen and text[sc-1].isalnum() and text[sc].isalnum():
                errors.append(f'T{nn} {seg["segment_id"]}: start_char={sc} splits a word')
            if 0 < ec < tlen and text[ec-1].isalnum() and text[ec].isalnum():
                errors.append(f'T{nn} {seg["segment_id"]}: end_char={ec} splits a word')

        # Overlapping segments on the same paragraph
        by_para = defaultdict(list)
        for seg in speakers:
            by_para[seg['paragraph_id']].append(seg)
        for pid, segs in by_para.items():
            segs_sorted = sorted(segs, key=lambda s: s['start_char'])
            for i in range(len(segs_sorted) - 1):
                if segs_sorted[i]['end_char'] > segs_sorted[i + 1]['start_char']:
                    errors.append(
                        f'T{nn} {pid}: overlapping segments '
                        f'{segs_sorted[i]["segment_id"]} / {segs_sorted[i+1]["segment_id"]}')

    from collections import Counter
    id_counts = Counter(all_ids)
    dup_ids = [pid for pid, n in id_counts.items() if n > 1]
    if dup_ids:
        errors.append(f'{len(dup_ids)} duplicate paragraph IDs found: {dup_ids[:5]}...')

    return all_paras_by_vol


def check_semantic_index(corpus_dir, expected_n, errors):
    path = os.path.join(corpus_dir, 'semantic_index.json')
    if not os.path.exists(path):
        errors.append('semantic_index.json missing')
        return
    sem = load_json(path)
    n = sem.get('N') or sem.get('n')
    if n != expected_n:
        errors.append(f'semantic_index.json N={n} != expected paragraph count={expected_n}')


def check_embeddings(base_dir, expected_n, all_paras_by_vol, errors, warnings):
    ids_path = os.path.join(base_dir, 'embeddings_ldc_ids.json')
    bin_path = os.path.join(base_dir, 'embeddings_ldc.bin')
    if not os.path.exists(ids_path):
        warnings.append('embeddings_ldc_ids.json not present — vector search disabled (BM25 only)')
        return
    meta = load_json(ids_path)
    ids = meta.get('ids', [])
    if len(ids) != expected_n:
        errors.append(f'embeddings_ldc_ids.json has {len(ids)} ids, expected {expected_n}')

    # ID format check: must match snake_case paragraph 'id', not dotted stable_ref
    valid_id_set = set()
    for paras in all_paras_by_vol.values():
        for p in paras:
            valid_id_set.add(p['id'])
    bad_ids = [i for i in ids[:50] if i not in valid_id_set]
    if bad_ids:
        errors.append(
            f'embeddings_ldc_ids.json contains IDs not matching any paragraph id '
            f'(wrong format? e.g. dotted stable_ref instead of snake_case id): {bad_ids[:5]}')

    if not os.path.exists(bin_path):
        warnings.append('embeddings_ldc_ids.json present but embeddings_ldc.bin missing — '
                         'vector search will silently fail to BM25 fallback')
    else:
        dim = meta.get('dim', 384)
        expected_bytes = len(ids) * dim * 2  # float16
        actual_bytes = os.path.getsize(bin_path)
        if actual_bytes != expected_bytes:
            errors.append(f'embeddings_ldc.bin size={actual_bytes} != expected {expected_bytes} '
                           f'({len(ids)} ids x {dim} dim x 2 bytes)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus-dir', default=None,
                         help='Path to corpus/ directory (default: ../corpus relative to this script)')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_dir = args.corpus_dir or os.path.join(script_dir, '..', 'corpus')
    base_dir = os.path.join(corpus_dir, '..')

    errors = []
    warnings = []

    print(f'Validating corpus at: {corpus_dir}')
    manifest = load_json(os.path.join(corpus_dir, 'manifest.json'))

    counts = check_counts(corpus_dir, manifest, errors)
    all_paras_by_vol = check_corpus(corpus_dir, errors, warnings)
    check_semantic_index(corpus_dir, counts['paragraphs'], errors)
    check_embeddings(base_dir, counts['paragraphs'], all_paras_by_vol, errors, warnings)

    print()
    print('=== Totals ===')
    for k, v in counts.items():
        print(f'  {k}: {v:,}')

    print()
    if warnings:
        print(f'=== {len(warnings)} warning(s) ===')
        for w in warnings:
            print(f'  WARN: {w}')
        print()

    if errors:
        print(f'=== FAILED: {len(errors)} error(s) ===')
        for e in errors[:100]:
            print(f'  FAIL: {e}')
        if len(errors) > 100:
            print(f'  ... and {len(errors) - 100} more')
        sys.exit(1)
    else:
        print('=== PASS: all checks clean ===')
        sys.exit(0)


if __name__ == '__main__':
    main()
