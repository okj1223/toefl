from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "toefl_ets_2026_set_15.tsv"

CARDS = [
    ("accessibility", "접근성 / 이용하기 쉬움", "누구나 정보·도구·공간에 어렵지 않게 접근할 수 있는 정도", "문턱이 낮아서 필요한 사람에게 열려 있는 느낌", "accessibility=접근하기 쉬움 / availability=이용 가능함 / usability=쓰기 편함"),
    ("algorithmic", "알고리즘 기반의", "정해진 계산·판단 절차에 따라 처리되는", "사람 감으로 대충이 아니라 규칙화된 절차가 돌리는 느낌", "algorithmic=규칙화된 계산 절차 기반의 / systematic=체계적인 / manual=사람이 직접 하는"),
    ("archive", "자료 보관소 / 보관하다", "나중에 다시 찾을 수 있게 기록과 파일을 저장해 둔 곳이나 그 행위", "지나간 자료를 버리지 않고 정리해 넣어두는 창고", "archive=기록을 장기 보관함 / repository=자료 저장소 / backup=복사본 저장"),
    ("bandwidth", "처리 여력 / 대역폭", "한 번에 처리하거나 소화할 수 있는 정보·업무의 용량", "통로가 얼마나 넓어서 많이 지나갈 수 있는지 보는 느낌", "bandwidth=처리 가능한 용량·여력 / capacity=수용 가능량 / speed=빠르기"),
    ("browser", "브라우저 / 웹 탐색 도구", "웹 자료를 찾아보고 화면에 띄우는 소프트웨어", "인터넷 자료를 창으로 열어 넘겨 보는 도구", "browser=웹을 탐색하는 도구 / platform=서비스가 돌아가는 기반 / app=특정 기능 앱"),
    ("cache", "임시 저장소 / 임시로 저장하다", "자주 쓰는 정보를 빠르게 다시 꺼내려고 잠시 저장해 둠", "매번 새로 찾지 않게 가까운 곳에 잠깐 보관하는 느낌", "cache=빠른 접근용 임시 저장 / archive=장기 보관 / memory=기억·저장 공간 일반"),
    ("clickthrough", "클릭 후 이동 / 클릭 반응", "온라인 콘텐츠에서 실제 클릭으로 다음 행동이 이어지는 것", "봤다는 수준을 넘어 눌러서 다음 단계로 들어가는 느낌", "clickthrough=클릭으로 후속 이동이 일어남 / view=그냥 봄 / engagement=적극적 관여"),
    ("cloud-based", "클라우드 기반의", "개인 기기 안이 아니라 온라인 서버와 네트워크에 저장·처리 기반을 둔", "내 컴퓨터 한 대보다 온라인 공간에 올려두고 쓰는 느낌", "cloud-based=온라인 서버 기반의 / local=기기 내부의 / online=인터넷에 연결된"),
    ("connectivity", "연결성 / 네트워크 접속 상태", "사람·장치·정보가 서로 이어지고 접속되는 정도", "끊어지지 않고 선이 살아 있어서 서로 오갈 수 있는 느낌", "connectivity=서로 연결되고 접속되는 성질 / communication=의미를 주고받음 / access=들어갈 수 있음"),
    ("crowdsourced", "대중 참여로 모은 / 집단 기여형의", "소수 전문가만이 아니라 많은 사람의 참여와 입력으로 만들어진", "여러 사람의 작은 기여를 모아 하나를 만드는 느낌", "crowdsourced=대중 기여로 모은 / collaborative=함께 작업하는 / expert-led=전문가 주도"),
    ("curate", "선별해 구성하다 / 큐레이션하다", "정보나 자료를 아무렇게나 모으지 않고 기준에 따라 골라 정리하다", "많은 것 중 쓸 만한 걸 골라 보기 좋게 배열하는 느낌", "curate=선별해 구성하다 / collect=모으다 / organize=정돈하다"),
    ("cybersecurity", "사이버 보안", "온라인 시스템과 정보를 무단 접근·공격·유출로부터 보호하는 일", "디지털 공간의 문과 잠금장치를 지키는 느낌", "cybersecurity=디지털 시스템 보안 / privacy=개인정보 보호 / encryption=암호화 방식"),
    ("dashboard", "대시보드 / 한눈에 보는 현황판", "여러 지표와 상태를 한 화면에서 요약해 보여주는 인터페이스", "흩어진 정보를 한 판에 모아 바로 보게 하는 조종판", "dashboard=현황을 모아 보여주는 화면 / overview=전체 개요 / interface=사용자가 만나는 화면·접점"),
    ("data-driven", "데이터 기반의", "감이나 전통보다 수집된 자료와 분석 결과를 근거로 삼는", "느낌이 아니라 숫자와 근거를 먼저 보는 결정 방식", "data-driven=데이터를 근거로 한 / empirical=관찰·자료 기반의 / intuitive=직관적인"),
    ("debug", "오류를 찾아 고치다", "시스템이나 절차가 어긋나는 원인을 찾아 수정하다", "겉 결과만 보지 않고 어디서 삐걱대는지 따라가 고치는 느낌", "debug=오류 원인을 찾아 수정하다 / troubleshoot=문제를 진단해 해결하다 / revise=내용을 고쳐 쓰다"),
    ("digitize", "디지털화하다 / 전산화하다", "종이·아날로그 자료를 전자 형식으로 바꾸다", "물리적 자료를 파일과 데이터 형태로 옮기는 느낌", "digitize=전자 형식으로 바꾸다 / scan=이미지로 읽어들이다 / encode=정보를 코드화하다"),
    ("download", "내려받기 / 다운로드하다", "온라인에 있는 파일이나 자료를 자기 기기로 가져오다", "저쪽 서버에 있는 걸 내 쪽으로 당겨오는 느낌", "download=온라인에서 내 기기로 받음 / upload=내 기기에서 온라인으로 올림 / retrieve=찾아 꺼냄"),
    ("e-commerce", "전자상거래", "온라인에서 상품과 서비스를 사고파는 거래", "가게 안이 아니라 화면과 결제 시스템 위에서 이루어지는 거래", "e-commerce=온라인 상거래 / retail=소매 판매 / marketplace=거래가 모이는 장터"),
    ("editable", "편집 가능한 / 수정할 수 있는", "내용이나 형식을 나중에 바꿀 수 있는", "한 번 정하면 끝이 아니라 다시 손댈 여지가 열려 있는 느낌", "editable=직접 수정할 수 있는 / modifiable=변형 가능함 / fixed=고정된"),
    ("encryption", "암호화", "정보를 허가 없이 읽기 어렵게 코드 형태로 바꾸는 보안 방식", "내용을 그대로 드러내지 않고 잠금 코드로 감싸는 느낌", "encryption=정보를 암호화함 / authentication=접속자를 확인함 / privacy=사생활 보호"),
    ("filter", "거르다 / 선별 기준", "많은 정보 중 조건에 맞는 것만 남기거나 보여주다", "전부 통과시키지 않고 체에 걸러 필요한 것만 남기는 느낌", "filter=기준에 따라 걸러냄 / sort=순서나 유형별로 정렬함 / screen=부적합한 것을 선별함"),
    ("firewall", "방화벽 / 접근 차단 장치", "외부 접속이나 공격이 함부로 들어오지 못하게 막는 보안 장치", "바깥과 안 사이에 세워둔 디지털 차단벽", "firewall=무단 접근을 막는 보안벽 / password=접속 암호 / boundary=경계선"),
    ("formatting", "서식 지정 / 형식 맞추기", "문서나 화면의 글자·배치·표현 형식을 보기 좋게 정리함", "내용을 그냥 두지 않고 정해진 모양으로 맞춰 정돈하는 느낌", "formatting=형식을 보기 좋게 맞춤 / editing=내용과 문장을 고침 / layout=배치 구조"),
    ("hyperlink", "하이퍼링크 / 연결 링크", "한 자료에서 다른 웹페이지나 위치로 바로 이동하게 하는 연결", "눌렀을 때 다른 정보로 점프하는 문", "hyperlink=웹상의 직접 연결 링크 / reference=참조 대상 / bookmark=저장해둔 위치"),
    ("indexing", "색인화 / 찾아보기용 정리", "자료를 검색하기 쉽게 기준에 따라 항목화하고 연결해 둠", "나중에 바로 찾을 수 있게 이름표와 위치표를 달아두는 느낌", "indexing=검색용으로 항목화함 / cataloging=목록으로 정리함 / archiving=보관함"),
    ("infographic", "인포그래픽 / 정보 시각화 자료", "수치나 설명을 그림·도표로 압축해 보여주는 시각 자료", "긴 글 대신 그림과 숫자로 한눈에 이해시키는 자료", "infographic=정보를 시각적으로 요약한 자료 / chart=도표 / illustration=설명용 그림"),
    ("input", "입력 / 투입 자료", "시스템이나 과정 안으로 들어가는 정보·자원", "밖에서 안으로 넣는 시작 재료", "input=과정에 들어가는 정보·자원 / output=밖으로 나온 결과 / intake=받아들이는 양"),
    ("interactive", "상호작용적인 / 쌍방향의", "한쪽이 일방적으로 보여주는 게 아니라 사용자의 반응에 따라 주고받는", "누르면 바뀌고 응답하면 다시 돌아오는 느낌", "interactive=쌍방향으로 반응하는 / passive=일방향으로 받는 / participatory=참여 중심의"),
    ("interoperability", "상호운용성 / 호환 작동성", "서로 다른 시스템이나 도구가 함께 연결되어 문제없이 작동하는 능력", "각자 따로 놀지 않고 연결해도 맞물려 도는 느낌", "interoperability=서로 다른 시스템이 함께 작동함 / compatibility=서로 맞게 쓸 수 있음 / integration=하나로 묶어 넣음"),
    ("latency", "지연 시간 / 반응 지연", "요청이나 신호 후 실제 반응이 돌아오기까지 걸리는 시간", "누른 뒤 바로가 아니라 살짝 늦게 따라오는 간격", "latency=반응이 돌아오는 지연 시간 / delay=늦어짐 일반 / lag=뒤처지는 시간차"),
    ("livestream", "실시간 방송 / 라이브 스트리밍", "녹화 뒤가 아니라 진행 중인 영상·음성을 온라인으로 바로 전송함", "지금 일어나는 것을 화면으로 즉시 흘려보내는 느낌", "livestream=실시간 온라인 송출 / recording=녹화본 / broadcast=방송 전송 일반"),
    ("log-in", "로그인 / 접속 인증", "계정 정보를 입력해 시스템 안으로 들어감", "문 앞에서 신분을 확인받고 안으로 들어가는 느낌", "log-in=계정으로 접속함 / authentication=접속 자격 확인 / registration=새로 등록함"),
    ("machine-readable", "기계가 읽을 수 있는", "사람만 이해하는 형식이 아니라 컴퓨터가 자동 처리할 수 있는 구조의", "눈으로 보기만 좋은 게 아니라 시스템이 바로 읽는 형태", "machine-readable=컴퓨터가 자동 처리 가능함 / human-readable=사람이 읽기 쉬움 / digitized=전자화된"),
    ("malware", "악성 소프트웨어", "시스템을 해치거나 정보를 훔치도록 만들어진 프로그램", "겉은 프로그램인데 안에서는 해를 끼치는 디지털 침입자", "malware=해를 주는 악성 소프트웨어 / virus=자기 복제형 악성코드 / software=프로그램 일반"),
    ("metadata", "메타데이터 / 자료 설명 정보", "데이터 자체를 설명하는 제목·출처·날짜·형식 같은 정보", "내용 본문 옆에 붙은 자료의 이름표와 설명표", "metadata=데이터를 설명하는 정보 / content=본문 내용 / annotation=설명 주석"),
    ("misinformation", "오정보 / 잘못된 정보", "사실과 다르거나 부정확해서 오해를 낳는 정보", "맞아 보이지만 방향을 잘못 잡게 만드는 정보", "misinformation=틀리거나 부정확한 정보 / disinformation=의도적으로 퍼뜨린 허위정보 / rumor=소문"),
    ("multimedia", "멀티미디어 / 복합 매체", "텍스트·이미지·소리·영상이 함께 쓰이는 자료나 형식", "한 종류 자료만이 아니라 여러 매체가 섞여 전달되는 느낌", "multimedia=여러 매체를 함께 활용함 / text-based=글 중심의 / audiovisual=소리와 영상 중심의"),
    ("navigate", "찾아 이동하다 / 탐색하다", "복잡한 정보나 공간 속에서 필요한 경로를 따라가다", "길을 잃지 않게 메뉴와 연결을 짚으며 움직이는 느낌", "navigate=경로를 찾아 이동·탐색하다 / browse=훑어보다 / access=들어가 이용하다"),
    ("newsletter", "뉴스레터 / 정기 안내 메일", "업데이트와 소식을 묶어 정기적으로 보내는 온라인 안내문", "가끔 흩어진 공지보다 한 번에 묶어 보내는 소식지", "newsletter=정기 소식 안내문 / bulletin=공지문 / email=전자우편 일반"),
    ("notification", "알림 / 통지", "새 정보·변경·요청이 있음을 알려 주는 메시지", "놓치지 말라고 화면이나 메일이 톡 알려주는 신호", "notification=변경·소식을 알려주는 메시지 / reminder=잊지 않게 다시 알림 / announcement=공식 발표"),
    ("open-source", "오픈소스의 / 공개 소스 기반의", "코드나 설계가 공개되어 누구나 확인·수정·공유할 수 있는", "닫힌 상자보다 안을 열어 함께 보고 고칠 수 있는 느낌", "open-source=소스가 공개된 / proprietary=독점 소유의 / shared=공유된"),
    ("output", "출력 / 산출물", "과정이나 시스템 밖으로 나온 결과나 생성물", "안에서 처리된 뒤 바깥으로 나온 결과물", "output=과정에서 나온 결과 / input=들어간 자료·자원 / outcome=최종 결과"),
    ("password-protected", "비밀번호로 보호된", "허가된 사람만 암호를 입력해 열 수 있게 잠겨 있는", "아무나 못 열게 문 앞에 비밀번호 자물쇠를 건 느낌", "password-protected=비밀번호로 접근을 막아둔 / encrypted=내용을 암호화한 / public=공개된"),
    ("platform", "플랫폼 / 기반 서비스", "사람과 콘텐츠, 기능이 모이고 상호작용하는 디지털 기반", "개별 기능들이 올라서 작동하는 온라인 바닥판", "platform=서비스와 상호작용이 올라서는 기반 / interface=사용자가 만나는 접점 / channel=전달 경로"),
    ("plug-in", "플러그인 / 추가 기능 모듈", "기존 프로그램에 붙여 기능을 더하는 작은 구성요소", "본체를 새로 갈지 않고 옆에 끼워 넣는 추가 장치", "plug-in=기존 시스템에 붙는 추가 기능 / module=기능 단위 / extension=기능 확장"),
    ("podcast", "팟캐스트 / 오디오 프로그램", "온라인으로 듣는 시리즈형 음성 콘텐츠", "시간 맞춰 방송을 기다리지 않고 골라 듣는 말 중심 콘텐츠", "podcast=온라인 오디오 콘텐츠 / livestream=실시간 송출 / lecture=강의"),
    ("pop-up", "팝업 창 / 갑자기 뜨는 창", "현재 화면 위에 추가로 떠서 메시지나 선택을 요구하는 창", "가던 화면 위로 작은 창이 툭 끼어드는 느낌", "pop-up=갑자기 뜨는 작은 창 / notification=알림 메시지 / webpage=웹페이지"),
    ("privacy", "사생활 보호 / 개인정보 보호", "개인 정보와 활동이 원치 않게 드러나지 않도록 지키는 상태나 권리", "내 정보의 문을 내가 열고 닫을 수 있게 지키는 느낌", "privacy=개인 정보와 사적 영역 보호 / security=시스템 안전 / confidentiality=비밀 유지"),
    ("profile", "프로필 / 특징 요약", "사람·집단·대상의 핵심 정보와 특성을 정리한 소개", "누군지 한눈에 보이게 핵심만 모아 적은 얼굴표", "profile=대상의 핵심 정보와 특징 요약 / identity=정체성 / description=설명"),
    ("public-facing", "외부 공개용의 / 사용자 대상의", "조직 내부용이 아니라 바깥 사람이나 일반 사용자에게 보이는", "안쪽 실무 화면이 아니라 밖으로 드러나는 창구 느낌", "public-facing=외부 사용자에게 보이는 / internal=내부용의 / private=비공개의"),
    ("query", "질의 / 검색 요청", "필요한 정보를 얻으려고 시스템이나 자료에 던지는 질문", "찾고 싶은 걸 검색창에 조건으로 던지는 느낌", "query=정보를 얻기 위한 질의 / question=질문 일반 / request=요청"),
    ("real-time", "실시간의", "지연을 크게 두지 않고 일이 일어나는 즉시 반영되는", "지금 변하는 것이 바로 화면과 결과에 따라붙는 느낌", "real-time=즉시 반영되는 실시간의 / delayed=늦게 반영되는 / live=현재 진행 중인"),
    ("searchable", "검색 가능한", "키워드나 조건으로 빠르게 찾아낼 수 있게 되어 있는", "자료 더미를 하나씩 뒤지지 않아도 바로 찾을 수 있는 상태", "searchable=검색해서 찾을 수 있는 / indexed=찾기 쉽게 색인화된 / archived=보관된"),
    ("server", "서버 / 중앙 처리 컴퓨터", "여러 사용자의 요청을 받아 데이터나 기능을 제공하는 시스템", "각자 요청을 보내면 뒤에서 받아 처리해주는 중심 기계", "server=요청을 처리해 제공하는 시스템 / device=개별 장치 / platform=서비스 기반"),
    ("shareability", "공유 용이성 / 퍼뜨리기 쉬움", "자료나 콘텐츠를 다른 사람에게 쉽게 전달·공유할 수 있는 정도", "좋으면 바로 복사해 남에게 넘길 수 있는 열린 정도", "shareability=공유하고 퍼뜨리기 쉬움 / accessibility=접근하기 쉬움 / visibility=눈에 잘 띔"),
    ("software", "소프트웨어 / 프로그램", "컴퓨터나 기기에서 작업을 수행하도록 하는 코드 기반 도구", "기계 껍데기보다 그 안에서 일을 시키는 프로그램 쪽", "software=작동을 지시하는 프로그램 / hardware=물리적 장치 / application=특정 목적 프로그램"),
    ("spam", "스팸 / 원치 않는 대량 메시지", "사용자가 원하지 않는데 반복적으로 들어오는 광고성·불필요 메시지", "내가 찾지 않았는데 화면과 메일을 지저분하게 메우는 잡신호", "spam=원치 않는 대량 메시지 / junk=쓸모없는 것 / notification=필요한 알림"),
    ("streaming", "스트리밍 / 실시간 전송 재생", "파일을 다 내려받기 전에 네트워크로 받으면서 바로 재생하는 방식", "데이터가 흘러오는 대로 끊기지 않게 이어 보는 느낌", "streaming=받으면서 바로 재생·전송함 / download=파일을 내려받음 / broadcast=송출"),
    ("subscribe", "구독하다 / 정기 수신하다", "콘텐츠나 소식을 계속 받아보기로 등록하다", "새 것이 올라오면 놓치지 않게 줄을 걸어두는 느낌", "subscribe=정기적으로 받아보도록 등록하다 / follow=업데이트를 따라가다 / enroll=과정에 등록하다"),
    ("tag", "태그 / 분류 표지", "내용을 찾거나 묶기 쉽게 붙이는 짧은 키워드·표지", "자료에 이름표를 달아 같은 것끼리 바로 모이게 하는 느낌", "tag=분류·검색용 표지 / label=이름표 / category=범주"),
    ("template", "템플릿 / 틀 양식", "비슷한 작업을 반복할 때 기본 구조로 재사용하는 형식", "매번 새로 만들지 않고 먼저 깔아두는 빈 양식", "template=반복해서 쓰는 기본 틀 / format=형식 / sample=예시"),
    ("thumbnail", "썸네일 / 미리보기 작은 이미지", "큰 콘텐츠를 열기 전에 미리 보여주는 축소 이미지", "내용 전체를 보기 전 작게 먼저 보여주는 얼굴 그림", "thumbnail=작은 미리보기 이미지 / preview=미리보기 / icon=상징 그림"),
    ("traceable", "추적 가능한", "출처나 이동 경로, 변경 이력을 따라가 확인할 수 있는", "지나간 발자국이 남아 어디서 왔는지 되짚을 수 있는 느낌", "traceable=경로나 출처를 따라 확인 가능함 / trackable=움직임을 추적할 수 있음 / anonymous=익명이라 출처가 안 드러남"),
    ("upload", "업로드하다 / 올리다", "자기 기기의 파일이나 자료를 온라인 공간으로 전송하다", "내 쪽에 있던 걸 서버나 플랫폼 쪽으로 밀어 올리는 느낌", "upload=로컬 자료를 온라인으로 올림 / download=온라인에서 내려받음 / submit=공식적으로 제출함"),
    ("user-generated", "사용자 제작의 / 이용자 생성형의", "기관이 일방적으로 만든 것이 아니라 일반 사용자가 만들어 올린", "플랫폼 주인보다 이용자들이 직접 채워 넣는 느낌", "user-generated=사용자가 만든 / curated=선별 편집된 / official=공식 제작된"),
    ("virtual", "가상의 / 온라인상의", "물리적 공간이 아니라 디지털 환경이나 시뮬레이션 안에서 이루어지는", "현장에 몸이 없어도 화면 속 공간에서 이루어지는 느낌", "virtual=디지털·가상 환경의 / physical=물리적인 / simulated=모의로 재현된"),
    ("web-based", "웹 기반의", "별도 설치보다 인터넷 브라우저와 온라인 환경에서 작동하는", "프로그램이 내 컴퓨터 안보다 웹 주소 위에서 열리는 느낌", "web-based=웹 환경에서 작동하는 / desktop=기기 설치형의 / offline=인터넷 없이 쓰는"),
    ("wireless", "무선의", "케이블 연결 없이 신호를 주고받는", "선을 꽂지 않아도 공기 중으로 연결되는 느낌", "wireless=물리적 선 없이 연결됨 / wired=케이블로 연결된 / portable=들고 다닐 수 있는"),
    ("workflow automation", "업무 자동화 / 절차 자동 처리", "반복적인 작업 흐름을 사람이 매번 하지 않고 시스템이 자동으로 수행하게 함", "손으로 하나씩 누르던 일을 규칙대로 자동으로 이어 돌리는 느낌", "workflow automation=반복 절차를 자동 처리함 / manual processing=사람이 직접 처리함 / scheduling=시간을 배정함"),
    ("zoomable", "확대·축소 가능한", "화면이나 지도, 이미지의 크기를 키우거나 줄이며 볼 수 있는", "멀리서 전체를 보다가 필요하면 가까이 당겨 보는 느낌", "zoomable=크기를 당겨 조절하며 볼 수 있는 / scalable=크기·규모 확장이 가능한 / fixed-size=크기가 고정된"),
    ("annotation layer", "주석 층 / 덧붙인 설명 표시층", "원본 정보 위에 설명이나 표시를 추가로 얹은 층", "원래 자료를 덮어쓰지 않고 위에 투명 메모지를 한 장 올리는 느낌", "annotation layer=원본 위에 덧붙인 설명층 / metadata=자료를 설명하는 정보 / overlay=위에 겹쳐 올린 층"),
    ("backup copy", "백업 복사본 / 예비 저장본", "원본이 없어지거나 손상될 때를 대비해 따로 저장해 둔 복사본", "문제 생겨도 다시 꺼낼 수 있게 한 벌 더 챙겨둔 느낌", "backup copy=예비로 따로 저장한 복사본 / archive=장기 보관본 / duplicate=복제본"),
    ("browser tab", "브라우저 탭 / 열린 웹 화면 칸", "한 브라우저 안에서 여러 페이지를 따로 열어두는 화면 단위", "창 하나 안에 책갈피처럼 여러 페이지를 나눠 꽂아둔 느낌", "browser tab=웹페이지를 나눠 여는 탭 / window=브라우저 창 / bookmark=저장해둔 링크"),
    ("content moderation", "콘텐츠 조정 / 게시물 관리", "온라인 게시물이 규칙과 안전 기준에 맞는지 검토·제한·정리하는 일", "아무 글이나 그대로 두지 않고 기준에 맞게 거르는 관리", "content moderation=게시물을 규칙에 따라 관리함 / censorship=표현을 제한함 / review=내용을 검토함"),
    ("data portability", "데이터 이동성 / 옮겨 쓸 수 있음", "한 서비스나 형식의 데이터를 다른 곳으로 가져가 활용할 수 있는 성질", "한 플랫폼에 갇히지 않고 내 자료를 들고 옮길 수 있는 느낌", "data portability=데이터를 다른 곳으로 옮겨 쓸 수 있음 / interoperability=시스템끼리 함께 작동함 / transferability=다른 맥락에 적용 가능함"),
    ("digital footprint", "디지털 흔적 / 온라인 활동 기록", "온라인에서 남긴 접속·게시·검색·공유의 기록 자취", "인터넷 위를 지나가며 뒤에 남긴 발자국", "digital footprint=온라인 활동이 남긴 흔적 / record=기록 일반 / profile=요약된 개인정보"),
    ("file-sharing", "파일 공유", "디지털 파일을 다른 사람이나 집단과 주고받을 수 있게 하는 일", "자료를 혼자만 갖지 않고 링크나 시스템으로 나눠주는 느낌", "file-sharing=파일을 공유함 / distribution=자료를 나눠 퍼뜨림 / submission=공식 제출"),
    ("geotagged", "위치 정보가 붙은", "사진이나 게시물, 데이터에 장소 좌표나 위치 설명이 연결된", "자료에 어디서 나온 건지 위치표를 꽂아두는 느낌", "geotagged=위치 태그가 붙은 / tagged=표지가 붙은 / location-based=위치 정보를 기준으로 한"),
    ("infostream", "정보 흐름 / 계속 들어오는 정보", "온라인에서 연속적으로 흘러들어오는 업데이트와 콘텐츠 흐름", "한 번에 끝나는 문서보다 계속 밀려오는 정보 물줄기", "infostream=지속적으로 들어오는 정보 흐름 / newsfeed=업데이트가 모인 피드 / stream=연속 흐름"),
    ("link-sharing", "링크 공유", "웹 주소를 보내 다른 사람이 같은 자료로 들어가게 하는 일", "파일 전체를 보내지 않고 들어가는 문 주소를 건네는 느낌", "link-sharing=웹 주소를 공유함 / file-sharing=파일 자체를 공유함 / citation=출처를 밝히며 참조함"),
    ("media literacy", "미디어 해석 역량 / 정보 판별력", "매체의 메시지와 출처, 의도를 비판적으로 읽고 판단하는 능력", "보이는 걸 그대로 믿지 않고 어디서 왜 나왔는지 한 번 더 읽는 힘", "media literacy=매체 정보를 비판적으로 해석하는 능력 / digital literacy=디지털 도구와 정보를 다루는 능력 / comprehension=내용 이해"),
    ("online etiquette", "온라인 예절 / 디지털 소통 규범", "온라인 상호작용에서 상대를 존중하며 적절하게 행동하는 규범", "화면 뒤에 사람이 있다는 걸 잊지 않고 말과 행동을 조심하는 느낌", "online etiquette=온라인 소통에서의 예절 / protocol=정해진 절차 / courtesy=예의"),
    ("screen time", "화면 사용 시간", "스마트폰·컴퓨터·영상 화면을 보는 데 쓰는 시간", "하루 중 눈과 시간이 화면에 붙잡혀 있는 양", "screen time=화면을 보는 시간 / usage=이용 정도 / exposure=자극이나 영향에 접함"),
    ("scrolling", "스크롤하며 넘겨보기", "화면을 위아래로 밀며 이어진 정보를 훑거나 탐색함", "종이를 넘기는 대신 화면을 손끝으로 밀어 내려가는 느낌", "scrolling=화면을 밀어 이어진 정보를 봄 / browsing=여러 내용을 훑어봄 / searching=목표를 두고 찾음"),
    ("search history", "검색 기록", "이전에 어떤 키워드와 자료를 찾아봤는지 남은 로그", "내가 찾았던 질문의 흔적이 시간순으로 남은 목록", "search history=과거 검색 기록 / browser history=방문한 웹페이지 기록 / archive=보관된 자료"),
    ("source attribution", "출처 표시 / 정보 출처 밝히기", "자료나 아이디어를 어디서 가져왔는지 명시하는 일", "내 말처럼 덮지 않고 정보가 나온 곳의 이름표를 붙이는 느낌", "source attribution=정보 출처를 밝힘 / citation=참고문헌 표기 / acknowledgment=도움·기여를 인정함"),
    ("two-factor", "이중 인증의", "비밀번호 하나만이 아니라 추가 확인 단계를 하나 더 두는 보안 방식의", "문 하나만 여는 게 아니라 두 번째 확인문을 더 거치는 느낌", "two-factor=두 단계 인증을 쓰는 / password-protected=비밀번호로 보호된 / single-step=한 단계만 거치는"),
    ("upload limit", "업로드 제한 용량", "한 번에 올릴 수 있는 파일 크기나 개수의 상한", "더 올리고 싶어도 이 선을 넘으면 막히는 용량 천장", "upload limit=올릴 수 있는 최대 한도 / bandwidth=처리 가능한 용량 / quota=할당된 제한량"),
    ("webinar", "웨비나 / 온라인 세미나", "인터넷으로 진행하며 발표와 질의응답을 포함하는 세미나형 행사", "같은 방에 모이지 않아도 화면을 통해 듣고 묻는 세미나", "webinar=온라인으로 진행되는 세미나 / seminar=대면·일반 세미나 / livestream=실시간 송출"),
    ("version history", "버전 이력 / 수정 기록", "파일이나 문서가 언제 어떻게 바뀌었는지 남긴 이전 버전들의 기록", "고치기 전후 흔적이 단계별로 남아 있어 되돌아볼 수 있는 느낌", "version history=이전 수정 단계들의 기록 / transcript=발언 기록 / backup copy=예비 저장본"),
    ("digital divide", "디지털 격차", "기술과 인터넷 접근·활용 능력에서 집단 간 차이가 벌어진 상태", "누군가는 쉽게 연결되는데 누군가는 문턱 앞에 막히는 차이", "digital divide=디지털 접근·활용의 격차 / inequality=불평등 일반 / accessibility=접근성"),
    ("evidence trail", "근거 흔적 / 추적 가능한 증거선", "판단이나 결론이 어떤 자료와 단계에서 나왔는지 따라갈 수 있게 남은 기록", "결론만 던지는 게 아니라 그 뒤를 따라가면 근거 발자국이 보이는 느낌", "evidence trail=결론까지 이어지는 근거 흔적 / trace=남은 자취 / documentation=문서 기록"),
    ("message thread", "메시지 스레드 / 이어진 대화 묶음", "관련 메시지들이 하나의 흐름으로 연결되어 모인 대화 단위", "흩어진 메시지가 아니라 같은 줄에 달린 대화 가지", "message thread=연결된 대화 묶음 / correspondence=서면 연락 교환 / comment=개별 의견"),
    ("screen capture", "화면 캡처 / 화면 저장 이미지", "현재 화면에 보이는 내용을 이미지로 잡아 저장한 것", "지금 화면을 그대로 얼려서 증거나 참고 자료로 남기는 느낌", "screen capture=화면을 이미지로 저장함 / screenshot=화면 캡처 이미지 / recording=영상으로 녹화함"),
    ("content update", "콘텐츠 업데이트 / 내용 갱신", "자료나 게시물의 정보를 최신 상태로 바꾸는 일", "예전 내용을 그대로 두지 않고 새 정보로 갈아끼우는 느낌", "content update=내용을 최신으로 갱신함 / revision=문서 내용을 고쳐 씀 / upload=새 파일을 올림"),
    ("device syncing", "기기 동기화 / 데이터 맞춤", "여러 기기의 파일이나 설정이 같은 최신 상태로 맞춰지게 함", "폰과 컴퓨터가 서로 다른 버전으로 따로 놀지 않게 맞춰 붙이는 느낌", "device syncing=여러 기기 상태를 맞춤 / backup=복사본 저장 / interoperability=서로 다른 시스템이 함께 작동함"),
    ("data visualization", "데이터 시각화", "수치나 패턴을 그래프·지도·도표로 보여주어 해석을 돕는 일", "숫자표만 보던 것을 눈에 보이는 모양으로 바꿔 읽기 쉽게 하는 느낌", "data visualization=자료를 시각적으로 표현함 / infographic=정보를 요약한 시각 자료 / illustration=설명용 그림"),
    ("remote access", "원격 접속 / 떨어진 곳에서 접근", "현장에 없어도 네트워크를 통해 시스템이나 자료에 들어갈 수 있음", "같은 방에 없지만 온라인 선으로 멀리서 문을 여는 느낌", "remote access=멀리서 네트워크로 접근함 / local access=현장에서 직접 접근함 / connectivity=연결성"),
    ("document sharing", "문서 공유", "같은 파일이나 문서를 여러 사람이 볼 수 있게 보내거나 열어두는 일", "문서를 내 책상에 묶어두지 않고 같이 볼 수 있게 풀어두는 느낌", "document sharing=문서를 다른 사람과 공유함 / file-sharing=파일 공유 / publication=공식 공개"),
    ("revision tracking", "수정 추적 / 변경 이력 관리", "문서나 자료에서 누가 무엇을 어떻게 바꿨는지 따라가며 기록하는 일", "수정이 조용히 사라지지 않고 누가 어디를 바꿨는지 흔적이 남는 느낌", "revision tracking=변경 내용을 따라가며 기록함 / version history=이전 버전 기록 / monitoring=진행 상황을 계속 점검함"),
    ("access log", "접속 기록 / 이용 로그", "누가 언제 시스템이나 자료에 들어왔는지 남은 기록", "문을 드나든 흔적을 시간표처럼 찍어둔 기록", "access log=접속 이력을 남긴 기록 / search history=검색 기록 / profile=사용자 정보 요약"),
    ("auto-save", "자동 저장", "사용자가 따로 저장 버튼을 누르지 않아도 시스템이 변경 내용을 계속 저장하는 기능", "혹시 잊어도 뒤에서 조용히 저장을 챙겨주는 느낌", "auto-save=변경 내용을 자동으로 저장함 / backup copy=예비 복사본 / manual save=직접 저장"),
    ("cross-post", "여러 플랫폼에 같이 올리다", "같은 게시물이나 공지를 한 곳만이 아니라 여러 온라인 채널에 함께 게시하다", "한 군데 올리고 끝내지 않고 여러 창구로 동시에 퍼뜨리는 느낌", "cross-post=여러 플랫폼에 함께 게시함 / repost=다시 올림 / publicize=널리 알림"),
    ("dataset", "데이터셋 / 자료 묶음", "분석이나 검토를 위해 구조화해 모아둔 데이터의 집합", "흩어진 숫자와 항목을 한 묶음으로 모아 분석 가능한 상태로 만든 것", "dataset=분석용으로 묶은 데이터 집합 / database=저장·검색용 데이터 구조 / sample=일부 표본"),
    ("default setting", "기본 설정", "사용자가 따로 바꾸기 전 시스템이 처음부터 적용해 두는 설정값", "아무것도 손대지 않으면 자동으로 깔려 있는 출발 상태", "default setting=처음 적용된 기본값 / preference=사용자 선호 설정 / customization=개별 맞춤 변경"),
    ("digital workflow", "디지털 작업 흐름", "문서 작성·공유·검토·저장이 온라인 도구와 시스템 안에서 이어지는 방식", "종이 대신 화면과 파일 링크를 따라 일이 흘러가는 줄", "digital workflow=온라인 도구 안에서 이어지는 작업 흐름 / workflow=업무 절차 흐름 일반 / collaboration=함께 작업함"),
    ("email thread", "이메일 스레드 / 이어진 메일 대화", "같은 주제의 답장들이 하나의 흐름으로 묶인 메일 대화", "메일이 따로 흩어지지 않고 같은 제목 아래 줄지어 달리는 느낌", "email thread=이어진 메일 대화 묶음 / message thread=이어진 메시지 묶음 / correspondence=서면 연락 교환"),
    ("file format", "파일 형식", "데이터나 문서가 어떤 구조와 규칙으로 저장되는지의 형식", "같은 내용이라도 어떤 그릇에 담겼는지 정하는 저장 모양", "file format=파일이 저장되는 형식 / formatting=문서 서식 맞추기 / template=반복 사용 틀"),
    ("link rot", "링크 소실 / 오래된 링크가 깨짐", "시간이 지나 웹 주소가 바뀌거나 사라져 연결이 작동하지 않게 되는 현상", "예전 문 주소를 눌렀는데 문이 없어져 길이 끊긴 느낌", "link rot=오래된 링크가 깨져 연결이 사라짐 / broken link=작동하지 않는 링크 / archiving=자료를 보관함"),
    ("mobile-friendly", "모바일 친화적인", "작은 화면과 터치 조작에서도 보기 쉽고 쓰기 편하게 맞춰진", "컴퓨터 화면만이 아니라 휴대폰 손끝에도 잘 맞는 느낌", "mobile-friendly=휴대폰 환경에서 쓰기 편한 / responsive=화면 크기에 맞게 반응하는 / desktop=컴퓨터 화면 중심의"),
    ("online forum", "온라인 포럼 / 웹 토론 공간", "인터넷에서 사람들이 질문과 의견을 올리며 논의하는 공개 공간", "같은 방이 아니라 게시판 위에서 생각을 주고받는 장소", "online forum=웹상의 공개 토론 공간 / forum=토론의 장 일반 / message thread=이어진 대화 묶음"),
    ("push alert", "푸시 알림 / 즉시 뜨는 알림", "앱이나 서비스가 새 정보를 사용자 화면에 바로 보내 띄우는 알림", "내가 직접 들어가지 않아도 화면으로 먼저 툭 밀려오는 신호", "push alert=서비스가 먼저 보내는 즉시 알림 / notification=알림 일반 / reminder=다시 상기시키는 알림"),
    ("screen-sharing", "화면 공유", "자기 화면을 다른 사람이 동시에 볼 수 있게 온라인으로 보여주는 기능", "각자 말로 설명하지 않고 같은 화면을 같이 펼쳐 보는 느낌", "screen-sharing=내 화면을 다른 사람에게 보여줌 / file-sharing=파일을 공유함 / livestream=실시간 화면·영상 송출"),
    ("search engine", "검색 엔진", "키워드나 질의를 바탕으로 관련 웹 자료를 찾아주는 시스템", "질문을 던지면 넓은 웹에서 관련 페이지를 끌어와 주는 도구", "search engine=웹 자료를 찾아주는 시스템 / browser=웹페이지를 여는 도구 / database=저장된 자료 구조"),
    ("session timeout", "세션 만료 / 접속 시간 초과", "일정 시간 반응이 없거나 제한 시간을 넘겨 자동으로 접속 상태가 끊기는 일", "오래 가만히 두면 열린 문이 자동으로 다시 닫히는 느낌", "session timeout=시간 초과로 접속 상태가 끊김 / log-out=직접 접속을 종료함 / delay=늦어짐"),
    ("software update", "소프트웨어 업데이트", "프로그램의 기능·보안·오류 수정 내용을 새 버전으로 반영함", "예전 버전을 그대로 쓰지 않고 더 나은 수정본으로 갈아끼우는 느낌", "software update=프로그램을 새 버전으로 갱신함 / patch=특정 문제를 고치는 수정 / upgrade=기능을 더 높은 버전으로 올림"),
    ("text mining", "텍스트 마이닝 / 대량 텍스트 분석", "많은 글 자료에서 반복 패턴이나 유의미한 정보를 자동으로 뽑아내는 분석", "긴 글더미를 사람이 다 읽기 전에 시스템이 패턴을 긁어내는 느낌", "text mining=대량 문서에서 패턴·정보를 추출함 / search=원하는 항목을 찾음 / analysis=자료를 해석함"),
    ("user feedback", "사용자 피드백", "서비스나 자료를 실제로 써본 사람이 보내는 반응과 개선 의견", "만든 쪽이 혼자 판단하지 않고 쓰는 쪽에서 돌아오는 목소리", "user feedback=사용자가 보내는 반응·개선 의견 / evaluation=공식 평가 / comment=개별 의견"),
    ("visual dashboard", "시각적 현황판 / 그래픽 대시보드", "수치와 상태를 그래프·색·배치로 한눈에 보이게 모아둔 화면", "복잡한 숫자를 바로 읽히는 그림판으로 바꿔 보여주는 느낌", "visual dashboard=시각적으로 정리한 현황 화면 / dashboard=요약 현황판 / chart=도표"),
    ("web traffic", "웹 트래픽 / 사이트 방문 흐름", "웹사이트로 들어오고 이동하는 사용자 방문량과 흐름", "사람들이 어느 문으로 들어와 어디로 흘러가는지 보는 온라인 동선", "web traffic=웹사이트 방문 흐름과 규모 / audience=보는 사람 집단 / connectivity=연결 상태"),
    ("zero-click", "클릭 없이 바로 보이는 / 클릭이 필요 없는", "링크를 누르지 않아도 검색 결과나 미리보기에서 정보가 바로 드러나는", "문을 한 번 더 안 열어도 겉 화면에서 답이 바로 보이는 느낌", "zero-click=클릭 없이 정보가 바로 노출됨 / clickthrough=눌러서 다음으로 이동함 / preview=미리보기"),
    ("auditable", "감사·검토 가능한 / 추적 검증 가능한", "과정과 기록이 남아 나중에 기준에 따라 점검할 수 있는", "결과만 던지는 게 아니라 나중에 따라가며 확인할 흔적이 남는 느낌", "auditable=나중에 기록을 따라 검토 가능함 / traceable=경로나 출처를 추적 가능함 / transparent=과정이 드러남"),
    ("cross-device", "여러 기기에서 이어지는", "폰·노트북·태블릿 등 서로 다른 기기에서 같은 작업이나 정보가 연결되는", "장치를 바꿔도 작업 흐름이 끊기지 않고 따라오는 느낌", "cross-device=여러 기기 사이에 이어지는 / wireless=선 없이 연결된 / interoperable=서로 다른 시스템이 함께 작동 가능한"),
    ("digital-first", "디지털 우선의", "종이·오프라인 절차보다 디지털 채널과 온라인 처리를 먼저 기준으로 삼는", "처음 설계부터 화면과 데이터 흐름을 중심에 두는 느낌", "digital-first=디지털 방식을 우선하는 / online=인터넷 연결 상태의 / manual=손작업 중심의"),
    ("file integrity", "파일 무결성 / 손상 없이 유지됨", "파일 내용이 의도치 않게 바뀌거나 깨지지 않고 온전하게 유지되는 상태", "옮기고 저장해도 안쪽 내용이 삐지지 않고 그대로 남는 느낌", "file integrity=파일 내용이 손상 없이 유지됨 / reliability=믿을 만함 / accuracy=정확성"),
    ("information overload", "정보 과부하", "들어오는 정보가 너무 많아 판단과 집중이 오히려 어려워지는 상태", "필요한 걸 고르기 전에 정보가 한꺼번에 쏟아져 머리가 막히는 느낌", "information overload=정보가 너무 많아 처리하기 어려움 / distraction=주의가 분산됨 / confusion=혼란"),
    ("open access", "오픈 액세스 / 자유 접근 가능", "유료 장벽이나 제한 없이 자료를 누구나 읽고 이용할 수 있게 열어둔 상태", "잠긴 문 뒤에 숨기지 않고 필요한 사람에게 자료를 열어둔 느낌", "open access=누구나 자료에 자유롭게 접근 가능함 / public-facing=외부 공개용의 / restricted=제한된"),
    ("platform-wide", "플랫폼 전체에 걸친", "특정 일부 기능이 아니라 서비스나 플랫폼 전체 범위에 적용되는", "한 구석만이 아니라 판 전체를 한꺼번에 덮는 느낌", "platform-wide=플랫폼 전체에 걸친 / local=일부 구역의 / systemwide=전체 시스템에 걸친"),
    ("response time", "응답 시간", "요청을 보낸 뒤 실제 답이나 반응이 돌아오기까지 걸리는 시간", "보낸 신호가 되돌아오는 데 얼마를 기다려야 하는지 보는 느낌", "response time=요청 후 반응이 돌아오는 시간 / latency=기술적 지연 시간 / turnaround=처리해서 돌려주는 소요 시간"),
    ("shareable link", "공유 가능한 링크", "다른 사람이 같은 자료나 페이지를 열 수 있게 전달할 수 있는 웹 주소", "파일 설명 대신 그 자료로 바로 들어가는 문 주소를 건네는 느낌", "shareable link=남에게 보낼 수 있는 접근 링크 / hyperlink=웹상 연결 링크 / file-sharing=파일 자체 공유"),
    ("version control", "버전 관리 / 수정 이력 제어", "파일이나 코드의 변경 단계를 추적하고 필요하면 이전 상태로 되돌릴 수 있게 관리하는 방식", "고쳐도 흔적이 남아 어느 버전인지 줄을 잡고 있는 느낌", "version control=변경 이력을 관리하고 되돌림 가능함 / version history=이전 수정 단계 기록 / backup copy=예비 복사본"),
    ("web interface", "웹 인터페이스 / 온라인 조작 화면", "사용자가 브라우저에서 기능과 데이터를 보고 조작하는 화면과 접점", "시스템 안쪽이 아니라 사람이 웹에서 마주하는 조작 창구", "web interface=웹에서 만나는 조작 화면 / interface=접점 일반 / dashboard=현황을 모은 화면"),
]


def build_back(core: str, extra: str, feeling: str, distinction: str) -> str:
    return "\n".join([f"핵심 뜻: {core}", f"부가 뜻: {extra}", f"핵심 느낌: {feeling}", f"구분: {distinction}"])


def main() -> None:
    existing = set()
    for path in sorted(ROOT.glob("toefl_ets_2026_set_*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.reader(f, delimiter="\t"):
                if row:
                    existing.add(row[0].strip())

    rows = []
    seen = set()
    for word, core, extra, feeling, distinction in CARDS:
        if word in existing or word in seen:
            continue
        rows.append([word, build_back(core, extra, feeling, distinction)])
        seen.add(word)
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
        manifest["files_created"].insert(14, TARGET.name)
    manifest["total_ets_cards"] = len(ets_words)
    manifest["timestamp"] = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{TARGET.name}: {len(rows)} cards")


if __name__ == "__main__":
    main()
