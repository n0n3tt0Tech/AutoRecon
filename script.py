#script.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt
from rich.prompt import IntPrompt
from rich import box

import requests
import dns.resolver
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


console = Console()

# -----------------------------------------------------
# Banner
# -----------------------------------------------------
def banner():
    console.print(Panel.fit(
        "[bold cyan]🔍 PENTEST AUTOMATION TOOL[/bold cyan]\n"
        "[green]Subdomains • Directories • Nmap • AI[/green]",
        border_style="cyan", padding=(1, 2)
    ))



def run_ai():
    console.print("[bold green]\n[+] Running AI analysis...[/bold green]")
    subprocess.run(["python3", "ai_analyze.py"])


# -----------------------------------------------------
# Load Wordlist
# -----------------------------------------------------
def load_wordlist(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[bold red][!] Wordlist not found: {path}[/bold red]")
        return []

# -----------------------------------------------------
# Resolve domain (nslookup)
# -----------------------------------------------------
def resolve_domain(domain):
    console.print(f"\n[bold yellow]🔎 Resolving domain: {domain}[/bold yellow]")

    with console.status("[cyan]Running nslookup...[/cyan]"):
        try:
            result = subprocess.check_output(
                ["nslookup", domain], universal_newlines=True)

            ip = None
            capture = False

            for line in result.split("\n"):
                line = line.strip()

                if "Non-authoritative answer:" in line:
                    capture = True
                    continue
                if line.startswith("Name:"):
                    capture = True
                    continue
                if capture and line.startswith("Address:"):
                    ip = line.split("Address:")[-1].strip()
                    ip = ip.split("#")[0].strip()
                    break

            if ip:
                console.print(f"[bold green]✔ IP Resolved: {ip}[/bold green]")
                return ip

            console.print("[bold red]No IP record found.[/bold red]")
            return None

        except Exception as e:
            console.print(f"[bold red][!] nslookup failed:[/bold red] {e}")
            return None

# -----------------------------------------------------
# Subdomain Worker
# -----------------------------------------------------
def subdomain_worker(test_domain, resolver, wildcard_ip):
    try:
        answers = resolver.resolve(test_domain)
        ips = [r.address for r in answers]
        if wildcard_ip and ips == wildcard_ip:
            return None
        return test_domain
    except:
        return None

# -----------------------------------------------------
# Subdomain Scan
# -----------------------------------------------------
def subdomain_scan(domain, wordlist, outfile, threads=20):

    resolver = dns.resolver.Resolver()
    console.print(f"\n[bold cyan]🔧 Starting Subdomain Enumeration[/bold cyan]")

    # Wildcard
    console.print("[yellow]Checking for wildcard DNS...[/yellow]")
    try:
        wc = resolver.resolve("neverexists12345." + domain)
        wildcard_ip = [r.address for r in wc]
        console.print(f"[red]Wildcard DNS detected: {wildcard_ip}[/red]")
    except:
        wildcard_ip = None
        console.print("[green]No wildcard DNS detected[/green]")

    found = []
    total = len(wordlist)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}")
    ) as progress:

        task = progress.add_task("Scanning...", total=total)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(subdomain_worker, f"{sub}.{domain}", resolver, wildcard_ip): sub
                for sub in wordlist
            }

            for f in as_completed(futures):
                result = f.result()
                progress.update(task, advance=1)

                if result:
                    found.append(result)

    with open(outfile, "w") as f:
        f.write("\n".join(found))

    console.print(
        Panel.fit(f"[green]✔ Saved to {outfile}[/green]", border_style="green")
    )

# -----------------------------------------------------
# Directory Worker
# -----------------------------------------------------
def dir_worker(url, wildcard_status, wildcard_length):
    try:
        r = requests.get(url, timeout=4, allow_redirects=False)
        if wildcard_length and r.status_code == wildcard_status and len(r.text) == wildcard_length:
            return None
        if r.status_code not in [404, 400]:
            return f"{url} [{r.status_code}]"
    except:
        return None

