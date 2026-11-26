#!/usr/bin/env python3
"""Append one kanji card per character found in Japanese renewal headwords."""

import argparse
from collections import defaultdict
from datetime import datetime
import gzip
import html
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

LEVELS = ('beginner', 'intermediate', 'advanced', 'conversation', 'academic')
LOCALES = ('ko', 'en-US', 'ja', 'zh-TW')
RELATION = 'custom:kanji-used-in'
LABELS = dict(zip(LOCALES, ('사용됨', 'Used in', '使われる語', '用於')))
HEADINGS = {
    'ko': ('음독', '훈독', '구자체', '신자체', '한자', '뜻 (영어 자료)'),
    'en-US': ('On reading', 'Kun reading', 'Old form', 'Standard Japanese form', 'Kanji', 'Meaning'),
    'ja': ('音読み', '訓読み', '旧字体', '新字体', '漢字', '意味（英語資料）'),
    'zh-TW': ('音讀', '訓讀', '舊字體', '日本新字體', '漢字', '字義（英文資料）'),
}
SOURCE = '[KANJIDIC2](https://www.edrdg.org/kanjidic/kanjidic_legacy.html) · EDRDG · CC BY-SA 4.0'
JOYO = '[常用漢字表](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/)'
# Localized glosses for modern Japanese senses that should not inherit Korean Hanja glosses.
GLOSSES = {
    '学': ('배우다 · 배움', 'learning · study', '知識や技術を身につける', '學習'),
    '食': ('먹다 · 음식', 'eat · food', '口に入れて味わう', '進餐或攝取營養'),
    '働': ('일하다', 'work', '仕事をする', '工作'),
    '曜': ('요일', 'day of the week', '曜日の区分', '星期中的某一天'),
    '込': ('들어가다 · 붐비다', 'go in · be crowded', '中に入る・混み合う', '進入・擁擠'),
    '酸': ('산 · 시다', 'acid · sour', '酸性・すっぱい', '酸・酸味'),
    '娘': ('딸', 'daughter', '子である女性', '女兒'),
    '駅': ('역 · 정거장', 'station', '鉄道の停車場', '車站'),
    '内': ('안 · 내부', 'inside', '内側・内部', '內部'),
    '教': ('가르치다', 'teach', '教えを伝える', '教導'),
    '説': ('설명 · 학설', 'explanation · theory', '説明・学説', '說明・學說'),
    '診': ('진찰하다', 'examine medically', '病状を調べる', '診察'),
    '戸': ('문짝 · 가구', 'door · household', '戸口・世帯', '門扇・戶'),
    '圏': ('범위 · 권역', 'sphere · area', '一定の範囲', '範圍・區域'),
    '税': ('세금', 'tax', '公的な負担金', '稅'),
    '磁': ('자기 · 자력', 'magnetism', '磁石に関わる性質', '磁性'),
    '脂': ('기름 · 지방', 'fat · grease', '動物のあぶら', '油脂'),
    '溶': ('녹다 · 녹이다', 'dissolve', '液体に混じり合う', '溶解'),
    '液': ('액체', 'liquid', '流動する物質', '液體'),
    '療': ('치료하다', 'treat an illness', '病気を治す', '治療'),
    '届': ('닿다 · 배달되다', 'reach · be delivered', '目的の所に至る', '送達'),
    '袋': ('주머니 · 봉지', 'bag · pouch', '物を入れる袋', '袋子'),
    '鍵': ('열쇠', 'key', '錠を開閉する道具', '鑰匙'),
    '箱': ('상자', 'box', '物を入れる箱', '箱子'),
    '円': ('둥글다 · 엔', 'round · yen', '丸い形・日本の通貨単位', '圓形・日圓'),
    '飲': ('마시다', 'drink', '液体を口にする', '飲用'),
    '呂': ('음률·목욕 관련 낱말에 쓰이는 글자', 'used in words for pitch and baths', '音律や浴室に関する語に使う字', '用於音律、浴室等詞'),
    '帽': ('모자', 'hat', '頭にかぶる物', '帽子'),
    '拶': ('다가오다', 'draw near', '近づく', '逼近'),
    '挨': ('다가가다', 'approach', '近寄る', '靠近'),
    '昆': ('형·후손', 'elder sibling or descendants', '年上のきょうだい・子孫', '兄長、後代'),
    '札': ('표·지폐', 'tag or banknote', '目印の小片や紙幣', '標籤、紙幣'),
    '炊': ('밥을 짓다', 'cook rice', '米を煮てご飯にする', '煮飯'),
    '稚': ('어리다', 'young or immature', '幼い', '年幼'),
    '紳': ('신사·품위 있는 사람', 'gentleman', '品位のある男性', '紳士'),
    '菓': ('과자', 'confectionery', '甘い食べ物', '糕餅、糖果'),
    '貰': ('받다', 'receive', '人から受け取る', '收下'),
    '酎': ('술·증류주', 'liquor or distilled spirits', '酒や蒸留した酒', '酒、蒸餾酒'),
    '駐': ('머무르다·주차하다', 'stay or park', 'とどまる・車を止める', '駐留、停車'),
    '剤': ('약제', 'preparation or medicine', '薬として調製したもの', '藥劑'),
    '岩': ('바위', 'rock', '大きな石', '岩石'),
    '融': ('녹다·융합하다', 'melt or merge', 'とける・一つに混じる', '融化、融合'),
    '齢': ('나이', 'age', '年の数', '年齡'),
    '掲': ('내걸다', 'display or put up', '上にあげて示す', '揭示'),
    '預': ('맡기다·맡다', 'entrust or keep for someone', '人に任せる・物を引き受ける', '寄存、受託保管'),
    '脱': ('벗다·벗어나다', 'take off or get out', '衣服をぬぐ・外に出る', '脫下、脫離'),
    '託': ('맡기다·부탁하다', 'entrust or request', '人に任せる', '託付'),
    '戻': ('돌아가다·되돌리다', 'return or put back', '元にかえる・元にかえす', '返回、放回'),
    '遮': ('가리다·가로막다', 'block or obstruct', '間に入って妨げる', '遮擋'),
    '描': ('그리다', 'draw or depict', '絵や言葉で表す', '描繪'),
    '清': ('맑다·깨끗하다', 'clear or pure', '澄んでいる・きれいな', '清澈、潔淨'),
    '濃': ('짙다·진하다', 'dense or concentrated', '色や味が強い', '濃厚'),
    '締': ('조이다·맺다', 'tighten or bind', 'きつく固定する・結ぶ', '繫緊、締結'),
    '繰': ('감다·차례로 넘기다', 'reel in or turn in order', '糸を巻き取る・順に動かす', '捲繞、依序翻動'),
    '詰': ('채우다·꽉 차다', 'fill up or be packed', '中がいっぱいになる', '填滿、塞滿'),
    '雇': ('고용하다', 'employ', '賃金を払って働いてもらう', '僱用'),
    '煮': ('삶다·끓이다', 'boil or simmer', '液体で加熱して調理する', '煮、燉'),
    '焦': ('타다·초조하다', 'scorch or be impatient', '焼けすぎる・気がせく', '燒焦、焦急'),
    '滑': ('미끄럽다·미끄러지다', 'slide or be slippery', 'なめらかに動く', '滑動'),
    '既': ('이미·벌써', 'already', 'それより前に済んでいる', '已經'),
    '括': ('묶다·한데 모으다', 'tie or group together', 'ひとまとまりにする', '綑綁、歸納'),
    '併': ('합치다·함께 하다', 'combine or do together', '一緒にする', '合併、並行'),
    '網': ('그물·연결망', 'net or network', '糸などで編んだもの・つながり', '網、網絡'),
    '扱': ('다루다·취급하다', 'handle or deal with', '物や人に対処する', '處理、對待'),
    '拭': ('닦다', 'wipe', '布などで汚れを取る', '擦拭'),
    '敷': ('깔다·펼치다', 'lay or spread', '下に広げて置く', '鋪設'),
    '棚': ('선반', 'shelf', '物を載せる板', '擱板'),
    '沸': ('끓다', 'boil', '液体が泡立つほど熱くなる', '沸騰'),
    '閲': ('열람하다·살펴보다', 'inspect or read', '資料などを見て確かめる', '閱覽、檢閱'),
    '晶': ('결정·빛나다', 'crystal or sparkle', '透明な結晶や輝き', '晶體、光亮'),
    '掘': ('파다', 'dig', '地面を深く取り去る', '挖掘'),
    '摩': ('문지르다', 'rub', 'こする', '摩擦'),
}
# Paired values are standard romanization and approximate Korean reading aids.
ROWS = (
    ('ア イ ウ エ オ', 'a i u e o', '아 이 우 에 오'),
    ('カ キ ク ケ コ キャ キュ キョ', 'ka ki ku ke ko kya kyu kyo', '카 키 쿠 케 코 캬 큐 쿄'),
    ('ガ ギ グ ゲ ゴ ギャ ギュ ギョ', 'ga gi gu ge go gya gyu gyo', '가 기 구 게 고 갸 규 교'),
    ('サ シ ス セ ソ シャ シュ ショ', 'sa shi su se so sha shu sho', '사 시 스 세 소 샤 슈 쇼'),
    ('ザ ジ ズ ゼ ゾ ジャ ジュ ジョ', 'za ji zu ze zo ja ju jo', '자 지 즈 제 조 자 주 조'),
    ('タ チ ツ テ ト チャ チュ チョ', 'ta chi tsu te to cha chu cho', '타 치 츠 테 토 차 추 초'),
    ('ダ ヂ ヅ デ ド ヂャ ヂュ ヂョ', 'da ji zu de do ja ju jo', '다 지 즈 데 도 자 주 조'),
    ('ナ ニ ヌ ネ ノ ニャ ニュ ニョ', 'na ni nu ne no nya nyu nyo', '나 니 누 네 노 냐 뉴 뇨'),
    ('ハ ヒ フ ヘ ホ ヒャ ヒュ ヒョ', 'ha hi fu he ho hya hyu hyo', '하 히 후 헤 호 햐 휴 효'),
    ('バ ビ ブ ベ ボ ビャ ビュ ビョ', 'ba bi bu be bo bya byu byo', '바 비 부 베 보 뱌 뷰 뵤'),
    ('パ ピ プ ペ ポ ピャ ピュ ピョ', 'pa pi pu pe po pya pyu pyo', '파 피 푸 페 포 퍄 퓨 표'),
    ('マ ミ ム メ モ ミャ ミュ ミョ', 'ma mi mu me mo mya myu myo', '마 미 무 메 모 먀 뮤 묘'),
    ('ヤ ユ ヨ ラ リ ル レ ロ リャ リュ リョ', 'ya yu yo ra ri ru re ro rya ryu ryo', '야 유 요 라 리 루 레 로 랴 류 료'),
    ('ワ ヰ ヱ ヲ ン ッ ー', 'wa wi we o n gem long', '와 위 웨 오 ㄴ ㅅ ー'),
)
MORA = {kana: (latin, ko) for a, b, c in ROWS for kana, latin, ko in zip(a.split(), b.split(), c.split())}
KATAKANA = str.maketrans({chr(n): chr(n + 96) for n in range(0x3041, 0x3097)})
KANA_WORD = re.compile(r'^[ぁ-ゖァ-ヺー]+$')
KANJI_ID = re.compile(r'^ja-kanji-[a-f0-9]+$')


