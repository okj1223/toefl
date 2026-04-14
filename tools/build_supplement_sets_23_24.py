#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = {
    "toefl_ets_2026_set_23.tsv",
    "toefl_ets_2026_set_24.tsv",
}


PRACTICAL_WORDS = [
    ("reschedule", "일정을 다시 잡다", "약속·수업·면담 시간을 다시 조정하다", "기존 시간표를 새 칸으로 옮기는 느낌", "reschedule=일정을 다시 잡다 / postpone=뒤로 미루다 / cancel=취소하다"),
    ("resend", "다시 보내다", "이메일·파일·메시지를 한 번 더 전송하다", "안 간 자료를 다시 밀어 보내는 느낌", "resend=다시 전송하다 / forward=전달하다 / submit=제출하다"),
    ("rebook", "다시 예약하다", "좌석·상담·예약을 새로 잡다", "놓친 자리를 다시 예약표에 넣는 느낌", "rebook=예약을 다시 잡다 / reserve=예약하다 / reschedule=시간을 다시 잡다"),
    ("recheck", "다시 확인하다", "정보·서류·답을 한 번 더 검토하다", "한 번 본 것을 오류 없게 다시 훑는 느낌", "recheck=재확인하다 / review=검토하다 / verify=검증하다"),
    ("reapply", "다시 지원하다", "프로그램·장학금·허가에 재신청하다", "한 번 넣었던 신청을 다시 접수하는 느낌", "reapply=다시 지원하다 / register=등록하다 / resubmit=다시 제출하다"),
    ("preregister", "사전 등록하다", "정식 시작 전에 미리 등록해 두다", "문 열리기 전에 이름을 먼저 올리는 느낌", "preregister=사전 등록하다 / enroll=등록하다 / sign up=신청하다"),
    ("shortlist", "최종 후보로 추리다", "지원자·선택지를 소수 후보로 좁히다", "긴 목록을 짧은 후보 명단으로 압축하는 느낌", "shortlist=최종 후보로 추리다 / select=선정하다 / exclude=제외하다"),
    ("signup", "신청 등록", "서비스·행사·수업 참여 신청", "참여 명단에 이름을 올리는 느낌", "signup=신청 등록 / enrollment=등록 / subscription=구독"),
    ("signoff", "최종 승인", "검토 후 공식적으로 승인하고 마무리하다", "마지막 확인 도장을 찍는 느낌", "signoff=최종 승인 / approval=승인 / confirmation=확인"),
    ("checkin", "접수 확인", "도착·출석·예약 상태를 현장에서 확인하다", "도착했다고 시스템에 찍는 느낌", "checkin=접수 확인 / registration=등록 / attendance=출석"),
    ("checkout", "대출·퇴실 처리", "빌린 자료를 처리하거나 이용을 마치고 나가다", "사용을 끝냈다고 절차를 닫는 느낌", "checkout=대출·퇴실 처리 / checkin=도착 확인 / return=반납하다"),
    ("walkin", "예약 없이 방문한 사람", "사전 예약 없이 직접 방문하는 이용자", "빈틈이 있으면 바로 들어오는 방문자 느낌", "walkin=예약 없이 방문 / appointment=예약 방문 / visitor=방문자"),
    ("dropoff", "맡기기", "서류·물건을 지정 장소에 두고 가다", "들고 온 것을 접수대에 내려놓는 느낌", "dropoff=맡기기 / pickup=찾아가기 / submit=제출하다"),
    ("pickup", "수령", "준비된 자료·물품을 찾아가다", "맡겨진 것을 다시 손에 들고 가는 느낌", "pickup=수령 / delivery=배송 / dropoff=맡기기"),
    ("handoff", "인계", "업무·자료·책임을 다음 사람에게 넘기다", "일의 바통을 다음 담당자에게 넘기는 느낌", "handoff=인계 / transfer=이관 / delegation=위임"),
    ("followup", "후속 확인", "이전 요청이나 면담 뒤에 이어서 확인하다", "한 번 말한 뒤 끊지 않고 다음 점검을 붙이는 느낌", "followup=후속 확인 / reminder=상기 알림 / response=답변"),
    ("inbox", "받은 편지함", "들어온 이메일·메시지가 모이는 곳", "도착한 메시지가 먼저 쌓이는 칸", "inbox=받은 편지함 / outbox=보낸 편지함 / archive=보관함"),
    ("outbox", "보낸 편지함", "발송했거나 발송 대기 중인 메시지함", "밖으로 나간 메시지를 모아 둔 칸", "outbox=보낸 편지함 / inbox=받은 편지함 / draft=초안"),
    ("sender", "보낸 사람", "메시지·소포·자료를 발신한 사람", "정보를 출발시킨 쪽", "sender=발신자 / recipient=수신자 / author=작성자"),
    ("salutation", "인사말", "이메일·편지 첫머리의 격식 있는 호칭 인사", "문장을 열 때 예의를 갖춰 먼저 거는 말", "salutation=첫 인사말 / greeting=인사 / signature=서명"),
    ("timeslot", "시간대", "예약·면담·발표가 배정된 특정 시간 칸", "하루 일정표에서 비워 둔 한 칸", "timeslot=예약 시간대 / timeframe=기간 틀 / deadline=마감 시한"),
    ("headsup", "미리 알림", "문제나 일정 변화를 사전에 알려 주는 짧은 경고", "나중에 놀라지 않게 먼저 고개를 들게 하는 알림", "headsup=사전 알림 / notice=공지 / warning=경고"),
    ("callback", "회신 전화", "이전 문의 뒤 다시 걸어 주는 전화", "끊긴 대화를 다시 전화로 이어 주는 느낌", "callback=회신 전화 / response=답변 / contact=연락"),
    ("voicemail", "음성 메시지", "통화가 안 될 때 남기는 녹음 메시지", "받지 못한 전화를 목소리 기록으로 남기는 느낌", "voicemail=음성 메시지 / message=메시지 일반 / recording=녹음"),
    ("overrun", "초과 진행되다", "예정 시간·예산을 넘겨 이어지다", "정해진 선을 넘어 뒤로 흘러가는 느낌", "overrun=시간·예산 초과 / exceed=넘다 / delay=지연되다"),
    ("frontdesk", "안내 데스크", "시설 입구에서 문의·접수를 처리하는 곳", "처음 들어가면 가장 먼저 들르는 안내 창구", "frontdesk=안내 데스크 / reception=접수처 / helpdesk=지원 창구"),
    ("helpdesk", "지원 창구", "기술 문제·서비스 문의를 도와주는 지원처", "막힌 문제를 들고 가서 푸는 도움 창구", "helpdesk=지원 창구 / frontdesk=안내 데스크 / hotline=전화 상담"),
    ("workstation", "작업용 자리", "컴퓨터와 장비를 갖춘 개인 작업 공간", "앉아서 바로 일할 수 있게 세팅된 자리", "workstation=작업용 자리 / workspace=작업 공간 / desktop=책상·데스크톱"),
    ("workspace", "작업 공간", "공부·협업·업무를 하는 공간이나 온라인 공간", "자료와 사람이 한데 놓여 일하는 판", "workspace=작업 공간 / workstation=개별 작업 자리 / office=사무실"),
    ("proofread", "교정하다", "오탈자·문장 오류를 제출 전 점검하다", "내기 전에 글 표면의 실수를 잡는 느낌", "proofread=오탈자 교정 / revise=내용 수정 / edit=편집하다"),
    ("reword", "바꿔 쓰다", "같은 뜻을 더 자연스럽거나 정확한 표현으로 고쳐 말하다", "뜻은 살리고 문장 옷을 갈아입히는 느낌", "reword=표현을 바꿔 쓰다 / paraphrase=의미를 풀어 다시 쓰다 / rewrite=다시 쓰다"),
    ("redraft", "초안을 다시 쓰다", "기존 초안을 바탕으로 새 버전을 다시 작성하다", "첫 원고를 갈아 새 원고로 다시 짜는 느낌", "redraft=초안을 다시 쓰다 / revise=고치다 / rewrite=전면적으로 다시 쓰다"),
    ("markup", "수정 표시", "문서에 덧붙인 교정·주석·표시", "원문 위에 빨간 수정 흔적을 남기는 느낌", "markup=수정 표시 / annotation=주석 / comment=의견"),
    ("waiver", "면제서", "요건·수수료·규정을 적용하지 않도록 승인한 문서", "원래 규칙을 이번 건만 풀어 주는 종이", "waiver=면제서 / exemption=면제 / permit=허가"),
    ("refund", "환불", "이미 낸 돈을 돌려받는 것", "나간 돈이 다시 내 계좌로 돌아오는 느낌", "refund=환불 / reimbursement=비용 상환 / discount=할인"),
    ("invoice", "청구서", "지불해야 할 금액과 항목을 적은 문서", "얼마를 내야 하는지 공식으로 적어 보낸 종이", "invoice=청구서 / receipt=영수증 / bill=요금 고지"),
    ("receipt", "영수증", "지불했음을 증명하는 문서", "돈을 냈다는 흔적을 남긴 증빙 종이", "receipt=영수증 / invoice=청구서 / proof=증빙"),
    ("deposit", "보증금", "예약·대여·입주를 위해 미리 맡겨 두는 돈", "나중 반환을 전제로 먼저 맡기는 금액", "deposit=보증금·예치금 / fee=수수료 / payment=지불"),
    ("stipend", "정액 지원금", "연구·연수·인턴 활동에 주는 정기 생활비성 지원금", "급여라기보다 정해진 활동비를 받는 느낌", "stipend=정액 지원금 / salary=급여 / grant=지원금"),
    ("reimbursement", "비용 상환", "먼저 쓴 비용을 증빙 후 돌려받는 것", "내가 먼저 낸 돈을 나중에 메워 받는 느낌", "reimbursement=비용 상환 / refund=환불 / compensation=보상"),
    ("referee", "추천인", "지원자를 평가하거나 추천서를 써 주는 사람", "지원서 뒤에서 신뢰를 보태는 평가자", "referee=추천인·심판 / recommender=추천인 / evaluator=평가자"),
    ("recommender", "추천인", "추천서를 써 주거나 지원자를 추천하는 사람", "내 역량을 대신 보증해 주는 사람", "recommender=추천인 / referee=추천인·평가자 / sponsor=후원자"),
    ("filename", "파일명", "파일을 구분하기 위해 붙인 이름", "자료를 찾게 해 주는 저장 이름표", "filename=파일명 / title=제목 / label=라벨"),
    ("folder", "폴더", "파일을 묶어 정리하는 저장 공간", "흩어진 자료를 한 칸에 모아 넣는 느낌", "folder=폴더 / directory=디렉터리 / file=파일"),
    ("sync", "동기화하다", "기기나 저장소의 최신 상태를 서로 맞추다", "서로 다른 파일 상태를 같은 쪽으로 맞춰 세우는 느낌", "sync=동기화하다 / update=갱신하다 / backup=백업하다"),
    ("backup", "백업", "원본 손실에 대비해 따로 저장해 둔 복사본", "혹시 망가져도 다시 꺼낼 여분을 남기는 느낌", "backup=예비 복사본 / archive=보관본 / copy=복사본"),
    ("login", "로그인", "계정 정보를 넣고 시스템에 접속하다", "닫힌 시스템 안으로 내 계정으로 들어가는 느낌", "login=로그인 / sign-in=로그인 / access=접속"),
    ("logout", "로그아웃", "사용을 마치고 계정 접속을 종료하다", "열어 둔 세션 문을 닫고 나오는 느낌", "logout=로그아웃 / disconnect=연결 해제 / exit=나가기"),
    ("username", "사용자 이름", "계정을 식별하는 로그인 이름", "시스템이 나를 알아보는 계정 이름표", "username=사용자 이름 / ID=식별자 / account=계정"),
    ("passcode", "비밀번호 코드", "접속이나 인증에 쓰는 숫자·문자 코드", "잠긴 문을 여는 짧은 인증 열쇠", "passcode=인증 코드 / password=비밀번호 / PIN=숫자 비밀번호"),
    ("barcode", "바코드", "스캔으로 정보를 읽는 막대형 코드", "찍으면 숨은 식별 정보가 열리는 코드", "barcode=바코드 / QR code=QR 코드 / label=표시"),
    ("timesheet", "근무시간 기록표", "일한 시간과 날짜를 적는 기록표", "내가 언제 얼마나 일했는지 남기는 표", "timesheet=근무시간 기록표 / schedule=일정표 / attendance=출석 기록"),
    ("queue", "대기열", "차례를 기다리는 줄이나 처리 순서", "먼저 온 순서대로 앞으로 밀리는 줄", "queue=대기열 / line=줄 / roster=명단"),
    ("waittime", "대기 시간", "차례나 응답을 기다리는 데 걸리는 시간", "시작 전 줄에서 흘러가는 기다림의 길이", "waittime=대기 시간 / delay=지연 / duration=지속 시간"),
    ("locker", "보관함", "개인 물건을 잠가 두는 작은 수납장", "잠깐 넣어 두고 나중에 찾는 개인 칸", "locker=보관함 / cabinet=수납장 / storage=보관 공간"),
    ("keycard", "출입 카드", "문을 열거나 신원을 확인하는 카드", "찍으면 출입 권한이 열리는 카드 열쇠", "keycard=출입 카드 / pass=출입증 / ID card=신분증"),
    ("shuttle", "셔틀", "정해진 구간을 반복 운행하는 이동편", "캠퍼스와 역 사이를 왔다 갔다 잇는 교통편", "shuttle=순환 셔틀 / bus=버스 / transport=교통"),
    ("buspass", "버스 정기권", "버스를 반복 이용할 수 있는 승차권", "매번 표를 끊지 않게 해 주는 탑승권", "buspass=버스 정기권 / ticket=승차권 / card=카드"),
    ("classmate", "반 친구", "같은 수업을 듣는 학생", "같은 강의실 명단에 함께 있는 사람", "classmate=같은 수업 학생 / teammate=같은 팀원 / peer=또래"),
    ("teammate", "팀원", "같은 팀에서 과제나 프로젝트를 함께하는 사람", "같은 목표를 놓고 역할을 나눈 동료", "teammate=팀원 / classmate=수업 동료 / colleague=직장 동료"),
    ("roommate", "룸메이트", "같은 방이나 숙소를 함께 쓰는 사람", "한 생활공간을 나눠 쓰는 동거 학우", "roommate=룸메이트 / housemate=같은 집 동거인 / classmate=수업 동료"),
    ("registrar", "학사 행정 담당 부서", "등록·성적·학적을 처리하는 대학 행정 부서나 담당자", "수업과 학적 기록을 공식 관리하는 창구", "registrar=학사 행정 부서 / advisor=지도교수·상담자 / office=사무실"),
    ("doublecheck", "재확인하다", "실수를 막으려고 한 번 더 점검하다", "닫기 전에 마지막으로 다시 찍어 보는 느낌", "doublecheck=재확인하다 / verify=검증하다 / skim=대충 훑다"),
    ("crosscheck", "교차 확인하다", "다른 자료와 대조해 정확성을 확인하다", "한 자료만 믿지 않고 옆 자료와 맞춰 보는 느낌", "crosscheck=교차 확인하다 / compare=비교하다 / verify=검증하다"),
    ("quickstart", "빠른 시작 안내", "처음 사용자가 바로 시작하게 돕는 짧은 안내", "긴 설명서 전에 바로 쓰게 해 주는 첫 단추", "quickstart=빠른 시작 안내 / tutorial=사용 설명 / manual=설명서"),
    ("slot", "시간·자리 한 칸", "일정표나 배정표에서 비워 둔 하나의 칸", "전체 표 안에서 내가 들어갈 빈 자리", "slot=배정 칸 / opening=빈 자리 / timeslot=시간대"),
    ("headcount", "인원수", "참여자나 참석자를 세어 낸 수", "방 안에 몇 명 있는지 머릿수를 세는 느낌", "headcount=인원수 / attendance=출석 / population=인구"),
    ("turnout", "참석률", "행사·투표·모임에 실제로 나온 사람 수나 비율", "부른 사람 중 실제로 얼마나 나왔는지 보는 느낌", "turnout=실제 참석 규모 / attendance=출석 상태 / participation=참여"),
    ("retake", "재응시하다", "시험이나 평가를 다시 보다", "한 번 본 시험을 다시 치러 점수를 바꾸는 느낌", "retake=시험을 다시 보다 / repeat=반복하다 / revise=고치다"),
    ("regrade", "재채점하다", "채점 결과를 다시 검토해 점수를 조정하다", "이미 매긴 점수를 다시 열어 확인하는 느낌", "regrade=재채점하다 / reassess=다시 평가하다 / appeal=이의 제기하다"),
    ("appeal", "이의를 제기하다", "결정·평가 결과를 다시 봐 달라고 공식 요청하다", "나온 판정에 한 번 더 심사를 요구하는 느낌", "appeal=이의 제기하다 / request=요청하다 / complain=불만을 말하다"),
    ("reopen", "다시 열다", "닫힌 신청·사건·파일을 다시 열어 처리하다", "끝난 줄 알던 창을 다시 여는 느낌", "reopen=다시 열다 / resume=재개하다 / unlock=잠금을 풀다"),
    ("resubmit", "다시 제출하다", "수정한 문서나 신청서를 다시 내다", "돌아온 과제를 고쳐 다시 올리는 느낌", "resubmit=다시 제출하다 / submit=제출하다 / reapply=다시 신청하다"),
    ("overwrite", "덮어쓰다", "기존 파일·내용을 새 내용으로 바꿔 저장하다", "옛 내용을 밀어내고 새 버전을 위에 씌우는 느낌", "overwrite=덮어쓰다 / replace=대체하다 / append=덧붙이다"),
    ("autosave", "자동 저장", "작업 중 변경사항을 시스템이 자동으로 저장하는 기능", "내가 누르지 않아도 중간중간 저장되는 안전망", "autosave=자동 저장 / backup=예비 저장 / save=저장하다"),
    ("walkthrough", "단계별 안내", "절차를 따라가며 보여 주는 설명", "처음부터 끝까지 옆에서 같이 걸어 주는 안내", "walkthrough=단계별 안내 / tutorial=사용법 설명 / overview=개요"),
    ("setup", "설정", "시작 전에 장비·계정·환경을 맞춰 두는 작업", "쓰려면 먼저 깔고 맞춰야 하는 준비 단계", "setup=초기 설정 / installation=설치 / configuration=구성 설정"),
    ("wordcount", "단어 수", "글에 들어간 단어의 총수", "길이를 단어 개수로 재는 눈금", "wordcount=단어 수 / length=길이 / limit=제한치"),
    ("spellcheck", "맞춤법 검사", "철자 오류를 자동·수동으로 확인하다", "글자 하나하나 틀린 철자를 잡아내는 느낌", "spellcheck=철자 검사 / proofread=교정하다 / grammarcheck=문법 검사"),
    ("grammarcheck", "문법 검사", "문법 오류와 문장 구조 문제를 점검하다", "문장 뼈대가 맞는지 규칙으로 확인하는 느낌", "grammarcheck=문법 검사 / spellcheck=철자 검사 / edit=편집하다"),
    ("handout", "배포 자료", "수업·회의 때 나눠 주는 참고 자료", "말만 듣지 않게 손에 쥐여 주는 종이 자료", "handout=배포 자료 / worksheet=학습지 / brochure=안내 책자"),
    ("printout", "인쇄물", "화면 파일을 종이로 출력한 것", "디지털 자료를 종이 한 장으로 뽑아 놓은 결과", "printout=인쇄물 / copy=복사본 / handout=배포 자료"),
    ("scan", "스캔하다", "문서·코드를 기계로 읽어 디지털 정보로 바꾸다", "종이나 코드를 빛으로 훑어 파일로 옮기는 느낌", "scan=스캔하다 / copy=복사하다 / inspect=점검하다"),
    ("scanner", "스캐너", "문서나 코드를 읽어 디지털화하는 장치", "종이를 파일로 바꿔 읽어 들이는 기계", "scanner=스캐너 / printer=프린터 / copier=복사기"),
    ("photocopy", "복사하다", "문서를 같은 내용의 종이 사본으로 복제하다", "원본 한 장을 똑같은 종이로 다시 찍는 느낌", "photocopy=복사하다 / scan=스캔하다 / print=인쇄하다"),
    ("slides", "발표 슬라이드", "발표나 수업용으로 넘겨 보는 화면 자료", "말의 흐름을 화면 칸칸이 보여 주는 자료", "slides=발표 슬라이드 / handout=배포 자료 / outline=개요"),
    ("projector", "프로젝터", "화면이나 슬라이드를 벽·스크린에 크게 비추는 장치", "작은 화면을 앞쪽 큰 스크린으로 쏘는 기계", "projector=프로젝터 / display=화면 표시 / screen=스크린"),
    ("soundcheck", "음향 점검", "발표·녹화 전에 마이크와 소리 상태를 확인하다", "말하기 전에 소리가 잘 나오는지 먼저 찍어 보는 느낌", "soundcheck=음향 점검 / rehearsal=리허설 / test=시험·점검"),
    ("turnaround", "처리 소요 시간", "요청을 받은 뒤 결과를 돌려주기까지 걸리는 시간", "맡긴 일이 한 바퀴 돌아 다시 돌아오는 속도", "turnaround=처리 소요 시간 / deadline=마감 시한 / duration=지속 시간"),
    ("leadtime", "사전 소요 기간", "준비·주문·승인에 미리 필요한 시간", "원하는 날보다 앞에서 확보해야 하는 준비 여유", "leadtime=사전 소요 기간 / timeframe=기간 틀 / delay=지연"),
    ("timeframe", "기간 틀", "일이 진행되거나 끝나야 하는 전체 시간 범위", "언제부터 언제까지라는 시간 울타리", "timeframe=기간 범위 / deadline=마감 시점 / schedule=일정표"),
    ("sincerely", "진심으로", "공손한 이메일 마무리에서 쓰는 진정성 있는 어조", "형식만이 아니라 성의 있게 끝맺는 느낌", "sincerely=진심으로 / respectfully=정중히 / casually=편하게"),
    ("courteous", "정중한", "상대에게 예의를 갖추고 배려하는 태도의", "요청을 해도 무례하지 않게 말끝을 다듬는 느낌", "courteous=정중한 / polite=공손한 / friendly=친근한"),
    ("respectfully", "정중하게", "상대의 위치와 상황을 존중하는 어조로", "강하게 밀어붙이지 않고 예의를 세워 말하는 느낌", "respectfully=정중하게 / sincerely=진심으로 / formally=격식 있게"),
    ("confirm", "확인하다", "예약·내용·일정을 맞다고 다시 확정하다", "헷갈리는 정보를 마지막으로 맞다고 잠그는 느낌", "confirm=확정 확인하다 / verify=증거로 검증하다 / approve=승인하다"),
    ("request", "요청하다", "필요한 도움·정보·변경을 정중히 부탁하다", "내가 필요한 것을 공식적으로 말해 달라는 느낌", "request=정중히 요청하다 / demand=강하게 요구하다 / ask=묻거나 부탁하다"),
    ("availability", "가능 시간·이용 가능성", "언제 이용 가능하거나 시간이 되는지의 상태", "비어 있어 쓸 수 있는지 보는 느낌", "availability=가능 여부·가능 시간 / accessibility=접근 가능성 / vacancy=빈자리"),
    ("advisor", "지도교수·상담자", "학업·진로·행정 선택을 조언하는 사람", "혼자 결정하기 전에 길을 같이 봐주는 안내자", "advisor=조언자·지도교수 / supervisor=감독자 / mentor=멘토"),
    ("troubleshooting", "문제 해결 점검", "오작동이나 오류 원인을 찾아 고치는 과정", "안 되는 지점을 하나씩 짚어 고치는 느낌", "troubleshooting=오류 원인 해결 / repair=수리 / diagnosis=진단"),
    ("campus", "캠퍼스", "대학 시설과 활동이 모여 있는 학교 구역", "수업·행정·생활이 한데 모이는 학교 공간", "campus=대학 구역 / facility=시설 / site=장소"),
    ("service", "서비스", "이용자를 지원하는 제도·업무·기능", "필요한 일을 대신 처리해 주는 지원 기능", "service=지원 서비스 / assistance=도움 / facility=시설"),
    ("interview", "면접", "질문과 답변을 통해 적합성과 경험을 평가하는 대화", "나를 설명하고 평가받는 공식 대화 자리", "interview=면접·면담 / conversation=대화 일반 / survey=설문"),
    ("email", "이메일", "전자 우편으로 보내는 업무·학업 메시지", "빠르게 기록을 남기며 주고받는 공식 메시지", "email=이메일 / message=메시지 일반 / letter=편지"),
    ("reconfirm", "재확인하다", "이미 정한 일정이나 내용을 한 번 더 확인하다", "한 번 잠근 약속을 다시 한 번 점검하는 느낌", "reconfirm=재확인하다 / confirm=확인하다 / recheck=다시 점검하다"),
    ("resubmit", "다시 제출하다", "수정한 문서나 신청서를 다시 내다", "돌아온 과제를 고쳐 다시 올리는 느낌", "resubmit=다시 제출하다 / submit=제출하다 / reapply=다시 신청하다"),
    ("reupload", "다시 업로드하다", "파일을 수정하거나 오류 후 다시 올리다", "빠진 파일을 다시 서버에 올려 놓는 느낌", "reupload=다시 업로드하다 / upload=업로드하다 / resend=다시 보내다"),
    ("rescan", "다시 스캔하다", "품질 문제나 누락 때문에 문서를 다시 스캔하다", "흐린 이미지가 나와 한 번 더 읽어 들이는 느낌", "rescan=다시 스캔하다 / scan=스캔하다 / photocopy=복사하다"),
    ("copier", "복사기", "문서를 종이 사본으로 찍어 내는 기계", "원본 종이를 여러 장으로 다시 찍는 장치", "copier=복사기 / scanner=스캐너 / printer=프린터"),
    ("printer", "프린터", "디지털 문서를 종이로 출력하는 장치", "화면 속 문서를 종이로 뽑는 기계", "printer=프린터 / copier=복사기 / projector=프로젝터"),
    ("lanyard", "목걸이형 출입줄", "ID 카드나 출입카드를 목에 거는 줄", "카드를 잃지 않게 몸에 걸어 두는 끈", "lanyard=목걸이형 카드 줄 / badge=신분 표지 / keycard=출입 카드"),
    ("badge", "신분 배지", "이름·소속·출입 권한을 보여 주는 표지", "누구인지 바로 보이게 다는 작은 신분표", "badge=신분 배지 / ID=신분증 / label=표지"),
    ("commute", "통학·통근하다", "집과 학교·직장을 정기적으로 오가다", "매일 같은 길을 왕복하는 이동 루틴", "commute=정기 통학·통근하다 / travel=여행·이동하다 / relocate=거주지를 옮기다"),
]


