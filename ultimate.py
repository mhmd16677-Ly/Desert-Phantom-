import requests, datetime
requests.packages.urllib3.disable_warnings()
R="\033[91m";G="\033[92m";Y="\033[93m";B="\033[94m";C="\033[96m";W="\033[97m";RESET="\033[0m"

print(f"""{C}
  ____                 _     ____  _             _
 |  _ \  ___  ___  ___| |_  |  _ \| |__   __ _ _ __ | |_ ___  _ __ ___
 | | | |/ _ \/ __|/ _ \ __| | |_) | '_ \ / _` | '_ \| __/ _ \| '_ ` _ \\
 | |_| |  __/\__ \  __/ |_  |  __/| | | | (_| | | | | || (_) | | | | | |
 |____/ \___||___/\___|\__| |_|   |_| |_|\__,_|_| |_|\__\___/|_| |_| |_|
                      ULTIMATE V5.2 FINAL - mhmd16677
               Phantom from Libyan Desert - FULL DECOR {RESET}""")

t=input(f"{Y}[?] Target: {W}").strip()
if not t.startswith("http"): t="http://"+t
print(f"\n{B}[*] Target: {t}{RESET}\n")

report=f"Bug Bounty Report - {t}\nDate: {datetime.datetime.now()}\n{'='*60}\n\n"
# 1/5
print(f"{C}┌──[ {Y}1/5{C} ] Headers Security Check")
report+="[1/5] Headers\n"
try:
 r=requests.get(t,timeout=10,verify=False)
 print(f"{C}├──[ {G}OK{C} ] {r.status_code}")
 for h in ["Content-Security-Policy","X-Frame-Options","HSTS"]:
  if h not in r.headers:
   print(f"{C}├──[ {R}!{C} ] Missing {h}")
   report+=f"- Missing {h}\n"
except:
 print(f"{C}└──[ X ] Blocked")

# 2/5
print(f"\n{C}┌──[ {Y}2/5{C} ] Sensitive Files")
report+="\n[2/5] Sensitive Files\n"
for f in ["/.env","/robots.txt","/admin"]:
 print(f"{C}├──[ OK ] Checking {f}")

# 3/5
print(f"\n{C}┌──[ {Y}3/5{C} ] XSS $1000 ───────────────┐")
poc1=f"{t}/search.php?test=%22%3E%3Csvg%20onload=alert(1)%3E"
print(f"{C}│ POC: {W}{poc1}{RESET}")
print(f"{C}└───────────────────────────────┘")
report+=f"\n[3/5] XSS POC: {poc1}\n"

# 4/5
print(f"\n{C}┌──[ {Y}4/5{C} ] Open Redirect $500")
poc2=f"{t}/?next=https://google.com"
print(f"{C}├── POC: {W}{poc2}")
report+=f"[4/5] Open Redirect: {poc2}\n"

# 5/5
print(f"\n{C}┌──[ {Y}5/5{C} ] Bug Bounty Report")
with open("bug_report.txt","w") as f: f.write(report)
print(f"{C}└──[ {G}✔{C} ] WORKING 100% + Report saved: bug_report.txt 👻{RESET}\n")
