---
type: reference
title: "언어 요약의 개념 풀이 보강 근거"
description: "2026-11-08 순환 정의를 고칠 때 확인한 기관 자료와 대표 뜻 선택."
---

# 순환 정의와 대표 뜻

요약은 표제어·음역을 지운 퀴즈 단서다. 사전 본문에서 뜻이 아닌 표기·발음·참조 주석을 제거하고 완전한 대표 뜻을 고른다. 여러 뜻 중 나중 뜻으로 이동해서 정답 누설만 피하지 않는다. HSK에서는 사전 순서상 먼저 오는 성씨·이형·지명보다 실제 본문에 있는 일반 어휘 뜻을 네 언어에서 함께 선택한다.

`author-language-summaries.py`는 본문을 바꾸지 않는다. 부족한 정의는 `overrides/`의 카드 ID별 문안으로 보강한다. 영어·한국어 뜻과 정답 글자가 함께 일치하거나 원본 카드 본문이 정확히 같을 때만 작성한 개념 문안을 다른 컬렉션에 재사용한다. 동형어를 표제어 하나만으로 연결하지 않는다. 해소하지 못한 항목은 `/tmp/graph-card-review/language-summary-issues.json`에 실제 원뜻과 ID를 기록한다.

## 기관에서 확인한 추가 식별 단서

- 적송의 붉은 갈색 수피와 일본 등 동아시아 분포: [일본 산림종합연구소](https://www.ffpri.go.jp/kys/business/jumokuen/jumoku/zukan/akamatu.html).
- 칡류의 덩이뿌리와 전분 이용: [Kew, Pueraria 속 설명](https://powo.science.kew.org/taxon/urn%3Alsid%3Aipni.org%3Anames%3A23394-1/general-information), [Pueraria montana 종](https://powo.science.kew.org/taxon/516708-1).
- 동백의 상록성·광택 있는 잎·겨울과 봄 개화: [일본 산림종합연구소 잎 설명](https://www.ffpri.go.jp/labs/mebaezukan/yabutubaki.html), [꽃과 개화기](https://www.ffpri.go.jp/skk/kenkyushokai/sikokudoshokubutu/yabutubaki.html).
- 백합류의 구근과 여섯 꽃덮이 조각: [Flora of Pakistan / eFloras](https://www.efloras.org/florataxon.aspx?flora_id=5&taxon_id=118558).
- 구라시키의 오카야마현 남부 위치: [구라시키시](https://www.city.kurashiki.okayama.jp/culture/global/1005171/1005264/1005378/1011014.html).
- 시마네의 일본 서부·동해 쪽 위치: [시마네현 영문 소개](https://www.pref.shimane.lg.jp/industry/enterprise/shien/kaigai/products/english/index.data/products_en.pdf).
- 기후의 일본 중앙 내륙 위치: [기후현](https://www.pref.gifu.lg.jp/uploaded/attachment/411121.pdf).
- 교토의 794년 도읍 설치: [교토시](https://www.city.kyoto.lg.jp/sogo/page/0000305427.html).
- 야마가타의 일본 동북부·동해 쪽 위치: [야마가타현](https://www.pref.yamagata.jp/documents/8094/welcome_to_yamagata_pamphlet.pdf).
- 광저우의 광둥성 성도·주장강 삼각주 위치: [광저우 외사 자료](https://www.gzfao.gov.cn/attachment/0/0/47/82.pdf), [홍콩 정부의 지역 소개](https://www.bayarea.gov.hk/en/about/guangzhou.html).
- 광둥의 중국 남부·홍콩 인접 위치: [광둥 외사부](https://en.gdfao.gov.cn/aboutguangdong.html), [홍콩 정부의 대만구 개요](https://www.bayarea.gov.hk/en/about/overview.html).
- 태극권의 이완된 원형 동작과 호흡 조절: [UNESCO 등재 신청 자료](https://ich.unesco.org/doc/src/43832.pdf).

위 근거는 요약의 식별 단서를 위한 확인이다. 전체 사전·번역의 독립 의미 검수나 미디어 검수를 뜻하지 않는다.

## Cyclic Chinese definitions

- 囉唆 is an alternative spelling of 囉嗦; the principal meaning is excessive, unceasing speech, supported by the [MOE revised dictionary](https://dict.revised.moe.edu.tw/dictView.jsp?ID=66331).
- 賢惠 is an alternative spelling of 賢慧, traditionally describing a woman as kind and understanding moral duties, supported by the [MOE revised dictionary](https://dict.revised.moe.edu.tw/dictView.jsp?ID=108139&la=1&powerMode=0). The clue preserves the gendered traditional scope rather than asserting a general norm.
- 纪录 resolves the existing cross-reference to 记录 in the same HSK pack. The clue uses the nominal written-account sense; the source explicitly excludes Taiwan interchangeability for the verb sense.
