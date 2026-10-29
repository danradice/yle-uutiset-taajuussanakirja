"""List repeated sentences that need a manual keep/drop decision before counting.

vrt_sentences.iter_kept_tokens() counts each distinct sentence once, but two
kinds of repetition cannot be settled automatically, and this script lists the
candidates for both (wordlist lemmas only: a sentence of bare numbers or names
cannot change any count):

  boilerplate_candidates_short.tsv
      Short plain body sentences (the shape the counter protects, so every
      occurrence is counted) with at least MIN_COPIES occurrences. Most are
      genuine ("Päinvastoin.", "En tiedä."), some are boilerplate the shape
      test misses ("Kuvaan liittyvä linkki"). Approved rows go to
      auxiliary_data/boilerplate_short_sentences.tsv.

  boilerplate_candidates_numeric.tsv
      Sentence templates that differ only in their numbers, with at least
      MIN_VARIANTS distinct variants. Many-variant templates are boilerplate
      ("Voit keskustella aiheesta 22.1. kello 22:een saakka"); the threshold
      keeps out independent sentences that happen to share a formula ("Ottelua
      seurasi N katsojaa"). Approved rows go to
      auxiliary_data/boilerplate_numeric_templates.tsv.

Excluded publishers, alt texts, robot texts and within-text serialisation
copies are excluded first,
exactly as the counter does. Columns are described in CLAUDE.md; `nav` flags a
navigation or promotion word (lue, katso, tästä, Areena, ...).

Each row also gets a rule-based `suggest` (drop/keep) and the `reason` for it,
from suggest() below, to make the review fast; `drop` is left blank for the
reviewer's decision. Run with --resuggest to recompute the suggestions in the
existing candidate files without rereading the corpus.

After the review (a non-blank `drop` marks a row as boilerplate), run with
--build-lists to write the two reviewed lists the counter reads.
"""

import csv
import re
import sys
from collections import Counter

from vrt_sentences import (ROOT, is_excluded_publisher, is_robot, iter_texts,
                           masked, vrt_files)

WORDLIST = ROOT / "word_lists/nykysuomensanalista2024.txt"
OUT_SHORT = ROOT / "auxiliary_data/boilerplate_candidates_short.tsv"
OUT_NUMERIC = ROOT / "auxiliary_data/boilerplate_candidates_numeric.tsv"
LIST_SHORT = ROOT / "auxiliary_data/boilerplate_short_sentences.tsv"
LIST_NUMERIC = ROOT / "auxiliary_data/boilerplate_numeric_templates.tsv"
MIN_COPIES = 10
MIN_VARIANTS = 10

NAV = re.compile(
    r"\b(lue|lukea|katso|katsele|kuuntele|seuraa|lataa|tilaa|vastaa|klikkaa|"
    r"äänestä|keskustele|keskustella|luitko|lähde|lähteet|täältä|tästä|tänne|"
    r"areena\w*|uutisvahti\w*|yle\w*)\b"
)
# Edit and moderation notes: "Päivitetty klo 13.35.", "Keskustelu sulkeutuu ..."
EDIT_NOTE = re.compile(
    r"\b(päivit\w*|korjat\w*|korjaus|muokat\w*|täydennet\w*|kommento\w*|keskustelu\w*)\b"
)
SENTENCE_END = re.compile(r"[.!?…][\"”’»)_*\s]*$")
GENERAL_PUBLISHERS = {"Yle Uutiset", "Yle Urheilu"}


class Info:
    """Where a candidate's copies occur: years, publishers and examples.

    Tracking starts at the copy that makes it a candidate (the second), so the
    year span and publisher share describe the repeats, not the first copy.
    """
    __slots__ = ("copies", "years", "publishers", "examples")

    def __init__(self):
        self.copies = 0
        self.years = set()
        self.publishers = Counter()
        self.examples = []

    def add(self, attrs, raw, keep_examples=1):
        self.copies += 1
        self.years.add(attrs.get("datefrom", "")[:4])
        self.publishers[attrs.get("publisher", "")] += 1
        if len(self.examples) < keep_examples:
            self.examples.append(raw)

    def columns(self):
        years = sorted(y for y in self.years if y)
        publisher, n = self.publishers.most_common(1)[0]
        span = f"{years[0]}-{years[-1]}" if years else ""
        return [span, len(years), publisher, f"{n / self.copies:.2f}"]


