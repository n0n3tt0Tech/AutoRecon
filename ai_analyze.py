#ai_analyze.py

import os
import json
import requests
from rich.console import Console
from rich.panel import Panel

console = Console()

# -----------------------------------------------
# Load Recon Files
# -----------------------------------------------
def load_file(path, description):
    if not os.path.exists(path):
        return f"No {description} file found at {path}"

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return f"Failed to read {description} file."


# -----------------------------------------------
# AI Request Function
# -----------------------------------------------
def ask_ai(subdomains, directories, nmap_output):
    api_url = "https://openrouter.ai/api/v1/chat/completions"

    # ⚠ Replace with your real key
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat").strip() or "deepseek/deepseek-chat"

    if not api_key:
        return "[AI Error] OPENROUTER_API_KEY environment variable is not set."

    prompt = f"""
You are a penetration testing assistant.

Here are the reconnaissance results:

### Subdomains found:
{subdomains}

### Directories found:
{directories}

### Nmap scan output:
{nmap_output}

Based on these results, suggest the next technical steps in detail that a pentester should take.
Make the suggestions specific, actionable, and prioritize high‑value exploitation paths.
"""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(api_url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()

        data = r.json()

        try:
            content = data["choices"][0]["message"]["content"]
            if not content or content.strip() == "":
                return "[AI Error] Model returned an empty response."
            return content
        except:
            return "[AI Error] Invalid model response format."

    except Exception as e:
        return f"[AI Error] {e}"


# -----------------------------------------------
# GUI / External Script Function
# -----------------------------------------------
def run_ai_analysis():
    """Runs AI analysis and returns the string result (no printing)."""
    subs = load_file("subdomains.txt", "subdomain")
    dirs = load_file("directories.txt", "directory")
    nmap_out = load_file("nmap_results.txt", "nmap")

    return ask_ai(subs, dirs, nmap_out)


# -----------------------------------------------
# CLI Entry Point
# -----------------------------------------------
def main():
    console.print(Panel("[bold cyan]AI Analysis — Next Pentest Steps[/bold cyan]", border_style="cyan"))

    subs = load_file("subdomains.txt", "subdomain")
    dirs = load_file("directories.txt", "directory")
    nmap_out = load_file("nmap_results.txt", "nmap")

    console.print("[green]✔ Loaded recon results[/green]")

    ai_response = ask_ai(subs, dirs, nmap_out)

    console.print(Panel(
        ai_response,
        title="AI Suggested Next Steps",
        border_style="magenta"
    ))


if __name__ == "__main__":
    main()