# -----------------------------------------------------
# Directory Scan
# -----------------------------------------------------
def dir_bruteforce(base_url, wordlist, outfile, threads=20):
    console.print(f"\n[bold cyan]📂 Directory Brute-Forcing[/bold cyan]")

    if not base_url.endswith("/"):
        base_url += "/"

    # Wildcard Check
    console.print("[yellow]Checking for wildcard response...[/yellow]")
    try:
        r = requests.get(base_url + "neverexists12345")
        wildcard_length = len(r.text)
        wildcard_status = r.status_code
        console.print(f"[red]Wildcard detected ({wildcard_status}, length={wildcard_length})[/red]")
    except:
        wildcard_length = wildcard_status = None
        console.print("[green]No wildcard detected[/green]")

    found = []
    total = len(wordlist)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}")
    ) as progress:

        task = progress.add_task("Scanning...", total=total)

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(dir_worker, f"{base_url}{p}", wildcard_status, wildcard_length): p
                for p in wordlist
            }

            for f in as_completed(futures):
                result = f.result()
                progress.update(task, advance=1)

                if result:
                    found.append(result)

    with open(outfile, "w") as f:
        f.write("\n".join(found))

    console.print(Panel.fit(
        f"[green]✔ Saved to {outfile}[/green]", border_style="green"))

# -----------------------------------------------------
# Nmap Scan Menu
# -----------------------------------------------------
def choose_nmap_scan():

    table = Table(title="Choose Nmap Scan Type", box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("1", "Fast Scan (-F)")
    table.add_row("2", "Full Port Scan (-p-)")
    table.add_row("3", "Default Scripts + Version Detection (-sC -sV)")
    table.add_row("4", "OS Detection (-O)")
    table.add_row("5", "Aggressive Scan (-A)")
    table.add_row("6", "Custom Flags")
    table.add_row("7", "Version Only (-sV)")

    console.print(table)

    choice = Prompt.ask("[bold yellow]Select option[/bold yellow]", choices=[str(i) for i in range(1, 8)])

    scan_types = {
        "1": "-F",
        "2": "-p-",
        "3": "-sC -sV",
        "4": "-O",
        "5": "-A",
        "7": "-sV"
    }

    if choice == "6":
        return Prompt.ask("Enter custom flags")

    return scan_types.get(choice, "-F")

# -----------------------------------------------------
# Run Nmap
# -----------------------------------------------------
def run_nmap_scan(domain):
    ip = resolve_domain(domain)
    if not ip:
        return

    flags = choose_nmap_scan()

    console.print(f"\n[bold cyan]🚀 Running Nmap on {ip} using: {flags}[/bold cyan]")

    with console.status("[green]Scanning...[/green]"):
        try:
            result = subprocess.check_output(
                ["nmap"] + flags.split() + [ip],
                universal_newlines=True,
                stderr=subprocess.STDOUT
            )

            console.print(Panel(result, title="Nmap Output", border_style="cyan"))

            with open("nmap_results.txt", "w") as f:
                f.write(result)

            console.print("[bold green]✔ Saved to nmap_results.txt[/bold green]")

        except subprocess.CalledProcessError as e:
            console.print(f"[red]Nmap Error:[/red]\n{e.output}")




# -----------------------------------------------------
# Main Menu
# -----------------------------------------------------
def main():

    banner()

    table = Table(title="Main Menu", box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    table.add_column("Task", style="green")

    table.add_row("1", "Subdomain Enumeration")
    table.add_row("2", "Directory Brute-Force")
    table.add_row("3", "Run All (Subdomain + Directory + Nmap)")
    table.add_row("4", "Nmap Scan Only")

    console.print(table)

    choice = Prompt.ask("[bold yellow]Choose[/bold yellow]", choices=["1","2","3","4"])

    threads = IntPrompt.ask("Threads", default=20)

    sub_wordlist = "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
    dir_wordlist = "/usr/share/wordlists/dirb/small.txt"

    sub_words = load_wordlist(sub_wordlist)
    dir_words = load_wordlist(dir_wordlist)

    console.print(f"[green]Loaded {len(sub_words)} subdomains[/green]")
    console.print(f"[green]Loaded {len(dir_words)} directories[/green]")

    if choice == "1":
        domain = Prompt.ask("Enter domain")
        subdomain_scan(domain, sub_words, "subdomains.txt", threads)
        run_ai()

    elif choice == "2":
        url = Prompt.ask("Enter base URL")
        dir_bruteforce(url, dir_words, "directories.txt", threads)
        run_ai()

    elif choice == "3":
        domain = Prompt.ask("Enter domain")
        url = Prompt.ask("Enter base URL")

        subdomain_scan(domain, sub_words, "subdomains.txt", threads)
        dir_bruteforce(url, dir_words, "directories.txt", threads)
        
        console.print("\n[cyan]Now choose Nmap scan type[/cyan]")
        run_nmap_scan(domain)
        run_ai()

        
    elif choice == "4":
        domain = Prompt.ask("Enter domain")
        run_nmap_scan(domain)
        run_ai()



if __name__ == "__main__":
    main()

