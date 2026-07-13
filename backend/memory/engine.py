import os
import datetime
import json
from typing import List, Dict
from .writer import MemoryWriter
from ..ollama_client import OllamaClient

class MemoryEngine:
    def __init__(self):
        self.memory_dir = "Memory"
        self.raw_dir = os.path.join(self.memory_dir, "RAW")
        self.summaries_dir = os.path.join(self.memory_dir, "Summaries")
        self.decisions_dir = os.path.join(self.memory_dir, "Decisions")
        self.insights_dir = os.path.join(self.memory_dir, "Insights")
        self.tasks_dir = os.path.join(self.memory_dir, "Tasks")
        
        # Create directories if they don't exist
        for directory in [self.raw_dir, self.summaries_dir, self.decisions_dir, self.insights_dir, self.tasks_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def save_conversation(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Save raw conversation to Memory/RAW"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_conversation.md"
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w') as f:
            for msg in conversation_history:
                f.write(f"{msg['role']}: {msg['content']}\n")
        
        return filepath
    
    def generate_summary(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Generate summary from conversation history using Ollama"""
        # Read memory model from config
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                memory_model = config["ollama"]["memory_model"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to default model if config not found
            memory_model = "qwen3-coder:30b"
        
        # Create prompt for Ollama
        conversation_text = ""
        for msg in conversation_history:
            conversation_text += f"{msg['role']}: {msg['content']}\n"
        
        prompt = f"""다음 대화의 간결한 요약을 제공해주세요:

{conversation_text}

플레이스홀더 텍스트, 테스트 메시지, 디버깅 메시지, 임시 예제, AI 자기 참조 및 구현 아티팩트를 무시하세요.

프로젝트 목표, 구현 진행 상황, 완료된 작업, 승인된 결정 및 다음 행동 계획만을 집중적으로 작성하세요.

지속 가능한 프로젝트 메모리만을 점포 형식으로 최대 5개의 항목으로 작성하세요:

# 요약

- ...
- ...
- ..."""

        # Send to Ollama using existing client with specified model
        client = OllamaClient(model=memory_model)
        summary = client.send_message(prompt)
        
        # Save summary to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_summary.md"
        filepath = os.path.join(self.summaries_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [summary, project-planning]\n")
            f.write("---\n\n")
            f.write(summary)
        
        return filepath
    
    def generate_decisions(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Generate decisions from conversation history using Ollama"""
        # Read memory model from config
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                memory_model = config["ollama"]["memory_model"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to default model if config not found
            memory_model = "qwen3-coder:30b"
        
        # Create prompt for Ollama
        conversation_text = ""
        for msg in conversation_history:
            conversation_text += f"{msg['role']}: {msg['content']}\n"
        
        prompt = f"""당신은 결정 추출 엔진입니다.

명시적으로 승인, 선택, 승인 또는 합의된 결정만을 추출하세요. 추측, 추론, 창의적 생성 또는 기술 사실을 결정으로 전환하지 마세요.

결정 예시:
- qwen3:8b를 메모리 모델로 사용
- 채팅 기능 유지
- 마크다운 파일에 메모리 저장
- 메모리 엔진과 채팅 흐름 분리
- 전용 메모리 폴더 사용

결정이 아닌 예시:
- 일반적인 기술 사실
- AI 생성 가정
- 승인되지 않은 권고
- 미래 가능성
- 추측
- 승인되지 않은 구현 아이디어

이 대화에서 명시적으로 승인된 결정만을 추출하세요:

{conversation_text}

결정이 없으면: "결정이 없습니다."를 반환하세요.

각 결정은 다음과 같은 형식으로 작성하세요:

# D-0001

결정:
<결정>

근거:
<근거>

상태:
승인됨"""

        # Send to Ollama using existing client with specified model
        client = OllamaClient(model=memory_model)
        decisions = client.send_message(prompt)
        
        # Save decisions to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_decisions.md"
        filepath = os.path.join(self.decisions_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [decision, architecture]\n")
            f.write("---\n\n")
            f.write(decisions)
        
        return filepath
    
    def generate_insights(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Generate insights from conversation history using Ollama"""
        # Read memory model from config
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                memory_model = config["ollama"]["memory_model"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to default model if config not found
            memory_model = "qwen3:8b"
        
        # Create prompt for Ollama
        conversation_text = ""
        for msg in conversation_history:
            conversation_text += f"{msg['role']}: {msg['content']}\n"
        
        prompt = f"""당신은 장기 메모리 통찰 엔진입니다.

대화에서 최대 3개의 안정적인 사용자 선호도를 추출하세요.

다음만을 식별하세요:
- 사용자 선호도
- 작업 방식

다음은 하지 마세요:
- 대화 요약
- 이벤트 설명
- 결정 반복
- 개발 철학 분석
- 결정 패턴 분석

대화:
{conversation_text}

출력 형식:

# I-0001

통찰:
...

근거:
...

최대 3개의 통찰만.

없는 경우 다음을 반환하세요:

식별된 통찰이 없습니다."""

        # Send to Ollama using existing client with specified model
        client = OllamaClient(model=memory_model)
        insights = client.send_message(prompt)
        
        # Save insights to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_insights.md"
        filepath = os.path.join(self.insights_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [insight, architecture]\n")
            f.write("---\n\n")
            f.write(insights)
        
        return filepath
    
    def generate_tasks(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Generate tasks from conversation history using Ollama"""
        # Read memory model from config
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                memory_model = config["ollama"]["memory_model"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to default model if config not found
            memory_model = "qwen3:8b"
        
        # Create prompt for Ollama
        conversation_text = ""
        for msg in conversation_history:
            conversation_text += f"{msg['role']}: {msg['content']}\n"
        
        prompt = f"""당신은 작업 추출 엔진입니다.

대화에서 작업 가능한 작업만을 추출하세요.

작업이어야 하는 조건:
- 미완료
- 작업 가능
- 명시적 또는 암시적으로 명시됨

다음은 포함하지 마세요:
- 완료된 작업
- 결정
- 통찰
- 가정

대화:
{conversation_text}

작업이 없으면:
"식별된 작업이 없습니다."를 반환하세요.

출력 형식:

# T-0001

작업:
...

상태:
todo

우선순위:
high"""

        # Send to Ollama using existing client with specified model
        client = OllamaClient(model=memory_model)
        tasks = client.send_message(prompt)
        
        # Save tasks to file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_tasks.md"
        filepath = os.path.join(self.tasks_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [task, planning]\n")
            f.write("---\n\n")
            f.write(tasks)
        
        return filepath
