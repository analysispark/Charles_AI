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
        
        # Create directories if they don't exist
        for directory in [self.raw_dir, self.summaries_dir, self.decisions_dir]:
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
        
        prompt = f"""Please provide a concise summary of the following conversation:

{conversation_text}

Focus only on actual project goals, implementation progress, completed work, accepted decisions, and next planned actions. Ignore placeholder text, testing messages, debugging messages, temporary examples, AI self-references, and implementation artifacts.

Write only persistent project memory in bullet point format with maximum 5 bullet points:

# Summary

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
        
        prompt = f"""You are a Decision Extraction Engine.

Extract ONLY decisions that were explicitly accepted, chosen, approved, or agreed upon. Do NOT infer, guess, invent, or convert technical facts into decisions unless they were explicitly accepted.

Examples of valid decisions:
- Use qwen3:8b as the memory model
- Keep chat functionality unchanged
- Store memory in markdown files
- Separate Memory Engine from chat flow
- Use dedicated memory folders

Examples of invalid decisions:
- Generic technical facts
- AI-generated assumptions
- Unaccepted recommendations
- Future possibilities
- Speculation
- Implementation ideas that were never agreed upon

Extract only the explicitly accepted decisions from this conversation:

{conversation_text}

If no decisions exist, return: "No decisions identified."

Format each decision as:

# D-0001

Decision:
<decision>

Reason:
<reason>

Status:
Accepted"""

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
