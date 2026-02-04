[Week 3] AI Agent MITM & Response Poisoning


1. 실습 개요
본 실습은 AI 에이전트(agent_b)와 도구 서버(tool_server) 간의 통신 과정을 가로채 데이터를 변조하는 MITM(Man-in-the-Middle) 공격을 수행한다. 이를 통해 에이전트의 의도와 관계없이 공격자가 원하는 민감한 데이터(passwd.txt)를 탈취하는 Response Poisoning(또는 Parameter Tampering) 과정을 학습한다.



2. 실습 환경 구성
Docker 컨테이너: agent_a, agent_b, tool_server 세 개의 서비스로 구성한다.

Proxy 설정: 에이전트 간 통신 및 서버 통신을 분석하기 위해 Burp Suite를 Proxy 서버로 설정한다.

데이터 마운트: 로컬의 data 폴더를 도커 컨테이너의 /data 경로에 볼륨 마운트하여 실시간 파일 읽기가 가능하도록 설정한다.



3. 취약점 분석
서버 측 결함: 기존 tool_server.py는 특정 문자열만 반환하도록 하드코딩되어 있어, 실제 파일 읽기 로직이 부재하였다.

에이전트 측 결함: agent_b가 사용자 프롬프트를 해석하여 도구를 호출할 때, 명확한 path 인자를 생성하지 못하고 "text" 필드에 경로를 포함하여 전송하는 현상이 발생한다.

보안 결함: 서버가 클라이언트로부터 전달받은 파일 경로(path)에 대해 화이트리스트 검증을 수행하지 않아, 공격자가 임의의 경로에 접근할 수 있는 취약점이 존재한다.



4. 공격 수행 과정
서버 코드 수정: tool_server.py가 전달받은 path 인자를 기반으로 실제 시스템 파일을 읽어오도록 로직을 수정한다.

패킷 가로채기: Burp Suite의 Intercept 기능을 활성화하여 agent_b에서 tool_server:8001/tool로 향하는 HTTP POST 요청을 가로챈다.

데이터 변조: Burp Suite Repeater 기능을 활용하여 요청 본문의 JSON 데이터를 수정한다.
<img width="866" height="1012" alt="변조 전" src="https://github.com/user-attachments/assets/6f9a9f14-4dac-4524-aaad-3cb64e535e2c" />

변조 전: {"args": {"text": "read file"}}
<img width="881" height="1012" alt="변조 후" src="https://github.com/user-attachments/assets/b9ac5e2c-5384-400b-aeec-69ffa0929a92" />

변조 후: {"args": {"path": "/data/passwd.txt"}}

결과 확인: 변조된 패킷을 전송하여 서버로부터 /data/passwd.txt의 내용을 응답으로 반환받는 데 성공한다.



5. 실습 결과
정상 통신: 에이전트가 /data/hello.txt를 호출하여 정상적인 인사말을 출력함을 확인하였다.

공격 성공: 변조된 경로 파라미터를 통해 민감한 정보가 포함된 passwd.txt 파일의 내용을 탈취 완료하였다.
