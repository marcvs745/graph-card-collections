---
type: review
title: "2026-11-08 음악·미술 인물 본문 보완"
description: "미술 인물 137개 설명의 근거와 적용하지 않는 음악 37개 보완안의 검토 이력."
---

# 범위와 보존

최종 적용 범위 정정: 사용자의 “인물 설명만 보완, 나머지 원본 유지” 지시에 따라 실제 설명 변경은 미술 인물 137장만이다. 음악 37장은 인물이 아닌 개념 카드이므로 네 언어 본문을 퍼블릭 원본으로 유지하고, 아래 음악 보완안은 적용하지 않는다. 아래는 저작·검토 과정의 근거 기록이며 전체 원본 대조는 [최종 검증](../tools/verify_editorial.py)을 따른다.

2026-11-08 작성. `music-*.json` 4개 팩의 37개 카드와 `art-*.json` 15개 팩의 `-artist-` 노드 137개(고유 귀속 해시 81개, 표시 이름 82개)를 네 언어로 보완했다. 호쿠사이는 같은 해시에 한국어·영어 이름이 있어 표시 이름 수가 하나 더 많다. 이는 본문 원본 개정이며 전체 컬렉션·요약·배포 완료를 뜻하지 않는다.

음악은 짧은 뜻을 악보 앞에 놓고, 정확한 기존 원리 설명을 유지하면서 음정 비교·따라 부르기·화음의 변한 성부 찾기·박 유지·음계 이동의 연습을 카드별로 연결했다. 반복된 일반 청취 지시를 제거하고 기존 ABC 블록과 합성음 한계, 기본위치·전위 및 조성·기보 조건을 보존했다. 정의만 읽어 청취 능력이 생기거나 특정 화음이 보편적 감정을 만든다고 주장하지 않는다.

미술은 반복된 ‘소장처 작가 표기’ 첫 문단을 실제 인물의 확인 가능한 정체성·시대·활동으로 교체했다. 기존 작품별 관찰·비교·주의·작품 목록은 그대로 보존하고 기관 출처를 덧붙였다. 반복 인물은 해시별로 동일한 네 언어 정체성을 사용했다. 작자 미상 집단·추종자·공방은 실명 인물의 확정 생애로 바꾸지 않았다. 다른 미술 카드 280개의 모든 설명 문자열은 개정 전과 동일하다.

# 출처와 해석의 한계

기존 Met API/공식 페이지·Open Access CSV 캐시의 `artistDisplayBio`, `artistRole`, 접두·접미 귀속, `constituents` 및 작품 설명을 인물별로 확인했다. 아래 표는 실제로 읽은 캐시의 대응 공용 API와 기관 출처다. 공용 API가 응답하지 않는 항목은 함께 제시한 기관 페이지와 당시 캐시 확인 기록을 구분한다. 이전 표본 검토의 기관 인물 자료도 재사용했다. 추가로 공식 웹 페이지 40445·73188·748432·35992·38016·446551·754013·49082·45329·733038·49453·50486을 다시 조회해 희소 인물·역할·연대 문제를 확인했다.

- 이유원은 단순 소유자가 아니라 시·서화에 능한 문신이자 고종 때 영의정을 지낸 인물이다. 김수규는 생애 자료가 적다는 한계를 유지한다.
- 이정의 출생년은 Met 기록 1541년과 이전 표본의 한국 기관 자료 1554년이 달라 새 인물 첫 문장에는 출생년을 쓰지 않았다. 조선 문인 화가라는 확인 범위만 사용한다.
- Pan Yunyu는 Met 활동기 약 15~16세기와 부채 연대 1604년 또는 1664년이 서로 맞지 않는다. 임의로 하나의 생애를 정하지 않고 연대 미확정으로 썼다.
- 고린 추종자의 생몰년을 고린 본인의 1658–1716년으로 쓰지 않는다. 앵그르와 공방의 공동 귀속, 장로·산라쿠·바셀리오스 및 바와니 다스 또는 추종자의 추정도 유지한다.
- Wang Yuan(王緣)은 그림을 그린 화가이고 조지겸은 묘사된 인물·제문 작성자다. 마쓰무라 게이분의 그림과 라이 산요의 뒷면 서예를 구별한다. 『샤나메』의 여러 제작자는 시인 피르다우시 한 사람과 같지 않다.
- 실명·활동 자료가 부족한 화가는 기관에서 확인한 시대·지역·역할까지만 썼다. 확인하지 못한 한자 이름은 새로 만들지 않고 기존 로마자 표기를 유지했다.

