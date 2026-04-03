from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPLACEMENTS = {
    "toefl_ets_2026_set_07.tsv": {
        "treatment": ("remedy", "해결책 / 개선 수단", "문제나 불리한 상태를 완화하거나 바로잡는 방법", "나쁜 상태를 그대로 두지 않고 고쳐보려는 카드", "remedy=문제를 완화·해결하는 수단 / solution=해결책 일반 / intervention=상황에 개입하는 조치"),
        "clinical": ("practice-oriented", "실무 지향적인 / 실제 적용 중심의", "이론보다 실제 상황에서의 적용과 판단을 중시하는", "책상 위 이론보다 현장에서 써먹는 쪽으로 기운 느낌", "practice-oriented=실제 적용 중심의 / theoretical=이론 중심의 / practical=실용적인"),
        "pathology": ("malfunction", "오작동 / 기능 이상", "원래 기대한 방식대로 작동하지 않는 상태", "돌아가야 할 장치나 체계가 어긋나 삐걱거리는 느낌", "malfunction=기능이 제대로 작동하지 않음 / defect=구조적 결함 / failure=작동 실패"),
        "organ": ("subsystem", "하위 체계 / 부분 시스템", "큰 시스템 안에서 특정 기능을 맡는 구성 단위", "전체 기계 안의 한 블록이 자기 역할을 맡는 느낌", "subsystem=전체 안의 부분 시스템 / component=구성 요소 / module=독립성이 있는 기능 단위"),
        "infection": ("penetration", "침투 / 안쪽으로 들어감", "바깥의 것이 경계나 표면을 넘어 내부로 들어가는 일", "겉에서 멈추지 않고 안으로 파고드는 느낌", "penetration=경계를 뚫고 안으로 들어감 / intrusion=원치 않는 침범 / absorption=안으로 흡수됨"),
        "contagious": ("cascading", "연쇄적으로 번지는 / 단계적으로 이어지는", "한 변화가 다음 변화들을 잇따라 일으키는", "하나가 넘어지면 다음 것들이 줄줄이 이어지는 느낌", "cascading=연쇄적으로 이어지는 / spreading=퍼져 나가는 / sequential=순서대로 이어지는"),
        "epidemic": ("widespread", "광범위한 / 널리 퍼진", "한 지역이나 일부 대상에만 머물지 않고 넓게 나타나는", "작은 점 하나가 아니라 넓은 면으로 퍼져 있는 느낌", "widespread=넓은 범위에 퍼진 / localized=국지적인 / prevalent=흔히 나타나는"),
        "pandemic": ("systemwide", "시스템 전반의 / 전체에 걸친", "부분 하나가 아니라 전체 체계에 폭넓게 영향을 미치는", "한 구석 문제가 아니라 판 전체로 퍼진 느낌", "systemwide=전체 시스템에 걸친 / local=국지적인 / comprehensive=포괄적인"),
        "immunize": ("buffer", "완충하다 / 충격을 줄이다", "외부 변화나 부담이 직접 크게 영향을 주지 않도록 중간에서 흡수하다", "충격을 그대로 맞지 않게 사이에 쿠션을 두는 느낌", "buffer=충격·변동을 완충하다 / protect=보호하다 / mitigate=나쁜 영향을 줄이다"),
        "vaccine": ("safeguard", "안전장치 / 보호책", "문제나 위험이 커지지 않도록 미리 마련한 보호 수단", "혹시 모를 문제를 막으려고 앞에 세워둔 안전막", "safeguard=위험을 막는 보호 조치 / preventive=예방적인 / remedy=문제 발생 후 해결책"),
        "antibody": ("counterforce", "대항력 / 반작용하는 힘", "한쪽 영향에 맞서 균형을 잡거나 밀어내는 힘", "들어오는 힘을 그냥 받지 않고 반대쪽에서 맞서는 느낌", "counterforce=상대 힘에 맞서는 반작용 / resistance=저항 / opposition=반대 입장"),
        "gene": ("specification", "명세 / 구체적 기준 설명", "무엇이 어떤 조건과 구조를 가져야 하는지 세부적으로 적은 기준", "막연한 아이디어를 정확한 조건표로 적어두는 느낌", "specification=세부 조건을 적은 명세 / blueprint=기본 설계도 / guideline=따를 지침"),
        "neuron": ("node", "마디 / 연결 지점", "연결망 안에서 정보나 흐름이 모이거나 갈라지는 한 지점", "여러 선이 만나고 다시 퍼지는 교차점", "node=네트워크의 연결 지점 / link=연결선 / hub=중심 연결점"),
        "neural": ("networked", "연결망을 이룬 / 네트워크화된", "여러 지점이 서로 이어져 정보를 주고받는 구조를 가진", "따로 떨어진 점들이 아니라 선으로 이어진 상태", "networked=서로 연결된 구조를 가진 / isolated=분리된 / integrated=하나의 체계로 결합된"),
        "receptor": ("interface", "접점 / 상호작용 경계면", "서로 다른 시스템이나 사람·정보가 만나 작동하는 지점", "안과 밖이 맞닿아 신호가 오가는 연결면", "interface=두 체계가 만나는 접점 / boundary=경계 / channel=정보가 지나가는 통로"),
        "hormone": ("regulator", "조절자 / 균형을 맞추는 요소", "어떤 과정의 속도나 강도를 조정하는 역할을 하는 것", "너무 과하거나 약하지 않게 눈금을 맞추는 손잡이", "regulator=작동 수준을 조절하는 요소·장치 / controller=직접 제어하는 주체 / moderator=토론 흐름을 조정하는 사람"),
        "metabolism": ("throughput", "처리량 / 처리 흐름", "시스템이 일정 시간 동안 처리하거나 통과시키는 양", "안으로 들어온 것이 얼마나 잘 돌아 나가는지 보는 흐름", "throughput=시간당 처리되는 양 / capacity=수용·처리 가능량 / output=밖으로 나온 결과물"),
        "tissue": ("substrate", "기반 재료 / 바탕이 되는 층", "어떤 과정이나 구조가 올라서는 물질적·개념적 바탕", "위에서 일이 일어나도록 아래에 깔린 받침층", "substrate=작용이 일어나는 바탕층 / foundation=토대 / material=재료"),
        "neuroplasticity": ("malleability", "가변성 / 바뀔 수 있는 성질", "경험이나 조건에 따라 형태나 방식이 달라질 수 있음", "딱딱하게 고정되지 않고 눌리며 다시 모양이 바뀌는 느낌", "malleability=형태·방식이 바뀔 수 있음 / flexibility=유연성 / rigidity=딱딱하게 고정됨"),
        "sensory": ("perceptual", "지각의 / 인식과 관련된", "정보를 받아들여 알아차리는 과정과 관련된", "밖의 자극이 머릿속 의미로 잡히는 쪽을 보는 느낌", "perceptual=지각·인식 과정의 / sensory=감각 입력의 / cognitive=사고 과정의"),
        "motor": ("action-oriented", "행동 지향적인 / 실행 중심의", "생각을 멈추지 않고 실제 행동이나 실행으로 옮기는 쪽의", "머릿속에서 끝나지 않고 몸이나 실행 단계로 나가는 느낌", "action-oriented=행동·실행 중심의 / analytical=분석 중심의 / passive=수동적인"),
        "sanitation": ("hygiene", "위생 / 청결 관리", "건강이나 안전을 위해 청결 상태를 유지하는 일", "오염되거나 지저분해지지 않게 깨끗한 선을 지키는 느낌", "hygiene=청결과 위생 관리 / sanitation=공공 위생 설비·관리 / cleanliness=깨끗한 상태"),
        "nutrition": ("intake", "섭취량 / 받아들이는 양", "몸이나 시스템 안으로 들어오는 자원이나 정보의 양", "밖에서 안으로 얼마를 들여오는지 세는 느낌", "intake=안으로 받아들이는 양 / input=투입되는 것 / consumption=소비·섭취"),
    },
    "toefl_ets_2026_set_14.tsv": {
        "excavate": ("uncover", "드러내다 / 밝혀내다", "가려져 있던 정보나 사실을 찾아 겉으로 나오게 하다", "덮여 있던 것을 걷어 안의 내용을 밖으로 꺼내는 느낌", "uncover=숨은 것을 드러내다 / reveal=밝히다 / discover=처음 찾아내다"),
        "excavation": ("recovery", "회수 / 되찾음", "흩어졌거나 가려진 자료·기능·상태를 다시 찾아 얻는 일", "잃거나 묻힌 것을 다시 손에 넣는 느낌", "recovery=다시 찾아 얻거나 회복함 / retrieval=찾아 꺼냄 / restoration=원래 상태로 되돌림"),
        "feudal": ("hierarchical", "위계적인 / 서열이 있는", "권한이나 지위가 층층이 나뉘어 배열된", "평평하지 않고 위아래 계단이 뚜렷한 느낌", "hierarchical=위계가 있는 / egalitarian=평등주의적인 / stratified=층으로 나뉜"),
        "folklore": ("storytelling", "서사 전달 / 이야기로 전하기", "정보나 의미를 이야기 형식으로 구성해 전달하는 방식", "날것의 사실을 줄거리와 장면으로 엮어 들려주는 느낌", "storytelling=이야기 구조로 전달함 / narration=사건을 서술함 / explanation=이유와 원리를 풀어 설명함"),
        "genealogy": ("pedigree", "계통 / 출처와 이어진 내력", "대상이나 아이디어가 어디서 이어져 왔는지 보여주는 출신과 연원", "지금 모습 뒤에 따라붙은 출발점과 이어진 줄기", "pedigree=출처와 계통의 내력 / origin=기원 / lineage=혈통·계열"),
        "historian": ("chronicler", "기록자 / 사건을 정리해 남기는 사람", "지나간 사건을 시간 흐름에 따라 정리해 글로 남기는 사람", "흘러간 일을 놓치지 않게 줄 세워 적는 사람", "chronicler=사건을 기록해 남기는 사람 / analyst=자료를 해석하는 사람 / observer=관찰자"),
        "manor": ("estate", "대규모 토지 자산 / 소유지", "넓은 땅과 관련 재산이 하나의 소유 단위로 묶인 것", "집 한 채보다 땅과 자산이 크게 묶인 덩어리", "estate=넓은 토지·재산 묶음 / property=소유 재산 일반 / site=특정 장소"),
        "maritime": ("transit-based", "이동 경로 중심의 / 수송과 연결된", "사람이나 물자의 이동·연결 경로에 초점을 둔", "대상 자체보다 어디서 어디로 오가는 선을 보는 느낌", "transit-based=이동·운송 경로에 초점을 둔 / stationary=고정된 / logistical=운영 이동과 관련된"),
        "monarchy": ("centralization", "중앙집중화 / 권한 집중", "결정권이나 자원이 한 중심으로 모이게 되는 구조", "권한이 여기저기 흩어지지 않고 가운데로 몰리는 느낌", "centralization=권한이 중심으로 모임 / decentralization=권한이 분산됨 / concentration=한곳에 모임"),
        "monument": ("marker", "표지 / 의미를 남기는 표시물", "어떤 장소나 사건을 알아보게 하거나 기억하게 하는 표시", "그냥 지나치지 않게 여기 의미가 있다고 찍어두는 느낌", "marker=의미나 위치를 표시하는 것 / symbol=의미를 대표하는 표지 / landmark=중요한 기준점"),
        "peasantry": ("workforce", "노동력 집단 / 일하는 인력", "생산이나 업무를 실제로 수행하는 사람들의 집단", "계획이 아니라 일을 몸으로 굴리는 사람들 전체", "workforce=일하는 인력 집단 / laborer=노동자 개인 / population=인구 집단"),
        "patrilineal": ("inheritance-based", "상속 기반의 / 계승 질서 중심의", "권리나 지위가 누구에게 어떻게 넘어가는지의 계승 규칙에 기반한", "관계보다 무엇을 누구에게 넘기는지의 줄을 먼저 보는 느낌", "inheritance-based=상속·계승 규칙에 기반한 / hereditary=세습적인 / familial=가족 관계의"),
        "matrilineal": ("family-based", "가족 관계 기반의 / 친족 중심의", "개인보다 가족·친족 관계망을 중심으로 조직된", "혼자 떨어진 개인보다 가족선 안에서 위치가 정해지는 느낌", "family-based=가족 관계를 바탕으로 한 / community-based=공동체 기반의 / individual-based=개인 중심의"),
        "medieval": ("preindustrial", "산업화 이전의", "산업 생산과 현대 도시체계가 본격화되기 전의", "공장과 대규모 현대 시스템 이전의 사회 조건을 보는 느낌", "preindustrial=산업화 이전의 / modern=근대·현대의 / traditional=전통적인"),
        "monastic": ("rule-bound", "규율에 묶인 / 규칙 중심의", "개인 재량보다 정해진 규칙과 절차를 강하게 따르는", "자유롭게 흘러가기보다 규칙선 안에서 움직이는 느낌", "rule-bound=규칙과 규율에 강하게 묶인 / flexible=유연한 / informal=비공식적인"),
        "paternal": ("senior-led", "상위자가 이끄는 / 연장자 주도의", "결정이나 방향이 위쪽 또는 선배·상위자 중심으로 잡히는", "아래에서 평등하게가 아니라 위에서 끌고 가는 느낌", "senior-led=상위자·선배가 주도하는 / participatory=참여 중심의 / egalitarian=평등주의적인"),
        "chieftain": ("figurehead", "상징적 지도자 / 대표 얼굴", "실제 세부 집행보다 집단을 대표하는 상징적 인물", "조직의 얼굴로 앞에 서지만 모든 실무를 직접 하진 않는 느낌", "figurehead=상징적 대표 인물 / leader=실제 지도자 일반 / spokesperson=공식 발언자"),
        "deity": ("idealized", "이상화된 / 높게 그려진", "현실 그대로보다 더 완벽하거나 가치 있게 표현된", "있는 그대로보다 위로 끌어올려 빛나게 그리는 느낌", "idealized=현실보다 이상적으로 그려진 / symbolic=상징적인 / realistic=현실적인"),
        "throne": ("legitimacy", "정당성 / 인정받을 만한 근거", "권한이나 주장, 제도가 타당하다고 받아들여지는 근거와 상태", "힘이 있다는 것보다 그 힘이 맞다고 인정받는 느낌", "legitimacy=권한·주장이 정당하다고 인정됨 / authority=공식 권위 / credibility=믿을 만함"),
        "tomb": ("memorial", "기념물 / 추모 대상", "사람이나 사건을 기억하고 기리기 위해 만든 대상이나 장소", "없어진 사람·사건을 기억 속에 세워두는 표시", "memorial=추모·기념 대상 / monument=기념 구조물 / reminder=떠올리게 하는 것"),
        "tribal": ("group-based", "집단 기반의 / 공동체 단위의", "개인 하나보다 소속 집단의 경계와 규범을 중심으로 작동하는", "혼자 판단하는 게 아니라 어느 집단에 속했는지가 먼저 보이는 느낌", "group-based=집단 단위로 작동하는 / individual=개인 중심의 / communal=공동체적인"),
        "warlike": ("conflict-prone", "갈등이 잦은 / 충돌로 기우는", "협력보다 대립과 충돌이 쉽게 생기는 경향이 있는", "작은 차이도 싸움 쪽으로 번지기 쉬운 느낌", "conflict-prone=갈등이 쉽게 생기는 / cooperative=협력적인 / aggressive=공격적인"),
    },
}


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join(
        [
            f"핵심 뜻: {core}",
            f"부가 뜻: {extra}",
            f"핵심 느낌: {feeling}",
            f"구분: {distinction}",
        ]
    )


