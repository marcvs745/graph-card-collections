#!/usr/bin/env python3
"""Author academic quiz clues from existing localized definitions and curated corrections.

Reads the public repository and writes an explicitly selected staging directory. The explicit corrections include the
reviewed Korean samples, existing art observations, and source-backed music and
artist identities. This is not an independent fact or media verification claim.
"""
import argparse,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCALES=('ko','en-US','ja','zh-TW')
EXCLUDED={'영어','일본어','중국어','한국어','한자'}
def plain(s):
 s=re.sub(r'```.*?```','',s,flags=re.S)
 s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
 return re.sub(r'\s+',' ',s.replace('**','').replace('`','')).strip()
def normalized(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
def paragraphs(d):
 d=re.sub(r'```.*?```','',d,flags=re.S)
 return [plain(p) for p in d.split('\n\n') if p.strip() and not p.lstrip().startswith(('#','- ','[')) and not re.search(r'https?://',p)]
def sentences(s):return re.split(r'(?<=[。！？])|(?<=다\.)\s+|(?<=요\.)\s+|(?<=[.!?])\s+(?=[A-Z「“0-9])',s)
def remove_subject(s,t,locale):
 terms=[t]+re.split(r'\s+(?:and|or|vs\.?|versus)\s+|와 |과 |및 |·|と|與|和|及|、|／| / ',t,flags=re.I)
 terms=sorted({x.strip() for x in terms if len(normalized(x))>1},key=len,reverse=True)
 for term in terms:
  esc=r"\s*".join(map(re.escape,term.split()))
  if locale=="en-US" and term.lower().endswith("s") and len(term)>4:esc=re.escape(term[:-1])+"s?"
  if locale=='en-US':
   verbs=r'is|are|means?|refers? to|describes?|states? that|says? that|measures?|represents?|expresses?|denotes?|compares?|studies|contains?'
   s=re.sub(r'^(?:[A-Za-z-]+\s+){0,2}'+esc+r'(?:s)?\s+(?:'+verbs+r')\s+', '',s,flags=re.I)
   s=re.sub(r'(?<=[;,.])\s*(?:an? |the |its )?'+esc+r'(?:s)?\s+(?:is|are|contains?)\s+', ' ',s,flags=re.I)
  elif locale=='ko':
   s=re.sub(r'^.{0,7}?'+esc+r'(?:이란|란|은|는|이|가)\s*','',s)
   s=re.sub(r'(?<=[,.])\s*'+esc+r'(?:은|는|이|가)\s*',' ',s)
  elif locale=='ja':
   s=re.sub(r'^.{0,7}?'+esc+r'(?:では|とは|は|が)[、\s]*','',s)
   s=re.sub(r'(?<=[、。])\s*'+esc+r'(?:とは|は|が)[、\s]*','',s)
  else:
   s=re.sub(r'^.{0,6}?'+esc+r'(?:是指|指的是|是|指|：|為|以)\s*','',s)
   s=re.sub(r'(?<=[；;。])\s*'+esc+r'(?:是|指|為|則是)\s*','',s)
 s=re.sub(r'\s+',' ',s).strip(' ,;，；、')
 return s

def clean_remaining_name(s,t,locale):
 # Names at the head of a localized definition become their predicates, not answer labels.
 esc=r"\s*".join(map(re.escape,t.split()))
 if locale=='en-US':
  base=t[:-1] if len(t)>4 and t.lower().endswith('s') else t
  pat=r"\s*".join(map(re.escape,base.split()))+('s?' if base!=t else '')
  m=re.match(r'^(?:The |An? |One )?'+pat+r'\b\s+(.+)$',s,re.I)
  if m:
   rest=m[1]
   changes={'occurs when':'A phenomenon in which','occurs':'An occurrence that','changes':'Changes to','isolates':'Isolation of','govern':'Factors governing','shares':'Sharing','involves':'Involving','track':'Tracking','assigns':'Assignment of','uses':'Use of','depends on':'Dependence on','gives':'A description giving','act':'Interactions acting','divides':'Division of','approximates':'An approximation of','relates':'A relation connecting','provides':'Provision of','converts':'Conversion of','equals':'A value equal to','include':'Including','belong to':'Belonging to','reads':'Reading','forms':'Formation of','builds':'Building','maintains':'Maintaining','acquires':'Acquisition of','transforms':'Transformation of','holds':'Holding','groups':'Grouping','encodes':'Encoding','comprises':'Comprising','concerns':'Concerning','stores':'Storage of','supports':'Support for','accesses':'Accessing','judges':'Judging','mixes':'Mixing','follows':'Following','makes':'Making','applies':'Applying','generates':'Generation of','draws':'Drawing','favors':'Favoring','monitors':'Monitoring','distinguish':'Distinguishing','examines':'Examination of','develops':'Development of','proposes that':'The proposal that','specifies':'A specification of','reduces':'Reduction of','selects':'Selection of','adapts':'Adaptation of','summarize':'A summary of','can':'Can','includes':'Including','counts':'A count of','lie':'A region lying','occupy':'A region occupying','records':'A record of','sets':'Setting','represents':'Representation of','describe':'Describing','describes':'Describing','require':'Requiring','requires':'Requiring','refer to':'Referring to','emphasizes':'Emphasis on','emphasize':'Emphasis on','explain':'An explanation of','explains':'An explanation of','studies':'Study of'}
   for verb,replacement in sorted(changes.items(),key=lambda x:-len(x[0])):
    if re.match(re.escape(verb)+r'\b',rest,re.I):rest=re.sub('^'+re.escape(verb),replacement,rest,count=1,flags=re.I);break
   s=rest
  # Repeated names later in a definition refer back to its already described subject.
  s=re.sub(r'\b'+pat+r'\b','this quantity' if any(w in t.lower() for w in ['rate','number','frequency','energy','speed','factor']) else 'this process',s,flags=re.I)
 elif locale=='ko':
  s=re.sub(r'^'+esc+r'(?:에서(?:는)?|에는|으로는|에서는)\s*','',s)
  s=re.sub(r'(?:이것을 |이를 )?'+esc+r'(?:이라고|라고|이라|라) (?:한다|합니다|부른다|부릅니다)[.]?$','',s)
  s=re.sub(esc+r'(?:은|는|이|가)\s*','',s)
 elif locale=='ja':
  s=re.sub(r'^'+esc+r'(?:では|には|の)?','',s)
  s=re.sub(esc+r'(?:は|が|を|の)',{'': ''}.get('',''),s)
 else:
  s=re.sub(r'^'+esc+r'(?:是指|指的是|表示|描述|是|指|的|為)?','',s)
 return re.sub(r'\s+',' ',s).strip(' ,;，；、')
def section_text(d,labels):
 for label in labels:
  m=re.search(r'^### '+re.escape(label)+r'\s*\n(.*?)(?=^### |\Z)',d,re.M|re.S)
  if m:return m[1]
 return ''
def derive(d,t,locale,card_id):
 if card_id.startswith('quotes-'):
  d=section_text(d,['맥락','Context','文脈','脈絡']) or d
 ps=paragraphs(d)
 if '-met-' in card_id:
  # Metadata is not a description of an artwork's distinctive content.
  if ps and re.search(r'제작 연대:|Dated|制作年代|年代：',ps[0]):ps=ps[1:]
 if '-artist-' in card_id:return ''
 if not card_id.startswith(('quotes-','music-')) and '-met-' not in card_id:
  bold=re.match(r'\*\*(.*?)\*\*',d,re.S)
  if bold:
   raw=sentences(plain(bold[1]))[0]
   return clean_remaining_name(remove_subject(raw,t,locale),t,locale)
 ps=[p for p in ps if len(p)>10 and normalized(p)!=normalized(t)]
 for p in ps:
  ss=sentences(p)
  for raw in ss:
   if re.search(r'제작 연대:|Dated|制作年代|年代：| · |표면은|正面是|表面は|front.*translat',raw,re.I):continue
   if '-met-' in card_id and re.search(r'하자[.。]?$|보자[.。]?$|세요[.。]?$|^(?:Follow|Compare|Count|Trace|Look|Start|Move|Notice|Read|Watch|Think)|よう[。]?$|比べ|見よう|^(?:先|沿著|比較|觀察|試想|追蹤)',raw,re.I):continue
   if '?' in raw or '？' in raw:continue
   s=remove_subject(raw,t,locale)
   if normalized(t) and normalized(t) in normalized(s) and ';' in s:s=s.split(';')[0].strip()
   if 8<=len(s)<=160 and not (len(normalized(t))>2 and normalized(t) in normalized(s)):
    return s
 return ''
def main(public_root, out):
 manifest=[{'id':json.loads(p.read_text())['collectionId'],'file':p.parent.name,'language':'academic'} for p in sorted((public_root/'collections').glob('*/collection.json')) if not p.parent.name.startswith(('en-','ja-','zh-','ko-','hanja-'))]
 assert len(manifest)==170
 out.mkdir(parents=True,exist_ok=True)
 flags=[];count=0
 final_overrides={}
 for final_path in sorted((ROOT/'editorial/summary-overrides').glob('academic-*-review.json')):
  for key, values in json.loads(final_path.read_text()).items():
   final_overrides.setdefault(key,{}).update(values)
 overrides = json.loads((ROOT/'editorial/academic-summary-corrections.json').read_text())
 for m in manifest:
  if m['language'] in EXCLUDED:continue
  data=json.loads((public_root/'collections'/m['file']/'collection.json').read_text())
  cards={}
  for c in data['cards']:
   loc=c['localization']['translations'];values={}
   for lang in LOCALES:
    v=loc[lang];s=overrides.get(c['cardId'],{}).get(lang) or derive(v['description'],v.get('title',c['title']),lang,c['cardId'])
    s=final_overrides.get(data['collectionId']+'::'+c['cardId'],{}).get(lang,s)
    if not s:flags.append({'file':m['file'],'cardId':c['cardId'],'locale':lang,'title':v.get('title',c['title']),'description':v['description']})
    values[lang]=s
   cards[c['cardId']]=values;count+=1
  (out/f"{m['file']}.json").write_text(json.dumps({'collectionId':m['id'],'cards':cards},ensure_ascii=False,indent=2)+'\n')
 (out/'review').mkdir(parents=True,exist_ok=True)
 (out/'review/academic-summary-flags.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2))
 print(f'{count} cards; {len(flags)} unresolved localized clues')
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--data-dir',type=Path,required=True,help='Public graph-card-collections checkout')
 parser.add_argument('--output-dir',type=Path,required=True,help='Temporary editorial staging directory')
 args=parser.parse_args()
 main(args.data_dir,args.output_dir)
