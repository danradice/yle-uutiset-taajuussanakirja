# Changelog

All notable changes to this dataset are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[semantic versioning](https://semver.org/) with a dataset reading of the three
numbers:

| Bump | Means |
|---|---|
| **MAJOR** | A different corpus span, or a change to how counts are produced (counting, merging, or homonym-splitting method). |
| **MINOR** | Added data: more headwords, an extra column, further subdictionaries. |
| **PATCH** | Corrections that leave method and coverage intact. |

Each released version is tagged `vX.Y.Z`, and the section below the matching
heading is what ships as the GitHub release notes.

## [1.1.1] - 2026-08-31

Citation metadata only. **No dictionary data changed** — every file under
`frequency_dicts/` is byte-identical to 1.1.0.

### Added

- `.zenodo.json`, which now drives the Zenodo record. Zenodo's CITATION.cff
  reader maps only title, authors, abstract, keywords, licence and message, so
  `version` fell through to the git tag and the record read *Version v1.1.0*
  under the wrong resource type. `.zenodo.json` takes precedence over
  CITATION.cff and pins the version, publication date, `dataset` type, language,
  ORCID and links to both upstream corpora.
- `scripts/check_release_metadata.py`, run by the release workflow: it fails the
  release when `CITATION.cff` and `.zenodo.json` disagree with each other, with
  the tag, or — since the citation restates its own version and year — with
  themselves. Any of those is otherwise invisible until the DOI is already
  minted.
- A **How to cite** section and a DOI badge in `README.md`, both pointing at the
  concept DOI `10.5281/zenodo.22162057`, which always resolves to the newest
  version.

### Changed

- `CITATION.cff` gains that concept DOI as its top-level `doi`, plus an ORCID and
  an affiliation, so the "Cite this repository" button prints the DOI instead of
  the repository URL. Its renderer reads `doi` and never `identifiers`, and
  otherwise falls back to `repository-code`; the DOI is restated under
  `preferred-citation` so that it is the link in the BibTeX output too, not only
  in APA. The button's string still differs from Zenodo's in styling — it writes
  `[Data set]` and prints no publisher for a dataset, which no CFF field can
  change.
- The attribution notice in `README.md` and `NOTICE` is labelled as the licence
  notice it is, rather than as "a suitable citation", and the Kotus *nykysuomen
  sanalista* is recorded as CC BY 4.0 rather than an unversioned CC BY.

## [1.1.0] - 2026-08-30

Adds a learner-facing top-10 000 list and fixes the line endings on every TSV.

### Added

- `frequency_dicts/taajuussanakirja_top10000.tsv` and
  `taajuussanakirja_top10000.csv` — the 10 000 most frequent rows, which cover
  **94.95%** of all corpus tokens. Both are committed and are the only files a
  release attaches; the full dictionary and the subdictionaries travel in
  GitHub's automatic source archive.
- The CSV is UTF-8 **with a BOM** and RFC 4180 CRLF line endings, so Excel opens
  it with `ä`/`ö` intact. It is the only file here that is not LF.

### Changed

- **All TSV files now use LF line endings**, not CRLF. The old CRLF made shell
  tools fail silently rather than loudly: `grep -cP '\t1$'` returned 0 instead of
  the 5 330 words occurring exactly once, and `cut -f3` returned values with a
  trailing carriage return that compared unequal to the number they printed as.
  Only the line endings changed — every value in every file is identical to
  1.0.0.

### Removed

- `taajuussanakirja_top5000.tsv`, which shipped inside the 1.0.0 archives. The
  top-10 000 replaces it: 5 000 rows covered 90.09% of tokens against 94.95%.
- The `.zip`/`.tar.gz` release bundles and `SHA256SUMS.txt`. The bundle was
  larger than GitHub's own source archive while containing less, and Zenodo
  archives the source archive rather than uploaded assets — so the DOI'd copy
  now matches what the release page advertises. Zenodo publishes an MD5 per file,
  which covers what the checksums were for.

### Notes on the top-10 000

- The cutoff is **positional**. Rank 10 000 has count 1 361, and three further
  rows share that exact count, so they fall outside the list despite being no
  less frequent than the last word kept.
- It is 10 000 **rows**, which is 9 986 distinct lemmas: 14 words (`aika`,
  `päästä`, `koko`, `juuri`, `vasta`, `kuusi` and others) appear twice because
  the homonym split gives them one row per word class.

## [1.0.0] - 2026-08-29

First release of the dictionary.

### Added

- `frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv` — **87 870 attested
  headwords** with their sanalista word class(es) and total corpus occurrences,
  tab-separated, sorted by frequency descending then headword. The Kotus
  *nykysuomen sanalista* lists 104 742 headwords in total; those with zero
  occurrences in the corpus are dropped.
- `frequency_dicts/subdictionaries/` — the same data split into **15 files**,
  one per word class plus `taajuussanakirja_luokittelematon.tsv` for the rows
  the sanalista lists without a class. These files deliberately overlap: 1 384
  multi-class lemmas appear in every matching file carrying their full count,
  so counts must never be summed across them.
- `auxiliary_data/` — the POS-merged intermediate counts and the raw and
  reviewed homonym tables, so stages 2 and 3 can be rerun without the corpora.
- `scripts/` — the four pipeline scripts, Python 3 standard library only.

### Method

- Counts are sourced from the **Yle Finnish News Archive (YLENEWS_FI)
  2011–2024**, all three VRT packages, `Punct` tokens excluded.
- **Counts are POS-merged.** The corpus tagger is not reliable enough to split a
  lemma's counts by word class, so every token of a lemma is counted together
  and the `Sanaluokat` column carries the sanalista's own classification
  instead.
- **43 homonyms** whose senses are genuinely different parts of speech (`panna`
  = verb "to put" vs. noun "a ban") were disambiguated **by hand** against
  example sentences pulled from the corpus, and appear as one row per class.
