# Yle Uutisten taajuussanakirja — a news-based Finnish frequency dictionary

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

### Stage 2 and 3 run from what is in this repo

The intermediate counts are committed, so you can regenerate the dictionary and
the subdictionaries without downloading anything:

```bash
python3 scripts/split_homonym_counts.py       # stage 2 — builds the dictionary
python3 scripts/build_pos_subdictionaries.py  # stage 3 — subdictionaries
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

## License

[CC BY 4.0](LICENSE). If you use a frequency dictionary from this repo, please
attribute:

> Yle Uutisten taajuussanakirja — a news-based Finnish frequency dictionary,
> Daniel Radice, CC BY 4.0. Derived from the Yle Finnish News Archive
> 2011–2024 (© Yle, CC BY 4.0, via Kielipankki) and the Kotus Nykysuomen
> sanalista (CC BY).

Both upstream sources are themselves CC BY and require attribution in their own
right. [NOTICE](NOTICE) records exactly what is covered and who must be credited;
[LICENSE](LICENSE) is the full CC BY 4.0 text.
