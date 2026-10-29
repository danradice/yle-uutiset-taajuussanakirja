# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Build a Finnish frequency dictionary (*taajuussanasto*) for the headwords in
`word_lists/nykysuomensanalista2024.txt` (the Kotus "nykysuomen sanalista"),
using token counts from the Yle Finnish News Archive (YLENEWS_FI) 2011–2024.

## Pipeline

Two ordered stages under `scripts/`. A manual boilerplate review comes before
them, and a manual homonym review sits between them. Stage 2 produces the
deliverable.

### Repetition removal — `vrt_sentences.py`

The archive repeats a lot of text, and almost all of the repetition is at the
level of sentences: only 12 of 1 043 653 text ids repeat. All three counting
scripts therefore read the corpus through `vrt_sentences.iter_kept_tokens()`.
It counts **each distinct sentence once**, applying these rules in order:

- **Whole texts dropped:**
  - texts from `Yle Selkouutiset` (simplified Finnish);
  - texts written by Yle's Voitto robot, recognised by its sign-off "Voitto-robotin tekemästä".
- **Sentences dropped:**
  - image alt texts (`type` `alt` or `heading-alt`);
  - serialisation copies: within one text, a sentence repeated in a *different* field. The JSON harvest emits the headline block, the lead and the caption twice.
- **Every other repeat** of a sentence, within a text or across texts, is dropped, except:
  - **protected short sentences**: at most `SHORT_MAX` = 4 tokens, body text, no `*`/`_` markup, and not on the stoplist. These recur naturally ("Päinvastoin.", "En tiedä."), so every occurrence counts;
  - **reviewed numeric templates**: a sentence whose digit-masked form is on the template list counts once *however many numbers it carries*. This covers comment-moderation footers, programme schedules and election pages. Masking is not global: few-variant formulas such as "Ottelua seurasi N katsojaa" stay exact-matched.

Sentence identity is the lowercased non-`Punct` word forms joined by spaces. The
first occurrence in (chronological) file order is the one kept. The 2.0.0
recount kept 81.9% of 296.6 M non-`Punct` tokens:

| Outcome | Share of tokens |
|---|---|
| serialisation copies | 10.4% |
| other repeats | 3.5% |
| alt texts | 3.2% |
| Selkouutiset | 0.5% |
| robot texts | 0.4% |
| templates | 0.1% |

Method relative to the Leipzig Corpora Collection (Quasthoff, Richter &
Biemann 2006), which removes duplicates and number-only near-duplicates at every
length: this method keeps genuine short repeats, masks numbers only for reviewed
templates, and uses the VRT's structure rather than form-based filters.

### Manual step — the boilerplate review (`list_boilerplate_candidates.py`)

`list_boilerplate_candidates.py` (slow) writes two candidate files to
`auxiliary_data/`:

- `boilerplate_candidates_short.tsv`: protectable sentences with at least 10 copies;
- `boilerplate_candidates_numeric.tsv`: digit-masked keys with at least 10 distinct variants.

Both keep only rows that contain a wordlist lemma.

Each row gets a rule-based `suggest`/`reason`:

| Reason | Meaning |
|---|---|
| `nav` | navigation, promotion or edit note |
| `label` | a colon, no sentence-final punctuation, or a template with fewer than 3 non-numeric words |
| `burst` | all copies within 3 years |
| `section` | at least 95% of copies outside the general news and sports sections |

The reviewer marks the rows to drop in `drop`. For 2.0.0 that was every
`nav` and `label` suggestion and none of `burst` or `section`, giving 734 short
rows and 1 040 templates. `--resuggest` recomputes the suggestions in place.
`--build-lists` then writes the two reviewed lists the counter reads:
`boilerplate_short_sentences.tsv` (the stoplist) and
`boilerplate_numeric_templates.tsv`. Both counting scripts exit if either list
is missing, so a recount cannot silently skip the review.

### Stage 1 — `count_local_vrt.py`

Scans the locally-downloaded YLENEWS VRT files and counts each lemma's
occurrences over the kept sentences, **POS ignored** (all word classes merged),
but only for lemmas
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
split back out by hand. `count_homonym_pos.py` produces the raw material. It
gives per-POS corpus counts for the 61 homonyms whose senses map to more than
one VRT pos code, with an `expected` flag marking tagger POS that the sanalista
does not list. That output is saved as
`auxiliary_data/homonym_pos_counts_2011_2024_raw.tsv` and reviewed by hand to
yield `auxiliary_data/homonym_pos_counts_2011_2024_ready.tsv`.

