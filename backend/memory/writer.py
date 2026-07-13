import os
import datetime
from typing import List, Dict

class MemoryWriter:
    def __init__(self):
        self.memory_dir = "Memory"
        self.summaries_dir = os.path.join(self.memory_dir, "Summaries")
        self.decisions_dir = os.path.join(self.memory_dir, "Decisions")
        self.insights_dir = os.path.join(self.memory_dir, "Insights")
        self.tasks_dir = os.path.join(self.memory_dir, "Tasks")
    
    def save_summary(self, summary: str, timestamp: str, project_name: str) -> str:
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
    
    def save_decisions(self, decisions: str, timestamp: str, project_name: str) -> str:
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
            f.write(decisions)
        
        return filepath
    
    def save_insights(self, insights: str, timestamp: str, project_name: str) -> str:
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
            f.write(insights)
        
        return filepath
    
    def save_tasks(self, tasks: str, timestamp: str, project_name: str) -> str:
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
            f.write(tasks)
        
        return filepath
