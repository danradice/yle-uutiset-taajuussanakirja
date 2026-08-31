"""Fail a release whose citation metadata does not agree with itself or the tag.

Two files describe the same release to two different services, in two different
formats: `.zenodo.json` is what Zenodo builds the DOI record from, and
`CITATION.cff` is what GitHub's "Cite this repository" button renders. Zenodo
reads `.zenodo.json` first and ignores `CITATION.cff` entirely when it is
present, so nothing but this check keeps the two in step -- and a stale version
in either one is invisible until it has already been published under a DOI.

Run with the version being released (`1.1.1`, or `v1.1.1`), or with no argument
to run only the cross-file checks, which is what a workflow_dispatch run does.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZENODO_JSON = ROOT / ".zenodo.json"
CITATION_CFF = ROOT / "CITATION.cff"

TREE_URL_PREFIX = "https://github.com/danradice/yle-uutiset-taajuussanakirja/tree/"


def cff_scalar(text, key):
    """Return a top-level scalar from CITATION.cff, or None if it is absent.

    Deliberately a regex and not a YAML parse: PyYAML is not in the standard
    library and is absent from a clean setup-python runner, and this repository
    has no dependencies anywhere else either. The anchor matters -- it is what
    keeps `version:` inside the indented `preferred-citation:` block from
    matching instead of the top-level one.
    """
    match = re.search(rf"^{key}:[ \t]*'?([^'\n]+?)'?[ \t]*$", text, re.MULTILINE)
    return match.group(1) if match else None


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "dev"
    # The workflow passes "dev" on workflow_dispatch, where no tag exists.
    tag_version = None if version == "dev" else version.lstrip("v")

    errors = []

    try:
        zenodo = json.loads(ZENODO_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{ZENODO_JSON.name} could not be read as JSON: {exc}", file=sys.stderr)
        return 1

    cff_text = CITATION_CFF.read_text(encoding="utf-8")
    cff_version = cff_scalar(cff_text, "version")
    cff_date = cff_scalar(cff_text, "date-released")

    zenodo_version = zenodo.get("version")
    zenodo_date = zenodo.get("publication_date")

    for name, value in (
        ("CITATION.cff version", cff_version),
        ("CITATION.cff date-released", cff_date),
        (".zenodo.json version", zenodo_version),
        (".zenodo.json publication_date", zenodo_date),
    ):
        if not value:
            errors.append(f"{name} is missing")

    if cff_version and zenodo_version and cff_version != zenodo_version:
        errors.append(
            f"version mismatch: CITATION.cff says {cff_version}, "
            f".zenodo.json says {zenodo_version}"
        )

    if cff_date and zenodo_date and cff_date != zenodo_date:
        errors.append(
            f"release date mismatch: CITATION.cff date-released is {cff_date}, "
            f".zenodo.json publication_date is {zenodo_date}"
        )

    # The isSupplementTo link points at the tagged tree, so it carries the
    # version too and goes stale in exactly the same way.
    tree_urls = [
        related["identifier"]
        for related in zenodo.get("related_identifiers", [])
        if related.get("identifier", "").startswith(TREE_URL_PREFIX)
    ]
    if not tree_urls:
        errors.append(f".zenodo.json has no related identifier under {TREE_URL_PREFIX}")
    elif zenodo_version:
        expected = f"{TREE_URL_PREFIX}v{zenodo_version}"
        for url in tree_urls:
            if url != expected:
                errors.append(f"tree link is {url}, expected {expected}")

    if tag_version:
        if cff_version and cff_version != tag_version:
            errors.append(
                f"CITATION.cff version is {cff_version}, but the tag is v{tag_version}"
            )
        if zenodo_version and zenodo_version != tag_version:
            errors.append(
                f".zenodo.json version is {zenodo_version}, but the tag is v{tag_version}"
            )

    if errors:
        print("citation metadata is inconsistent:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print(
            "bump the version and date in CITATION.cff and .zenodo.json "
            "(including the tree link) before tagging",
            file=sys.stderr,
        )
        return 1

    scope = f"tag v{tag_version}" if tag_version else "cross-file only, no tag"
    print(f"citation metadata agrees ({scope}): version {cff_version}, {cff_date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
