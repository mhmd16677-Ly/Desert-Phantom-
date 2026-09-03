import requests

print("=== Header Hunter by Mhmd ===")
url = input("Enter website (ex: https://google.com): ")

try:
    r = requests.get(url, timeout=5)
    print(f"\n[+] Server: {r.headers.get('Server', 'Not Found')}")
    
    # فحص الحمايات
    checks = {
        "X-Frame-Options": "حماية من Clickjacking",
        "Content-Security-Policy": "حماية من XSS",
        "Strict-Transport-Security": "حماية HTTPS"
    }
    
    print("\n[+] Security Check:")
    for header, desc in checks.items():
        if header in r.headers:
            print(f"  [OK] {header} موجود - {desc}")
        else:
            print(f"  [MISS] {header} ناقص! - {desc} -> ثغرة محتملة!")

except Exception as e:
    print(f"Error: {e}")

