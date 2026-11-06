"""Count the wordlist's lemmas in the Yle News (2011-2024) VRT files.

Stage 1 of the pipeline, and the only stage that needs the corpora. One pass
over the locally-downloaded YLENEWS VRT files (three download packages covering
2011-2024) writes two tab-separated files to auxiliary_data/:

lemma_counts_merged_2011_2024.tsv
    One row per attested headword (zero-count headwords are dropped), sorted by
    frequency descending then headword, with columns:

      Hakusana   - the headword/lemma.
      Sanaluokat - the possible word classes for the lemma, taken from the
                   wordlist's Sanaluokka column across all of the lemma's senses.
                   A word class carried by more than one sense (i.e. the lemma has
                   several meanings of that same part of speech) is flagged with
                   a trailing asterisk, e.g. "substantiivi*, adjektiivi".
      count      - corpus occurrences of that lemma, POS ignored (all word
                   classes merged).

    POS is deliberately not used to split counts: the sanalista already fixes
    each lemma's word class(es), and trusting the corpus tagger only fragments
    a lemma's counts across spurious classes (e.g. bogus "Foreign" tags).

homonym_pos_counts_2011_2024_raw.tsv
    The raw material for the manual homonym review. Merging is wrong for
    homonyms whose senses are *different* parts of speech (panna = verb "to
    put" vs. noun "a ban"), so their counts are broken down by the tagger's pos
    code. Target lemmas: headwords the sanalista marks as homonyms (numbered
    Homonymia) whose senses map to more than one distinct VRT pos code.
    Homonyms whose senses share a single code (two substantiivi senses, both N)
    are excluded, since the corpus tag cannot tell those apart. Columns:

      Hakusana - the homonym headword/lemma.
      pos      - the VRT pos code the tagger assigned.
      count    - occurrences of the lemma under that pos. An expected pos code
                 with no corpus hits still gets a row, with count 0, so every
                 word class the sanalista lists is represented.
      expected - "yes" if `pos` is one of the codes the sanalista's word classes
                 for this lemma map to, else "no". A "no" row is a tagger POS the
                 sanalista doesn't list (often a mistag, e.g. spurious Foreign).

    Rows are sorted by headword, then count descending within each headword.
    Both files are counted in the same pass, so a homonym's per-pos counts sum
    to its merged count.

Counting runs over the sentences vrt_sentences.iter_kept_tokens() keeps: each
distinct sentence once, with alt texts, robot texts and reviewed boilerplate
removed and short plain sentences protected (see that module). Only lemmas in
the wordlist are counted, which keeps memory bounded across the whole 14-year
dataset. Punct tokens are never counted.
"""

import csv
from collections import Counter, defaultdict

from sanalista import format_sanaluokat, load_wordlist, pos_codes
from vrt_sentences import ROOT, VRT_ROOTS, iter_kept_tokens, report, vrt_files

MERGED = ROOT / "auxiliary_data/lemma_counts_merged_2011_2024.tsv"
HOMONYMS = ROOT / "auxiliary_data/homonym_pos_counts_2011_2024_raw.tsv"


def homonym_targets(senses):
    """Return {lemma: expected VRT code set} for multi-code homonyms."""
    targets = {}
    for lemma, rows in senses.items():
        if not any(row["Homonymia"].strip() for row in rows):
            continue
        codes = pos_codes(row["Sanaluokka"] for row in rows)
        if len(codes) > 1:
            targets[lemma] = codes
    return targets


def write_merged(senses, counts):
    rows = [
        (lemma, format_sanaluokat(r["Sanaluokka"] for r in senses[lemma]), count)
        for lemma in senses
        if (count := counts.get(lemma, 0)) > 0
    ]
    rows.sort(key=lambda r: (-r[2], r[0]))  # frequency desc, then headword

    with open(MERGED, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Hakusana", "Sanaluokat", "count"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {MERGED}")


def write_homonyms(targets, pos_counts):
    rows = [
        (lemma, pos, count, "yes" if pos in targets[lemma] else "no")
        for (lemma, pos), count in pos_counts.items()
    ]

    # An expected pos code with no corpus hits still gets a row (count 0), so
    # every word class the sanalista lists for the lemma is represented.
    seen = defaultdict(set)
    for lemma, pos in pos_counts:
        seen[lemma].add(pos)
    rows += [
        (lemma, pos, 0, "yes")
        for lemma, codes in targets.items()
        for pos in sorted(codes - seen[lemma])
    ]

    rows.sort(key=lambda r: (r[0], -r[2], r[1]))  # headword asc, count desc, pos

    with open(HOMONYMS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Hakusana", "pos", "count", "expected"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} (lemma, pos) rows for {len(targets)} lemmas to {HOMONYMS}")


def main():
    senses = load_wordlist()
    targets = homonym_targets(senses)
    print(f"Loaded {len(senses)} unique headwords, {len(targets)} multi-pos homonyms")

    paths = vrt_files()
    print(f"Found {len(paths)} VRT files across {len(VRT_ROOTS)} roots")

    counts = Counter()
    pos_counts = Counter()
    stats = Counter()
    for lemma, pos in iter_kept_tokens(paths, stats):
        if lemma in senses:
            counts[lemma] += 1
            if lemma in targets:
                pos_counts[(lemma, pos)] += 1
    report(stats)

    write_merged(senses, counts)
    write_homonyms(targets, pos_counts)


if __name__ == "__main__":
    main()
