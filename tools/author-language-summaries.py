#!/usr/bin/env python3
"""Derive quiz clues from complete principal dictionary senses, never text slices.

Only writes new summary sources. Circular/overlong definitions are reported and
left absent rather than disguised as usable clues. Run from the repository root.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ('ko', 'en-US', 'ja', 'zh-TW')
LANGUAGES = {'영어', '일본어', '중국어', '한국어', '한자'}

# Meaning-preserving paraphrases for circular English glosses. Reused only for
# identical headwords, never as a mechanical removal of a word inside a sentence.
ENGLISH = {
    'a': 'Indefinite article marking one unspecified singular countable noun',
    'at': 'Marks location or a particular point',
    'black': 'The darkest color, with little or no reflected light',
    'blue': 'The color associated with a clear daytime sky',
    'brown': 'The color associated with wood or soil',
    'brush': 'A tool with bristles for cleaning or smoothing surfaces',
    'coffee': 'A drink made by brewing roasted beans in water',
    'egg': 'A rounded reproductive body laid by a bird, often eaten as food',
    'fat': 'An oily substance stored in the body; having a large amount of this substance',
    'fight': 'To struggle against or engage in a physical conflict',
    'fish': 'An aquatic animal with gills; to catch such animals',
    'good': 'Of high quality or morally right',
    'green': 'The color associated with grass and many leaves',
    'hair': 'Fine strands growing from the skin of the head or body',
    'money': 'Coins, notes, or other means used to pay for things',
    'north': 'The compass direction opposite south',
    'paint': 'A colored substance spread on a surface; to coat or create a picture with it',
    'plastic': 'A material that can be shaped into many forms',
    'red': 'The color associated with blood',
    'sleep': 'A natural resting state in which awareness of surroundings is reduced',
    'smile': 'To raise the corners of the mouth as a facial expression',
    'that': 'Points to a particular person or thing; introduces an idea or fact',
    'the': 'Definite article marking specific or previously mentioned things',
    'third': 'At position number 3 in an ordered sequence',
    'twenty-first': 'At position number 21 in an ordered sequence',
    'twenty-second': 'At position number 22 in an ordered sequence',
    'twenty-third': 'At position number 23 in an ordered sequence',
    'white': 'The lightest color, associated with fresh snow',
    'yellow': 'The color associated with ripe lemons',
    'access': 'A way or opportunity to enter or use something',
    'account': 'An arrangement for keeping money at a bank; a report or explanation',
    'adopt': 'To take up an idea or practice; to legally take a child into a family',
    'afford': 'To have enough money, time, or other resources for something',
    'apply': 'To formally request something; to put something into use',
    'balance': 'A state of equilibrium; the amount remaining in an account',
    'bench': 'A long seat for several people, often found in a park',
    'billion': '1,000,000,000 in the short scale used in modern English',
    'blame': 'To say someone is responsible for something bad',
    'blank': 'Empty, with no writing or information filled in',
    'bow': 'To bend the head or body as a gesture',
    'bump': 'To hit something accidentally; a raised swelling',
    'bury': 'To put in the ground and cover with earth',
    'character': 'A personality; a person in a story; a written symbol',
    'charm': 'An attractive quality that makes people like someone',
    'chest': 'The front of the body between the neck and waist',
    'chief': 'Most important; a person in charge of a group',
    'compare': 'To consider similarities and differences between things',
    'continue': 'To carry on without stopping or after a pause',
    'cope': 'To deal successfully with a difficult problem',
    'copy': 'A reproduction of an original; to reproduce something',
    'cottage': 'A small house in the countryside',
    'cotton': 'A soft plant fiber used to make cloth',
    'crown': 'A ceremonial headpiece worn by a monarch',
    'current': 'Present or happening now; a flow of water or electricity',
    'damage': 'Harm that reduces the condition or usefulness of something',
    'deck': 'A floor on a ship; a pack of playing cards; a raised outdoor platform',
    'delay': 'To make something happen later than planned',
    'delight': 'Great pleasure; to give great pleasure',
    'depend': 'To need support from someone or something; to be determined by something',
    'direct': 'Straightforward; to tell someone what to do',
    'disgust': 'A strong feeling of revulsion',
    'doubt': 'Uncertainty about whether something is true',
    'ease': 'Comfort or lack of difficulty; to lessen something unpleasant',
    'empty': 'Containing nothing; to remove the contents',
    'exchange': 'To give something and receive something else in return',
    'expert': 'A person with special knowledge or skill',
    'factor': 'Something influencing a result; a number dividing another exactly',
    'faint': 'Hard to perceive; to lose consciousness',
    'female': 'The sex that typically produces eggs in reproduction',
    'final': 'Last in a sequence; the deciding match in a competition',
    'finance': 'The management of money; to provide funds',
    'flag': 'A marked piece of cloth used as a symbol or signal',
    'flight': 'The act of flying; a scheduled journey by aircraft',
    'float': 'To stay on a liquid without sinking',
    'flood': 'Water covering land that is normally dry',
    'flow': 'To move steadily and continuously, as a liquid does',
    'force': 'Strength or power; to compel someone to do something',
    'forward': 'Toward the front; to pass something on',
    'fright': 'Sudden fear',
    'fur': 'The thick covering of soft strands on an animal’s skin',
    'gate': 'An opening with a movable barrier in a fence; an aircraft boarding point',
    'giant': 'An imaginary person of enormous size; extremely large',
    'glue': 'An adhesive substance used to stick surfaces together',
    'hide': 'To put something where it cannot be seen or found',
    'hug': 'To hold someone closely in the arms',
    'increase': 'To become or make larger in amount or size',
    'individual': 'A single person or thing considered separately',
    'influence': 'The power to affect what happens or how someone acts',
    'male': 'The sex that typically produces sperm in reproduction',
    'net': 'A mesh of knotted threads; the amount remaining after deductions',
    'ought': 'Expresses what should be done or is expected to happen',
    'patient': 'A person receiving medical care; able to wait without annoyance',
    'progress': 'Movement toward a goal or a better state',
    'pump': 'A device that moves liquid or gas',
    'punish': 'To impose a penalty for wrongdoing',
    'refer': 'To mention something or consult a source',
    'rely': 'To trust or need someone or something for support',
    'rent': 'Payment for temporary use of property; to pay or charge for such use',
    'sheet': 'A thin flat piece of paper or other material; a bed covering',
    'shock': 'A sudden disturbing feeling; to cause such a feeling',
    'smoke': 'Airborne particles from burning; to inhale and exhale tobacco fumes',
    'spray': 'To scatter liquid in small drops',
    'supply': 'Goods made available; to provide what is needed',
    'sweep': 'To clear dirt with a broom; to move across a wide area',
    'text': 'Written content; a short electronic message',
    'uniform': 'Standard clothing for members of a group; consistent throughout',
    'wave': 'A moving ridge of water; to move back and forth',
    'whether': 'Introduces alternatives or uncertainty about something being so',
    'chemical': 'A substance; relating to the study of matter and its reactions',
    'gender': 'A social or personal identity associated with categories such as men and women',
    'nuclear': 'Relating to the central part of an atom or energy released from it',
    'classical': 'Related to traditional ideas or an established musical tradition',
    'tendency': 'A likelihood of happening or behaving in a certain way',
    'racial': 'Related to groups distinguished by inherited physical appearance',
    'fax': 'A document transmitted over a telephone line as an image',
    'prospective': 'Possible or expected in the future',
    'exceptional': 'Unusually excellent',
    'firework': 'A device producing a bang and colored flashes when lit',
    'introductory': 'Coming before the main event or part',
    'grill': 'A cooking device with heat below a rack',
    'comb': 'To smooth hair by using a toothed tool to remove tangles',
    'bulb': 'A rounded or teardrop-shaped object',
    'amino': 'Relating to the nitrogen-containing group found in protein building blocks',
    'grammatical': 'Relating to rules for forming sentences',
    'work on': 'To try to improve or develop something',
    'argue about': 'To disagree over a subject',
    'believe in': 'To accept the existence or value of something',
    'dream about': 'To experience images of something during sleep',
    'warm': 'To make something moderately hot',
    'hand': 'To pass something directly to someone',
    'dream': 'Images or experiences occurring during sleep',
    '＆': 'Connects words or phrases by addition',
    'ＯＮ': 'In an operating or activated state',
    'ＮＯＲ': 'Boolean operation that is true only when neither input is true',
    'ＭｉＧ': 'A Russian aircraft designation',
    'ＭＰ３': 'A compressed digital audio format',
    '云': '(Classical) to say',
    '大厦': 'A grand building, used in the names of prominent buildings',
    '合并': 'To merge or combine',
    '尽快': 'As quickly or as soon as possible',
    '腮': 'The side of the face below the eye',
    '台风': 'Stage presence or poise',
    '掏': 'To take something out of a pocket or scoop it out',
    '溪': 'A small stream or rivulet',
    '此起彼伏': 'Recurring in succession, with one event beginning as another subsides',
    '기 [2]': 'The opening stage in a four-part structure of a text or poem',
    '전 [4]': 'The decisive turn in the third stage of a four-part text structure',
    '조선': 'A Korean state founded in 1392, with Hanyang as its capital, that lost sovereignty to Japan in 1910',
}


def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFKC', value).casefold() if c.isalnum())


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def split_outside_parens(text, delimiters):
    parts, start, depth = [], 0, 0
    for index, char in enumerate(text):
        if char in '(（[':
            depth += 1
        elif char in ')）]':
            depth = max(0, depth - 1)
        elif char in delimiters and depth == 0:
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def leaks(text, answer):
    answer = unicodedata.normalize('NFKC', answer).strip()
    if not answer:
        return False
    if not normalized(answer):
        return answer in text
    if re.fullmatch(r'[A-Za-z][A-Za-z -]*', answer):
        return bool(re.search(r'(?<![A-Za-z])' + re.escape(answer).replace(r'\ ', r'\s+') + r'(?![A-Za-z])', unicodedata.normalize('NFKC', text), re.I))
    return normalized(answer) in normalized(text)


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = text.replace('**', '').replace('\\', '')
    text = re.sub(r'^\s*\d+[.)]\s*', '', text)
    return re.sub(r'\s+', ' ', text).strip(' ;；。.')


def senses(description, locale):
    # Korean KRdict overlays keep all meanings in their own numbered sections.
    sections = re.findall(r'### 뜻 \d+\s*\n(.*?)(?=\n### |\n---|\Z)', description, re.S)
    if sections:
        return [plain(s.strip().splitlines()[0]) for s in sections]
    block = re.split(r'\n\s*### |\n---', description, maxsplit=1)[0].strip()
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    numbered = [plain(line) for line in lines if re.match(r'^\d+[.)]\s', line)]
    if numbered:
        return numbered
    # A separate prose paragraph can be a caution; the first complete meaning
    # paragraph remains the principal sense rather than an arbitrary first line.
    block = re.split(r'(?:Patterns by sense|Pattern|Usage|意味ごとの文型|用法|文型|各義句型|句型)\s*[:：]', block)[0]
    return [plain(block.split('\n\n')[0])]


def aliases(card, translation, description, language):
    values = [translation['title'], card['title']]
    if language == '일본어':
        # Particle lessons name the actual tested form after the centered dot.
        # A composite lesson title must not conceal leakage of that answer.
        for title in values[:]:
            if '·' in title:
                tested_form = title.rsplit('·', 1)[1].strip()
                if re.fullmatch(r'[ぁ-んァ-ン一-龥]+', tested_form):
                    values.append(tested_form)
        for match in re.finditer(r'^(?:표기|읽기|Spelling|Reading|表記|読み|寫法|讀音)\s*[:：]\s*([^\n]+)', description, re.M):
            variants = [v.strip() for v in re.split(r'\s*/\s*', match.group(1))]
            # A single mora (e.g. 五 can be read い) occurring inside an
            # unrelated word is not an answer-revealing alias occurrence.
            if match.group(0).startswith(('읽기', 'Reading', '読み', '讀音')):
                variants = [v for v in variants if len(v) > 1]
            values.extend(variants)
    elif language == '중국어':
        for match in re.finditer(r'^(?:번체|Traditional form|繁体字|繁體字)\s*[:：]\s*([^\n]+)', description, re.M):
            values.append(match.group(1))
    # Korean source headings sometimes include an entry disambiguator.
    if language == '한국어':
        values.extend(re.sub(r'\s*\[\d+\]\s*', '', v) for v in values[:])
    return sorted({v.strip() for v in values if v.strip()}, key=len, reverse=True)


def choose(definitions, answers):
    def safe(s):
        balanced = all(s.count(left) == s.count(right) for left, right in [('(', ')'), ('（', '）'), ('[', ']')])
        return balanced and 1 <= len(s) <= 160 and not any(leaks(s, answer) for answer in answers) and not re.search(r'https?://|```|^#', s)
    for definition in definitions[:1]:
        # Pinyin + written-headword labels identify a sense; they are not part
        # of the definition and would disclose the answer in a reverse prompt.
        definition = re.sub(r'^[A-Za-zÀ-ž\s]+[（(][^）)]+[）)]\s*[:：]\s*', '', definition)
        definition = re.sub(r'^[\u3400-\u9fff]+\s+[A-Za-zÀ-ž\s]+\s*[:：]\s*', '', definition)
        definition = re.sub(r'^[A-Za-zÀ-ž\s]+\s*[:：]\s*', '', definition)
        for parenthetical in re.findall(r'[（(][^）)]*[）)]', definition):
            if any(leaks(parenthetical, answer) for answer in answers):
                definition = definition.replace(parenthetical, '')
        definition = re.sub(r', such as\b.*', '', definition)
        # Remove an explicit label before its definition, not occurrences from
        # inside the meaning ("An airport: a place ..." -> "a place ...").
        for answer in answers:
            if re.fullmatch(r'[A-Za-z][A-Za-z -]*', answer):
                word = re.escape(answer)
                definition = re.sub(r'^(?:(?:A|An|The|To)\s+)?' + word + r'\s*[:：]\s*', '', definition, flags=re.I)
                definition = re.sub(r'^(To|An?|The)\s+' + word + r'\s+or\s+', r'\1 ', definition, flags=re.I)
                definition = re.sub(r'^(?:An?|The)\s+' + word + r',?\s+(?:including\s+)?(?=(?:an?|the|one|someone|something|who|which)\b)', '', definition, flags=re.I)
                # In these source overlays a bare repeated lemma before a
                # semicolon is a label, not a distinct dictionary meaning.
                definition = re.sub(r'^(?:(?:A|An|The|To)\s+)?' + word + r'\s*;\s*', '', definition, flags=re.I)
            else:
                definition = re.sub(r'^' + re.escape(answer) + r'\s*[:：]\s*', '', definition)
        # Dictionary pronunciation advice can quote the answer. The meaning
        # before it remains a complete clue; the usage stays in the description.
        definition = re.sub(r'[（(](?:丁寧には|공손하게|禮貌說法).*?[）)]', '', definition)
        definition = definition.strip()
        if safe(definition):
            return definition
        sentence = re.split(r'(?<=[。.!?])\s*', definition)[0]
        if safe(plain(sentence)):
            return plain(sentence)
        # Choose a whole source sense/synonym separated by a dictionary delimiter.
        # No character truncation, generated ellipsis, or blank placeholder.
        chunks = [plain(split_outside_parens(definition, ';；')[0])]
        for chunk in chunks:
            if safe(chunk):
                return chunk
        # Comma-separated dictionary synonyms can supply a non-circular clue.
        # Do not split complete explanatory English clauses at commas.
        if len(chunks[0]) <= 80 and not re.search(r'\b(?:which|that|when|where|such as)\b', chunks[0]):
            prefix_match = re.match(r'^(?:\([^)]*\)|（[^）]*）)\s*', chunks[0])
            prefix = prefix_match.group(0) if prefix_match else ''
            for chunk in split_outside_parens(chunks[0], '、，,'):
                chunk = plain(chunk)
                if prefix and not chunk.startswith(prefix.strip()):
                    chunk = prefix + chunk
                if safe(chunk) and len(chunk) >= 2:
                    return chunk
    return None


def load_inputs(data_dir):
    collections_dir = data_dir / 'collections' if (data_dir / 'collections').is_dir() else data_dir
    paths = sorted(collections_dir.glob('*/collection.json'))
    if not paths:
        raise ValueError('Expected the public repository root or its collections directory')
    languages = {'en': '영어', 'ja': '일본어', 'zh': '중국어', 'ko': '한국어', 'hanja': '한자'}
    manifest, canonical, overlays = [], {}, {}
    for path in paths:
        slug = path.parent.name
        language = languages.get(slug.split('-')[0])
        if language is None:
            continue
        pack = json.loads(path.read_text())
        collection = {'id': pack['collectionId'], 'file': slug, 'language': language}
        manifest.append(collection)
        canonical[slug] = pack
        overlays[slug] = {'cards': {
            card['cardId']: {'localization': {'translations': {
                locale: {'title': value.get('title', card['title']), **value}
                for locale, value in card['localization']['translations'].items()
            }}}
            for card in pack['cards']
        }}
    if len(manifest) != 38:
        raise ValueError(f'Expected 38 public language/hanja collections, found {len(manifest)}')
    return manifest, canonical, overlays


def run(data_dir, output):
    output.mkdir(parents=True, exist_ok=True)
    issues = []
    overrides = {}
    override_dir = ROOT / 'editorial/summary-overrides'
    if override_dir.exists():
        for path in sorted(override_dir.glob('*.json')):
            for key, locales in json.loads(path.read_text()).items():
                overrides.setdefault(key, {}).update(locales)
    total = authored = complete = 0
    records = []
    packs = {}
    manifest, canonical_inputs, overlay_inputs = load_inputs(data_dir)
    # The same Korean word may already have a fuller four-language dictionary
    # definition. Match its actual Korean lemma, not a loose English homonym.
    korean_dictionary = {}
    for collection in manifest:
        if collection['language'] != '한국어':
            continue
        canonical = canonical_inputs[collection['file']]
        overlay = overlay_inputs[collection['file']]
        for card in canonical['cards']:
            lemma = re.sub(r'\s*\[\d+\]', '', card['title'])
            first_gloss = re.search(r'^English:\s*(.+)', card['description'], re.M)
            labels = {normalized(s.removeprefix('to ')) for s in first_gloss.group(1).split(';')} if first_gloss else set()
            korean_dictionary.setdefault(lemma, []).append((overlay['cards'][card['cardId']]['localization']['translations'], labels))
    for collection in manifest:
        if collection['language'] not in LANGUAGES:
            continue
        slug = collection['file']
        canonical = canonical_inputs[slug]
        overlay = overlay_inputs[slug]
        cards = {}
        for card in canonical['cards']:
            cid = card['cardId']
            values = {}
            translations = overlay['cards'][cid]['localization']['translations']
            english_definitions = senses(translations['en-US']['description'], 'en-US')
            selected_sense = 0
            # Dictionary ordering can put spelling cross-references or a
            # surname before the ordinary HSK meaning. Pick that meaning once
            # using the English source, and align the choice across locales.
            metadata = r'\b(?:variant|surname|family name|used in|abbreviation (?:for|of))\b|(?:^|:\s*)see\b'
            if collection['language'] == '중국어':
                metadata += r'|\b(?:district|county|prefecture|province|township|city)\b'
            if re.search(metadata, english_definitions[0], re.I):
                for index, definition in enumerate(english_definitions[1:], 1):
                    if not re.search(metadata, definition, re.I):
                        selected_sense = index
                        break
            for locale in LOCALES:
                total += 1
                translated = overlay['cards'][cid]['localization']['translations'].get(locale)
                if not translated:
                    issues.append({'collection': slug, 'cardId': cid, 'locale': locale, 'problem': 'missing translation'})
                    continue
                definitions = senses(translated['description'], locale)
                if selected_sense and len(definitions) == len(english_definitions):
                    definitions = definitions[selected_sense:selected_sense + 1]
                if collection['language'] == '한자' and locale == 'ko':
                    # The final syllable in libhangul's 음훈 is the answer's
                    # pronunciation, not part of its conceptual meaning.
                    meaning = definitions[0].rsplit(' ', 1)[0]
                    english = {normalized(s.removeprefix('to ')) for s in senses(translations['en-US']['description'], 'en-US')[:1]}
                    candidates = [meaning, meaning + '다']
                    if meaning.endswith('을'):
                        candidates.append(meaning[:-1] + '다')
                    elif meaning and 0xAC00 <= ord(meaning[-1]) <= 0xD7A3 and (ord(meaning[-1]) - 0xAC00) % 28 == 8:
                        candidates.append(meaning[:-1] + chr(ord(meaning[-1]) - 8) + '다')
                    for candidate in candidates:
                        if any(english.intersection(labels) for _, labels in korean_dictionary.get(candidate, [])):
                            meaning = candidate
                            break
                    definitions = [meaning]
                answers = aliases(card, translated, translated['description'], collection['language'])
                value = choose(definitions, answers)
                if value is None and locale == 'en-US' and translated['title'] in ENGLISH:
                    value = choose([ENGLISH[translated['title']]], answers)
                if value is None and collection['language'] == '한자':
                    korean_meaning = plain(card['description'].split('\n')[0]).rsplit(' ', 1)[0]
                    lemma = korean_meaning
                    if lemma.endswith('을'):
                        lemma = lemma[:-1] + '다'
                    elif lemma and 0xAC00 <= ord(lemma[-1]) <= 0xD7A3 and (ord(lemma[-1]) - 0xAC00) % 28 == 8:
                        lemma = lemma[:-1] + chr(ord(lemma[-1]) - 8) + '다'
                    english_meanings = {normalized(s.removeprefix('to ')) for s in senses(overlay['cards'][cid]['localization']['translations']['en-US']['description'], 'en-US')[:1]}
                    for equivalent, labels in korean_dictionary.get(lemma, []):
                        # Korean homographs are separate dictionary entries:
                        # e.g. 모 can mean a square/corner or "some". Require
                        # an independently matching English sense as well.
                        if not english_meanings.intersection(labels):
                            continue
                        # Principal dictionary meaning only: later homonymous
                        # senses are not evidence for the character's meaning.
                        value = choose(senses(equivalent[locale]['description'], locale)[:1], answers)
                        if value is not None:
                            break
                override = overrides.get(f'{collection["id"]}::{cid}', {}).get(locale)
                if override is not None:
                    value = override.strip()
                    if not 1 <= len(value) <= 160 or '\n' in value or any(leaks(value, answer) for answer in answers):
                        value = None
                if value is None:
                    issues.append({'collection': slug, 'cardId': cid, 'locale': locale, 'title': translated['title'], 'aliases': answers, 'definitions': definitions, 'invalidOverride': override if override is not None else None, 'problem': 'no complete non-circular principal sense <=160'})
                else:
                    values[locale] = value
                    authored += 1
            cards[cid] = values
            records.append((collection, card, translations, values))
            complete += len(values) == 4
        packs[collection['id']] = (slug, cards)
        write_json(output / f'{slug}.json', {'collectionId': collection['id'], 'cards': cards})
        print(f'{slug}: {len(cards)} cards; {sum(len(v) for v in cards.values())}/{len(cards)*4} locale clues', flush=True)
    concepts = {}
    for collection, card, translations, values in records:
        keys = [('source', card['title'], card['description'])]
        if values.get('ko') and values.get('en-US'):
            core = lambda s: normalized(re.split(r'[;；,、，]', s)[0].removeprefix('To ').removeprefix('A ').removeprefix('The '))
            for answer in aliases(card, translations['ko'], translations['ko']['description'], collection['language']):
                keys.append(('concept', normalized(answer), core(values['ko']), core(values['en-US'])))
        for key in keys:
            for locale, value in values.items():
                concepts.setdefault((key, locale), set()).add(value)
    reused = 0
    for collection, card, translations, values in records:
        for locale in LOCALES:
            if locale in values or overrides.get(f'{collection["id"]}::{card["cardId"]}', {}).get(locale) is not None:
                continue
            answers = aliases(card, translations[locale], translations[locale]['description'], collection['language'])
            keys = [('source', card['title'], card['description'])]
            if values.get('ko') and values.get('en-US'):
                for answer in answers:
                    keys.append(('concept', normalized(answer), core(values['ko']), core(values['en-US'])))
            for key in keys:
                candidates = concepts.get((key, locale), set())
                # Ambiguous matching meanings are not guessed. Exact source
                # identity or agreement on both English and Korean core clues
                # is required before sharing a written conceptual paraphrase.
                if len(candidates) != 1:
                    continue
                candidate = next(iter(candidates))
                if not any(leaks(candidate, answer) for answer in answers):
                    values[locale] = candidate
                    reused += 1
                    break
    for collection_id, (slug, cards) in packs.items():
        write_json(output / f'{slug}.json', {'collectionId': collection_id, 'cards': cards})
    issues = [issue for issue in issues if issue['locale'] not in packs[f'builtin-{issue["collection"]}'][1][issue['cardId']]]
    authored = sum(len(values) for _, _, _, values in records)
    complete = sum(len(values) == 4 for _, _, _, values in records)
    issue_path = output / 'review/language-summary-issues.json'
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(issue_path, issues)
    print(json.dumps({'localeFields': total, 'authored': authored, 'completeCards': complete, 'reused': reused, 'gaps': len(issues), 'issueFile': str(issue_path)}))


if __name__ == '__main__':
    assert choose(['愛する；傾向がある'], ['愛']) is None
    assert choose(['shēn：深い（字義どおり、または比喩的に）'], ['深']) is None
    assert choose(['（丁寧語）お金、貨幣'], ['お金']) == '（丁寧語）貨幣'
    assert choose(['x' * 161], ['answer']) is None
    assert leaks('A cat', 'a') and not leaks('cat', 'a')
    assert leaks('數字三', '三')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, required=True, help='Public canonical repository root or its collections directory, with */collection.json and inline translations')
    parser.add_argument('--output-dir', type=Path, required=True, help='Explicit staging directory for the 38 proposed summary files; never writes canonical collections')
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)
