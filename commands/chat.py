from agent import ask_llm_stream
from memory import add_user, add_ai, get_context, clear
from utils import detect_lang, is_code

from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt


EXIT_COMMANDS = {"exit", "quit", "bye", "q"}


def run(console) -> None:
    console.print(
        Panel(
            "💬 Text chat mode — type [bold]exit[/bold] or [bold]quit[/bold] to stop.\n"
            "Type [bold]clear[/bold] to reset conversation memory.",
            title="[bold cyan]Chat[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            console.print("[dim]Goodbye![/dim]")
            break

        if user_input.lower() == "clear":
            clear()
            console.print("[dim]Memory cleared.[/dim]")
            continue

        add_user(user_input)

        context = get_context()
        full_prompt = (
            f"Conversation:\n{context}\nUser: {user_input}"
            if context else user_input
        )

        live_text = Text()
        result = ""

        try:
            with Live(live_text, console=console, refresh_per_second=15):
                for chunk in ask_llm_stream(full_prompt):
                    live_text.append(chunk)
                    result += chunk
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            console.print(
                Panel(f"[red]⚠ {e}[/red]", title="Error", border_style="red")
            )
            continue

        add_ai(result)

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
