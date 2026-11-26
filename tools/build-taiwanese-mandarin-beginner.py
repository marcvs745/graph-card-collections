"""Build the Taiwanese Mandarin starter deck from the reviewed editorial rows."""

import argparse
import csv
from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = 'zh-tw-mandarin-beginner'
LEVELS = {
    'ko': ('중국어(대만) · 초급', '번체자와 대만 표준 중국어로 인사, 길 찾기, 식사와 결제 표현을 익힙니다.', '병음', '주음', '발음 출처'),
    'en-US': ('Taiwanese Mandarin · Beginner', 'Learn greetings, directions, dining, and payment expressions in Taiwanese Mandarin with Traditional Chinese characters.', 'Pinyin', 'Zhuyin', 'Pronunciation source'),
    'ja': ('台湾華語 · 初級', '繁体字と台湾華語で、あいさつ、道案内、食事や支払いの表現を学びます。', 'ピンイン', '注音', '発音の出典'),
    'zh-TW': ('臺灣華語・初級', '用繁體字學習臺灣華語的問候、問路、用餐與付款用語。', '漢語拼音', '注音', '讀音來源'),
}
TOPICS = ['중국어', '일반 어휘', '초급']
RELATION = {
    'id': 'custom:related-situation', 'label': '같은 상황',
    'localizedLabels': {'ko': '같은 상황', 'en-US': 'Related situation', 'ja': '同じ場面', 'zh-TW': '相關情境'},
}
EDGES = {
    'hello': ['goodbye'], 'thanks': ['no-problem'], 'excuse': ['no-problem', 'ask'],
    'ask': ['where', 'mrt'], 'today': ['tomorrow'], 'where': ['restroom', 'station'],
    'restroom': ['entrance'], 'may': ['pay'], 'bus': ['station', 'ride'], 'mrt': ['exit', 'ride'],
    'taxi': ['ride'], 'train': ['platform', 'station'], 'station': ['platform', 'entrance'],
    'platform': ['arrive'], 'entrance': ['exit'], 'walk': ['arrive'], 'ride': ['arrive'],
    'water': ['drink'], 'tea': ['drink'], 'coffee': ['want'], 'bento': ['lunch', 'buy'],
    'breakfast': ['lunch'], 'lunch': ['dinner'], 'dinner': ['eat'],
    'how-much': ['money', 'dollar'], 'buy': ['convenience', 'pay'], 'pay': ['cash', 'money'],
    'cash': ['dollar'], 'hospital': ['bus'], 'eat': ['noodles'], 'want': ['noodles'],
}
NAER = 'https://coct.naer.edu.tw/page.jsp?ID=41'
MOE_NI = 'https://dict.revised.moe.edu.tw/dictView.jsp?ID=3026'
MOE_HAO = 'https://dict.revised.moe.edu.tw/dictView.jsp?ID=80848'


def make_card(row):
    title = row['word']
    translations = {}
    for locale, (_, _, pinyin, zhuyin, source) in LEVELS.items():
        hint = row['en' if locale == 'en-US' else locale]
        if title in hint or title not in row['example-zh']:
            raise ValueError(f'Invalid clue or example: {title}')
        details = [f"**{hint}**", f"**{pinyin}** {row['pinyin']}  \n**{zhuyin}** {row['zhuyin']}",
                   f"*{row['example-zh']}*"]
        if locale != 'zh-TW':
            details[-1] += '\n' + row['example-' + ('en' if locale == 'en-US' else locale)]
        if row['readingSource'] == 'MOE':
            credit = f'[教育部《重編國語辭典修訂本》你]({MOE_NI}) · [好]({MOE_HAO})'
        else:
            credit = f"[國家教育研究院・三等七級詞語表 #{row['readingSource']}]({NAER}) · CC BY"
        details.append(f'{source} {credit}')
        translations[locale] = dict(title=title, summary=hint, description='\n\n'.join(details), descriptionFormat='markdown')
    return {'cardId': f'zh-tw-{row["id"]}', 'role': 'none', **translations['ko'], 'images': [],
            'relations': [{'type': RELATION['id'], 'targetCardId': f'zh-tw-{target}'} for target in EDGES.get(row['id'], [])],
            'localization': {'sourceLocale': 'ko', 'translations': translations}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--published-at', required=True)
    args = parser.parse_args()
    date = datetime.fromisoformat(args.published_at)
    if date.tzinfo is None:
        parser.error('Timestamp requires a UTC offset')
    with (ROOT / 'editorial' / 'taiwanese-mandarin-beginner.tsv').open(encoding='utf-8') as file:
        cards = [make_card(row) for row in csv.DictReader(file, delimiter='\t')]
    ids = {card['cardId'] for card in cards}
    assert len(ids) == len(cards) and all(relation['targetCardId'] in ids for card in cards for relation in card['relations'])
    translations = {locale: {'title': info[0], 'description': info[1]} for locale, info in LEVELS.items()}
    deck = {'protocolVersion': 2, 'collectionId': 'builtin-' + SLUG, **translations['ko'],
            'contentVersion': f'taiwan-mandarin-{date.date()}-1', 'publishedAt': args.published_at,
            'viewMode': 'both', 'tags': ['vocabulary'], 'topics': TOPICS, 'assets': [], 'cards': cards,
            'customRelations': [RELATION], 'localization': {'sourceLocale': 'ko', 'translations': translations}}
    output = ROOT / 'collections' / SLUG / 'collection.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(deck, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8')
    print(f'{len(cards)} cards, {sum(len(card["relations"]) for card in cards)} related-situation links')


if __name__ == '__main__':
    main()