def chars(text):
    return {c for c in text if unicodedata.name(c, '').startswith(('CJK UNIFIED IDEOGRAPH-', 'CJK COMPATIBILITY IDEOGRAPH-'))}


def romanizations(reading):
    is_on = reading == reading.translate(KATAKANA)
    text = reading.translate(KATAKANA)
    chunks = []
    while text:
        mora = text[:2] if text[:2] in MORA else text[:1]
        if mora not in MORA:
            return None
        chunks.append(MORA[mora])
        text = text[len(mora):]
    romaji, hangul = [], []
    for i, (latin, ko) in enumerate(chunks):
        following = chunks[i + 1][0] if i + 1 < len(chunks) else ''
        previous = chunks[i - 1][0] if i else ''
        if latin == 'gem':
            if not hangul or not following or following in {'gem', 'n', 'long'}:
                return None
            romaji.append('t' if following.startswith('ch') else following[0])
            hangul[-1] = chr(ord(hangul[-1]) + 19)
        elif latin == 'n':
            if not hangul:
                return None
            romaji.append("n'" if following.startswith(('a', 'i', 'u', 'e', 'o', 'y')) else 'n')
            hangul[-1] = chr(ord(hangul[-1]) + 4)
        elif latin == 'long' or (latin in ('u', 'o') and previous.endswith('o')
                                 and (is_on or latin == 'o' or i + 1 < len(chunks))):
            vowel = previous[-1:]
            if vowel not in 'aiueo' or not romaji:
                return None
            romaji[-1] = romaji[-1][:-1] + dict(zip('aiueo', 'āīūēō'))[vowel]
            hangul.append(dict(zip('aiueo', '아이우에오'))[vowel])
        else:
            romaji.append(latin)
            hangul.append(ko)
    return ''.join(romaji), ''.join(hangul)


