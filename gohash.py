#!/usr/bin/env python3
"""
Go-Hash - Hash Identifier
Modified by KUSH-COD3R
"""

import requests
import json
import sys
import time
import subprocess
import platform


def check_internet():
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        subprocess.check_call(['ping', param, '1', 'www.google.com'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        return True
    except:
        return False


COLORS = {
    'Bl': '\033[30m',
    'Re': '\033[1;31m',
    'Gr': '\033[1;32m',
    'Ye': '\033[1;33m',
    'Blu': '\033[1;34m',
    'Mage': '\033[1;35m',
    'Cy': '\033[1;36m',
    'Wh': '\033[1;37m',
    'reset': '\033[0m'
}


def c(text, color):
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


def banner():
    print(f"""
{c('     ██████╗  ██████╗       ██╗  ██╗ █████╗ ███████╗██╗  ██╗', 'Gr')}
{c('    ██╔════╝ ██╔═══██╗      ██║  ██║██╔══██╗██╔════╝██║  ██║', 'Gr')}
{c('    ██║  ███╗██║   ██║█████╗███████║███████║███████╗███████║', 'Gr')}
{c('    ██║   ██║██║   ██║╚════╝██╔══██║██╔══██║╚════██║██╔══██║', 'Gr')}
{c('    ╚██████╔╝╚██████╔╝      ██║  ██║██║  ██║███████║██║  ██║', 'Gr')}
{c('     ╚═════╝  ╚═════╝       ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝', 'Gr')}
{c('           <<------ CODE BY HUNX ------>>', 'Wh')}
{c('                      < Hash identified >', 'Wh')}
""")


def identify_hash():
    api_url = 'https://hashes.com/en/api/identifier'
    
    print(f"\n  {c('[+]', 'Gr')} {c('Enter Your Hash :', 'Gr')}", end=' ')
    hash_input = input()
    
    if not hash_input.strip():
        print(f"  {c('Error: Hash cannot be empty!', 'Re')}")
        return
    
    try:
        response = requests.get(api_url, params={'hash': hash_input}, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            algorithms = data.get('algorithms', [])
            algoritm_hash = ', '.join(algorithms) if algorithms else 'Unknown'
            time.sleep(2)
            
            print(f'\n  {c("="*20, "Wh")} {c("Show Algorithm Hash", "Ye")} {c("="*20, "Wh")}')
            print(f'\n  {c("[+]", "Gr")} {c("Hash :", "Gr")} {hash_input}')
            print(f'  {c("[+]", "Gr")} {c("Algorithm :", "Gr")} {c(algoritm_hash, "Ye")}')
            print(f'\n  {c("="*56, "Wh")}')
            
            while True:
                user_input = input(f"\n  {c('Do you want to identify the hash again?', 'Wh')} {c('Y/N', 'Gr')} {c(':', 'Wh')} ").lower()
                if user_input == 'y':
                    identify_hash()
                    return
                elif user_input == 'n':
                    print(f'  {c("Exit Tools !!!", "Re")}')
                    return
                else:
                    print(c("  Invalid option!", "Re"))
        else:
            error_msg = data.get('message', 'Unknown error')
            print(f'  {c("[!]", "Gr")} {c("Hash :", "Gr")} {c(error_msg, "Re")}')
            
    except requests.exceptions.RequestException as e:
        print(f'  {c("Error:", "Re")} {c(str(e), "Re")}')
    except json.JSONDecodeError:
        print(f'  {c("Error: Invalid response from server", "Re")}')
    except Exception as e:
        print(f'  {c("Error:", "Re")} {c(str(e), "Re")}')


def main():
    if not check_internet():
        print(c("No internet connection! Please check your network.", "Re"))
        sys.exit(1)
    
    banner()
    
    while True:
        identify_hash()
        
        while True:
            again = input(f"\n  {c('Do you want to start again?', 'Wh')} {c('Y/N', 'Gr')} {c(':', 'Wh')} ").lower()
            if again == 'y':
                break
            elif again == 'n':
                print(c("  Exiting...", "Ye"))
                sys.exit(0)
            else:
                print(c("  Invalid option!", "Re"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c('  Program stopped...', 'Wh')}")
        sys.exit(0)