QUANT_WORDS = [
    ("approximation", "근사치", "정확한 값에 가깝게 어림한 값이나 계산", "완전한 정답은 아니어도 가까운 값으로 붙는 느낌", "approximation=근사치 / estimate=추정치 / exact value=정확한 값"),
    ("variability", "변동성", "값이나 결과가 일정하지 않고 퍼지는 정도", "데이터가 한 점에 모이지 않고 흔들리며 흩어지는 느낌", "variability=변동성 / variance=분산 / stability=안정성"),
    ("scatter", "흩어지다", "값이나 점이 한곳에 모이지 않고 퍼지다", "점들이 중앙에서 사방으로 퍼져 있는 느낌", "scatter=흩어지다 / cluster=모이다 / spread=퍼지다"),
    ("cluster", "군집", "서로 가까운 값이나 항목이 뭉쳐 있는 집합", "비슷한 점들이 한 덩어리로 모이는 느낌", "cluster=군집 / group=집단 일반 / category=범주"),
    ("outlier", "이상치", "전체 패턴에서 멀리 벗어난 데이터 값", "무리에서 혼자 멀리 튀어나간 점", "outlier=이상치 / anomaly=이례 현상 / exception=예외"),
    ("baseline", "기준선", "비교를 위해 먼저 잡아 둔 출발 기준값", "변화를 읽기 전에 바닥에 깔아 둔 기준선", "baseline=기준선 / benchmark=비교 기준 / average=평균"),
    ("projection", "예측치", "현재 추세나 자료로 앞으로를 계산해 낸 값", "지금 선을 미래 쪽으로 길게 뻗어 보는 느낌", "projection=예측치 / forecast=예보 / estimate=추정"),
    ("forecast", "예측하다", "자료와 추세를 바탕으로 미래 값을 내다보다", "현재 흐름을 보고 다음 구간을 미리 그리는 느낌", "forecast=미래를 예측하다 / predict=예측하다 / estimate=어림하다"),
    ("interval", "구간", "두 값이나 두 시점 사이의 범위", "시작점과 끝점 사이를 한 칸으로 보는 느낌", "interval=구간 / range=범위 / gap=차이"),
    ("margin", "오차 범위", "측정·판단에서 허용되는 차이의 폭", "딱 한 점이 아니라 좌우로 둔 여유 폭", "margin=오차·여백 범위 / threshold=기준선 / limit=한계"),
    ("ratio", "비율", "두 수를 나누어 비교한 값", "하나가 다른 하나에 대해 몇 배인지 보는 눈금", "ratio=비율 / proportion=전체 중 비중 / rate=단위당 변화"),
    ("proportion", "비중", "전체 안에서 한 부분이 차지하는 몫", "큰 원 안에서 한 조각이 얼마나 되는지 보는 느낌", "proportion=전체 중 비중 / ratio=두 수의 비 / fraction=분수"),
    ("percentage", "백분율", "전체를 100으로 놓고 나타낸 비율", "몇 퍼센트인지 100칸 눈금으로 읽는 느낌", "percentage=백분율 / proportion=비중 / percent point=퍼센트포인트"),
    ("median", "중앙값", "크기순으로 정렬했을 때 가운데 놓인 값", "줄 세운 숫자들 한가운데를 찍는 느낌", "median=중앙값 / mean=평균 / mode=최빈값"),
    ("mean", "평균값", "전체 합을 개수로 나눈 대표값", "데이터 무게중심을 한 점으로 잡는 느낌", "mean=평균값 / median=중앙값 / average=평균 일반"),
    ("dispersion", "산포", "값들이 중심에서 얼마나 흩어져 있는지의 정도", "데이터가 넓게 퍼졌는지 좁게 모였는지 보는 느낌", "dispersion=산포 / concentration=집중 / distribution=분포"),
    ("skew", "한쪽으로 치우치다", "분포나 해석이 한 방향으로 기울다", "그래프 꼬리가 한쪽으로 길게 늘어지는 느낌", "skew=한쪽으로 치우치다 / bias=편향 / tilt=기울다"),
    ("deviation", "편차", "기준값이나 평균에서 얼마나 벗어났는지의 차이", "중심선에서 얼마나 옆으로 떨어졌는지 보는 느낌", "deviation=편차 / error=오차 / difference=차이"),
    ("slope", "기울기", "그래프나 변화선이 얼마나 가파르게 오르내리는지", "선이 위아래로 얼마나 비스듬한지 보는 느낌", "slope=기울기 / incline=경사 / trend=추세"),
    ("plateau", "정체 구간", "증가나 감소가 멈추고 거의 평평해진 상태", "오르던 선이 꼭대기에서 납작해지는 느낌", "plateau=정체 구간 / peak=정점 / stagnation=침체"),
    ("uptrend", "상승 추세", "시간이 갈수록 전반적으로 올라가는 흐름", "그래프가 대체로 위로 방향을 잡는 느낌", "uptrend=상승 추세 / increase=증가 / surge=급등"),
    ("downtrend", "하락 추세", "시간이 갈수록 전반적으로 내려가는 흐름", "그래프가 대체로 아래로 향하는 느낌", "downtrend=하락 추세 / decline=감소 / drop=하락"),
    ("spike", "급등", "짧은 시간에 값이 뾰족하게 크게 뛰다", "그래프에 갑자기 솟은 뾰족한 봉우리", "spike=급등 / surge=급증 / fluctuation=변동"),
    ("dip", "일시적 하락", "잠깐 아래로 내려갔다가 다시 움직이는 하락", "선이 짧게 꺼졌다가 다시 이어지는 느낌", "dip=일시적 하락 / decline=지속적 감소 / trough=저점"),
    ("surge", "급증", "수치나 양이 갑자기 크게 늘다", "눌려 있던 값이 한 번에 위로 치솟는 느낌", "surge=급증 / rise=상승 / spike=짧은 급등"),
    ("decline", "감소하다", "수치·비중·성과가 아래로 내려가다", "높던 선이 점점 아래로 기울어지는 느낌", "decline=감소하다 / drop=뚝 떨어지다 / deteriorate=악화되다"),
    ("trendline", "추세선", "여러 점의 전체 방향을 요약해 그은 선", "흩어진 점들 위에 큰 방향선을 얹는 느낌", "trendline=추세선 / curve=곡선 / baseline=기준선"),
    ("timepoint", "측정 시점", "데이터를 기록한 특정 시간 지점", "긴 시간축 위에 콕 찍은 관찰 시점", "timepoint=측정 시점 / interval=구간 / deadline=마감 시점"),
    ("increment", "증가분", "단계적으로 늘어난 작은 변화량", "한 칸씩 더해지는 작은 상승 단위", "increment=증가분 / increase=증가 / step=단계"),
    ("decrement", "감소분", "단계적으로 줄어든 작은 변화량", "한 칸씩 덜어지는 작은 감소 단위", "decrement=감소분 / decrease=감소 / reduction=축소"),
    ("magnitude", "규모", "변화·효과·차이가 얼마나 큰지의 크기", "방향보다 얼마나 센지 재는 크기 눈금", "magnitude=규모·크기 / extent=범위 / intensity=강도"),
    ("amplitude", "진폭", "값이 기준선에서 위아래로 흔들리는 최대 폭", "중심선에서 가장 멀리 흔들리는 높이", "amplitude=진폭 / frequency=빈도 / magnitude=크기"),
    ("frequency", "빈도", "일정 기간에 어떤 일이 얼마나 자주 일어나는지", "같은 사건이 몇 번 반복되는지 세는 느낌", "frequency=빈도 / rate=비율·속도 / incidence=발생률"),
    ("cohort", "집단", "같은 조건이나 기간으로 묶어 추적한 대상 집단", "비슷한 출발선을 가진 사람들을 한 묶음으로 보는 느낌", "cohort=추적 집단 / sample=표본 / population=모집단"),
    ("subset", "부분집합", "전체 데이터에서 특정 기준으로 떼어 낸 일부", "큰 집합 안에서 조건 맞는 조각만 따로 꺼내는 느낌", "subset=부분집합 / sample=표본 / category=범주"),
    ("dataset", "데이터셋", "분석에 쓰도록 묶어 둔 자료 집합", "낱값들을 한 분석 상자로 담아 놓은 묶음", "dataset=데이터셋 / sample=표본 / archive=보관 자료"),
    ("datapoint", "데이터 점", "각 관측값 하나하나를 이루는 개별 값", "그래프 위에 찍히는 한 점짜리 관측치", "datapoint=개별 관측값 / record=기록 / metric=지표"),
    ("metric", "측정 지표", "성과나 상태를 판단하는 수치 기준", "무엇이 좋아졌는지 숫자로 재는 잣대", "metric=측정 지표 / criterion=판단 기준 / index=지수"),
    ("indicator", "지표", "어떤 상태나 변화를 간접적으로 보여 주는 신호", "보이지 않는 상태를 대신 알려 주는 숫자 신호", "indicator=지표 / signal=신호 / metric=측정 지표"),
    ("denominator", "분모", "비율 계산에서 기준이 되는 아래쪽 값", "얼마 중에서 보느냐를 정하는 바닥 수", "denominator=분모 / numerator=분자 / base=기준값"),
    ("numerator", "분자", "비율 계산에서 세고 싶은 위쪽 값", "전체 중 실제로 관심 있는 몫을 올려 적는 수", "numerator=분자 / denominator=분모 / count=개수"),
    ("rounding", "반올림", "값을 정해진 자릿수에 맞춰 단순화하다", "긴 숫자의 꼬리를 잘라 가까운 칸으로 맞추는 느낌", "rounding=반올림 / approximation=근사 / truncation=절삭"),
    ("underestimate", "과소평가하다", "실제보다 작거나 덜 중요하다고 판단하다", "진짜 크기를 아래쪽으로 작게 잡는 느낌", "underestimate=과소평가하다 / overestimate=과대평가하다 / estimate=추정하다"),
    ("overestimate", "과대평가하다", "실제보다 크거나 더 중요하다고 판단하다", "진짜보다 위쪽으로 크게 잡아 보는 느낌", "overestimate=과대평가하다 / underestimate=과소평가하다 / exaggerate=과장하다"),
    ("plausibility", "그럴듯함", "설명이 자료와 상식에 비추어 성립할 만한 정도", "완전히 증명 전이라도 말이 되는지 가늠하는 느낌", "plausibility=그럴듯함 / validity=타당성 / certainty=확실성"),
    ("uncertainty", "불확실성", "결과나 수치가 확정되지 않은 정도", "값 주변에 안개가 남아 딱 하나로 못 박히지 않는 느낌", "uncertainty=불확실성 / ambiguity=의미 모호성 / risk=위험"),
    ("robustness", "견고성", "조건이 조금 바뀌어도 결과가 유지되는 정도", "살짝 흔들어도 결론이 쉽게 무너지지 않는 힘", "robustness=견고성 / reliability=신뢰성 / stability=안정성"),
    ("sensitivity", "민감도", "입력이나 조건 변화에 결과가 얼마나 반응하는지", "조금 바꿨을 때 결과가 얼마나 예민하게 움직이는지 보는 느낌", "sensitivity=민감도 / susceptibility=취약성 / responsiveness=반응성"),
    ("specificity", "특이성", "원하지 않는 대상을 덜 섞고 정확히 구분하는 정도", "아무거나 잡지 않고 목표만 좁혀 찍는 느낌", "specificity=특이성·정확한 구분성 / precision=정밀도 / generality=일반성"),
    ("granularity", "세분성", "자료나 분류를 얼마나 잘게 나눠 보는지의 정도", "큰 덩어리를 더 촘촘한 칸으로 쪼개 보는 느낌", "granularity=세분성 / detail=세부 정도 / resolution=해상도"),
    ("normalization", "정규화", "서로 다른 값을 비교 가능하게 같은 기준으로 맞추다", "단위와 크기를 같은 눈금판 위에 올리는 느낌", "normalization=정규화 / standardization=표준화 / adjustment=조정"),
    ("weighting", "가중치 부여", "항목별 중요도를 다르게 반영하다", "모든 값을 똑같이 보지 않고 더 무거운 점수를 얹는 느낌", "weighting=가중치 부여 / prioritization=우선순위화 / averaging=평균화"),
    ("benchmarking", "기준 비교", "외부 기준이나 우수 사례와 비교해 수준을 평가하다", "내 값만 보지 않고 기준선 옆에 나란히 세우는 느낌", "benchmarking=기준 비교 / evaluation=평가 / ranking=순위 매기기"),
    ("extrapolate", "외삽하다", "관측된 범위 밖의 값을 기존 추세로 미뤄 추정하다", "이미 본 선을 보지 못한 바깥 구간으로 더 뻗는 느낌", "extrapolate=범위 밖으로 추정하다 / interpolate=사이값을 추정하다 / predict=예측하다"),
    ("interpolate", "보간하다", "이미 아는 두 값 사이의 중간값을 추정하다", "두 점 사이 빈칸을 선으로 메워 읽는 느낌", "interpolate=사이값을 추정하다 / extrapolate=범위 밖을 추정하다 / estimate=어림하다"),
    ("aggregate", "합산하다", "여러 값을 하나로 묶어 총합이나 집계값을 만들다", "흩어진 숫자를 한 바구니에 모아 큰 값을 만드는 느낌", "aggregate=합산하다 / compile=모아 정리하다 / average=평균 내다"),
    ("disaggregate", "세분해 나누다", "집계된 전체를 하위 항목으로 다시 나누어 보다", "한 덩어리 합계를 다시 조각별로 풀어 보는 느낌", "disaggregate=세분해 나누다 / segment=구분하다 / classify=분류하다"),
    ("tabulate", "표로 정리하다", "값이나 결과를 행과 열 형태로 정돈하다", "흩어진 수치를 표 칸에 차례대로 넣는 느낌", "tabulate=표로 정리하다 / summarize=요약하다 / list=나열하다"),
    ("summarize", "요약하다", "핵심 추세나 결과만 간단히 정리하다", "세부를 다 들지 않고 큰 결론만 압축하는 느낌", "summarize=요약하다 / describe=설명하다 / conclude=결론짓다"),
    ("quantify", "수량화하다", "크기나 정도를 숫자로 나타내다", "막연한 차이를 숫자 눈금 위에 올리는 느낌", "quantify=수량화하다 / measure=측정하다 / evaluate=평가하다"),
    ("calibrate", "보정하다", "측정값이 기준에 맞도록 장비나 척도를 조정하다", "틀어진 눈금을 표준선에 다시 맞추는 느낌", "calibrate=계측 보정하다 / adjust=조정하다 / correct=교정하다"),
    ("simulate", "모의 실험하다", "실제 상황을 모델로 재현해 결과를 살펴보다", "현실을 축소 모델로 돌려 미리 보는 느낌", "simulate=모의 실험하다 / imitate=흉내 내다 / predict=예측하다"),
    ("trace", "추적하다", "변화나 원인의 흐름을 단계별로 따라가다", "결과에서 출발해 경로를 선처럼 되짚는 느낌", "trace=흐름을 추적하다 / monitor=지켜보다 / infer=추론하다"),
    ("compare", "비교하다", "두 값이나 집단의 차이와 공통점을 대조하다", "나란히 놓고 어디가 같고 다른지 보는 느낌", "compare=비교하다 / contrast=차이를 대비하다 / evaluate=평가하다"),
    ("rank", "순위를 매기다", "값이나 항목을 높고 낮음 순서로 배열하다", "여러 대상을 성과 순서대로 줄 세우는 느낌", "rank=순위를 매기다 / rate=점수를 주다 / sort=정렬하다"),
    ("classify", "분류하다", "공통 기준에 따라 항목을 범주로 나누다", "섞인 항목에 라벨을 붙여 칸을 나누는 느낌", "classify=분류하다 / categorize=범주화하다 / rank=순위화하다"),
    ("stratification", "층화", "집단을 기준별 하위층으로 나누어 분석하는 것", "전체를 한 번에 보지 않고 층층이 갈라 보는 느낌", "stratification=층화 / segmentation=세분화 / classification=분류"),
    ("segmentation", "세분화", "큰 집단이나 시장을 더 작은 하위 집단으로 나누다", "한 덩어리를 의미 있는 조각들로 다시 자르는 느낌", "segmentation=세분화 / stratification=층화 / categorization=분류"),
    ("association", "연관성", "두 변수나 현상이 함께 나타나는 관계", "하나가 움직일 때 다른 하나도 같이 이어지는 느낌", "association=연관성 / correlation=상관관계 / causation=인과"),
    ("causation", "인과관계", "한 요인이 다른 결과를 실제로 일으키는 관계", "같이 나타나는 정도가 아니라 한쪽이 다른 쪽을 밀어내는 느낌", "causation=인과관계 / correlation=상관관계 / association=연관성"),
    ("confounding", "교란", "숨은 제3 요인이 변수 관계 해석을 흐리게 하는 것", "겉으로 보이는 연결 사이에 다른 원인이 끼어드는 느낌", "confounding=교란 / bias=편향 / error=오차"),
    ("randomization", "무작위 배정", "대상을 우연 기준으로 나누어 편향을 줄이다", "누가 어디 들어갈지 의도 대신 추첨으로 가르는 느낌", "randomization=무작위 배정 / allocation=배분 / selection=선택"),
    ("replicability", "재현 가능성", "같은 절차를 다시 했을 때 결과가 되풀이될 수 있는 정도", "한 번만 맞는 게 아니라 다시 해도 따라 나오는 힘", "replicability=재현 가능성 / reliability=신뢰성 / validity=타당성"),
    ("generalization", "일반화", "일부 결과를 더 넓은 집단이나 상황으로 확장해 말하다", "작은 표본에서 본 패턴을 더 큰 범위로 넓히는 느낌", "generalization=일반화 / extrapolation=범위 밖 추정 / assumption=가정"),
    ("extrapolation", "외삽 추정", "관측 범위 밖을 기존 추세로 넓혀 추정한 값이나 결론", "본 구간 바깥으로 선을 연장해 얻은 추정", "extrapolation=외삽 추정 / interpolation=보간 / projection=예측치"),
    ("interpolation", "보간 추정", "이미 아는 두 점 사이 빈 구간을 채워 추정한 값", "두 기준점 사이를 자연스럽게 이어 중간값을 읽는 느낌", "interpolation=보간 추정 / extrapolation=외삽 추정 / approximation=근사"),
    ("thresholding", "임계값 적용", "특정 기준선 이상·이하를 나누어 판정하다", "선 하나를 그어 넘었는지 안 넘었는지 가르는 느낌", "thresholding=임계값 적용 / filtering=걸러내기 / classification=분류"),
    ("filtering", "필터링", "기준에 맞지 않는 값이나 잡음을 걸러 내다", "통과 조건에 맞는 것만 체로 남기는 느낌", "filtering=걸러내기 / screening=선별 / exclusion=제외"),
    ("ranking", "순위화", "값이나 대상의 상대적 위치를 순서로 정하다", "크고 작은 순으로 줄을 세워 위치를 매기는 느낌", "ranking=순위화 / rating=점수화 / classification=분류"),
    ("upward", "위쪽으로", "수치나 방향이 위로 향하는", "선이나 움직임이 아래가 아니라 위를 향하는 느낌", "upward=위쪽으로 / downward=아래쪽으로 / forward=앞으로"),
    ("downward", "아래쪽으로", "수치나 방향이 아래로 향하는", "높던 위치에서 아래를 향해 내려가는 느낌", "downward=아래쪽으로 / upward=위쪽으로 / backward=뒤로"),
    ("comparability", "비교 가능성", "서로 다른 값이나 집단을 공정하게 견줄 수 있는 정도", "같은 눈금 위에 올려 비교해도 되는 상태", "comparability=비교 가능성 / similarity=유사성 / equivalence=동등성"),
    ("uncorrelated", "상관없는", "두 변수의 움직임이 서로 체계적으로 이어지지 않는", "한쪽이 움직여도 다른 쪽은 따라가지 않는 느낌", "uncorrelated=상관없는 / independent=독립적인 / unrelated=관련 없는"),
    ("nonlinear", "비선형의", "변화가 일정한 직선 비율로 늘거나 줄지 않는", "같은 간격으로 움직이지 않고 휘어지는 변화선", "nonlinear=비선형의 / linear=선형의 / irregular=불규칙한"),
    ("linear", "선형의", "변화가 대체로 직선적 비율로 이어지는", "입력이 늘면 출력도 일정한 선을 따라 움직이는 느낌", "linear=선형의 / nonlinear=비선형의 / sequential=순차적인"),
    ("cumulative", "누적되는", "시간이 지나며 값이나 효과가 계속 더해지는", "한 번의 변화가 끝나지 않고 층층이 쌓이는 느낌", "cumulative=누적되는 / incremental=단계적으로 느는 / temporary=일시적"),
    ("incremental", "점진적인", "큰 변화가 아니라 작은 단계로 차근차근 늘어나는", "한 번에 뛰지 않고 계단처럼 조금씩 가는 느낌", "incremental=점진적인 / gradual=서서히 / abrupt=갑작스러운"),
    ("proportional", "비례하는", "한 값이 다른 값의 크기에 맞춰 함께 늘거나 줄어드는", "한쪽이 두 배면 다른 쪽도 그 비율로 따라가는 느낌", "proportional=비례하는 / related=관련된 / equivalent=동등한"),
    ("inverse", "반비례의", "한 값이 커질수록 다른 값이 반대로 작아지는 관계의", "한쪽이 올라가면 다른 쪽은 내려가는 거울 관계", "inverse=반대 방향 관계의 / opposite=반대의 / reciprocal=역수의"),
    ("annualized", "연율로 환산한", "짧은 기간의 변화를 1년 기준으로 바꾸어 나타낸", "부분 기간 값을 1년짜리 눈금으로 늘려 보는 느낌", "annualized=연율 환산한 / annual=연간의 / monthly=월간의"),
    ("seasonality", "계절성", "특정 시기마다 반복되는 주기적 패턴", "해마다 비슷한 때에 다시 나타나는 출렁임", "seasonality=계절성 / cycle=주기 / trend=장기 추세"),
    ("cyclicality", "순환성", "오르내림이 주기적으로 되풀이되는 성질", "변화가 한 번 끝나지 않고 파도처럼 다시 도는 느낌", "cyclicality=순환성 / seasonality=계절성 / randomness=무작위성"),
    ("volatility", "변동성", "값이 짧은 기간에 크게 출렁이는 정도", "그래프가 잔잔하지 않고 크게 흔들리는 느낌", "volatility=변동성 / variability=퍼짐 정도 / instability=불안정성"),
    ("stabilization", "안정화", "흔들리던 값이나 상태가 더 일정해지는 과정", "출렁이던 선이 점점 평평해지며 자리를 잡는 느낌", "stabilization=안정화 / normalization=기준 맞춤 / recovery=회복"),
    ("deterioration", "악화", "상태나 성과가 시간이 지나며 더 나빠지는 것", "선이 아래로 가면서 질도 함께 떨어지는 느낌", "deterioration=악화 / decline=감소 / degradation=저하"),
    ("improvement", "개선", "성과나 상태가 더 나아지는 변화", "막히던 값이 좋은 방향으로 올라가는 느낌", "improvement=개선 / increase=증가 / recovery=회복"),
    ("attainment", "달성", "목표나 기준에 실제로 도달하는 것", "설정한 선을 마침내 넘어서는 느낌", "attainment=목표 달성 / achievement=성취 / acquisition=획득"),
    ("shortfall", "부족분", "필요한 양이나 목표치에 못 미친 차이", "도달해야 할 선 아래에 남은 빈칸", "shortfall=부족분 / deficit=적자·결손 / gap=차이"),
    ("surplus", "초과분", "필요량이나 기준을 넘겨 남는 양", "필요선을 넘고도 남아 위로 튀어나온 몫", "surplus=초과분 / excess=과잉 / reserve=비축분"),
    ("convergence", "수렴", "여러 값이나 경로가 점차 비슷한 방향으로 모이는 것", "떨어진 선들이 한 점 쪽으로 좁혀 오는 느낌", "convergence=수렴 / overlap=겹침 / alignment=정렬"),
    ("divergence", "발산", "값이나 경로가 시간이 갈수록 서로 멀어지는 것", "처음 가까웠던 선들이 점점 벌어지는 느낌", "divergence=발산·차이 확대 / deviation=편차 / difference=차이"),
    ("stagnation", "정체", "성장이나 개선이 거의 멈춰 더 나아가지 않는 상태", "움직이던 선이 제자리에서 굳어 버린 느낌", "stagnation=정체 / plateau=정체 구간 / decline=감소"),
    ("acceleration", "가속", "증가나 변화 속도가 더 빨라지는 것", "같은 방향 변화가 점점 더 빠르게 붙는 느낌", "acceleration=가속 / increase=증가 / momentum=탄력"),
    ("deceleration", "감속", "증가나 이동 속도가 점차 느려지는 것", "앞으로 가긴 하지만 속도가 서서히 풀리는 느낌", "deceleration=감속 / slowdown=둔화 / decline=감소"),
    ("plateauing", "정체 단계에 들어섬", "증가세가 약해져 평평한 구간으로 가는 상태", "가파른 선이 더는 안 오르고 납작해지는 느낌", "plateauing=정체 단계 진입 / stabilizing=안정화 / declining=감소"),
    ("breakdown", "세부 내역", "전체 수치를 항목별로 나누어 보여 준 정리", "한 숫자 덩어리를 항목별 조각으로 풀어 놓은 표", "breakdown=세부 내역 / summary=요약 / distribution=분포"),
    ("readout", "출력 결과", "장비·분석에서 바로 읽히는 표시값이나 결과", "기계나 표가 화면에 띄워 주는 숫자 결과", "readout=출력 결과 / output=산출물 / indicator=지표"),
    ("data-based", "자료 기반의", "주관보다 수집된 자료를 근거로 한", "느낌보다 데이터 바닥 위에 올려 말하는 느낌", "data-based=자료 근거의 / subjective=주관적"),
    ("measurability", "측정 가능성", "현상이나 성과를 실제로 수치로 잴 수 있는 정도", "막연한 말을 숫자 자에 올릴 수 있는지 보는 느낌", "measurability=측정 가능성 / observability=관찰 가능성 / precision=정밀도"),
    ("observability", "관찰 가능성", "현상이나 상태를 직접 또는 간접 지표로 볼 수 있는 정도", "숨어 있는 상태가 밖에서 읽히는지 보는 느낌", "observability=관찰 가능성 / visibility=가시성 / measurability=측정 가능성"),
    ("traceability", "추적 가능성", "결과·기록·출처를 거슬러 확인할 수 있는 정도", "어디서 왔는지 선을 따라 되짚을 수 있는 상태", "traceability=추적 가능성 / accountability=책임성 / transparency=투명성"),
    ("comparative", "비교의", "둘 이상의 대상을 견주어 차이와 공통점을 보는", "혼자 보지 않고 옆에 세워 상대적으로 읽는 느낌", "comparative=비교의 / comparable=비교 가능한 / contrasting=대비되는"),
    ("descriptive", "기술적인", "원인 판단보다 관찰된 특징을 설명하는", "왜보다 무엇이 어떻게 보이는지를 먼저 적는 느낌", "descriptive=기술적인 / analytical=분석적인 / evaluative=평가적인"),
    ("inferential", "추론의", "관측된 자료에서 더 넓은 결론을 이끌어 내는", "보이는 숫자 너머의 결론을 조심스럽게 뽑는 느낌", "inferential=추론의 / descriptive=기술적인 / speculative=추측성의"),
    ("statistically", "통계적으로", "개별 사례보다 자료 패턴과 수치 기준에 따라", "감각이 아니라 통계 눈금으로 판단하는 느낌", "statistically=통계적으로 / numerically=수치상 / qualitatively=질적으로"),
    ("numerically", "수치상으로", "말보다 숫자 값으로 표현했을 때", "서술보다 숫자 칸에 넣어 보는 느낌", "numerically=수치상으로 / statistically=통계적으로 / verbally=말로"),
    ("approximately", "대략", "정확히 딱 맞지는 않지만 가까운 값으로", "정답점 주변에 가까이 붙여 말하는 느낌", "approximately=대략 / roughly=거칠게 대략 / exactly=정확히"),
    ("roughly", "대충", "세밀하지 않지만 큰 범위에서 어림하여", "잔선을 다 지우고 큰 윤곽만 잡아 말하는 느낌", "roughly=대충·거칠게 / approximately=대략 / precisely=정확히"),
    ("consistently", "일관되게", "여러 번이나 여러 조건에서 비슷한 패턴으로", "한 번만이 아니라 계속 같은 방향으로 나오는 느낌", "consistently=일관되게 / repeatedly=반복해서 / uniformly=균일하게"),
    ("systematically", "체계적으로", "정해진 기준과 순서에 따라 빠짐없이", "즉흥이 아니라 절차와 구조를 따라 훑는 느낌", "systematically=체계적으로 / randomly=무작위로 / casually=느슨하게"),
    ("sequentially", "순차적으로", "한 단계씩 정해진 순서를 따라", "앞 단계가 끝나야 다음 칸으로 넘어가는 느낌", "sequentially=순차적으로 / simultaneously=동시에 / randomly=무작위로"),
    ("simultaneously", "동시에", "둘 이상의 일이 같은 시점에 함께 일어나는 방식으로", "시간축 위에서 여러 사건이 한 칸에 겹치는 느낌", "simultaneously=동시에 / sequentially=순서대로 / independently=독립적으로"),
    ("cautiously", "조심스럽게", "결론을 단정하지 않고 불확실성을 고려하며", "성급히 점프하지 않고 한 발씩 확인하는 느낌", "cautiously=조심스럽게 / confidently=확신 있게 / tentatively=잠정적으로"),
    ("tentatively", "잠정적으로", "확정 전이지만 일단 임시 결론으로", "아직 못 박지 않고 연필로 먼저 적어 두는 느낌", "tentatively=잠정적으로 / temporarily=일시적으로 / conclusively=결정적으로"),
    ("substantially", "상당히", "작은 차이를 넘어서 의미 있게 큰 정도로", "눈에 띄게 큰 폭으로 결론 쪽에 힘을 싣는 느낌", "substantially=상당히 / marginally=약간 / slightly=조금"),
    ("marginally", "약간만", "차이나 효과가 아주 작은 폭으로", "선은 움직였지만 가장자리를 조금 건드린 정도", "marginally=약간만 / substantially=상당히 / dramatically=극적으로"),
    ("uniformly", "균일하게", "부분마다 큰 차이 없이 비슷한 수준으로", "어느 칸을 봐도 높낮이가 비슷한 느낌", "uniformly=균일하게 / unevenly=불균등하게 / consistently=일관되게"),
    ("unevenly", "불균등하게", "부분이나 집단마다 고르게 나뉘지 않고 차이가 나게", "한쪽은 두껍고 한쪽은 얇게 울퉁불퉁 퍼진 느낌", "unevenly=불균등하게 / uniformly=균일하게 / randomly=무작위로"),
    ("monotonically", "단조롭게 한 방향으로", "중간에 반전 없이 계속 증가하거나 감소하는 방식으로", "중간에 꺾이지 않고 한 방향으로만 가는 선", "monotonically=단조롭게 한 방향으로 / steadily=꾸준히 / erratically=불규칙하게"),
    ("erratically", "불규칙하게", "예측하기 어렵게 들쭉날쭉한 방식으로", "선이 매끄럽지 않고 여기저기 갑자기 튀는 느낌", "erratically=불규칙하게 / steadily=꾸준히 / randomly=무작위로"),
    ("steadily", "꾸준히", "급격한 흔들림 없이 일정한 속도로 이어지게", "큰 튐 없이 한 방향으로 차분히 이어지는 느낌", "steadily=꾸준히 / abruptly=갑자기 / intermittently=간헐적으로"),
    ("intermittently", "간헐적으로", "계속 이어지지 않고 끊겼다 나타나는 방식으로", "쭉 이어지지 않고 켜졌다 꺼졌다 하는 느낌", "intermittently=간헐적으로 / continuously=연속적으로 / occasionally=가끔"),
    ("continuously", "연속적으로", "중간 끊김 없이 이어지게", "선이 중간에 끊기지 않고 계속 이어지는 느낌", "continuously=연속적으로 / intermittently=간헐적으로 / repeatedly=반복해서"),
    ("comparatively", "비교적", "다른 대상과 견주어 볼 때 상대적으로", "절대값 하나보다 옆과 비교한 위치로 말하는 느낌", "comparatively=비교적 / relatively=상대적으로 / absolutely=절대적으로"),
    ("relative", "상대적인", "다른 기준이나 대상과의 관계 속에서 정해지는", "혼자 고정된 값이 아니라 옆과의 위치로 의미가 바뀌는 느낌", "relative=상대적인 / absolute=절대적인 / comparative=비교의"),
    ("absolute", "절대적인", "다른 기준과 상관없이 고정된 값이나 기준의", "옆과 비교하지 않고 그 자체 값으로 못 박는 느낌", "absolute=절대적인 / relative=상대적인 / fixed=고정된"),
    ("estimate", "추정하다", "불완전한 자료로 대략 값을 계산하다", "정확한 수치 대신 가까운 값을 계산해 보는 느낌", "estimate=추정하다 / calculate=정확히 계산하다 / guess=짐작하다"),
    ("parameterize", "매개변수로 표현하다", "모델이나 식을 몇 개 핵심 변수로 나타내다", "복잡한 관계를 조절 가능한 변수 손잡이로 바꾸는 느낌", "parameterize=매개변수로 표현하다 / model=모델링하다 / quantify=수량화하다"),
    ("dimensionality", "차원 수", "자료나 모델이 가진 변수·축의 개수와 복잡도", "평면이 아니라 몇 개 방향으로 펼쳐져 있는지 세는 느낌", "dimensionality=차원 수 / scale=척도 / complexity=복잡성"),
    ("scalability", "확장성", "규모가 커져도 시스템이나 방법이 감당하며 작동하는 정도", "작게 되던 방식이 커져도 무너지지 않고 늘어나는 힘", "scalability=확장성 / flexibility=유연성 / capacity=수용력"),
    ("throughput", "처리량", "일정 시간 안에 시스템이나 절차가 처리하는 양", "시간당 얼마나 많은 항목이 통과하는지 보는 느낌", "throughput=처리량 / capacity=최대 수용력 / speed=속도"),
    ("latency", "지연 시간", "요청 후 반응이 나타나기까지 걸리는 짧은 시간", "보냈는데 바로 안 돌아오고 사이에 생기는 짧은 빈칸", "latency=지연 시간 / delay=지연 / response time=응답 시간"),
    ("uptake", "채택률", "제도·서비스·권고가 실제로 받아들여지는 정도", "제안한 것이 현장에서 얼마나 먹혀 들어가는지 보는 느낌", "uptake=채택·흡수 정도 / adoption=도입 / participation=참여"),
    ("retention", "유지율", "사람이나 정보가 시간이 지나도 남아 있는 정도", "처음 들어온 것이 빠져나가지 않고 남는 힘", "retention=유지율·보유 / persistence=지속성 / recall=회상"),
    ("attrition", "이탈률", "시간이 지나며 참여자나 구성원이 빠져나가는 감소", "처음 있던 집단이 조금씩 떨어져 나가는 느낌", "attrition=이탈 감소 / turnover=교체율 / dropout=중도 이탈"),
    ("coverage", "포괄 범위", "자료·제도·측정이 어디까지 포함하는지의 넓이", "지도가 빈틈 없이 얼마나 덮고 있는지 보는 느낌", "coverage=포괄 범위 / scope=범위 / completeness=완전성"),
    ("completeness", "완전성", "빠진 항목 없이 필요한 정보가 다 채워진 정도", "표에 빈칸 없이 필요한 조각이 다 들어 있는 느낌", "completeness=완전성 / accuracy=정확성 / coverage=포괄 범위"),
    ("precision", "정밀도", "값이나 구분이 얼마나 세밀하고 흔들림 적게 잡히는지", "대충 넓게가 아니라 좁은 점에 또렷하게 맞추는 느낌", "precision=정밀도 / accuracy=정확도 / specificity=특이성"),
]


