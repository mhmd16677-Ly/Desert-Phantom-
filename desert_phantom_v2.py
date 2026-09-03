#!/usr/bin/env python3
import requests
R="\033[91m";G="\033[92m";Y="\033[93m";C="\033[96m";W="\033[0m";B="\033[1m"
headers={"User-Agent":"Mozilla/5.0"}
WORDLIST=["admin","login","wp-admin","backup","config",".env","dashboard","robots.txt","sitemap.xml",".htaccess",".git","test","dev","api","admin.php","phpmyadmin","old","tmp","private","user","log","install","sql"]
def banner():
    print(f"{C}{B}\n ____  ____  ____  ____ _____   ____  _   _    _   _ _____ ___  __  __ \n|  _ \\|  _ \\/ ___||  _ \\_   _| |  _ \\| | | |  / \\  | \\ | |_   _/ _ \\|  \\/  |\n| | | | |_) \\___ \\| |_) || |   | |_) | |_| | / _ \\ |  \\| | | || | |\\/| |\n| |_| |  __/ ___) |  _ < | |   |  __/|  _  |/ ___ \\| |\\  | | || |_| | |  | |\n|____/|_|  |____/|_| \\_\\|_|   |_|   |_| |_/_/   \\_\\_| \\_| |_| \\___/|_|  |_|\n{Y}  V2.0 Fixed | By Mhmd {W}\n")
def get_url(target):
    # يجرب http و https
    if target.startswith("http"): return target
    return target

def scan_dirs(url):
    print(f"\n{B}{C}[+] فحص: {url}{W}\n")
    url=url.rstrip("/")
    for w in WORDLIST:
        full=f"{url}/{w}"
        try:
            r=requests.get(full,headers=headers,timeout=10,allow_redirects=False)
            if r.status_code==200: print(f"{G}[FOUND 200] {full}{W}")
            elif r.status_code==403: print(f"{Y}[FORBIDDEN 403] {full}{W}")
        except: pass
    print(f"\n{G}[+] كمل فحص المسارات{W}")

def scan_headers(url):
    print(f"\n{B}{C}[+] فحص الحماية: {url}{W}\n")
    try:
        r=requests.get(url,headers=headers,timeout=10)
        print(f"Server: {r.headers.get('Server','?')} | Status: {r.status_code}")
        for h in ["X-Frame-Options","Content-Security-Policy","Strict-Transport-Security","X-Content-Type-Options"]:
            if h in r.headers: print(f"  {G}[OK] {h}{W}")
            else: print(f"  {R}[MISS] {h} ناقص!{W}")
    except Exception as e: print(f"{R}Error: {e}{W}")

if __name__=="__main__":
    banner()
    target=input(f"{B}Enter website (with http://): {W}").strip()
    if not target.startswith("http"):
        # خليه http افتراضي للمواقع التدريبية
        target="http://"+target
    print("1-Finder 2-Headers 3-Full")
    c=input("اختيارك [1/2/3]: ").strip()
    if c=="1": scan_dirs(target)
    elif c=="2": scan_headers(target)
    else: scan_dirs(target); scan_headers(target)
