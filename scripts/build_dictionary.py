"""Build the final frequency dictionary by splitting the merged homonym rows.

Stage 2 of the pipeline. count_lemmas.py (stage 1) merges every word class
under a single lemma total in

    auxiliary_data/lemma_counts_merged_2011_2024.tsv        (Hakusana, Sanaluokat, count)

For the homonyms whose senses are genuinely different parts of speech, that
total has been disambiguated by hand into per-POS counts in

    auxiliary_data/homonym_pos_counts_2011_2024_ready.tsv   (Hakusana, pos, count, expected)

This script folds those back in: each such lemma's single merged row is replaced
by one row per POS listed for it, carrying that POS's count, and writes the final
frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv.

The ready file uses VRT pos codes (N, V, A, ...) while the frequency list's
Sanaluokat column uses the sanalista's Finnish word-class names. Each code is
therefore mapped back to whichever of *that lemma's own* sanalista classes maps
onto it, which resolves the otherwise ambiguous codes (Num -> numeraali vs.
järjestysluku, Adp -> postpositio vs. prepositio). The trailing asterisk marking
a class carried by more than one sense is preserved.

A ready row whose pos is DROPPED ("-") holds tokens removed from the lemma
altogether (another headword mis-lemmatised onto it, or a proper name). It
counts toward the check that a lemma's rows sum to its merged total, but is not
written out. A lemma left with a single kept row is corrected rather than split,
so it keeps its merged Sanaluokat label: the column still lists the sanalista's
classes, not the one the remaining count was tagged with.

Rows for lemmas not in the ready file pass through untouched. The output is a
separate file from the stage 1 merged list, so the dictionary is always rebuilt
from that list rather than from itself (this script is not idempotent on its own
output: a lemma already split would have no single row to replace).
"""

import csv
import sys
from collections import defaultdict

from sanalista import SANALUOKKA_TO_POS, class_labels, load_wordlist
from vrt_sentences import ROOT

MERGED = ROOT / "auxiliary_data/lemma_counts_merged_2011_2024.tsv"
READY = ROOT / "auxiliary_data/homonym_pos_counts_2011_2024_ready.tsv"
OUTPUT = ROOT / "frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv"
DROPPED = "-"


def load_ready(path):
    """lemma -> [(pos, count), ...] in file order."""
    per_lemma = defaultdict(list)
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            if not row or not row[0].strip():
                continue
            per_lemma[row[0].strip()].append((row[1].strip(), int(row[2])))
    return per_lemma


def label_for(lemma, pos, labels, warnings):
    """The sanalista class label for `pos`, chosen among the lemma's own classes."""
    candidates = [c for c in labels.get(lemma, {}) if pos in SANALUOKKA_TO_POS.get(c, set())]
    if len(candidates) == 1:
        return labels[lemma][candidates[0]]
    if not candidates:
        warnings.append(f"{lemma}: pos {pos} matches no sanalista class; using {pos!r}")
        return pos
    warnings.append(f"{lemma}: pos {pos} matches several classes {candidates}; joined")
    return ", ".join(labels[lemma][c] for c in candidates)


def main():
    labels = {
        lemma: class_labels(r["Sanaluokka"] for r in rows)
        for lemma, rows in load_wordlist().items()
    }
    ready = load_ready(READY)
    print(f"Loaded per-POS counts for {len(ready)} lemmas from {READY}")

    with open(MERGED, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        freq_rows = [(r[0], r[1], int(r[2])) for r in reader if r]

    warnings = []
    out_rows = []
    seen = set()
    for lemma, sanaluokat, count in freq_rows:
        if lemma not in ready:
            out_rows.append((lemma, sanaluokat, count))
            continue
        seen.add(lemma)
        split_total = sum(c for _, c in ready[lemma])
        if split_total != count:
            warnings.append(
                f"{lemma}: split counts total {split_total} != merged count {count} "
                f"(difference {split_total - count:+d})"
            )
        kept = [(pos, c) for pos, c in ready[lemma] if pos != DROPPED]
        if len(kept) == 1:
            out_rows.append((lemma, sanaluokat, kept[0][1]))
            continue
        for pos, c in kept:
            out_rows.append((lemma, label_for(lemma, pos, labels, warnings), c))

    missing = sorted(set(ready) - seen)
    if missing:
        warnings.append(f"in ready file but not in frequency list: {missing}")

    out_rows.sort(key=lambda r: (-r[2], r[0]))  # frequency desc, then headword

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(out_rows)

    added = len(out_rows) - len(freq_rows)
    print(f"Processed {len(seen)} lemmas: {len(freq_rows)} rows -> {len(out_rows)} ({added:+d})")
    if warnings:
        print(f"\n{len(warnings)} warning(s):", file=sys.stderr)
        for w in warnings:
            print(f"  {w}", file=sys.stderr)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
