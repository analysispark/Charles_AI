import requests
import json
from typing import Optional

class OllamaClient:
    def __init__(self, host: str = "localhost", port: int = 11434, model: str = "qwen3-coder:30b"):
        self.host = host
        self.port = port
        self.model = model
        self.base_url = f"http://{host}:{port}"
    
    def send_message(self, message: str) -> str:
        try:
            payload = {
                "model": self.model,
                "prompt": message,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {str(e)}")
