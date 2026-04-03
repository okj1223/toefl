from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_17.tsv"

CARDS = [
    ("administrability", "행정적으로 운영 가능함", "좋은 원칙이어도 실제 조직과 절차 안에서 집행할 수 있는 정도", "아이디어가 문서 밖 실제 행정으로 굴러가는지 보는 느낌", "administrability=행정 운영 가능성 / feasibility=실현 가능성 / implementation=실행"),
    ("advocacy", "옹호 / 정책 지지 활동", "어떤 집단이나 입장을 위해 근거를 들며 지지하고 설득하는 활동", "가만히 관망하지 않고 이쪽 입장을 밀어주는 목소리", "advocacy=공개적으로 옹호·지지함 / lobbying=정책 결정자에게 압력을 넣음 / support=일반적 지지"),
    ("allocation formula", "배분 공식 / 할당 기준식", "자원이나 예산을 어떤 기준으로 나눌지 정한 계산 규칙", "누구에게 얼마를 줄지 감이 아니라 규칙표로 나누는 느낌", "allocation formula=배분 계산 기준식 / quota=할당량 / budget rule=예산 규칙"),
    ("appeal process", "이의 제기 절차 / 항소 절차", "결정에 동의하지 않을 때 다시 검토를 요청하는 공식 단계", "한 번 결정으로 끝내지 않고 다시 따져볼 문을 여는 절차", "appeal process=결정 재검토를 요청하는 절차 / complaint=불만 제기 / review=검토"),
    ("authorizing body", "승인 기관 / 권한 부여 주체", "정책이나 사업, 규칙을 공식적으로 허가할 권한을 가진 조직", "최종 OK 도장을 찍을 권한이 있는 쪽", "authorizing body=공식 승인 권한을 가진 기관 / committee=심의 집단 / agency=집행 기관"),
    ("beneficiary", "수혜자 / 혜택을 받는 사람", "정책이나 프로그램의 지원과 혜택을 실제로 받는 대상", "설계가 아니라 결과를 직접 받는 사람", "beneficiary=혜택을 받는 대상 / recipient=공식 수령인 / participant=참가자"),
    ("budgetary", "예산상의 / 재정 배분과 관련된", "돈이 어디서 나오고 어디에 쓰이는지와 관련된", "좋은 말보다 예산표에서 실제로 감당 가능한지를 보는 느낌", "budgetary=예산·재정 배분과 관련된 / fiscal=국가 재정의 / financial=돈 전반의"),
    ("caseworker", "사례 담당자 / 개별 지원 담당 직원", "개별 사람이나 가구의 상황을 따라가며 지원 절차를 돕는 담당자", "제도 전체보다 한 사람의 상황을 맡아 붙어서 따라가는 실무자", "caseworker=개별 사례를 맡아 돕는 담당자 / coordinator=업무 조정자 / counselor=상담자"),
    ("citizen input", "시민 의견 / 주민 참여 의견", "정책이나 사업을 정할 때 시민이 내는 의견과 제안", "결정권자끼리만 닫고 하지 않고 바깥 목소리를 넣는 느낌", "citizen input=시민이 제공하는 의견 / public comment=공식 의견 제출 / feedback=반응·조언"),
    ("coordinating agency", "조정 기관 / 관계 기관 연결 담당 조직", "여러 부서나 집단이 따로 움직이지 않게 역할과 일정을 맞추는 조직", "흩어진 실무 라인을 한 줄로 꿰어주는 중심 기관", "coordinating agency=여러 주체를 조율하는 기관 / regulator=규제 담당자 / operator=실제 운영 주체"),
    ("decentralize", "분권화하다 / 권한을 분산하다", "결정과 자원을 한 중심에만 두지 않고 여러 지역·기관으로 나누다", "한 꼭대기에서 다 잡지 않고 아래와 옆으로 나눠 맡기는 느낌", "decentralize=권한을 분산하다 / delegate=권한·업무를 맡기다 / centralize=한 중심으로 모으다"),
    ("deliverable-based", "산출물 기준의 / 결과물 중심의", "추상적 노력보다 제출 가능한 결과물과 완료 항목을 기준으로 삼는", "얼마나 바빴나보다 무엇을 실제로 내놨는지 보는 느낌", "deliverable-based=결과물 기준의 / outcome-based=성과 중심의 / process-based=과정 중심의"),
    ("discretionary", "재량적인 / 선택적으로 쓸 수 있는", "법이나 규칙 안에서도 담당자나 기관이 어느 정도 판단해 선택할 수 있는", "딱 한 길만 강제하지 않고 상황에 따라 손을 움직일 여지가 있는 느낌", "discretionary=재량으로 판단 가능한 / mandatory=의무적인 / optional=선택 가능한"),
    ("eligibility", "자격 요건 충족 / 지원 대상 자격", "혜택이나 프로그램을 받을 조건에 해당하는 상태", "아무나 들어가는 게 아니라 기준선 안에 들어왔는지 보는 느낌", "eligibility=지원·혜택 대상 자격 / qualification=요건을 갖춤 / admission=들어오도록 허가함"),
    ("enforcement", "집행 / 강제 이행", "정해진 규칙이나 결정이 실제로 지켜지도록 적용하고 요구하는 일", "종이에만 있던 규칙을 현실에서 안 지키면 움직여 잡는 느낌", "enforcement=규칙을 실제로 지키게 집행함 / implementation=정책을 실행함 / regulation=규칙으로 통제함"),
    ("entitlement", "법적 수급권 / 당연히 받을 권리", "정해진 조건을 충족하면 제도적으로 받을 수 있는 권리나 혜택", "호의로 받는 게 아니라 제도상 내 몫으로 청구할 수 있는 느낌", "entitlement=규정상 받을 권리 / benefit=혜택 / privilege=특권"),
    ("equity-oriented", "형평성 중심의", "모두에게 똑같이보다 조건 차이를 고려해 더 공정한 결과를 보려는", "표면상 동일보다 실제 불리함을 줄이는 공정 쪽에 눈이 가는 느낌", "equity-oriented=형평성에 초점을 둔 / equal=동일한 / fairness-based=공정성 중심의"),
    ("federated", "연합형의 / 분산된 단위가 연결된", "하나의 단일 중심보다 여러 단위가 연결되어 함께 작동하는", "각자 독립성은 두되 느슨하게 묶어 한 체계로 움직이는 느낌", "federated=여러 단위가 연결된 연합형의 / centralized=중앙집중형의 / distributed=여러 곳에 나뉜"),
    ("funding stream", "재원 흐름 / 자금 공급 경로", "돈이 어느 출처에서 어느 프로그램이나 조직으로 흘러가는지의 경로", "예산이 한 곳에 머물지 않고 어떤 길로 흘러 들어오는지 보는 느낌", "funding stream=자금이 흘러오는 경로 / revenue source=수입원 / grant=지원금"),
    ("grievance", "공식 불만 / 고충 제기", "불공정하거나 문제가 있다고 느껴 절차 안에서 제기하는 불만", "그냥 속상함이 아니라 제도 안에 올리는 문제 제기", "grievance=공식 고충·불만 제기 / complaint=불만 / appeal=결정 재검토 요청"),
    ("implementer", "실행 담당자 / 집행 주체", "정책이나 계획을 실제 현장에서 적용하고 움직이는 사람이나 조직", "설계자보다 문서 내용을 실제 행동으로 옮기는 쪽", "implementer=정책·계획을 실행하는 주체 / planner=계획을 짜는 사람 / administrator=행정을 운영하는 사람"),
    ("incentivize", "유인을 주다 / 그렇게 하도록 만들다", "보상이나 제도 설계를 통해 특정 행동을 더 하게 만들다", "하고 싶게 만드는 당근이나 구조를 걸어 행동을 끌어내는 느낌", "incentivize=보상·유인으로 행동을 끌어냄 / motivate=동기를 부여함 / require=의무로 요구함"),
    ("inclusionary", "포용적인 / 배제하지 않으려는", "특정 집단을 빠뜨리지 않고 정책이나 절차 안에 포함하려는", "문을 좁게 닫기보다 더 많은 사람이 들어올 자리를 만드는 느낌", "inclusionary=배제를 줄이고 포함하려는 / inclusive=포용적인 / selective=선별적인"),
    ("interagency", "기관 간의 / 여러 부처가 함께하는", "한 기관 내부만이 아니라 서로 다른 조직이나 부처 사이에 걸친", "칸막이 하나 안이 아니라 기관들 사이를 가로지르는 느낌", "interagency=기관들 사이에 걸친 / internal=조직 내부의 / cross-sector=여러 부문에 걸친"),
    ("jurisdictional", "관할권의 / 담당 구역과 권한에 관한", "누가 어떤 영역에 대해 법적·행정적 권한을 갖는지와 관련된", "이 일은 어느 쪽이 책임지고 결정할 수 있는지 경계를 따지는 느낌", "jurisdictional=관할 권한·구역과 관련된 / regional=지역의 / legal=법적인"),
    ("localize", "현지화하다 / 지역 조건에 맞추다", "일반 원칙이나 제도를 특정 지역 상황에 맞게 조정하다", "한 벌짜리 규칙을 그대로 덮지 않고 그 지역 옷에 맞게 줄이는 느낌", "localize=지역 조건에 맞게 조정하다 / adapt=변화에 맞춰 바꾸다 / standardize=하나의 기준으로 맞추다"),
    ("mandated", "의무화된 / 공식적으로 요구된", "선택이 아니라 규정이나 권한으로 반드시 하도록 정해진", "안 해도 되는 선택지가 아니라 해야 한다고 못 박힌 느낌", "mandated=공식적으로 의무화된 / required=필수의 / optional=선택의"),
    ("multi-stakeholder", "다양한 이해관계자가 참여하는", "한 주체만이 아니라 여러 관련 집단이 함께 얽힌", "결정표에 여러 쪽 목소리와 이해가 같이 올라오는 느낌", "multi-stakeholder=여러 이해관계자가 얽힌 / unilateral=한쪽이 단독으로 하는 / participatory=참여형의"),
    ("noncompliance", "규정 미준수 / 불이행", "정해진 규칙이나 요구를 따르지 않는 상태", "규칙선 밖으로 벗어나 있는데도 안 맞춘 상태", "noncompliance=규정을 지키지 않음 / violation=위반 / resistance=따르지 않으려는 저항"),
    ("operationalize", "실행 가능한 형태로 옮기다 / 조작화하다", "추상적 개념이나 정책 목표를 실제 절차나 측정 항목으로 바꾸다", "큰 말을 현장에서 움직일 버튼과 기준으로 바꾸는 느낌", "operationalize=추상 개념을 실제 실행·측정 형태로 바꿈 / implement=실행하다 / define=의미를 규정하다"),
    ("ordinance", "조례 / 지방 규정", "특정 지역이나 지방정부가 정하는 공식 규칙", "국가 전체 법보다 지역 단위로 적용되는 규칙", "ordinance=지방 조례·규정 / law=법 일반 / policy=방침"),
    ("oversight board", "감독 위원회 / 감시 기구", "운영이 기준과 책임에 맞는지 점검하는 공식 집단", "실행하는 쪽 위에서 제대로 하는지 눈을 떼지 않는 판", "oversight board=운영을 감독하는 위원회 / committee=심의 집단 / regulator=규제 주체"),
    ("pilot program", "시범 사업 / 시험 운영 프로그램", "전면 도입 전에 작은 규모로 먼저 해보며 효과와 문제를 확인하는 제도", "바로 전체로 깔기 전에 작은 판에서 먼저 시험해보는 느낌", "pilot program=작게 먼저 해보는 시범 사업 / full rollout=전면 시행 / trial=시험적 시도"),
    ("policymaking", "정책 결정 / 정책 형성", "문제를 어떻게 다룰지 규칙과 방향, 자원 배분을 공식적으로 정하는 과정", "현실 문제를 다룰 큰 규칙과 방향을 짜는 결정 과정", "policymaking=정책을 만드는 과정 / governance=운영·통치 체계 / administration=집행 행정"),
    ("public comment", "공식 의견 제출 / 공개 의견 수렴", "정책이나 규정안에 대해 일반 시민이나 이해관계자가 내는 공개 의견", "초안이 닫히기 전에 바깥 목소리를 공식 창구로 넣는 느낌", "public comment=공개 절차 안에서 내는 공식 의견 / feedback=반응·조언 / protest=항의"),
    ("redistributive", "재분배적인 / 자원을 다시 나누는", "기존 자원이나 혜택의 분배를 바꿔 집단 간 차이를 조정하려는", "처음 나뉜 몫을 그대로 두지 않고 다시 갈라 맞추는 느낌", "redistributive=자원을 다시 나누는 / distributive=분배와 관련된 / compensatory=손실을 보전하는"),
    ("regulatory scope", "규제 범위 / 적용 관할", "어떤 규칙이나 기관이 어디까지 다루고 적용할 수 있는지의 범위", "이 규칙의 손이 닿는 선이 어디까지인지 보는 느낌", "regulatory scope=규제의 적용 범위 / jurisdiction=관할권 / coverage=포괄 범위"),
    ("rollout", "단계적 도입 / 시행 개시", "정책이나 서비스를 한꺼번에 또는 순차적으로 현장에 내놓기 시작함", "준비한 것을 문서 안에 두지 않고 바깥으로 깔기 시작하는 느낌", "rollout=실제 현장 도입·배포 / implementation=실행 / launch=시작 공개"),
    ("rulemaking", "규칙 제정 / 시행 규정 만들기", "정책 원칙을 구체적 규정과 절차로 공식화하는 과정", "큰 방향을 현장에서 따를 세부 규칙 문장으로 바꾸는 느낌", "rulemaking=공식 규칙을 제정함 / legislation=법을 만드는 일 / enforcement=규칙을 집행함"),
    ("service delivery", "서비스 제공 / 현장 전달", "정책이나 지원이 실제 대상자에게 어떻게 전달되고 도달하는지", "제도 설계가 책상에서 끝나지 않고 사람에게 실제로 닿는 흐름", "service delivery=서비스가 대상자에게 실제 제공됨 / implementation=실행 / outreach=외부 연결 활동"),
    ("streamline", "간소화하다 / 절차를 매끄럽게 하다", "불필요한 단계나 중복을 줄여 진행이 더 빠르고 단순하게 되도록 하다", "복잡한 줄을 걷어내서 한 줄로 부드럽게 흐르게 하는 느낌", "streamline=절차를 간소화해 매끄럽게 함 / simplify=단순하게 함 / facilitate=쉽게 진행되게 돕다"),
    ("subsidize", "보조금을 주다 / 재정 지원하다", "비용 부담을 줄이도록 공공 자금이나 외부 돈으로 일부를 지원하다", "전체 값을 혼자 다 내게 두지 않고 뒤에서 돈을 보태주는 느낌", "subsidize=비용을 일부 지원하다 / sponsor=후원하다 / fund=자금을 대다"),
    ("targeting criteria", "대상 선정 기준", "어떤 집단이나 지역을 우선 지원 대상으로 삼을지 정하는 조건", "누구에게 먼저 자원을 보낼지 가르는 필터 기준", "targeting criteria=지원 대상을 고르는 기준 / eligibility=자격 요건 / screening=선별 심사"),
    ("transparency rule", "투명성 규칙 / 공개 기준", "결정 근거와 과정, 정보 공개 수준을 분명히 하도록 정한 기준", "어떻게 정했는지 안 보이게 숨기지 말라는 공개 원칙", "transparency rule=과정과 근거를 드러내게 하는 규칙 / disclosure=정보 공개 / confidentiality=비밀 유지"),
    ("unfunded", "재원이 없는 / 예산이 붙지 않은", "필요한 실행 비용이나 공식 재정 지원이 배정되지 않은", "하라고는 했지만 실제 돈줄이 안 붙은 느낌", "unfunded=예산이나 재원이 배정되지 않은 / underfunded=돈이 부족하게 배정된 / funded=자금이 지원된"),
    ("uptake rate", "이용률 / 채택 속도", "사람이나 조직이 새 제도·서비스·정보를 얼마나 빠르게 받아들이는지의 비율", "만들어 둔 것이 실제로 얼마나 빨리 사람들 손에 잡히는지 보는 눈금", "uptake rate=새 제도·서비스를 받아들이는 비율 / adoption rate=채택 비율 / participation rate=참여 비율"),
    ("vulnerable group", "취약 집단 / 보호가 필요한 집단", "위험이나 손실, 배제에 더 쉽게 노출되는 사람들의 집단", "같은 충격에도 더 먼저 흔들릴 수 있어 따로 보호를 봐야 하는 집단", "vulnerable group=위험에 더 취약한 집단 / minority=소수 집단 / disadvantaged group=불리한 조건의 집단"),
    ("whole-of-government", "정부 전체가 함께하는 / 범정부적", "한 부처만이 아니라 여러 정부 기관이 함께 연계해 움직이는", "칸막이 하나만 움직이지 않고 정부 전체가 한 팀처럼 맞추는 느낌", "whole-of-government=여러 정부 기관이 함께하는 / interagency=기관 간의 / centralized=한 중심에 모인"),
    ("zoning", "구역 지정 / 용도별 지역 규제", "토지나 공간을 어떤 용도로 쓸 수 있는지 구역별로 나눠 정하는 일", "지도 위를 칸칸이 나눠 여기선 무엇이 가능한지 정해두는 느낌", "zoning=공간을 용도별로 구역 규정함 / planning=계획 수립 / designation=공식 지정"),
    ("case review", "사례 검토 / 개별 건 재심사", "한 사람이나 한 사건의 자료를 다시 보고 판단과 조치를 점검하는 일", "제도 전체가 아니라 이 한 건을 열어 다시 따져보는 느낌", "case review=개별 사례를 다시 검토함 / audit=기록과 절차를 점검함 / appeal process=이의 제기 절차"),
    ("community liaison", "지역사회 연결 담당자", "기관과 주민, 이용자 사이의 소통과 연결을 맡는 사람", "조직 안 말과 바깥 현장 목소리를 오가게 하는 다리", "community liaison=기관과 지역사회를 잇는 담당자 / spokesperson=공식 발언자 / coordinator=업무 조정자"),
    ("compliance audit", "준수 감사 / 규정 이행 점검", "정해진 기준과 규칙을 실제로 따랐는지 기록과 절차를 조사하는 일", "말로 지켰다가 아니라 증거를 열어 정말 맞췄는지 보는 느낌", "compliance audit=규정 준수를 점검하는 감사 / oversight=감독·감시 / review=검토"),
    ("cost-sharing", "비용 분담", "한쪽이 전부 부담하지 않고 여러 주체가 비용을 나누어 맡는 방식", "청구서를 한 사람에게 몰지 않고 여러 몫으로 나눠 드는 느낌", "cost-sharing=비용을 여러 주체가 나눠 부담함 / subsidy=일부를 보조해줌 / allocation=자원·비용 배분"),
    ("cross-jurisdictional", "여러 관할권에 걸친", "하나의 법적·행정적 경계 안에만 머물지 않고 여러 구역과 권한을 가로지르는", "담당 구역 선 하나로 안 끊기고 여러 경계를 넘나드는 느낌", "cross-jurisdictional=여러 관할권에 걸친 / local=한 지역 안의 / transboundary=경계를 가로지르는"),
    ("defunding", "재정 지원 중단 / 예산 삭감", "기존에 붙어 있던 자금을 줄이거나 끊어 사업이나 조직의 재원을 빼는 일", "돌아가던 돈줄을 조이거나 끊어서 판을 작게 만드는 느낌", "defunding=지원 예산을 줄이거나 끊음 / budget cut=예산 삭감 / underfunding=불충분한 지원"),
    ("disbursement", "자금 지급 / 지출 집행", "승인된 예산이나 지원금을 실제로 내보내 대상자나 사업에 전달함", "예산표에만 두지 않고 돈이 실제로 밖으로 나가는 단계", "disbursement=승인된 자금을 지급·집행함 / expenditure=돈을 씀 / allocation=어디에 나눌지 배정함"),
    ("equity audit", "형평성 점검 / 불균형 검토", "정책이나 서비스가 집단 간에 불리함이나 편차를 만들지 않는지 점검하는 일", "표면상 운영보다 누가 더 빠지고 밀리는지 다시 비춰보는 검사", "equity audit=형평성 문제를 점검함 / compliance audit=규정 준수를 점검함 / assessment=평가"),
    ("evidence-based", "증거 기반의 / 근거 중심의", "정책이나 판단을 주장보다 자료와 검증된 결과에 기대어 세우는", "좋아 보이는 말보다 실제 근거를 먼저 깔고 가는 느낌", "evidence-based=검증된 근거에 기반한 / data-driven=자료를 근거로 한 / opinion-based=의견 중심의"),
    ("gatekeeping", "진입 통제 / 접근 문턱 관리", "누가 자원이나 기회, 정보에 들어올 수 있는지 앞단에서 걸러 정하는 일", "문 앞에서 들어갈 사람과 막힐 사람을 가르는 느낌", "gatekeeping=접근과 진입을 통제함 / screening=사전 선별함 / exclusion=배제"),
    ("governance gap", "통치 공백 / 관리 책임의 빈틈", "누가 맡는지 불분명하거나 조율이 안 돼 규칙과 책임이 비는 구간", "책임선 사이가 벌어져 아무도 제대로 안 잡는 빈틈", "governance gap=책임·관리 공백 / oversight gap=감독 빈틈 / loophole=규칙의 허점"),
    ("impact assessment", "영향 평가", "정책이나 사업이 실제로 어떤 결과와 부작용을 낼지 또는 냈는지 체계적으로 따지는 일", "해봤더니 무엇이 좋아지고 무엇이 흔들렸는지 결과 지도를 그리는 느낌", "impact assessment=정책·사업의 영향을 평가함 / evaluation=가치를 판단함 / risk assessment=위험을 평가함"),
    ("implementation gap", "실행 격차 / 계획-현장 차이", "정책 목표나 설계와 실제 현장 집행 사이에 생기는 차이", "문서에는 되는데 현장에서는 그만큼 안 따라오는 틈", "implementation gap=설계와 실제 실행 사이 차이 / policy gap=정책 목표와 현실의 간극 / discrepancy=불일치"),
    ("institutional buy-in", "기관 차원의 동의 / 조직적 지지 확보", "정책이나 변화가 실제로 굴러가도록 조직 내부가 받아들이고 지지하는 상태", "겉승인만이 아니라 안쪽 조직이 같이 움직여주려는 동의가 생긴 느낌", "institutional buy-in=조직이 변화나 정책을 받아들이고 지지함 / approval=공식 승인 / acceptance=받아들임"),
    ("means-tested", "소득·재산 기준 심사를 거치는", "누가 필요한지 자원 수준을 따져 제한적으로 지원 대상을 정하는", "모두에게 열기보다 필요 정도를 따져 문을 여는 방식", "means-tested=자산·소득 기준으로 지원 대상을 가림 / universal=보편적으로 모두에게 적용되는 / targeted=특정 대상 중심의"),
    ("outcome metric", "성과 지표 / 결과 측정 기준", "정책이나 프로그램이 어떤 결과를 냈는지 판단하는 측정 항목", "했는지 말만이 아니라 무엇이 달라졌는지 재는 눈금", "outcome metric=결과를 판단하는 지표 / indicator=상태를 보여주는 신호 / benchmark=비교 기준"),
    ("participatory planning", "참여형 계획 수립", "전문가나 기관만이 아니라 영향을 받는 사람들이 같이 의견을 내며 계획을 짜는 방식", "책상 안에서 혼자 정하지 않고 여러 사람이 같이 지도를 그리는 느낌", "participatory planning=참여자 의견을 반영해 계획을 세움 / top-down planning=위에서 내려오는 계획 / consultation=협의"),
    ("program uptake", "프로그램 이용 채택 / 제도 사용 증가", "대상자나 현장이 새 프로그램을 실제로 얼마나 받아들여 쓰는지", "만들어 둔 제도가 사람 손에 잡혀 실제로 쓰이기 시작하는 느낌", "program uptake=프로그램을 실제로 받아들여 사용함 / enrollment=등록 상태 / participation=참여"),
    ("procedural fairness", "절차적 공정성", "결과만이 아니라 결정 과정과 규칙 적용이 납득 가능하고 공정한 정도", "무슨 결론이냐뿐 아니라 그 결론까지 간 길이 공정했는지 보는 느낌", "procedural fairness=결정 절차의 공정성 / equity=조건 차이를 고려한 형평성 / transparency=과정 공개성"),
    ("public-facing service", "대민 서비스 / 시민 대상 서비스", "조직 내부 업무가 아니라 시민이나 이용자에게 직접 보이고 제공되는 서비스", "안쪽 사무가 아니라 바깥 사람이 실제로 마주하는 창구", "public-facing service=시민·사용자에게 직접 제공되는 서비스 / internal process=조직 내부 절차 / service delivery=서비스 제공"),
    ("quota-based", "할당량 기준의", "일정 수나 비율을 채우도록 목표나 배분을 정하는 방식의", "얼마를 채워야 한다는 숫자칸을 먼저 박아두는 느낌", "quota-based=할당량 기준으로 운영되는 / merit-based=성과·자격 기준의 / proportional=비율에 맞춘"),
    ("resource targeting", "자원 집중 지원 / 대상 맞춤 배분", "제한된 자원을 모두에게 똑같이보다 우선 필요한 대상과 문제에 맞춰 보내는 것", "넓게 흩뿌리기보다 필요한 지점에 조준해 넣는 느낌", "resource targeting=자원을 특정 필요나 대상에 맞춰 배분함 / allocation=나누어 배정함 / prioritization=우선순위를 정함"),
    ("service gap", "서비스 공백 / 제공이 비는 구간", "필요한 지원이나 이용 경로가 충분히 닿지 않아 생기는 빈틈", "제도가 있는데도 실제 사람에게 닿는 선이 중간에서 끊긴 느낌", "service gap=서비스가 충분히 제공되지 않는 빈틈 / access barrier=접근 장벽 / shortage=부족"),
    ("stakeholder mapping", "이해관계자 지도화 / 관련 주체 파악", "누가 영향을 받고 누가 결정과 실행에 관여하는지 관계와 위치를 정리하는 일", "흩어진 사람과 기관을 관계선 위에 올려 누가 어디 있는지 보는 느낌", "stakeholder mapping=관련 주체와 관계를 정리함 / network analysis=연결망을 분석함 / consultation=관련자와 협의함"),
    ("sunset clause", "일몰 조항 / 자동 종료 규정", "정해진 시간이 지나면 제도나 규정이 자동으로 끝나거나 재검토되도록 넣은 조항", "한 번 만든 규칙이 영원히 가는 게 아니라 끝나는 날짜를 미리 박아두는 느낌", "sunset clause=시간이 지나면 효력이 끝나게 하는 조항 / expiration=만료 / amendment=수정안"),
    ("underrepresented", "과소대표된 / 충분히 반영되지 않은", "어떤 집단이 실제 규모나 중요성에 비해 결정·참여·표현에서 덜 드러나는", "있긴 한데 판 위에서 자기 몫만큼 목소리가 안 잡힌 느낌", "underrepresented=대표성과 참여가 부족하게 반영된 / minority=소수 집단 / excluded=배제된"),
    ("user pathway", "이용자 경로 / 서비스 이용 흐름", "사람이 정보나 지원에 접근해 신청·이용·후속 단계로 이동하는 순서", "사용자가 제도 안에서 어느 문을 지나 어디로 가는지 따라가는 길", "user pathway=이용자가 거치는 단계별 경로 / service delivery=서비스 전달 / workflow=업무 흐름"),
    ("adjudicator", "판정자 / 심사 결정자", "쟁점이나 신청 건을 기준에 따라 검토하고 공식 판단을 내리는 사람", "의견을 듣고 마지막에 어느 쪽이 맞는지 판정하는 자리", "adjudicator=공식 판단을 내리는 사람 / reviewer=검토자 / mediator=중재자"),
    ("appropriation", "예산 배정 / 공식 재원 승인", "특정 목적에 쓸 공공 자금을 공식적으로 배정하거나 승인함", "돈이 어디로 가야 하는지 예산 봉투에 이름을 붙이는 느낌", "appropriation=공공 예산을 공식 배정함 / allocation=자원을 나눠 배정함 / expenditure=실제 지출"),
    ("benefit cap", "급여 상한 / 지원 한도", "받을 수 있는 혜택이나 지원액에 둔 최대 제한선", "필요해도 이 선 위로는 더 못 받게 천장을 씌운 느낌", "benefit cap=지원액의 상한선 / quota=할당량 / ceiling=최대 한계선"),
    ("case backlog", "미처리 사례 누적 / 밀린 처리 건", "아직 심사·처리하지 못한 개별 신청이나 사건이 쌓여 있는 상태", "서류가 줄 서서 뒤로 밀린 채 쌓이는 느낌", "case backlog=밀린 미처리 사례 묶음 / backlog=밀린 작업 목록 / caseload=담당 사례량"),
    ("citizen-facing", "시민 대상의 / 대민 창구 쪽의", "조직 내부용이 아니라 시민이 직접 보고 이용하는 서비스나 절차와 관련된", "사무실 안쪽보다 바깥 사람이 마주하는 앞창구 느낌", "citizen-facing=시민이 직접 마주하는 / public-facing=외부 공개용의 / internal=내부용의"),
    ("co-funding", "공동 재원 지원 / 비용 공동 부담", "한 기관만이 아니라 여러 주체가 함께 자금을 대는 방식", "한쪽 돈줄만 기대지 않고 여러 곳이 같이 비용을 받치는 느낌", "co-funding=여러 주체가 함께 재원을 지원함 / cost-sharing=비용을 나눠 부담함 / sponsorship=후원"),
    ("compliance burden", "준수 부담 / 규정 이행 비용", "규칙을 지키기 위해 드는 시간·서류·비용·행정 부담", "규정을 맞추느라 현장에 추가로 얹히는 무게", "compliance burden=규정을 지키는 데 드는 부담 / administrative cost=행정 비용 / oversight=감독"),
    ("coverage gap", "보장 공백 / 적용 누락 구간", "제도나 서비스가 필요한 사람이나 영역을 충분히 덮지 못해 생기는 빈틈", "제도 그물 사이로 일부 대상이 빠져나가는 구멍", "coverage gap=보장·적용이 비는 부분 / service gap=서비스 공백 / exclusion=배제"),
    ("decision rule", "결정 규칙 / 판단 기준", "어떤 조건에서 어떤 선택을 할지 미리 정해둔 공식 기준", "상황마다 흔들리지 않게 선택 버튼을 정해 둔 규칙", "decision rule=판단을 내리는 기준 규칙 / criterion=판단 항목 / guideline=지침"),
    ("devolution", "권한 이양 / 하위 단위로 넘김", "중앙이 갖던 권한이나 책임을 지역·하위 기관으로 넘기는 일", "위에서 쥐고 있던 결정을 아래 단위로 내려 보내는 느낌", "devolution=권한을 하위 단위로 이양함 / decentralization=권한 분산 / delegation=업무를 맡김"),
    ("eligibility screening", "자격 심사 / 지원 대상 선별", "신청자가 정해진 조건에 맞는지 먼저 검토해 걸러내는 과정", "문 안에 들이기 전에 기준표로 한 번 거르는 느낌", "eligibility screening=자격 요건을 먼저 심사함 / screening=사전 선별 / eligibility=자격 상태"),
    ("enrollment pathway", "등록 경로 / 참여 진입 절차", "대상자가 제도나 프로그램에 들어오기 위해 거치는 단계와 이동 흐름", "관심에서 신청, 등록까지 어느 문을 순서대로 지나가는지 보는 길", "enrollment pathway=등록까지 이어지는 진입 단계 / user pathway=이용자 경로 / registration=등록 절차"),
    ("fiscal year", "회계연도 / 예산 기준 연도", "예산 편성과 결산을 한 주기로 묶어 관리하는 공식 연도 단위", "달력 연도보다 예산표가 돌아가는 한 바퀴 기준", "fiscal year=예산·회계 관리 기준 연도 / calendar year=달력상 1년 / budget cycle=예산 주기"),
    ("governing charter", "운영 헌장 / 기본 규정 문서", "조직이나 제도의 목적, 권한, 운영 원칙을 정한 기본 문서", "세부 규칙 전에 이 조직이 무엇을 어떻게 할지 바닥 원칙을 적은 문서", "governing charter=운영 원칙과 권한을 정한 기본 문서 / constitution=기본 구조·헌법 / bylaw=세부 내규"),
    ("implementation toolkit", "실행 도구 모음 / 현장 적용 자료", "정책이나 제도를 현장에서 적용할 때 쓰는 양식·지침·점검표 묶음", "큰 방향을 실제 업무로 옮길 때 손에 들고 쓰는 실무 상자", "implementation toolkit=현장 실행을 돕는 도구·자료 묶음 / guideline=지침 / checklist=점검표"),
    ("inspection regime", "점검 체계 / 정기 검사 제도", "기준 준수 여부를 어떤 방식과 주기로 검사할지 정한 감독 구조", "가끔 눈대중이 아니라 언제 어떻게 볼지 짜인 검사 시스템", "inspection regime=정해진 방식의 점검·검사 체계 / oversight=감독 / monitoring=지속적 점검"),
    ("intervention package", "개입 프로그램 묶음 / 종합 지원 패키지", "한 조치만이 아니라 여러 지원이나 정책 수단을 묶어 제공하는 구성", "문제 하나에 카드 한 장이 아니라 여러 도구를 묶어 같이 쓰는 느낌", "intervention package=여러 조치를 묶은 개입 패키지 / program=운영 사업 / remedy=개선 수단"),
    ("legislative agenda", "입법 의제 / 법안 우선순위 목록", "어떤 법과 제도 변화를 우선 다룰지 정한 정치·입법 과제 목록", "여러 현안 중 법으로 먼저 손볼 항목을 줄 세운 목록", "legislative agenda=입법에서 우선 다룰 안건 목록 / agenda=논의 안건 목록 / policy priority=정책 우선순위"),
    ("monitoring framework", "모니터링 틀 / 점검 체계", "무엇을 어떤 지표와 주기로 볼지 정한 체계적 점검 구조", "그냥 자주 보는 게 아니라 어떤 눈금으로 어떻게 따라갈지 깔아둔 틀", "monitoring framework=체계적으로 점검하는 구조 / dashboard=현황을 모아 보여주는 화면 / evaluation=평가"),
    ("needs assessment", "수요·필요 평가", "대상 집단이 실제로 무엇이 부족하고 어떤 지원이 필요한지 체계적으로 파악하는 일", "무엇을 줄지 정하기 전에 어디가 얼마나 비어 있는지 먼저 재는 느낌", "needs assessment=필요와 부족을 체계적으로 파악함 / impact assessment=영향을 평가함 / survey=조사"),
    ("operating mandate", "운영 권한 / 수행 임무 범위", "조직이나 기관이 공식적으로 맡아 수행해야 하는 역할과 권한의 범위", "이 기관이 어디까지 책임지고 움직여야 하는지 적힌 임무선", "operating mandate=공식적으로 맡은 운영 권한·임무 / authorization=권한 부여 / jurisdiction=관할권"),
    ("policy alignment", "정책 정합성 / 정책 간 방향 맞춤", "여러 제도와 사업이 서로 충돌하지 않고 같은 목표와 기준에 맞게 연결된 정도", "각자 따로 노는 정책을 한 방향으로 줄 맞추는 느낌", "policy alignment=정책들 사이 방향과 기준이 맞음 / coordination=조정 / consistency=일관성"),
    ("program continuity", "사업 연속성 / 중단 없이 이어짐", "지원이나 운영이 단절되지 않고 다음 단계나 기간으로 계속 이어지는 상태", "한 번 시작한 서비스가 중간에 뚝 끊기지 않고 이어지는 느낌", "program continuity=사업·지원이 계속 이어짐 / continuity=연속성 / sustainability=지속 가능성"),
    ("provider network", "서비스 제공자 네트워크", "지원과 서비스를 실제로 제공하는 기관·인력·시설이 연결된 체계", "한 기관만이 아니라 여러 제공자들이 선으로 얽혀 있는 전달망", "provider network=서비스 제공 주체들의 연결망 / network=연결망 / service delivery=서비스 제공"),
    ("public mandate", "공적 위임 / 시민이 부여한 수행 명분", "조직이나 정부가 공공 목적을 위해 행동할 정당한 권한과 요구를 부여받은 상태", "하고 싶어서가 아니라 시민 쪽에서 맡긴 공적 임무를 받은 느낌", "public mandate=공적으로 부여받은 수행 권한·임무 / legitimacy=정당성 / authority=공식 권위"),
    ("quality assurance", "품질 보증 / 기준 충족 관리", "서비스나 결과가 정해진 수준을 꾸준히 충족하도록 점검하고 관리하는 일", "결과가 들쭉날쭉하지 않게 품질선 아래로 떨어지지 않도록 잡는 느낌", "quality assurance=품질 기준을 유지하도록 관리함 / validation=타당성을 확인함 / monitoring=계속 점검함"),
    ("reporting line", "보고 계통 / 지휘·책임선", "누가 누구에게 보고하고 책임지는지 정해진 조직 내 연결선", "일이 올라갈 때 어느 선을 따라 누구에게 닿는지 정해둔 줄", "reporting line=조직 내 보고·책임 연결선 / hierarchy=위계 구조 / workflow=업무 흐름"),
    ("service standard", "서비스 기준 / 제공 품질 기준", "이용자에게 제공해야 할 속도·정확성·절차 수준을 정한 기준", "대충 해도 되는 게 아니라 최소 이 정도로 제공하라는 품질선", "service standard=서비스 제공 수준 기준 / benchmark=비교 기준 / guideline=지침"),
    ("statutory", "법률로 정해진 / 법정의", "단순 권고가 아니라 법 조항과 공식 법적 근거에 의해 규정된", "좋으면 하고 말면 마는 게 아니라 법 안에 박힌 느낌", "statutory=법률에 의해 정해진 / regulatory=규정에 따른 / advisory=권고 성격의"),
    ("transition plan", "전환 계획 / 변경 이행 계획", "기존 제도나 방식에서 새 체계로 옮겨갈 때 어떤 순서로 바꿀지 정한 계획", "한 번에 확 바꾸다 무너지지 않게 넘어가는 다리를 놓는 느낌", "transition plan=새 체계로 넘어가는 단계 계획 / roadmap=진행 경로 / rollout=도입 시행"),
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
        manifest["files_created"].insert(16, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    gen = ROOT / "generation_notes.md"
    gen.write_text(
        gen.read_text(encoding="utf-8").replace(
            "- ETS sets `01` to `16` exist, bringing the ETS-based total to 1600 cards\n",
            "- ETS sets `01` to `17` exist, bringing the ETS-based total to 1700 cards\n",
        ),
        encoding="utf-8",
    )

    plan = ROOT / "WORK_PLAN.md"
    text = plan.read_text(encoding="utf-8")
    text = text.replace(
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_16.tsv`\n",
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_17.tsv`\n",
    )
    text = text.replace(
        "- Current ETS row count after the latest expansion pass: 1600\n",
        "- Current ETS row count after the latest expansion pass: 1700\n",
    )
    plan.write_text(text, encoding="utf-8")

    task_next = ROOT / ".task_next.md"
    task_next.write_text(
        task_next.read_text(encoding="utf-8")
        .replace("`toefl_ets_2026_set_17.tsv`", "`toefl_ets_2026_set_18.tsv`")
        .replace(
            "policy, governance, institutions, implementation, social programs, and public outcomes, with broad analytical language and limited bureaucracy jargon.",
            "argumentation, critique, interpretation, evidence framing, rhetorical stance, and scholarly communication across reading, speaking, and writing tasks.",
        ),
        encoding="utf-8",
    )

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
