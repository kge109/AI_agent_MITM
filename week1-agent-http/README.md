Week 1: Agent HTTP Communication & Packet Analysis


1. 개요

목적: Docker 환경에서 두 Agent 간의 HTTP 통신 구현 및 패킷 분석
환경: Docker Desktop, Docker Compose, PyCharm, Wireshark
대상: Agent A (Client / 172.18.0.2), Agent B (Server / 172.18.0.3)


2. 프로젝트 구조

week1/
├── agent_a/ (Client)
│   ├── agent_a.py
│   └── Dockerfile
├── agent_b/ (Server)
│   ├── agent_b.py
│   └── Dockerfile
└── docker-compose.yml


3. 실행 방법

# 컨테이너 빌드 및 실행
docker-compose up --build


4. 통신 결과 및 패킷 분석
[터미널에서 Docker 실행 로그 확인]
<img width="725" height="164" alt="스크린샷 2026-01-05 오후 8 41 11" src="https://github.com/user-attachments/assets/a842f6b8-276a-435d-989b-bf43198bc849" />

내용: Agent A가 Agent B에게 read_file 도구 호출 요청을 보내고, 정상 응답(200 OK)을 수신함.
확인 사항: Agent B의 수신 로그와 Agent A의 서버 응답 JSON 데이터 일치 여부.

[Wireshark 패킷 캡처 및 JSON 페이로드]
<img width="1656" height="469" alt="스크린샷 2026-01-05 오후 9 24 43" src="https://github.com/user-attachments/assets/261978af-5054-43a1-b827-e7410a03d526" />

분석 도구: tcpdump로 .pcap 추출 후 Wireshark 분석
분석 결과: POST /tool HTTP/1.1 요청 내에서 JSON 페이로드(tool: read_file, path: /hello.txt)가 **평문(Plaintext)**으로 노출됨.


5. 보안 취약점 분석 (Week 1 결론)

현재 Agent 간 통신에 암호화(HTTPS/TLS)가 적용되지 않아 네트워크 도청 시 AI Agent의 도구 호출 의도와 파라미터가 실시간으로 노출됨.
이는 향후 진행할 MITM(중간자 공격) 환경에서 공격자가 데이터를 탈취하거나 위변조하기 매우 쉬운 상태임을 시사함.
