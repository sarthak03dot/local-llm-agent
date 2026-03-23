import subprocess
import platform
import speech_recognition as sr

from rich.panel import Panel


speech_process = None


def speak(text: str) -> None:
    global speech_process
    
    # Strip newlines to prevent command issues
    clean_text = text[:800].replace('\n', ' ').replace('\r', '')
    
    if platform.system() == "Windows":
        safe_text_win = clean_text.replace("'", "''")
        ps_script = f"Add-Type -AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe_text_win}')"
        speech_process = subprocess.Popen(["powershell", "-Command", ps_script])
    elif platform.system() == "Darwin":
        safe_text_mac = clean_text.replace('"', '\\"')
        speech_process = subprocess.Popen(["say", "-v", "Samantha", safe_text_mac])
    else:
        safe_text_linux = clean_text.replace('"', '\\"')
        try:
            speech_process = subprocess.Popen(["espeak", safe_text_linux])
        except FileNotFoundError:
            pass


def stop_speaking() -> None:
    global speech_process
    if speech_process:
        speech_process.terminate()
        speech_process = None


def listen(console) -> str | None:
    recognizer = sr.Recognizer()

    try:
        mic = sr.Microphone()
    except OSError:
        console.print(
            "[red]⚠ No microphone detected. Check your audio device.[/red]"
        )
        return None

    with mic as source:
        console.print(
            Panel(
                "🎤 Speak now...",
                title="Listening",
                border_style="yellow",
                padding=(1, 1),
            )
        )
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            console.print("[red]⏱ No speech detected[/red]")
            return None

    try:
        text = recognizer.recognize_google(audio)
        console.print(
            Panel(text, title="You said", border_style="cyan", padding=(1, 1))
        )
        return text

    except sr.UnknownValueError:
        console.print("[red]🔇 Could not understand speech[/red]")
        return None
    except sr.RequestError:
        console.print("[red]🌐 Network error during speech recognition[/red]")
        return None