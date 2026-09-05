#!/data/data/com.termux/files/usr/bin/python3
# Desert Phantom V15.0 ULTIMATE FIXED - by qadi | mhmd16677 | Libya
# FIXED: No invalid escape sequences | Beautiful AI Report | HackerOne Ready

import argparse, datetime, pathlib, html, os, sys
from pathlib import Path
import requests
from concurrent.futures import ThreadPoolExecutor

# No more "\|" bug - using raw string
BANNER = r"""
 ____ _____ ____ _____ ____ _____ ____ _ _ _ _ _ _____ ___ __ __
| _ \| ____/ ___|| ____| _ \|_ _| | _ \| | | | / \ | \ | |_ _/ _ \| \/ |
| | | | _| \___ \| _| | |_) | | | | |_) | |_| | / _ \ | \| | | || | | | |\/| |
| |_| | |___ ___) | |___| _ < | | | __/| _ |/ ___ \| |\ | | || |_| | | | |
|____/|_____|____/|_____|_| \_\ |_| |_| |_| |_/_/ \_\_| \_| |_| \___/|_| |_|
                    V15.0 FIXED - BEAUTIFUL AI REPORT
"""

def check_live(url):
    try:
        r = requests.get(url, timeout=5, verify=False, headers={"User-Agent":"PhantomV15"})
        if r.status_code < 500:
            return url, r.status_code
    except:
        pass
    return None

def check_vuln(base_url):
    vulns = []
    payloads = {
        "wordpress-db-exposure": ("/db.sql", "HIGH", "#ff0055"),
        "exposed-env": ("/.env", "HIGH", "#ff0055"),
        "git-exposure": ("/.git/HEAD", "HIGH", "#ff0055"),
        "phpinfo-files": ("/info.php", "MEDIUM", "#ff8800"),
        "aspx-debug-mode": ("/debug", "LOW", "#ffcc00"),
        "backup-zip": ("/backup.zip", "MEDIUM", "#ff8800"),
    }
    for name, (path, sev, color) in payloads.items():
        url = base_url.rstrip("/") + path
        try:
            r = requests.get(url, timeout=6, verify=False)
            if r.status_code == 200 and len(r.text) > 20 and "404" not in r.text[:100]:
                # simple fingerprint
                if path == "/db.sql" and ("CREATE TABLE" in r.text or "INSERT INTO" in r.text):
                    vulns.append({"name":name,"severity":sev,"url":url,"color":color,"evidence":r.text[:120]})
                elif path in ["/.env","/.git/HEAD","/backup.zip","/info.php","/debug"] and r.status_code == 200:
                    vulns.append({"name":name,"severity":sev,"url":url,"color":color,"evidence":f"Status {r.status_code} - {len(r.text)} bytes"})
        except:
            continue
    return vulns

