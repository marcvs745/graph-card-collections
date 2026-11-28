"""Label vocabulary and character cards in the Japanese and Taiwan Mandarin built-ins."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("ja-renewal", "zh-tw-mandarin")
LEVELS = ("beginner", "intermediate", "advanced", "conversation", "academic")
TAG_BY_ROLE = {"none": "어휘", "class": "한자"}
SUFFIX = "-card-tags1"


def main() -> None:
    pending = []
    for language in LANGUAGES:
        for level in LEVELS:
            slug = f"{language}-{level}"
            path = ROOT / "collections" / slug / "collection.json"
            deck = json.loads(path.read_text(encoding="utf-8"))
            if deck["collectionId"] != f"builtin-{slug}":
                raise ValueError(f"{slug}: unexpected collection ID")
            roles = {card["role"] for card in deck["cards"]}
            if roles != TAG_BY_ROLE.keys():
                raise ValueError(f"{slug}: review the card assignments for roles {sorted(roles)}")
            changed = False
            for card in deck["cards"]:
                tags = card.get("tags", [])
                label = TAG_BY_ROLE[card["role"]]
                if label not in tags:
                    card["tags"] = [*tags, label]
                    changed = True
            if changed:
                if not deck["contentVersion"].endswith(SUFFIX):
                    deck["contentVersion"] += SUFFIX
                pending.append((path.with_name("collection.tags-v1.json"), deck))
    for path, deck in pending:
        path.write_text(json.dumps(deck, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"{path.parent.name}: {len(deck['cards'])}")


if __name__ == "__main__":
    main()
