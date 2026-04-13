"""Chat Service - chat 모듈의 대화 처리 핵심 로직."""

from core.llm import LLMManager
from core.memory import MemoryManager
from core.prompt import PromptManager


class ChatService:
    """
    ChatService는 세 가지 매니저를 오케스트레이션합니다.

    - PromptManager: chat 모듈용 시스템 프롬프트 로드
    - MemoryManager: 대화 이력 관리
    - LLMManager: Ollama 모델과 통신
    """

    def __init__(
        self,
        llm_manager=None,
        memory_manager=None,
        prompt_manager=None,
    ):
        # 테스트/확장을 위해 의존성을 주입할 수 있게 구성
        self.llm = llm_manager or LLMManager()
        self.memory = memory_manager or MemoryManager()
        self.prompt = prompt_manager or PromptManager()

    def process(self, payload):
        """
        공통 입출력 스펙에 맞춰 대화 요청을 처리합니다.

        입력 예시:
            {"query": "안녕", "context": {...}}

        출력 예시:
            {"response": "...", "data": {...}}
        """
        user_query = (payload or {}).get("query", "").strip()
        context = (payload or {}).get("context", {})

        if not user_query:
            return {
                "response": "질문이 비어 있어요. query에 질문을 넣어 주세요.",
                "data": {"error": "empty_query"},
            }

        # 1) 모듈 전용 시스템 프롬프트 로드
        system_prompt = self.prompt.get_system_prompt("chat")

        # 2) 이전 대화 이력 + 현재 유저 메시지 구성
        messages = self.memory.get_context_messages(system_prompt)
        messages.append({"role": "user", "content": user_query})

        # 3) LLM 호출
        assistant_reply = self.llm.chat(messages)

        # 4) 메모리 업데이트 (사용자/어시스턴트 순서 보관)
        self.memory.add_message("user", user_query)
        self.memory.add_message("assistant", assistant_reply)

        return {
            "response": assistant_reply,
            "data": {
                "module": "chat",
                "history_count": len(self.memory.get_history()),
                "context": context,
            },
        }

    def reset_memory(self):
        """현재 세션의 대화 기록을 초기화합니다."""
        self.memory.clear()
        return {"response": "대화 기록을 초기화했어요.", "data": {"cleared": True}}
