"""
LLM Manager - Ollama와의 통신을 담당
모든 모듈은 이 매니저를 통해서만 LLM에 접근합니다.
"""

import requests
import yaml


class LLMManager:
    def __init__(self, config_path="config/settings.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.model = config["llm"]["model"]
        self.base_url = config["llm"]["base_url"]
        self.temperature = config["llm"]["temperature"]
        self.max_tokens = config["llm"]["max_tokens"]

    def generate(self, prompt, system_prompt=None):
        """단일 프롬프트로 응답 생성"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"LLM 연결 오류: {str(e)}"

    def chat(self, messages):
        """다중 턴 대화 (대화 기록 포함)"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"LLM 연결 오류: {str(e)}"
