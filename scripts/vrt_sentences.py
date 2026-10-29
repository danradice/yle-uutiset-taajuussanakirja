"""Read the YLENEWS VRT files sentence by sentence, with repetition removed.

Shared by count_local_vrt.py, count_homonym_pos.py and
list_boilerplate_candidates.py, so that every count is taken over the same
sentences.

The archive repeats a lot of text, almost all of it at sentence level (repeated
whole articles are negligible: 12 of 1 043 653 text ids). iter_kept_tokens()
counts each distinct sentence once, with these rules:

  excluded publisher
             Texts from EXCLUDED_PUBLISHERS are dropped whole. Yle Selkouutiset
             is news rewritten in simplified Finnish (selkokieli), a deliberately
             restricted register that would skew a general frequency list.
  alt        Image alt texts (sentence type "alt" or "heading-alt") are dropped:
             they are accessibility metadata, often keyword strings or bare
             names, not running text.
  robot      Texts written by Yle's Voitto robot (sports round-ups, 2016-2024)
             are dropped whole. They are recognised by the robot's own sign-off,
             so articles that only mention Voitto are kept.
  serialisation
             Within a text, a sentence repeated in a *different* field is
             dropped. The JSON harvest emits the headline block, the lead and
             the main image caption twice (lead as "text/lead" and again as
             "text/text", and so on).
  template   A sentence whose digit-masked form is on the reviewed list
             NUMERIC_TEMPLATES counts once however many numbers it carries
             ("Voit keskustella aiheesta 22.1. kello 22:een saakka").
  repeat     Any other exact repeat, within a text or across texts, is dropped,
             unless it is protected: a short (<= SHORT_MAX tokens) body-text
             sentence with no markdown emphasis that is not on the reviewed
             SHORT_STOPLIST. Short sentences recur naturally ("Päinvastoin.",
             "En tiedä.", "Kukaan ei loukkaantunut."), so every occurrence of
             those is kept.

Sentence identity ignores case and punctuation: the key is the sentence's
non-Punct word forms, lowercased and joined by single spaces. The first
occurrence in file order (chronological) is the one kept.

YLENEWS VRT columns: word, ref, lemma, lemmacomp, pos, msd, dephead, deprel,
lex - lemma is field index 2, pos is index 4. Punct tokens are never counted.
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VRT_ROOTS = [
    ROOT / "corpora/ylenews-fi-2011-2018-s-vrt/vrt",
    ROOT / "corpora/ylenews-fi-2019-2021-s-vrt/vrt",
    ROOT / "corpora/ylenews-fi-2022-2024-s-vrt/data",
]
SHORT_STOPLIST = ROOT / "auxiliary_data/boilerplate_short_sentences.tsv"
NUMERIC_TEMPLATES = ROOT / "auxiliary_data/boilerplate_numeric_templates.tsv"

SHORT_MAX = 4                      # longest sentence (non-Punct tokens) protected
ALT_TYPES = {"alt", "heading-alt"}
BODY_PARAGRAPHS = {"text", "quote"}
ROBOT_SIGNOFF = "voitto-robotin tekemästä"
EXCLUDED_PUBLISHERS = {"Yle Selkouutiset"}

TEXT_ATTRS = re.compile(r'(publisher|datefrom)="([^"]*)"')
SENTENCE_ATTRS = re.compile(r' type="([^"]*)" paragraph_type="([^"]*)"')
DIGITS = re.compile(r"\d+")
MARKUP = re.compile(r"[*_]")


class Sentence:
    __slots__ = ("field", "words", "tokens", "markup", "raw")

    def __init__(self, field):
        self.field = field    # (type, paragraph_type)
        self.words = []       # non-Punct word forms
        self.tokens = []      # (lemma, pos) of the non-Punct tokens
        self.markup = False   # a Punct token carries markdown emphasis (* or _)
        self.raw = []         # every word form, Punct included, for display

    @property
    def key(self):
        return " ".join(self.words).lower()

    @property
    def is_alt(self):
        return self.field[0] in ALT_TYPES

    @property
    def is_body(self):
        return self.field[0] == "text" and self.field[1] in BODY_PARAGRAPHS

    @property
    def protectable(self):
        """Short plain body text: the shape of a sentence that recurs naturally."""
        return len(self.words) <= SHORT_MAX and self.is_body and not self.markup


def masked(key):
    """The sentence key with every digit run replaced by 0."""
    return DIGITS.sub("0", key)


def vrt_files():
    return sorted(f for root in VRT_ROOTS for f in root.glob("**/*.vrt"))


def iter_texts(paths, progress=True):
    """Yield (attrs, [Sentence...]) per <text>, attrs holding publisher and datefrom."""
    for i, path in enumerate(paths, 1):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("<"):
                    if line.startswith("<sentence"):
                        m = SENTENCE_ATTRS.search(line)
                        sent = Sentence(m.groups() if m else ("", ""))
                        sents.append(sent)
                    elif line.startswith("<text "):
                        attrs = dict(TEXT_ATTRS.findall(line))
                        sents = []
                    elif line.startswith("</text"):
                        yield attrs, [s for s in sents if s.words]
                    continue
                fields = line.rstrip("\n").split("\t")
                if len(fields) < 5:
                    continue
                sent.raw.append(fields[0])
                if fields[4] == "Punct":
                    if MARKUP.search(fields[0]):
                        sent.markup = True
                    continue
                sent.words.append(fields[0])
                sent.tokens.append((fields[2], fields[4]))
        if progress:
            print(f"[{i}/{len(paths)}] processed {path}", file=sys.stderr)


def is_robot(sents):
    return any(ROBOT_SIGNOFF in s.key for s in sents)


def is_excluded_publisher(attrs):
    return attrs.get("publisher") in EXCLUDED_PUBLISHERS


def load_reviewed_list(path):
    """Set of keys from a reviewed boilerplate list (column `key`)."""
    if not path.exists():
        sys.exit(
            f"Missing {path}: run list_boilerplate_candidates.py and review its "
            "output first (see CLAUDE.md)."
        )
    with open(path, encoding="utf-8") as f:
        return {row["key"] for row in csv.DictReader(f, delimiter="\t")}


def iter_kept_tokens(paths, stats):
    """Yield (lemma, pos) for every token of every kept sentence.

    `stats` (a Counter) receives token totals per outcome: kept,
    kept_protected_repeat, dup_serialisation, dup_template, dup_repeat, alt,
    robot, excluded_publisher.
    """
    stoplist = load_reviewed_list(SHORT_STOPLIST)
    templates = load_reviewed_list(NUMERIC_TEMPLATES)
    seen = set()            # hash of every sentence key counted so far
    seen_template = set()   # hash of every listed masked key counted so far
    for attrs, sents in iter_texts(paths):
        if is_excluded_publisher(attrs):
            stats["excluded_publisher"] += sum(len(s.words) for s in sents)
            continue
        if is_robot(sents):
            stats["robot"] += sum(len(s.words) for s in sents)
            continue
        here = {}           # key hash -> field of its first copy in this text
        for s in sents:
            n = len(s.words)
            if s.is_alt:
                stats["alt"] += n
                continue
            key = s.key
            k = hash(key)
            first_field = here.setdefault(k, s.field)
            if first_field != s.field:
                stats["dup_serialisation"] += n
                continue
            m = masked(key)
            if m != key and m in templates:
                seen.add(k)
                mk = hash(m)
                if mk in seen_template:
                    stats["dup_template"] += n
                    continue
                seen_template.add(mk)
                outcome = "kept"
            elif k not in seen:
                seen.add(k)
                outcome = "kept"
            elif s.protectable and key not in stoplist:
                outcome = "kept_protected_repeat"
            else:
                stats["dup_repeat"] += n
                continue
            stats[outcome] += n
            yield from s.tokens


def report(stats):
    """Print the per-outcome token breakdown."""
    total = sum(stats.values())
    print(f"Corpus tokens (non-Punct): {total}")
    for outcome in ("kept", "kept_protected_repeat", "dup_serialisation",
                    "dup_template", "dup_repeat", "alt", "robot",
                    "excluded_publisher"):
        n = stats[outcome]
        print(f"  {outcome:22} {n:12} {100 * n / total:6.2f}%")
