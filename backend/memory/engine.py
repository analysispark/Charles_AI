import os
import datetime
from typing import List, Dict

class MemoryEngine:
    def __init__(self):
        self.memory_dir = "Memory"
        self.raw_dir = os.path.join(self.memory_dir, "RAW")
        
        # Create directories if they don't exist
        os.makedirs(self.raw_dir, exist_ok=True)
    
    def save_conversation(self, conversation_history: List[Dict], project_name: str = "Unknown"):
        """Save raw conversation to Memory/RAW"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}_conversation.md"
        filepath = os.path.join(self.raw_dir, filename)
        
        with open(filepath, 'w') as f:
            for msg in conversation_history:
                f.write(f"{msg['role']}: {msg['content']}\n")
        
        return filepath