def joyo_data(file):
    output = {}
    text = file.read_text(encoding='cp932')
    for row in re.findall(r'<tr>\s*(.*?)</tr>', text, flags=re.S | re.I):
        columns = re.findall(r'<td[^>]*>(.*?)</td>', row, flags=re.S | re.I)
        if len(columns) != 4:
            continue

        def cells(cell):
            return [html.unescape(re.sub('<[^>]+>', '', entry)).strip()
                    for entry in re.split(r'<br\s*/?>', cell, flags=re.I)]

        name = cells(columns[0])[0]
        if not name or not chars(name[0]):
            continue
        old = re.search(r'（(.)）', name)
        readings = tuple(x for x in cells(columns[1]) if KANA_WORD.fullmatch(x))
        output[name[0]] = (old[1] if old and chars(old[1]) else None, readings)
    if not 2100 <= len(output) <= 2200 or output.get('学') != ('學', ('ガク', 'まなぶ')):
        raise ValueError('Unexpected Jōyō table')
    return output


def dictionary(file):
    with gzip.open(file) as source:
        root = ET.parse(source).getroot()
    output = {}
    for entry in root.findall('character'):
        readings = [r.text.strip('.-').replace('.', '') for r in entry.findall('.//rmgroup/reading')
                    if r.get('r_type') in ('ja_on', 'ja_kun') and r.text and not r.text.startswith('-')]
        meanings = [m.text for m in entry.findall('.//rmgroup/meaning') if not m.attrib
                    and m.text and not m.text.startswith('(') and not chars(m.text)]
        output[entry.findtext('literal')] = (list(dict.fromkeys(readings)), meanings)
    if len(output) < 13000:
        raise ValueError('Incomplete KANJIDIC2')
    return output


