"""Per-POS corpus counts for the multi-word-class homonyms, for disambiguation.

The main frequency list (count_local_vrt.py) merges every word class under one
lemma total. That is wrong for homonyms whose senses are *different* parts of
speech (e.g. panna = verb "to put" vs. noun "a ban"): their merged count needs
splitting back out per sense. This script produces the raw material for that.

Target lemmas: headwords the sanalista marks as homonyms (numbered Homonymia)
whose senses map to more than one distinct VRT pos code. Homonyms whose senses
share a single code (e.g. two substantiivi senses -> both N) are excluded, since
the corpus tag cannot tell those apart.

For each target lemma it counts occurrences in the YLENEWS VRT files broken down
by the tagger's pos code (N, V, A, Adv, ...), and writes a tab-separated table:

  Hakusana - the homonym headword/lemma.
  pos      - the VRT pos code the tagger assigned.
  count    - occurrences of the lemma under that pos, 2011-2024. An expected
             pos code that never occurs in the corpus still gets a row, with
             count 0, so every word class the sanalista lists is represented.
  expected - "yes" if `pos` is one of the codes the sanalista's word classes for
             this lemma map to, else "no". An "no" row is a tagger POS the
             sanalista doesn't list (often a mistag, e.g. spurious Foreign) and
             flags where manual disambiguation is needed.

Rows are sorted by headword, then count descending within each headword.

YLENEWS VRT columns: word, ref, lemma, lemmacomp, pos, msd, dephead, deprel,
lex - lemma is field index 2, pos is index 4. Punct tokens are dropped.
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
OUTPUT = ROOT / "auxiliary_data/homonym_pos_counts_2011_2024_raw.tsv"

# Sanaluokka (sanalista word class) -> VRT/Korp pos code(s). The corpus does not
# distinguish prepositio/postpositio (both Adp), so those collapse onto one code.
SANALUOKKA_TO_POS = {
    "substantiivi": {"N"},
    "verbi": {"V"},
    "adjektiivi": {"A"},
    "adverbi": {"Adv"},
    "pronomini": {"Pron"},
    "numeraali": {"Num"},
    "järjestysluku": {"Num"},
    "konjunktio": {"C", "CS"},
    "rinnastuskonjunktio": {"C"},
    "alistuskonjunktio": {"CS"},
    "interjektio": {"Interj"},
    "postpositio": {"Adp"},
    "prepositio": {"Adp"},
    "kieltoverbi": {"V"},
}


def split_classes(sanaluokka):
    """Split a (possibly multi-valued) Sanaluokka field into individual classes."""
    classes = []
    for part in (sanaluokka or "").split(","):
        for tok in part.split("+"):
            tok = tok.strip()
            if tok:
                classes.append(tok)
    return classes


def expected_pos_codes(sanaluokka_fields):
    """Union of VRT pos codes the lemma's sanalista word classes map to."""
    codes = set()
    for field in sanaluokka_fields:
        for cls in split_classes(field):
            codes |= SANALUOKKA_TO_POS.get(cls, set())
    return codes


def load_target_lemmas(path):
    """Return {lemma: expected VRT code set} for multi-code homonyms."""
    senses = defaultdict(list)      # lemma -> list of Sanaluokka fields
    is_homonym = defaultdict(bool)  # lemma -> any numbered Homonymia?
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            lemma = row["Hakusana"]
            senses[lemma].append(row["Sanaluokka"])
            if row["Homonymia"].strip():
                is_homonym[lemma] = True

    targets = {}
    for lemma, fields in senses.items():
        if not is_homonym[lemma]:
            continue
        codes = expected_pos_codes(fields)
        if len(codes) > 1:
            targets[lemma] = codes
    return targets


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
            counts[(lemma, pos)] += 1


def main():
    targets = load_target_lemmas(WORDLIST)
    print(f"Loaded {len(targets)} multi-pos homonym lemmas from {WORDLIST}")

    vrt_files = sorted(f for root in VRT_ROOTS for f in root.glob("**/*.vrt"))
    print(f"Found {len(vrt_files)} VRT files across {len(VRT_ROOTS)} roots")

    counts = Counter()
    for i, vrt_path in enumerate(vrt_files, 1):
        count_file(vrt_path, targets, counts)
        print(f"[{i}/{len(vrt_files)}] processed {vrt_path}", file=sys.stderr)

    rows = [
        (lemma, pos, count, "yes" if pos in targets[lemma] else "no")
        for (lemma, pos), count in counts.items()
    ]

    # An expected pos code with no corpus hits still gets a row (count 0), so
    # every word class the sanalista lists for the lemma is represented.
    seen = defaultdict(set)
    for lemma, pos in counts:
        seen[lemma].add(pos)
    rows += [
        (lemma, pos, 0, "yes")
        for lemma, codes in targets.items()
        for pos in sorted(codes - seen[lemma])
    ]

    rows.sort(key=lambda r: (r[0], -r[2], r[1]))  # headword asc, count desc, pos

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Hakusana", "pos", "count", "expected"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} (lemma, pos) rows for {len(targets)} lemmas to {OUTPUT}")


if __name__ == "__main__":
    main()
