from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_20.tsv"

CARDS = [
    ("aesthetic", "미학적인 / 아름다움과 표현 방식에 관한", "기능보다 형태, 분위기, 감각적 인상을 어떻게 구성하는지와 관련된", "쓸모만이 아니라 보이고 느껴지는 결을 보는 느낌", "aesthetic=감각적 아름다움과 표현 방식의 / artistic=예술적인 / functional=기능적인"),
    ("allegorical", "우화적인 / 다른 뜻을 빗대어 담은", "겉이야기 뒤에 더 큰 의미나 사회적 메시지를 상징적으로 숨겨 놓은", "겉 장면 하나가 사실 다른 뜻을 대신 들고 있는 느낌", "allegorical=겉이야기 너머 상징적 뜻을 담은 / literal=문자 그대로의 / symbolic=상징적인"),
    ("ambience", "분위기 / 공간이나 장면이 주는 전체 느낌", "조명, 소리, 배치, 말투 등이 합쳐져 만들어내는 정서적 환경", "한 요소보다 장면 전체에 깔린 공기의 색깔", "ambience=공간이나 장면의 전체 분위기 / tone=말이나 작품의 태도와 어조 / setting=배경"),
    ("articulate", "분명히 표현하다 / 조리 있게 말하다", "생각이나 해석을 흐릿하게 두지 않고 말이나 글로 또렷하게 드러내다", "머릿속 느낌을 밖으로 선명한 말 형태로 꺼내는 느낌", "articulate=생각을 분명히 표현하다 / express=표현하다 / imply=암시하다"),
    ("auditory cue", "청각적 신호 / 소리로 주는 단서", "장면 전환, 감정, 위험, 리듬 등을 소리를 통해 알아차리게 하는 표시", "눈이 아니라 귀로 다음 의미를 살짝 찔러 주는 신호", "auditory cue=소리로 전달되는 단서 / visual cue=눈으로 보이는 단서 / background noise=배경 소음"),
    ("backdrop", "배경막 / 사건이나 분위기를 받쳐 주는 배경", "주요 행동 앞에 깔려 장면의 맥락이나 분위기를 만들어 주는 배경 요소", "앞의 인물보다 뒤에서 의미의 무대를 깔아 주는 판", "backdrop=앞 장면을 받치는 배경 / foreground=앞쪽에 두드러진 부분 / setting=이야기가 놓인 환경"),
    ("brushstroke", "붓질 / 표현이 드러나는 한 획", "그림의 물리적 붓자국뿐 아니라 스타일이 드러나는 개별 표현 흔적", "매끈한 결과 뒤에 손의 방향이 남은 한 줄의 흔적", "brushstroke=붓의 한 획이나 표현 흔적 / texture=표면 질감 / outline=윤곽선"),
    ("captioned", "설명이 붙은 / 자막이나 캡션이 달린", "이미지나 장면 아래에 의미, 출처, 대사를 보충하는 짧은 글이 붙은", "그림만 던지지 않고 옆에 읽는 힌트를 붙여 둔 느낌", "captioned=설명 글이나 자막이 붙은 / annotated=주석이 달린 / untitled=제목이 없는"),
    ("choreograph", "동작을 짜다 / 움직임의 흐름을 설계하다", "춤만이 아니라 사람이나 장면의 이동과 순서를 의도적으로 배열하다", "움직임이 제멋대로가 아니라 보이지 않는 동선으로 짜이는 느낌", "choreograph=동작과 순서를 설계하다 / improvise=즉흥적으로 하다 / coordinate=맞춰 움직이게 하다"),
    ("cinematic", "영화적인 / 장면감 있게 구성된", "카메라처럼 시각적 전환, 구도, 분위기를 강하게 살린 표현 방식의", "글이나 이미지가 머릿속에서 영화 장면처럼 펼쳐지는 느낌", "cinematic=영화 장면처럼 구성된 / theatrical=연극 무대 같은 / descriptive=묘사가 자세한"),
    ("collage", "콜라주 / 여러 조각을 이어 붙인 구성", "서로 다른 이미지, 자료, 스타일을 한 화면이나 작품 안에 붙여 새 의미를 만드는 방식", "하나의 매끈한 덩어리보다 다른 조각들이 일부러 맞붙어 있는 느낌", "collage=여러 조각을 붙여 만든 구성 / montage=장면을 이어 붙인 편집 / blend=자연스럽게 섞음"),
    ("color palette", "색상 팔레트 / 주로 쓰는 색의 조합", "작품이나 화면이 일관되게 사용하는 색 범위와 그 조합", "아무 색이나 쓰지 않고 특정 색 상자 안에서 분위기를 맞추는 느낌", "color palette=선택된 색 조합 / hue=색조 / contrast=대비"),
    ("composition", "구도 / 요소를 배열한 전체 구성", "부분들이 어디에 놓이고 어떻게 균형을 이루는지에 관한 짜임", "각 조각보다 그 조각들이 화면 안에서 자리 잡는 방식", "composition=요소의 전체 배열과 구도 / layout=배치 / component=개별 구성 요소"),
    ("connotation", "함축 의미 / 단어·이미지가 덧붙여 풍기는 뜻", "직접 뜻 외에 문화적, 감정적으로 함께 따라오는 인상이나 연상", "사전 뜻 옆에 그림자처럼 붙어 오는 느낌", "connotation=표면 뜻 너머 따라오는 함축 / denotation=직접적인 기본 뜻 / implication=말 속에 담긴 시사점"),
    ("curatorial", "큐레이션의 / 무엇을 골라 어떻게 보여줄지에 관한", "많은 자료 중 일부를 선택하고 순서를 짜서 해석의 틀을 만드는 일과 관련된", "그냥 모아 놓는 게 아니라 무엇을 어떻게 보게 할지 편집하는 느낌", "curatorial=선별·배열해 보여주는 방식의 / archival=자료 보존과 관련된 / editorial=편집 판단의"),
    ("depict", "묘사하다 / 그림이나 말로 그려 보이다", "사람, 장면, 상황을 구체적 형태로 나타내 독자가 머릿속에 보게 하다", "뜻을 설명만 하지 않고 눈앞에 장면을 세워 주는 느낌", "depict=구체적 모습으로 묘사하다 / describe=말로 설명하다 / portray=특정 인상으로 그려내다"),
    ("dramatic tension", "극적 긴장감 / 다음 전개를 기다리게 하는 팽팽함", "갈등, 정보 지연, 대비를 통해 장면이 쉽게 풀리지 않고 긴장을 유지하는 상태", "줄이 느슨하지 않고 당겨져 있어 다음 순간을 붙잡는 느낌", "dramatic tension=전개를 끌고 가는 긴장감 / suspense=결과를 기다리는 조마조마함 / conflict=갈등 자체"),
    ("evocative", "강한 연상을 불러일으키는", "직접 다 설명하지 않아도 장면, 감정, 기억, 분위기를 생생히 떠올리게 하는", "말 한 조각이 머릿속에 냄새와 그림까지 같이 깨우는 느낌", "evocative=강한 이미지·감정을 불러일으키는 / suggestive=무언가를 암시하는 / explicit=직접 드러내는"),
    ("expressive", "표현력이 강한 / 감정과 의미가 잘 드러나는", "형식이 단순히 정확한 것을 넘어 내면의 느낌이나 태도가 밖으로 뚜렷이 나오는", "겉모양 뒤에 담긴 감정의 결이 선명히 비치는 느낌", "expressive=감정과 의미를 풍부하게 드러내는 / descriptive=자세히 묘사하는 / restrained=절제된"),
    ("foreground", "전면에 내세우다 / 눈에 띄게 강조하다", "여러 요소 중 특정 부분을 배경이 아니라 해석의 중심으로 끌어올리다", "뒤에 깔아두지 않고 앞자리로 당겨 스포트라이트를 비추는 느낌", "foreground=특정 요소를 앞세워 강조하다 / highlight=돋보이게 하다 / background=뒤로 물리다"),
    ("genre-bending", "장르를 넘나드는 / 기존 장르 경계를 비트는", "한 장르 규칙만 따르지 않고 서로 다른 형식과 기대를 섞어 새 효과를 만드는", "정해진 칸 하나에 안 들어가고 장르 벽을 비틀어 넘는 느낌", "genre-bending=장르 경계를 섞고 흔드는 / hybrid=둘 이상이 섞인 / conventional=관습적인"),
    ("iconic", "상징적으로 유명한 / 한눈에 알아볼 만큼 대표적인", "많은 사람이 그 이미지나 장면을 특정 시대, 인물, 의미와 바로 연결할 만큼 널리 각인된", "설명이 길지 않아도 보자마자 대표 이미지로 꽂히는 느낌", "iconic=대표 이미지처럼 널리 각인된 / famous=유명한 / symbolic=상징적 의미를 띤"),
    ("immersive", "몰입감 있는 / 그 안에 들어간 듯 느끼게 하는", "관찰자와 작품 사이 거리를 줄여 장면이나 경험 속에 깊이 빨려 들어가게 하는", "밖에서 구경만 하는 게 아니라 안쪽 공기에 잠기는 느낌", "immersive=경험 속으로 깊이 끌어들이는 / engaging=흥미롭게 붙잡는 / distant=거리를 둔"),
    ("improvise", "즉흥적으로 하다 / 현장에서 바로 만들어 내다", "미리 완전히 정한 대본이나 구조 없이 상황에 맞춰 표현이나 해결을 즉석에서 만들어 가다", "정해진 악보보다 지금 순간 손끝에서 바로 만들어지는 느낌", "improvise=즉석에서 만들어 하다 / rehearse=미리 연습하다 / choreograph=동작을 짜다"),
    ("interpretive", "해석의 / 의미를 어떻게 읽는지에 관한", "사실 자체보다 자료나 장면에 어떤 의미를 부여하고 이해하는지에 초점을 둔", "그 자체를 보는 것보다 어떤 렌즈로 읽느냐가 앞서는 느낌", "interpretive=의미 해석에 관한 / descriptive=모습을 묘사하는 / analytical=구조와 관계를 따지는"),
    ("juxtapose", "병치하다 / 나란히 놓아 대비를 만들다", "두 이미지나 생각을 일부러 가까이 놓아 차이, 긴장, 새 의미가 드러나게 하다", "따로 보면 덜 보이던 차이가 옆에 붙자 확 튀어나오는 느낌", "juxtapose=나란히 놓아 대비와 의미를 드러내다 / compare=비교하다 / merge=합치다"),
    ("layered", "층위가 겹친 / 의미가 여러 겹인", "한 번 읽고 끝나는 단일 의미보다 표면 아래에 다른 감정과 해석이 겹쳐 있는", "겉 한 장을 넘기면 아래에 또 다른 뜻의 막이 깔린 느낌", "layered=의미나 구성의 층이 여러 겹인 / simple=단순한 / dense=내용이 빽빽한"),
    ("lyrical", "서정적인 / 리듬과 감정이 살아 있는", "정보 전달보다 음악성, 감정, 부드러운 흐름이 강하게 느껴지는 표현의", "문장이 딱딱한 설명보다 노래하듯 감정선을 타는 느낌", "lyrical=리듬과 감정이 강한 서정적 표현의 / poetic=시적인 / factual=사실 중심의"),
    ("metaphorical", "은유적인 / 다른 것을 빌려 뜻을 옮긴", "직접 말하지 않고 다른 이미지나 개념을 빌려 추상적 의미를 드러내는", "하나를 말하는데 사실 다른 장면으로 뜻을 비춰 보여주는 느낌", "metaphorical=다른 대상을 빌려 뜻을 옮기는 / literal=직접적인 / figurative=비유적인"),
    ("minimalist", "미니멀한 / 요소를 최대한 덜어낸", "장식과 세부를 많이 더하기보다 꼭 필요한 형태와 선만 남겨 효과를 만드는", "꽉 채우기보다 덜어내서 빈자리와 핵심만 또렷해지는 느낌", "minimalist=요소를 덜어내 단순하게 구성한 / elaborate=장식과 세부가 많은 / sparse=성긴"),
    ("motif", "반복 모티프 / 되풀이되며 의미를 만드는 요소", "이미지, 소리, 문구, 상황이 반복적으로 나타나 작품의 핵심 주제를 묶어 주는 단위", "한 번 스치고 끝나지 않고 다시 돌아오며 의미를 엮는 표식", "motif=반복되는 주제 요소 / theme=작품 전체의 중심 주제 / symbol=특정 의미를 담은 상징물"),
    ("multimodal", "다중 양식의 / 글·이미지·소리 등 여러 표현 방식이 섞인", "한 가지 전달 채널만 쓰지 않고 서로 다른 감각·기호 체계를 함께 활용하는", "한 화면이나 자료가 글 한 줄이 아니라 여러 감각 문을 같이 여는 느낌", "multimodal=여러 표현 양식을 함께 쓰는 / visual=시각 중심의 / textual=글 중심의"),
    ("narrative arc", "서사 곡선 / 이야기가 진행되며 오르내리는 큰 흐름", "도입, 전개, 긴장 고조, 해결처럼 사건과 감정이 시간 속에서 움직이는 전체 궤적", "장면들이 낱개가 아니라 하나의 휘어진 선으로 올라갔다 내려오는 느낌", "narrative arc=이야기 전개의 큰 곡선 / plot=사건 배열 / episode=개별 사건 단위"),
    ("nuanced", "미묘한 차이를 담은 / 단순하지 않게 결이 살아 있는", "흑백으로 딱 자르지 않고 감정, 판단, 의미의 작은 차이를 함께 보여 주는", "한 색으로 칠하지 않고 중간 톤까지 살려 보는 느낌", "nuanced=미묘한 차이와 결을 담은 / subtle=섬세하게 드러나는 / simplistic=지나치게 단순한"),
    ("orchestrate", "조율해 엮다 / 여러 요소를 의도적으로 맞춰 움직이게 하다", "음악만이 아니라 사람, 장면, 효과, 절차를 서로 어긋나지 않게 짜서 하나의 결과를 만들다", "각자 따로 울리는 소리를 한 흐름 안에 맞춰 세우는 느낌", "orchestrate=여러 요소를 조율해 하나로 엮다 / organize=조직하다 / improvise=즉흥으로 하다"),
    ("performative", "행위 자체가 의미를 만드는 / 보여주는 수행의 성격이 강한", "내용만 전달하는 것이 아니라 말하거나 행동하는 방식 자체가 사회적 의미를 만들어 내는", "무슨 말을 했나보다 그것을 어떻게 보여주며 했나가 의미가 되는 느낌", "performative=행위의 수행 자체가 의미를 만드는 / expressive=감정을 드러내는 / theatrical=무대적으로 과장된"),
    ("perspective shift", "관점 전환 / 보는 위치나 해석 틀이 바뀜", "같은 장면이나 문제를 다른 인물, 가치, 거리에서 보게 되어 의미가 달라지는 변화", "카메라 위치를 옮기자 같은 장면의 강조점이 바뀌는 느낌", "perspective shift=보는 관점이 바뀌는 것 / reinterpretation=다시 해석함 / bias=한쪽으로 기운 시각"),
    ("photorealistic", "사진처럼 사실적인", "실제 사진과 거의 비슷하게 빛, 질감, 비율, 세부를 살려 재현한", "그린 것인데도 카메라로 찍은 것처럼 보이는 느낌", "photorealistic=사진처럼 사실적으로 재현한 / stylized=의도적으로 양식을 변형한 / abstract=구체 형상을 덜어낸"),
    ("pictorial", "그림으로 표현된 / 시각 이미지 중심의", "설명이나 논증보다 그림, 화면, 시각적 장면을 통해 전달되는 성격의", "말보다 이미지가 먼저 장면을 열어 주는 느낌", "pictorial=그림과 이미지 중심의 / textual=글 중심의 / verbal=말로 된"),
    ("portrayal", "묘사 방식 / 어떤 인물·집단·사건을 그려내는 표현", "대상을 단순 복사하는 것이 아니라 특정 인상과 해석이 담기게 보여주는 방식", "있는 그대로 사진 찍기보다 어떤 얼굴로 보이게 그리느냐가 드러나는 느낌", "portrayal=특정 인상으로 대상을 그려낸 방식 / depiction=묘사 / stereotype=고정된 단순화 이미지"),
    ("resonance", "울림 / 감정적·문화적으로 오래 남는 힘", "작품이나 말이 즉시 끝나지 않고 경험, 기억, 가치와 맞닿아 깊게 남는 효과", "소리가 멈춰도 안쪽에서 한동안 진동이 이어지는 느낌", "resonance=마음이나 문화 속에 오래 남는 울림 / impact=즉각적 영향 / relevance=관련성"),
    ("rhythmic", "리듬감 있는 / 반복과 강약의 흐름이 있는", "음악뿐 아니라 문장, 동작, 편집이 일정한 박자나 흐름감을 만들어 내는", "고른 정보 나열보다 몸이 따라가는 박이 살아 있는 느낌", "rhythmic=박자와 반복 흐름이 있는 / monotonous=단조로운 / melodic=선율적인"),
    ("scene-setting", "장면 설정 / 분위기와 맥락을 먼저 깔아 주는", "본격 사건이나 주장 전에 배경, 분위기, 시각적 단서를 배치해 이해의 틀을 만드는", "이야기를 바로 던지지 않고 먼저 무대 조명과 배경을 켜는 느낌", "scene-setting=장면과 분위기를 먼저 깔아 줌 / exposition=배경 정보를 설명함 / transition=장면을 넘김"),
    ("sensory detail", "감각적 세부 묘사 / 보고 듣고 느끼는 구체적 단서", "추상적 설명보다 색, 소리, 질감, 움직임 같은 감각 정보를 통해 장면을 선명하게 만드는 세부 요소", "머리로 아는 정보가 아니라 몸으로 느끼는 단서가 장면을 살리는 느낌", "sensory detail=감각을 살리는 구체적 묘사 / abstract idea=추상 개념 / description=묘사 일반"),
    ("silhouette", "실루엣 / 윤곽만 드러난 형태", "세부보다 바깥선과 형태의 덩어리가 빛 대비 속에서 두드러져 보이는 모습", "안쪽 무늬보다 어두운 외곽선 하나로 형상이 읽히는 느낌", "silhouette=윤곽이 강조된 모습 / outline=테두리선 / shadow=그림자"),
    ("soundscape", "사운드스케이프 / 한 공간을 이루는 전체 소리 환경", "한 소리만이 아니라 배경음, 목소리, 잡음, 울림이 합쳐져 만드는 청각적 장면", "귀로 듣는 풍경 전체가 한 겹의 공간처럼 펼쳐지는 느낌", "soundscape=공간 전체의 소리 풍경 / soundtrack=작품에 깔린 음악·음향 트랙 / ambience=전체 분위기"),
    ("spectator", "관람자 / 공연이나 장면을 지켜보는 사람", "직접 실행하는 사람보다 무대, 경기, 작품을 일정 거리에서 보는 위치에 있는 사람", "무대 위가 아니라 객석 쪽에서 의미를 받아 보는 자리", "spectator=지켜보는 관람자 / participant=직접 참여자 / audience=집합적 관객"),
    ("staging", "무대 연출 / 장면을 공간과 동작으로 배치하는 방식", "무대나 화면에서 인물, 소품, 움직임, 조명을 어떻게 놓아 의미를 만들지 구성하는 일", "대사만이 아니라 어디에 서고 어디서 빛이 들어오는지가 뜻이 되는 느낌", "staging=공간과 동작을 짜는 연출 / acting=연기 / production=제작 전체"),
    ("stylized", "양식화된 / 사실 그대로보다 특정 스타일로 변형한", "현실을 그대로 복사하기보다 선, 색, 비율, 움직임을 의도적으로 바꿔 독특한 인상을 만든", "실제 모습 위에 작가의 스타일 필터가 강하게 씌워진 느낌", "stylized=특정 양식으로 변형한 / realistic=현실에 가깝게 재현한 / exaggerated=과장된"),
    ("subtext", "숨은 뜻 / 겉으로 말하지 않은 밑바닥 의미", "대사나 장면의 표면 아래에 감정, 갈등, 의도가 직접 말하지 않은 채 깔려 있는 의미", "문장 위는 잔잔한데 아래층에서 다른 말이 흐르는 느낌", "subtext=겉표현 아래 깔린 숨은 의미 / context=주변 맥락 / implication=시사하는 뜻"),
    ("symbolism", "상징성 / 어떤 것이 더 큰 의미를 대표하게 쓰이는 방식", "사물이나 장면이 자기 자체를 넘어 가치, 감정, 역사적 의미를 대신하게 만드는 표현", "작은 이미지 하나가 더 큰 뜻의 깃발처럼 서는 느낌", "symbolism=대상이 더 큰 의미를 대표하는 방식 / metaphor=다른 것을 빌려 뜻을 옮김 / literalness=직접적 의미"),
    ("textured", "질감이 살아 있는 / 결이 느껴지는", "표면이 지나치게 매끈하지 않고 시각적·언어적 층과 결이 드러나는", "손끝이나 눈으로 울퉁불퉁한 결이 잡히는 느낌", "textured=질감과 결이 살아 있는 / smooth=매끈한 / layered=층이 겹친"),
    ("thematic", "주제적인 / 중심 의미와 반복되는 문제의식에 관한", "개별 사건보다 작품이나 자료 전체를 묶는 핵심 주제와 연결된", "흩어진 장면들을 한 줄로 꿰는 큰 의미 실", "thematic=작품의 중심 주제와 관련된 / topical=지금 다루는 화제의 / episodic=개별 사건 단위의"),
    ("tonal", "어조나 분위기의 / 작품이 띠는 정서적 색조의", "내용 자체보다 말투, 색, 소리, 연출이 만들어내는 감정적 온도와 관련된", "같은 말이라도 따뜻한지 차가운지의 색깔이 먼저 느껴지는 층", "tonal=정서적 어조와 분위기에 관한 / thematic=주제와 관련된 / verbal=언어적인"),
    ("understated", "절제된 / 과하게 드러내지 않은", "감정이나 의미를 크게 외치지 않고 낮은 강도로 눌러 보여 오히려 여운을 남기는", "큰 손짓 대신 작게 눌러 말해서 더 오래 남는 느낌", "understated=과장 없이 절제된 / subtle=은근한 / dramatic=강하게 눈에 띄는"),
    ("visualize", "시각화하다 / 눈에 보이게 떠올리거나 표현하다", "추상 정보나 생각을 머릿속 이미지나 도식, 장면 형태로 바꾸다", "말만 있던 것을 눈앞 그림으로 세워 보는 느낌", "visualize=눈에 보이는 이미지로 만들거나 떠올리다 / imagine=상상하다 / illustrate=그림·예로 보여주다"),
    ("voiceover", "내레이션 음성 / 화면 위에 덧입힌 목소리", "화면에 직접 말하는 입이 보이지 않아도 설명이나 해석을 덧붙이는 녹음 음성", "보이는 장면 위로 보이지 않는 목소리가 의미를 얹는 느낌", "voiceover=화면 위에 덧입힌 설명 음성 / narration=이야기 전달 / dialogue=인물 간 대화"),
    ("vocal delivery", "발화 전달 방식 / 목소리로 어떻게 말하는지", "무엇을 말했는지만이 아니라 속도, 억양, 강세, 멈춤으로 의미와 감정을 실어 내는 방식", "같은 문장도 목소리의 밀고 당김이 다른 뜻을 입히는 느낌", "vocal delivery=목소리로 말하는 방식 / pronunciation=발음 / diction=단어 선택과 발화 방식"),
    ("archival", "기록 보존의 / 자료 아카이브와 관련된", "과거 자료를 모으고 정리해 나중에 다시 검토하거나 해석할 수 있게 하는 일과 관련된", "지나간 흔적을 흩어지지 않게 선반에 보존해 두는 느낌", "archival=기록 자료 보존과 관련된 / historical=역사적인 / curatorial=무엇을 골라 어떻게 보여줄지의"),
    ("atmospheric", "분위기를 강하게 자아내는", "장면의 줄거리보다 빛, 소리, 밀도, 여백을 통해 특정 정서를 짙게 깔아 주는", "사건보다 공기가 먼저 몸에 감기는 듯한 느낌", "atmospheric=장면 분위기를 강하게 만드는 / dramatic=극적으로 강한 / ambient=주변에 은은히 깔린"),
    ("authorial", "작가의 / 창작자의 관점과 통제가 드러나는", "작품 속 선택과 설명이 창작자의 해석, 목소리, 배열 의도를 드러내는 성격의", "누가 이 장면을 이렇게 보여주게 골랐는지가 느껴지는 느낌", "authorial=작가의 관점과 통제가 드러나는 / editorial=편집 판단의 / anonymous=익명의"),
    ("body language", "몸짓 언어 / 자세와 움직임으로 드러나는 비언어적 신호", "말보다 시선, 손짓, 거리, 자세를 통해 감정이나 관계를 전달하는 표현", "입보다 몸의 방향과 긴장이 먼저 말을 거는 느낌", "body language=몸으로 드러나는 비언어 신호 / gesture=손짓·동작 / speech=말"),
    ("camera angle", "카메라 각도 / 어떤 위치와 높이에서 보여주는지", "같은 대상이라도 위, 아래, 옆, 가까이서 찍어 인상과 힘의 관계를 달리 만드는 시점 선택", "어디서 보느냐가 대상의 크기와 권력을 바꿔 보이게 하는 느낌", "camera angle=촬영 시점의 각도 / perspective=보는 관점 / frame=화면 경계와 구성"),
    ("characterization", "인물 형상화 / 어떤 성격과 동기로 그려내는 방식", "인물이 대사, 행동, 묘사, 반응을 통해 어떤 사람으로 이해되게 만드는 구성", "이름표보다 반복된 말과 행동이 한 사람의 결을 빚는 느낌", "characterization=인물을 어떤 성격으로 그려내는 방식 / portrayal=대상을 어떤 인상으로 보여주는 방식 / personality=성격 자체"),
    ("contextualize", "맥락화하다 / 주변 조건 속에서 이해되게 놓다", "작품이나 발언을 따로 떼어 보지 않고 시대, 장소, 목적, 관계와 함께 읽게 하다", "한 조각을 공중에 띄우지 않고 원래 놓인 판 위에 다시 얹는 느낌", "contextualize=주변 맥락 속에 놓고 이해하다 / isolate=따로 떼어내다 / interpret=의미를 해석하다"),
    ("creative medium", "창작 매체 / 뜻을 담는 표현 재료나 형식", "회화, 사진, 영상, 소리, 글처럼 아이디어를 실제로 구현하는 전달 형식", "같은 생각도 어떤 그릇에 담느냐에 따라 다른 결로 나오는 느낌", "creative medium=아이디어를 담는 표현 매체 / format=형식 / platform=유통·발표 기반"),
    ("cultural lens", "문화적 렌즈 / 특정 문화 기준으로 보는 해석 틀", "장면이나 텍스트를 읽을 때 어떤 가치, 관습, 역사 경험이 해석을 거르는지 보여주는 시각", "있는 그대로 본다고 생각해도 사실 특정 문화 안경을 끼고 보는 느낌", "cultural lens=문화 기준이 반영된 해석 시각 / bias=한쪽으로 기운 판단 / worldview=세계를 보는 큰 틀"),
    ("curate", "선별해 구성하다 / 보여줄 자료를 골라 배열하다", "많은 항목을 그대로 다 내놓지 않고 목적과 해석에 맞게 고르고 순서를 짜다", "무작정 쌓는 게 아니라 무엇을 앞세우고 묶을지 손으로 골라 내는 느낌", "curate=자료를 선별해 구성하다 / collect=모으다 / archive=보존용으로 정리하다"),
    ("dramaturgical", "극구성의 / 장면과 갈등을 어떻게 짜는지와 관련된", "이야기나 공연이 사건, 긴장, 전환, 인물 관계를 어떤 구조로 배열하는지에 관한", "한 장면씩 따로가 아니라 무대 전체가 어떤 긴장선으로 짜였는지 보는 느낌", "dramaturgical=극적 구조와 장면 배열에 관한 / theatrical=연극적인 / narrative=이야기 구조의"),
    ("embody", "몸으로 구현하다 / 어떤 의미나 가치를 실제 모습으로 드러내다", "추상적 생각이나 성격을 말로만 설명하지 않고 행동, 형태, 목소리로 직접 나타내다", "개념이 공중에 떠 있지 않고 몸과 형식 안에 입혀지는 느낌", "embody=의미·가치를 구체적 형태로 드러내다 / symbolize=상징하다 / represent=대표하거나 나타내다"),
    ("emotive", "감정을 강하게 불러일으키는", "정보보다 듣는 사람이나 보는 사람의 감정 반응을 직접 건드리는 힘이 큰", "머리로 이해하기 전에 먼저 마음 쪽을 당기는 느낌", "emotive=감정 반응을 강하게 일으키는 / emotional=감정과 관련된 / neutral=중립적인"),
    ("frame narrative", "틀 서사 / 안쪽 이야기를 감싸는 바깥 이야기 구조", "한 이야기 안에 다른 이야기를 넣고 바깥 구조가 안쪽 해석을 잡아 주는 방식", "안쪽 그림을 그냥 두지 않고 바깥 액자가 의미의 테두리를 정하는 느낌", "frame narrative=바깥 이야기가 안쪽 이야기를 감싸는 구조 / subplot=부차적 줄거리 / context=주변 맥락"),
    ("impressionistic", "인상주의적인 / 정확한 세부보다 순간적 인상과 빛을 살린", "대상을 또렷한 윤곽보다 변화하는 느낌, 색, 분위기, 감각으로 포착하는 표현 방식의", "정밀 복사보다 스쳐 보이는 빛과 공기의 느낌을 먼저 잡는 느낌", "impressionistic=순간적 인상과 분위기를 살린 / realistic=사실적으로 재현한 / abstract=구체 형상을 덜어낸"),
    ("intertextual", "텍스트 상호참조적인 / 다른 작품과의 연결이 드러나는", "한 작품의 의미가 다른 이야기, 문장, 이미지, 장르 관습을 불러와 함께 읽히는", "혼자 닫힌 글이 아니라 다른 글들의 메아리가 안에서 들리는 느낌", "intertextual=다른 텍스트와 연결해 읽히는 / original=독자적인 / referential=무언가를 참조하는"),
    ("linear narrative", "직선적 서사 / 시간 순서대로 이어지는 이야기", "사건이 앞뒤를 자주 뒤섞지 않고 비교적 시간의 순서를 따라 진행되는 구조", "이야기가 갈래로 튀기보다 한 길을 따라 앞으로 나아가는 느낌", "linear narrative=시간 순서로 진행되는 서사 / nonlinear narrative=순서가 뒤섞인 서사 / chronology=시간 순서"),
    ("medium-specific", "매체 고유의 / 그 표현 형식만의 특성을 살린", "글, 영화, 음악, 회화 등 특정 매체가 다른 형식과 다르게 가지는 표현 조건을 반영한", "아무 데나 옮겨도 같은 뜻이 아니라 그 매체만의 손맛이 살아 있는 느낌", "medium-specific=특정 매체의 고유 특성을 반영한 / transferable=다른 맥락으로 옮길 수 있는 / generic=일반적인"),
    ("montage", "몽타주 / 장면 조각을 이어 붙여 의미를 만드는 편집", "서로 다른 이미지나 순간을 연속으로 배치해 새로운 리듬과 연결을 만들어 내는 방식", "낱장면이 이어 붙는 순서 자체가 새로운 뜻을 만들어내는 느낌", "montage=장면을 이어 붙인 편집 구성 / collage=이미지 조각을 한 화면에 붙인 구성 / sequence=연속 배열"),
    ("nonlinear", "비선형의 / 순서가 한 줄로만 진행되지 않는", "시간, 원인, 전개가 곧장 일직선으로 이어지지 않고 되돌아가거나 갈라지는", "한 방향 직진보다 길이 접히고 돌아 나오는 흐름", "nonlinear=순서나 전개가 직선적이지 않은 / linear=일직선 순서의 / fragmented=조각난"),
    ("offscreen", "화면 밖의 / 보이지 않지만 장면에 영향을 주는", "카메라나 화면 안에 직접 보이지 않아도 소리나 시선으로 존재가 느껴지는", "눈앞 프레임 밖에서 무언가가 장면을 당기고 있는 느낌", "offscreen=화면 밖에 있는 / unseen=보이지 않는 / background=뒤쪽의"),
    ("ornamental", "장식적인 / 꾸미는 효과를 더하는", "핵심 기능보다 표면의 아름다움, 패턴, 시각적 풍부함을 위해 덧붙인 성격의", "구조를 떠받치기보다 겉면에 무늬와 결을 얹는 느낌", "ornamental=장식을 위한 / decorative=꾸밈의 / functional=기능적인"),
    ("pacing", "전개 속도 / 장면과 정보가 흘러가는 리듬", "이야기, 설명, 편집, 공연이 너무 빠르거나 느리지 않게 어떤 속도감으로 움직이는지", "무슨 일이 있느냐보다 그 일이 숨차게 가는지 천천히 번지는지를 조절하는 박자", "pacing=전개와 전달의 속도 조절 / rhythm=반복과 강약의 흐름 / timing=언제 맞춰 내는가"),
    ("performer", "수행자 / 무대나 장면에서 직접 표현하는 사람", "관람자가 아니라 연기, 연주, 발표, 낭독 등 행위를 실제로 몸과 목소리로 보여 주는 사람", "의미를 설명하는 사람이 아니라 몸으로 앞에서 구현하는 자리", "performer=직접 표현 행위를 하는 사람 / spectator=지켜보는 사람 / presenter=발표하는 사람"),
    ("poetics", "시학 / 표현이 어떻게 미적 효과를 만드는지의 원리", "특정 작품이나 장르가 언어, 이미지, 형식으로 의미와 아름다움을 구성하는 방식에 대한 틀", "내용 요약보다 표현의 결이 어떤 규칙으로 움직이는지 보는 느낌", "poetics=표현이 미적 효과를 만드는 원리 / aesthetics=아름다움과 감각의 기준 / rhetoric=설득과 표현 전략"),
    ("rehearsed", "리허설된 / 미리 연습하고 맞춘", "즉흥이 아니라 반복 연습을 통해 동작, 발화, 순서를 어느 정도 정돈해 둔", "처음 그 자리에서 나온 게 아니라 여러 번 몸에 맞춰 본 느낌", "rehearsed=미리 연습된 / improvised=즉흥적인 / scripted=대본에 따라 짠"),
    ("reinterpret", "재해석하다 / 기존 의미를 다른 틀로 다시 읽다", "이미 알려진 작품, 사건, 상징을 다른 시대나 관점에서 새 의미로 다시 보이게 하다", "같은 자료를 그대로 두고 읽는 렌즈를 바꿔 뜻을 다시 여는 느낌", "reinterpret=기존 것을 다른 관점으로 다시 해석하다 / revise=수정하다 / contextualize=맥락 속에 다시 놓다"),
    ("scenic", "경치 같은 / 장면성이 강한", "정보보다 눈앞에 펼쳐지는 시각적 배경과 공간감이 두드러지는", "설명문보다 풍경이 한 화면처럼 먼저 열리는 느낌", "scenic=시각적 장면성과 풍경감이 강한 / picturesque=그림처럼 보기 좋은 / descriptive=묘사적인"),
    ("scripted", "대본화된 / 미리 정한 문구와 순서에 따른", "발화나 행동이 현장에서 자유롭게 나온 것이 아니라 미리 짜인 텍스트와 흐름을 따르는", "즉석 반응보다 종이 위에 먼저 적힌 길을 따라가는 느낌", "scripted=대본과 정해진 순서를 따른 / improvised=즉흥적인 / rehearsed=연습된"),
    ("semiotic", "기호학적인 / 표지와 상징이 뜻을 어떻게 만드는지와 관련된", "이미지, 색, 몸짓, 단어가 단순한 물체를 넘어 어떤 의미를 표시하는지 분석하는", "눈에 보이는 것이 그냥 사물이 아니라 뜻을 띤 기호로 읽히는 느낌", "semiotic=기호와 의미 작동에 관한 / symbolic=상징적인 / semantic=언어 의미에 관한"),
    ("spatial arrangement", "공간 배치 / 요소를 어디에 놓는가의 짜임", "인물, 사물, 텍스트, 빈 공간이 어느 위치와 거리로 놓여 의미와 시선을 만드는지", "무엇이 있느냐만큼 그것들이 서로 어디 떨어져 놓였는지가 뜻이 되는 느낌", "spatial arrangement=요소의 공간적 배치 / composition=전체 구도 / layout=배치 설계"),
    ("symbolic weight", "상징적 무게 / 어떤 이미지가 지닌 의미의 큰 비중", "겉보기보다 역사, 기억, 가치, 정체성과 많이 연결되어 해석상 무겁게 작동하는 힘", "작은 대상인데 그 뒤에 큰 의미 덩어리가 매달려 있는 느낌", "symbolic weight=이미지가 가진 의미상의 무게 / significance=중요성 / visibility=눈에 띄는 정도"),
    ("textual evidence", "텍스트 근거 / 해석을 뒷받침하는 구체적 문구나 장면", "작품을 마음대로 말하지 않고 실제 문장, 묘사, 구조에서 끌어온 확인 가능한 근거", "해석을 허공에 띄우지 않고 본문 한 줄에 발을 딛게 하는 느낌", "textual evidence=본문에서 끌어온 구체적 근거 / interpretation=해석 / quotation=직접 인용"),
    ("visual metaphor", "시각적 은유 / 이미지로 다른 뜻을 빗대는 표현", "대상을 그대로 보여주는 것 같지만 장면이나 형태가 다른 추상 의미를 비춰 드러내는 방식", "그림 하나가 직접 설명 대신 다른 생각을 겹쳐 보여주는 느낌", "visual metaphor=이미지로 만든 은유 / symbol=의미를 대표하는 상징 / illustration=설명용 그림"),
    ("world-building", "세계 구축 / 작품 속 환경과 규칙을 설계함", "인물만이 아니라 장소, 제도, 분위기, 역사, 규칙을 세워 하나의 허구 세계를 설득력 있게 만드는 일", "배경이 납작한 종이가 아니라 들어가 살 수 있는 판으로 두꺼워지는 느낌", "world-building=작품 세계의 환경과 규칙을 구축함 / setting=배경 / storytelling=이야기 전달"),
    ("abstract", "추상적인 / 구체 사물보다 형태·개념·관계를 드러내는", "현실의 사물을 그대로 복사하기보다 선, 색, 구조, 개념으로 핵심을 덜어내 보여주는", "무엇을 닮았나보다 어떤 관계와 느낌만 남겨 뼈대를 세우는 느낌", "abstract=구체 형상을 덜어내고 개념·형태를 강조한 / concrete=구체적인 / realistic=사실적인"),
    ("audience-centered", "관객 중심의 / 보는 사람의 이해와 반응을 고려한", "창작자 내부 논리만이 아니라 수용자가 어떻게 보고 느끼고 따라올지를 함께 설계한", "만드는 쪽 만족보다 받아들이는 사람의 자리에서 다시 맞춰 보는 느낌", "audience-centered=수용자 반응과 이해를 중심에 둔 / author-centered=작가 의도 중심의 / accessible=이해하기 쉬운"),
    ("chiaroscuro", "명암 대비법 / 빛과 어둠의 강한 대비로 형상을 살리는 방식", "밝은 부분과 어두운 부분을 뚜렷하게 갈라 입체감, 긴장, 분위기를 만드는 표현", "빛이 닿은 면과 어둠이 먹은 면이 부딪히며 형태가 살아나는 느낌", "chiaroscuro=빛과 어둠의 강한 대비 표현 / contrast=대비 일반 / shading=명암을 넣는 기법"),
    ("coherent style", "일관된 스타일 / 표현 방식이 흩어지지 않고 맞물림", "색, 어조, 형식, 움직임이 따로 놀지 않고 하나의 인상과 원칙 아래 연결된 상태", "각 장면이 제각각 튀지 않고 같은 손의 리듬으로 묶이는 느낌", "coherent style=표현 방식이 일관되게 이어짐 / uniformity=획일성 / inconsistency=일관성 없음"),
    ("contrastive", "대조적인 / 차이를 일부러 부각하는", "서로 다른 색, 태도, 장면, 주장 등을 가까이 놓아 차이가 선명히 보이게 하는", "비슷하게 녹이는 게 아니라 다름이 더 날카롭게 보이게 맞세우는 느낌", "contrastive=차이를 부각하는 / comparative=비교하는 / harmonious=조화로운"),
    ("documentary-style", "다큐멘터리식의 / 실제 기록처럼 보이게 구성된", "허구나 해석이 있어도 인터뷰, 현장감, 기록 화면 같은 형식을 빌려 사실성을 높인", "꾸며 낸 이야기라도 현장 기록을 보는 듯한 질감을 입히는 느낌", "documentary-style=다큐 기록 방식처럼 구성된 / fictional=허구의 / observational=관찰 중심의"),
    ("expressive range", "표현 폭 / 감정과 의미를 드러낼 수 있는 범위", "한 가지 톤에 갇히지 않고 섬세함, 강함, 유머, 긴장 등 여러 결을 담아낼 수 있는 정도", "한 음만 내는 악기보다 넓은 음역으로 감정을 펼치는 느낌", "expressive range=표현할 수 있는 감정·의미의 폭 / versatility=다방면으로 쓸 수 있는 능력 / intensity=강도"),
    ("framing device", "프레이밍 장치 / 이야기를 어떤 틀로 보게 만드는 구조", "독자나 관객이 장면을 어떻게 이해해야 하는지 방향을 잡아 주는 서두, 바깥 이야기, 반복 구조 같은 장치", "내용 자체보다 그 내용을 어떤 액자에 넣어 보게 하느냐를 정하는 장치", "framing device=해석 틀을 만드는 서사 장치 / frame narrative=바깥 이야기가 안쪽 이야기를 감싸는 구조 / exposition=배경 설명"),
    ("genre convention", "장르 관습 / 특정 장르에서 기대되는 익숙한 규칙", "독자나 관객이 미스터리, 로맨스, 다큐, 강연 등에서 자연스럽게 예상하는 전개와 표현 방식", "새 작품도 아예 빈칸에서 시작하지 않고 익숙한 규칙 선을 밟는 느낌", "genre convention=특정 장르의 익숙한 규칙 / trope=자주 반복되는 장치나 유형 / innovation=새로운 변형"),
    ("gestural", "몸짓의 / 손·팔·자세 같은 동작 표현과 관련된", "언어 설명보다 움직임과 자세 자체가 감정, 의도, 리듬을 드러내는 성격의", "말보다 손끝과 몸의 선이 먼저 의미를 전달하는 느낌", "gestural=몸짓 표현과 관련된 / verbal=말의 / kinetic=움직임의"),
    ("handcrafted", "손으로 공들여 만든 듯한 / 수작업 느낌의", "기계적으로 균일한 인상보다 사람 손의 흔적, 작은 불규칙성, 공들인 제작감이 살아 있는", "매끈한 대량 생산보다 손이 직접 만진 온도가 남은 느낌", "handcrafted=수작업 감각이 살아 있는 / mass-produced=대량 생산된 / polished=매끈하게 다듬어진"),
    ("high-contrast", "고대비의 / 밝고 어두움이나 색 차이가 큰", "비슷한 톤으로 흐릿하게 섞이지 않고 서로 다른 밝기나 색이 강하게 갈라지는", "경계가 흐물하지 않고 빛과 색 차이가 눈에 확 부딪히는 느낌", "high-contrast=밝기·색 차이가 큰 / muted=색이나 대비가 눌린 / balanced=균형 잡힌"),
    ("imagery", "심상 / 머릿속에 떠오르는 감각적 이미지 표현", "말이나 장면이 독자에게 시각, 청각, 촉각 같은 구체적 감각 이미지를 불러오게 하는 표현", "문장이 정보만 주는 게 아니라 안쪽 스크린에 장면을 띄우는 느낌", "imagery=감각 이미지를 불러오는 표현 / symbolism=상징성 / description=묘사 일반"),
    ("mise-en-scene", "미장센 / 화면이나 무대 안 요소를 통째로 배치한 연출", "배우, 소품, 조명, 공간, 색을 한 프레임 안에 어떻게 놓아 의미를 만드는지의 전체 구성", "대사 하나보다 화면 안 모든 배치가 한꺼번에 의미를 밀어 올리는 느낌", "mise-en-scene=프레임 안 요소의 전체 연출 배치 / composition=구도 / staging=무대적 장면 배치"),
    ("motivic", "모티프적인 / 반복 요소가 의미를 엮는", "특정 이미지나 소리, 문구가 되풀이되며 작품 전체의 연결과 주제를 강화하는 성격의", "한 번 등장한 표식이 다시 돌아오며 숨은 실처럼 장면들을 묶는 느낌", "motivic=반복 모티프와 관련된 / thematic=주제와 관련된 / incidental=우연적이고 부차적인"),
    ("nonverbal cue", "비언어적 신호 / 말 없이 전달되는 단서", "표정, 시선, 자세, 침묵, 움직임처럼 언어 문장 없이도 관계와 감정을 알려 주는 표시", "입은 가만히 있어도 몸과 눈이 다른 말을 보내는 느낌", "nonverbal cue=말 없이 주는 신호 / auditory cue=소리 단서 / explicit statement=직접 말한 진술"),
    ("presentational", "제시 방식의 / 내용을 어떻게 보여주는지에 관한", "내용 자체보다 자료, 장면, 말이 어떤 순서와 형식으로 관객 앞에 배치되는지와 관련된", "무엇을 담았나만큼 그것을 어떤 겉모양과 순서로 내놓는지가 앞서는 느낌", "presentational=보여주는 형식과 제시에 관한 / substantive=내용 자체의 / visual=시각적인"),
    ("readability", "가독성 / 읽고 따라가기 쉬운 정도", "문장, 배열, 글자, 구조가 독자가 의미를 막힘없이 파악하기에 얼마나 편한지", "내용이 좋아도 눈과 머리가 덜 걸리고 술술 따라갈 수 있는지의 느낌", "readability=읽기 쉬운 정도 / legibility=글자 형태를 알아보기 쉬운 정도 / accessibility=접근하기 쉬운 정도"),
    ("rendering", "표현·재현 결과 / 어떤 방식으로 구현한 모습", "대상이나 아이디어를 그림, 말, 소리, 디지털 형식으로 바꾸어 나타낸 결과나 그 방식", "원래 것을 그대로 두지 않고 특정 표현 재료로 다시 빚어낸 모습", "rendering=어떤 방식으로 구현해 나타낸 결과 / depiction=묘사 / reproduction=복제"),
    ("repertoire", "레퍼토리 / 반복해서 활용할 수 있는 표현·기술의 목록", "공연곡만이 아니라 사람이 상황에 따라 꺼내 쓸 수 있는 방식, 기법, 반응의 축적된 범위", "필요할 때마다 꺼내 쓸 수 있게 몸이나 기억에 쌓인 카드 묶음", "repertoire=활용 가능한 표현·기술의 범위 / inventory=보유 목록 / routine=반복 절차"),
    ("screen-based", "화면 기반의 / 디지털 화면을 통해 전달되는", "종이, 실물, 현장 직접성이 아니라 모니터나 디스플레이를 주요 전달 창으로 삼는", "눈앞 물체보다 화면이라는 창을 통해 경험이 들어오는 느낌", "screen-based=화면을 주요 매체로 하는 / live=현장에서 직접 벌어지는 / print-based=인쇄물 기반의"),
    ("sequencing", "순서 배열 / 어떤 장면·정보를 어떤 차례로 놓는가", "개별 요소가 아니라 그것들을 어떤 전후 관계로 이어 배치해 이해와 감정을 조절하는 일", "재료가 같아도 놓는 순서가 바뀌면 흐름과 뜻이 달라지는 느낌", "sequencing=요소를 어떤 순서로 배열하는 일 / pacing=전개 속도 조절 / ordering=차례 정하기"),
    ("sonic", "소리의 / 음향적 특성과 관련된", "의미를 글뜻보다 소리의 질감, 울림, 높낮이, 공간감으로 전달하는 면과 관련된", "내용을 읽기보다 귀에 닿는 소리 결을 먼저 보는 느낌", "sonic=소리와 음향의 / auditory=청각의 / musical=음악적인"),
    ("spare", "군더더기 없는 / 표현을 일부러 적게 쓴", "감정이나 정보를 과하게 덧붙이지 않고 최소한의 요소만 남겨 절제된 효과를 만드는", "많이 말하지 않아서 오히려 남은 빈칸이 또렷해지는 느낌", "spare=표현이 군더더기 없이 절제된 / minimalist=요소를 덜어낸 양식의 / ornate=장식이 많은"),
    ("storyboard", "스토리보드 / 장면 순서를 그림과 메모로 미리 짠 계획", "완성 영상이나 공연 전에 각 장면이 어떻게 이어질지 시각적으로 배열한 설계판", "머릿속 장면을 바로 찍기 전에 칸칸이 펼쳐놓는 사전 지도", "storyboard=장면 순서를 미리 그림으로 짠 계획 / script=대본 / outline=개요"),
    ("symbol-laden", "상징이 많이 실린 / 의미를 덧입힌 이미지가 많은", "겉으로 단순한 사물에도 문화적·역사적 의미를 많이 얹어 해석하게 만드는", "작은 이미지들이 빈 장식이 아니라 의미 무게를 잔뜩 짊어진 느낌", "symbol-laden=상징 의미가 많이 실린 / decorative=장식적인 / literal=직접적인"),
    ("textile", "직물의 / 천과 짜임과 관련된", "재료의 실, 결, 짜임, 촉감이 표현이나 문화적 의미에 직접 연결되는", "색만 보는 게 아니라 섬유가 엮인 결 자체가 의미를 갖는 느낌", "textile=천과 짜임에 관한 / textured=질감이 살아 있는 / fabric=천 재료"),
    ("tonality", "색조·음조의 성격 / 전체 톤을 이루는 결", "시각에서는 색의 조화, 음악이나 말에서는 높낮이와 음색이 만들어내는 전체 분위기", "개별 음 하나보다 전체가 어떤 색과 음의 기운으로 물들어 있는지", "tonality=전체 색조·음조의 성격 / tone=어조나 정서적 색 / pitch=음의 높이"),
    ("voice modulation", "목소리 조절 / 톤·높이·강도를 바꿔 의미를 싣는 방식", "똑같은 문장이라도 목소리의 높낮이, 세기, 속도를 바꿔 태도와 감정을 다르게 전달하는 것", "문장의 뜻 위에 목소리의 파도 모양을 얹는 느낌", "voice modulation=목소리 톤과 강약을 조절함 / vocal delivery=목소리로 전달하는 방식 전체 / intonation=억양"),
    ("visual hierarchy", "시각적 위계 / 무엇을 먼저 보게 할지 정하는 화면상의 우선순위", "크기, 색, 위치, 여백, 굵기 차이로 관객 시선이 어떤 순서로 이동하게 할지 만든 구조", "눈이 아무 데나 헤매지 않고 중요한 것부터 차례로 끌리는 길", "visual hierarchy=시선의 우선순위를 만드는 시각 구조 / layout=배치 / emphasis=강조"),
    ("vividness", "생생함 / 장면이나 감각이 또렷하게 살아나는 정도", "표현이 흐릿한 개념에 머물지 않고 구체적 색, 소리, 움직임으로 선명하게 다가오는 힘", "설명만 남지 않고 장면이 눈앞에 확 켜지는 정도", "vividness=장면과 감각의 생생함 / clarity=명확성 / intensity=강도"),
    ("ambient sound", "주변음 / 배경에 깔려 공간감을 만드는 소리", "대사나 주 선율보다 공간의 실제성, 거리감, 분위기를 형성하는 환경 소리", "주인공처럼 튀진 않아도 장면의 공기를 귀로 채워 주는 소리층", "ambient sound=공간 분위기를 만드는 주변 소리 / soundtrack=작품에 쓰인 음악·음향 / noise=잡음"),
    ("artifice", "인공적 연출성 / 일부러 만들어낸 꾸밈의 흔적", "자연스럽게 그냥 놓인 것처럼 보이기보다 구성과 연출이 의도적으로 짜였다는 느낌", "현실 그대로인 척하지 않고 만든 손길의 흔적이 살짝 보이는 느낌", "artifice=의도적으로 만들어낸 연출성 / authenticity=진정성·실재감 / fabrication=조작이나 날조"),
    ("close-up", "클로즈업 / 대상을 가까이 당겨 세부를 크게 보여줌", "전체보다 얼굴, 손, 물건 일부를 크게 잡아 감정이나 단서를 강하게 부각하는 화면 방식", "멀리서 보던 장면을 코앞까지 당겨 작은 표정과 결을 크게 보게 하는 느낌", "close-up=대상을 가까이 크게 보여주는 화면 / wide shot=넓은 범위를 보여주는 화면 / detail=세부"),
    ("cross-cutting", "교차 편집 / 다른 장면을 번갈아 붙여 연결과 긴장을 만드는 방식", "서로 다른 장소나 행동을 순서대로 번갈아 보여 주며 동시성, 대비, 긴장을 만드는 편집", "한 장면만 오래 보는 대신 두 흐름을 오가며 줄을 팽팽하게 당기는 느낌", "cross-cutting=장면을 교차로 이어붙이는 편집 / montage=장면 조각을 이어 붙여 의미를 만드는 구성 / continuity editing=자연스러운 연결을 유지하는 편집"),
    ("evocation", "환기 / 직접 말하지 않고 감정·기억·장면을 불러냄", "설명을 다 채우기보다 이미지나 소리로 특정 느낌과 연상을 일으키는 작용", "닫힌 설명문보다 안쪽 기억을 두드려 깨우는 울림", "evocation=감정·기억·이미지를 불러일으킴 / explanation=설명 / depiction=묘사"),
    ("expressive gesture", "표현적 몸짓 / 감정과 의도를 드러내는 동작", "단순한 움직임이 아니라 관계, 태도, 감정선을 눈에 보이게 만드는 손짓과 자세", "말 한 줄보다 팔과 어깨의 방향이 감정을 먼저 열어 주는 느낌", "expressive gesture=감정·의도를 드러내는 몸짓 / body language=몸짓 신호 전체 / random movement=우연한 움직임"),
    ("framed shot", "프레임 잡힌 화면 / 어떤 경계 안에 대상을 배치한 샷", "무엇을 넣고 무엇을 자르며 어떤 거리와 구도로 보여줄지 정한 하나의 화면 구성", "세상이 통째로 보이는 게 아니라 사각 경계 안에 의미가 잘려 들어오는 느낌", "framed shot=프레임 안에 배치된 하나의 화면 / composition=구도 / camera angle=촬영 각도"),
    ("introspective", "성찰적인 / 바깥 사건보다 내면을 들여다보는", "행동의 규모보다 감정, 기억, 판단, 자기인식을 깊이 파고드는 성격의", "밖으로 크게 움직이기보다 안쪽 방으로 천천히 내려가는 느낌", "introspective=내면 성찰에 집중한 / reflective=되돌아보는 / outward-looking=바깥을 향한"),
    ("kinetic", "운동감 있는 / 움직임의 에너지가 강한", "멈춘 형태보다 몸, 선, 카메라, 리듬이 계속 움직이는 듯한 감각을 주는", "정지된 그림인데도 안에서 속도와 방향이 흐르는 느낌", "kinetic=움직임의 에너지가 느껴지는 / static=정적인 / gestural=몸짓과 관련된"),
    ("live rendition", "실황 해석·연주 / 현장에서 다시 표현한 버전", "기록된 원본을 그대로 재생하는 것이 아니라 현장에서 목소리, 템포, 분위기를 실어 새로 구현한 표현", "같은 곡이나 텍스트도 그 자리 공기 속에서 다시 살아나는 느낌", "live rendition=현장에서 다시 표현한 버전 / recording=녹음·기록물 / interpretation=해석"),
    ("mimetic", "모방적인 / 현실의 모습을 닮게 재현하는", "대상을 직접 닮도록 따라 그리거나 연기해 실제 모습과의 유사성을 강조하는", "원본과 비슷하게 비춰 보이려는 거울 같은 느낌", "mimetic=현실을 닮게 재현하는 / abstract=구체 형상을 덜어낸 / symbolic=상징적인"),
    ("mood-setting", "분위기 조성의 / 감정적 배경을 먼저 깔아 주는", "이야기 정보보다 색, 음악, 조명, 리듬으로 관객이 어떤 정서로 들어갈지 먼저 정하는", "본격 사건 전에 마음의 온도와 조명을 먼저 맞춰 놓는 느낌", "mood-setting=감정적 분위기를 먼저 조성하는 / scene-setting=장면 배경을 깔아 주는 / explanatory=설명적인"),
    ("narratorial", "서술자의 / 이야기를 누가 어떻게 말하는지와 관련된", "사건 자체보다 설명하는 목소리의 위치, 신뢰도, 태도, 정보 선택이 드러나는", "이야기 밖에서 누가 어떤 목소리로 안내하는지가 의미가 되는 느낌", "narratorial=서술자 목소리와 전달 방식의 / authorial=작가 관점의 / narrative=이야기 구조의"),
    ("oral storytelling", "구술 이야기 전달 / 말로 직접 들려주는 서사 방식", "글로 고정된 텍스트보다 목소리, 억양, 반복, 청중 반응을 타며 전해지는 이야기 방식", "종이 위 문장보다 입에서 입으로 살아 움직이는 이야기 결", "oral storytelling=말로 직접 전하는 서사 / written narrative=글로 쓴 이야기 / performance=수행 표현"),
    ("overstylized", "지나치게 양식화된 / 스타일이 과하게 앞서는", "현실감이나 자연스러움보다 특정 양식 효과가 너무 강해 인공적인 인상이 두드러지는", "스타일 필터가 너무 진해서 대상보다 양식 자체가 먼저 보이는 느낌", "overstylized=양식 효과가 과하게 강한 / stylized=의도적으로 양식화된 / naturalistic=자연스럽고 사실적인"),
    ("re-enactment", "재연 / 과거 장면이나 사건을 다시 연기해 보여줌", "이미 있었던 상황을 몸짓, 대사, 연출로 다시 구성해 관객이 보게 하는 것", "지나간 일을 설명만 하지 않고 다시 눈앞에서 한 번 돌려 보여주는 느낌", "re-enactment=과거 장면을 다시 연기해 보여줌 / reconstruction=자료로 다시 구성함 / rehearsal=미리 연습함"),
    ("scene transition", "장면 전환 / 한 장면에서 다음 장면으로 넘어감", "시간, 장소, 분위기, 시점이 바뀌며 관객이 새 단위로 이동하게 되는 연결 방식", "한 무대 조명이 꺼지고 다음 조명이 켜지며 시선이 옮겨가는 느낌", "scene transition=장면이 다음 단위로 넘어가는 것 / pacing=전개 속도 / cut=편집상 잘라 넘김"),
    ("semi-abstract", "반추상적인 / 현실 형상을 일부 남기되 단순화한", "완전히 알아볼 수 없는 추상은 아니지만 구체 사물을 부분적으로 덜어내고 형태를 변형한", "무엇인지 어렴풋이 보이지만 세부는 스타일 속으로 줄어든 느낌", "semi-abstract=현실 형상을 일부 남긴 추상적 표현 / abstract=구체 형상을 크게 덜어낸 / realistic=사실적인"),
    ("site-specific", "장소 특정적인 / 그 공간과 떼어내기 어렵게 설계된", "어느 곳에서나 똑같이 놓이는 것이 아니라 특정 장소의 역사, 구조, 동선, 분위기와 맞물려 의미가 생기는", "작품이 그냥 이동 가능한 물건이 아니라 그 장소에 뿌리를 내린 느낌", "site-specific=특정 장소와 결합해 의미가 생기는 / portable=옮기기 쉬운 / universal=장소와 덜 묶인"),
    ("sonority", "울림의 풍부함 / 소리의 공명감", "소리가 얇게 끝나지 않고 공간과 음색 안에서 얼마나 꽉 차고 깊게 울리는지의 성질", "한 음이 납작하지 않고 안쪽 공기까지 둥글게 진동하는 느낌", "sonority=소리의 풍부한 울림 / volume=소리 크기 / resonance=감정적·문화적 울림까지 포함할 수 있는 더 넓은 울림"),
    ("spatialized", "공간화된 / 위치와 거리감이 느껴지게 배치된", "소리나 이미지, 정보가 한 점에 뭉치지 않고 서로 다른 위치와 깊이를 가진 것처럼 구성된", "평평한 한 줄보다 앞뒤좌우로 펼쳐진 자리감이 생기는 느낌", "spatialized=공간상의 위치감이 나게 배치된 / flattened=납작하게 눌린 / localized=특정 위치에 국한된"),
    ("spectacle", "볼거리 중심의 장관 / 강한 시각적·감각적 효과", "내용의 논리보다 크기, 화려함, 움직임, 소리로 관객을 강하게 압도하는 장면성", "생각보다 먼저 눈과 귀를 확 잡아끄는 큰 무대 효과", "spectacle=강한 감각적 볼거리와 장관 / drama=갈등과 전개가 있는 극적 효과 / display=보여줌"),
    ("stylistic consistency", "양식적 일관성 / 표현 방식이 흔들리지 않고 이어짐", "작품이나 자료 전체에서 색, 어조, 선, 형식 선택이 서로 어긋나지 않고 하나의 규칙을 유지하는 상태", "장면마다 다른 손처럼 튀지 않고 같은 표현 결이 계속 이어지는 느낌", "stylistic consistency=표현 양식이 일관되게 유지됨 / coherence=전체가 잘 맞물리는 일관성 / variation=변화"),
    ("symbolic register", "상징의 층위 / 어느 수준의 의미 체계로 읽히는가", "이미지나 표현이 일상적 의미를 넘어 종교적, 정치적, 문화적 의미망 안에서 작동하는 층", "겉뜻 위에 더 큰 의미 언어가 얹혀 다른 높이로 읽히는 느낌", "symbolic register=상징 의미가 작동하는 층위 / literal meaning=직접 의미 / connotation=함축적 연상"),
    ("tonal shift", "어조 전환 / 분위기나 태도의 색이 바뀜", "작품이나 발화가 진지함에서 유머로, 차분함에서 긴장으로처럼 정서적 결을 바꾸는 변화", "같은 길 위에서 조명 색이 바뀌며 장면의 온도가 달라지는 느낌", "tonal shift=정서적 어조가 바뀌는 변화 / topic shift=화제가 바뀜 / pacing change=전개 속도가 바뀜"),
    ("visual motif", "시각 모티프 / 반복되는 이미지 요소", "특정 색, 형태, 사물, 구도가 반복 등장하며 장면들을 묶고 주제를 강화하는 이미지 단위", "다시 나타나는 작은 그림 표식이 작품 전체에 숨은 실을 거는 느낌", "visual motif=반복되는 이미지 요소 / symbol=특정 의미를 대표하는 상징 / pattern=반복되는 형태 일반"),
    ("vocal inflection", "목소리 굴곡 / 뜻과 감정을 싣는 억양 변화", "한 문장 안에서 높낮이와 세기를 어떻게 꺾고 올려 태도나 숨은 의미를 드러내는지", "글자는 같아도 목소리 끝이 살짝 꺾이며 다른 뜻이 비치는 느낌", "vocal inflection=목소리 높낮이와 세기의 변화 / intonation=문장 억양 / pronunciation=발음"),
    ("accessible style", "이해하기 쉬운 문체 / 수용자에게 열려 있는 표현 방식", "복잡한 내용도 독자나 관객이 과도한 배경지식 없이 따라오게 비교적 분명하고 열려 있게 전달하는 방식", "문턱을 높이지 않고 보는 사람이 안으로 들어오게 길을 열어 주는 느낌", "accessible style=수용자가 따라오기 쉬운 표현 방식 / plain style=간결하고 직접적인 문체 / esoteric style=소수만 이해하기 쉬운 난해한 방식"),
    ("curated sequence", "선별 배열 / 고른 항목을 어떤 순서로 보여주는 구성", "무엇을 포함할지만이 아니라 어떤 앞뒤 흐름으로 놓아 해석과 관심을 이끌지까지 정한 배열", "좋은 조각을 모으는 데서 끝나지 않고 보는 길까지 손으로 짜는 느낌", "curated sequence=선별한 항목을 의도적으로 배열한 순서 / sequencing=순서 배열 / random order=무작위 순서"),
    ("dramatic emphasis", "극적 강조 / 특정 순간이나 감정을 강하게 부각함", "조명, 속도, 목소리, 대비, 반복을 통해 어떤 장면이나 의미를 더 크게 느끼게 만드는 처리", "여러 요소 중 하나에 무대 조명을 더 세게 몰아 주는 느낌", "dramatic emphasis=특정 순간을 강하게 부각함 / subtle emphasis=은근한 강조 / exaggeration=과장"),
    ("expressive economy", "절제된 표현 효율 / 적은 요소로 큰 효과를 내는 방식", "많은 설명이나 장식을 더하지 않고 선택된 몇 가지 표현으로 의미와 감정을 밀도 있게 전달하는", "말을 많이 쌓지 않아도 한두 획이 큰 울림을 내는 느낌", "expressive economy=적은 표현으로 효과를 크게 내는 절제 / minimalism=덜어낸 양식 / verbosity=말이 많은 표현"),
    ("image-saturated", "이미지가 빽빽한 / 시각 요소가 매우 많은", "텍스트나 여백보다 이미지, 장면, 시각적 단서가 촘촘히 채워져 강한 인상을 주는", "화면에 빈칸보다 그림 조각들이 계속 밀려드는 느낌", "image-saturated=시각 이미지가 매우 많은 / sparse=성긴 / text-heavy=글이 많은"),
    ("layered interpretation", "겹겹의 해석 / 한 가지로 닫히지 않는 다층적 읽기", "작품이나 장면이 표면 의미, 문화 맥락, 상징, 감정선을 함께 품어 여러 수준으로 읽히는 것", "첫 번째 답 아래에 또 다른 읽기 층이 계속 접혀 있는 느낌", "layered interpretation=여러 층위로 읽는 해석 / single reading=하나로 닫힌 해석 / ambiguity=여러 뜻으로 열려 있음"),
    ("representational", "재현적인 / 현실이나 대상을 어떤 방식으로 나타내는", "작품이 현실 세계, 집단, 사건을 완전히 중립적으로 복사하는 것이 아니라 특정 방식으로 보여주는 것과 관련된", "대상을 그냥 놓지 않고 어떤 창으로 다시 보여주느냐가 앞서는 느낌", "representational=대상을 어떤 방식으로 재현하는 / abstract=구체 대상을 덜어낸 / symbolic=의미를 대표하는"),
]


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join([f"핵심 뜻: {core}", f"부가 뜻: {extra}", f"핵심 느낌: {feeling}", f"구분: {distinction}"])


