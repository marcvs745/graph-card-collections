---
type: guide
title: "Card summary editorial sources"
description: "Meaning clues, source selection, reproducible staging, and review limits."
---

# Summary authoring

The canonical values are the `summary` fields in `collections/*/collection.json`. This directory contains explicit editorial corrections and evidence used to produce those values. The application does not carry or load these authoring files.

A clue describes the card's meaning or function in one plain-text line of 1–160 UTF-16 code units. It is system and quiz metadata, not a card-view introduction. Avoid the answer title, spelling/reading aliases, and obvious answer components of compound titles. Do not mechanically delete a title or truncate a definition into a fragment. Preserve the actual description.

Use the ordinary meaning appropriate to the collection. Skip surname/place-name homographs and pure dictionary cross-references when they are not the learning target; do not switch to an unrelated later sense merely to avoid repeating the answer. Preposition collections need grammatical function, and sentence-pattern lessons need a meaning or usage clue rather than an example that reveals the answer.

Create temporary proposals from this checkout:

```
python3 tools/author-language-summaries.py --data-dir . --output-dir /tmp/graph-card-language-proposals
python3 tools/author-academic-summaries.py --data-dir . --output-dir /tmp/graph-card-academic-proposals
```

The tools read canonical inline translations and the corrections here; they write only the explicitly chosen output directory. Review the proposed values before copying only `summary` into the corresponding base/Korean and four localized fields. The correction records preserve source credits through the original collection and cited evidence; the source collection's license conditions still apply to derived definitions.

Run `python3 tools/verify_editorial.py` after application. For the 2026-11-08 change, also run it with `--baseline-ref 13d9693989c9ba9d52ddb88a5bd0a5a6da7c1443` to prove 137 approved art-person descriptions changed, 50,018 other bodies stayed exact, and IDs, titles, relations, source credits and image bytes stayed unchanged. Music's 37 concept-card bodies remain original.

The language/hanja authoring covers 38 collections / 47,027 cards / 188,108 localized clues. Remaining academic/general-knowledge authoring covers 170 collections / 3,128 cards / 12,512 localized clues. Coverage, normalized-title checks and declared language-alias checks are automated; meaning review uses source selection, explicit authored corrections and targeted/representative checks. It is not an independently exhaustive native-speaker or educator certification of all 50,155 cards.

[Art-person evidence and non-applied music proposal history](person-description-review.md) and the review notes in `summary-overrides/` record the focused editorial work. Publication is separate from staging and validation.
