import subprocess
import os
from agent import ask_llm
from utils import clean_code
from rich.panel import Panel
from rich.syntax import Syntax

MAX_RETRIES = 3

RUNNERS = {
    ".js": ["node"],
    ".ts": ["npx", "ts-node"],
    ".py": ["python3"],
}


def _detect_runner(file: str) -> list[str]:
    _, ext = os.path.splitext(file)
    return RUNNERS.get(ext.lower(), ["node"])


def run(console, file: str) -> None:
    if not os.path.exists(file):
        console.print(
            Panel(
                f"[red]File not found:[/red] {file}",
                title="Error",
                border_style="red",
            )
        )
        return

    runner = _detect_runner(file)

    for attempt in range(1, MAX_RETRIES + 1):
        result = subprocess.run(runner + [file], capture_output=True, text=True)

        if result.returncode == 0:
            console.print(
                Panel(
                    result.stdout or "[dim](no output)[/dim]",
                    title="[bold green]✅ Success[/bold green]",
                    border_style="green",
                )
            )
            return

        error = result.stderr or result.stdout
        console.print(
            Panel(
                error,
                title=f"[bold red]❌ Error (attempt {attempt}/{MAX_RETRIES})[/bold red]",
                border_style="red",
            )
        )

        if attempt == MAX_RETRIES:
            break

        with open(file) as f:
            code = f.read()

        fixed = ask_llm(f"Fix this error:\n{error}\n\nCode:\n{code}")
        fixed = clean_code(fixed)

        with open(file, "w") as f:
            f.write(fixed)

        console.print(
            Panel(
                Syntax(fixed, "javascript", theme="monokai"),
                title=f"[bold yellow]🔧 Fixed (attempt {attempt})[/bold yellow]",
                border_style="yellow",
            )
        )

    console.print(
        Panel(
            "[red]Could not fix the file after 3 attempts. Manual review required.[/red]",
            title="[bold red]🚫 Giving Up[/bold red]",
            border_style="red",
        )
    )