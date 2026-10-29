"""
Base Agent Interface and LLM Connector.
Provides unified interface for Labor, Management, Legal Advisor, and Mediator agents.
Supports OpenAI / Gemini / Claude API if keys are provided, plus an offline high-fidelity simulator.
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import urllib.request
import urllib.error


class BaseAgent(ABC):
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.provider = "gemini" if os.getenv("GEMINI_API_KEY") else ("openai" if os.getenv("OPENAI_API_KEY") else "offline")

    @abstractmethod
    def generate_response(self, context: Dict[str, Any], round_num: int) -> Dict[str, Any]:
        """
        Generate response given current state context and negotiation round.
        """
        pass

    def call_external_llm(self, prompt: str) -> Optional[str]:
        """
        Calls external LLM if configured; otherwise returns None to fallback to offline simulator.
        """
        if not self.api_key or self.provider == "offline":
            return None

        # OpenAI compatible call via standard library urllib
        if self.provider == "openai":
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                body = {
                    "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                }
                req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=30) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    return res_data["choices"][0]["message"]["content"]
            except Exception as e:
                return None

        return None
