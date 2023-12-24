import subprocess
from time import sleep
from datetime import datetime
import pyautogui as pg
import re

RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE = '\033[94m'
RESET='\033[0m'


wifi_ssid = str(input(f"{YELLOW}[?] What is the Wi-Fi name? > {RESET}"))
define_counter = int(input(f"{YELLOW}[?] Check every ... seconds. > {RESET}"))
location = input(f"{BLUE}[INFO] Type 'exit' to quit.\n[WARN] Put your cursor where you want it to be clicked and type 'get' here. > {RESET}")


def check_wifi_connection():
    counter = define_counter
    if define_counter != 0:
        while True:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
            pattern = re.compile(fr'\b{re.escape(wifi_ssid)}\b', re.IGNORECASE)
            match = re.search(pattern, result)
            if match and match.group() == wifi_ssid:
                print(f"{GREEN}[+] You are now connected to the {wifi_ssid} network. {40*'>'} {datetime.now()} {RESET}")
                click()
                break
            else:
                print(f"{RED}[-] You are not currently connected to the {wifi_ssid} network. {40*'>'} {datetime.now()} {RESET}")
                counter -= 1
                sleep(define_counter)
                if counter == 0:
                    counter = define_counter

def click():
    try:
        getX, getY = coordinates[0], coordinates[1]
        pg.click(x=getX, y=getY, duration=2)
        print(f"{GREEN}[SUCCESS] Clicked. {40*'>'} {datetime.now()} {RESET}")
    except NameError:
        return f"{GREEN}[INFO] Quitted by user. {40*'>'} {datetime.now()} {RESET}"
    

try:
    if location == "exit" or location == "EXIT":
        print(f"{GREEN}[INFO] Quitted by user.\n[INFO] Only the wifi network will be checked, no additional action will be taken.  {RESET}")
        check_wifi_connection()
    elif location == "get" or location == "GET":
        coordinates = pg.position()
        print(f"{GREEN}[INFO] Coordinates received.{RESET}")
        check_wifi_connection() 
    else:
        print(f"{RED}[-] Invalid Entry.{RESET}")          
except KeyboardInterrupt:
    print(f"{GREEN}[INFO] Quitted by user. {40*'>'} {datetime.now()} {RESET}")
