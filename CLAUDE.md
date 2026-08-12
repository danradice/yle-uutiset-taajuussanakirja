# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Build a Finnish frequency dictionary (*taajuussanasto*) for the headwords in
`word_lists/nykysuomensanalista2024.txt` (the Kotus "nykysuomen sanalista"),
using token counts from the Yle Finnish News Archive (YLENEWS_FI) 2011–2024.

## Pipeline

Two ordered stages under `scripts/`, plus a manual disambiguation step between
them. Stage 2 produces the deliverable.

### Stage 1 — `count_local_vrt.py`

Scans the locally-downloaded YLENEWS VRT files and counts each lemma's
occurrences, **POS ignored** (all word classes merged), but only for lemmas
present in the wordlist (keeps memory bounded across the 14-year dataset). It
writes one row per attested headword (zero-count headwords are dropped), sorted
by frequency descending then headword, to the **tab-separated** intermediate
`auxiliary_data/lemma_counts_merged_2011_2024.tsv`, with columns:

- `Hakusana` — the headword/lemma.
- `Sanaluokat` — the possible word classes for the lemma, taken from the
  wordlist's `Sanaluokka` column across all of the lemma's senses, deduped and
  in first-appearance order. A class carried by **more than one sense** (the
  lemma has several meanings of that same part of speech) gets a trailing
  asterisk, e.g. `substantiivi*, adjektiivi`. A multi-valued field like
  `substantiivi, adjektiivi` is one sense with two classes, so it counts once
  per class and does not by itself trigger an asterisk. A blank `Sanaluokka`
  yields an empty `Sanaluokat` cell.
- `count` — total corpus occurrences of that lemma (POS ignored).

Deliberately, the corpus tagger's POS is **not** used to split counts here: the
sanalista already fixes each lemma's word class(es), so trusting the tagger only
fragments a lemma's counts across spurious classes (see "Known data-quality
issues").

### Manual step — disambiguating the multi-class homonyms

Merging is wrong for the homonyms whose senses are genuinely *different* parts
of speech (e.g. `panna` = verb "to put" vs. noun "a ban"), so those totals are
split back out by hand. `count_homonym_pos.py` produces the raw material —
per-POS corpus counts for the homonyms whose senses map to more than one VRT pos
code, with an `expected` flag marking tagger POS the sanalista does not list.
That output is saved as `auxiliary_data/homonym_pos_counts_2011_2024_raw.tsv` and reviewed manually (mistagged buckets folded into the correct POS,
resolved lemmas dropped) to yield
`auxiliary_data/homonym_pos_counts_2011_2024_ready.tsv`.

### Stage 2 — `split_homonym_counts.py`

Folds the reviewed per-POS counts back in: each affected lemma's single merged
row is replaced by one row per POS, carrying that POS's count. Writes the final
**tab-separated** `frequency_dicts/taajuussanasto_ylenews_2011_2024.tsv` (same
three columns as stage 1). The ready file's VRT pos codes are mapped back to the
sanalista's Finnish class names, choosing among *that lemma's own* classes —
which resolves `Num` (numeraali vs. järjestysluku) and `Adp` (postpositio vs.
prepositio). It warns when a lemma's split counts do not sum to its merged
total, which catches arithmetic slips in the manual step.

The dictionary must always be rebuilt from the stage 1 list: stage 2 is not
idempotent on its own output, since an already-split lemma has no single row to
replace.

### Stage 3 (optional) — `build_pos_subdictionaries.py`

Splits the finished dictionary into one file per word class under
`frequency_dicts/subdictionaries/`, each keeping the dictionary's three columns
and frequency-descending order.

