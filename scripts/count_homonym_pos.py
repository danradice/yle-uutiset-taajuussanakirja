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
  count    - occurrences of the lemma under that pos, 2011-2024, over the
             same sentences count_local_vrt.py counts (vrt_sentences.py), so
             a lemma's per-pos counts sum to its merged total. An expected
             pos code that never occurs in the corpus still gets a row, with
             count 0, so every word class the sanalista lists is represented.
  expected - "yes" if `pos` is one of the codes the sanalista's word classes for
             this lemma map to, else "no". An "no" row is a tagger POS the
             sanalista doesn't list (often a mistag, e.g. spurious Foreign) and
             flags where manual disambiguation is needed.

Rows are sorted by headword, then count descending within each headword.

VRT parsing and the repetition rules live in vrt_sentences.py. Punct tokens
are never counted.
"""

import csv
from collections import Counter, defaultdict

from vrt_sentences import ROOT, VRT_ROOTS, iter_kept_tokens, report, vrt_files

WORDLIST = ROOT / "word_lists/nykysuomensanalista2024.txt"
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


def main():
    targets = load_target_lemmas(WORDLIST)
    print(f"Loaded {len(targets)} multi-pos homonym lemmas from {WORDLIST}")

    paths = vrt_files()
    print(f"Found {len(paths)} VRT files across {len(VRT_ROOTS)} roots")

    counts = Counter()
    stats = Counter()
    for lemma, pos in iter_kept_tokens(paths, stats):
        if lemma in targets:
            counts[(lemma, pos)] += 1
    report(stats)

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
