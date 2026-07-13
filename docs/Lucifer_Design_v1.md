# Lucifer_Design_v1.md

Version: 1.0
Status: Draft
Owner: 박지훈
Project: Lucifer AI
Last Updated: 2026-07-13

---

# 1. Vision

Lucifer는 개인 연구실을 위한 AI 기반 Second Brain이다.

Lucifer는 단순한 챗봇이 아니다.

Lucifer의 목적은 다음과 같다.

- 사용자의 지식을 지속적으로 축적한다.
- 사용자의 연구 활동을 지원한다.
- 사용자의 프로젝트를 이해한다.
- 사용자의 문서를 활용하여 답변한다.
- 사용자의 외부 기억장치(Second Brain) 역할을 수행한다.

Lucifer는 PDF를 기억하지 않는다.

Lucifer는 "지식"을 기억한다.

모든 지식은 Markdown 형태로 저장된다.

---

# 2. Design Philosophy

## Principle 1

Lucifer는 모델 중심이 아니라 Knowledge 중심이다.

잘 정리된 지식이 강력한 모델보다 중요하다.

---

## Principle 2

모든 저장 데이터는 Markdown으로 관리한다.

특정 데이터베이스에 종속되지 않는다.

---

## Principle 3

모든 기능은 점진적으로 추가한다.

작동하는 작은 시스템을 먼저 만들고,
이후 기능을 확장한다.

---

## Principle 4

사용자와 Lucifer는 대화를 통해 상호작용한다.

사용자는 기술적인 명령보다 자연어를 사용한다.

예)

"루시퍼, 오늘 회의록 정리해줘."

"루시퍼, DEXA 관련 논문 찾아줘."

"루시퍼, 다음 주 수업 아이디어를 정리해줘."

---

# 3. Current Starting Point

현재 구축 완료 상태

- Linux Server
- Ollama 설치 완료
- 모델 다운로드 완료
- Charles_Vault 생성 완료
- Aider 사용 가능

현재 설계 범위에서 제외

- Qdrant
- Embedding
- Chunking
- Vector Database
- RAG

위 항목은 고려하지 않는다.

---

# 4. System Architecture

사용자

↓

Lucifer Web UI

↓

Lucifer Backend

↓

Ollama

↓

Model

(Qwen / DeepSeek / Gemma)

---

향후

사용자

↓

Lucifer Web UI

↓

Lucifer Backend

↓

Lucifer Vault Engine

↓

Charles_Vault

↓

Ollama

↓

Model

형태로 발전한다.

---

# 5. Charles_Vault Structure

현재 고정 구조

Charles_Vault/

- Paper/
- Topic/
- Person/
- Project/
- Meeting/
- Note/
- Skill/

구조 변경은 추후 검토 전까지 하지 않는다.

---

# 6. Development Roadmap

## Phase 1

Lucifer Core Chat

목표

브라우저에서 AI와 대화 가능

구현 항목

- 채팅 UI
- Ollama 연결
- 모델 응답 출력

구현 제외

- Voice
- Vault 검색
- 파일 저장
- 문서 분석

성공 기준

사용자가

"안녕"

입력

↓

모델 응답 출력

---

## Phase 2

Model Management

목표

모델 변경 가능

예)

- Qwen
- DeepSeek
- Gemma

구현 항목

- 모델 선택 드롭다운
- 기본 모델 설정
- 현재 모델 표시

---

## Phase 3

Vault Awareness

목표

Lucifer가 Vault 구조를 인식한다.

예)

"현재 어떤 폴더가 있어?"

↓

Paper
Topic
Project
Meeting
Note
Skill

출력

구현 범위

파일 읽기 없음

폴더 존재 확인만

---

## Phase 4

Vault Reading

목표

Markdown 문서 읽기

예)

"Project 폴더 보여줘"

"Meeting 폴더 보여줘"

"Charles_AI.md 읽어줘"

구현 범위

읽기 전용

쓰기 기능 없음

---

## Phase 5

Voice Input

목표

음성 입력

기술 후보

- Whisper
- Faster-Whisper

예)

마이크 버튼

↓

음성

↓

텍스트 변환

↓

Lucifer 질문

---

## Phase 6

Voice Output

목표

음성 응답

기술 후보

- Piper
- Coqui
- Edge TTS

예)

Lucifer 답변

↓

음성 출력

---

## Phase 7

Vault Integration

목표

Lucifer가 Vault를 이해한다.

예)

"DEXA 관련 자료 찾아줘"

↓

Topic 탐색

↓

Paper 탐색

↓

관련 정보 제공

---

# 7. Technical Stack

Frontend

- HTML
- CSS
- JavaScript

초기 버전에서는 React 사용하지 않는다.

이유

빠른 개발
단순성
유지보수 용이성

---

Backend

- FastAPI

---

LLM

- Ollama

지원 예정 모델

- Qwen
- DeepSeek
- Gemma

---

# 8. Folder Structure

Lucifer/

├── backend/
│
├── frontend/
│
├── config/
│
├── logs/
│
├── data/
│
├── docs/
│
└── tests/

---

# 9. Configuration Rules

모든 설정값은 코드에 하드코딩하지 않는다.

설정 파일 사용.

예)

config/settings.json

또는

config/config.yaml

---

포함 항목

- Default Model
- Ollama Host
- Port
- UI Settings

---

# 10. Coding Rules

Aider는 항상 아래 규칙을 따른다.

1.

전체 구조를 우선 구현한다.

기능 추가보다 구조를 우선한다.

---

2.

확장 가능한 방식으로 작성한다.

임시 코드 금지.

---

3.

Backend / Frontend 분리한다.

---

4.

모든 기능은 모듈화한다.

---

5.

로그를 남긴다.

---

6.

설정값은 config에서 관리한다.

---

7.

하드코딩 금지

---

# 11. Out Of Scope

현재 절대 구현하지 않는다.

- Qdrant
- Embedding
- Chunking
- RAG
- PostgreSQL
- MongoDB
- Multi-Agent
- Autonomous Agent
- Knowledge Graph 자동 생성

위 기능은 Lucifer v1 범위 밖이다.

---

# 12. Definition of Success

Lucifer v1 성공 조건

1.

브라우저 접속 가능

2.

채팅 가능

3.

Ollama 응답 가능

4.

모델 변경 가능

5.

안정적으로 실행 가능

그 외 기능은 이후 버전에서 구현한다.

---

End of Lucifer_Design_v1
