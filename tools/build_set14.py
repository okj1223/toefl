from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_14.tsv"


CARDS = [
    ("abolition", "폐지 / 철폐", "제도나 관행을 공식적으로 없앰", "남겨두지 않고 제도를 걷어내는 느낌", "abolition=제도 폐지 / reform=고쳐서 바꿈 / repeal=법을 공식 취소함"),
    ("ancestry", "조상 계통 / 혈통", "가계나 집단의 출신 뿌리", "지금 사람 뒤로 이어진 뿌리를 거슬러 보는 느낌", "ancestry=조상 계통 / heritage=물려받은 유산 / lineage=혈통의 계열"),
    ("antiquity", "고대 / 아주 오래된 시대", "기록상 먼 과거의 시기나 오래됨", "현재와 멀리 떨어진 오래된 시간층", "antiquity=고대·오래됨 / prehistory=문자 기록 이전 / tradition=전해 내려온 관습"),
    ("artifact", "인공 유물", "사람이 만들어 남긴 물건으로 과거를 보여주는 자료", "땅이나 기록 속에서 나온 사람 손의 흔적", "artifact=사람이 만든 유물 / specimen=표본 / relic=과거의 남은 흔적"),
    ("assimilate", "동화되다 / 흡수하다", "새 문화나 정보를 받아들여 기존 체계 안에 섞이다", "낯선 것이 안으로 들어와 점점 하나처럼 섞이는 느낌", "assimilate=흡수해 동화시키다 / integrate=구조 안에 함께 포함시키다 / adapt=환경에 맞춰 조정하다"),
    ("autonomous", "자율적인 / 자치적인", "외부 통제 없이 스스로 결정·운영하는", "밖에서 끌려가기보다 안에서 스스로 움직이는 느낌", "autonomous=자율·자치적인 / independent=의존하지 않는 / sovereign=정치적으로 주권을 가진"),
    ("chronicle", "연대기 / 기록하다", "사건을 시간 순서대로 적은 기록이나 그렇게 남기는 일", "언제 무슨 일이 있었는지 줄 세워 적는 느낌", "chronicle=시간순 기록 / archive=보관 기록물 / narrative=이야기식 서술"),
    ("chronological", "시간 순서의 / 연대순의", "사건을 발생한 순서대로 배열한", "앞뒤 시간을 따라 차례대로 늘어놓는 느낌", "chronological=시간 순서대로 / sequential=순차적으로 / historical=역사와 관련된"),
    ("citizenship", "시민권 / 시민으로서의 자격", "공동체 구성원으로 인정받는 법적·사회적 지위", "그 사회 안의 정식 구성원으로 서 있는 느낌", "citizenship=시민으로서의 자격과 지위 / nationality=국적 / residency=거주 자격"),
    ("civilization", "문명 / 고도화된 사회", "도시·제도·문화가 발달한 큰 사회 체계", "흩어진 삶이 제도와 문화로 커다랗게 짜인 상태", "civilization=발달한 사회·문명 / culture=생활양식과 가치체계 / society=사람들의 조직된 집단"),
    ("clan", "씨족 / 혈연 집단", "조상이나 혈연을 공유한다고 보는 전통적 집단", "가족보다 넓게 한 뿌리로 묶인 무리", "clan=혈연 기반 집단 / tribe=더 넓은 부족 집단 / family=가족 단위"),
    ("colonial", "식민지의 / 식민 지배와 관련된", "한 지역이 다른 권력에 지배·정착 통제되는 체제와 관련된", "밖에서 들어온 권력이 땅과 제도를 누르는 느낌", "colonial=식민 지배와 관련된 / imperial=제국 권력의 / native=토착의"),
    ("conquest", "정복 / 무력 장악", "힘으로 지역이나 집단을 굴복시키고 지배권을 얻는 일", "전쟁과 강압으로 땅과 권력을 가져가는 느낌", "conquest=무력 정복 / occupation=점령 상태 / expansion=영토·영향력 확대"),
    ("consolidate", "공고히 하다 / 통합 강화하다", "흩어진 권력·조직·성과를 더 단단한 하나로 만들다", "여러 조각을 모아 흔들리지 않게 굳히는 느낌", "consolidate=합쳐서 단단히 굳히다 / unify=하나로 묶다 / strengthen=힘을 키우다"),
    ("constitution", "헌법 / 기본 구조", "국가의 핵심 원칙을 정한 법 또는 제도의 기본 짜임", "위에 얹힌 규칙보다 더 바닥의 틀을 잡는 느낌", "constitution=헌법·근본 구조 / law=법 일반 / framework=구조적 틀"),
    ("continuity", "연속성 / 지속적 이어짐", "변화 속에서도 끊기지 않고 이어지는 성질", "중간에 뚝 끊기지 않고 줄이 계속 이어지는 느낌", "continuity=연속성 / persistence=계속 남아 있음 / stability=상태가 크게 흔들리지 않음"),
    ("convention", "관습 / 공식 회의", "오래 굳어진 사회적 방식 또는 정식 모임", "사람들이 으레 그렇게 하는 약속된 방식", "convention=관습·대회 / custom=생활 관습 / conference=발표·논의 중심 회의"),
    ("craftsmanship", "장인 기술 / 정교한 솜씨", "손으로 물건을 잘 만들고 다듬는 숙련된 기술", "대충이 아니라 손끝으로 공들여 만든 완성도", "craftsmanship=장인적 제작 솜씨 / skill=기술 일반 / workmanship=작업 품질"),
    ("cultivate", "경작하다 / 키워 발전시키다", "땅·능력·관계를 돌보며 자라게 하다", "그냥 두지 않고 손을 대며 점점 키우는 느낌", "cultivate=돌보며 기르다 / nurture=성장을 보살피다 / harvest=다 자란 것을 거두다"),
    ("customary", "관습적인 / 보통의", "오랜 습관이나 사회 규범상 흔히 따르는", "특별 규칙보다 원래 늘 그렇게 해온 방식", "customary=관습적으로 으레 하는 / conventional=통상적·관례적인 / habitual=개인의 습관적인"),
    ("declaration", "선언 / 공식 공표", "입장·원칙·독립 등을 분명하게 밝히는 공식 발표", "모호하게 두지 않고 밖으로 분명히 선포하는 느낌", "declaration=공식 선언 / announcement=알림 발표 / statement=입장 진술"),
    ("demographic", "인구 집단의 / 인구통계의", "연령·성별·분포 같은 인구 특성과 관련된", "개인 한 명보다 사람 집단의 구성 패턴을 보는 느낌", "demographic=인구 집단 특성의 / statistical=통계의 / social=사회적"),
    ("descendant", "후손", "어떤 조상이나 집단에서 이어 내려온 사람", "앞선 세대에서 아래로 이어져 내려온 사람", "descendant=후손 / ancestor=조상 / heir=상속자"),
    ("diaspora", "디아스포라 / 흩어진 이주 집단", "원래 고향을 떠나 여러 지역에 퍼져 사는 집단", "하나의 출발지에서 여러 곳으로 흩어진 공동체", "diaspora=고향 밖으로 흩어진 집단 / migration=이주 이동 / exile=추방·망명"),
    ("dynasty", "왕조 / 지배 가문", "같은 가문이 여러 세대에 걸쳐 통치하는 체제", "권력이 한 집안 줄기를 타고 이어지는 느낌", "dynasty=세습 통치 가문·왕조 / monarchy=군주제 / empire=제국"),
    ("egalitarian", "평등주의적인", "지위나 권리 차이를 줄이고 동등성을 중시하는", "위아래를 크게 세우지 않고 같은 선을 보려는 느낌", "egalitarian=평등을 중시하는 / democratic=민주적 절차를 중시하는 / equal=동등한"),
    ("emancipation", "해방 / 속박으로부터의 자유", "억압·예속 상태에서 벗어나게 됨", "묶여 있던 상태에서 끈이 풀리는 느낌", "emancipation=제도적·사회적 해방 / liberation=해방 일반 / independence=독립"),
    ("empire", "제국", "여러 지역이나 민족을 넓게 지배하는 거대한 정치 체계", "중심 권력이 넓은 땅을 크게 거느리는 구조", "empire=광범위한 제국 지배 체제 / kingdom=왕국 / state=국가 일반"),
    ("enduring", "오래 지속되는 / 오래 남는", "시간이 지나도 쉽게 사라지지 않는", "잠깐 반짝이 아니라 오래 버티며 남는 느낌", "enduring=오래 지속되는 / temporary=일시적인 / lasting=지속 효과가 긴"),
    ("ethnic", "민족의 / 종족 집단의", "공유된 출신·언어·문화 정체성과 관련된", "국가 경계보다 사람 집단의 뿌리와 문화 정체성을 보는 느낌", "ethnic=민족 집단의 / national=국가의 / cultural=문화의"),
    ("excavate", "발굴하다 / 파내다", "땅속이나 묻힌 층을 파서 유물·흔적을 드러내다", "덮인 흙을 걷어 아래 숨은 과거를 꺼내는 느낌", "excavate=유물·땅을 발굴하다 / uncover=가려진 것을 드러내다 / dig=파다"),
    ("excavation", "발굴 작업 / 발굴 현장", "묻힌 유물이나 구조를 드러내기 위해 파고 조사하는 일", "땅을 층층이 열어 과거 흔적을 찾는 작업", "excavation=고고학적 발굴 작업 / survey=사전 조사 / exploration=탐사"),
    ("feudal", "봉건제의", "토지·신분·충성 관계로 권력이 짜인 과거 사회 체제와 관련된", "땅과 신분이 위아래로 묶인 오래된 권력 구조", "feudal=봉건적 체제의 / aristocratic=귀족 중심의 / hierarchical=위계적인"),
    ("folklore", "민속 전승 / 구전 설화", "한 집단 안에서 전해지는 이야기·믿음·관습", "책보다 입과 생활 속으로 이어진 옛이야기", "folklore=민속 전승·설화 / mythology=신화 체계 / legend=전설"),
    ("frontier", "변경 지역 / 미개척 경계", "정착지·지식·영향력이 막 넓어지는 가장자리", "이미 익숙한 영역의 끝, 바깥으로 열리는 경계선", "frontier=확장되는 경계·변경 / border=경계선 / boundary=범위의 한계선"),
    ("genealogy", "계보 / 족보 연구", "가문과 조상 관계를 따라 정리한 계통", "누가 누구에게서 이어졌는지 가지를 그려 보는 느낌", "genealogy=가계 계보 / ancestry=조상 계통 / history=과거 기록 일반"),
    ("governance", "통치 방식 / 운영 체계", "권한과 규칙으로 조직이나 사회를 운영하는 방식", "누가 어떤 원칙으로 굴리는지 짜인 운영 구조", "governance=통치·운영 체계 / government=정부 조직 / administration=행정 집행"),
    ("hierarchy", "위계 / 서열 구조", "지위와 권한이 층층이 나뉘어 배열된 구조", "평평하지 않고 계단처럼 위아래가 갈린 느낌", "hierarchy=위계 구조 / ranking=순위 배열 / class=사회적 계층"),
    ("historian", "역사가 / 역사 연구자", "과거 자료를 해석하고 서술하는 전문가", "남은 기록을 읽어 과거 이야기를 다시 짜는 사람", "historian=역사를 연구·서술하는 사람 / archaeologist=유물을 발굴해 과거를 연구하는 사람 / chronicler=사건을 기록하는 사람"),
    ("immigrant", "이민자 / 이주해 온 사람", "다른 나라나 지역으로 옮겨 와 정착한 사람", "고향을 떠나 새 사회 안으로 들어온 사람", "immigrant=들어와 정착한 이민자 / migrant=이동하는 사람 일반 / refugee=피난 온 난민"),
    ("indigenous", "토착의 / 원주민의", "어떤 지역에 원래부터 뿌리를 둔 사람·문화·생물과 관련된", "밖에서 들어온 게 아니라 그 땅에서 원래 이어진 느낌", "indigenous=토착의·원주민의 / native=본래 그곳의 / local=그 지역의"),
    ("inheritance", "상속 / 물려받은 것", "재산·권리·특성·문화가 앞세대에서 뒤세대로 넘어오는 것", "앞사람이 남긴 것이 내 쪽으로 이어져 들어오는 느낌", "inheritance=물려받은 재산·특성 / heritage=문화적 유산 / legacy=뒤에 남긴 영향"),
    ("inscription", "새겨진 글 / 비문", "돌·금속·기념물 등에 새긴 문자 기록", "종이 대신 단단한 표면에 남긴 오래가는 글", "inscription=새겨진 문구·비문 / manuscript=손으로 쓴 원고 / record=기록 일반"),
    ("institution", "제도 / 기관", "사회가 지속되도록 자리 잡은 공식 조직이나 규칙 체계", "개인 선택을 넘어 사회 안에 굳어진 틀", "institution=사회적 제도·기관 / organization=조직체 / custom=관습"),
    ("insurrection", "봉기 / 반란", "기존 권력에 맞서 집단이 무력이나 강하게 들고일어남", "아래에서 위 권력에 확 치고 올라가는 저항", "insurrection=권력에 맞선 봉기 / rebellion=반란 일반 / protest=항의 행동"),
    ("intergenerational", "세대 간의", "서로 다른 세대 사이에서 일어나거나 이어지는", "한 세대 안이 아니라 부모·자녀 세대를 가로지르는 느낌", "intergenerational=세대 간의 / historical=역사적 / familial=가족의"),
    ("interpretation", "해석 / 의미 풀이", "자료나 사건의 뜻을 읽어내는 방식", "같은 사실을 두고 어떤 의미로 볼지 틀을 씌우는 느낌", "interpretation=의미를 읽는 해석 / explanation=원인을 풀어 설명함 / translation=언어를 옮김"),
    ("kingdom", "왕국", "왕이나 여왕이 다스리는 국가나 영역", "한 군주의 통치 아래 묶인 정치 공간", "kingdom=군주가 다스리는 왕국 / empire=여러 지역을 거느린 제국 / state=국가 일반"),
    ("landmark", "획기적 사건 / 지표가 되는 기준점", "역사나 변화 과정에서 방향을 바꾼 중요한 지점", "여기서부터 흐름이 달라졌다고 찍히는 표지", "landmark=중요한 전환점·기준물 / milestone=진행 중 주요 단계 / turning point=결정적 전환점"),
    ("legacy", "유산 / 남긴 영향", "앞선 시대나 사람이 뒤에 남긴 오래 가는 흔적과 영향", "지나간 뒤에도 계속 뒤따라 남는 자취", "legacy=뒤에 남긴 영향·유산 / heritage=문화적으로 물려받은 유산 / inheritance=직접 물려받은 것"),
    ("lineage", "혈통 / 계통", "조상에서 후손으로 이어지는 가계나 계열", "한 줄기로 이어진 뿌리의 선", "lineage=혈통의 계열 / ancestry=조상 뿌리 / dynasty=통치 가문의 계승"),
    ("manor", "장원 / 영지의 중심 거주지", "봉건 사회에서 토지와 주변 노동이 묶인 대규모 농장·저택", "한 지역의 땅과 지배가 큰 저택을 중심으로 묶인 느낌", "manor=장원·영주 저택 / estate=큰 토지 재산 / village=마을"),
    ("maritime", "해상의 / 바다와 관련된", "무역·이동·권력이 바다를 통해 이루어지는 것과 관련된", "육지가 아니라 바닷길을 따라 움직이는 느낌", "maritime=바다·해상 활동의 / naval=해군의 / coastal=해안의"),
    ("merchant", "상인 / 무역상", "상품을 사고팔며 유통과 교역을 맡는 사람", "물건을 이동시키며 이익을 만드는 거래자", "merchant=교역·판매를 하는 상인 / trader=사고파는 거래자 / artisan=직접 만드는 장인"),
    ("metropolitan", "대도시의 / 중심 도시권의", "인구와 제도가 집중된 큰 도시와 그 영향권에 속한", "작은 지방보다 중심 대도시의 규모와 밀도를 가진 느낌", "metropolitan=대도시권의 / urban=도시의 / provincial=지방의"),
    ("migration", "이주 / 이동", "사람이나 집단이 다른 지역으로 옮겨 가는 흐름", "한 곳에 고정되지 않고 삶의 터를 옮겨가는 움직임", "migration=집단적 이동·이주 / immigration=들어오는 이민 / relocation=거처·위치를 옮김"),
    ("monarchy", "군주제", "왕이나 여왕이 국가 원수로 있는 통치 체제", "정치 권력의 꼭대기에 왕이 놓인 구조", "monarchy=군주제 / democracy=민주제 / dictatorship=독재 체제"),
    ("monument", "기념물 / 역사적 구조물", "사건·인물·시대를 기념하거나 보여주는 큰 건축물·조형물", "과거를 잊지 말라고 돌과 형태로 세워둔 흔적", "monument=기념 구조물 / memorial=추모 목적의 기념물 / statue=조각상"),
    ("multicultural", "다문화의", "여러 문화 집단이 함께 존재하거나 상호작용하는", "한 색이 아니라 여러 문화가 같이 놓인 느낌", "multicultural=여러 문화가 공존하는 / diverse=다양한 / cosmopolitan=여러 문화에 열린 도시적"),
    ("mythology", "신화 체계 / 신화학", "한 문화가 전해 온 신과 세계 설명 이야기들의 집합", "개별 옛이야기보다 신들의 세계관이 짜인 큰 묶음", "mythology=신화 체계 / folklore=민간 전승 / legend=전설"),
    ("nationalism", "민족주의 / 국가주의", "국가나 민족 공동체에 강한 소속과 우선성을 두는 이념", "우리 집단의 정체성과 이익을 앞세우는 힘", "nationalism=국가·민족 중심 이념 / patriotism=애국심 / identity=정체성"),
    ("nomadic", "유목의 / 이동 생활을 하는", "한곳에 정착하지 않고 이동하며 사는 방식과 관련된", "집과 생계가 고정되지 않고 따라 움직이는 느낌", "nomadic=이동 생활의 / sedentary=정착 생활의 / migratory=계절적·주기적으로 이동하는"),
    ("oral", "구두의 / 말로 전해지는", "글이 아니라 말이나 입으로 전달되는", "종이에 적기보다 입에서 입으로 흐르는 느낌", "oral=구두의·말로 하는 / written=문서로 된 / verbal=말의"),
    ("patronage", "후원 / 비호", "권력자나 부유층이 예술·학문·사람을 지원하며 보호하는 관계", "힘 있는 쪽이 뒤에서 밀어주고 감싸는 느낌", "patronage=권력·재정적 후원 관계 / sponsorship=행사·활동 후원 / protection=보호"),
    ("peasant", "농민 / 소작민", "역사적으로 땅을 경작하며 낮은 신분·경제 위치에 놓인 사람", "사회 아래쪽에서 땅을 일구며 살아가는 사람", "peasant=역사적 맥락의 농민·소작민 / farmer=농업 종사자 일반 / serf=봉건적 예속 농민"),
    ("pilgrimage", "순례 / 성지 방문", "종교적·상징적 의미를 따라 특정 장소로 가는 긴 방문", "단순 관광이 아니라 뜻을 따라 길을 떠나는 느낌", "pilgrimage=종교·상징적 순례 / journey=여행·여정 일반 / expedition=목적을 둔 탐사"),
    ("preservation", "보존 / 보호 유지", "유물·건물·기록·환경이 훼손되지 않도록 지키는 일", "시간이 지나도 망가지지 않게 붙잡아 두는 느낌", "preservation=원형을 지키는 보존 / conservation=자원·유산을 아끼며 관리 / restoration=손상된 것을 복원"),
    ("prosperity", "번영 / 경제적·사회적 풍요", "사회나 집단이 안정적으로 잘살고 성장하는 상태", "살림과 사회가 넉넉하게 커지는 느낌", "prosperity=풍요로운 번영 / wealth=재산·부 / growth=성장"),
    ("reconstruction", "재건 / 복원적 재구성", "무너진 제도·건물·역사상을 다시 세우거나 자료로 다시 짜는 일", "흩어진 조각을 모아 다시 형태를 세우는 느낌", "reconstruction=다시 세우거나 재구성함 / restoration=원래 상태에 가깝게 복원함 / renovation=낡은 것을 새로 고침"),
    ("refugee", "난민 / 피난민", "전쟁·박해·재난을 피해 떠난 사람", "살던 곳을 떠날 수밖에 없어 보호를 찾아 움직이는 사람", "refugee=위험을 피해 온 난민 / immigrant=정착 목적 이민자 / exile=추방되거나 망명한 상태"),
    ("relic", "유물 / 남은 흔적", "과거 시대·사람·관습에서 지금까지 남은 물건이나 잔재", "사라진 시대가 남겨 놓은 작은 조각", "relic=과거의 남은 유물·잔재 / artifact=사람이 만든 유물 / remnant=남은 일부"),
    ("renaissance", "부흥 / 재탄생", "예술·학문·관심이 다시 활발해지는 시기나 운동", "한동안 약해졌다가 다시 살아 올라오는 느낌", "renaissance=문화·학문의 부흥 / revival=되살아남 일반 / reform=제도 개선"),
    ("resettlement", "재정착 / 이주 후 정착", "다른 곳으로 옮겨 새 삶의 터를 다시 잡는 과정", "떠난 뒤 다시 자리를 잡고 삶을 세우는 느낌", "resettlement=새 지역에 다시 정착함 / relocation=위치를 옮김 / displacement=강제로 밀려남"),
    ("revolt", "반란 / 봉기하다", "지배나 권위에 맞서 집단이 들고일어나다", "더는 못 참겠다고 아래에서 위로 치받는 느낌", "revolt=반란·저항 봉기 / protest=항의하다 / riot=소요·폭동"),
    ("ritual", "의식 / 의례", "공동체나 종교 안에서 정해진 방식으로 반복되는 상징적 행동", "그냥 행동이 아니라 의미를 담아 정해진 순서로 하는 일", "ritual=상징적 의례 행위 / ceremony=공식 행사 의식 / custom=관습"),
    ("royalty", "왕족 / 왕실", "왕이나 여왕과 그 가족, 또는 군주적 지위", "일반 귀족보다 왕의 자리를 중심으로 한 혈통 집단", "royalty=왕족·왕실 / nobility=귀족 계층 / monarchy=군주제"),
    ("rural", "농촌의 / 시골의", "도시보다 인구가 적고 농업·자연 공간이 두드러진 지역의", "빽빽한 도시 밖 넓은 들과 마을 쪽 느낌", "rural=농촌의 / urban=도시의 / remote=멀리 떨어진"),
    ("scribe", "필경사 / 기록 필사자", "인쇄 이전이나 공식 기록에서 글을 베껴 쓰고 남기던 사람", "말과 문서를 손으로 옮겨 기록하는 사람", "scribe=필사·기록 담당자 / writer=글 쓰는 사람 일반 / clerk=사무 기록 담당자"),
    ("sedentary", "정착 생활의 / 오래 앉아 있는", "한곳에 머물러 사는 방식 또는 몸을 덜 움직이는 상태", "계속 이동하기보다 한자리에 자리 잡은 느낌", "sedentary=정착형·비활동적인 / nomadic=유목·이동형의 / stationary=움직이지 않는"),
    ("settlement", "정착지 / 합의", "사람들이 자리 잡고 사는 곳 또는 분쟁을 끝내는 합의", "흩어지던 것이 한곳이나 한 결론으로 자리를 잡는 느낌", "settlement=정착지·합의 / village=마을 / agreement=합의 일반"),
    ("slavery", "노예제 / 노예 상태", "사람이 소유와 강제 노동의 대상이 되는 제도나 상태", "사람의 자유가 제도적으로 묶인 상태", "slavery=노예제·노예 상태 / bondage=예속 상태 / servitude=강제적 종속"),
    ("sovereignty", "주권 / 자주적 통치권", "외부 지배 없이 스스로 다스릴 수 있는 최고 권한", "최종 결정권이 자기 공동체 안에 있는 상태", "sovereignty=국가·집단의 최고 자치 권한 / autonomy=자율성 / independence=독립 상태"),
    ("stability", "안정성 / 흔들리지 않음", "큰 혼란이나 급변 없이 상태가 유지되는 성질", "바닥이 쉽게 흔들리지 않고 버티는 느낌", "stability=안정적으로 유지됨 / continuity=끊기지 않는 이어짐 / security=위험으로부터 안전함"),
    ("stratified", "계층화된 / 층으로 나뉜", "사회나 구조가 서로 다른 층위로 분리·배열된", "평평하지 않고 여러 층으로 갈라진 느낌", "stratified=계층으로 나뉜 / hierarchical=위계가 있는 / divided=나뉜"),
    ("succession", "계승 / 이어받음", "권력·지위·순서가 다음 사람이나 단계로 넘어감", "앞사람 자리와 역할이 다음 줄로 넘어가는 느낌", "succession=지위·권력의 계승 / inheritance=재산·특성의 상속 / sequence=순서"),
    ("territory", "영토 / 관할 영역", "국가·집단·동물이 차지하거나 통제하는 공간", "여기까지가 내 영향권이라고 둘러친 땅", "territory=지배·관할 영역 / region=지역 / domain=활동·권한 영역"),
    ("textile", "직물 / 섬유 제품", "실이나 섬유를 짜서 만든 천과 관련 제품", "역사 속 생산과 교역을 보여주는 짜인 천", "textile=천·직물 제품 / fabric=천 재료 / garment=옷"),
    ("throne", "왕좌 / 군주 권력", "왕이 앉는 자리 또는 군주의 지위 자체", "한 의자라기보다 왕권의 꼭대기를 상징하는 자리", "throne=왕좌·군주 지위 / crown=왕관·왕권 상징 / monarchy=군주제"),
    ("tomb", "무덤 / 묘소", "시신이나 유해를 안치하는 구조물이나 장소", "죽은 이를 넣고 기념하는 닫힌 공간", "tomb=무덤 구조물 / grave=매장 장소 일반 / monument=기념 구조물"),
    ("tribal", "부족의 / 부족 집단과 관련된", "작은 전통 집단의 혈연·문화·정치 구조와 관련된", "국가보다 작고 친족·관습으로 묶인 집단 느낌", "tribal=부족 집단의 / ethnic=민족 집단의 / communal=공동체의"),
    ("treaty", "조약 / 공식 협정", "국가나 집단이 권리와 의무를 정해 맺는 공식 합의", "말로 끝내지 않고 문서로 묶은 국가 간 약속", "treaty=국가·집단 간 공식 조약 / agreement=합의 일반 / contract=법적 계약"),
    ("uprising", "봉기 / 반란", "사람들이 권력에 맞서 집단적으로 일어나는 사건", "눌려 있던 집단이 한꺼번에 위로 솟는 느낌", "uprising=집단적 봉기 / revolt=반란 / protest=항의 행동"),
    ("urbanization", "도시화", "인구와 생활·산업이 도시로 집중되는 변화 과정", "사람과 기능이 점점 도시 쪽으로 빨려 들어가는 흐름", "urbanization=도시로 집중되는 과정 / industrialization=산업 중심 구조로 바뀜 / migration=사람의 이동"),
    ("vernacular", "일상 언어의 / 토착어", "공식·고전어보다 사람들이 실제 생활에서 쓰는 지역 언어", "권위 있는 문어보다 사람들이 입으로 쓰는 자기말", "vernacular=일상 토착어·구어의 / dialect=지역 방언 / formal=격식 있는"),
    ("vessel", "선박 / 용기", "사람·물건을 실어 나르는 배 또는 담는 그릇", "무언가를 담거나 운반하는 바깥 껍질", "vessel=배·용기 / ship=큰 배 / container=담는 용기"),
    ("warlike", "호전적인 / 전쟁을 좋아하는 듯한", "갈등을 무력으로 풀려는 성향이 강한", "협상보다 싸움 쪽으로 쉽게 기우는 느낌", "warlike=전쟁·전투를 선호하는 듯한 / aggressive=공격적인 / militant=투쟁적으로 강경한"),
    ("waterway", "수로 / 배가 다니는 물길", "교통·무역·이동에 쓰이는 강·운하 같은 물길", "땅길 대신 물 위로 열린 이동 통로", "waterway=배가 다니는 물길 / canal=인공 운하 / river=강"),
    ("artisan", "장인 / 숙련 수공업자", "손기술로 물건을 정교하게 만드는 사람", "기계보다 손과 숙련으로 결과물을 만드는 사람", "artisan=숙련 장인 / craftsman=수공예 기술자 / laborer=일반 노동자"),
    ("chieftain", "부족장 / 지도자", "전통 집단이나 부족을 이끄는 우두머리", "공식 국가 수장보다 지역 집단의 중심 지도자", "chieftain=부족장·우두머리 / ruler=통치자 일반 / elder=연장자 지도자"),
    ("commemorate", "기념하다 / 기억을 공식적으로 되새기다", "중요한 사람이나 사건을 잊지 않도록 행사·표지로 남기다", "지나간 일을 그냥 넘기지 않고 의미 있게 다시 세우는 느낌", "commemorate=공식적으로 기념하다 / celebrate=축하하다 / remember=기억하다"),
    ("deity", "신 / 신적 존재", "종교나 신화 속 초월적 존재", "사람보다 위에 놓인 숭배 대상의 존재", "deity=신적 존재 / god=신 일반 / spirit=영적 존재"),
    ("displacement", "강제 이주 / 밀려남", "사람이나 집단이 기존 자리에서 밀려나 다른 곳으로 옮겨짐", "원래 있던 곳에서 힘에 의해 밖으로 떠밀리는 느낌", "displacement=자리에서 밀려남·강제 이동 / migration=이주 이동 / relocation=새 장소로 옮김"),
    ("heirloom", "가보 / 대대로 물려받은 물건", "가족 안에서 세대를 넘어 전해지는 소중한 물건", "물건 하나에 집안의 시간이 같이 묻어 이어지는 느낌", "heirloom=집안 대대로 내려온 가보 / artifact=역사적 유물 / souvenir=기념품"),
    ("homeland", "고향 땅 / 조국", "정체성과 뿌리를 두는 원래의 땅이나 공동체", "몸은 떠나 있어도 돌아가는 마음의 출발지", "homeland=정체성의 근거가 되는 고향 땅 / birthplace=태어난 곳 / territory=관할 영토"),
    ("iconography", "도상 해석 / 상징 이미지 체계", "그림·조각 속 상징과 이미지가 어떤 의미를 갖는지 보는 체계", "겉모습 아래 상징 코드를 읽어내는 방식", "iconography=이미지 상징 체계와 해석 / symbolism=상징성 일반 / imagery=이미지 표현"),
    ("kinship", "친족 관계 / 혈연 유대", "가족과 혈연을 기준으로 맺어진 사회적 연결", "개인을 집안과 친족망 안에 묶어 주는 관계선", "kinship=친족 관계망 / family=가족 단위 / ancestry=조상 계통"),
    ("manorial", "장원제의 / 영지 중심의", "봉건적 장원 운영과 토지 질서에 관련된", "넓은 영지를 중심으로 경제와 권력이 돌아가는 느낌", "manorial=장원제·영지 중심의 / feudal=봉건제 전반의 / agrarian=농업 기반의"),
    ("matrilineal", "모계 혈통의", "어머니 쪽 계통을 따라 친족과 상속을 잇는", "가계의 줄이 아버지가 아니라 어머니 쪽으로 이어지는 느낌", "matrilineal=모계 혈통을 따르는 / patrilineal=부계 혈통을 따르는 / maternal=어머니 쪽의"),
    ("medieval", "중세의", "고대 이후 근대 이전의 역사 시기와 관련된", "성·길드·봉건 질서가 떠오르는 오래된 중간 시대", "medieval=중세 시대의 / ancient=고대의 / modern=근대·현대의"),
    ("monastic", "수도원의 / 수도 생활의", "종교적 규율 아래 공동생활과 수행을 하는 집단과 관련된", "세속 바깥에서 규칙을 따라 조용히 사는 느낌", "monastic=수도원·수도 생활의 / religious=종교적인 / ascetic=금욕적인"),
    ("numismatic", "화폐 연구의 / 동전 수집·연구의", "옛 동전과 화폐를 통해 시대와 경제를 보는 연구와 관련된", "작은 동전 하나에서 시대 정보를 읽는 느낌", "numismatic=화폐·동전 연구의 / economic=경제의 / archaeological=고고학의"),
    ("paternal", "부계의 / 아버지 쪽의", "아버지나 아버지 계통과 관련된", "가족 관계를 아버지 쪽 선으로 보는 느낌", "paternal=아버지 쪽의 / maternal=어머니 쪽의 / patrilineal=부계 혈통을 따르는"),
    ("patrilineal", "부계 혈통의", "아버지 쪽 계통을 따라 친족과 상속을 잇는", "가계의 줄이 아버지 쪽으로 내려가는 느낌", "patrilineal=부계 혈통을 따르는 / matrilineal=모계 혈통을 따르는 / paternal=아버지 쪽의"),
    ("peasantry", "농민 계층", "역사적 사회 구조에서 농민들이 이루는 계층 전체", "개별 농부보다 사회 한 층을 이루는 농민 집단", "peasantry=농민 계층 전체 / peasant=농민 한 사람 / working class=노동 계층"),
    ("precolonial", "식민지화 이전의", "외부 식민 지배가 들어오기 전 시대와 관련된", "바깥 제국이 들어오기 전 자기 질서가 있던 시기", "precolonial=식민 지배 이전의 / colonial=식민 지배기의 / indigenous=토착의"),
    ("remnant", "잔존물 / 남은 일부", "큰 것이 사라진 뒤에도 일부 남아 있는 흔적이나 조각", "다 없어지지 않고 끝에 조금 남은 자투리", "remnant=남은 일부·잔재 / relic=과거의 유물·흔적 / remainder=나머지"),
    ("shrine", "성지 / 신전", "종교적 숭배나 기념을 위해 마련된 장소", "특정 신성함이나 기억 앞에 멈춰 서는 장소", "shrine=숭배·기념의 성소 / temple=종교 건축물 / monument=기념 구조물"),
    ("subsistence", "생계 유지 / 자급 수준의 생활", "최소한 먹고살 만큼 생산하고 버티는 방식", "남는 축적보다 하루하루 살아낼 만큼 유지하는 느낌", "subsistence=기초 생계 유지·자급 / livelihood=생계를 버는 방식 / prosperity=넉넉한 번영"),
    ("urbanism", "도시 생활 양식 / 도시 중심 사고", "도시의 공간·생활·사회 구조를 중심으로 보는 성향이나 방식", "삶의 기준이 도시 구조와 리듬에 맞춰진 느낌", "urbanism=도시 중심 생활·사고 / urbanization=도시로 집중되는 과정 / metropolitan=대도시권의"),
    ("vassal", "봉신 / 예속된 신하", "봉건 질서에서 보호와 토지를 받는 대신 충성을 바치는 하위 지배층", "독립적 군주가 아니라 위 권력에 묶인 충성 관계", "vassal=봉건적 예속 신하 / lord=상위 영주 / servant=일반 하인"),
    ("upheaval", "격변 / 대혼란", "사회나 정치 질서가 크게 뒤흔들리는 변화", "바닥부터 뒤집혀 안정이 깨지는 느낌", "upheaval=질서를 크게 흔드는 격변 / reform=제도 개선 / unrest=불안과 소요"),
    ("agrarian", "농업 중심의 / 농경 사회의", "토지 경작과 농업 생산이 사회의 중심인", "도시 산업보다 땅과 농사가 바닥을 이루는 느낌", "agrarian=농업 기반의 / rural=농촌의 / industrial=산업의"),
    ("annexation", "병합 / 영토 편입", "한 지역을 자국의 통치권 아래 공식적으로 편입하는 일", "경계 밖 땅을 자기 지도 안으로 끌어넣는 느낌", "annexation=영토를 공식 편입함 / occupation=점령 / integration=제도 안으로 통합"),
    ("caravan", "대상 / 이동 상인 행렬", "사막·장거리 길에서 함께 이동하는 상인·여행자 무리", "혼자 가지 않고 짐과 사람을 줄지어 함께 움직이는 행렬", "caravan=장거리 이동 상인·여행 행렬 / convoy=호위받는 차량·선박 행렬 / expedition=목적 있는 탐사대"),
    ("citadel", "성채 / 요새화된 중심지", "도시나 지역 방어를 위한 튼튼한 중심 요새", "위험할 때 버티는 돌로 된 마지막 중심 거점", "citadel=도시 중심 성채 / fortress=방어용 요새 / palace=왕궁"),
    ("diasporic", "디아스포라의 / 흩어진 이주 집단과 관련된", "고향 밖 여러 지역에 퍼진 공동체의 정체성·문화와 관련된", "떨어져 있어도 같은 뿌리가 여러 곳에 이어진 느낌", "diasporic=디아스포라 집단의 / migratory=이동성의 / ethnic=민족 집단의"),
    ("exile", "망명 / 추방", "정치적·사회적 이유로 고향 밖에 강제로 떠나 있거나 그렇게 만드는 일", "돌아가고 싶어도 원래 자리 밖으로 밀려난 상태", "exile=고향 밖으로 추방·망명됨 / migration=이주 / banishment=추방 처벌"),
    ("hinterland", "내륙 배후지", "해안·도시·중심지 뒤쪽에 놓인 덜 중심적인 내륙 지역", "앞의 중심 도시를 뒤에서 받치는 안쪽 땅", "hinterland=중심지 뒤의 내륙 배후지 / frontier=확장 경계지역 / countryside=농촌 지방"),
    ("irrigation", "관개 / 물대기", "농경지에 물길을 대어 작물을 키우는 체계", "자연 비만 기다리지 않고 물을 끌어와 땅을 적시는 느낌", "irrigation=농경지에 물을 대는 체계 / drainage=물을 빼는 배수 / cultivation=경작"),
    ("marooned", "고립된 / 멀리 떨어져 꼼짝 못하는", "외딴 곳에 남겨져 이동이나 구조가 어려운", "사람과 길에서 떨어져 혼자 갇힌 느낌", "marooned=외딴 곳에 고립된 / isolated=분리된 / stranded=발이 묶인"),
    ("mobilization", "동원 / 조직적 결집", "사람·자원·여론을 어떤 목적을 위해 움직이게 모으는 일", "흩어진 힘을 한 방향으로 일으켜 세우는 느낌", "mobilization=사람·자원을 목적 있게 동원함 / recruitment=사람을 모집함 / activation=작동을 시작함"),
    ("pastoral", "목축의 / 전원의", "가축을 기르며 살아가는 방식이나 평화로운 전원 풍경과 관련된", "도시 소음보다 풀밭과 가축이 있는 느린 풍경", "pastoral=목축·전원적인 / rural=농촌의 / agricultural=농업의"),
    ("pilgrim", "순례자", "종교적·상징적 목적지로 길을 떠난 사람", "여행객보다 의미 있는 장소를 향해 걷는 사람", "pilgrim=순례하는 사람 / traveler=여행자 일반 / devotee=헌신적 신자"),
    ("pottery", "도자기 / 토기", "흙을 빚고 구워 만든 용기나 물건", "손으로 빚은 흙이 불을 거쳐 남는 생활 유물", "pottery=도자기·토기 / ceramic=도자 재료·제품 / vessel=용기"),
    ("resilience", "회복력 / 버티는 힘", "충격이나 변화 후에도 무너지지 않고 다시 적응하는 능력", "흔들려도 다시 제자리로 튀어 오르는 힘", "resilience=충격을 견디고 회복하는 힘 / stability=안정 유지 / endurance=오래 버팀"),
]