def load_cards() -> dict[str, list[list[str]]]:
    cards_by_file = {}
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            cards_by_file[path.name] = [row for row in csv.reader(f, delimiter="\t") if row]
    return cards_by_file


def validate(cards_by_file: dict[str, list[list[str]]]) -> None:
    owner = {}
    for filename, rows in cards_by_file.items():
        for row in rows:
            word = row[0].strip()
            if word in owner:
                raise RuntimeError(f"duplicate before rewrite: {word} in {owner[word]} and {filename}")
            owner[word] = filename

    for filename, mapping in REPLACEMENTS.items():
        old_words = {row[0].strip() for row in cards_by_file[filename]}
        for old_word, (new_word, *_rest) in mapping.items():
            if old_word not in old_words:
                raise RuntimeError(f"{old_word} missing in {filename}")
            if new_word != old_word and new_word in owner and owner[new_word] != filename:
                raise RuntimeError(f"{new_word} already exists in {owner[new_word]}")


def rewrite(cards_by_file: dict[str, list[list[str]]]) -> dict[str, int]:
    changed = {}
    for filename, mapping in REPLACEMENTS.items():
        out = []
        count = 0
        for word, back in cards_by_file[filename]:
            if word in mapping:
                new_word, core, extra, feeling, distinction = mapping[word]
                out.append([new_word, build_back(core, extra, feeling, distinction)])
                count += 1
            else:
                out.append([word, back])
        cards_by_file[filename] = out
        changed[filename] = count
    return changed


