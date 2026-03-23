from typing import List

CONTEXT_WINDOW = 5


class Memory:
    def __init__(self) -> None:
        self._messages: List[dict] = []

    def add_user(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_ai(self, text: str) -> None:
        self._messages.append({"role": "assistant", "content": text})

    def clear(self) -> None:
        self._messages.clear()

    def get_context(self) -> str:
        recent = self._messages[-CONTEXT_WINDOW:]
        return "".join(
            f"{m['role']}: {m['content']}\n" for m in recent
        )


# Singleton — existing code imports these functions directly
_default = Memory()

add_user = _default.add_user
add_ai = _default.add_ai
clear = _default.clear
get_context = _default.get_context