def load_existing_words() -> set[str]:
    words: set[str] = set()
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        if path.name == TARGET.name:
            continue
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.reader(f, delimiter="\t"):
                if row:
                    words.add(row[0].strip())
    return words


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: {extra}",
            f"핵심 느낌: {feeling}",
            f"구분: {distinction}",
        ]
    )


def write_set14() -> list[str]:
    existing = load_existing_words()
    selected = []
    seen = set()

    for word, core, extra, feeling, distinction in CARDS:
        if word in existing or word in seen:
            continue
        selected.append((word, build_back(core, extra, feeling, distinction)))
        seen.add(word)
        if len(selected) == 100:
            break

    if len(selected) < 100:
        raise RuntimeError(f"Only {len(selected)} non-duplicate cards available for set 14")

    with TARGET.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerows(selected)

    return [word for word, _ in selected]


def refresh_headword_files() -> int:
    ets_words: list[str] = []
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            ets_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)

    awl_words: list[str] = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)

    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    all_words = sorted(set(ets_words + awl_words))
    (ROOT / "all_headwords.txt").write_text("\n".join(all_words) + "\n", encoding="utf-8")
    return len(ets_words)


def update_manifest(total_ets_cards: int) -> None:
    path = ROOT / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if TARGET.name not in manifest["files_created"]:
        manifest["files_created"].insert(13, TARGET.name)
    manifest["total_ets_cards"] = total_ets_cards
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_notes(total_ets_cards: int) -> None:
    gen_notes = ROOT / "generation_notes.md"
    text = gen_notes.read_text(encoding="utf-8")
    text = text.replace(
        "- ETS sets `01` to `13` exist, bringing the ETS-based total to 1300 cards\n",
        f"- ETS sets `01` to `14` exist, bringing the ETS-based total to {total_ets_cards} cards\n",
    )
    gen_notes.write_text(text, encoding="utf-8")

    work_plan = ROOT / "WORK_PLAN.md"
    text = work_plan.read_text(encoding="utf-8")
    text = text.replace(
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_13.tsv`\n",
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_14.tsv`\n",
    )
    text = text.replace(
        "- Current ETS row count after the latest expansion pass: 1300\n",
        f"- Current ETS row count after the latest expansion pass: {total_ets_cards}\n",
    )
    work_plan.write_text(text, encoding="utf-8")


def main() -> None:
    words = write_set14()
    total_ets_cards = refresh_headword_files()
    update_manifest(total_ets_cards)
    update_notes(total_ets_cards)

    print(f"generated {TARGET.name}: {len(words)} cards")
    print(f"total ETS cards: {total_ets_cards}")
    print("sample:", ", ".join(words[:10]))


if __name__ == "__main__":
    main()
