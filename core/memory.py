"""
Memory Manager - 대화 기록을 관리
단기 메모리: 현재 대화 세션의 기록 (RAM)
장기 메모리: 과거 대화 저장 (DB로 확장 예정)
"""


class MemoryManager:
    def __init__(self, max_history=20):
        self.max_history = max_history
        self.history = []

    def add_message(self, role, content):
        """role: 'user' 또는 'assistant'"""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2) :]

    def get_history(self):
        return self.history.copy()

    def clear(self):
        self.history = []

    def get_context_messages(self, system_prompt):
        """시스템 프롬프트 + 대화 기록을 합쳐 반환"""
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history)
        return messages
