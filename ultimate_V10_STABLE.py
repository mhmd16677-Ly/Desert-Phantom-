#!/usr/bin/env python3
# Desert Phantom V10 ULTIMATE - mhmd16677 | Tripoli, LY
# FOR AUTHORIZED TESTING ONLY - Bug Bounty Professional

import os, sys, socket, json, argparse, subprocess, requests
from pathlib import Path
from datetime import datetime

HOME = Path.home()
GO_BIN = HOME / "go" / "bin"

def banner():
    print("""
\x1b[96m
 ██████╗ ███████╗███████╗███████╗██████╗ ████████╗
 ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
 ██║ ██║█████╗ ███████╗█████╗ ██████╔╝ ██║
 ██║ ██║██╔══╝ ╚════██║██╔══╝ ██╔══██╗ ██║
 ██████╔╝███████╗███████║███████╗██║ ██║ ██║
 ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝ ╚═╝ ╚═╝
 V10 ULTIMATE | mhmd16677 | Career Ready
\x1b[0m
    """)

def tool_path(name):
    p = GO_BIN / name
    if p.exists(): return str(p)
    try:
        out = subprocess.run(f"which {name}", shell=True, capture_output=True, text=True, timeout=5)
        if out.stdout.strip(): return out.stdout.strip()
    except: pass
    return name

def scan_tech(url):
    tech=[]
    try:
        r=requests.get(url, timeout=8, headers={"User-Agent":"Desert-Phantom-V10"}, verify=False)
        h=str(r.headers).lower(); b=r.text.lower()
        if "wp-content" in b or "wordpress" in b: tech.append("WordPress")
        if "joomla" in b: tech.append("Joomla")
        if "drupal" in b: tech.append("Drupal")
        if "laravel" in h or "php" in h: tech.append("PHP/Laravel")
        if "next" in b or "react" in b: tech.append("React/Next.js")
        if "nginx" in h: tech.append("Nginx")
        if "cloudflare" in h: tech.append("Cloudflare")
        if not tech: tech=["Unknown"]
    except: tech=["Unreachable"]
    return tech

def scan_ports(host):
    opens=[]
    for port in [21,22,80,443,8080,8443,3000,5000,8000,9000]:
        try:
            s=socket.socket(); s.settimeout(1)
            if s.connect_ex((host,port))==0: opens.append(port)
            s.close()
        except: pass
    return opens

def main():
    banner()
    parser=argparse.ArgumentParser(description="Desert Phantom V10 ULTIMATE - Authorized Bug Bounty")
    parser.add_argument("-d","--domain", required=True, help="example.com - must be authorized target")
    args=parser.parse_args()
    domain=args.domain.replace("https://","").replace("http://","").split("/")[0]
    out=Path(f"Phantom_V10_{domain.replace('.','_')}_{datetime.now().strftime('%Y%m%d')}")
    out.mkdir(exist_ok=True)
    print(f"[+] Target: {domain}")
    print(f"[+] Output: {out}")

    print("\n[1/4] Subdomain Enum...")
    subs=[]
    sf=tool_path("subfinder")
    if Path(sf).exists():
        try:
            cmd=f"{sf} -d {domain} -silent -timeout 30"
            res=subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            subs=[x for x in res.stdout.splitlines() if x]
        except: pass
    if not subs:
        print(" -> subfinder not found / fallback list")
        subs=[domain, f"www.{domain}", f"api.{domain}", f"dev.{domain}", f"admin.{domain}", f"test.{domain}"]
    (out/"subs.txt").write_text("\n".join(subs))
    print(f" -> {len(subs)} subs")

    print("\n[2/4] Live Filter (FIX for empty live.txt)...")
    live=[]
    hx=tool_path("httpx")
    if Path(hx).exists():
        try:
            cmd=f"cat {out/'subs.txt'} | {hx} -silent -tech-detect -status-code -title -follow-redirects -timeout 10 -retries 1 -threads 50"
            res=subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            live=[x for x in res.stdout.splitlines() if x]
        except Exception as e: print(f" httpx error: {e}")
    if not live:
        print(" -> httpx empty, using requests fallback (هذا يصلح مشكلة live.txt الفاضي)")
        for s in subs[:30]:
            for proto in ["https://","http://"]:
                try:
                    r=requests.get(proto+s, timeout=6, verify=False)
                    if r.status_code < 500:
                        live.append(f"{proto}{s} [{r.status_code}] {r.headers.get('Server','')}")
                        break
                except: pass
    (out/"live.txt").write_text("\n".join(live))
    print(f" -> Live: {len(live)}")

    print("\n[3/4] Tech + Ports...")
    findings=[]
    for entry in live[:25]:
        url=entry.split()[0] if entry else f"https://{domain}"
        host=url.replace("https://","").replace("http://","").split("/")[0].split(":")[0]
        tech=scan_tech(url); ports=scan_ports(host)
        findings.append({"url":url,"host":host,"tech":tech,"ports":ports})
        print(f" {host} => {','.join(tech)} | Ports {ports}")

    print("\n[4/4] Reports...")
    md=f"# Desert Phantom V10 - {domain}\n\n**Author:** mhmd16677 - Tripoli, LY\n**Date:** {datetime.now()}\n**Scope:** Authorized testing only\n\n## Live ({len(live)})\n" + "\n".join([f"- {x}" for x in live]) + "\n\n## Findings\n"
    for f in findings:
        md+=f"\n### {f['host']}\n- URL: {f['url']}\n- Tech: {', '.join(f['tech'])}\n- Ports: {f['ports']}\n"

    (out/"Report.md").write_text(md, encoding="utf-8")
    (out/"Report.json").write_text(json.dumps({"domain":domain,"live":live,"findings":findings}, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n\x1b[92m[✓] DONE -> {out}/\x1b[0m")
    print(f" - {out/'live.txt'} ({len(live)} live)")
    print(f" - {out/'Report.md'}")
    print(f" - {out/'Report.json'}")
    print("\nNote: استخدم هذا فقط على برامج عندك تصريح عليها HackerOne/Bugcrowd")

if __name__=="__main__":
    main()
