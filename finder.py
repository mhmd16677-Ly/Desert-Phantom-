import requests
headers = {"User-Agent": "Mozilla/5.0"}

url = input("Enter site: ").rstrip("/")
words = ["admin", "login", "backup", "config", "test", "dashboard", ".env", "robots.txt"]

print(f"\n[+] Scanning {url}...\n")
for w in words:
    full = f"{url}/{w}"
    try:
        r = requests.get(full, headers=headers, timeout=5)
        if r.status_code == 200:
            print(f"[FOUND] {full} -> {r.status_code} 🔥")
        elif r.status_code == 403:
            print(f"[FORBIDDEN] {full} -> 403 (محمي لكن موجود!)")
        else:
            print(f"[--] {full} -> {r.status_code}")
    except Exception as e:
        print(f"[ERR] {full} -> {e}")

