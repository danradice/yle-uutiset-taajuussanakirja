# Homonym processing decisions (2.0.0)

These decisions turn `homonym_pos_counts_2011_2024_raw.tsv` into
`homonym_pos_counts_2011_2024_ready.tsv`. They replace the v1.x decisions, which
split 43 lemmas. Some of those were wrong: for example, `päästä`/N was folded
into Adp, but it is the verbal noun *pääseminen*.

The evidence is in `homonym_pos_examples.md`, section "2.0.0 review".

## Criterion

A homonym is split only if its **genuine minority sense is at least the
top-10 000 cutoff count** (1 080 in the 2.0.0 recount). "Genuine" means after
the spurious tag buckets are resolved. The split matters only when the second
sense becomes its own entry in the learner list. Below the cutoff, the split
just moves tagger noise between rows past rank 10 000. Every other multi-class
lemma keeps its merged stage 1 row.

The decisions work on whole tag buckets only, not word forms. A bucket is:
- **folded** into another POS of the same lemma when it is the same word, mistagged;
- **dropped** (`pos` = `-` in the ready file) when it is a different headword
  mis-lemmatised onto this one, or a proper name.

Dropped tokens are **not** moved to the headword they belong to. Leakage that
whole tag buckets cannot separate is accepted and noted below.

## Split (7 lemmas)

| Lemma | Kept rows | Folded | Dropped | Leakage accepted |
|---|---|---|---|---|
| aika | N, Adv | | A (0 tokens) | ~3/10 Adv are the noun (*aika ajoin*, *on aika siirtyä*); some N "aika" is the adverb |
| päästä | V, Adp | N → V (*pääseminen*) | Adv (imperative of *päästää*, song title *Päästä varpaisiin*), Foreign | ~2/10 Adp are the noun *pää* or a negative passive verb |
| koko | A, N | Pron → A ("whole"), Adv → N (*kokokin*) | Foreign | ~30% of N is *kokoon*/*koolle* (other headwords) |
| juuri | Adv, N | | A (surname *Juurinen*), Foreign | |
| kuusi | Num, N | A → Num | | many N nominatives "kuusi" are the number, so spruce is ~6–8 k |
| kohta | N, Adv | A → Adv | | some N "kohta" is the adverb (*kohta vuoden päivät*) |
| panna | V, N | A → N (*pannaton*), Adv → V | | ~8% of N is *paneminen* (the verb) |

## Corrected, not split (one kept row, merged Sanaluokat label kept)

| Lemma | Dropped | Why |
|---|---|---|
| vasta | N (39 528) | 83% *vastaan*, 13% *vastassa*, 1% *vastoin*; the noun "bath whisk" is <1% |
| voi | Adv, A, V (1 601) | *voikin*/*voihan*/*voiko* = *voida*; *voiton* = *voitto*. N and Interj are folded together and still mostly *voida* (10/10 N, ~7/10 Interj samples) |
| rikki | A (142) | surname *Rikkinen*. N (sulphur, ~600–800 genuine) is folded into Adv: below the cutoff |
| vuoksi | N (636) | the river Vuoksi; *teidän vuoksenne* is the postposition. A (1) folded into Adp |

## Not split, merged row unchanged

- **The minority sense is not a separate word, or is below the cutoff once cleaned:**
  - iso: N is substantivised adjectives and *Iso Omena*; Adv is *isommin*.
  - riski: A is 9/10 the noun; "strong" is about 300.
  - kymmenes: N is mostly *joka kymmenes* (the ordinal); "a tenth" is about 150.
  - taata: N is *takaaminen* (the verb); "dad" is about 2. V also holds about 740 *takaisin*.
  - live, läpi, viisi, lento, vika, kiltti, lähin, pro, aina, perin, kiire, suoja, jonne.
- **Every lemma with a total below 2 × 1 080 cannot qualify:** raaka and below.

## Known effect on other headwords (not corrected)

These tokens are counted under the wrong lemma in stage 1, and dropping them
from the homonym does not restore them to the headword they belong to.
Estimated missing counts:

| Headword | Missing tokens | Its stage 1 count |
|---|---|---|
| vastassa | ~5 200 | 987 |
| kokoon | ~3 000 | 300 |
| koolle | ~3 000 | 55 |
| vastaan | ~33 000 | 164 408 |
| vastoin | ~400 | 1 084 |

Lemmas never broken down by tag may contain similar errors that have not been
seen.