**Criterion:** a homonym is split only if its *genuine* minority sense is at
least the top-10 000 cutoff count (1 080 in 2.0.0). Only then does the second
sense become its own learner-list entry; below that a split only moves tagger
noise around. 2.0.0 splits 7 lemmas: `aika`, `päästä`, `koko`, `juuri`,
`kuusi`, `kohta` and `panna`.

**The review handles whole tag buckets, not word forms.** Each bucket is either:
- **folded** into another POS of the same lemma, when it is the same word mistagged; or
- **dropped** (a `pos` of `-`), when it is a different headword mis-lemmatised onto this one, or a proper name.

Dropped tokens are *not* moved to the headword they belong to. Four lemmas are
corrected this way without being split: `vasta`, `voi`, `rikki` and `vuoksi`.
The decisions, and the leakage knowingly left in, are in
`homonym_processing_notes.md`.

### Stage 2 — `split_homonym_counts.py`

Folds the reviewed per-POS counts back in: each affected lemma's single merged
row is replaced by one row per POS, carrying that POS's count. Writes the final
**tab-separated** `frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv` (same
three columns as stage 1). The ready file's VRT pos codes are mapped back to the
sanalista's Finnish class names, choosing among *that lemma's own* classes —
which resolves `Num` (numeraali vs. järjestysluku) and `Adp` (postpositio vs.
prepositio). It warns when a lemma's split counts do not sum to its merged
total, which catches arithmetic slips in the manual step. Dropped (`-`) rows
count toward that sum but are not written out. A lemma left with a single kept
row has been corrected rather than split, so it keeps its merged `Sanaluokat`
label.

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
would double-count the 1 419 multi-class lemmas. The `Sanaluokat` column is
carried over so any row shows whether its count is shared.

Rows whose `Sanaluokat` is blank (forms the sanalista lists without a word
class: `enempää`, `osin`, `vuonna`, ...) go to
`taajuussanakirja_luokittelematon.tsv`, so no dictionary row is lost.

### Stage 4 (optional) — `build_top_list.py`

Cuts the learner-facing top-10 000 head off the dictionary and writes it twice:
`taajuussanakirja_top10000.tsv` (UTF-8, LF) and `taajuussanakirja_top10000.csv`
(UTF-8 **with BOM**, CRLF). Both are committed, and they are the *only* assets a
release attaches.

The dictionary is already sorted, so this is `rows[:TOP_N]` — a head, not a
re-sort, which means the top list cannot disagree with the dictionary. Same
three columns, no `rank` (the homonym split puts some lemmas on two rows and
ties leave rank ambiguous). It prints coverage (95.15% of tokens), the distinct
lemma count (9 993 lemmas in 10 000 rows), and a warning when the positional
cutoff falls inside a run of equal counts — currently 6 rows share count 1 081
and fall outside.

Both files sit under GitHub's 512 KB limit for rendering tabular data, so they
display as tables on github.com where the 2.4 MB dictionary does not. That is
why they are committed rather than generated at release time.

### Line endings

Every TSV is written with `lineterminator="\n"`. Python's `csv.writer` defaults
to CRLF, which made shell tools fail *silently*: `grep -cP '\t1$'` returned 0
instead of 5 330, and `cut -f3` yielded a trailing `\r` that compared unequal to
the number it printed as. The **CSV is the sole exception** and keeps CRLF plus
a BOM, because RFC 4180 specifies it and Excel expects it.

### Releases

`.github/workflows/release.yml` runs on a `v*` tag. It reruns stages 2–4 and
fails on `git diff --exit-code -- frequency_dicts/`, so a release cannot ship
data that the committed intermediates do not reproduce. It then slices the
version's section out of `CHANGELOG.md` with `awk` — failing if that section is
absent, the guard against tagging a release nobody wrote notes for — and calls
`gh release create` with the two top-10 000 files. The version comes from the
tag only (`$GITHUB_REF_TYPE` must be `tag`); on `workflow_dispatch` the gates run
and publishing is skipped.

There is deliberately **no packaging step**: both assets are committed files, so
nothing is generated at release time. GitHub's automatic source archive is the
"everything" download, and it is also what Zenodo archives for the DOI, so the
archived and advertised copies match.

