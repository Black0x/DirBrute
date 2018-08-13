#!/usr/bin/python3
import os
import argparse
import requests
import threading
from sys import stdout
from datetime import datetime
def banner():
    print("\n ____  _      ____             _       ")
    print("|  _ \(_)_ __| __ ) _ __ _   _| |_ ___ ")
    print("| | | | | '__|  _ \| '__| | | | __/ _ \\")
    print("| |_| | | |  | |_) | |  | |_| | ||  __/")
    print("|____/|_|_|  |____/|_|   \__,_|\__\___|Coded by Black0x\n\n")
def check(full_url):
    r = requests.get(full_url)
    return r.status_code
def brute():
    while True:
        with lock:
            dir_ = wordlist.readline().strip()
            if dir_ == "":
                break
            else:
                full_url = url + dir_
        o = check(full_url)
        with lock:
            if o == 404:
                stdout.write("[!] 404 Not found: " + full_url + "                  \r")
                stdout.flush()
            else:
                print("[+] Found: " + full_url + " [Code: " + str(o) + "]           ")
def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str)
    parser.add_argument("-w", "--wordlist", type=str)
    parser.add_argument("-t", "--threads", type=int)
    args = parser.parse_args()
    if args.url and args.wordlist:
        global url
        global lock
        global wordlist
        global wordlist_file
        url = args.url
        lock = threading.Lock()
        wordlist_file = args.wordlist
        try:
            wordlist = open(wordlist_file, "r")
            try:
                print("[-] Testing connection to url")
                requests.get(url, timeout=10)
                print("[-] Starting brute force")
                if args.threads:
                    for i in range(args.threads):
                        threading.Thread(target=brute).start()
                else:
                    brute()
            except requests.exceptions.ConnectionError:
                print("[!] Error: cannot connect to url")
            except requests.exceptions.Timeout:
                print("[!] Error: connection to url timed out")
        except IOError:
            print("[!] Error: wrong wordlist file: " + wordlist_file)
    else:
        print("[!] Usage 1: ./DirBrute.py -u <url> -w <wordlist>")
        print("[!] Usage 2: ./DirBrute.py -u <url> -w <wordlist> -t <threads>")
try:
    main()
except KeyboardInterrupt:
    os._exit(1)