def write_cards(cards_by_file: dict[str, list[list[str]]]) -> None:
    for filename, rows in cards_by_file.items():
        with (ROOT / filename).open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerows(rows)


def refresh_wordlists(cards_by_file: dict[str, list[list[str]]]) -> None:
    ets_words = []
    for filename in sorted(cards_by_file):
        ets_words.extend(row[0].strip() for row in cards_by_file[filename])
    (ROOT / ".existing_words.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")
    (ROOT / "all_ets_headwords.txt").write_text("\n".join(ets_words) + "\n", encoding="utf-8")

    awl_words = []
    for path in sorted(ROOT.glob("toefl_awl_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            awl_words.extend(row[0].strip() for row in csv.reader(f, delimiter="\t") if row)
    (ROOT / "all_awl_headwords.txt").write_text("\n".join(awl_words) + "\n", encoding="utf-8")
    (ROOT / "all_headwords.txt").write_text("\n".join(sorted(set(ets_words + awl_words))) + "\n", encoding="utf-8")


def main() -> None:
    cards_by_file = load_cards()
    validate(cards_by_file)
    changed = rewrite(cards_by_file)
    write_cards(cards_by_file)
    refresh_wordlists(cards_by_file)
    for filename, count in changed.items():
        print(f"{filename}: {count} replaced")


if __name__ == "__main__":
    main()
