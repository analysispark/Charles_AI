import os
import datetime
from typing import List, Dict
from .ollama_client import chat_with_ollama

class MemoryEngine:
    def __init__(self):
        self.memory_dir = "Memory"
        self.raw_dir = os.path.join(self.memory_dir, "RAW")
        self.summaries_dir = os.path.join(self.memory_dir, "Summaries")
        self.decisions_dir = os.path.join(self.memory_dir, "Decisions")
        self.insights_dir = os.path.join(self.memory_dir, "Insights")
        self.tasks_dir = os.path.join(self.memory_dir, "Tasks")
        
        # Create directories if they don't exist
        for directory in [self.raw_dir, self.summaries_dir, self.decisions_dir, 
                         self.insights_dir, self.tasks_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def generate_memory_from_conversation(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Generate all memory types from conversation history using Ollama"""
        
        # Save raw conversation
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_conversation.md"
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w') as f:
            for msg in conversation_history:
                f.write(f"{msg['role']}: {msg['content']}\n")
        
        # Generate content using Ollama
        summary = self._generate_summary(conversation_history)
        decisions = self._generate_decisions(conversation_history)
        insights = self._generate_insights(conversation_history)
        tasks = self._generate_tasks(conversation_history)
        
        # Save generated files
        summary_filepath = self._save_summary(summary, timestamp, project_name)
        decisions_filepath = self._save_decisions(decisions, timestamp, project_name)
        insights_filepath = self._save_insights(insights, timestamp, project_name)
        tasks_filepath = self._save_tasks(tasks, timestamp, project_name)
        
        return {
            "raw": filepath,
            "summary": summary_filepath,
            "decisions": decisions_filepath,
            "insights": insights_filepath,
            "tasks": tasks_filepath
        }
    
    def _generate_summary(self, conversation_history: List[Dict]) -> str:
        """Generate summary using Ollama"""
        prompt = f"Please provide a concise summary of the following conversation:\n\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "\nSummary:"
        
        return chat_with_ollama([{"role": "user", "content": prompt}])
    
    def _generate_decisions(self, conversation_history: List[Dict]) -> List[str]:
        """Generate decisions using Ollama"""
        prompt = f"Based on the following conversation, extract key decisions made:\n\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "\nPlease list the decisions in the format 'D-0001: Decision description' and return as a list."
        
        response = chat_with_ollama([{"role": "user", "content": prompt}])
        # In a real implementation, this would parse the response into a proper list
        return [response]  # Placeholder - would be parsed properly
    
    def _generate_insights(self, conversation_history: List[Dict]) -> List[str]:
        """Generate insights using Ollama"""
        prompt = f"Based on the following conversation, extract key insights about user preferences and behavior:\n\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "\nPlease list the insights in bullet point format."
        
        response = chat_with_ollama([{"role": "user", "content": prompt}])
        # In a real implementation, this would parse the response into a proper list
        return [response]  # Placeholder - would be parsed properly
    
    def _generate_tasks(self, conversation_history: List[Dict]) -> List[str]:
        """Generate tasks using Ollama"""
        prompt = f"Based on the following conversation, extract action items and tasks:\n\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += "\nPlease list the tasks with status tracking (todo, in-progress, completed) in the format 'T-0001: Task description (Status: todo)' and return as a list."
        
        response = chat_with_ollama([{"role": "user", "content": prompt}])
        # In a real implementation, this would parse the response into a proper list
        return [response]  # Placeholder - would be parsed properly
    
    def _save_summary(self, summary: str, timestamp: str, project_name: str) -> str:
        """Save summary to markdown file"""
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
    
    def _save_decisions(self, decisions: List[str], timestamp: str, project_name: str) -> str:
        """Save decisions to markdown file"""
        filename = f"{timestamp}_decisions.md"
        filepath = os.path.join(self.decisions_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [decision, architecture]\n")
            f.write("---\n\n")
            for decision in decisions:
                f.write(f"{decision}\n")
        
        return filepath
    
    def _save_insights(self, insights: List[str], timestamp: str, project_name: str) -> str:
        """Save insights to markdown file"""
        filename = f"{timestamp}_insights.md"
        filepath = os.path.join(self.insights_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [insight, architecture]\n")
            f.write("---\n\n")
            for insight in insights:
                f.write(f"- {insight}\n")
        
        return filepath
    
    def _save_tasks(self, tasks: List[str], timestamp: str, project_name: str) -> str:
        """Save tasks to markdown file"""
        filename = f"{timestamp}_tasks.md"
        filepath = os.path.join(self.tasks_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("---\n")
            f.write(f"date: {timestamp}\n")
            f.write(f"project: {project_name}\n")
            f.write("source: Conversation\n")
            f.write("tags: [task, planning]\n")
            f.write("---\n\n")
            for task in tasks:
                f.write(f"{task}\n")
        
        return filepath
