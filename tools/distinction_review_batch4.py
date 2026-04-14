#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


REPLACEMENTS: dict[str, dict[str, str | None]] = {
    "toefl_awl_set_02.tsv": {
        "secure": "secure=확보하다 / safe=안전한 상태이다",
        "seek": "seek=적극적으로 찾거나 추구하다 / request=공식적으로 요청하다",
        "select": "select=기준을 두고 골라 뽑다 / elect=투표로 뽑다",
        "deduce": "deduce=전제로부터 결론을 끌어내다 / infer=근거에서 추론하다",
        "maximize": "maximize=가능한 한 크게 하다 / optimize=가장 좋게 조정하다",
        "negate": "negate=효과·의미를 무효로 만들다 / deny=사실을 부인하다",
        "publish": "publish=공식적으로 출판·공개하다 / print=인쇄하다",
        "scheme": "scheme=조직적인 계획·제도 / plot=음모",
        "sex": "sex=생물학적 성 / gender=사회·정체성 차원의 성",
        "shift": "shift=방향·상태가 바뀌다 / transfer=옮기다",
        "commit": "commit=책임 있게 전념하다 / promise=약속하다",
        "debate": "debate=찬반 근거를 두고 토론하다 / discuss=폭넓게 논의하다",
        "emerge": "emerge=새로 드러나다 / arise=생겨나다",
        "implicate": "implicate=연루시키거나 함축하다 / imply=암시하다",
        "principal": "principal=주요한·교장·원금 / principle=원칙",
        "statistic": "statistic=통계치 한 개 / data=자료 전반",
        "undertake": "undertake=책임지고 맡아 시작하다 / attempt=가볍게 시도하다",
        "academy": None,
        "clause": "clause=문장 속 절 또는 계약 조항 / sentence=완결된 문장",
        "evolve": "evolve=점진적으로 발달하다 / transform=큰 폭으로 바뀌다",
        "expose": "expose=드러내거나 노출시키다 / reveal=밝혀 보이다",
        "liberal": "liberal=자유주의적인 / conservative=보수적인",
        "license": "license=공식 허가·면허 / permit=허가증",
        "pursue": "pursue=목표를 계속 추구하다 / seek=찾거나 구하다",
    },
    "toefl_ets_2026_set_03.tsv": {
        "adjacent": "adjacent=바로 옆의 / nearby=가까운",
        "alter": "alter=일부를 바꾸다 / transform=근본적으로 바꾸다",
        "approach": "approach=문제에 접근하는 방식 / method=실행하는 구체적 방법",
        "attain": "attain=노력 끝에 이루다 / reach=도달하다",
        "capable": "capable=능력이 있다 / competent=충분히 해낼 만큼 유능하다",
        "cease": "cease=공식적으로 중단하다 / suspend=일시 중단하다",
        "channel": "channel=흐름이나 전달의 통로 / medium=전달 매체",
        "circulate": "circulate=여러 곳을 돌며 퍼지다 / spread=널리 퍼지다",
        "collapse": "collapse=갑자기 무너지다 / decline=점차 약해지다",
        "comprehensive": "comprehensive=빠짐없이 포괄한 / detailed=세부가 자세한",
        "compute": "compute=수치로 계산하다 / estimate=대략 추산하다",
        "conceive": "conceive=개념을 떠올리다 / devise=방법을 고안하다",
        "concurrent": "concurrent=같은 시기에 함께 일어나는 / parallel=나란히 진행되는",
        "consistent": "consistent=앞뒤가 일관된 / coherent=논리적으로 잘 이어진",
        "constant": "constant=계속 이어지는 / stable=크게 변하지 않는",
        "consume": "consume=써서 소모하다 / exhaust=완전히 고갈시키다",
        "contemporary": "contemporary=같은 시대의 / modern=현대의",
        "conventional": "conventional=관습적으로 통용되는 / traditional=오래 전해 온",
        "coordinate": "coordinate=여러 부분을 맞춰 조정하다 / integrate=하나로 통합하다",
        "core": None,
        "decade": None,
        "definite": "definite=분명한 / specific=구체적인",
        "deny": "deny=사실을 부인하다 / refuse=거부하다",
        "designate": "designate=공식적으로 지정하다 / assign=맡기거나 배정하다",
        "device": "device=특정 기능을 가진 기기 / equipment=장비 전체",
        "distribute": "distribute=여러 곳에 나누어 주다 / allocate=몫을 정해 배정하다",
        "domestic": "domestic=국내의 / household=가정의",
        "duration": "duration=지속된 시간의 길이 / interval=사이의 간격",
        "economy": "economy=경제 체제 전반 / market=거래가 이루어지는 시장",
        "element": "element=구성 요소 / factor=영향을 주는 요소",
        "equate": "equate=같다고 여기다 / compare=비교하다",
        "equivalent": "equivalent=가치·기능이 같은 / equal=양이 같은",
        "erode": "erode=서서히 깎이거나 약해지다 / destroy=한꺼번에 크게 파괴하다",
        "ethical": "ethical=윤리에 맞는 / legal=법에 맞는",
    },
    "toefl_ets_2026_set_05.tsv": {
        "broaden": "broaden=범위를 넓히다 / deepen=더 깊게 하다",
        "code": None,
        "commission": None,
        "compete": "compete=서로 이기려 다투다 / cooperate=함께 협력하다",
        "complement": "complement=부족한 부분을 보완하다 / replace=대신하다",
        "confer": "confer=공식적으로 주다 / discuss=의논하다",
        "couple": "couple=둘을 연결하다 / pair=둘을 한 짝으로 묶다",
        "dispose": "dispose=처리하다 / arrange=배치하다",
        "edit": "edit=표현을 손봐 다듬다 / revise=내용까지 다시 고치다",
        "evident": "evident=보면 분명한 / explicit=분명히 말로 드러난",
        "exceed": "exceed=기준을 넘다 / surpass=더 뛰어나다",
        "flexible": "flexible=상황에 맞게 바꿀 수 있는 / stable=안정적으로 거의 안 바뀌는",
        "highlight": "highlight=눈에 띄게 강조하다 / indicate=가리키다",
        "hypothetical": "hypothetical=가정에 근거한 / theoretical=이론 차원의",
        "immune": "immune=영향을 받지 않거나 면역된 / resistant=버텨 내는 성향이 있는",
        "label": "label=이름표를 붙이거나 분류하다 / classify=유형별로 분류하다",
        "link": "link=연결 짓다 / associate=연관 짓다",
        "locate": "locate=위치를 찾아내다 / identify=무엇인지 밝혀내다",
        "methodology": "methodology=방법론 / method=개별 방법",
        "occupy": "occupy=공간·시간을 차지하다 / possess=소유하다",
        "output": "output=생산·산출된 양 / outcome=결과",
        "persist": "persist=계속 이어지다 / remain=그대로 남아 있다",
        "precede": "precede=앞서 오다 / follow=뒤따르다",
        "quote": "quote=말이나 문장을 그대로 인용하다 / cite=출처를 언급하다",
        "radical": "radical=근본부터 바꾸는 / gradual=점진적인",
        "random": "random=무작위의 / arbitrary=근거 없이 제멋대로인",
        "reveal": "reveal=드러내 보이다 / indicate=시사하다",
        "subsidy": "subsidy=특정 목적의 보조금 / grant=심사·지원 성격의 지원금",
        "sustain": "sustain=지속시키다 / maintain=현재 상태를 유지하다",
    },
    "toefl_ets_2026_set_08.tsv": {
        "contribute": "contribute=결과에 보태다 / cause=직접 원인이 되다",
        "discuss": "discuss=함께 논의하다 / debate=찬반을 두고 다투다",
        "draft": "draft=초안을 잡다 / outline=개요만 세우다",
        "dynamic": "dynamic=변화와 움직임이 큰 / stable=안정적인",
        "acute": "acute=갑작스럽고 심한 / chronic=오랫동안 계속되는",
        "chronic": "chronic=오랫동안 계속되는 / acute=갑작스럽고 심한",
        "baseline": "baseline=비교 출발점이 되는 기준선 / benchmark=평가에 쓰는 기준점",
        "regularity": "regularity=규칙적으로 되풀이됨 / consistency=앞뒤가 한결같음",
        "evaluate": "evaluate=가치·효과를 판단하다 / assess=수준·상태를 평가하다",
        "projection": "projection=추세를 바탕으로 한 전망 / estimate=대략적인 추산",
        "setback": "setback=진행이 뒤로 밀리는 차질 / failure=완전한 실패",
        "rehabilitation": "rehabilitation=기능 회복을 위한 훈련 / recovery=자연스러운 회복",
        "adverse": "adverse=해로운 결과를 낳는 / toxic=독성이 있는",
        "instruct": "instruct=절차를 알려 주다 / direct=어떻게 하라고 지시하다",
        "screening": "screening=집단을 먼저 걸러 보는 검사 / diagnosis=원인을 확정하는 진단",
        "method": "method=체계적인 방법 / technique=구체적 기법",
        "moderate": "moderate=중간 정도의 / extreme=극단적인",
        "organize": "organize=체계 있게 정리하다 / classify=기준별로 분류하다",
        "practical": "practical=실제 적용에 쓸 수 있는 / theoretical=이론 중심의",
        "priority": "priority=먼저 처리할 우선 항목 / urgency=당장 급한 정도",
        "revise": "revise=검토 후 내용을 고치다 / edit=문장을 다듬다",
        "malfunction": "malfunction=제대로 작동하지 않다 / defect=본래 결함이 있다",
        "schedule": "schedule=시간 순서로 짠 일정 / agenda=논의할 안건 목록",
        "transmission": "transmission=전파되는 과정 / spread=퍼져 나감",
        "widespread": "widespread=널리 퍼진 / localized=일부 지역에만 있는",
    },
    "toefl_ets_2026_set_13.tsv": {
        "redundancy": "redundancy=불필요한 중복 / repetition=반복 자체",
        "refute": "refute=근거로 반박하다 / deny=그냥 부인하다",
        "requisite": "requisite=필수 조건 / prerequisite=선행 조건",
        "scrutiny": "scrutiny=매우 세밀한 검토 / review=일반적 검토",
        "superfluous": "superfluous=있어도 쓸모없는 과잉 / redundant=중복되어 불필요한",
        "tentative": "tentative=잠정적인 / provisional=임시로 정한",
        "underscore": None,
        "unprecedented": "unprecedented=전례 없는 / novel=새로운",
        "validate": "validate=타당성·유효성을 확인 / verify=사실 여부를 확인",
        "contingency": "contingency=예상 밖 상황 가능성 / emergency=이미 닥친 긴급 사태",
        "corroborate": "corroborate=추가 증거로 뒷받침 / confirm=맞음을 확인",
        "deflect": "deflect=방향·주의를 다른 데로 돌리다 / evade=직접 답을 피하다",
        "detract": "detract=가치·품질을 깎다 / undermine=기반을 약화시키다",
        "diverge": "diverge=한 지점에서 갈라지다 / deviate=기준에서 벗어나다",
        "elucidate": "elucidate=복잡한 내용을 밝혀 설명 / clarify=헷갈리는 점을 분명히 하다",
        "encroach": "encroach=서서히 침범하다 / intrude=불쑥 끼어들다",
        "epitomize": "epitomize=핵심 특징을 대표하다 / exemplify=예시로 보여주다",
        "galvanize": "galvanize=행동하게 강하게 자극하다 / motivate=동기를 주다",
        "immutable": "immutable=본질적으로 바뀌지 않는 / fixed=지금 고정된",
        "impede": "impede=진행을 늦추며 방해하다 / obstruct=앞을 막아 가로막다",
        "impoverish": "impoverish=내용·자원을 빈약하게 하다 / deplete=고갈시키다",
        "juxtapose": "juxtapose=나란히 놓고 대비하다 / contrast=차이를 부각하다",
        "mobilize": "mobilize=자원·사람을 실제로 동원하다 / organize=체계 있게 정리하다",
        "omit": "omit=빠뜨리다 / exclude=의도적으로 빼다",
        "overt": "overt=겉으로 드러난 / implicit=겉으로 드러나지 않은",
        "peripheral": "peripheral=주변부의 / central=핵심의",
        "propensity": "propensity=특정 방향으로 기우는 성향 / tendency=일반적 경향",
        "salient": "salient=핵심이라 특히 눈에 띄는 / prominent=크게 눈에 띄는",
        "sparing": None,
        "tacit": "tacit=말하지 않아도 전제된 / explicit=분명히 말한",
        "transient": "transient=잠깐 스쳐 지나가는 / temporary=한동안만 지속되는",
        "guideline": "guideline=따르는 것이 권장되는 지침 / rule=반드시 지켜야 하는 규칙",
        "milestone": "milestone=중간의 중요한 성취점 / deadline=끝내야 하는 시점",
        "shortage": "shortage=필요량에 못 미치는 부족 / scarcity=원래 드문 희소함",
        "diminish": "diminish=점점 줄어들다 / disappear=아예 사라지다",
        "supply": "supply=필요한 것을 제공하다·공급량 / demand=필요로 하는 양",
        "review": "review=다시 살펴보다 / revise=고쳐 다듬다",
        "reserve": "reserve=비축해 둔 것 / stock=현재 보유량",
        "irrigate": "irrigate=농지에 물을 대다 / drain=물을 빼다",
    },
    "toefl_ets_2026_set_18.tsv": {
        "revolt": "revolt=체제에 맞선 봉기 / protest=반대 의사 표시",
        "leadership": "leadership=이끄는 능력이나 지도부 / authority=공식 권한",
        "sedentary": "sedentary=정착해 사는 / nomadic=이동하며 사는",
        "slavery": "slavery=노예 상태·제도 / servitude=강한 종속 상태",
        "stratified": "stratified=층위가 나뉜 / hierarchical=위계가 뚜렷한",
        "succession": "succession=지위·권력의 계승 / inheritance=재산의 상속",
        "uprising": "uprising=집단적 봉기 / protest=항의 행동",
        "urbanization": "urbanization=도시로 집중되는 과정 / industrialization=산업 중심 구조 변화",
        "idealized": "idealized=현실보다 이상화된 / realistic=현실적인",
        "preindustrial": "preindustrial=산업화 이전의 / industrial=산업화된",
        "rule-bound": "rule-bound=규칙에 강하게 묶인 / flexible=유연한",
        "precolonial": "precolonial=식민 지배 이전의 / colonial=식민 지배기의",
        "remnant": "remnant=남은 일부 / relic=과거의 흔적",
        "shrine": "shrine=숭배·기념의 성소 / temple=종교 의식 공간",
        "urbanism": "urbanism=도시적 생활 양식·사고 / urbanization=도시화 과정",
        "subordinate": "subordinate=상위 체계 아래 놓인 / dependent=의존적인",
        "upheaval": "upheaval=질서를 뒤흔드는 격변 / reform=개선 목적의 변화",
        "agrarian": "agrarian=농업 기반의 / industrial=산업 기반의",
        "stronghold": None,
        "exile": "exile=추방되거나 망명한 상태 / migration=자발적 이동",
        "bandwidth": "bandwidth=처리 가능한 용량 / capacity=수용 가능량",
        "data-driven": "data-driven=데이터 근거 중심의 / empirical=관찰·자료 기반의",
        "digitize": "digitize=디지털 형식으로 바꾸다 / scan=이미지로 읽어 들이다",
        "filter": "filter=기준에 따라 걸러내다 / sort=순서나 기준으로 나누다",
        "indexing": "indexing=검색할 수 있게 항목화함 / archiving=장기 보관함",
        "latency": "latency=응답이 돌아오기까지의 지연 / lag=체감되는 뒤처짐",
        "misinformation": "misinformation=틀린 정보 / disinformation=의도적 허위정보",
    },
    "toefl_ets_2026_set_24.tsv": {
        "proofread": "proofread=오탈자만 교정하다 / revise=내용까지 고쳐 다듬다",
        "reword": "reword=표현만 바꿔 쓰다 / paraphrase=의미를 풀어 다시 쓰다",
        "redraft": "redraft=초안을 다시 쓰다 / revise=일부를 고쳐 다듬다",
        "waiver": "waiver=요건·비용 면제 / exemption=규정상 면제",
        "refund": "refund=낸 돈을 돌려줌 / reimbursement=쓴 비용을 되갚음",
        "invoice": "invoice=청구서 / receipt=지불 증빙 영수증",
        "receipt": "receipt=영수증 / invoice=청구서",
        "deposit": "deposit=보증금·예치금 / fee=서비스 수수료",
        "stipend": "stipend=정액 지원금 / salary=근로 대가 급여",
        "reimbursement": "reimbursement=쓴 비용을 되갚음 / refund=낸 돈을 돌려줌",
        "referee": "referee=추천인·심판 / recommender=추천서 맥락 추천인",
        "recommender": "recommender=추천서 맥락 추천인 / referee=추천인·심판",
        "backup": "backup=복구용 예비본 / archive=장기 보관본",
        "registrar": "registrar=등록·성적 기록 담당 부서 / advisor=학업 조언 담당",
        "crosscheck": "crosscheck=서로 대조해 확인하다 / verify=사실 여부를 확인하다",
        "retake": "retake=시험을 다시 보다 / repeat=과목·과정을 다시 듣다",
        "regrade": "regrade=재채점하다 / appeal=이의 제기하다",
        "appeal": "appeal=공식적으로 이의 제기하다 / complain=불만을 말하다",
        "resubmit": "resubmit=수정 후 다시 제출하다 / reapply=다시 지원하다",
        "scan": "scan=문서를 디지털로 읽다 / photocopy=종이로 복사하다",
        "photocopy": "photocopy=종이로 복사하다 / scan=디지털로 읽다",
        "turnaround": "turnaround=처리 완료까지 걸리는 시간 / deadline=끝내야 하는 시점",
        "leadtime": "leadtime=시작 전에 필요한 준비 기간 / delay=예정보다 늦어짐",
        "advisor": "advisor=조언·학업 지도 담당 / supervisor=업무·연구 감독",
        "troubleshooting": "troubleshooting=오류 원인을 찾아 해결 / repair=고장 난 것을 고치다",
        "approximation": "approximation=정확값에 가까운 값 / estimate=대략 어림한 값",
        "scatter": "scatter=흩어져 퍼지다 / cluster=가깝게 모이다",
        "cluster": "cluster=가깝게 모인 군집 / scatter=흩어짐",
        "outlier": "outlier=다른 값과 크게 벗어난 이상치 / anomaly=눈에 띄는 이례 현상",
        "forecast": "forecast=근거를 바탕으로 전망하다 / estimate=현재 값을 어림잡다",
        "percentage": "percentage=전체 중 몇 퍼센트인지 / percent point=퍼센트의 차이",
        "median": "median=가운데 값 / mean=산술평균",
        "mean": "mean=산술평균 / median=가운데 값",
    },
}


def apply_changes(path: Path, changes: dict[str, str | None]) -> int:
    rows: list[tuple[str, str]] = []
    modified = 0

    with path.open(encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for headword, back in reader:
            if headword not in changes:
                rows.append((headword, back))
                continue

            target = changes[headword]
            lines = [line for line in back.split("\n") if not line.startswith("구분:")]
            if target is not None:
                lines.append(f"구분: {target}")
            new_back = "\n".join(lines)
            if new_back != back:
                modified += 1
            rows.append((headword, new_back))

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    return modified


def main() -> int:
    total = 0
    changed_files = 0
    for name, changes in REPLACEMENTS.items():
        path = Path(name)
        modified = apply_changes(path, changes)
        if modified:
            changed_files += 1
            total += modified
            print(f"{path.name}: {modified}")
    print(f"changed_files={changed_files} changed_rows={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