A lemma listed under several word classes (e.g. `mukaan` = "adverbi,
postpositio") appears in **every** matching subdictionary carrying its **full**
count — the corpus count behind such a lemma was never split between its
classes, so the merged total is the only honest figure. **The subdictionaries
therefore overlap and their counts must never be summed across files**, which
would double-count the 1384 multi-class lemmas. The `Sanaluokat` column is
carried over so any row shows whether its count is shared.

Rows whose `Sanaluokat` is blank (forms the sanalista lists without a word
class: `enempää`, `osin`, `vuonna`, ...) go to
`taajuussanasto_luokittelematon.tsv`, so no dictionary row is lost.

### Commands

```bash
python3 scripts/count_local_vrt.py            # stage 1 (slow; reads all VRT files)
python3 scripts/count_homonym_pos.py          # homonym per-POS counts (slow; feeds the manual step)
python3 scripts/split_homonym_counts.py       # stage 2 — builds the final dictionary (fast)
python3 scripts/build_pos_subdictionaries.py  # stage 3 — per-word-class subdictionaries (fast)
```

Scripts can be run from any directory: all data paths are anchored to the repo
root via `ROOT = Path(__file__).resolve().parent.parent`, not the CWD.

## Data layout & formats

- `word_lists/nykysuomensanalista2024.txt` — **tab-separated**, columns
  `Hakusana` (headword/lemma), `Homonymia`, `Sanaluokka`, `Taivutustiedot`.
- `frequency_dicts/taajuussanasto_ylenews_2011_2024.tsv` — the **deliverable**,
  tab-separated; written by stage 2.
- `frequency_dicts/subdictionaries/taajuussanasto_<sanaluokka>.tsv` — one file
  per word class, written by stage 3, plus `taajuussanasto_luokittelematon.tsv`
  for rows with a blank `Sanaluokat`. These overlap: see stage 3 above before
  aggregating anything across them.
- `auxiliary_data/` — intermediates and working files, all tab-separated:
  - `lemma_counts_merged_2011_2024.tsv` — stage 1 output (POS merged).
  - `homonym_pos_counts_2011_2024_raw.tsv` — `count_homonym_pos.py` output.
  - `homonym_pos_counts_2011_2024_ready.tsv` — the manually reviewed version,
    stage 2's input.
  - `homonym_pos_examples.md` — example sentences pulled from the VRT for
    lemma/POS combinations needing review, with the conclusions drawn from them.
  - `homonym_processing_notes.md` — the resulting manual decisions: which
    buckets were redistributed into which POS, and which lemmas were removed.
- `corpora/ylenews-fi-{2011-2018,2019-2021,2022-2024}-s-vrt/` — the three
  downloaded VRT packages. VRT lives under `vrt/` for the first two and `data/`
  for the third; `VRT_ROOTS` in the scripts hard-codes these paths.

### YLENEWS VRT column order

Tab-separated, one token per line; `<...>` lines are structural markup and are
skipped. Columns: `word, ref, lemma, lemmacomp, pos, msd, dephead, deprel, lex`.
**`pos` is field index 4, `lemma` is index 2** — this differs from the S24 VRT
format; do not assume field 3 is pos. `Punct` tokens are dropped during
counting.

## Known data-quality issues

See `auxiliary_data/homonym_pos_examples.md` for the evidence and
`auxiliary_data/homonym_processing_notes.md` for the decisions it led to.
Tagger errors are why stage 1 ignores POS: mistagging as
`Foreign` splits a lemma across spurious pos categories (e.g. `ry` picks up 5),
and some words appear only under a wrong pos. Merging all pos under one lemma
total sidesteps this; the `Sanaluokat` column preserves the sanalista's own
word-class information instead of relying on the corpus tagger.

The manual disambiguation step exists because the tagger cannot be trusted even
for the multi-class homonyms. Example sentences pulled for review showed whole
buckets to be artefacts: `kuti`/A was the verb *kutista* mis-lemmatised, `kuti`/Adv
was the noun (sports slang "shot") mistagged, and `läpi`/N, `lähin`/Adv and
`kiltti`/N contained none of the noun/adverb senses their tags claimed. An
`expected=yes` flag therefore does **not** vindicate a bucket — the sanalista
listing a noun sense does not mean the tagged tokens are that noun.

## Korp API

The corpora can alternatively be queried via the Korp API
(https://www.kielipankki.fi/support/korpapi/); local notes in `Korp_API.txt`.
Corpus IDs: `YLENEWS_FI_<YEAR>_S` for each year 2011–2024.
