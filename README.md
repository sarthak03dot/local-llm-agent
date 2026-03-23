# 🤖 AI Agent

A cross-platform local CLI AI coding assistant powered by **Ollama** and `qwen2.5-coder`.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally (`ollama serve`)

Install Python dependencies (Windows & macOS):
```bash
pip install requests typer rich SpeechRecognition pyaudio
```

### Model Setup
By default, the agent uses `qwen2.5-coder:1.5b-base`. However, you can create a customized model with the included `Modelfile`.

```bash
ollama pull qwen2.5-coder:1.5b-base
ollama cp qwen2.5-coder:1.5b-base zyentric-base
ollama create zyentric-agent -f Modelfile
```
To use the custom model:
- **Windows**: `set OLLAMA_MODEL=zyentric-agent`
- **macOS/Linux**: `export OLLAMA_MODEL=zyentric-agent`

---

## Commands

| Command | Description |
|---|---|
| `python main.py ask "<question>"` | Ask the AI a question (streamed, with memory) |
| `python main.py run <file>` | Run a JS/TS/Python file and auto-fix errors (max 3 retries) |
| `python main.py chat` | Interactive text-chat REPL with memory |
| `python main.py modiji` | Voice-powered conversation mode (Works on Windows & macOS) |

---

## Configuration (Environment Variables)

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `qwen2.5-coder:1.5b-base` | Model name to use |

---

## Project Structure

```text
ai-agent/
├── main.py            # CLI entry point (typer)
├── agent.py           # Ollama HTTP client (streaming + non-streaming)
├── memory.py          # Conversation memory (Memory class)
├── utils.py           # Language detection & code cleaning helpers
├── voice.py           # Cross-platform TTS & STT (SpeechRecognition)
├── Modelfile          # Custom Ollama model definition
└── commands/
    ├── ask.py         # `ask` command
    ├── chat.py        # `chat` interactive REPL
    ├── run.py         # `run` command (auto-fix loop)
    └── modiji.py      # `modiji` voice assistant
```

---

## Usage Examples

```bash
# Ask a coding question
python main.py ask "Write a Python function to reverse a string"

# Run and auto-fix a Python or JavaScript/TypeScript file
python main.py run script.js
python main.py run app.py

# Start an interactive text chat session
python main.py chat

# Start voice mode (Cross-platform)
python main.py modiji
```
