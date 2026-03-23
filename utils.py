import re


def detect_lang(text: str) -> str:
    """Heuristically detect the programming language in a code snippet."""
    checks = [
        (["#include", "std::"], "cpp"),
        (["import java.", "public class", "System.out.print"], "java"),
        (["def ", "@app.", "import os", "import re"], "python"),
        (["console.log", "const ", "let ", "=>", "require(", "module.exports"], "javascript"),
        (["interface ", ": string", ": number", ": boolean", "tsx", "React.FC"], "typescript"),
        (["func ", "fmt.Println", "package main"], "go"),
        (["fn ", "let mut", "println!", "impl "], "rust"),
        (["<!DOCTYPE", "<html", "<div", "<body"], "html"),
    ]
    for keywords, lang in checks:
        if any(k in text for k in keywords):
            return lang
    return "text"


def clean_code(text: str) -> str:
    """Strip markdown fenced code blocks and trailing artefacts."""
    text = text.strip()
    # Remove opening fence: ```python, ```js, ``` etc.
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    # Remove closing fence
    text = re.sub(r"\n?```$", "", text)
    # Remove stray closing brace followed by period (LLM artefact)
    text = text.replace("}.", "}")
    return text.strip()


def is_code(text: str) -> bool:
    """Return True if the text looks like a code snippet."""
    code_signals = [
        "def ", "class ", "function ", "const ", "let ", "var ",
        "=>", "#include", "import ", "package ", "fn ", "func ",
        "System.out", "console.log",
    ]
    return any(sig in text for sig in code_signals)