def suggest(key, example, n_years, top_publisher, top_share, numeric):
    """Rule-based (suggestion, reason) for a candidate row.

    Boilerplate signals: a navigation or edit note; a label (a colon, or no
    sentence-final punctuation); a burst (all copies within three years); one
    specialised section (>= 95% of copies outside the general news and sports
    sections); for templates, fewer than three words besides the numbers (date
    and time headers, vote tallies). Anything else looks like a sentence that
    recurs because it is written that way, and is suggested for keeping.
    """
    if NAV.search(key) or EDIT_NOTE.search(key):
        return "drop", "nav"
    if ":" in example or not SENTENCE_END.search(example):
        return "drop", "label"
    if numeric and sum(1 for w in key.split() if not re.fullmatch(r"[\d.,:/-]+", w)) < 3:
        return "drop", "label"
    if int(n_years) <= 3:
        return "drop", "burst"
    if float(top_share) >= 0.95 and top_publisher not in GENERAL_PUBLISHERS:
        return "drop", "section"
    return "keep", ""


def resuggest():
    """Recompute suggest/reason in the existing candidate files."""
    for path, numeric in ((OUT_SHORT, False), (OUT_NUMERIC, True)):
        with open(path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        for r in rows:
            example = r["example_1"] if numeric else r["example"]
            r["suggest"], r["reason"] = suggest(
                r["key"], example, r["n_years"], r["top_publisher"],
                r["top_share"], numeric)
        fields = [c for c in rows[0] if c not in ("suggest", "reason", "drop")]
        fields += ["suggest", "reason", "drop"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fields, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"Updated suggestions in {path}")


def build_lists():
    """Write the reviewed lists from the candidate rows marked in `drop`."""
    for src, dst, example in ((OUT_SHORT, LIST_SHORT, "example"),
                              (OUT_NUMERIC, LIST_NUMERIC, "example_1")):
        with open(src, encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f, delimiter="\t")
                    if r["drop"].strip()]
        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["key", "example", "copies"])
            w.writerows([r["key"], r[example], r["copies"]] for r in rows)
        print(f"Wrote {len(rows)} reviewed rows to {dst}")


def load_wordlist_lemmas():
    with open(WORDLIST, encoding="utf-8") as f:
        return {row["Hakusana"] for row in csv.DictReader(f, delimiter="\t")}


def main():
    lemmas = load_wordlist_lemmas()
    seen = set()           # hash of every exact key met
    short_count = Counter()  # key hash -> protectable occurrences
    short = {}             # key -> Info, once a protectable key recurs
    variants = Counter()   # masked-key hash -> distinct exact variants
    masked_copies = Counter()  # masked-key hash -> occurrences of any variant
    numeric = {}           # masked key -> Info, once a template has 2 variants
    first_variant = {}     # masked-key hash -> raw of its first variant

    for attrs, sents in iter_texts(vrt_files()):
        if is_excluded_publisher(attrs) or is_robot(sents):
            continue
        here = {}
        for s in sents:
            if s.is_alt:
                continue
            key = s.key
            k = hash(key)
            if here.setdefault(k, s.field) != s.field:
                continue          # serialisation copy
            raw = " ".join(s.raw)
            new = k not in seen
            seen.add(k)

            if s.protectable:
                short_count[k] += 1
                if key in short:
                    short[key].add(attrs, raw)
                elif short_count[k] == 2 and any(l in lemmas for l, _ in s.tokens):
                    short[key] = Info()
                    short[key].add(attrs, raw)

            m = masked(key)
            if m == key:
                continue
            mk = hash(m)
            masked_copies[mk] += 1
            if new:
                variants[mk] += 1
            if m in numeric:
                info = numeric[m]
                info.add(attrs, raw, keep_examples=2 if new else 0)
            elif variants[mk] == 1 and new:
                first_variant[mk] = raw
            elif variants[mk] == 2 and new and any(l in lemmas for l, _ in s.tokens):
                info = numeric[m] = Info()
                info.examples.append(first_variant.pop(mk, ""))
                info.add(attrs, raw, keep_examples=2)

    rows = sorted(
        ([key, info.examples[0], short_count[hash(key)]] + info.columns()
         + ["x" if NAV.search(key) else "", ""]
         for key, info in short.items() if short_count[hash(key)] >= MIN_COPIES),
        key=lambda r: (-r[2], r[0]),
    )
    with open(OUT_SHORT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["key", "example", "copies", "years", "n_years",
                    "top_publisher", "top_share", "nav", "drop"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} short-sentence candidates to {OUT_SHORT}")

    rows = sorted(
        ([m, *(info.examples + ["", ""])[:2], variants[hash(m)],
          masked_copies[hash(m)]]
         + info.columns() + ["x" if NAV.search(m) else "", ""]
         for m, info in numeric.items() if variants[hash(m)] >= MIN_VARIANTS),
        key=lambda r: (-r[3], r[0]),
    )
    with open(OUT_NUMERIC, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["key", "example_1", "example_2", "variants", "copies",
                    "years", "n_years", "top_publisher", "top_share", "nav",
                    "drop"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} numeric-template candidates to {OUT_NUMERIC}")
    resuggest()


if __name__ == "__main__":
    if "--resuggest" in sys.argv[1:]:
        resuggest()
    elif "--build-lists" in sys.argv[1:]:
        build_lists()
    else:
        main()
