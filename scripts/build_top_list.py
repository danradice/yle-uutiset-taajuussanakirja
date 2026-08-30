"""Cut the learner-facing top-N head off the frequency dictionary.

Writes the same rows in two formats, because they serve different people:

    frequency_dicts/taajuussanakirja_top10000.tsv   UTF-8, LF      — canonical
    frequency_dicts/taajuussanakirja_top10000.csv   UTF-8 BOM, CRLF — Excel

The CSV is the one file in this repository that keeps CRLF: RFC 4180 specifies
it and Excel expects it, and the BOM is what makes Excel render ä/ö correctly
instead of mojibake. Every TSV here is LF.

The dictionary is already sorted by frequency descending then headword, so this
is a *head, not a re-sort* — `rows[:TOP_N]`, verbatim. Taking a slice of an
already-ordered file means the top list cannot disagree with the dictionary
about ordering or content; any bug would have to be in stage 2, where it would
show up everywhere rather than only here.

Same three columns as the dictionary, and deliberately no `rank`: the homonym
split puts some lemmas on two rows, and ties in `count` leave rank ambiguous, so
a rank column would be this script's invention rather than the data's.

Both files land under GitHub's 512 KB limit for rendering tabular data, so they
display as browsable tables on github.com — which the 2.4 MB full dictionary
does not. That is the main reason they are committed rather than generated at
release time, and they are the only assets a release uploads.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTIONARY = ROOT / "frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv"
OUTDIR = ROOT / "frequency_dicts"
TOP_N = 10000


def main():
    with open(DICTIONARY, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [r for r in reader if r]

    head = rows[:TOP_N]

    tsv_path = OUTDIR / f"taajuussanakirja_top{TOP_N}.tsv"
    with open(tsv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(head)

    # utf-8-sig writes the BOM; the default dialect is RFC 4180 (comma, CRLF).
    csv_path = OUTDIR / f"taajuussanakirja_top{TOP_N}.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(head)

    print(f"{len(head)} rows -> {tsv_path.name}, {csv_path.name}")

    total = sum(int(r[2]) for r in rows)
    covered = sum(int(r[2]) for r in head)
    boundary = int(head[-1][2])
    distinct = len({r[0] for r in head})
    print(
        f"  covers {covered / total * 100:.2f}% of all corpus tokens; "
        f"lowest count {boundary}"
    )
    print(
        f"  {distinct} distinct lemmas "
        f"({len(head) - distinct} appear twice from the homonym split)"
    )

    # The cutoff is positional, so it can fall in the middle of a run of equal
    # counts and exclude words no less frequent than the last one kept. That is
    # acceptable but must never be silent — a future recount could land the
    # boundary on a much larger tie.
    excluded_ties = sum(1 for r in rows[TOP_N:] if int(r[2]) == boundary)
    if excluded_ties:
        print(
            f"  NOTE: {excluded_ties} further row(s) share count {boundary} "
            f"and fall outside the cutoff"
        )


if __name__ == "__main__":
    main()
