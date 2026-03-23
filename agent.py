import os
import json
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b-base")

TIMEOUT = 30  # seconds


def ask_llm(prompt: str) -> str:
    """Send a prompt to Ollama and return the full response string."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"Cannot connect to Ollama at {OLLAMA_URL}. Is it running?"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError(
            f"Ollama did not respond within {TIMEOUT}s."
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}") from e


def ask_llm_stream(prompt: str):
    """Send a prompt to Ollama and yield response tokens as they arrive."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": True},
            stream=True,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"Cannot connect to Ollama at {OLLAMA_URL}. Is it running?"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError(
            f"Ollama did not respond within {TIMEOUT}s."
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}") from e

    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode())
            if "response" in chunk:
                yield chunk["response"]