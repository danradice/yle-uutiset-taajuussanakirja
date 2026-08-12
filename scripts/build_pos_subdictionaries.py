"""Split the frequency dictionary into one subdictionary per word class.

Reads the final frequency_dicts/taajuussanasto_ylenews_2011_2024.tsv and writes
one tab-separated file per word class to frequency_dicts/subdictionaries/,
each keeping the dictionary's three columns and its frequency-descending order.

A lemma listed under several word classes (e.g. `mukaan` = "adverbi, postpositio")
appears in *every* matching subdictionary carrying its **full** count. The corpus
count behind such a lemma was never split between its classes, so there is no
per-class figure to give: the merged total is the only honest number. This means
the subdictionaries deliberately overlap, and their counts must not be summed
across files — doing so double-counts every multi-class lemma.

The `Sanaluokat` column is carried over unchanged, so a row in, say, the verbi
subdictionary still shows whether its count is shared with another class. The
trailing asterisk (a class carried by more than one sense) is ignored when
grouping but preserved in the output.

Rows with a blank `Sanaluokat` belong to no class; the sanalista lists these
forms without a word class (`enempää`, `osin`, `vuonna`, ...). They go to
`taajuussanasto_luokittelematon.tsv` so no dictionary row is lost.
"""

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTIONARY = ROOT / "frequency_dicts/taajuussanasto_ylenews_2011_2024.tsv"
OUTDIR = ROOT / "frequency_dicts/subdictionaries"


def filename_slug(cls):
    """ASCII-safe filename stem for a word class (järjestysluku -> jarjestysluku).

    Only the filename is transliterated; the Sanaluokat values inside the files
    keep their original spelling.
    """
    return cls.translate(str.maketrans("äöåÄÖÅ", "aoaAOA"))


def split_classes(sanaluokat):
    """Split a Sanaluokat cell into individual classes, dropping any asterisk."""
    classes = []
    for part in (sanaluokat or "").split(","):
        cls = part.strip().rstrip("*").strip()
        if cls:
            classes.append(cls)
    return classes


def main():
    with open(DICTIONARY, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [(r[0], r[1], int(r[2])) for r in reader if r]

    by_class = defaultdict(list)
    unassigned = []
    for row in rows:
        classes = split_classes(row[1])
        if not classes:
            unassigned.append(row)
            continue
        for cls in classes:
            by_class[cls].append(row)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for cls, cls_rows in sorted(by_class.items(), key=lambda kv: -len(kv[1])):
        cls_rows.sort(key=lambda r: (-r[2], r[0]))  # frequency desc, then headword
        path = OUTDIR / f"taajuussanasto_{filename_slug(cls)}.tsv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(header)
            writer.writerows(cls_rows)
        print(f"{len(cls_rows):>6} rows  {path.name}")

    if unassigned:
        unassigned.sort(key=lambda r: (-r[2], r[0]))
        path = OUTDIR / "taajuussanasto_luokittelematon.tsv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(header)
            writer.writerows(unassigned)
        print(f"{len(unassigned):>6} rows  {path.name}  (blank Sanaluokat)")

    multi = sum(1 for r in rows if len(split_classes(r[1])) > 1)
    written = sum(len(v) for v in by_class.values()) + len(unassigned)
    print(
        f"\n{len(rows)} dictionary rows -> {written} rows across "
        f"{len(by_class) + bool(unassigned)} files ({multi} multi-class lemmas duplicated)"
    )


if __name__ == "__main__":
    main()