Asset filenames carry no version, so
`…/releases/latest/download/taajuussanakirja_top10000.csv` always resolves to
the newest release.

### Citation metadata

Two files describe a release, to two different services, and they must agree.

`CITATION.cff` is what GitHub's "Cite this repository" button renders, via the
`cff` Ruby gem. Two facts about that renderer decide the file's shape, both
learned the hard way from its source:

- It takes the citation's URL from `repository-code` in preference to `url`, and
  overrides both only when the **top-level `doi:` key** is set. `identifiers:` is
  never consulted for the DOI. So the DOI has to be that key, or the button
  prints the GitHub URL and no DOI at all.
- Its APA output prints a publisher only for `type: book`, and its BibTeX maps a
  dataset to `@misc`, which has no publisher field. **Nothing in CFF can make the
  button say "Zenodo"**, `preferred-citation` included — the rendered string
  differs from the Zenodo record's by that word and by `[Data set]` against
  `[Dataset]`, and that is formatter styling, not a metadata error. Do not try to
  fix it by declaring a different `type`: it would misdescribe the dataset and
  lose the `[Data set]` label.

`preferred-citation` is why the file restates its own title, authors, version and
year: APA prefers the DOI unaided, but the BibTeX formatter takes its `url` from
`repository-code`, and only a reference — which is what `preferred-citation`
becomes — has no `repository-code` to lose to. So that block is what puts the DOI
in *both* formats. Its `publisher: Zenodo` is accurate metadata that neither
format prints. Every value it duplicates is checked against the original by the
gate below, because a stale copy would render on the button after the next
release.

The DOI is the **concept** DOI (`10.5281/zenodo.22162057`), which resolves to the
newest version — a version DOI cannot live in the repo, because Zenodo only mints
it once the tag has been published.

To see exactly what the button will show: `gem install cff`, then
`ruby -EUTF-8 -r cff -e 'puts CFF::File.read("CITATION.cff").to_apalike'`.

`.zenodo.json` drives the Zenodo record. It exists because Zenodo's CFF reader
maps just six fields (title, authors, abstract, keywords, license, message) and
ignores `version`, `date-released`, `type`, `identifiers` and `references`;
those fall back to GitHub release defaults, so the record took its version
straight from the tag and read *Version v1.1.0*. Zenodo reads `.zenodo.json`
first and **ignores `CITATION.cff` entirely when it is present**, so everything
the record needs has to be in it. Its fields are the pre-RDM "legacy" Zenodo
shape (`upload_type`, `imprint_publisher`, …), still the supported contract.
Unknown keys are dropped silently, but a bad *value* — an unmapped licence id or
relation type — fails the release archiving, so change it carefully. Two traps
worth remembering: omitting `license` silently makes a dataset **CC0**, and
`imprint_publisher` is deliberately absent because it defaults to `Zenodo`,
which is correct (the publisher is the archive holding the fixed copy).

