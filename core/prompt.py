"""
Prompt Manager - 시스템 프롬프트를 관리
"""

import os


class PromptManager:
    def __init__(self, prompts_dir="modules"):
        self.prompts_dir = prompts_dir
        self.default_prompt = self._load_default_prompt()

    def _load_default_prompt(self):
        return """당신은 사용자의 개인 AI 비서입니다.

## 핵심 원칙
- 질문에 정확하고 도움이 되는 답변을 제공합니다.
- 한국어로 자연스럽게 대화합니다.
- 모르는 것은 모른다고 솔직하게 말합니다.
- 간결하면서도 충분한 정보를 제공합니다.

## 응답 스타일
- 친근하지만 전문적인 톤을 유지합니다.
- 필요한 경우 단계별로 설명합니다.
- 사용자의 의도를 파악하여 최적의 답변을 제공합니다."""

    def get_system_prompt(self, module_name=None):
        if module_name:
            prompt_path = os.path.join(
                self.prompts_dir, module_name, "prompts", "system.txt"
            )
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    return f.read()
        return self.default_prompt

    def update_default_prompt(self, new_prompt):
        self.default_prompt = new_prompt
