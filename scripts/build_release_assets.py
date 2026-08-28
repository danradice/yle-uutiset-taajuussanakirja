"""Package the finished dictionary into the archives published on a release.

Everything this writes is derived from files already committed to the repo, so
a release is only ever a repackaging — never a recount. The dictionary itself,
the subdictionaries, LICENSE, NOTICE and CITATION.cff are copied verbatim; the
CSV, JSON and top-5000 files are converted from the dictionary at build time
rather than committed, so there is exactly one copy of the data under version
control and the alternative formats cannot drift out of sync with it.

Writes to dist/ (gitignored, wiped on every run):

    taajuussanakirja-ylenews-2011-2024-<version>.zip
    taajuussanakirja-ylenews-2011-2024-<version>.tar.gz
    SHA256SUMS.txt      over the two archives, in `sha256sum -c` format
    RELEASE_NOTES.md    the matching section sliced out of CHANGELOG.md

Both archives hold the same tree under one top-level directory, so they unpack
cleanly. The CSV is written with a UTF-8 BOM: its whole reason for existing is
Excel, which mangles a/o umlauts without one. The TSV stays plain UTF-8.

Every format keeps the dictionary's three columns exactly. No rank column is
added -- the homonym split puts some lemmas on two rows and ties in `count`
leave rank ambiguous, so any rank would be this script's invention rather than
the data's.

Usage:

    python3 scripts/build_release_assets.py [--version 1.0.0]

The version defaults to $GITHUB_REF_NAME with a leading "v" stripped (so a
tag push needs no argument), and to "dev" outside CI.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICTIONARY = ROOT / "frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv"
SUBDICTS = ROOT / "frequency_dicts/subdictionaries"
CHANGELOG = ROOT / "CHANGELOG.md"
DIST = ROOT / "dist"

VERBATIM = ["LICENSE", "NOTICE", "CITATION.cff"]
STEM = "taajuussanakirja-ylenews-2011-2024"
TOP_N = 5000

REPO_URL = "https://github.com/danradice/yle-uutiset-taajuussanakirja"

# Links here are absolute on purpose: this README travels inside a zip, where
# the repo-relative links of the main README would all be dead.
BUNDLE_README = """\
# Yle Uutisten taajuussanakirja {version}

A news-based Finnish frequency dictionary: corpus frequencies for the headwords
of the Kotus *nykysuomen sanalista*, counted against the Yle Finnish News
Archive (YLENEWS_FI) 2011-2024.

Full documentation, the build scripts and the intermediate data:
<{repo}>

## What is in this archive

| File | Contents |
|---|---|
| `taajuussanakirja_ylenews_2011_2024.tsv` | The dictionary. {rows} rows, tab-separated, UTF-8. |
| `taajuussanakirja_ylenews_2011_2024.csv` | The same rows as RFC 4180 CSV, UTF-8 **with BOM** for Excel. |
| `taajuussanakirja_ylenews_2011_2024.json` | The same rows as an array of objects. |
| `taajuussanakirja_top5000.tsv` | The {top_n} most frequent rows. |
| `subdictionaries/` | The same data split into {subdict_count} files, one per word class. |
| `LICENSE`, `NOTICE`, `CITATION.cff` | Licence, attribution and citation metadata. |

## Columns

| Column | Meaning |
|---|---|
| `Hakusana` | The headword / lemma, exactly as the sanalista spells it. |
| `Sanaluokat` | The word class(es) the **sanalista** assigns -- not the corpus tagger's guess. Comma-separated. May be empty for the handful of forms the sanalista lists without a class. |
| `count` | Total corpus occurrences of the lemma. |

A trailing asterisk in `Sanaluokat` marks a class carried by more than one
sense: `joka` -> `pronomini*` is two different pronouns. A multi-valued entry
like `substantiivi, adjektiivi` is one sense wearing two hats and gets no
asterisk.

Counts are **POS-merged**: a lemma's `count` is every corpus token of that
lemma regardless of how the tagger classified it, because the tagger is not
reliable enough to split them. The exception is the 43 homonyms whose senses
are genuinely different parts of speech, which were split by hand and appear as
one row per class.

## The subdictionaries overlap -- never sum counts across them

A lemma listed under several word classes -- `mukaan` is `adverbi, postpositio`
-- appears in **every** matching subdictionary carrying its **full** count. The
corpus count behind such a lemma was never split between its classes, so the
merged total is the only honest figure to report for either one. Adding the
files together double-counts 1384 multi-class lemmas.

