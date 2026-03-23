from voice import listen, speak
from agent import ask_llm
from memory import add_user, add_ai, get_context

from rich.panel import Panel
from rich.markdown import Markdown

import random

EXIT_PHRASES = {"exit", "stop", "quit", "bye", "goodbye", "shut down"}
SPEAK_MAX_CHARS = 300


def get_intro() -> str:
    intros = [
        "Hello! Modiji is online. What mission do we have today?",
        "Hey boss... Modiji is at your service. What do you want to build?",
        "Greetings! Ready to conquer some code?",
        "System activated... Modiji online 😎. How can I help?",
    ]
    return random.choice(intros)


def run(console) -> None:
    console.print("🤖 Modiji is online...\n")

    intro = get_intro()
    console.print(
        Panel(intro, title="👋 Welcome", border_style="yellow", padding=(1, 2))
    )
    speak(intro)

    while True:
        text = listen(console)

        if not text:
            continue

        if text.lower().strip() in EXIT_PHRASES:
            farewell = "Goodbye! Happy coding!"
            console.print(
                Panel(farewell, title="Modiji", border_style="yellow", padding=(1, 2))
            )
            speak(farewell)
            break

        # Strip wake word if present
        command = text.replace("modiji", "").strip()
        if not command:
            continue

        add_user(command)

        prompt = f"""You are Modiji, a helpful AI assistant.

Conversation:
{get_context()}
User: {command}
"""

        try:
            response = ask_llm(prompt)
        except (ConnectionError, TimeoutError, RuntimeError) as e:
            console.print(
                Panel(f"[red]⚠ {e}[/red]", title="Error", border_style="red")
            )
            continue

        add_ai(response)

        console.print(
            Panel(
                Markdown(response),
                title="[bold green]Modiji[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

        # Limit TTS length to avoid very long speech
        speak(response[:SPEAK_MAX_CHARS])