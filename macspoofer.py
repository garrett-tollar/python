#!/usr/bin/env python

import subprocess
import argparse
import sys
import os


def clear():
    if name == "nt":
        _ = system("cls")
    else: 
        _ = system("clear")

def get_args():
    parser = argparse.ArgumentParser(
        prog="macspoofer.py",
        usage="%(prog)s [options]",
        add_help=True,
        allow_abbrev=True,
    )

    # Define arguments
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("-i", "--interface", required=False, type=str.lower, default="wlan0", metavar="", help="specify target interface (default: wlan0)")
    group.add_argument("-m", "--mac", required=False, type=str.lower, default="11:22:33:44:55:66", metavar="", help="specify desired MAC address (default: 11:22:33:44:55:66)")
    group.add_argument("-r", "--random", required=False, default=False, action="store_true", help="assign random MAC address")
    group.add_argument("-o", "--original", required=False, action="store_true", help="reset interface to original MAC address")
    group.add_argument("-c", "--current", required=False, action="store_true", help="display current MAC address")
    group.add_argument("-M", "--mode", required=False, choices=["monitor", "managed"], help="set wireless interface into monitor/managed mode")

    return parser.parse_args(), parser

def get_help(parser):
    parser.print_help()
    sys.exit(1) # Exit with an error code

def set_random():
    # Generate random 12-digit hex pair string
    raw_mac = str(os.urandom(6).hex())

    # Alter LSB to ensure unicast, locally administered address
    first_byte = int(raw_mac[:2], 16)
    first_byte = (first_byte | 0x02) & 0xFE
    first_byte_hex = f"{first_byte:02x}"

    # Format hex string with colon delimiters
    new_mac = ':'.join([first_byte_hex] + [raw_mac[i:i+2] for i in range(2, 12, 2)])

    return new_mac

def reset_original(interface):
    new_mac = subprocess.check_output(
        ["awk", "-F: ", "{print $2}"],
        input = subprocess.check_output(["ethtool", "-P", interface], text=True),
        text = True
    )

    print(f"[+] Resetting MAC address for {interface} back to {new_mac}")

def get_current(interface):
    new_mac = subprocess.check_output(
        ["awk", "-F: ", "{print $2}"],
        input = subprocess.check_output(["ethtool", "-P", interface], text=True),
        text = True
    )

    print(f"[+] Current {interface} MAC address: {new_mac}")    

def set_mac(interface, new_mac):
    steps = [
        (f"sudo ifconfig {interface} down", f"Bringing {interface} down"),
        (f"sudo ifconfig {interface} hw ether {new_mac}", f"Setting {interface} MAC address to {new_mac}"),
        (f"sudo ifconfig {interface} up", f"Bringing {interface} up")
    ]

    for cmd, desc in steps:
        print(f"[-] {desc}...")
        result = subprocess.call(cmd, shell=True)
        if result == 0:
            print(f"[+] {desc} completed successfully")
        else:
            print(f"[X] {desc} failed with exit code {result}")
            break

def change_state(interface, mode):
    steps = [
        (f"sudo ip link set {interface} down", f"Bringing {interface} down"),
        (f"sudo iw {interface} set type {mode}", f"Setting {interface} mode to {mode} mode"),
        (f"sudo ip link set {interface} up", f"Bringing {interface} up")
    ]

    for cmd, desc in steps:
        print(f"[-] {desc}...")
        result = subprocess.call(cmd, shell=True)
        if result == 0:
            print(f"[+] {desc} completed successfully")
        else:
            print(f"[X] {desc} failed with exit code {result}")
            break

def main():
    args, parser = get_args()

    if len(sys.argv) == 1: # If no other arguments are specified (program name counts as 1 argument)
        get_help(parser)

    if args.mac:
        new_mac = args.mac

    if args.random:
        new_mac = set_random()

    if args.current:
        get_current(args.interface)

    if args.original:
        reset_original(args.interface)
    else:
        set_mac(args.interface, new_mac)

    if args.mode:
        change_state(args.interface, args.mode)

if __name__ == "__main__":
    main()