def main() -> None:
    existing = set()
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            existing.update(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)

    rows = []
    for word, core, extra, feeling, distinction in CARDS:
        if word in existing:
            continue
        rows.append([word, build_back(core, extra, feeling, distinction)])
        if len(rows) == 100:
            break

    if len(rows) < 100:
        raise RuntimeError(f"only {len(rows)} cards")

    with TARGET.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)

    ets_words = []
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            ets_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")

    awl_words = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text("\n".join(sorted(set(ets_words + awl_words))) + "\n", encoding="utf-8")

    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if TARGET.name not in manifest["files_created"]:
        manifest["files_created"].insert(19, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    notes_path = ROOT / "generation_notes.md"
    notes_path.write_text(
        notes_path.read_text(encoding="utf-8").replace(
            "- ETS sets `01` to `19` exist, bringing the ETS-based total to 1900 cards\n",
            "- ETS sets `01` to `20` exist, bringing the ETS-based total to 2000 cards\n",
        ),
        encoding="utf-8",
    )

    plan_path = ROOT / "WORK_PLAN.md"
    plan_path.write_text(
        plan_path.read_text(encoding="utf-8")
        .replace(
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_19.tsv`\n",
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_20.tsv`\n",
        )
        .replace(
            "- Current ETS row count after the latest expansion pass: 1900\n",
            "- Current ETS row count after the latest expansion pass: 2000\n",
        ),
        encoding="utf-8",
    )

    task_next = ROOT / ".task_next.md"
    task_next.write_text(
        task_next.read_text(encoding="utf-8")
        .replace("`toefl_ets_2026_set_20.tsv`", "`toefl_ets_2026_set_21.tsv`")
        .replace(
            "creative works, visual/auditory representation, aesthetics, interpretation, and performance, with transferable culture-and-analysis vocabulary.",
            "social interaction, norms, participation, institutional behavior, and public communication, while keeping terms broadly reusable beyond one discipline.",
        ),
        encoding="utf-8",
    )

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