음악의 기초 관계는 [Open Music Theory의 음정](https://viva.pressbooks.pub/openmusictheory/chapter/intervals/), [3화음](https://viva.pressbooks.pub/openmusictheory/chapter/triads/), [복합박자](https://viva.pressbooks.pub/openmusictheory/chapter/compound-meters-and-time-signatures/)를 함께 확인했다. 단음계 장은 조회가 차단되어 재확인 완료로 세지 않으며 기존 정확한 네 언어 설명과 악보 조건을 유지했다. 새 문장은 기존 사실을 바탕으로 쓴 독자적 연습 안내이며 외부 교재 문장을 번역·복제하지 않았다.

# 검증과 남은 범위

로컬 비교에서 대상 174개 카드·696개 언어 문자열이 변경되었고, 비대상 미술 280개 카드·1,120개 언어 문자열은 동일했다. 37개 음악 카드의 네 언어 ABC 블록 148개가 정확히 보존됐고 원래 URL도 모두 남았다. 모든 카드 ID·언어 키·컬렉션 ID를 보존했다. 모든 미술 인물의 기존 첫 문단 이후 설명은 부분 문자열로 그대로 유지됨을 확인했다.

이 기록은 텍스트·기보 데이터와 기관 근거의 검토다. 실제 음원 청취·연주 또는 전체 이미지의 새 시각 검수, 독립 번역 감수, 생성 결과·사용자 편집본 보존·배포는 별도 검증 대상이다. 생성과 비대상 최종 결과 검증은 상위 작업이 수행한다.

# 인물별 근거

| 인물·귀속 | 읽은 기관 캐시 | 인물 배경 출처 |
| --- | --- | --- |
| Genga | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/45326) | [기관 자료](https://www.metmuseum.org/art/collection/search/45326) |
| Hu Yuan | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/49454) | [기관 자료](https://www.metmuseum.org/art/collection/search/49454) |
| Kano Tsunenobu | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/74462) | [기관 자료](https://www.metmuseum.org/art/collection/search/74462) |
| Katsushika Hokusai | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/45434) | [기관 자료](https://www.metmuseum.org/art/collection/search/45434) |
| Kawamura Bunpō | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/78584) | [기관 자료](https://www.metmuseum.org/art/collection/search/78584) |
| Lu Kezheng | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/35977) | [기관 자료](https://www.metmuseum.org/art/collection/search/35977) |
| Matsumura Keibun | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/667297) | [기관 자료](https://knmdb.kyohaku.go.jp/eng/7694.html) |
| Miwa Zaiei | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/49082) | [기관 자료](https://www.metmuseum.org/art/collection/search/49082) |
| Nakabayashi Chikutō | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/897136) | [기관 자료](https://www.metmuseum.org/art/collection/search/897136) |
| Pan Yunyu | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/35992) | [기관 자료](https://www.metmuseum.org/art/collection/search/35992) |
| Qi Zhijia | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/35994) | [기관 자료](https://www.metmuseum.org/art/collection/search/35994) |
| Tang Guang | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/754013) | [기관 자료](https://www.metmuseum.org/art/collection/search/754013) |
| Tani Bunchō | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/49003) | [기관 자료](https://www.metmuseum.org/art/collection/search/49003) |
| Thomas Cole | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/10497) | [기관 자료](https://www.metmuseum.org/art/collection/search/10497) |
| Urakami (Uragami) Gyokudō | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/77191) | [기관 자료](https://www.metmuseum.org/art/collection/search/77191) |
| Utagawa Hiroshige | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/36521) | [기관 자료](https://www.metmuseum.org/art/collection/search/36521) |
| Wang Hui | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/36071) | [기관 자료](https://www.metmuseum.org/art/collection/search/36071) |
| Wang Yuan | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/49453) | [기관 자료](https://www.metmuseum.org/art/collection/search/49453) |
| William Merritt Chase | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/10473) | [기관 자료](https://www.metmuseum.org/art/collection/search/10473) |
| Wu Xizai | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/49448) | [기관 자료](https://www.metmuseum.org/art/collection/search/49448) |
| 가노 산라쿠 추정 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/843267) | [기관 자료](https://www.metmuseum.org/art/collection/search/843267) |
| 귀스타브 쿠르베 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436023) | [기관 자료](https://www.metmuseum.org/art/collection/search/436023) |
| 김수규 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/73188) | [기관 자료](https://www.metmuseum.org/art/collection/search/73188) |
| 니콜라 푸생 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437326) | [기관 자료](https://www.metmuseum.org/art/collection/search/437326) |
| 두초 디 부오닌세냐 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438754) | [기관 자료](https://www.metmuseum.org/art/collection/search/438754) |
| 라파엘로 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437372) | [기관 자료](https://www.metmuseum.org/art/collection/search/437372) |
| 렘브란트 판 레인 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437394) | [기관 자료](https://www.metmuseum.org/art/collection/search/437394) |
| 로히어르 판 데르 베이던 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437487) | [기관 자료](https://www.metmuseum.org/art/collection/search/437487) |
| 만디 공방의 화가 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/38016) | [기관 자료](https://www.metmuseum.org/art/collection/search/38016) |
| 바와니 다스 또는 추종자 추정 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/456949) | [기관 자료](https://www.metmuseum.org/art/collection/search/456949) |
| 베르트 모리조 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437159) | [기관 자료](https://www.metmuseum.org/art/collection/search/437159) |
| 브론치노 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435802) | [기관 자료](https://www.metmuseum.org/art/collection/search/435802) |
| 빈센트 반 고흐 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437984) | [기관 자료](https://www.metmuseum.org/art/collection/search/437984) |
| 산드로 보티첼리 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/459016) | [기관 자료](https://www.nationalgallery.org.uk/artists/sandro-botticelli) |
| 성 프란치스코의 화가 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/459046) | [기관 자료](https://www.metmuseum.org/art/collection/search/459046) |
| 시모네 마르티니 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437675) | [기관 자료](https://www.metmuseum.org/essays/italian-painting-of-the-later-middle-ages) |
| 신학권(호: 도암) | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/748432) | [기관 자료](https://www.metmuseum.org/art/collection/search/748432) |
| 안드레아 만테냐 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436966) | [기관 자료](https://www.metmuseum.org/art/collection/search/436966) |
| 알프레드 시슬레 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437683) | [기관 자료](https://www.metmuseum.org/art/collection/search/437683) |
| 앙리 드 툴루즈로트레크 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437835) | [기관 자료](https://www.metmuseum.org/art/collection/search/437835) |
| 앙리 루소 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438822) | [기관 자료](https://www.metmuseum.org/art/collection/search/438822) |
| 앙투안 와토 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437926) | [기관 자료](https://www.metmuseum.org/art/collection/search/437926) |
| 얀 반 에이크 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436282) | [기관 자료](https://www.metmuseum.org/art/collection/search/436282) |
| 에두아르 마네 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436947) | [기관 자료](https://www.metmuseum.org/art/collection/search/436947) |
| 에드가 드가 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438817) | [기관 자료](https://www.metmuseum.org/art/collection/search/438817) |
| 에티오피아 북부 고지대 화가 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/317618) | [기관 자료](https://www.metmuseum.org/art/collection/search/317618) |
| 여러 화가와 제작자 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/446551) | [기관 자료](https://www.metmuseum.org/art/collection/search/446551) |
| 오가타 고린의 추종자 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/45329) | [기관 자료](https://www.metmuseum.org/art/collection/search/45329) |
| 오귀스트 르누아르 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437434) | [기관 자료](https://www.metmuseum.org/art/collection/search/437434) |
| 외젠 들라크루아 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436176) | [기관 자료](https://www.metmuseum.org/art/collection/search/436176) |
| 요하네스 페르메이르 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437881) | [기관 자료](https://www.metmuseum.org/art/collection/search/437881) |
| 이유원 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/40445) | [기관 자료](https://www.metmuseum.org/art/collection/search/40445) |
| 이정(호: 탄은) | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/50486) | [기관 자료](https://www.metmuseum.org/art/collection/search/50486) |
| 자크루이 다비드 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436105) | [기관 자료](https://www.metmuseum.org/art/collection/search/436105) |
| 장로 추정 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/36023) | [기관 자료](https://www.metmuseum.org/art/collection/search/36023) |
| 장오귀스트도미니크 앵그르 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/459106) | [기관 자료](https://www.metmuseum.org/art/collection/search/459106) |
| 장오귀스트도미니크 앵그르와 공방 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436708) | [기관 자료](https://www.metmuseum.org/art/collection/search/436708) |
| 장오노레 프라고나르 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436322) | [기관 자료](https://www.metmuseum.org/art/collection/search/436322) |
| 장프랑수아 밀레 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437098) | [기관 자료](https://www.metmuseum.org/art/collection/search/437098) |
| 조르주 쇠라 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437654) | [기관 자료](https://www.metmuseum.org/art/collection/search/437654) |
| 조반니 바론치오 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/459045) | [기관 자료](https://www.metmuseum.org/art/collection/search/459045) |
| 조반니 벨리니 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435640) | [기관 자료](https://www.metmuseum.org/art/collection/search/435640) |
| 조지프 말로드 윌리엄 터너 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437853) | [기관 자료](https://www.metmuseum.org/art/collection/search/437853) |
| 조토 디 본도네 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436504) | [기관 자료](https://www.metmuseum.org/essays/italian-painting-of-the-later-middle-ages) |
| 지상코뿔새 화가로 알려진 바셀리오스 추정 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/733038) | [기관 자료](https://www.metmuseum.org/art/collection/search/733038) |
| 카미유 코로 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435988) | [기관 자료](https://www.metmuseum.org/art/collection/search/435988) |
| 카미유 피사로 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438738) | [기관 자료](https://www.metmuseum.org/art/collection/search/438738) |
| 카스파르 다비트 프리드리히 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438417) | [기관 자료](https://www.metmuseum.org/art/collection/search/438417) |
| 테오도르 루소 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/438816) | [기관 자료](https://www.metmuseum.org/art/collection/search/438816) |
| 테오도르 제리코 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436455) | [기관 자료](https://www.metmuseum.org/art/collection/search/436455) |
| 티치아노 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437823) | [기관 자료](https://www.metmuseum.org/art/collection/search/437823) |
| 페테르 파울 루벤스 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437535) | [기관 자료](https://www.metmuseum.org/art/collection/search/437535) |
| 페트뤼스 크리스튀스 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435896) | [기관 자료](https://www.metmuseum.org/art/collection/search/435896) |
| 폴 고갱 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436446) | [기관 자료](https://www.metmuseum.org/art/collection/search/436446) |
| 폴 세잔 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435882) | [기관 자료](https://www.metmuseum.org/art/collection/search/435882) |
| 프라 필리포 리피 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436896) | [기관 자료](https://www.metmuseum.org/art/collection/search/436896) |
| 프랑수아 부셰 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435739) | [기관 자료](https://www.metmuseum.org/art/collection/search/435739) |
| 피에트로 로렌체티 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436908) | [기관 자료](https://www.metmuseum.org/art/collection/search/436908) |
| 피터르 브뤼헐(아버지) | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/435809) | [기관 자료](https://www.metmuseum.org/de/essays/pieter-bruegel-the-elder-ca-1525-1569) |
| 한스 멤링 | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/437490) | [기관 자료](https://www.metmuseum.org/art/collection/search/437490) |
| 한스 홀바인(아들) | [공식 기록](https://collectionapi.metmuseum.org/public/collection/v1/objects/436658) | [기관 자료](https://www.metmuseum.org/art/collection/search/436658) |
