#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import json
import string
import random
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.provider import APIProvider
from utils.decorators import MessageDecorator

def format_phone(num):
    return ''.join([n for n in num if n in string.digits]).strip()

def get_phone_info():
    while True:
        cc = input("Enter your country code (Without +): ")
        cc = format_phone(cc)
        target = input(f"Enter the target number: +{cc} ")
        target = format_phone(target)
        if len(target) < 7 or len(target) > 15:
            print("Invalid phone number. Please try again.")
            continue
        return cc, target

def pretty_print(cc, target, success, failed):
    print(f"Target: +{cc} {target}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")

def workernode(cc, target, count, delay, max_threads):
    api = APIProvider(cc, target, "call")
    success, failed = 0, 0

    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = [executor.submit(api.hit) for _ in range(count - success)]
            for job in as_completed(jobs):
                result = job.result()
                if result:
                    success += 1
                else:
                    failed += 1
                pretty_print(cc, target, success, failed)
                time.sleep(delay)

    print("Bombing completed!")

def main():
    cc, target = get_phone_info()
    count = int(input("Enter number of calls to make: "))
    delay = float(input("Enter delay time (in seconds): "))
    max_threads = int(input("Enter number of threads: "))

    workernode(cc, target, count, delay, max_threads)

if __name__ == "__main__":
    main()
