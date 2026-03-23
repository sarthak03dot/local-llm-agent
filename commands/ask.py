from agent import ask_llm_stream
from memory import add_user, add_ai, get_context
from utils import detect_lang, is_code
from voice import speak

from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax


def run(console, user_prompt: str) -> None:
    console.print(
        Panel(user_prompt, title="[bold cyan]You[/bold cyan]", border_style="cyan", padding=(0, 1))
    )

    add_user(user_prompt)

    # Build prompt with memory context
    context = get_context()
    full_prompt = f"Conversation so far:\n{context}\nUser: {user_prompt}" if context else user_prompt

    live_text = Text()
    result = ""

    try:
        with Live(live_text, console=console, refresh_per_second=15):
            for chunk in ask_llm_stream(full_prompt):
                live_text.append(chunk)
                result += chunk
    except (ConnectionError, TimeoutError, RuntimeError) as e:
        console.print(
            Panel(f"[red]⚠ Error: {e}[/red]", title="AI Error", border_style="red")
        )
        return

    add_ai(result)

    # Display result
    if is_code(result):
        lang = detect_lang(result)
        console.print(
            Panel(
                Syntax(result, lang, theme="monokai", line_numbers=False),
                title="[bold green]AI[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(result, title="[bold green]AI[/bold green]", border_style="green")
        )
        speak(result)