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
