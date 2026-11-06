"""Read the Kotus nykysuomen sanalista and its word classes.

Shared by count_lemmas.py, build_dictionary.py, build_pos_subdictionaries.py and
list_boilerplate_candidates.py, so that every script reads the wordlist and
interprets its Sanaluokka field the same way.

word_lists/nykysuomensanalista2024.txt is tab-separated, with columns Hakusana
(headword), Homonymia, Sanaluokka and Taivutustiedot. A headword has one row per
sense; a numbered Homonymia marks the senses of a homonym.
"""

import csv
from collections import Counter

from vrt_sentences import ROOT

WORDLIST = ROOT / "word_lists/nykysuomensanalista2024.txt"

# Sanaluokka (sanalista word class) -> VRT/Korp pos code(s). The corpus does not
# distinguish prepositio/postpositio (both Adp), so those collapse onto one code.
SANALUOKKA_TO_POS = {
    "substantiivi": {"N"},
    "verbi": {"V"},
    "adjektiivi": {"A"},
    "adverbi": {"Adv"},
    "pronomini": {"Pron"},
    "numeraali": {"Num"},
    "järjestysluku": {"Num"},
    "konjunktio": {"C", "CS"},
    "rinnastuskonjunktio": {"C"},
    "alistuskonjunktio": {"CS"},
    "interjektio": {"Interj"},
    "postpositio": {"Adp"},
    "prepositio": {"Adp"},
    "kieltoverbi": {"V"},
}


def load_wordlist(path=WORDLIST):
    """Return {headword: [sense row, ...]}, headwords in first-seen order.

    Each sense row is the wordlist row as a dict (Hakusana, Homonymia,
    Sanaluokka, Taivutustiedot).
    """
    senses = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            senses.setdefault(row["Hakusana"], []).append(row)
    return senses


def split_classes(sanaluokka):
    """Split a (possibly multi-valued) Sanaluokka field into individual classes.

    A single sense can carry several word classes, e.g. "substantiivi, adjektiivi"
    (comma- or "+"-separated), so a field is not one opaque label.
    """
    classes = []
    for part in (sanaluokka or "").split(","):
        for tok in part.split("+"):
            tok = tok.strip()
            if tok:
                classes.append(tok)
    return classes


def class_labels(fields):
    """{class: label} for a lemma's per-sense Sanaluokka fields, in first-seen order.

    `fields` holds one raw Sanaluokka value per sense. A class carried by more
    than one sense (the lemma has several meanings of that part of speech) gets a
    trailing asterisk in its label; a class repeated within one sense does not.
    """
    meanings = Counter()
    for field in fields:
        for cls in dict.fromkeys(split_classes(field)):  # distinct within a sense
            meanings[cls] += 1
    return {cls: cls + ("*" if n > 1 else "") for cls, n in meanings.items()}


def format_sanaluokat(fields):
    """The Sanaluokat cell for a lemma's per-sense Sanaluokka fields."""
    return ", ".join(class_labels(fields).values())


def pos_codes(fields):
    """Union of VRT pos codes the lemma's sanalista word classes map to."""
    codes = set()
    for field in fields:
        for cls in split_classes(field):
            codes |= SANALUOKKA_TO_POS.get(cls, set())
    return codes
