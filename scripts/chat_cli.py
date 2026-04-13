"""터미널에서 chat 모듈을 빠르게 검증하는 프로토타입 스크립트."""

from modules.chat.service import ChatService


def main():
    service = ChatService()

    print("개인 AI 비서 프로토타입 (종료: /exit, 메모리 초기화: /reset)")
    while True:
        user_input = input("\nYou> ").strip()

        if user_input == "/exit":
            print("Assistant> 다음에 또 만나요!")
            break

        if user_input == "/reset":
            result = service.reset_memory()
            print(f"Assistant> {result['response']}")
            continue

        result = service.process({"query": user_input, "context": {"channel": "cli"}})
        print(f"Assistant> {result['response']}")


if __name__ == "__main__":
    main()