def write_rows(path: Path, rows: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)


def build_rows(items: list[tuple[str, str, str, str, str]], used: set[str], count: int) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for word, core, sub, feel, distinction in items:
        if word in used:
            continue
        back = "\n".join(
            [
                f"핵심 뜻: {core}",
                f"부가 뜻: {sub}",
                f"핵심 느낌: {feel}",
                f"구분: {distinction}",
            ]
        )
        rows.append((word, back))
        used.add(word)
        if len(rows) == count:
            break
    if len(rows) != count:
        raise RuntimeError(f"expected {count} rows, got {len(rows)}")
    return rows


def load_existing_headwords() -> set[str]:
    used: set[str] = set()
    patterns = ("toefl_ets_2026_set_[0-9][0-9].tsv", "toefl_awl_set_[0-9][0-9].tsv")
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if path.name in TARGET_FILES:
                continue
            with path.open(encoding="utf-8", newline="") as handle:
                for row in csv.reader(handle, delimiter="\t"):
                    if row:
                        used.add(row[0])
    return used


def main() -> int:
    used = load_existing_headwords()
    set23 = build_rows(PRACTICAL_WORDS, used, 100)
    set24 = build_rows(QUANT_WORDS, used, 100)
    write_rows(ROOT / "toefl_ets_2026_set_23.tsv", set23)
    write_rows(ROOT / "toefl_ets_2026_set_24.tsv", set24)
    print("set23=100 set24=100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
