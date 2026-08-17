"""Build the Yle News (2011-2024) frequency list for nykysuomensanalista2024.txt.

Counts every wordlist headword's lemma frequency across the locally-downloaded
YLENEWS VRT files (three separate download packages covering 2011-2024), then
writes one row per attested headword (zero-count headwords are dropped), sorted
by frequency descending then headword. The output is tab-separated, with columns:

  Hakusana   - the headword/lemma.
  Sanaluokat - the possible word classes for the lemma, taken from the
               wordlist's Sanaluokka column across all of the lemma's senses.
               A word class carried by more than one sense (i.e. the lemma has
               several meanings of that same part of speech) is flagged with a
               trailing asterisk, e.g. "substantiivi*, adjektiivi".
  count      - total corpus occurrences of that lemma, POS ignored (all word
               classes merged). Only lemmas in the wordlist are counted, which
               keeps memory bounded across the whole 14-year dataset.

POS is deliberately not used to split counts: the sanalista already fixes each
lemma's word class(es), and trusting the corpus tagger only fragments a lemma's
counts across spurious classes (e.g. bogus "Foreign" tags).

YLENEWS VRT columns are: word, ref, lemma, lemmacomp, pos, msd, dephead,
deprel, lex - note lemma is field index 2 and pos is index 4 (not 3, that's
lemmacomp). Punct tokens are dropped.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDLIST = ROOT / "word_lists/nykysuomensanalista2024.txt"
VRT_ROOTS = [
    ROOT / "corpora/ylenews-fi-2011-2018-s-vrt/vrt",
    ROOT / "corpora/ylenews-fi-2019-2021-s-vrt/vrt",
    ROOT / "corpora/ylenews-fi-2022-2024-s-vrt/data",
]
OUTPUT = ROOT / "auxiliary_data/lemma_counts_merged_2011_2024.tsv"


def split_classes(sanaluokka):
    """Split a (possibly multi-valued) Sanaluokka field into individual classes.

    A single sense can carry several word classes, e.g. "substantiivi, adjektiivi"
    (comma- or "+"-separated), so a field is not one opaque label.
    """
    classes = []
    for part in (sanaluokka or "").split(","):
        for tok in part.split("+"):
            tok = tok.strip()
            if tok:
                classes.append(tok)
    return classes


def format_sanaluokat(fields):
    """Format the Sanaluokat cell from a lemma's per-sense Sanaluokka fields.

    `fields` is the list of raw Sanaluokka values, one per wordlist row (sense),
    in sense order. Each word class is listed once, in order of first appearance;
    a class carried by more than one sense gets a trailing asterisk.
    """
    order = []
    meanings = Counter()
    for field in fields:
        for pos in dict.fromkeys(split_classes(field)):  # distinct within a sense
            if pos not in meanings:
                order.append(pos)
            meanings[pos] += 1
    return ", ".join(pos + ("*" if meanings[pos] > 1 else "") for pos in order)


def load_wordlist(path):
    """Return (unique headwords in first-seen order, headword -> [Sanaluokka...])."""
    order = []
    senses = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            lemma = row["Hakusana"]
            if lemma not in senses:
                order.append(lemma)
            senses[lemma].append(row["Sanaluokka"])
    return order, senses


def count_file(vrt_path, target_lemmas, counts):
    with open(vrt_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("<"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 5:
                continue
            lemma = fields[2]
            pos = fields[4]
            if pos == "Punct" or lemma not in target_lemmas:
                continue
            counts[lemma] += 1


def main():
    order, senses = load_wordlist(WORDLIST)
    target_lemmas = set(senses)
    print(f"Loaded {len(order)} unique headwords from {WORDLIST}")

    vrt_files = sorted(
        f for root in VRT_ROOTS for f in root.glob("**/*.vrt")
    )
    print(f"Found {len(vrt_files)} VRT files across {len(VRT_ROOTS)} roots")

    counts = Counter()
    for i, vrt_path in enumerate(vrt_files, 1):
        count_file(vrt_path, target_lemmas, counts)
        print(f"[{i}/{len(vrt_files)}] processed {vrt_path}", file=sys.stderr)

    rows = [
        (lemma, format_sanaluokat(senses[lemma]), count)
        for lemma in order
        if (count := counts.get(lemma, 0)) > 0
    ]
    rows.sort(key=lambda r: (-r[2], r[0]))  # frequency desc, then headword

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Hakusana", "Sanaluokat", "count"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
