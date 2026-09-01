# Yle Uutisten taajuussanakirja — a news-based Finnish frequency dictionary

[![Latest release](https://img.shields.io/github/v/release/danradice/yle-uutiset-taajuussanakirja)](https://github.com/danradice/yle-uutiset-taajuussanakirja/releases/latest)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22162057.svg)](https://doi.org/10.5281/zenodo.22162057)

Corpus frequencies for the headwords of the Kotus *nykysuomen sanalista*,
counted against the **Yle Finnish News Archive (YLENEWS_FI) 2011–2024**.

The deliverable is
[`frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv`](frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv):
**87 870 attested headwords**, tab-separated, sorted by frequency descending
then headword. Headwords with zero corpus occurrences are dropped (the sanalista
lists 104 742 in total).

```
Hakusana	Sanaluokat	count
olla	verbi	15149528
ja	konjunktio, adverbi	8009977
se	pronomini	3740116
ei	kieltoverbi, substantiivi	3312474
että	konjunktio	2616520
```

## Download

**Most people want the top 10 000.** It covers **94.95%** of everything in the
corpus, renders as a browsable table right here on GitHub, and needs no
unzipping:

| | Direct link | For |
|---|---|---|
| [`taajuussanakirja_top10000.tsv`](frequency_dicts/taajuussanakirja_top10000.tsv) | [latest release](https://github.com/danradice/yle-uutiset-taajuussanakirja/releases/latest/download/taajuussanakirja_top10000.tsv) | Scripts, text tools |
| [`taajuussanakirja_top10000.csv`](frequency_dicts/taajuussanakirja_top10000.csv) | [latest release](https://github.com/danradice/yle-uutiset-taajuussanakirja/releases/latest/download/taajuussanakirja_top10000.csv) | Excel, Google Sheets, Anki |

Those release links always resolve to the newest version, so they are safe to
put on a course page and forget.

Two things to know about the list. The cutoff is **positional**: rank 10 000 has
count 1 361 and three further rows share that count, so they fall outside the
list despite being no less frequent. And it is 10 000 *rows*, which is 9 986
distinct lemmas — 14 words appear twice because the homonym split gives them one
row per word class.

**For everything else**, take the *Source code* archive from the
[latest release](https://github.com/danradice/yle-uutiset-taajuussanakirja/releases/latest),
or just clone. It holds the full 87 870-row dictionary, all 15 subdictionaries,
the build scripts and the intermediate counts — 2.4 MB compressed.

### File formats

Every `.tsv` here is UTF-8 with **LF** line endings and needs no quoting: no
field contains a tab, so splitting on `\t` is always correct. The `.csv` is the
single exception — UTF-8 **with a BOM** and **CRLF** endings, as RFC 4180
specifies and Excel expects, with the 1 384 comma-bearing `Sanaluokat` values
quoted. If you are scripting, prefer the TSV.

### Columns

| Column | Meaning |
|---|---|
| `Hakusana` | The headword / lemma, exactly as the sanalista spells it. |
| `Sanaluokat` | The word class(es) the **sanalista** assigns to the lemma — not the corpus tagger's guess. Comma-separated, deduped, in first-appearance order. May be empty for the handful of forms the sanalista lists without a class. |
| `count` | Total corpus occurrences of the lemma. |

**The asterisk in `Sanaluokat`** marks a class carried by *more than one sense* —
the lemma has several distinct meanings of that same part of speech. `joka`
→ `pronomini*` is two different pronouns. A multi-valued entry like
`substantiivi, adjektiivi` is one sense wearing two hats and gets no asterisk.

**Counts are POS-merged by default.** A lemma's `count` is every corpus token of
that lemma regardless of how the tagger classified it — see
[Why POS is ignored](#why-pos-is-ignored). The exception is the 43 homonyms whose
senses are genuinely different parts of speech, which were split by hand and
appear as one row per class:

```
panna	verbi	22175
panna	substantiivi	2028
```

## Word-class subdictionaries

[`frequency_dicts/subdictionaries/`](frequency_dicts/subdictionaries/) holds the
same data split into one file per word class, same three columns, same ordering.

| File | Rows | | File | Rows |
|---|---:|---|---|---:|
| `taajuussanakirja_substantiivi.tsv` | 65 415 | | `taajuussanakirja_pronomini.tsv` | 62 |
| `taajuussanakirja_adjektiivi.tsv` | 9 526 | | `taajuussanakirja_prepositio.tsv` | 53 |
| `taajuussanakirja_verbi.tsv` | 9 169 | | `taajuussanakirja_konjunktio.tsv` | 34 |
| `taajuussanakirja_adverbi.tsv` | 4 413 | | `taajuussanakirja_luokittelematon.tsv` | 15 |
| `taajuussanakirja_postpositio.tsv` | 293 | | `taajuussanakirja_kieltoverbi.tsv` | 12 |
| `taajuussanakirja_interjektio.tsv` | 168 | | `taajuussanakirja_alistuskonjunktio.tsv` | 6 |
| `taajuussanakirja_numeraali.tsv` | 131 | | `taajuussanakirja_rinnastuskonjunktio.tsv` | 2 |
| | | | `taajuussanakirja_jarjestysluku.tsv` | 1 |

> [!WARNING]
> **These files overlap. Never sum counts across them.**
>
> A lemma listed under several word classes — `mukaan` is `adverbi,
> postpositio` — appears in **every** matching subdictionary carrying its
> **full** count. The corpus count behind such a lemma was never split between
> its classes, so the merged total is the only honest figure to report for
> either one. Adding the files together double-counts 1 384 multi-class lemmas.
>
> The `Sanaluokat` column travels with every row, so you can always see whether
> a given count is shared: more than one class listed means it is.

Rows whose `Sanaluokat` is blank (`enempää`, `osin`, `vuonna`, …) land in
`taajuussanakirja_luokittelematon.tsv`, so no dictionary row is lost.

## Rebuilding

### Stages 2–4 run from what is in this repo

The intermediate counts are committed, so you can regenerate the dictionary and
the subdictionaries without downloading anything:

```bash
python3 scripts/split_homonym_counts.py       # stage 2 — builds the dictionary
python3 scripts/build_pos_subdictionaries.py  # stage 3 — subdictionaries
python3 scripts/build_top_list.py             # stage 4 — the top-10 000 list
```

Python 3 standard library only; no dependencies. Scripts can be run from any
directory — paths are anchored to the repo root, not the CWD.

> [!IMPORTANT]
> Stage 2 is **not idempotent on its own output**. It always rebuilds from
> `auxiliary_data/lemma_counts_merged_2011_2024.tsv`, because an already-split
> lemma no longer has the single merged row it needs to replace.

### Stage 1 needs the corpora

Recounting from scratch requires the three VRT packages (~27 GB), which are
**not** in this repo. Download them from Kielipankki and unpack into `corpora/`:

| Package | PID |
|---|---|
| `ylenews-fi-2011-2018-s-vrt` | http://urn.fi/urn:nbn:fi:lb-2020021107 |
| `ylenews-fi-2019-2021-s-vrt` | http://urn.fi/urn:nbn:fi:lb-2022082503 |
| `ylenews-fi-2022-2024-s-vrt` | http://urn.fi/urn:nbn:fi:lb-2025110405 |

`VRT_ROOTS` in [`scripts/count_local_vrt.py`](scripts/count_local_vrt.py)
expects the VRT under `vrt/` for the first two packages and `data/` for the
third — the layout the downloads already ship with:

```
corpora/
├── ylenews-fi-2011-2018-s-vrt/vrt/
├── ylenews-fi-2019-2021-s-vrt/vrt/
└── ylenews-fi-2022-2024-s-vrt/data/
```

Then:

```bash
python3 scripts/count_local_vrt.py    # stage 1 — slow, reads every VRT file
python3 scripts/count_homonym_pos.py  # per-POS counts for the manual step
```

Between stage 1 and stage 2 sits a **manual disambiguation step**:
`count_homonym_pos.py` writes per-POS counts for the multi-class homonyms to
`auxiliary_data/homonym_pos_counts_2011_2024_raw.tsv`, which is reviewed by hand
— mistagged buckets folded into the correct class, bogus lemmas dropped — to
produce the `_ready.tsv` that stage 2 consumes. Both files are committed, so
this step does not need repeating.

The corpora can alternatively be queried through the
[Korp API](https://www.kielipankki.fi/support/korpapi/) (corpus IDs
`YLENEWS_FI_<YEAR>_S`); working notes in [`Korp_API.txt`](Korp_API.txt).

## Known data-quality issues

### Why POS is ignored

The corpus tagger is not reliable enough to split a lemma's counts by word
class. Mistagging as `Foreign` alone scatters a lemma across spurious
categories — `ry` picks up five — and some words surface *only* under a wrong
POS. Merging every POS into one lemma total sidesteps the problem entirely, and
the `Sanaluokat` column preserves the sanalista's own word-class information
instead of relying on the tagger.

### Why the homonym split was done by hand

The same distrust applies to the genuinely multi-class homonyms, so those were
reviewed individually against example sentences pulled from the corpus. Whole
buckets turned out to be artefacts: `kuti`/A was the verb *kutista*
mis-lemmatised, `kuti`/Adv was the noun (sports slang for "shot") mistagged, and
`läpi`/N, `lähin`/Adv and `kiltti`/N contained none of the noun/adverb senses
their tags claimed.

The evidence is in
[`auxiliary_data/homonym_pos_examples.md`](auxiliary_data/homonym_pos_examples.md)
and the resulting decisions in
[`auxiliary_data/homonym_processing_notes.md`](auxiliary_data/homonym_processing_notes.md).

## Releases and versioning

Pushing a `vX.Y.Z` tag runs
[`.github/workflows/release.yml`](.github/workflows/release.yml), which rebuilds
stages 2–4 from the committed intermediates, fails if anything under
`frequency_dicts/` differs from what is committed, and then publishes the
release with that version's `CHANGELOG.md` section as its notes. The only
attached assets are the two top-10 000 files; GitHub's automatic source archive
carries everything else.

Versions are semantic, read for a dataset:

| Bump | Means |
|---|---|
| **MAJOR** | A different corpus span, or a change to how counts are produced. |
| **MINOR** | Added data: more headwords, an extra column, further subdictionaries. |
| **PATCH** | Corrections that leave method and coverage intact. |

To cut a release: add the section to [`CHANGELOG.md`](CHANGELOG.md), then bump
the version and date in **both** citation files — `version` and `date-released`
in [`CITATION.cff`](CITATION.cff), `version`, `publication_date` and the tagged
tree link in [`.zenodo.json`](.zenodo.json) — and tag.
[`scripts/check_release_metadata.py`](scripts/check_release_metadata.py) fails
the release if those disagree with each other or with the tag. Running the
workflow via **workflow_dispatch** first exercises every gate without spending a
tag.

## How to cite

> Radice, D. (2026). *Yle Uutisten taajuussanakirja — a news-based Finnish
> frequency dictionary* (Version 1.1.1) [Data set]. Zenodo.
> <https://doi.org/10.5281/zenodo.22162057>

That is the **concept DOI**, which always resolves to the newest version. Every
release also has its own version DOI, shown on the Zenodo record page — cite
that one if you need to pin the exact data behind a published result.

GitHub's "Cite this repository" button offers the same citation in APA and
BibTeX, from [`CITATION.cff`](CITATION.cff) — same authors, year, version and
DOI. The two sites style it differently and neither can be talked out of it:
GitHub writes `[Data set]` and names no publisher, Zenodo writes `[Dataset]` and
names itself.

## License

[CC BY 4.0](LICENSE). The attribution notice for this work — the credit line the
licence asks you to carry, which is a different thing from the citation above:

> Yle Uutisten taajuussanakirja — a news-based Finnish frequency dictionary,
> Daniel Radice, CC BY 4.0. Derived from the Yle Finnish News Archive
> 2011–2024 (© Yle, CC BY 4.0, via Kielipankki) and the Kotus Nykysuomen
> sanalista (© Kotus, CC BY 4.0).

Both upstream sources are themselves CC BY 4.0 and require attribution in their
own right. The citation button shows only this work and never the sources it
derives from, which is why they are spelled out here. [NOTICE](NOTICE) records
exactly what is covered and who must be credited; [LICENSE](LICENSE) is the full
CC BY 4.0 text.
