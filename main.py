import typer
from rich.console import Console

from commands.ask import run as ask_cmd
from commands.run import run as run_cmd
from commands.modiji import run as modiji_cmd
from commands.chat import run as chat_cmd

app = typer.Typer(
    name="ai-agent",
    help="A local AI coding assistant powered by Ollama.",
)
console = Console()


@app.command()
def ask(prompt: str = typer.Argument(..., help="Question or instruction for the AI")):
    """Ask the AI a single question (streamed answer with memory context)."""
    ask_cmd(console, prompt)


@app.command()
def run(file: str = typer.Argument(..., help="Path to the JS/TS/Python file to run")):
    """Run a file and auto-fix errors using the AI (up to 3 retries)."""
    run_cmd(console, file)


@app.command()
def modiji():
    """Start a voice-powered conversation with Modiji AI."""
    modiji_cmd(console)


@app.command()
def chat():
    """Start an interactive text chat session with memory."""
    chat_cmd(console)


if __name__ == "__main__":
    app()