The `Sanaluokat` column travels with every row, so you can always see whether a
given count is shared: more than one class listed means it is.

## Licence and attribution

CC BY 4.0 (see `LICENSE`). If you use this dictionary, please attribute:

> Yle Uutisten taajuussanakirja -- a news-based Finnish frequency dictionary,
> Daniel Radice, CC BY 4.0. Derived from the Yle Finnish News Archive
> 2011-2024 ((c) Yle, CC BY 4.0, via Kielipankki) and the Kotus Nykysuomen
> sanalista (CC BY).

Both upstream sources are themselves CC BY and require attribution in their own
right; `NOTICE` records exactly what is covered and who must be credited.
"""


def read_dictionary():
    """Return (header, rows) from the dictionary, or raise if it looks unusable."""
    if not DICTIONARY.exists():
        raise SystemExit(f"dictionary not found: {DICTIONARY}\nrun scripts/split_homonym_counts.py first")
    with open(DICTIONARY, encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [r for r in reader if r]
    if not rows:
        raise SystemExit(f"dictionary has no data rows: {DICTIONARY}")
    return header, rows


def release_notes(version):
    """Slice CHANGELOG.md between this version's heading and the next one."""
    text = CHANGELOG.read_text(encoding="utf-8")
    pattern = rf"^## \[{re.escape(version)}\].*?$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise SystemExit(
            f"no '## [{version}]' section in {CHANGELOG.name} -- "
            f"write the changelog entry before tagging {version}"
        )
    rest = text[match.end():]
    end = re.search(r"^## ", rest, re.MULTILINE)
    return (rest[: end.start()] if end else rest).strip() + "\n"


def write_csv(path, header, rows):
    # utf-8-sig: the BOM is what makes Excel read the umlauts correctly.
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)  # default dialect is RFC 4180
        writer.writerow(header)
        writer.writerows(rows)


def write_json(path, header, rows):
    keys = [h.lower() for h in header]
    records = [
        {keys[0]: r[0], keys[1]: r[1], keys[2]: int(r[2])} for r in rows
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=None)
        f.write("\n")


def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        writer.writerows(rows)


def stage_bundle(staging, header, rows, version):
    """Fill the archive's top-level directory."""
    staging.mkdir(parents=True)

    shutil.copy2(DICTIONARY, staging / DICTIONARY.name)
    for name in VERBATIM:
        shutil.copy2(ROOT / name, staging / name)
    shutil.copytree(SUBDICTS, staging / "subdictionaries")
    subdict_count = len(list((staging / "subdictionaries").glob("*.tsv")))

    write_csv(staging / f"{DICTIONARY.stem}.csv", header, rows)
    write_json(staging / f"{DICTIONARY.stem}.json", header, rows)
    write_tsv(staging / "taajuussanakirja_top5000.tsv", header, rows[:TOP_N])

    (staging / "README.md").write_text(
        BUNDLE_README.format(
            version=f"v{version}",
            repo=REPO_URL,
            rows=f"{len(rows):,}".replace(",", " "),
            top_n=f"{min(TOP_N, len(rows)):,}".replace(",", " "),
            subdict_count=subdict_count,
        ),
        encoding="utf-8",
    )
    return subdict_count


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_version():
    ref = os.environ.get("GITHUB_REF_NAME", "")
    return ref[1:] if ref.startswith("v") else (ref or "dev")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--version",
        default=default_version(),
        help="version to package (default: $GITHUB_REF_NAME without 'v', else 'dev')",
    )
    version = parser.parse_args().version

    header, rows = read_dictionary()
    notes = release_notes(version) if version != "dev" else "(dev build)\n"

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    name = f"{STEM}-{version}"
    subdict_count = stage_bundle(DIST / name, header, rows, version)

    archives = [
        Path(shutil.make_archive(str(DIST / name), fmt, root_dir=DIST, base_dir=name))
        for fmt in ("zip", "gztar")
    ]
    shutil.rmtree(DIST / name)

    (DIST / "SHA256SUMS.txt").write_text(
        "".join(f"{sha256(a)}  {a.name}\n" for a in archives), encoding="utf-8"
    )
    (DIST / "RELEASE_NOTES.md").write_text(notes, encoding="utf-8")

    print(f"{len(rows)} dictionary rows + {subdict_count} subdictionaries -> {name}")
    for path in sorted(DIST.iterdir()):
        print(f"{path.stat().st_size:>10,} bytes  {path.name}")


if __name__ == "__main__":
    main()
