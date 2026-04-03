from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_21.tsv"

CARDS = [
    ("affiliation", "소속 / 어떤 집단과 연결된 관계", "개인이 기관, 단체, 네트워크, 정체성 집단과 공식적·사회적으로 이어져 있는 상태", "혼자 떠 있는 점이 아니라 어느 울타리에 선을 대고 있는 느낌", "affiliation=집단과의 소속 관계 / membership=구성원 자격 / association=연결·연상"),
    ("agenda-setting", "의제 설정 / 무엇을 먼저 논의할지 정함", "여러 문제 중 어떤 주제를 공적 논의의 중심으로 끌어올릴지 방향을 잡는 일", "모든 말이 동시에 나오지 않게 토론판의 첫 줄을 정하는 느낌", "agenda-setting=공론장의 논의 우선순위를 정함 / prioritization=우선순위 정하기 / framing=어떤 틀로 보게 하는 방식"),
    ("allyship", "연대적 지지 / 직접 당사자가 아니어도 함께 편드는 태도", "자신이 중심 피해 당사자가 아니어도 불평등 문제에서 책임 있게 지지와 행동을 보태는 것", "밖에서 구경만 하지 않고 같은 편 줄에 서서 어깨를 붙이는 느낌", "allyship=당사자와 함께하는 지지와 연대 / sympathy=공감 / sponsorship=공식 후원"),
    ("asymmetry", "비대칭 / 양쪽 힘·정보·지위가 같지 않음", "상호작용하는 두 집단이나 개인이 자원, 권한, 정보에서 균형을 이루지 못하는 상태", "마주 보는 저울이 한쪽으로 기울어 출발선부터 다른 느낌", "asymmetry=양쪽이 균형을 이루지 못함 / inequality=불평등 / imbalance=균형이 어긋남"),
    ("backlash", "역풍 / 변화에 대한 반발", "새 정책, 사회 변화, 발언이 나온 뒤 이에 맞서 강한 저항이나 부정 반응이 되돌아오는 현상", "앞으로 밀어낸 힘에 뒤에서 반대로 확 치고 들어오는 바람", "backlash=변화나 조치에 대한 반발 역풍 / criticism=비판 / resistance=저항"),
    ("bystander", "방관자 / 현장에 있지만 직접 개입하지 않는 사람", "문제나 상호작용을 보고 있으면서도 당사자나 개입자로 들어가지 않고 옆에 머무는 사람", "장면 안에는 있지만 손을 안 대고 가장자리에서 보는 자리", "bystander=현장에 있으나 개입하지 않는 사람 / witness=목격자 / participant=참여자"),
    ("civic-minded", "시민의식이 있는 / 공공의 이익을 생각하는", "개인 이익만이 아니라 공동체 규범, 공적 책임, 사회적 참여를 염두에 두는", "내 일만 보는 게 아니라 모두가 쓰는 길의 상태도 같이 보는 느낌", "civic-minded=공공 책임과 시민 참여를 중시하는 / public-spirited=공익 지향적인 / self-interested=자기 이익 중심의"),
    ("coalition-building", "연합 형성 / 여러 집단을 묶어 공동전선을 만듦", "이해관계가 완전히 같지 않은 집단들도 공통 목표를 중심으로 협력 구조를 만들어 가는 일", "따로 흩어진 선들을 하나의 굵은 밧줄로 묶는 느낌", "coalition-building=여러 집단을 연합으로 묶음 / collaboration=협력 / alliance=동맹"),
    ("cohesion", "결속력 / 집단이 흩어지지 않고 묶이는 힘", "구성원들이 서로 완전히 따로 놀지 않고 공동 규범과 소속감으로 연결되는 정도", "여러 조각이 쉽게 떨어지지 않게 안쪽 접착력이 살아 있는 느낌", "cohesion=집단을 묶는 결속력 / solidarity=연대감 / coherence=논리·구성의 일관성"),
    ("communal", "공동체의 / 함께 나누고 유지하는", "개인 단위보다 공동의 공간, 책임, 기억, 자원과 연결된 성격의", "혼자 소유한 물건보다 여럿이 함께 쓰고 지키는 울타리 안의 느낌", "communal=공동체가 함께 나누는 / collective=집단 전체의 / personal=개인의"),
    ("conformity", "동조 / 집단 규범에 맞추려는 경향", "자신의 판단을 완전히 숨기지 않더라도 집단 기대와 어긋나지 않게 행동이나 의견을 맞추는 성향", "튀는 방향보다 주변 줄에 발을 맞춰 들어가는 느낌", "conformity=집단 기준에 맞춰 따르는 경향 / compliance=규칙이나 요구를 따름 / independence=독자성"),
    ("consensus-building", "합의 형성 / 여러 의견을 모아 공통 결론을 만드는 과정", "한쪽이 일방적으로 밀기보다 서로의 차이를 조정해 같이 받아들일 수 있는 결론을 만드는 일", "각자 흩어진 목소리를 겹치는 가운데 지점으로 천천히 모으는 느낌", "consensus-building=공통 합의를 만들어 가는 과정 / negotiation=조건을 조율하는 협상 / persuasion=설득"),
    ("cultural fluency", "문화적 유창성 / 다른 문화 규범을 읽고 맞춰 소통하는 능력", "언어만 아는 것을 넘어 상대 집단의 예의, 암묵 규칙, 맥락을 이해하며 상호작용하는 능력", "단어는 맞아도 어색하지 않게 그 문화의 숨은 리듬까지 타는 느낌", "cultural fluency=문화 규범을 읽고 자연스럽게 소통하는 능력 / language fluency=언어 유창성 / cultural awareness=문화 인식"),
    ("deliberative", "숙의적인 / 충분히 논의하며 판단하는", "즉각 반응보다 이유, 근거, 대안, 공적 영향을 두고 차분히 따져 보는 성격의", "한 번에 찍지 않고 여러 목소리를 올려놓고 천천히 저울질하는 느낌", "deliberative=토론과 숙고를 거쳐 판단하는 / impulsive=충동적인 / reflective=되돌아보는"),
    ("dissenting", "이견을 내는 / 다수 의견에 반대하는", "지배적 합의나 공식 입장과 같은 줄에 서지 않고 다른 판단을 드러내는", "모두 같은 방향으로 손들 때 옆에서 다른 팻말을 드는 느낌", "dissenting=다수·공식 의견에 반대하는 / critical=비판적인 / supportive=지지하는"),
    ("disenfranchised", "권리에서 배제된 / 정치·사회 참여 힘이 약한", "법적·제도적·사회적 이유로 자신의 목소리를 충분히 내거나 영향력을 행사하기 어려운 상태의", "회의장은 열려 있어도 내 표와 말이 문턱 밖으로 밀려난 느낌", "disenfranchised=참여 권한과 영향력에서 배제된 / marginalized=주변화된 / empowered=힘과 권한을 가진"),
    ("egalitarian", "평등주의적인 / 지위 차이를 덜 강조하는", "특정 신분이나 권위가 과도하게 우위에 서지 않고 비교적 동등한 권리와 대우를 중시하는", "줄의 맨 위와 아래를 강하게 갈라놓기보다 평평한 바닥을 만들려는 느낌", "egalitarian=평등한 관계와 대우를 중시하는 / hierarchical=위계적인 / inclusive=포용적인"),
    ("etiquette", "예절 / 상황에 맞는 사회적 행동 규범", "공식 법보다 더 부드러운 수준에서 어떤 자리에서 어떻게 말하고 행동해야 하는지를 정하는 관습", "틀리면 처벌받기보다 분위기가 어색해지는 보이지 않는 행동 규칙", "etiquette=사회적 예절과 관습 규범 / protocol=공식 절차와 의례 / manners=예의범절"),
    ("grassroots", "풀뿌리의 / 현장 시민에서 아래로부터 올라오는", "정부나 중앙 조직이 먼저 내려보내는 방식이 아니라 지역 구성원과 일반 참여자가 기반이 되는", "위에서 설계된 탑보다 땅 아래 잔뿌리에서 힘이 올라오는 느낌", "grassroots=아래로부터 시민 기반의 / top-down=위에서 아래로 내려오는 / local=지역의"),
    ("gatekeeping", "진입 통제 / 누가 들어오거나 인정받을지 가르는 일", "정보, 자원, 자격, 발표 기회에 접근할 수 있는 사람과 없는 사람을 선별하거나 막는 구조", "문 앞에서 열쇠를 쥔 쪽이 누구를 들여보낼지 고르는 느낌", "gatekeeping=접근과 인정의 문을 통제함 / screening=선별함 / exclusion=배제"),
    ("hierarchical", "위계적인 / 윗단과 아랫단이 뚜렷이 나뉜", "사람이나 조직이 동등한 수평 관계보다 지위와 명령선에 따라 층층이 배열된", "한 평면이 아니라 위아래 계단이 선명한 구조", "hierarchical=지위와 권한이 층층이 나뉜 / egalitarian=평등주의적인 / centralized=중앙에 권한이 몰린"),
    ("inclusivity", "포용성 / 다양한 사람이 배제되지 않고 함께 들어오는 정도", "특정 배경이나 정체성의 사람만 편하게 들어오는 구조가 아니라 더 많은 사람이 참여하고 존중받게 하는 성질", "문이 좁게 한 줄만 통과시키지 않고 여러 사람이 들어올 수 있게 열리는 느낌", "inclusivity=다양한 사람을 배제하지 않고 받아들이는 성질 / diversity=구성의 다양성 / tolerance=관용"),
    ("interpersonal", "대인 관계의 / 사람 사이 상호작용과 관련된", "개인 내부보다 두 사람 이상이 서로 말하고 반응하고 관계를 조정하는 방식에 관한", "머릿속 혼잣말보다 사람과 사람 사이 공간에서 일이 생기는 느낌", "interpersonal=사람 사이 상호작용의 / intrapersonal=개인 내면의 / social=사회적인"),
    ("legitimacy", "정당성 / 받아들여질 만한 근거와 승인", "단순히 힘이 있다는 뜻보다 제도나 공동체가 그 결정과 권위를 옳고 타당하다고 인정하는 정도", "억지로 밀어붙인 힘이 아니라 주변이 고개를 끄덕일 만한 자격을 얻는 느낌", "legitimacy=권위나 결정이 정당하다고 인정받는 상태 / legality=법적으로 적법함 / authority=권한"),
    ("liaison", "연락·조정 담당자 / 두 집단 사이 연결 창구", "서로 다른 부서, 기관, 집단이 직접 어긋나지 않도록 정보를 넘기고 협의를 잇는 사람이나 역할", "끊어진 두 방 사이에 계속 오가며 말을 이어주는 다리", "liaison=두 집단을 잇는 조정 창구 / representative=대표자 / mediator=갈등을 중재하는 사람"),
    ("marginalized", "주변화된 / 중심 결정과 인정에서 밀려난", "수나 존재가 없다는 뜻이 아니라 권력, 자원, 가시성, 발언권에서 중심 자리 밖으로 밀린", "방 안에 있어도 테이블 가운데가 아니라 벽 쪽으로 밀려난 느낌", "marginalized=사회적 중심과 자원에서 밀려난 / disenfranchised=참여 권한이 약한 / minority=수적으로 적은 집단"),
    ("mediation", "중재 / 사이에서 갈등과 오해를 조정함", "대립하는 쪽들이 직접 부딪혀 굳어지지 않도록 제3자가 말과 조건을 조율해 접점을 찾게 돕는 과정", "두 줄이 정면충돌하지 않게 가운데에서 매듭을 풀어 주는 느낌", "mediation=제3자가 갈등을 조정하는 중재 / negotiation=당사자 간 협상 / arbitration=중재자가 판정하는 절차"),
    ("mobilize", "동원하다 / 사람과 자원을 행동으로 모아 움직이게 하다", "흩어진 지지, 인력, 자금, 관심을 실제 참여나 캠페인 행동으로 전환해 모으다", "가만히 있던 힘을 불러 모아 한 방향으로 걷게 만드는 느낌", "mobilize=사람과 자원을 모아 행동하게 하다 / recruit=새로 끌어모으다 / activate=작동시키다"),
    ("normative", "규범적인 / 무엇이 옳고 바람직한지 기준을 두는", "사실이 어떻게 되었는지만 말하기보다 어떤 기준대로 해야 한다는 판단이 들어간", "있는 그대로 묘사보다 이래야 한다는 잣대가 같이 서 있는 느낌", "normative=옳고 바람직함의 기준을 담은 / descriptive=있는 그대로 설명하는 / prescriptive=어떻게 해야 한다고 처방하는"),
    ("peer pressure", "또래 압력 / 주변 집단에 맞추라는 사회적 압박", "공식 명령이 없어도 같은 집단 사람들의 기대와 시선 때문에 특정 행동을 따르게 되는 압력", "누가 손목을 잡진 않아도 주변 눈빛이 같은 줄로 밀어 넣는 느낌", "peer pressure=주변 또래 집단이 주는 동조 압력 / social influence=사회적 영향 / coercion=강압"),
    ("participatory", "참여형의 / 구성원이 직접 관여하는", "전문가나 상층부만 결정하지 않고 영향을 받는 사람들도 과정에 들어와 의견과 실행을 나누는", "객석에 앉혀두지 않고 무대와 회의 테이블 안으로 끌어들이는 느낌", "participatory=구성원이 직접 참여하는 / consultative=의견을 묻는 / passive=수동적인"),
    ("polarization", "양극화 / 입장과 집단이 서로 더 갈라짐", "중간 지점에서 섞이기보다 두 진영이 더 멀리 벌어지고 상대를 덜 받아들이게 되는 현상", "가운데 다리가 얇아지고 양끝 언덕이 서로 더 멀어지는 느낌", "polarization=입장과 집단이 양끝으로 갈라짐 / disagreement=의견 불일치 / segmentation=여러 조각으로 나뉨"),
    ("public-facing", "대중을 직접 상대하는 / 외부 공개 접점의", "내부 문서나 백오피스가 아니라 시민, 사용자, 방문자, 독자가 직접 보고 이용하는 쪽에 놓인", "건물 뒤 사무실보다 사람들이 드나드는 앞문 쪽에 서 있는 느낌", "public-facing=외부 대중과 직접 맞닿는 / internal=내부용의 / outward-facing=바깥을 향한"),
    ("rapport", "라포 / 편하게 소통하는 신뢰 관계", "서로 경직된 거리만 두지 않고 대화가 비교적 자연스럽고 신뢰 있게 이어지는 관계의 질", "문장만 오가는 게 아니라 사이 공기가 조금 부드럽게 풀린 느낌", "rapport=편하게 소통하는 신뢰감 있는 관계 / trust=신뢰 / familiarity=익숙함"),
    ("reciprocity", "상호성 / 한쪽만이 아니라 서로 주고받는 원리", "지원, 호의, 협력, 책임이 일방향으로만 흐르지 않고 서로 오가는 기대와 구조", "한쪽에서만 계속 보내지 않고 공이 다시 돌아오는 느낌", "reciprocity=서로 주고받는 상호성 / mutuality=서로 함께하는 성질 / one-sidedness=일방성"),
    ("representative body", "대표 기구 / 구성원을 대신해 의견과 결정을 다루는 조직", "전체 구성원이 매번 직접 나서지 않아도 선출되거나 지정된 대표들이 논의와 결정을 맡는 구조", "사람들의 목소리가 한 명씩 흩어지지 않고 대표 테이블로 모이는 느낌", "representative body=구성원을 대신해 논의·결정을 맡는 조직 / committee=위원회 / constituency=대표받는 집단"),
    ("sanction", "제재 / 규범 위반에 대해 가하는 불이익", "공동체나 제도가 규칙을 어긴 행동에 대해 공식적·사회적으로 주는 불이익이나 제한", "규칙을 넘었을 때 그냥 지나가지 않고 되돌아오는 벌점 같은 힘", "sanction=규범 위반에 대한 제재 / penalty=벌칙 / approval=승인"),
    ("social capital", "사회적 자본 / 관계망과 신뢰에서 나오는 자원", "돈이나 지위 자체보다 사람 사이 연결, 평판, 호혜, 신뢰가 실제 기회와 협력을 열어 주는 힘", "통장 잔고가 아니라 사람 사이 선들이 나중에 문을 열어 주는 자산", "social capital=관계와 신뢰에서 나오는 자원 / economic capital=경제적 자본 / network=관계망"),
    ("social cue", "사회적 단서 / 상황과 관계를 읽게 하는 신호", "표정, 말투, 침묵, 거리, 호칭처럼 지금 어떻게 행동해야 하는지 알려 주는 대인 신호", "규칙 책 대신 사람들 반응과 공기에서 읽히는 작은 표지판", "social cue=사회적 상황을 읽게 하는 신호 / nonverbal cue=말 없는 단서 / signal=신호 일반"),
    ("stakeholder dialogue", "이해관계자 대화 / 관련 집단 간 공식적 소통", "영향을 받는 여러 집단이 각자의 우려와 요구를 드러내고 조정하는 논의 과정", "한쪽 발표로 끝내지 않고 여러 자리의 목소리를 같은 테이블 위에 올리는 느낌", "stakeholder dialogue=이해관계자 간 소통과 조정 / public hearing=공청회 / consultation=의견 수렴"),
    ("stigma", "낙인 / 특정 집단이나 상태에 붙는 부정적 사회표지", "개인의 실제 모습보다 사회가 특정 특성에 부정적 의미를 붙여 거리와 차별을 만드는 효과", "피부에 실제로 적힌 건 아닌데 주변 시선이 보이지 않는 딱지를 붙이는 느낌", "stigma=부정적 사회 낙인 / stereotype=고정된 단순화 이미지 / prejudice=편견"),
    ("trust-building", "신뢰 형성 / 서로 믿고 협력할 기반을 쌓음", "한 번의 약속보다 반복된 투명한 소통과 책임 있는 행동을 통해 관계의 신뢰도를 높이는 과정", "말 한마디보다 시간에 걸쳐 천천히 다리를 놓는 느낌", "trust-building=관계의 신뢰 기반을 쌓음 / rapport-building=편한 소통 관계를 만듦 / persuasion=설득"),
    ("unanimity", "만장일치 / 모두가 같은 결론에 동의함", "대부분이 아니라 참여한 구성원 전원이 공식적으로 같은 입장을 취하는 상태", "회의 테이블에서 손이 하나도 빠지지 않고 같은 방향으로 올라간 느낌", "unanimity=전원이 같은 결론에 동의함 / consensus=대체로 함께 받아들일 수 있는 합의 / majority=다수"),
    ("voice", "발언권 / 자기 관점이 드러나고 들릴 수 있는 힘", "문장 그대로의 목소리만이 아니라 공동체나 제도 안에서 자기 경험과 입장을 표현하고 인정받는 자리", "말소리가 있다는 뜻보다 그 말이 묻히지 않고 테이블 위에 놓이는 느낌", "voice=자기 입장을 드러내고 들리게 할 수 있는 자리와 힘 / opinion=의견 / representation=대변"),
    ("whistleblower", "내부고발자 / 조직 안 문제를 밖으로 알리는 사람", "조직 내부에서 본 위법, 부정, 위험을 침묵하지 않고 신고하거나 공개하는 사람", "안쪽에서 덮인 문제를 문 밖으로 들고 나오는 사람", "whistleblower=내부 문제를 신고·공개하는 사람 / informant=정보 제공자 / dissenter=이견을 내는 사람"),
    ("advisory role", "자문 역할 / 직접 결정보다 조언과 권고를 맡는 위치", "최종 결정을 직접 내리는 자리보다 근거와 관점을 제공해 판단을 돕는 역할", "운전대를 잡기보다 옆자리에서 지도와 해석을 건네는 느낌", "advisory role=결정을 돕는 자문 역할 / decision-making role=직접 결정 역할 / support role=보조 역할"),
    ("behavioral norm", "행동 규범 / 이 상황에서 보통 기대되는 행동 기준", "법처럼 강제적이지 않아도 특정 집단이나 장소에서 일반적으로 따라야 한다고 여겨지는 행동 방식", "종이에 안 적혀도 다들 아는 듯 맞춰 걷는 보이지 않는 선", "behavioral norm=기대되는 행동 기준 / rule=명시적 규칙 / custom=오래 이어진 관습"),
    ("bridge-building", "가교 형성 / 갈라진 집단 사이 연결을 만드는 일", "서로 불신하거나 따로 움직이던 사람들 사이에 대화와 협력의 통로를 여는 과정", "끊어진 양쪽 둑 사이에 다시 건널 수 있는 판을 놓는 느낌", "bridge-building=집단 사이 연결과 신뢰를 만드는 일 / mediation=갈등 중재 / outreach=외부와 연결하려는 접근"),
    ("collective voice", "집단적 목소리 / 여러 사람의 요구와 관점을 함께 드러내는 힘", "개별 의견이 흩어질 때보다 공동의 입장으로 묶여 더 크게 들리는 표현과 대표성", "작은 목소리들이 합쳐져 하나의 더 굵은 파동이 되는 느낌", "collective voice=여러 사람의 입장을 함께 드러내는 목소리 / individual voice=개인 목소리 / consensus=합의"),
    ("conduct code", "행동 강령 / 어떤 기준으로 행동해야 하는지 적은 규범", "구성원이 서로와 외부를 대할 때 지켜야 할 기준, 금지, 절차를 정리한 문서나 규칙 체계", "막연한 좋은 태도가 아니라 어디까지 되고 안 되는지 선을 그어 둔 안내판", "conduct code=행동 기준을 정한 강령 / guideline=지침 / law=법"),
    ("conflict de-escalation", "갈등 완화 / 긴장과 공격성을 낮추는 대응", "대립이 더 크게 번지지 않도록 말투, 절차, 거리 조정, 중재로 상황의 열기를 내리는 것", "불꽃에 바람을 더 넣지 않고 온도를 천천히 낮춰 폭발을 막는 느낌", "conflict de-escalation=갈등의 긴장을 낮춤 / mediation=중재 / compromise=절충"),
    ("consultative", "의견 수렴형의 / 결정 전 관련자 의견을 듣는", "한쪽이 혼자 확정하기보다 영향을 받는 사람들에게 의견을 묻고 반영 가능성을 여는 방식의", "닫힌 방 안에서 정하지 않고 문을 열어 목소리를 먼저 듣는 느낌", "consultative=관련자 의견을 듣는 방식의 / participatory=당사자가 직접 참여하는 / unilateral=일방적인"),
    ("community liaison", "지역사회 연락 담당 / 기관과 주민 사이를 잇는 창구", "조직이 지역 주민이나 외부 집단과 소통하고 우려를 전달받도록 중간 다리를 맡는 사람이나 역할", "기관 건물과 동네 사이를 오가며 말이 끊기지 않게 잇는 사람", "community liaison=기관과 지역사회를 잇는 연락 담당 / liaison=연결 창구 일반 / spokesperson=대변인"),
    ("cross-cultural", "문화 간의 / 서로 다른 문화가 만나는", "한 문화 내부만이 아니라 서로 다른 관습, 가치, 소통 방식이 부딪히고 조정되는 상황과 관련된", "각자 다른 규칙으로 움직이던 사람들이 한 장면에서 만나는 느낌", "cross-cultural=서로 다른 문화 사이의 / multicultural=여러 문화가 공존하는 / intercultural=문화 간 상호작용을 강조하는"),
    ("dispute resolution", "분쟁 해결 / 갈등을 절차와 조정으로 풀어냄", "의견 충돌이나 권리 다툼을 그냥 오래 끌지 않고 협상, 중재, 합의 절차로 정리하는 일", "서로 당기던 줄을 끊지 않고 매듭을 풀어 다시 정리하는 느낌", "dispute resolution=분쟁을 절차적으로 해결함 / mediation=중재 / litigation=법적 소송"),
    ("engagement level", "참여 수준 / 얼마나 적극적으로 관여하는가", "사람들이 단순히 존재만 하는지, 실제 응답·토론·행동에 얼마나 깊이 들어오는지를 나타내는 정도", "자리에 앉아만 있는지 아니면 몸을 앞으로 기울여 손을 드는지의 차이", "engagement level=관여와 참여의 정도 / attendance=출석 / commitment=헌신"),
    ("group dynamic", "집단 역학 / 구성원 사이 힘과 상호작용의 패턴", "누가 말하고 누가 침묵하며 어떤 연합과 긴장이 생기는지처럼 집단 안에서 움직이는 관계 구조", "각 개인 성격만이 아니라 사람들 사이 보이지 않는 힘줄이 움직이는 느낌", "group dynamic=집단 내부 상호작용과 힘의 패턴 / team climate=팀 분위기 / social structure=사회적 구조"),
    ("host community", "수용 공동체 / 외부인이나 프로그램을 받아들이는 지역사회", "방문자, 이주자, 프로젝트, 시설이 들어올 때 그것을 맞이하고 영향을 받는 기존 공동체", "밖에서 들어오는 것을 빈 공간이 아니라 이미 살던 사람들이 맞아들이는 자리", "host community=외부 사람이나 사업을 받아들이는 기존 지역사회 / local residents=지역 주민 / target community=사업 대상 공동체"),
    ("identity-based", "정체성 기반의 / 집단 소속과 자기인식에 근거한", "개인의 선택을 단순 취향보다 성별, 언어, 지역, 인종, 세대 같은 사회적 정체성과 연결해 보는", "무작위 개인이 아니라 내가 어느 이름표 아래 서 있는지가 영향을 주는 느낌", "identity-based=사회적 정체성에 근거한 / individual=개인적인 / demographic=인구집단 특성의"),
    ("informal norm", "비공식 규범 / 문서보다 관습으로 지켜지는 기준", "규칙집에 분명히 쓰이지 않아도 구성원이 경험으로 익혀 따르는 행동 기대", "종이는 없지만 어기면 다들 금방 눈치채는 암묵적 선", "informal norm=암묵적·비공식 행동 기준 / formal rule=명시적 공식 규칙 / habit=개인 습관"),
    ("institutional trust", "제도 신뢰 / 기관과 절차가 공정하고 믿을 만하다고 보는 정도", "개인 호감이 아니라 학교, 정부, 조직, 절차가 약속과 기준을 지킬 것이라는 공적 믿음", "사람 하나보다 제도라는 기계가 임의로 흔들리지 않을 거라 기대하는 느낌", "institutional trust=기관과 절차에 대한 신뢰 / personal trust=개인에 대한 신뢰 / legitimacy=정당성 인정"),
    ("intergroup", "집단 간의 / 서로 다른 사회 집단 사이에서 생기는", "한 집단 내부가 아니라 서로 다른 소속과 정체성을 가진 집단들이 만나고 비교되고 긴장하는 관계와 관련된", "방 하나 안의 대화보다 서로 다른 울타리 사이에 선이 오가는 느낌", "intergroup=집단 사이의 / intragroup=집단 내부의 / interpersonal=개인 사이의"),
    ("lived experience", "실제 삶의 경험 / 당사자로 겪으며 쌓인 체감", "통계나 외부 관찰만으로는 다 담기지 않는, 직접 그 조건 속에서 살아온 사람의 경험과 감각", "밖에서 본 보고서보다 안에서 몸으로 지나온 흔적이 말하는 느낌", "lived experience=당사자로 직접 겪은 삶의 경험 / observation=관찰 / anecdote=일화"),
    ("majoritarian", "다수결 중심의 / 다수의 뜻을 우선하는", "전체 합의나 소수 보호보다 숫자상 많은 쪽의 선호와 결정을 더 강하게 반영하는 성격의", "모든 목소리를 고르게 재기보다 가장 큰 덩어리의 표가 방향을 잡는 느낌", "majoritarian=다수의 뜻을 우선하는 / pluralistic=여러 집단 공존을 인정하는 / unanimous=전원 일치의"),
    ("mutual obligation", "상호 의무 / 서로에게 책임과 기대를 지는 관계", "한쪽만 도와주는 구조가 아니라 관계 속 각자가 상대에게 일정한 책임과 응답성을 갖는 상태", "받기만 하는 줄이 아니라 양쪽에 같이 묶인 약속 매듭", "mutual obligation=서로에게 책임과 의무를 짐 / reciprocity=서로 주고받는 상호성 / dependency=의존 관계"),
    ("opinion climate", "여론 분위기 / 어떤 의견이 말하기 쉽거나 어려운 공기", "사람들이 자기 생각을 내기 전에 주변이 어느 입장을 더 안전하고 정상으로 보는지 형성된 공적 분위기", "같은 의견이라도 이 방 공기에서는 쉽게 나오고 저 방에서는 삼키게 되는 느낌", "opinion climate=의견 표현을 둘러싼 사회적 분위기 / public opinion=여론 내용 / social norm=사회 규범"),
    ("participation barrier", "참여 장벽 / 참여를 어렵게 만드는 조건", "관심이 없어서가 아니라 비용, 언어, 시간, 접근성, 위계 때문에 실제 참여가 막히는 요소", "문은 있는 것 같지만 입구 앞에 낮지 않은 턱이 놓인 느낌", "participation barrier=참여를 가로막는 조건 / access barrier=접근 장벽 / reluctance=꺼림"),
    ("peer recognition", "동료 인정 / 같은 집단 구성원에게서 받는 평가와 승인", "권위자 보상보다 함께 일하거나 비슷한 위치에 있는 사람들이 능력과 기여를 인정하는 것", "위에서 찍는 도장보다 옆자리 사람들이 고개를 끄덕이는 힘", "peer recognition=동료 집단이 주는 인정 / official recognition=공식 인정 / popularity=인기"),
    ("pluralistic", "다원주의적인 / 여러 입장과 집단이 함께 존재함을 인정하는", "한 기준이나 정체성으로 모두를 밀어넣기보다 서로 다른 가치와 방식이 공존할 수 있다고 보는", "한 색으로 덮기보다 여러 색이 같은 판에 같이 놓일 자리를 여는 느낌", "pluralistic=다양한 집단과 입장의 공존을 인정하는 / majoritarian=다수 우선의 / homogeneous=동질적인"),
    ("public deliberation", "공적 숙의 / 공동 문제를 공개적으로 근거를 두고 토론함", "개인끼리만 속삭이는 수준이 아니라 공동체 문제를 공개된 장에서 이유와 대안을 놓고 논의하는 과정", "숨은 거래보다 밝은 테이블 위에서 이유를 펴놓고 함께 따지는 느낌", "public deliberation=공동 문제에 대한 공개적 숙의 / debate=논쟁 / consultation=의견 수렴"),
    ("rule compliance", "규칙 준수 / 정해진 기준과 절차를 따름", "규범을 알고만 있는 것이 아니라 실제 행동과 운영이 그 기준 안에 머무는 상태", "선을 알고 지나치는 게 아니라 발이 선 안쪽에 머무는 느낌", "rule compliance=규칙과 절차를 따름 / conformity=집단 기대에 동조함 / enforcement=집행"),
    ("social accountability", "사회적 책임성 / 행동을 공동체 앞에서 설명하고 책임지는 성질", "개인이나 조직이 자기 결정의 영향을 외면하지 않고 공적 기준과 타인의 평가 앞에서 답할 수 있어야 한다는 성질", "혼자 닫아두지 않고 내 선택을 사람들 앞에 내놓고 설명해야 하는 느낌", "social accountability=공동체 앞에서 행동 책임을 지는 성질 / transparency=투명성 / obligation=의무"),
    ("spokesperson", "대변인 / 조직이나 집단 입장을 공식적으로 말하는 사람", "개인 의견보다 조직의 공식 메시지를 외부에 전달하고 질문에 대응하는 역할", "자기 말보다 뒤에 선 집단의 목소리를 앞에서 대신 꺼내는 사람", "spokesperson=조직 입장을 공식적으로 말하는 사람 / representative=대표자 / liaison=연결 담당자"),
    ("status-seeking", "지위 추구적인 / 인정과 서열 상승을 노리는", "행동의 목적이 내용 자체보다 더 높은 평가, 권위, 눈에 띄는 위치를 얻는 데 많이 향한", "무슨 일을 하느냐보다 사다리에서 한 칸 더 위로 보이려는 움직임", "status-seeking=지위와 인정 상승을 추구하는 / achievement-oriented=성과를 중시하는 / altruistic=이타적인"),
    ("subgroup", "하위 집단 / 큰 집단 안에서 다시 나뉜 작은 묶음", "전체 공동체나 조직 안에 공통 관심, 역할, 정체성으로 따로 구분되는 작은 집단", "한 큰 원 안에 다시 작은 원들이 접혀 있는 느낌", "subgroup=큰 집단 안의 작은 하위 집단 / minority=수적으로 적은 집단 / faction=내부 파벌"),
    ("tacit agreement", "암묵적 합의 / 말로 다 적지 않았지만 서로 받아들이는 공통 이해", "공식 문서나 선언은 없어도 반복된 상호작용 속에서 서로 이렇게 하자고 사실상 맞춰진 상태", "서명은 없는데도 눈빛과 관행으로 이미 고개를 끄덕인 느낌", "tacit agreement=말하지 않아도 공유된 암묵적 합의 / formal contract=공식 계약 / assumption=추정"),
    ("team norm", "팀 규범 / 그 팀에서 보통 어떻게 일하고 말하는지의 기준", "공식 업무표보다 한 팀 안에서 회의, 피드백, 책임 분담, 응답 방식에 대해 자연스럽게 자리 잡은 기준", "이 팀 방에 들어오면 다들 몸에 익혀 따르는 고유 리듬과 선", "team norm=팀 내부의 일하는 방식과 상호작용 기준 / rule=명시적 규칙 / culture=더 넓은 조직 문화"),
    ("turn-taking", "발언 순서 교대 / 대화에서 차례를 주고받는 방식", "여러 사람이 말할 때 끼어들기, 넘겨주기, 침묵, 응답 타이밍으로 순서를 조절하는 상호작용 방식", "대화가 한 사람 독주가 아니라 말의 공이 서로 넘어가는 리듬", "turn-taking=대화에서 발언 차례를 주고받는 방식 / interruption=끼어들기 / dialogue=대화"),
    ("unwritten rule", "불문율 / 적혀 있지 않아도 지켜지는 규칙", "공식 문서는 아니지만 집단 안에서 대부분 알고 따르며 어기면 어색해지는 행동 기준", "칠판엔 없지만 다들 어디 선까지는 넘지 않는다는 걸 아는 느낌", "unwritten rule=문서화되지 않았지만 통용되는 규칙 / informal norm=암묵적 비공식 규범 / policy=공식 정책"),
    ("value alignment", "가치 정렬 / 서로 중요하게 보는 기준이 맞아떨어짐", "개인, 팀, 조직이 무엇을 우선하고 어떤 방향을 옳다고 보는지가 크게 어긋나지 않는 상태", "서로 다른 배가지만 노가 같은 방향으로 물을 젓는 느낌", "value alignment=중요 가치와 방향이 맞아떨어짐 / agreement=의견 일치 / compatibility=서로 잘 맞음"),
    ("voluntary association", "자발적 결사체 / 강제가 아니라 뜻에 따라 모인 단체", "국가나 고용 관계로 자동 편입된 것이 아니라 공통 관심과 목표를 따라 자발적으로 조직한 집단", "억지로 배치된 줄이 아니라 스스로 손을 잡고 만든 모임", "voluntary association=자발적으로 만든 단체 / institution=제도화된 기관 / coalition=공동 목적을 위한 연합"),
    ("workplace culture", "직장 문화 / 일터에서 당연하게 여기는 행동과 분위기", "급여 구조만이 아니라 말투, 협업 방식, 피드백, 권위 거리, 인정 방식이 형성하는 일터의 공기", "같은 직무라도 이 사무실에서는 몸이 어떤 리듬으로 움직이는지가 달라지는 느낌", "workplace culture=일터의 규범과 분위기 / organizational culture=조직 문화 전체 / office etiquette=사무실 예절"),
    ("accountability mechanism", "책임성 장치 / 행동 결과를 설명하고 책임지게 만드는 구조", "권한이 있는 사람이 자기 결정을 숨기지 못하고 점검, 보고, 평가를 통해 책임지게 하는 제도적 장치", "움직인 손이 흔적 없이 사라지지 않고 다시 설명대로 돌아오게 묶는 고리", "accountability mechanism=책임을 지게 만드는 제도적 장치 / oversight=감독 / transparency measure=투명성을 높이는 수단"),
    ("audience engagement", "청중 참여·관여 / 듣는 사람이 얼마나 적극적으로 반응하고 따라오는가", "말하는 쪽이 혼자 떠드는 정도가 아니라 청중이 관심, 이해, 질문, 반응으로 얼마나 들어오는지", "객석이 조용히 멀어져 있지 않고 앞쪽으로 몸을 기울이는 느낌", "audience engagement=청중의 적극적 관여와 반응 / engagement level=참여 정도 / attendance=참석"),
    ("collective responsibility", "집단적 책임 / 한 사람만이 아니라 함께 지는 책임", "문제와 결과를 개인 하나에게만 돌리지 않고 팀이나 공동체가 역할과 부담을 나눠 지는 구조", "무게를 한 손가락에 걸지 않고 여러 어깨가 같이 받치는 느낌", "collective responsibility=집단이 함께 나눠 지는 책임 / individual responsibility=개인 책임 / accountability=책임을 설명하고 지는 성질"),
    ("community input", "지역사회·구성원 의견 / 관련 사람들이 직접 내는 피드백", "전문가가 밖에서 추정한 요구가 아니라 실제 영향을 받는 사람들이 제안과 우려를 전달하는 입력", "설계자 머릿속 가정 대신 현장 사람들의 목소리가 자료로 들어오는 느낌", "community input=구성원이나 지역사회가 내는 의견 / stakeholder feedback=이해관계자 피드백 / expert advice=전문가 조언"),
    ("consent-based", "동의 기반의 / 당사자 수락을 전제로 하는", "힘이나 관습으로 밀어붙이지 않고 당사자가 알고 받아들였는지를 핵심 기준으로 삼는", "아무리 가능해 보여도 먼저 고개 끄덕임이 있어야 문이 열리는 느낌", "consent-based=당사자 동의를 전제로 하는 / coercive=강압적인 / voluntary=자발적인"),
    ("cross-sector", "부문 간의 / 정부·민간·비영리 등 서로 다른 영역이 함께하는", "한 조직 분야 안에서만 끝나지 않고 서로 다른 제도 영역이 협력하거나 영향을 주고받는", "각자 다른 건물의 사람들이 한 프로젝트 다리 위에서 만나는 느낌", "cross-sector=서로 다른 사회·조직 부문이 함께하는 / cross-functional=여러 기능 부서가 함께하는 / single-sector=한 부문에 한정된"),
    ("dialogic", "대화적인 / 한쪽 전달보다 주고받는 상호작용의", "말이 일방향 발표로 닫히지 않고 상대 응답과 의미 조정을 포함하는 성격의", "한 사람이 벽에 말하는 게 아니라 말이 오가며 사이 공간에서 뜻이 생기는 느낌", "dialogic=상호응답적 대화의 / monologic=일방향 발화의 / conversational=대화체의"),
    ("diplomatic", "외교적이고 신중한 / 갈등을 자극하지 않게 조절하는", "자기 입장을 숨긴다는 뜻만이 아니라 상대 체면과 관계를 고려해 표현 강도와 표현 방식을 조심스럽게 맞추는", "날카로운 말을 그대로 던지지 않고 모서리를 조금 다듬어 건네는 느낌", "diplomatic=관계를 고려해 신중하게 표현하는 / blunt=직설적인 / strategic=전략적인"),
    ("disclosure norm", "공개 규범 / 무엇을 얼마나 드러내야 하는지에 대한 기대", "개인 정보, 이해관계, 오류, 기준 등을 어떤 상황에서 밝혀야 한다고 여겨지는지에 관한 사회적·제도적 기준", "감춰도 되는 선과 열어야 하는 선이 어디인지 정하는 보이지 않는 문턱", "disclosure norm=정보 공개에 대한 기대와 기준 / transparency=투명성 / privacy rule=사생활 보호 규칙"),
    ("embedded in", "안에 깊이 박힌 / 특정 구조와 맥락 속에 놓인", "개인 행동이나 의미가 혼자 따로 생긴 것이 아니라 제도, 관계, 문화, 역사 속에 깊이 연결되어 있는", "표면 위에 따로 떠 있는 점이 아니라 큰 틀 안에 뿌리 박힌 느낌", "embedded in=특정 구조나 맥락 안에 깊이 연결된 / located in=물리적으로 위치한 / influenced by=영향을 받은"),
    ("equitable access", "공정한 접근성 / 특정 집단만 덜 막히지 않게 접근 기회를 맞춤", "모두에게 똑같은 문을 열었다고 끝내지 않고 서로 다른 조건에서도 실제로 비슷하게 이용할 수 있게 하는 것", "입구 하나를 같게 두는 게 아니라 각자 문턱 높이까지 함께 보는 느낌", "equitable access=조건 차이를 고려한 공정한 접근 / equal access=같은 형태의 접근 기회 / preferential access=우선 접근"),
    ("facilitative", "촉진적인 / 사람들이 말하고 협력하기 쉽게 돕는", "직접 결론을 대신 내기보다 참여자들이 의견을 내고 조정하고 다음 행동으로 가게 과정을 열어 주는", "앞에서 명령하는 손보다 흐름이 막히지 않게 길을 터 주는 손", "facilitative=과정과 참여를 촉진하는 / directive=지시적인 / supportive=도움을 주는"),
    ("group belonging", "집단 소속감 / 그 안에 내가 포함되어 있다고 느끼는 감각", "명단상 포함 여부만이 아니라 정서적으로 그 집단 안에서 받아들여지고 자리를 가진다고 느끼는 상태", "문은 통과했지만 더 나아가 내 자리가 안쪽에 생긴 느낌", "group belonging=집단 안에 받아들여진다는 소속감 / membership=구성원 자격 / identification=그 집단과 자신을 연결해 느끼는 것"),
    ("identity marker", "정체성 표지 / 어떤 소속과 위치를 드러내는 표시", "옷차림, 언어, 이름, 상징, 행동양식처럼 개인이 어느 집단과 연결되는지 알아보게 하는 단서", "겉에 붙은 작은 표식이 뒤의 소속 이야기를 열어 주는 느낌", "identity marker=정체성과 소속을 드러내는 표지 / symbol=상징 / label=이름표"),
    ("institutionalized", "제도화된 / 관행이 공식 구조와 규칙 속에 굳어진", "한 번의 행동이 아니라 반복된 방식이 규칙, 절차, 조직 구조에 들어가 비교적 안정적으로 자리 잡은", "즉석 습관이 아니라 조직의 뼈대 안에 아예 홈이 파인 느낌", "institutionalized=제도와 절차 속에 굳어진 / informal=비공식적인 / established=자리 잡은"),
    ("issue advocacy", "쟁점 옹호 활동 / 특정 공공 문제에 대해 지지와 변화를 밀어붙임", "개별 이익만이 아니라 정책, 권리, 사회문제에 대해 공개적으로 입장을 내고 설득과 행동을 조직하는 일", "조용한 의견을 현수막과 발언으로 공론장 쪽으로 밀어 올리는 느낌", "issue advocacy=특정 공공 쟁점에 대한 옹호와 행동 / lobbying=정책 결정자를 겨냥한 영향 행사 / awareness-raising=인식 제고"),
    ("line of authority", "권한선 / 누가 누구에게 보고하고 결정하는지의 계통", "조직 안에서 결정권과 보고 관계가 어떤 방향으로 이어지는지 보여주는 공식 구조", "누가 최종적으로 문을 열고 누구 말을 따라 올라가는지 그린 선", "line of authority=권한과 보고가 이어지는 공식 계통 / hierarchy=위계 구조 / chain of command=명령 계통"),
    ("majority view", "다수 견해 / 더 많은 사람이 공유하는 입장", "공식 합의와 같을 수도 있지만, 현재 더 큰 비율의 사람이 지지하거나 당연하게 여기는 관점", "회의장 안에서 가장 많은 의자가 향하고 있는 쪽", "majority view=다수가 지지하는 견해 / consensus=함께 받아들일 수 있는 합의 / dominant view=우세한 관점"),
    ("mutually reinforcing", "서로를 강화하는 / 한쪽이 다른 쪽을 더 키워 주는", "두 규범, 행동, 제도가 따로 작동하는 데서 끝나지 않고 서로를 되밀어 더 굳히거나 확대하는", "두 톱니가 따로 도는 게 아니라 맞물리며 서로 힘을 더해 주는 느낌", "mutually reinforcing=서로의 효과를 강화하는 / reciprocal=서로 주고받는 / independent=독립적인"),
    ("norm enforcement", "규범 집행 / 기대를 어겼을 때 사회적 압력이나 제재로 바로잡음", "규칙이 그냥 말로만 있지 않고 칭찬, 비판, 배제, 처벌 등을 통해 실제 행동을 기준 쪽으로 끌어오는 일", "선 하나를 그어놓고 넘는 순간 주변 힘이 다시 안쪽으로 밀어넣는 느낌", "norm enforcement=규범을 실제 행동에 적용해 따르게 함 / rule compliance=규칙 준수 상태 / sanction=제재"),
    ("organizational buy-in", "조직 내 동의와 지지 / 구성원이 계획을 받아들이고 따라갈 준비", "상층부 결정이 문서에만 있는 것이 아니라 실행할 사람들이 필요성과 방향에 어느 정도 납득하고 동참하는 상태", "명령이 내려왔다보다 사람들이 마음과 손을 같이 얹는 느낌", "organizational buy-in=조직 구성원의 수용과 지지 / compliance=겉으로 규칙을 따름 / commitment=헌신"),
    ("out-group", "외집단 / 자기 소속 바깥으로 구분되는 집단", "내가 속한 우리 집단과 대비되어 거리감, 고정관념, 경쟁의 대상으로 인식될 수 있는 바깥 집단", "우리라는 원 밖에 다른 색으로 둘러쳐진 바깥 원", "out-group=자기 집단 바깥으로 구분된 집단 / in-group=자기 소속 집단 / outsider=외부자"),
    ("participation rate", "참여율 / 대상자 중 실제 참여한 비율", "참여 가능 인원 전체에 비해 실제로 신청, 출석, 발언, 투표, 응답에 들어온 사람이 얼마나 되는지", "열린 문 개수보다 그 문을 실제로 통과한 사람이 몇 퍼센트인지 보는 느낌", "participation rate=가능한 대상 중 실제 참여한 비율 / turnout=특히 투표나 행사 참여율 / attendance rate=출석률"),
    ("public narrative", "공적 서사 / 사회가 어떤 사건을 어떤 이야기로 받아들이는가", "개별 사실 나열보다 언론, 기관, 공동체가 어떤 원인과 의미를 중심으로 사건을 이야기하는 틀", "흩어진 사건들이 사회 머릿속에서 하나의 큰 줄거리로 묶이는 느낌", "public narrative=사회적으로 공유되는 사건 해석의 이야기 틀 / storyline=줄거리 / discourse=담론"),
    ("role expectation", "역할 기대 / 그 위치의 사람이 이렇게 하리라 여기는 기준", "개인의 성향과 별개로 교사, 학생, 대표자, 신입 구성원 등 특정 위치에 대해 주변이 예상하는 행동과 책임", "이 자리에 서면 보이지 않는 대본 일부가 같이 따라붙는 느낌", "role expectation=특정 사회적 위치에 붙는 행동 기대 / duty=의무 / stereotype=고정된 단순화 이미지"),
    ("shared understanding", "공유된 이해 / 서로 같은 뜻과 상황 인식을 어느 정도 나눔", "단어는 같아도 다르게 해석하지 않도록 참여자들이 기준, 목적, 맥락을 비슷하게 맞춘 상태", "각자 다른 지도를 들고 있지 않고 같은 방향 표시를 어느 정도 공유하는 느낌", "shared understanding=뜻과 상황 인식을 함께 맞춘 상태 / agreement=의견 일치 / common knowledge=모두 알고 있다고 여기는 정보"),
    ("social distance", "사회적 거리감 / 지위·친밀도·소속 차이에서 생기는 간격", "물리적 거리가 아니라 서로 얼마나 가깝거나 멀게 느끼고 어떤 말과 행동을 허용하는지가 달라지는 관계상의 거리", "같은 방에 있어도 보이지 않는 간격이 말투와 자세를 갈라놓는 느낌", "social distance=관계·지위·소속에서 생기는 거리감 / physical distance=물리적 거리 / formality=격식"),
    ("status hierarchy", "지위 위계 / 누가 더 높은 인정과 권한을 갖는지의 서열 구조", "공식 직급뿐 아니라 평판, 전문성, 나이, 자원 때문에 누가 위나 아래로 여겨지는지 형성된 배열", "사람들이 평평히 서 있는 듯해도 실제로는 보이지 않는 높낮이 계단이 있는 느낌", "status hierarchy=지위와 인정의 서열 구조 / social hierarchy=사회적 위계 / role differentiation=역할 분화"),
    ("transparency pledge", "투명성 약속 / 정보를 숨기지 않고 공개하겠다는 공적 선언", "결정 기준, 이해관계, 오류, 자료를 가능한 공개하겠다고 외부나 구성원 앞에 내건 약속", "닫힌 서랍 대신 창을 열어두겠다고 먼저 말로 걸어두는 느낌", "transparency pledge=정보 공개와 투명성을 약속하는 선언 / disclosure policy=공개 규정 / accountability statement=책임성에 대한 진술"),
    ("underrepresented", "충분히 대표되지 못한 / 인원이나 영향력에 비해 목소리가 적은", "사회나 조직에 실제 존재하지만 회의, 자료, 리더십, 결정 구조에서 비중이 충분히 드러나지 않는 상태의", "자리는 있어야 할 만큼 있는데 마이크와 화면 안에서는 작게만 잡히는 느낌", "underrepresented=존재에 비해 대표성과 가시성이 부족한 / marginalized=중심에서 밀려난 / minority=수적으로 적은"),
    ("value-laden", "가치 판단이 실린 / 중립처럼 보여도 어떤 기준을 담은", "말이나 분류, 설명이 사실 전달만 하는 듯해도 무엇을 더 좋고 나쁘게 보는 기준을 함께 싣고 있는", "평평한 정보판처럼 보여도 아래에 한쪽으로 기우는 저울이 깔린 느낌", "value-laden=가치 판단이 담긴 / neutral=중립적인 / normative=어떻게 해야 하는지 기준을 두는"),
    ("volunteer-based", "자원봉사 기반의 / 자발적 참여 인력에 기대는", "급여를 받는 정규 인력보다 자발적으로 시간을 내는 사람들의 참여가 운영의 중요한 기반이 되는", "돈으로 고용한 손보다 스스로 보태는 손들이 조직을 받치는 느낌", "volunteer-based=자발적 참여 인력에 기반한 / staff-led=직원이 주도하는 / grassroots=아래로부터 시민 기반의"),
    ("welcome culture", "환대 문화 / 새 사람과 다른 사람을 편하게 받아들이는 분위기", "절차상 입장을 허용하는 것 이상으로 낯선 구성원도 말하고 머물기 쉽게 만드는 상호작용 습관과 분위기", "문은 열려 있고 안쪽 공기도 낯선 사람을 밀어내지 않는 느낌", "welcome culture=새 사람을 편하게 받아들이는 분위기 / inclusivity=포용성 / hospitality=환대"),
    ("advocacy network", "옹호 네트워크 / 공통 쟁점에 대해 연결되어 움직이는 집단망", "개별 단체나 개인이 따로 말하는 대신 정보, 자원, 메시지를 연결해 더 큰 영향력을 만드는 관계망", "흩어진 촛불이 선으로 이어져 더 멀리 보이는 불빛망", "advocacy network=공통 쟁점을 위해 연결된 옹호 관계망 / coalition=공동 행동 연합 / social network=사회적 연결망 일반"),
    ("citizenship norm", "시민성 규범 / 좋은 시민이라면 어떻게 참여하고 책임져야 하는지에 대한 기대", "법적 신분보다 공동체 구성원으로서 발언, 협력, 준수, 배려를 어떻게 해야 한다고 보는 기준", "시민이라는 이름표에 따라붙는 보이지 않는 행동 기준", "citizenship norm=시민에게 기대되는 참여와 책임 기준 / legal citizenship=법적 시민 신분 / civic duty=시민의 의무"),
    ("collaborative ethos", "협력적 풍토 / 같이 일하고 나누려는 기본 태도", "경쟁과 단절보다 정보 공유, 공동 문제 해결, 상호 존중을 당연하게 여기는 집단의 분위기", "각자 칸막이 안에 숨기보다 테이블 위에 같이 펴놓는 공기", "collaborative ethos=협력을 중시하는 집단 분위기와 태도 / teamwork=팀으로 일함 / competition=경쟁"),
    ("community representation", "공동체 대표성 / 해당 집단의 목소리와 특성이 적절히 반영됨", "결정 자리나 자료에서 영향을 받는 공동체가 아예 빠지지 않고 현실에 맞게 어느 정도 반영되는 상태", "밖에서 대신 말하는 그림자만이 아니라 실제 공동체 얼굴이 테이블에 들어오는 느낌", "community representation=공동체가 적절히 대표되고 반영됨 / symbolic representation=상징적 대변 / participation=참여"),
    ("cross-group dialogue", "집단 간 대화 / 서로 다른 집단이 직접 말과 이해를 주고받음", "같은 편 안에서만 말하지 않고 서로 다른 입장과 경험을 가진 집단이 접촉하며 오해와 차이를 조정하는 대화", "각자 자기 방에서만 외치지 않고 문 사이 통로에서 목소리가 만나는 느낌", "cross-group dialogue=서로 다른 집단 사이의 대화 / intergroup contact=집단 간 접촉 / debate=논쟁"),
    ("decision legitimacy", "결정 정당성 / 그 결정이 받아들여질 만하다고 여겨지는 정도", "결과가 마음에 드는지와 별개로 절차, 대표성, 근거가 충분해 그 결정이 부당하지 않다고 인정되는 상태", "결론이 떨어졌을 때 왜 이 결론이 나왔는지 납득의 받침대가 같이 서 있는 느낌", "decision legitimacy=결정이 정당하다고 인정받는 정도 / procedural fairness=절차적 공정성 / approval=승인"),
    ("dialogue facilitation", "대화 촉진 / 사람들이 말하고 듣고 조정하도록 흐름을 여는 일", "토론자가 한쪽으로 쏠리거나 막히지 않도록 질문, 순서, 요약, 규칙으로 대화의 통로를 열어 주는 역할", "직접 답을 대신 말하기보다 막힌 대화 길을 다시 트는 손", "dialogue facilitation=대화가 잘 오가게 과정을 돕는 일 / moderation=토론 진행 관리 / mediation=갈등 중재"),
    ("equity-oriented", "형평성 지향의 / 다른 출발 조건을 고려해 공정함을 맞추려는", "모두에게 똑같이 주는 데서 끝내지 않고 누가 구조적으로 불리한지 보며 실제 결과의 공정성을 높이려는", "같은 자 하나로 대충 재지 않고 서로 다른 높이의 발판까지 같이 보는 느낌", "equity-oriented=조건 차이를 고려한 공정함을 지향하는 / equality-oriented=같은 대우 자체를 중시하는 / merit-based=실적 기준을 중시하는"),
    ("group cohesion", "집단 결속 / 구성원이 서로 묶여 함께 움직이는 정도", "각자 개인으로만 흩어지지 않고 신뢰, 소속감, 공동 목표로 한 팀처럼 이어지는 상태", "여러 점이 느슨히 흩어진 게 아니라 안쪽 실로 단단히 묶인 느낌", "group cohesion=집단의 결속 정도 / cohesion=결속력 일반 / morale=사기"),
    ("identity affirmation", "정체성 인정 / 자기 소속과 경험이 존중받고 확인되는 느낌", "특정 배경이나 정체성이 숨겨야 할 결함처럼 다뤄지지 않고 공개적으로 인정되고 지지받는 경험", "내 이름표를 접어 넣지 않아도 괜찮다고 주변이 같이 말해주는 느낌", "identity affirmation=정체성이 인정받는 경험 / recognition=인정 / validation=타당하다고 확인받음"),
    ("institutional barrier", "제도적 장벽 / 개인 노력만으로 넘기 어려운 규칙과 구조의 막힘", "의지 부족이 아니라 절차, 비용, 자격 기준, 행정 구조 자체가 특정 사람의 접근이나 참여를 어렵게 하는 요소", "개인 앞의 작은 돌이 아니라 시스템 안에 박힌 높은 문턱", "institutional barrier=제도 구조가 만드는 장벽 / personal obstacle=개인적 장애물 / access barrier=접근 장벽"),
    ("majority rule", "다수결 원칙 / 더 많은 표를 얻은 쪽이 결정하는 방식", "모든 참여자가 완전히 동의하지 않아도 수적으로 더 큰 쪽의 선택을 공식 결정으로 삼는 절차", "가장 큰 표 묶음이 최종 방향의 손잡이를 잡는 느낌", "majority rule=다수표를 기준으로 결정하는 원칙 / unanimity=만장일치 / consensus=합의"),
    ("norm violation", "규범 위반 / 기대된 행동 기준을 어김", "법을 어기는 수준일 수도 있지만 더 넓게는 그 집단이 당연하게 여기는 행동선을 넘는 것", "눈에 안 보이는 선을 넘자 주변 공기가 바로 삐걱거리는 느낌", "norm violation=기대된 규범을 어기는 행동 / rule breach=명시적 규칙 위반 / deviance=사회 기준에서 벗어남"),
    ("participatory culture", "참여 문화 / 구성원이 보고 듣기만 하지 않고 기여하는 분위기", "콘텐츠나 결정이 소수 생산자에게만 몰리지 않고 많은 사람이 의견, 수정, 공유, 협업으로 들어오는 문화", "완성품을 멀리서 소비만 하지 않고 손을 얹어 같이 만드는 공기", "participatory culture=많은 구성원이 직접 기여하는 문화 / audience engagement=청중 관여 / passive consumption=수동적 소비"),
    ("public comment", "공개 의견 제출 / 정책·계획에 대해 외부가 공식적으로 내는 의견", "기관 결정 전에 시민이나 이해관계자가 문서나 발언으로 의견과 우려를 공식적으로 제출하는 절차나 그 내용", "닫힌 문 안 결정 전에 바깥 목소리가 기록으로 들어가는 창구", "public comment=공개 절차에서 제출하는 의견 / feedback=피드백 일반 / testimony=공식 진술"),
    ("social inclusion", "사회적 포용 / 다양한 사람이 관계와 제도 안에서 배제되지 않게 함", "존재를 인정하는 데서 끝나지 않고 교육, 참여, 자원, 소속의 실제 기회 안으로 들어오게 하는 것", "문 밖에 세워두지 않고 안쪽 자리와 길까지 같이 내어 주는 느낌", "social inclusion=사람들이 사회적 관계와 제도 안에서 배제되지 않게 함 / inclusivity=포용성 / integration=통합"),
    ("trust deficit", "신뢰 부족 / 관계나 제도에 대한 믿음이 모자란 상태", "사람이나 기관이 말대로 책임 있게 행동할 거라는 기대가 약해 협력과 수용이 잘 안 생기는 상태", "다리를 건너도 될지 바닥이 계속 꺼질 것 같아 발을 못 싣는 느낌", "trust deficit=신뢰가 부족한 상태 / skepticism=회의적 태도 / mistrust=불신"),
    ("underserved", "충분한 서비스를 받지 못하는 / 필요한 지원이 덜 닿는", "수요가 없다는 뜻이 아니라 교육, 의료, 정보, 자원 등이 다른 집단보다 충분히 제공되지 않는 상태의", "지도에는 구역이 있지만 실제 지원 손길이 자주 비껴가는 느낌", "underserved=필요한 서비스와 자원이 충분히 닿지 않는 / disadvantaged=불리한 조건에 놓인 / underrepresented=대표성이 부족한"),
    ("voluntary compliance", "자발적 준수 / 강한 단속보다 스스로 규칙을 따름", "처벌이 두려워서만이 아니라 규범과 목적을 어느 정도 받아들여 스스로 기준을 지키는 상태", "누가 계속 감시하지 않아도 안쪽에서 선을 넘지 않으려는 브레이크가 작동하는 느낌", "voluntary compliance=스스로 받아들여 규칙을 따름 / enforced compliance=단속으로 따르게 함 / conformity=주변 기대에 맞춤"),
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
        manifest["files_created"].insert(20, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    notes_path = ROOT / "generation_notes.md"
    notes_path.write_text(
        notes_path.read_text(encoding="utf-8").replace(
            "- ETS sets `01` to `20` exist, bringing the ETS-based total to 2000 cards\n",
            "- ETS sets `01` to `21` exist, bringing the ETS-based total to 2100 cards\n",
        ),
        encoding="utf-8",
    )

    plan_path = ROOT / "WORK_PLAN.md"
    plan_path.write_text(
        plan_path.read_text(encoding="utf-8")
        .replace(
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_20.tsv`\n",
            "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_21.tsv`\n",
        )
        .replace(
            "- Current ETS row count after the latest expansion pass: 2000\n",
            "- Current ETS row count after the latest expansion pass: 2100\n",
        ),
        encoding="utf-8",
    )

    task_next = ROOT / ".task_next.md"
    task_next.write_text(
        task_next.read_text(encoding="utf-8")
        .replace("`toefl_ets_2026_set_21.tsv`", "`toefl_ets_2026_set_22.tsv`")
        .replace(
            "social interaction, norms, participation, institutional behavior, and public communication, while keeping terms broadly reusable beyond one discipline.",
            "environmental change, resource use, sustainability, resilience, and long-term planning, using broad academic terms rather than narrow ecology jargon.",
        ),
        encoding="utf-8",
    )

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