def load(file):
    return json.loads(file.read_text(encoding='utf-8'))


def localized(card, locale):
    return card.get('localization', {}).get('translations', {}).get(locale, {})


def looks_like_gloss(value, kanji, reading_aliases):
    return value and value not in reading_aliases and kanji not in value and not re.search(r'[\r\n]', value)


def get_glosses(kanji, old, readings, lexical, hanja, english):
    if kanji in GLOSSES:
        return dict(zip(LOCALES, GLOSSES[kanji])), []
    meanings = {'en-US': english}
    reference = hanja.get(kanji) or hanja.get(old)
    for locale in ('ko', 'ja', 'zh-TW'):
        candidates = [localized(reference, locale).get('summary')] if reference else []
        candidates.extend(localized(source, locale).get('summary') for source in lexical.get(kanji, []))
        clue = next((value for value in candidates if looks_like_gloss(value, kanji, readings)), None)
        if clue:
            meanings[locale] = clue
    fallback = [locale for locale in LOCALES if locale not in meanings]
    return {locale: meanings.get(locale, english) for locale in LOCALES}, fallback


def for_locale(char, old, readings, definition, fallback, locale, duplicate, official):
    on, kun, old_label, new_label, kanji_label, gloss_label = HEADINGS[locale]
    shown = {on: [], kun: []}
    for reading in readings:
        aids = romanizations(reading)
        if aids is None:
            continue
        group = on if reading[0].translate(KATAKANA) == reading[0] and reading[0] != 'ー' else kun
        aid = aids[1] if locale == 'ko' else aids[0]
        shown[group].append(reading if locale == 'ja' else f'{reading} ({aid})')
    sections = [f'**{gloss_label}** · {definition}' if fallback else f'**{definition}**']
    sections.extend(f'**{label}** · ' + ' · '.join(values) for label, values in shown.items() if values)
    if old:
        sections.append(f'{old} ({old_label}) → {char} ({new_label})')
    sections.append((JOYO + ' · ' if official else '') + SOURCE)
    title = f'{char} · {kanji_label}' if duplicate else char
    return dict(title=title, description='\n\n'.join(sections), summary=definition, descriptionFormat='markdown')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--joyo', type=Path, required=True)
    parser.add_argument('--kanjidic', type=Path, required=True)
    parser.add_argument('--published-at', required=True)
    args = parser.parse_args()
    date = datetime.fromisoformat(args.published_at)
    if not date.tzinfo:
        parser.error('--published-at requires a UTC offset')
    collections = Path(__file__).resolve().parent.parent / 'collections'
    joyo, definitions = joyo_data(args.joyo), dictionary(args.kanjidic)
    hanja = {}
    for level in ('beginner', 'intermediate', 'advanced'):
        for card in load(collections / f'hanja-{level}' / 'collection.json')['cards']:
            hanja.setdefault(card['title'], card)
    paths = [collections / f'ja-renewal-{level}' / 'collection.json' for level in LEVELS]
    decks = [load(path) for path in paths]
    lexical = defaultdict(list)
    for deck in decks:
        for card in deck['cards']:
            if KANJI_ID.fullmatch(card['cardId']):
                continue
            if len(card['title']) == 1 and chars(card['title']):
                lexical[card['title']].append(card)

    audit = {}
    for level, path, deck in zip(LEVELS, paths, decks):
        original = [card for card in deck['cards'] if not KANJI_ID.fullmatch(card['cardId'])]
        existing_titles = {card['title'] for card in original}
        uses = defaultdict(list)
        for card in original:
            headword = localized(card, 'ja').get('title', card['title'])
            for char in chars(headword):
                uses[char].append(card['cardId'])
        new_cards, skipped, fallback = [], [], defaultdict(int)
        for char, targets in sorted(uses.items(), key=lambda entry: (-len(entry[1]), entry[0])):
            old, official_readings = joyo.get(char, (None, ()))
            dictionary_readings, meanings = definitions.get(char, ([], []))
            readings = list(dict.fromkeys(r for r in official_readings or dictionary_readings
                                          if KANA_WORD.fullmatch(r) and romanizations(r)))
            english = ' · '.join(meanings[:2])
            if not readings or not english:
                skipped.append(char)
                continue
            glosses, using_english = get_glosses(char, old, readings, lexical, hanja, english)
            for locale in using_english:
                fallback[locale] += 1
            translations = {locale: for_locale(char, old, readings, glosses[locale], locale in using_english,
                                               locale, char in existing_titles, char in joyo)
                            for locale in LOCALES}
            for translation in translations.values():
                if char in translation['summary']:
                    translation['summary'] = english
            card = {'cardId': f'ja-kanji-{ord(char):x}', 'role': 'class', **translations['ko'],
                    'images': [], 'relations': [{'type': RELATION, 'targetCardId': target} for target in targets],
                    'localization': {'sourceLocale': 'ko', 'translations': translations}}
            new_cards.append(card)
        deck['cards'] = original + new_cards
        deck['customRelations'] = [r for r in deck['customRelations'] if r['id'] != RELATION] + [
            {'id': RELATION, 'label': LABELS['ko'], 'localizedLabels': LABELS}]
        deck['contentVersion'] = f'renewal-{date.date()}-kanji-1'
        deck['publishedAt'] = args.published_at
        assert len({card['cardId'] for card in deck['cards']}) == len(deck['cards'])
        audit[level] = {'words': len(original), 'kanji': len(new_cards), 'edges': sum(len(c['relations']) for c in new_cards),
                        'englishGlossFallback': dict(fallback), 'excluded': sorted(skipped)}
        path.write_text(json.dumps(deck, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
