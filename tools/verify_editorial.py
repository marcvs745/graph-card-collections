"""Validate quiz clues and prove that an editorial change preserves other content."""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import unicodedata

LOCALES = ('ko', 'en-US', 'ja', 'zh-TW')


def reveals_title(title, summary):
    title = unicodedata.normalize('NFKC', title).casefold().strip()
    summary = unicodedata.normalize('NFKC', summary).casefold()
    if re.fullmatch(r'[a-z][a-z\s\W]*', title) and re.search('[a-z]', title):
        return re.search(r'(?<![a-z])' + re.escape(title) + r'(?![a-z])', summary) is not None
    normalized = ''.join(c for c in title if c.isalnum())
    if not normalized:
        return bool(title) and title in summary
    if len(normalized) == 1 and re.fullmatch('[가-힣]', normalized):
        return re.search(r'(?<![가-힣])' + normalized + r'(?:은|는|이|가|을|를|의)?(?![가-힣])', summary) is not None
    return normalized in ''.join(c for c in summary if c.isalnum())


def without_editorial_fields(collection):
    value = copy.deepcopy(collection)
    for key in ('contentVersion', 'publishedAt'):
        value.pop(key, None)
    for card in value['cards']:
        card.pop('summary', None)
        card.pop('description', None)
        for translated in card.get('localization', {}).get('translations', {}).values():
            translated.pop('summary', None)
            translated.pop('description', None)
    return value


def verify(root, baseline_ref=None):
    collections = cards = summaries = changed = protected = 0
    baseline_files = None
    if baseline_ref:
        baseline_files = set(subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', baseline_ref, 'collections'], cwd=root, text=True
        ).splitlines())
        current_files = {str(p.relative_to(root)) for p in (root / 'collections').rglob('*') if p.is_file()}
        assert current_files == baseline_files, 'Collection/asset file set changed'
    allowlist_path = root / 'tools/editorial-description-targets.json'
    allowlist = set(json.loads(allowlist_path.read_text())) if allowlist_path.exists() else set()
    seen_targets = set()
    for path in sorted((root / 'collections').glob('*/collection.json')):
        collection = json.loads(path.read_text())
        collections += 1
        old = None
        if baseline_ref:
            old = json.loads(subprocess.check_output(
                ['git', 'show', f'{baseline_ref}:{path.relative_to(root)}'], cwd=root, text=True))
            assert without_editorial_fields(collection) == without_editorial_fields(old), path
            old_cards = {c['cardId']: c for c in old['cards']}
        for card in collection['cards']:
            cards += 1
            key = collection['collectionId'] + '::' + card['cardId']
            translations = card.get('localization', {}).get('translations', {})
            assert set(LOCALES).issubset(translations), (key, 'missing locale')
            assert card.get('summary') == translations['ko'].get('summary'), (key, 'base/ko mismatch')
            for locale in LOCALES:
                translated = translations[locale]
                clue = translated.get('summary')
                assert isinstance(clue, str) and clue.strip() and clue == clue.strip(), (key, locale, 'empty or untrimmed clue')
                assert '\n' not in clue and '\r' not in clue and len(clue.encode('utf-16-le')) // 2 <= 160, (key, locale, 'clue shape')
                assert not reveals_title(translated.get('title', card['title']), clue), (key, locale, 'title leak')
                summaries += 1
            if old is not None:
                previous = old_cards[card['cardId']]
                differences = [card['description'] != previous['description']]
                differences += [translations[loc]['description'] != previous['localization']['translations'][loc]['description'] for loc in LOCALES]
                if key in allowlist:
                    assert all(differences), (key, 'target not improved in every locale')
                    seen_targets.add(key)
                    changed += 1
                else:
                    assert not any(differences), (key, 'unapproved body change')
                    protected += 1
    if baseline_ref:
        assert seen_targets == allowlist, 'Description target set mismatch'
        assets = sorted(p for p in baseline_files if not p.endswith('/collection.json'))
        # git diff also catches binary modifications without loading every image into memory.
        for start in range(0, len(assets), 200):
            assert not subprocess.check_output(['git', 'diff', '--name-only', baseline_ref, '--', *assets[start:start + 200]], cwd=root), 'Assets changed'
    return dict(collections=collections, cards=cards, localizedSummaries=summaries,
                changedBodies=changed, preservedBodies=protected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-ref', help='Git revision before the editorial update')
    args = parser.parse_args()
    print(json.dumps(verify(Path(__file__).resolve().parents[1], args.baseline_ref)))
