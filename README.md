The AutoRecon is a multi-threaded reconnaissance framework designed to accelerate the initial phases of an engagement by bridging traditional security engineering with large language model (LLM) automation.

In modern security operations, scanners generate massive volumes of raw log data. Sifting through hundreds of subdomains, directory paths, and open ports to find an actual entry point is time-consuming. This toolkit automates that entire bottleneck: it actively probes the target infrastructure using high-performance multi-threading, structures the output, and hands off the consolidated threat surface data to an AI analysis engine.

By leveraging contextual prompting through the OpenRouter API, the tool acts as a virtual Red Team assistant—instantly interpreting scanning artifacts to isolate high-value vulnerabilities (like exposed configuration files or unpatched services) and mapping out precise, actionable attack paths for the operator.


```markdown
# 🔍 AI-Powered Pentest Automation Tool

A lightweight, multi-threaded penetration testing automation framework written in Python. This toolkit streamlines initial reconnaissance by blending asset discovery (**Subdomain Enumeration**, **Directory Brute-Forcing**, and **Port Scanning**) with automated **AI-driven contextual analysis** to prioritize offensive attack vectors.

---

## 🚀 Features

* **Subdomain Enumeration:** Fast multi-threaded DNS resolution with integrated wildcard DNS detection to prevent false positives.
* **Directory Brute-Forcing:** High-performance web path scanning featuring smart wildcard response filtering based on status codes and response length.
* **Flexible Nmap Integration:** Automated target port resolution providing custom preset scans ranging from fast sweeps to aggressive deep inspection frameworks.
* **AI Attack Surface Analysis:** Links directly with OpenRouter (DeepSeek/Custom models) to automatically ingest recon files and output targeted, high-value exploitation recommendations.
* **Rich Interactive Terminal UI:** Employs real-time status spinners, data dynamic formatting tables, and interactive menus.

---

## 🛠️ Architecture Workflow

1. **Reconnaissance Engine (`script.py`):** Drives target lookup, directories profiling, and active port states tracking while storing artifacts locally on disk.
2. **Contextual Analysis Ingestion:** `ai_analyze.py` targets the generated text dumps (`subdomains.txt`, `directories.txt`, `nmap_results.txt`) dynamically.
3. **LLM Evaluation Logic:** Consolidates raw tool responses into structured payloads forwarded via OpenRouter APIs to deliver prioritized next-step action matrices.

---

## 📋 Prerequisites

This tool relies on classic network utilities and a Linux-based security architecture (like Kali Linux). Ensure the following system elements are accessible:

* `nslookup` (Standard DNS utility)
* `nmap` (Network mapper utility)
* Default system wordlists installed at:
    * `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`
    * `/usr/share/wordlists/dirb/small.txt`

---

## ⚙️ Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
   cd your-repo-name

```

2. **Install Python Dependencies:**
```bash
pip install -r requirements.txt

```


*(Ensure your `requirements.txt` contains: `rich`, `requests`, and `dnspython`)*
3. **Configure API Keys:**
Export your OpenRouter API variables into your local terminal profile or operating environment:
```bash
export OPENROUTER_API_KEY="your_secret_openrouter_api_key"
# Optional configuration:
export OPENROUTER_MODEL="deepseek/deepseek-chat"

```



---

## ⚡ Usage

Run the primary automation controller to open the interactive operations dashboard:

```bash
python3 script.py

```

### Main Options Menu:

* **Option 1:** Subdomain Enumeration + AI Threat Modeling
* **Option 2:** Directory Brute-Force Discovery + AI Web Mapping
* **Option 3:** Full Threat Surface Mapping (Runs Subdomains, Directories, Nmap, and complete AI Attack Path Analysis)
* **Option 4:** Isolated Nmap Target Port Scanning + AI Recommendations

---

## 📂 Output Artifacts

The tool automatically updates local snapshots across execution loops, producing structural text files utilized for compliance reporting and tool feeding:

* `subdomains.txt` — Discovered target assets list.
* `directories.txt` — Valid live endpoints mapped via dictionary lookup.
* `nmap_results.txt` — Full raw port scanner console output logs.

---

## ⚖️ Legal Disclaimer

> **WARNING:** This automation tool is created strictly for authorized educational research, security evaluations, and defensive penetration testing engagements. Running aggressive port maps or dictionary brute-forcing against targets without explicit, written administrative authorization is strictly illegal. The author accepts no liability for misuse or damages resulting from this software utility.

```

```
