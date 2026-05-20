# 🔍 AutoRecon

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