`scripts/check_release_metadata.py` is the gate. It fails the release when the
two files disagree on version or date, when `CITATION.cff` disagrees with itself
(a `version` restated under `preferred-citation`, a `year` that is not
`date-released`'s), when the tagged tree link in `.zenodo.json` is stale, or — on
a tag run — when either file disagrees with the tag. It reads the CFF scalars
with anchored regexes rather than a YAML parse, deliberately: PyYAML is absent
from a clean `setup-python` runner and this repo is stdlib-only everywhere else.

To cut a release: add the `## [X.Y.Z]` section to `CHANGELOG.md`, then bump the
version and date in **both** citation files — `version` and `date-released` in
`CITATION.cff`; `version`, `publication_date` and the `/tree/vX.Y.Z` link in
`.zenodo.json` — then push the tag. Versions are semver read for a dataset —
MAJOR for a different corpus span or counting method, MINOR for added data or
columns, PATCH for corrections.

### Commands

```bash
python3 scripts/list_boilerplate_candidates.py  # boilerplate candidates (slow; feeds the review)
python3 scripts/list_boilerplate_candidates.py --build-lists  # reviewed lists from the `drop` column (fast)
python3 scripts/count_local_vrt.py            # stage 1 (slow; reads all VRT files)
python3 scripts/count_homonym_pos.py          # homonym per-POS counts (slow; feeds the manual step)
python3 scripts/split_homonym_counts.py       # stage 2 — builds the final dictionary (fast)
python3 scripts/build_pos_subdictionaries.py  # stage 3 — per-word-class subdictionaries (fast)
python3 scripts/build_top_list.py             # stage 4 — top-10 000 list, TSV + CSV (fast)
python3 scripts/check_release_metadata.py     # citation metadata gate (fast)
```

Scripts can be run from any directory: all data paths are anchored to the repo
root via `ROOT = Path(__file__).resolve().parent.parent`, not the CWD.

## Data layout & formats

- `word_lists/nykysuomensanalista2024.txt` — **tab-separated**, columns
  `Hakusana` (headword/lemma), `Homonymia`, `Sanaluokka`, `Taivutustiedot`.
- `frequency_dicts/taajuussanakirja_ylenews_2011_2024.tsv` — the **deliverable**,
  tab-separated; written by stage 2.
- `frequency_dicts/subdictionaries/taajuussanakirja_<sanaluokka>.tsv` — one file
  per word class, written by stage 3, plus `taajuussanakirja_luokittelematon.tsv`
  for rows with a blank `Sanaluokat`. These overlap: see stage 3 above before
  aggregating anything across them.
- `frequency_dicts/taajuussanakirja_top10000.{tsv,csv}` — the top-10 000 head,
  written by stage 4; the only files a release attaches.
- `auxiliary_data/` — intermediates and working files, all tab-separated:
  - `lemma_counts_merged_2011_2024.tsv` — stage 1 output (POS merged).
  - `homonym_pos_counts_2011_2024_raw.tsv` — `count_homonym_pos.py` output.
  - `homonym_pos_counts_2011_2024_ready.tsv` — the manually reviewed version,
    stage 2's input.
  - `homonym_pos_examples.md` — example sentences pulled from the VRT for
    lemma/POS combinations needing review, with the conclusions drawn from them.
  - `homonym_processing_notes.md` — the resulting manual decisions: the split
    criterion, which buckets were folded into which POS, and which were dropped.
  - `boilerplate_candidates_{short,numeric}.tsv` — `list_boilerplate_candidates.py`
    output with the reviewer's `drop` marks.
  - `boilerplate_short_sentences.tsv` (the protection stoplist) and
    `boilerplate_numeric_templates.tsv` — the reviewed lists that
    `vrt_sentences.py` reads, as `key, example, copies`.
- `corpora/ylenews-fi-{2011-2018,2019-2021,2022-2024}-s-vrt/` — the three
  downloaded VRT packages. VRT lives under `vrt/` for the first two and `data/`
  for the third; `VRT_ROOTS` in `scripts/vrt_sentences.py` hard-codes these paths.

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

**Mis-lemmatisation across headwords.** The corpus lemma field sometimes names
the wrong headword, and stage 1 counts the token under that lemma. It surfaces
only where the homonym review breaks a lemma down by tag. For example, 83% of
`vasta`/N is *vastaan* and 13% is *vastassa*; `koko`/N contains *kokoon* and
*koolle*; most of `voi` is *voida*. Dropping those tokens from the homonym does
not restore them to their own headword, so the following stay undercounted
(about 1/5 of the corpus sampled; missing tokens are estimates):

| Headword | Stage 1 count | Missing tokens (est.) |
|---|---|---|
| `vastassa` | 987 | ~5 200 |
| `kokoon` | 300 | ~3 000 |
| `koolle` | 55 | ~3 000 |
| `vastaan` | 164 408 | ~33 000 |

Lemmas never broken down by tag may hide similar errors.

**Repetition in the archive.** This is why counting goes through
`vrt_sentences.py` (see "Repetition removal" above). Before 2.0.0, every token
was counted. That inflated photo and caption vocabulary
(`kuvituskuva` 55 754 → 1 961), robot sports templates (`keltainen` 37 147 → 6 869,
`vaihto` 45 802 → 16 510), navigation lines (`lukea` 253 362 → 84 082) and
moderation footers (`keskustella` 86 979 → 60 971). 183 rare lemmas attested only
in alt texts or boilerplate dropped out of the dictionary.

## Korp API

The corpora can alternatively be queried via the Korp API
(https://www.kielipankki.fi/support/korpapi/); local notes in `Korp_API.txt`.
Corpus IDs: `YLENEWS_FI_<YEAR>_S` for each year 2011–2024.
