from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_13.tsv"


CARDS = [
    ("agenda", "의제 / 안건", "회의에서 다룰 항목들 / 우선순위", "무엇을 먼저 논의할지 적어둔 목록", "agenda=논의 안건 목록 / schedule=시간표 / topic=주제 하나"),
    ("adjourn", "회의를 마치다 / 휴회하다", "논의를 잠시 멈추거나 공식 종료하다", "모임을 일단 접고 끝내는 느낌", "adjourn=회의를 마치다 / postpone=나중으로 미루다 / suspend=일시 중단하다"),
    ("alumni", "졸업생들 / 동문", "학교 출신자 집단", "같은 학교를 나온 사람들 묶음", "alumni=졸업생 집단 / graduates=졸업한 사람들 / classmates=같은 반·동기"),
    ("amendment", "수정안 / 개정", "문서·규칙·제안의 일부를 고친 내용", "원안을 조금 고쳐 끼워 넣는 느낌", "amendment=공식 수정안 / revision=전반적 수정 / correction=오류 바로잡기"),
    ("applicant", "지원자 / 신청자", "프로그램·장학금·직무 등에 신청한 사람", "기회를 얻으려고 서류를 낸 사람", "applicant=지원한 사람 / candidate=선발 대상자 / nominee=지명된 사람"),
    ("appointment", "약속 / 면담 예약", "정해진 만남 또는 공식 임명", "시간을 잡아 만나는 공식 자리", "appointment=예약된 만남 / reservation=자리·시설 예약 / meeting=논의 모임"),
    ("attendance", "출석 / 참석", "수업이나 행사에 실제로 온 상태", "자리에 와 있는지 세는 느낌", "attendance=출석 여부 / participation=활동 참여 / enrollment=등록 상태"),
    ("attendee", "참석자", "행사·강연·회의에 온 사람", "그 자리에 실제로 온 사람", "attendee=행사 참석자 / participant=활동에 참여하는 사람 / audience=듣고 보는 청중"),
    ("brainstorm", "아이디어를 자유롭게 내다", "초기 단계에서 여러 생각을 빠르게 모으다", "판단을 미루고 생각을 쏟아내는 느낌", "brainstorm=아이디어를 많이 내다 / discuss=의견을 나누다 / plan=실행안을 짜다"),
    ("briefing", "간략한 설명 / 사전 보고", "핵심 정보를 짧게 전달하는 안내", "본격 작업 전에 요점만 압축해 알려주는 느낌", "briefing=짧은 사전 설명 / report=조사·진행 보고 / lecture=수업형 강의"),
    ("bulletin", "공지 / 게시 안내문", "여러 사람에게 알리는 짧은 공식 안내", "게시판에 붙는 공지 느낌", "bulletin=게시형 공지 / announcement=공식 발표 / notice=알림문"),
    ("candidate", "후보자 / 검토 대상", "선발·임명·검증을 앞둔 사람이나 대안", "여러 선택지 중 심사 대상에 오른 것", "candidate=후보·심사 대상 / applicant=지원자 / option=선택 가능한 대안"),
    ("chairperson", "의장 / 회의 진행 책임자", "회의를 이끌고 발언 순서와 절차를 조정하는 사람", "회의 테이블의 중심에서 진행을 잡는 사람", "chairperson=회의 진행 책임자 / moderator=토론 흐름 조정자 / coordinator=업무 연결 담당자"),
    ("citation", "인용 / 참고문헌 표기", "출처를 밝히기 위해 다는 문헌 정보", "어디서 가져왔는지 근거를 붙이는 표시", "citation=출처 표기 / reference=참고문헌·참조 대상 / quotation=직접 인용문"),
    ("circulate", "돌려보다 / 회람하다", "자료나 정보를 여러 사람에게 차례로 전달하다", "문서가 사람들 사이를 한 바퀴 도는 느낌", "circulate=여러 사람에게 돌리다 / distribute=나누어 배포하다 / forward=전달해 보내다"),
    ("coauthor", "공동 저자", "한 논문이나 글을 함께 쓴 사람", "같은 글에 이름을 같이 올린 사람", "coauthor=공동 집필자 / collaborator=협력자 / contributor=기여한 사람"),
    ("cohort", "같은 집단 / 동기 집단", "같은 시기나 조건으로 묶인 연구·교육 집단", "같은 출발선을 공유하는 한 무리", "cohort=같은 기준으로 묶인 집단 / group=일반적 집단 / class=한 학년·수업 집단"),
    ("collaboration", "협업 / 공동 작업", "여러 사람이 역할을 나눠 함께 성과를 내는 일", "각자 따로가 아니라 같이 만들어 가는 느낌", "collaboration=함께 일함 / cooperation=서로 협조함 / coordination=일정을 맞춰 조율함"),
    ("colloquium", "학술 토론회 / 콜로키엄", "전문 발표 후 질의와 토론이 이어지는 학술 모임", "강의보다 더 토론 중심인 학술 자리", "colloquium=학술 토론 모임 / seminar=소규모 학술 수업·발표 / symposium=여러 발표가 있는 공식 학술 행사"),
    ("committee", "위원회", "특정 안건을 검토·결정하기 위해 꾸린 공식 집단", "일을 나눠 맡은 소수 결정 그룹", "committee=공식 심의 집단 / panel=발표·심사단 / board=최상위 이사회·위원회"),
    ("compile", "취합하다 / 편집해 모으다", "흩어진 자료를 모아 하나로 정리하다", "조각난 정보를 한 파일로 엮는 느낌", "compile=모아 정리하다 / collect=그냥 모으다 / summarize=핵심만 요약하다"),
    ("compliance", "규정 준수", "정해진 규칙·기준·절차를 따르는 상태", "룰에서 벗어나지 않게 맞춰 가는 느낌", "compliance=규정 준수 / obedience=명령 복종 / conformity=집단 기준에 맞춤"),
    ("consensus", "합의 / 의견 일치", "논의 끝에 대체로 함께 받아들이는 결론", "완벽히 같진 않아도 다 같이 고개를 끄덕이는 상태", "consensus=폭넓은 합의 / agreement=일반적 동의 / compromise=서로 양보한 절충"),
    ("consultation", "상담 / 협의", "조언을 구하거나 의견을 맞추기 위한 공식 대화", "혼자 정하지 않고 물어보고 조율하는 자리", "consultation=전문가·관계자와 상담·협의 / discussion=폭넓은 논의 / advice=받는 조언 자체"),
    ("convene", "소집하다 / 모이다", "회의나 공식 모임을 열거나 그 자리에 모이다", "정해진 자리로 사람들을 불러 모으는 느낌", "convene=공식적으로 소집하다 / gather=모이다 / assemble=한곳에 집합시키다"),
    ("coordinator", "조정자 / 진행 담당자", "사람·일정·업무 연결을 맞춰 주는 사람", "따로 움직이는 일을 한 줄로 엮는 사람", "coordinator=실무 조율자 / supervisor=감독·지도자 / organizer=행사 준비 책임자"),
    ("correspondence", "서신 교환 / 업무 연락", "이메일·편지 등으로 오가는 공식 소통", "문서로 주고받는 연락의 흐름", "correspondence=서면 연락 교환 / communication=소통 전반 / message=개별 메시지 하나"),
    ("credential", "자격 증명 / 인증", "능력·신분·학력을 보여 주는 공식 증빙", "이 사람이 조건을 갖췄다는 공식 표시", "credential=자격을 증명하는 문서·경력 / certificate=수료·자격 증서 / qualification=자격 요건 자체"),
    ("deadline", "마감 기한", "제출이나 완료를 끝내야 하는 마지막 시점", "그때를 넘기면 늦는 선", "deadline=마감 시한 / timeline=전체 일정 흐름 / due date=제출 예정 날짜"),
    ("delegate", "위임하다 / 대표로 보내다", "권한이나 일을 다른 사람에게 맡기다", "내가 다 하지 않고 역할을 넘기는 느낌", "delegate=권한·업무를 맡기다 / assign=일을 배정하다 / authorize=공식 권한을 주다"),
    ("deliberation", "숙의 / 신중한 논의", "결정을 내리기 전에 차분히 따져 보는 과정", "급히 결론 내지 않고 곱씹어 보는 논의", "deliberation=신중한 숙고·논의 / debate=찬반을 겨루는 토론 / discussion=일반적 논의"),
    ("discussant", "토론 발표자 / 지정 토론자", "발표 내용에 대해 논평과 질문을 맡은 사람", "발표를 듣고 바로 반응을 정리해 던지는 사람", "discussant=지정 논평자 / presenter=발표자 / moderator=토론 진행자"),
    ("disseminate", "널리 퍼뜨리다 / 배포하다", "연구 결과나 정보를 많은 사람에게 확산시키다", "알아야 할 내용을 넓게 퍼뜨리는 느낌", "disseminate=지식·정보를 확산하다 / distribute=자료를 나눠 주다 / spread=일반적으로 퍼지다"),
    ("draft", "초안 / 초안을 쓰다", "완성 전 단계로 먼저 써 본 문서", "나중에 고칠 걸 전제로 일단 틀을 적는 느낌", "draft=수정 전 초안 / outline=큰 구조만 잡은 개요 / manuscript=작성된 원고"),
    ("enrollment", "등록 / 수강 신청 상태", "수업·프로그램에 공식적으로 이름을 올린 상태", "명단에 들어가서 정식 참가자가 되는 것", "enrollment=등록 상태·인원 / registration=등록 절차 / attendance=실제 출석"),
    ("excerpt", "발췌문 / 일부 인용", "긴 글에서 떼어 낸 짧은 부분", "전체 중 필요한 조각만 잘라 온 느낌", "excerpt=일부 발췌문 / quotation=인용문 / summary=요약문"),
    ("extension", "연장 / 기한 추가", "시간·기간·범위를 더 늘리는 것", "끝나는 선을 뒤로 조금 늘려 주는 느낌", "extension=기한·범위 연장 / postponement=일정 자체 연기 / expansion=규모 확대"),
    ("facilitate", "원활하게 하다 / 촉진하다", "일이나 논의가 더 쉽게 진행되도록 돕다", "막힌 흐름을 부드럽게 열어 주는 느낌", "facilitate=진행을 쉽게 돕다 / promote=적극 장려하다 / assist=직접 도와주다"),
    ("faculty", "교수진 / 교직원 집단", "대학에서 가르치거나 연구하는 교원 집단", "학생이 아니라 학교 측 학문 인력", "faculty=교수진 집단 / staff=행정·지원 직원 / department=학과 조직"),
    ("feedback", "피드백 / 반응 의견", "결과나 초안에 대해 돌아오는 평가·조언", "내가 낸 것에 대해 다시 돌아오는 신호", "feedback=개선용 반응·의견 / evaluation=공식 평가 / comment=개별 의견"),
    ("fellowship", "연구 장학금 / 연구직 지원", "연구·학업 수행을 위해 주는 재정적·직위 지원", "공부·연구를 이어가게 해주는 공식 후원", "fellowship=연구 장학·지원직 / scholarship=학비 중심 장학금 / grant=프로젝트 자금 지원"),
    ("follow-up", "후속 조치 / 추가 확인", "처음 일이나 대화 뒤에 이어서 확인·보완하는 행동", "한 번 하고 끝내지 않고 뒤를 챙기는 느낌", "follow-up=후속 확인·조치 / reminder=잊지 않게 알림 / review=다시 검토"),
    ("forum", "공개 토론의 장 / 포럼", "여러 사람이 의견을 나누는 공식 공개 자리", "의견을 꺼내 놓는 열린 토론 공간", "forum=공개 논의의 장 / seminar=학술 발표·수업형 모임 / meeting=특정 안건 회의"),
    ("guideline", "지침 / 가이드라인", "어떻게 해야 하는지 알려 주는 기준선", "세부 규칙보다는 따라갈 방향을 잡아 주는 선", "guideline=따를 기준·권고 / rule=지켜야 할 규칙 / protocol=정해진 절차"),
    ("handbook", "안내서 / 편람", "필요한 규정과 절차를 모아 둔 실용적 책자", "모르는 게 생길 때 찾아보는 사용설명서 느낌", "handbook=실무 안내서 / manual=작동·절차 설명서 / brochure=홍보용 소책자"),
    ("handout", "배포 자료", "수업이나 발표 때 참가자에게 나눠 주는 자료", "듣는 사람이 손에 들고 보는 종이·파일", "handout=참가자 배포 자료 / slide=화면 발표 자료 / worksheet=연습용 활동지"),
    ("instructor", "강사 / 수업 담당자", "수업을 직접 가르치는 사람", "강의실에서 설명을 이끄는 사람", "instructor=가르치는 담당자 / professor=대학 교수 직위 / tutor=개별 지도자"),
    ("internship", "인턴십 / 실무 연수", "현장에서 경험을 쌓는 단기 실습·근무 과정", "배운 것을 실제 일터에서 시험해보는 기간", "internship=현장 실습 과정 / training=훈련 전반 / employment=정식 고용"),
    ("invitation", "초대 / 참여 요청", "행사나 발표에 와 달라는 공식·비공식 요청", "같이 와서 참여해 달라고 문을 여는 느낌", "invitation=초대 요청 / announcement=알림 발표 / offer=제안·기회 제공"),
    ("keynote", "기조연설 / 핵심 발표", "행사의 큰 방향을 여는 중심 강연", "전체 분위기와 핵심 메시지를 먼저 잡는 발표", "keynote=행사의 중심 기조연설 / lecture=일반 강의 / presentation=특정 내용을 보여주는 발표"),
    ("liaison", "연락 담당자 / 연결 역할", "두 집단 사이에서 소통과 조율을 맡는 사람", "따로 있는 쪽들을 이어 주는 다리 역할", "liaison=집단 사이 연락·연결 담당 / coordinator=업무 조정자 / representative=대표자"),
    ("logistics", "실무 준비 / 운영 세부사항", "장소·시간·장비·이동 등 실행에 필요한 조정", "아이디어보다 실제 굴러가게 만드는 뒷단 준비", "logistics=운영·준비 세부사항 / planning=계획 수립 / management=전체 관리"),
    ("manuscript", "원고", "출판이나 제출을 위해 작성한 글의 본문 초안·완성본", "논문·책으로 내기 전 손에 든 글 파일", "manuscript=제출·출판용 원고 / draft=아직 고치는 초안 / article=출판된 글"),
    ("memorandum", "공식 메모 / 업무 전달문", "조직 안에서 짧고 공식적으로 남기는 안내 문서", "말로 흘리지 않고 문서로 박아 두는 메모", "memorandum=공식 업무 메모 / note=짧은 메모 / report=더 긴 보고서"),
    ("mentor", "멘토 / 조언자", "경험을 바탕으로 성장과 판단을 도와주는 사람", "앞서 간 사람이 방향을 짚어 주는 느낌", "mentor=성장을 돕는 조언자 / supervisor=업무·연구 지도자 / advisor=공식·비공식 조언자"),
    ("milestone", "중간 이정표 / 주요 달성 단계", "긴 프로젝트 중 중요한 점검·완료 지점", "전체 길에서 여기까지 왔다고 표시하는 기준점", "milestone=중요한 단계 달성점 / deadline=마감 시점 / goal=최종 목표"),
    ("moderator", "진행자 / 사회자", "토론의 흐름과 발언 순서를 조정하는 사람", "말들이 엉키지 않게 순서를 잡아 주는 역할", "moderator=토론 진행자 / chairperson=회의 책임자 / host=행사 진행·초청자"),
    ("nomination", "지명 / 후보 추천", "공식 역할이나 상의 후보로 이름을 올리는 일", "이 사람을 후보로 세우자고 올려 보내는 느낌", "nomination=후보로 지명함 / recommendation=추천 의견 / appointment=공식 임명"),
    ("nominee", "지명된 후보자", "추천이나 공식 지명을 받은 사람", "아직 확정 전이지만 이름이 올라간 사람", "nominee=지명된 후보 / candidate=검토 대상 후보 / awardee=수상자"),
    ("orientation", "오리엔테이션 / 기본 안내", "새 과정이나 기관을 시작하기 전에 받는 소개와 안내", "처음 들어와서 지도를 펼쳐 보는 단계", "orientation=초기 적응 안내 / training=기술·업무 훈련 / introduction=일반적 소개"),
    ("outline", "개요 / 윤곽을 잡다", "전체 구조와 큰 항목을 먼저 정리한 틀", "세부를 채우기 전에 뼈대를 세우는 느낌", "outline=큰 틀의 개요 / draft=문장까지 쓴 초안 / summary=내용을 줄인 요약"),
    ("panel", "토론 패널 / 심사단", "발표·토론·심사를 맡은 여러 명의 구성원", "앞에 앉아 질문하고 평가하는 한 줄 사람들", "panel=토론·심사단 / committee=공식 의사결정 위원회 / audience=일반 청중"),
    ("participant", "참가자", "활동·연구·행사에 실제로 참여하는 사람", "가만히 듣기만이 아니라 그 일 안에 들어간 사람", "participant=활동 참가자 / attendee=자리에 온 사람 / respondent=응답자"),
    ("peer", "동료 / 또래 집단", "비슷한 지위나 수준에 있는 사람", "위아래가 아니라 같은 선상에 있는 사람", "peer=비슷한 위치의 동료 / colleague=함께 일하는 동료 / supervisor=윗선 지도자"),
    ("petition", "청원 / 요청서를 내다", "공식 결정자에게 변화를 요구하며 서명과 함께 내는 요청", "그냥 불만이 아니라 문서로 요구를 올리는 느낌", "petition=공식 청원 / request=일반 요청 / complaint=불만 제기"),
    ("plenary", "전체회의의 / 총회의", "참가자 전원이 함께 모이는 공식 세션과 관련된", "작은 분과가 아니라 모두가 한 방에 모이는 느낌", "plenary=전체회의의 / breakout=소그룹 분과의 / general=일반적인"),
    ("poster", "발표 포스터 / 게시물", "연구 내용을 한 장에 시각적으로 정리한 전시 자료", "긴 발표 대신 벽에 붙여 설명하는 연구 요약판", "poster=게시·전시 포스터 / paper=논문 글 / slide=화면 발표 자료"),
    ("prerequisite", "선수 요건 / 사전 조건", "수업이나 단계에 들어가기 전에 먼저 갖춰야 하는 조건", "이걸 먼저 해야 다음 문이 열리는 느낌", "prerequisite=먼저 필요한 조건·과목 / requirement=필수 요건 전반 / preparation=사전 준비"),
    ("preliminary", "예비의 / 사전 단계의", "최종 결론 전에 먼저 하는 초기 검토나 결과", "확정 전이라 먼저 맛보기로 보는 단계", "preliminary=예비·초기 단계의 / tentative=잠정적인 / final=최종적인"),
    ("proceedings", "학술대회 논문집 / 공식 회의 기록", "회의나 학회에서 발표된 내용을 모은 공식 기록물", "행사에서 나온 내용을 문서로 남긴 묶음", "proceedings=학회 발표·회의 기록집 / minutes=회의 요약 기록 / transcript=발언을 적은 기록문"),
    ("proposal", "제안서 / 연구 계획안", "승인이나 지원을 받기 위해 내는 계획 문서", "이렇게 하겠다고 먼저 설득하는 문서", "proposal=공식 제안서 / plan=내부 실행 계획 / suggestion=가벼운 제안"),
    ("protocol", "절차 / 공식 규약", "일을 일관되게 처리하기 위한 정해진 단계와 규칙", "아무렇게나 하지 말고 정해진 순서대로 가는 길", "protocol=공식 절차·규약 / guideline=따를 방향·권고 / policy=조직의 방침"),
    ("publicize", "홍보하다 / 널리 알리다", "행사나 결과를 많은 사람에게 알려 관심을 끌다", "모르는 사람이 없게 바깥으로 크게 띄우는 느낌", "publicize=널리 알리다 / announce=공식 발표하다 / advertise=광고하다"),
    ("questionnaire", "설문지 / 질문지", "정보를 모으기 위해 정해진 질문을 적어둔 양식", "응답을 받으려고 질문 칸을 미리 깔아 둔 종이", "questionnaire=설문 질문지 / survey=조사 전체 또는 설문 / interview=직접 묻는 면담"),
    ("quorum", "의사정족수", "회의가 공식 결정을 내리기 위해 최소한 있어야 하는 인원", "사람 수가 이만큼은 차야 회의가 성립되는 기준선", "quorum=의결 가능한 최소 인원 / majority=과반수 / attendance=출석 인원"),
    ("rapport", "친밀한 신뢰 관계", "대화나 협업이 편하게 이어질 만큼 쌓인 좋은 관계", "말이 잘 통하고 경계가 풀린 연결감", "rapport=편안한 신뢰·유대 / relationship=관계 일반 / trust=믿음"),
    ("recipient", "수령인 / 받는 사람", "장학금·이메일·상 등을 받는 사람", "무언가가 최종적으로 도착하는 사람", "recipient=공식적으로 받는 사람 / receiver=받는 사람 일반 / awardee=상을 받은 사람"),
    ("recruitment", "모집 / 선발 활동", "참가자·학생·직원을 찾아 뽑는 과정", "필요한 사람을 모으려고 끌어들이는 작업", "recruitment=사람을 모집·선발하는 과정 / selection=뽑는 판단 단계 / admission=입학·입회 허가"),
    ("referral", "추천 / 의뢰 연결", "다른 사람이나 기관으로 공식적으로 소개해 넘기는 일", "필요한 곳으로 이어 보내는 연결표", "referral=다른 곳으로 추천·의뢰 / recommendation=좋다고 추천함 / transfer=소속·위치를 옮김"),
    ("registration", "등록 / 신청 절차", "수업·행사에 이름과 정보를 공식 접수하는 과정", "참가하려고 행정 절차를 밟는 단계", "registration=등록 절차 / enrollment=등록된 상태·인원 / application=지원서 제출"),
    ("rehearsal", "리허설 / 예행연습", "발표나 공연 전에 실제처럼 맞춰 보는 연습", "실전 전에 한 번 끝까지 돌려보는 느낌", "rehearsal=실전형 예행연습 / practice=연습 일반 / demonstration=보여주기 시연"),
    ("reminder", "알림 / 상기시키는 말", "잊지 않도록 다시 알려 주는 메시지나 신호", "머릿속에서 빠지지 않게 한 번 더 톡 건드리는 느낌", "reminder=잊지 않게 상기함 / notification=시스템·공식 알림 / warning=위험 경고"),
    ("repository", "저장소 / 자료 보관처", "파일·데이터·자료를 모아 두는 보관 공간", "자료를 한곳에 쌓아 두고 찾아 쓰는 창고", "repository=자료 저장소 / database=구조화된 데이터베이스 / archive=장기 보관 기록물"),
    ("reservation", "예약", "자리·시설·장비를 미리 확보해 두는 일", "나중에 쓰려고 지금 내 몫을 잡아 두는 느낌", "reservation=자리·공간 예약 / appointment=사람과의 약속 예약 / booking=예약 행위 일반"),
    ("roster", "명단 / 근무·참가자 목록", "사람들의 이름과 배정 정보를 적은 목록", "누가 들어 있는지 줄줄이 적은 표", "roster=사람 명단·배정표 / list=목록 일반 / schedule=시간 배치표"),
    ("roundtable", "원탁 토론 / 자유 토의 모임", "위계보다 수평적 논의를 강조하는 집단 토론", "한 방향 강의가 아니라 둘러앉아 주고받는 느낌", "roundtable=수평적 집단 토론 / seminar=학술 수업·발표 모임 / lecture=일방향 강의"),
    ("rubric", "평가 기준표", "과제나 발표를 어떤 기준으로 채점할지 정리한 틀", "점수를 줄 때 어디를 볼지 칸칸이 정해 둔 표", "rubric=채점 기준표 / criterion=판단 기준 하나 / guideline=일반 지침"),
    ("scholarship", "장학금 / 학문성", "학업 비용 지원금 또는 학술적 연구 역량", "공부를 지원하는 돈이나 학문적 깊이", "scholarship=장학금·학술성 / fellowship=연구 중심 지원 / grant=특정 프로젝트 자금"),
    ("screening", "선별 심사 / 사전 점검", "지원자나 자료를 먼저 걸러 적합성을 확인하는 과정", "전부 들이지 않고 먼저 체에 거르는 단계", "screening=사전 선별·심사 / evaluation=가치·성과 평가 / review=검토"),
    ("seminar", "세미나 / 토론식 수업", "작은 규모에서 발표와 토론이 중심이 되는 학술 모임", "강의만 듣지 않고 함께 읽고 말하는 수업", "seminar=소규모 토론형 학술 모임 / lecture=강의 중심 수업 / workshop=실습 중심 모임"),
    ("spokesperson", "대변인 / 공식 발언자", "단체나 팀을 대표해 입장을 말하는 사람", "여러 사람의 입을 하나로 모아 밖에 말하는 사람", "spokesperson=공식 대변인 / representative=대표자 일반 / speaker=말하는 사람·발표자"),
    ("submission", "제출물 / 제출", "과제·신청서·논문을 내는 행위나 낸 결과물", "손에 들고 있던 문서를 마감선 안으로 넣는 느낌", "submission=제출 행위·제출물 / application=지원서 / draft=수정 전 초안"),
    ("supervisor", "지도자 / 감독자", "연구나 업무 진행을 살피고 방향을 잡아 주는 책임자", "위에서 방향과 기준을 잡아 주는 사람", "supervisor=연구·업무를 감독하는 사람 / mentor=성장 조언자 / manager=조직 운영 관리자"),
    ("symposium", "학술 심포지엄", "한 주제를 두고 여러 발표와 토론이 이어지는 공식 학술 행사", "여러 발표가 한 흐름으로 이어지는 큰 학술 자리", "symposium=공식 학술 발표 행사 / seminar=소규모 토론형 모임 / forum=공개 논의의 장"),
    ("syllabus", "강의계획서", "한 학기 수업 목표·일정·평가 기준을 정리한 문서", "수업 전체 지도를 첫날 나눠주는 종이", "syllabus=수업 전체 계획서 / curriculum=교육과정 체계 / timetable=시간표"),
    ("teamwork", "팀워크 / 협력 작업", "공동 목표를 위해 역할을 맞춰 함께 일하는 능력과 방식", "각자 따로보다 팀으로 맞물려 움직이는 힘", "teamwork=팀으로 협력하는 방식·능력 / collaboration=함께 작업하는 과정 / leadership=이끄는 역할"),
    ("timetable", "시간표 / 일정표", "언제 무엇이 진행되는지 시간 순서로 적은 표", "하루·학기 흐름을 시간 칸에 꽂아 둔 표", "timetable=시간 중심 일정표 / schedule=일정표 일반 / agenda=논의할 안건 목록"),
    ("transcript", "성적증명서 / 기록문", "성적이나 발언 내용을 공식적으로 적어 둔 문서", "말하거나 평가된 내용을 문자로 남긴 기록", "transcript=공식 성적·발언 기록문 / record=기록 일반 / certificate=증명서"),
    ("tutorial", "튜토리얼 / 소규모 지도 수업", "개별 또는 소그룹으로 개념과 과제를 지도하는 수업", "큰 강의보다 가까이 붙어서 짚어 주는 수업", "tutorial=소규모 지도 수업·안내 / lecture=대형 강의 / workshop=실습형 수업"),
    ("undergraduate", "학부생의 / 학부생", "대학원 전 단계의 학사 과정 학생이나 그 과정 관련", "아직 대학원 전, 학부 단계에 있는 느낌", "undergraduate=학부생·학부 과정의 / graduate=대학원생·졸업자의 / freshman=1학년"),
    ("venue", "장소 / 개최지", "행사나 회의가 열리는 특정 공간", "이 일이 실제로 열리는 무대가 되는 곳", "venue=행사 개최 장소 / location=위치 일반 / site=현장·부지"),
    ("waitlist", "대기자 명단", "정원 초과 후 자리가 나면 들어갈 수 있도록 이름을 올린 목록", "지금은 못 들어가지만 빈자리를 기다리는 줄", "waitlist=대기자 명단 / roster=확정된 명단 / queue=순서를 기다리는 줄"),
    ("workshop", "워크숍 / 실습형 세미나", "참가자가 직접 해보며 배우는 집중형 모임", "앉아 듣기보다 손과 말로 같이 만들어 보는 자리", "workshop=실습·참여형 모임 / seminar=토론형 학술 모임 / lecture=강의형 수업"),
    ("accreditation", "공식 인가 / 인증", "기관이나 프로그램이 기준을 충족했다고 인정받는 것", "외부 기준을 통과해 공식 도장을 받는 느낌", "accreditation=기관·과정의 공식 인가 / certification=개인·제품의 자격 인증 / approval=일반 승인"),
    ("acknowledgment", "감사의 표시 / 인정", "도움이나 기여를 공식적으로 밝혀 적는 일", "받은 도움을 그냥 넘기지 않고 이름을 적어주는 느낌", "acknowledgment=기여·도움 인정 / appreciation=감사하는 마음 / recognition=성과·가치의 인정"),
    ("advisory", "자문용의 / 권고 성격의", "결정을 직접 내리기보다 조언과 권고를 제공하는", "명령이 아니라 참고할 방향을 주는 느낌", "advisory=자문·권고 성격의 / mandatory=의무적인 / consultative=협의·자문 중심의"),
    ("archiving", "자료 보관 / 아카이브화", "나중에 찾을 수 있게 기록과 파일을 체계적으로 저장하는 일", "당장 쓰고 버리지 않고 정리해 쌓아 두는 느낌", "archiving=장기 보관용 정리 저장 / backup=복사본 저장 / filing=서류를 분류해 꽂아두기"),
    ("breakout", "소그룹 분과의 / 분임 토론", "전체 모임에서 나뉘어 하는 작은 그룹 세션", "큰 방에서 갈라져 작은 방으로 흩어지는 느낌", "breakout=소그룹 분과 세션 / plenary=전체회의 세션 / workshop=참여형 실습 모임"),
    ("caption", "그림·표 설명문 / 캡션", "이미지나 도표 아래 붙는 짧은 설명", "자료 옆에 붙어 의미를 짚어 주는 작은 문장", "caption=그림·표 설명문 / label=이름표·항목명 / title=전체 제목"),
    ("cohesion", "응집력 / 결속", "팀이나 글의 요소들이 잘 붙어 하나로 이어지는 성질", "따로따로 흩어지지 않고 안에서 잘 붙는 힘", "cohesion=안에서 잘 연결되는 응집력 / coherence=논리적으로 잘 이어지는 일관성 / unity=전체가 하나로 묶인 느낌"),
    ("conferral", "수여 / 학위·상 공식 부여", "학위나 상을 공식적으로 주는 행위", "자격이나 영예를 공식 절차로 건네는 느낌", "conferral=학위·상 수여 / awarding=상 지급 일반 / granting=허가·권리 부여"),
    ("debrief", "사후 점검하다 / 결과를 짚어보다", "활동이 끝난 뒤 무엇이 있었는지 돌아보고 정리하다", "끝난 직후 경험을 펼쳐 놓고 복기하는 느낌", "debrief=끝난 뒤 함께 점검하다 / review=검토하다 / brief=시작 전에 요약 설명하다"),
    ("endorsement", "공개 지지 / 추천 승인", "사람이나 제안을 공식적으로 좋다고 밀어주는 표현", "뒤에서 조용히가 아니라 이름 걸고 지지하는 느낌", "endorsement=공식 지지·추천 / approval=승인 / sponsorship=재정·공식 후원"),
    ("fieldwork", "현장 조사 / 현지 연구", "교실이나 사무실 밖 실제 현장에서 자료를 모으는 연구 활동", "책상 밖으로 나가 직접 보고 기록하는 느낌", "fieldwork=현장에서 하는 조사·연구 / experiment=통제된 실험 / observation=관찰 행위"),
    ("handshake", "악수 / 합의의 상징적 확인", "인사나 협력 시작을 보여 주는 상징적 몸짓", "말로만이 아니라 손을 맞잡아 관계를 여는 느낌", "handshake=인사·합의 확인의 악수 / agreement=합의 내용 / greeting=인사 일반"),
    ("inquiry", "문의 / 조사", "정보나 설명을 얻기 위해 묻거나 알아보는 일", "모르는 걸 그냥 두지 않고 캐묻고 확인하는 움직임", "inquiry=공식 문의·조사 / question=질문 하나 / investigation=더 깊은 조사"),
    ("invigilation", "시험 감독", "시험 중 규정을 지키는지 지켜보는 감독 업무", "부정행위 없이 치르는지 눈으로 지키는 역할", "invigilation=시험 감독 / supervision=일반 감독·지도 / monitoring=상황을 계속 관찰함"),
    ("itinerary", "여행·방문 일정표", "이동과 방문 순서를 시간대별로 적은 계획표", "어디서 어디로 갈지 길순서를 적어 둔 일정", "itinerary=이동·방문 중심 일정표 / timetable=시간표 / agenda=회의 안건"),
    ("onboarding", "초기 적응 안내 / 합류 절차", "새 구성원이 조직과 업무에 익숙해지도록 돕는 과정", "들어온 첫 단계에서 시스템에 태워 적응시키는 느낌", "onboarding=새 구성원 적응 절차 / orientation=초기 소개·안내 / training=업무 기술 훈련"),
    ("outreach", "대외 홍보 / 외부 연계 활동", "학교나 기관 밖의 사람들에게 다가가 연결을 만드는 활동", "안에만 머물지 않고 바깥으로 손을 뻗는 느낌", "outreach=외부 대상 연결·홍보 활동 / publicity=널리 알리는 홍보 / service=봉사·지원 활동"),
    ("plagiarism", "표절", "남의 글이나 아이디어를 출처 없이 자기 것처럼 쓰는 일", "빌려 온 생각을 출처표 없이 내 이름으로 덮는 것", "plagiarism=출처 없이 베끼는 표절 / citation=출처 표기 / paraphrase=뜻을 살려 바꿔 쓰기"),
    ("proctor", "시험 감독관", "시험장에서 규정과 진행을 관리하는 사람", "시험실 질서를 지키는 공식 감시자", "proctor=시험 감독관 / examiner=시험 평가자·출제자 / supervisor=일반 감독자"),
    ("readout", "요점 보고 / 결과 브리핑", "논의나 회의 결과를 핵심만 정리해 전달하는 설명", "무슨 얘기가 나왔는지 결론만 꺼내 읽어 주는 느낌", "readout=회의·결과 요점 보고 / summary=요약 / transcript=발언 기록문"),
    ("recap", "요약해 되짚다 / 핵심 정리", "이미 논의한 내용을 짧게 다시 정리하다", "흩어진 말을 한 번 접어서 다시 보여주는 느낌", "recap=간단히 되짚어 정리하다 / review=다시 검토하다 / repeat=그대로 반복하다"),
    ("sponsorship", "후원 / 재정 지원", "행사·연구·활동을 돈이나 공식 지원으로 뒷받침하는 일", "혼자 못 굴러가는 일을 뒤에서 밀어주는 지원", "sponsorship=후원·지원 제공 / funding=자금 지원 / endorsement=공개 지지"),
    ("whiteboard", "화이트보드 / 판서판", "회의나 수업 중 아이디어를 적고 공유하는 판", "말을 바로 적어 모두가 같이 보는 벽 위 메모장", "whiteboard=판서용 보드 / screen=화면 표시 장치 / notebook=개인 기록용 공책"),
    ("backlog", "미처리 목록 / 밀린 작업", "아직 처리하지 못해 쌓여 있는 과제나 요청", "해야 할 일이 뒤에 줄줄이 밀려 있는 느낌", "backlog=밀린 미처리 작업 묶음 / workload=현재 맡은 일의 양 / agenda=논의할 안건 목록"),
    ("checklist", "점검표 / 체크리스트", "빠뜨리지 않게 항목별로 확인하도록 만든 목록", "하나씩 표시하며 누락을 막는 목록", "checklist=확인용 항목표 / guideline=따를 지침 / inventory=보유 목록"),
    ("facilitator", "진행 촉진자 / 협의 조력자", "토론이나 협업이 매끄럽게 흘러가도록 돕는 사람", "사람들 말과 흐름이 막히지 않게 밀어주는 역할", "facilitator=논의·협업을 원활하게 돕는 사람 / moderator=발언 순서를 조정하는 진행자 / coordinator=실무 연결 담당자"),
    ("headcount", "인원수 파악 / 참석 인원", "몇 명이 있는지 세거나 확인한 수", "일단 사람 수부터 정확히 세는 느낌", "headcount=현장 인원 파악 수치 / attendance=출석 상태 / enrollment=등록 인원"),
    ("markup", "수정 표시 / 주석 달린 교정", "초안 위에 고칠 부분과 의견을 표시해 둔 것", "원문 위에 빨간펜 흔적을 얹는 느낌", "markup=문서 위 수정 표시 / annotation=설명 주석 / revision=수정된 새 버전"),
    ("photocopy", "복사본 / 복사하다", "문서나 자료를 종이로 복제한 것 또는 그렇게 만드는 일", "원본을 여러 장 찍어 나눠 가질 수 있게 만드는 느낌", "photocopy=종이 복사본·복사하다 / printout=출력물 / duplicate=복제본"),
    ("showcase", "전시 발표하다 / 선보이다", "성과나 작품을 사람들이 잘 보도록 공개적으로 보여주다", "숨겨둔 결과물을 앞에 꺼내 보여주는 느낌", "showcase=성과를 눈에 띄게 선보이다 / present=발표하다 / display=전시하다"),
    ("timeslot", "시간대 / 배정된 발표 시간", "일정표 안에서 특정 활동에 잡힌 짧은 시간 구간", "긴 일정표 안에 끼워 넣은 자기 차례의 시간칸", "timeslot=배정된 시간칸 / deadline=마감 시한 / appointment=약속된 만남"),
    ("walkthrough", "단계별 설명 / 시연 안내", "절차나 자료를 처음부터 따라가며 하나씩 설명하는 것", "처음부터 끝까지 같이 걸으며 짚어주는 느낌", "walkthrough=순서대로 따라가며 설명하는 안내 / demonstration=보여주며 시연 / tutorial=학습용 지도 설명"),
    ("workload", "업무량 / 과제 부담", "한 사람이 맡고 있는 일의 양과 부담", "등에 얹힌 할 일의 무게", "workload=맡은 일의 양 / backlog=밀린 미처리 일 / responsibility=맡은 책임"),
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


def write_set13() -> list[str]:
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
        raise RuntimeError(f"Only {len(selected)} non-duplicate cards available for set 13")

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
        manifest["files_created"].insert(12, TARGET.name)
    manifest["total_ets_cards"] = total_ets_cards
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_notes(total_ets_cards: int) -> None:
    gen_notes = ROOT / "generation_notes.md"
    text = gen_notes.read_text(encoding="utf-8")
    text = text.replace(
        "- ETS sets `01` to `12` exist, bringing the ETS-based total to 1200 cards\n",
        f"- ETS sets `01` to `13` exist, bringing the ETS-based total to {total_ets_cards} cards\n",
    )
    gen_notes.write_text(text, encoding="utf-8")

    work_plan = ROOT / "WORK_PLAN.md"
    text = work_plan.read_text(encoding="utf-8")
    text = text.replace(
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_12.tsv`\n",
        "- Existing ETS files: `toefl_ets_2026_set_01.tsv` to `toefl_ets_2026_set_13.tsv`\n",
    )
    text = text.replace(
        "- Current ETS row count after the latest expansion pass: 1200\n",
        f"- Current ETS row count after the latest expansion pass: {total_ets_cards}\n",
    )
    text = text.replace(
        "1. Rewrite existing ETS TSVs into the no-example multiline format.\n"
        "2. Re-run validation and fix any malformed cards automatically where possible.\n"
        "3. Decide the next ETS expansion ceiling from quality/coverage rather than a fixed 3000-card target.\n"
        "4. Build the AWL headword pipeline with sublist metadata retained in notes or manifest.\n",
        "1. Continue ETS expansion one set at a time with quality gates and no hard 3000-card quota.\n"
        "2. Re-run validation after each new set and repair malformed cards immediately.\n"
        "3. Do a semantic polishing pass on machine-generated AWL glosses before final study use.\n"
        "4. Periodically prune overly specialized or duplicate-prone ETS tail candidates.\n",
    )
    work_plan.write_text(text, encoding="utf-8")


def main() -> None:
    words = write_set13()
    total_ets_cards = refresh_headword_files()
    update_manifest(total_ets_cards)
    update_notes(total_ets_cards)

    print(f"generated {TARGET.name}: {len(words)} cards")
    print(f"total ETS cards: {total_ets_cards}")
    print("sample:", ", ".join(words[:10]))


if __name__ == "__main__":
    main()