def main():
    parser = argparse.ArgumentParser(description="Phantom V15")
    parser.add_argument("-d","--domain", required=True, help="Target domain")
    args = parser.parse_args()
    domain = args.domain.strip().replace("https://","").replace("http://","").split("/")[0]

    print(f"\033[96m{BANNER}\033[0m")
    print(f"\033[93m[~] Target: {domain} | Hunter: qadi | Libya | mhmd16677\033[0m\n")

    # 1. Subdomain generation (fixed list without escape bug)
    prefixes = ["www","mail","dev","api","test","admin","portal","backup","db","corp","prod","beta","demo","manage","secure","jira","jenkins","grafana","gitlab","kibana","rest","testphp","testaspnet"]
    subs = [f"http://{p}.{domain}" for p in prefixes] + [f"https://{p}.{domain}" for p in prefixes]
    subs.append(f"https://{domain}")

    print(f"[*] Generated {len(subs)} subs, checking live...")
    live_urls = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        results = ex.map(check_live, subs)
        for res in results:
            if res:
                live_urls.append(res[0])
                print(f" \033[92m+ LIVE [{res[1]}] {res[0]}\033[0m")

    if not live_urls:
        live_urls = [f"https://{domain}"]

    print(f"\n[*] Scanning {len(live_urls)} live hosts for HIGH vulns...")
    all_vulns = []
    with ThreadPoolExecutor(max_workers=15) as ex:
        for vuln_list in ex.map(check_vuln, live_urls[:10]):
            all_vulns.extend(vuln_list)
            for v in vuln_list:
                print(f" \033[91m! [{v['severity']}] {v['name']} => {v['url']}\033[0m")

    # AI Priority
    high = [v for v in all_vulns if v['severity']=="HIGH"]
    all_vulns = sorted(all_vulns, key=lambda x: {"HIGH":0,"MEDIUM":1,"LOW":2}[x['severity']])

    # Report
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.home() / f"Phantom_V15_{domain}_{ts}"
    out_dir.mkdir(exist_ok=True)

    vhtml = ""
    if not all_vulns:
        vhtml = "<p style='color:#888'>No critical exposures found - target looks clean (good for learning).</p>"
    else:
        for v in all_vulns:
            vhtml += f"""
            <div style='border-left:5px solid {v['color']};background:#15151f;padding:14px;margin:12px 0;border-radius:10px'>
                <div style='display:flex;justify-content:space-between'><b style='color:{v['color']};font-size:16px'>[{v['severity']}] {html.escape(v['name'])}</b><span style='background:{v['color']};color:#000;padding:2px 8px;border-radius:12px;font-size:12px'>{v['severity']}</span></div>
                <div style='margin-top:8px'><a href='{v['url']}' style='color:#00ff88;word-break:break-all'>{v['url']}</a></div>
                <div style='color:#888;font-size:12px;margin-top:6px'>Evidence: {html.escape(v['evidence'][:200])}</div>
                <div style='margin-top:8px;font-size:13px'><b>AI Business Impact:</b> { 'Full DB leak - Account Takeover - $$$' if v['severity']=='HIGH' else 'Info disclosure - Low risk' }</div>
            </div>
            """

    live_html = "".join([f"<div style='padding:4px'>• <span style='color:#00ff88'>{html.escape(u)}</span></div>" for u in live_urls[:20]])

    html_report = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>PHANTOM V15 - {html.escape(domain)}</title>
    <style>body{{background:#080810;color:#e0e0e0;font-family:Inter,monospace;margin:0}}.hdr{{background:linear-gradient(90deg,#7b2cff,#00ff88);padding:28px;text-align:center;color:#fff}}.stats{{display:flex;justify-content:center;gap:14px;padding:20px;flex-wrap:wrap}}.card{{background:#1a1a2e;border-radius:12px;padding:16px 22px;min-width:95px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.4)}}.num{{font-size:28px;font-weight:800;color:#00ff88}}.sec{{max-width:950px;margin:auto;padding:20px}} h2{{color:#00ff88;border-bottom:2px solid #1a1a2e;padding-bottom:8px}} pre{{background:#111;padding:14px;border-radius:8px;white-space:pre-wrap;border:1px solid #222}}</style>
    </head><body>
    <div class='hdr'><h1>🤖 DESERT PHANTOM V15.0 FIXED</h1><p>{html.escape(domain)} | Bug Bounty Hunter: qadi | Tripoli, Libya | mhmd16677</p><p>V15 - AI Priority Engine + Business Report - No Glitch</p></div>
    <div class='stats'><div class='card'><div class='num'>{len(subs)}</div><div>Subdomains</div></div><div class='card'><div class='num'>{len(live_urls)}</div><div>Live</div></div><div class='card'><div class='num' style='color:#ff0055'>{len(all_vulns)}</div><div>Vulns</div></div><div class='card'><div class='num' style='color:#ff0055'>{len(high)}</div><div>HIGH</div></div></div>
    <div class='sec'><h2>💥 Vulnerabilities (AI Sorted)</h2>{vhtml}
    <h2>🎯 Live Hosts</h2>{live_html}
    <h2>📝 HackerOne English Template (Copy)</h2>
    <pre>Title: [{{severity}}] {{name}} at {html.escape(domain)}
Description:
Found publicly accessible file at {{url}}.

Steps to Reproduce:
1. Navigate to {{url}}
2. Observe file content leaks

Impact: Data leak / Account Takeover potential - High business impact.
Remediation: Remove file from public web root or protect with auth.

Researcher: mhmd16677 - Libya
</pre>
    </div></body></html>
    """
    (out_dir/"Report_AI.html").write_text(html_report, encoding="utf-8")
    (out_dir/"live.txt").write_text("\n".join(live_urls), encoding="utf-8")
    (out_dir/"vulns.json").write_text(str(all_vulns), encoding="utf-8")

    print(f"\n\033[92m✅ V15 COMPLETE - No SyntaxWarning!\033[0m")
    print(f"📁 {out_dir}")
    print(f"📄 Report_AI.html - OPEN IT: cd {out_dir} && python -m http.server 8888")
    print(f" Then: http://127.0.0.1:8888/Report_AI.html")

if __name__ == "__main__":
    main()
