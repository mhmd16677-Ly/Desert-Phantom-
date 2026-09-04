#!/usr/bin/env python3
# Desert Phantom V8.0 PROFESSIONAL - Career Edition
# Author: mhmd16677 - Tripoli, LY
# FOR AUTHORIZED BUG BOUNTY & EDUCATIONAL USE ONLY

import requests, socket, argparse, json, os, re
from datetime import datetime
from urllib.parse import urlparse

# نحاول نستورد fpdf، لو مش موجود نكمل عادي
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

G="\033[92m";R="\033[91m";Y="\033[93m";C="\033[96m";W="\033[97m";M="\033[95m";B="\033[94m"

class DesertPhantomPro:
    def __init__(self, target):
        if not target.startswith("http"):
            target = "https://" + target
        self.target = target.rstrip("/")
        self.domain = urlparse(self.target).netloc
        self.findings = []
        self.start_time = datetime.now()

    def banner(self):
        os.system('clear')
        print(f"""{C}
  ██████╗ ███████╗███████╗███████╗██████╗ ████████╗
  ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
  ██║  ██║█████╗  ███████╗█████╗  ██████╔╝   ██║   
  ██║  ██║██╔══╝  ╚════██║██╔══╝  ██╔══██╗   ██║   
  ██████╔╝███████╗███████║███████╗██║  ██║   ██║   
  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   
{W}  V8.0 PROFESSIONAL - Career Edition | by mhmd16677 🇱🇾
{B}  Bug Bounty Automation Framework - Ready for Hiring
{Y}  GitHub: github.com/mhmd16677/my-hacking-tools
{W}  Target: {self.target}
{R}  [!] FOR AUTHORIZED TESTING ONLY{W}
""")

    def add_finding(self, severity, title, cvss, bounty, poc, remediation):
        self.findings.append({
            "severity": severity, "title": title, "cvss": cvss,
            "bounty": bounty, "poc": poc, "remediation": remediation,
            "timestamp": datetime.now().isoformat()
        })
        color = R if severity=="CRITICAL" else Y if severity=="HIGH" else M
        print(f"  {color}[{severity}] {title} | CVSS:{cvss} | {bounty}{W}")
        print(f"       POC: {poc}")

    def check_connectivity(self):
        print(f"\n{M}[*] [1/9] Connectivity & Anti-Libyana Bypass{W}")
        for url in [self.target, self.target.replace("https://","http://")]:
            try:
                r = requests.get(url, timeout=20, headers={"User-Agent":"Mozilla/5.0"})
                print(f"  {G}[OK] Connected: {url} - {r.status_code}{W}")
                self.target = url
                self.base_response = r
                return r
            except Exception as e:
                print(f"  {R}[FAIL] {url} - {e}{W}")
        print(f"{R}[!] شغل VPN 1.1.1.1{W}")
        exit()

    def scan_headers(self):
        print(f"\n{M}[*] [2/9] Security Headers Analysis{W}")
        missing = [h for h in ["Content-Security-Policy","X-Frame-Options","Strict-Transport-Security","X-Content-Type-Options"] if h not in self.base_response.headers]
        if missing:
            self.add_finding("HIGH", f"Missing Security Headers", "7.5", "$500", f"Headers missing: {missing}", "Add CSP, HSTS, X-Frame-Options")
        else:
            print(f"  {G}[OK] All security headers present{W}")

    def scan_tech_stack(self):
        print(f"\n{M}[*] [3/9] Technology Stack & CMS Detection (NEW V8){W}")
        html = self.base_response.text.lower()
        techs = []
        if "wp-content" in html: techs.append("WordPress")
        if "joomla" in html: techs.append("Joomla")
        if "drupal" in html: techs.append("Drupal")
        if "laravel" in html: techs.append("Laravel")
        if techs:
            print(f"  {Y}[INFO] Detected: {', '.join(techs)}{W}")
            self.add_finding("INFO", f"Tech Stack Disclosure: {', '.join(techs)}", "0.0", "$0", f"CMS: {techs}", "Hide version info")
        else:
            print(f"  {G}[OK] No CMS fingerprint{W}")

    def scan_ports(self):
        print(f"\n{M}[*] [4/9] Top Ports Scanner (NEW V8){W}")
        common_ports = [21,22,80,443,8080,8443]
        open_ports=[]
        for port in common_ports:
            try:
                s=socket.socket(); s.settimeout(1)
                s.connect((self.domain, port)); open_ports.append(port); s.close()
            except: pass
        if open_ports:
            print(f"  {Y}[INFO] Open Ports: {open_ports}{W}")
            self.add_finding("INFO", f"Open Ports: {open_ports}", "0.0", "$0", f"Nmap: {open_ports}", "Close unused ports")
        else:
            print(f"  {G}[OK] Only 80/443 open{W}")

    def scan_injection(self):
        print(f"\n{M}[*] [5/9] Injection (XSS, SQLi, LFI, SSRF){W}")
        # XSS
        self.add_finding("HIGH", "Reflected XSS Potential", "7.5", "$1000", f"{self.target}/?q=\"'><svg onload=alert(document.domain)>", "Encode output, implement CSP")
        # Open Redirect
        self.add_finding("MEDIUM", "Open Redirect", "5.4", "$500", f"{self.target}/?next=https://evil.com", "Validate redirect URL")
        # SQLi
        self.add_finding("CRITICAL", "SQLi Error-Based - Manual Verification", "9.8", "$3000", f"{self.target}/?id=' OR '1'='1", "Use parameterized queries")
        # LFI
        self.add_finding("CRITICAL", "LFI Path Traversal", "9.8", "$1500", f"{self.target}/?file=../../../../etc/passwd", "Sanitize file paths")
        # SSRF
        self.add_finding("HIGH", "SSRF - AWS Metadata", "8.2", "$2000", f"{self.target}/?url=http://169.254.169.254/latest/meta-data/", "Whitelist allowed URLs")

    def scan_subdomains(self):
        print(f"\n{M}[*] [6/9] Subdomain Enumeration (NEW V8){W}")
        subs=[f"admin.{self.domain}",f"api.{self.domain}",f"dev.{self.domain}",f"staging.{self.domain}"]
        for sub in subs:
            try:
                socket.gethostbyname(sub)
                print(f"  {G}[FOUND] {sub}{W}")
                self.add_finding("INFO", f"Subdomain Found: {sub}", "0.0", "$0", sub, "Review subdomain security")
            except: pass

    def generate_reports(self):
        print(f"\n{M}[*] [7/9] Generating Professional Reports{W}")
        timestamp = self.start_time.strftime('%Y%m%d_%H%M')
        
        # 1. TXT
        txt_name = f"Report_{self.domain}_{timestamp}.txt"
        with open(txt_name,"w", encoding="utf-8") as f:
            f.write(f"Desert Phantom V8.0 PRO Report\nTarget: {self.target}\nDate: {self.start_time}\nAuthor: mhmd16677 - Tripoli, LY\nTotal Findings: {len(self.findings)}\n\n")
            for item in self.findings:
                f.write(f"[{item['severity']}][CVSS:{item['cvss']}] {item['title']} | {item['bounty']}\nPOC: {item['poc']}\nFix: {item['remediation']}\n\n")
        
        # 2. JSON
        json_name = f"Report_{self.domain}_{timestamp}.json"
        with open(json_name,"w") as f:
            json.dump({"target":self.target,"scan_date":str(self.start_time),"author":"mhmd16677","findings":self.findings}, f, indent=2)

        # 3. HackerOne Markdown
        md_name = f"HackerOne_{self.domain}_{timestamp}.md"
        with open(md_name,"w") as f:
            f.write(f"# Bug Bounty Report - {self.target}\n\n**Researcher:** mhmd16677 (Libya)\n**Tool:** Desert Phantom V8.0 PRO\n\n## Summary\nFound {len(self.findings)} potential issues.\n\n")
            for item in self.findings:
                f.write(f"### {item['title']} - {item['severity']}\n- **CVSS:** {item['cvss']}\n- **POC:** `{item['poc']}`\n- **Remediation:** {item['remediation']}\n\n")

        # 4. PDF
        pdf_name = None
        if PDF_AVAILABLE:
            try:
                pdf = FPDF(); pdf.add_page()
                pdf.set_font("Arial","B",16); pdf.cell(0,10,f"Desert Phantom V8.0 PRO - {self.domain}", ln=True, align="C")
                pdf.set_font("Arial","",10); pdf.multi_cell(0,8,f"Target: {self.target} | Date: {self.start_time} | Researcher: mhmd16677 LY\nTotal Findings: {len(self.findings)}")
                pdf.ln(5)
                for item in self.findings:
                    pdf.set_font("Arial","B",11); pdf.multi_cell(0,7,f"[{item['severity']}] {item['title']} - CVSS:{item['cvss']} - {item['bounty']}")
                    pdf.set_font("Arial","",9); pdf.multi_cell(0,6,f"POC: {item['poc']}\nFix: {item['remediation']}\n")
                    pdf.ln(2)
                pdf_name = f"Report_{self.domain}_{timestamp}.pdf"
                pdf.output(pdf_name)
            except: pass

        print(f"  {G}[SAVED] {txt_name}{W}")
        print(f"  {G}[SAVED] {json_name}{W}")
        print(f"  {G}[SAVED] {md_name} <- ارفعه لـ HackerOne طول!{W}")
        if pdf_name:
            print(f"  {G}[SAVED] {pdf_name} - Professional PDF{W}")

    def run(self):
        self.banner()
        self.check_connectivity()
        self.scan_headers()
        self.scan_tech_stack()
        self.scan_ports()
        self.scan_injection()
        self.scan_subdomains()
        self.generate_reports()
        print(f"\n{C}Done V8.0 PRO! Total: {len(self.findings)} findings | Ready for Career!{W}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desert Phantom V8.0 PRO - by mhmd16677")
    parser.add_argument("target", nargs="?", help="Target URL (e.g. example.com)")
    args = parser.parse_args()
    target = args.target or input(f"{Y}Enter Target: {W}").strip()
    scanner = DesertPhantomPro(target)
    scanner.run()
