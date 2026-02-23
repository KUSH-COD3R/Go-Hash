#!/usr/bin/env python3
"""
Go-Hash - Hash Identifier
Modified by KUSH-COD3R
"""

import requests
import json
import sys
import os
import time
import subprocess
import platform
from datetime import datetime


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


HISTORY_FILE = 'hash_history.txt'


def save_history(hash_input, algorithms):
    try:
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] Hash: {hash_input} | Algorithm: {algorithms}\n")
    except Exception as e:
        print(f"  {c('Warning: Could not save history:', 'Ye')} {e}")


def view_history():
    if not os.path.exists(HISTORY_FILE):
        print(f"  {c('No history found!', 'Ye')}")
        return
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"  {c('No history found!', 'Ye')}")
            return
        
        print(f"\n  {c('='*60, 'Wh')}")
        print(f"  {c('HASH HISTORY', 'Ye')}")
        print(f"  {c('='*60, 'Wh')}")
        
        for line in lines[-20:]:
            print(f"  {c(line.strip(), 'Wh')}")
        
        print(f"  {c('='*60, 'Wh')}")
    except Exception as e:
        print(f"  {c('Error reading history:', 'Re')} {e}")


def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print(f"  {c('History cleared!', 'Gr')}")
    else:
        print(f"  {c('No history to clear!', 'Ye')}")


def save_to_file(hash_input, algorithms):
    filename = f"hash_result_{int(time.time())}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Hash Identifier Result\n")
            f.write(f"{'='*40}\n")
            f.write(f"Hash: {hash_input}\n")
            f.write(f"Algorithm: {algorithms}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"  {c('Result saved to:', 'Gr')} {c(filename, 'Ye')}")
        return True
    except Exception as e:
        print(f"  {c('Error saving file:', 'Re')} {e}")
        return False


def batch_hash_check(hashes):
    results = []
    
    print(f"\n  {c('Processing', 'Ye')} {c(str(len(hashes)), 'Gr')} {c('hashes...', 'Ye')}\n")
    
    api_url = 'https://hashes.com/en/api/identifier'
    
    for i, hash_input in enumerate(hashes, 1):
        try:
            response = requests.get(api_url, params={'hash': hash_input}, timeout=10)
            data = response.json()
            
            if data.get('success'):
                algorithms = data.get('algorithms', [])
                algoritm_hash = ', '.join(algorithms) if algorithms else 'Unknown'
                results.append((hash_input, algoritm_hash, 'Success'))
                print(f"  {c('[', 'Gr')}{c(str(i), 'Wh')}{c(']', 'Gr')} {c(hash_input, 'Wh')} {c('->', 'Ye')} {c(algoritm_hash, 'Gr')}")
            else:
                error_msg = data.get('message', 'Unknown')
                results.append((hash_input, error_msg, 'Failed'))
                print(f"  {c('[', 'Re')}{c(str(i), 'Wh')}{c(']', 'Re')} {c(hash_input, 'Wh')} {c('->', 'Ye')} {c(error_msg, 'Re')}")
            
            time.sleep(0.5)
            
        except Exception as e:
            results.append((hash_input, str(e), 'Error'))
            print(f"  {c('[', 'Re')}{c(str(i), 'Wh')}{c(']', 'Re')} {c(hash_input, 'Wh')} {c('->', 'Ye')} {c('Error', 'Re')}")
    
    return results


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


def main_menu():
    print(f"""
  {c('[1]', 'Gr')} {c('Identify Single Hash', 'Wh')}
  {c('[2]', 'Gr')} {c('Batch Hash Check', 'Wh')}
  {c('[3]', 'Gr')} {c('View History', 'Wh')}
  {c('[4]', 'Gr')} {c('Clear History', 'Wh')}
  {c('[5]', 'Gr')} {c('Exit', 'Wh')}
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
            
            save_history(hash_input, algoritm_hash)
            
            save_opt = input(f"\n  {c('Save result to file?', 'Wh')} {c('Y/N', 'Gr')} {c(':', 'Wh')} ").lower()
            if save_opt == 'y':
                save_to_file(hash_input, algoritm_hash)
            
        else:
            error_msg = data.get('message', 'Unknown error')
            print(f'  {c("[!]", "Gr")} {c("Hash :", "Gr")} {c(error_msg, "Re")}')
            
    except requests.exceptions.RequestException as e:
        print(f'  {c("Error:", "Re")} {c(str(e), "Re")}')
    except json.JSONDecodeError:
        print(f'  {c("Error: Invalid response from server", "Re")}')
    except Exception as e:
        print(f'  {c("Error:", "Re")} {c(str(e), "Re")}')


def batch_mode():
    print(f"\n  {c('Enter hashes (one per line).', 'Wh')}")
    print(f"  {c('Press', 'Wh')} {c('Enter', 'Gr')} {c('twice to finish:', 'Wh')}")
    
    hashes = []
    while True:
        h = input("  > ")
        if h.strip():
            hashes.append(h.strip())
        else:
            break
    
    if not hashes:
        print(f"  {c('No hashes entered!', 'Ye')}")
        return
    
    results = batch_hash_check(hashes)
    
    success_count = sum(1 for r in results if r[2] == 'Success')
    print(f"\n  {c('Results:', 'Ye')} {c(str(success_count), 'Gr')}/{c(str(len(results)), 'Wh')} {c('successful', 'Wh')}")
    
    save_opt = input(f"\n  {c('Save all results to file?', 'Wh')} {c('Y/N', 'Gr')} {c(':', 'Wh')} ").lower()
    if save_opt == 'y':
        filename = f"batch_results_{int(time.time())}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Batch Hash Check Results\n")
                f.write(f"{'='*50}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*50}\n\n")
                for hash_input, algo, status in results:
                    f.write(f"Hash: {hash_input}\n")
                    f.write(f"Algorithm: {algo}\n")
                    f.write(f"Status: {status}\n")
                    f.write(f"{'-'*50}\n")
            print(f"  {c('Results saved to:', 'Gr')} {c(filename, 'Ye')}")
        except Exception as e:
            print(f"  {c('Error saving file:', 'Re')} {e}")


def main():
    if not check_internet():
        print(c("No internet connection! Please check your network.", "Re"))
        sys.exit(1)
    
    banner()
    
    while True:
        main_menu()
        
        choice = input(f"  {c('Select option:', 'Wh')} {c('[1-5]', 'Gr')} ").strip()
        
        if choice == '1':
            identify_hash()
        elif choice == '2':
            batch_mode()
        elif choice == '3':
            view_history()
        elif choice == '4':
            clear_history()
        elif choice == '5':
            print(c("  Exiting...", "Ye"))
            sys.exit(0)
        else:
            print(c("  Invalid option!", "Re"))
        
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{c('  Program stopped...', 'Wh')}")
        sys.exit(0)
