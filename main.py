import concurrent.futures, tls_client, colorama, datetime, requests, random, base64, string, ctypes, copy, json, re, os

from colorama           import Fore
from datetime           import datetime

codes = open("data/codes.txt", "r").read().splitlines()
proxies = open("data/proxies.txt", "r").read().splitlines()

colorama.init()

valid = 0
invalid = 0
fail = 0

def title_worker():
    global valid, invalid, fail
    ctypes.windll.kernel32.SetConsoleTitleW(f'[Promotion - @Blk1337] ~ Valid : {valid} | Invalid: {invalid} | Failed : {fail}')

def log(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f' [{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] ({Fore.LIGHTGREEN_EX}+{Fore.WHITE}) {text}')

def error(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f' [{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] ({Fore.LIGHTRED_EX}+{Fore.WHITE}) {text}')

base_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
}

def check(code: str):
    global valid, invalid, fail
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    proxy = random.choice(proxies)
    headers = copy.copy(base_headers)
    if "https://" in code:
        gift = code.split("/")[3]
    else:
        gift = code.split("/")[1]
    session = tls_client.Session(client_identifier="chrome_111", random_tls_extension_order=True)
    response = session.get(f"https://discord.com/api/v9/entitlements/gift-codes/{gift}?country_code=DE&with_application=false&with_subscription_plan=true", headers = headers, proxy=f"http://{proxy}")
    if response.status_code == 200:
        log(f"Valid - {code}")
        valid += 1
        title_worker()
        with open("valid.txt", "a") as gifts:
            gifts.write(f"{code}\n")
    elif response.status_code == 429:
        failed("Failed to check, due to ratelimit")
        failed += 1
        title_worker()
    elif response.status_code == 404:
        error(f"Invalid or Already used - {code}")
        invalid += 1
        title_worker()
    else:
        failed("Failed to check, due to unexpected error")
        failed += 1
        title_worker()

def main():
    title_worker()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    os.system("cls")
    threads = int(input(f" [{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] ({Fore.YELLOW}?{Fore.WHITE}) Enter threads: "))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as checker:
        for code in codes:
            checker.submit(check, code)
    print(f" [{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] ({Fore.YELLOW}!{Fore.WHITE}) Finished all threads, press enter to exit")
    input("")

main()