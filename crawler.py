# Simple python web crawler
# 
# To-Do:
# [x] Error handling function for port number validation
# [x] Search page source code for links/anchors
# [ ] Add scope definition functionality to avoid crawling external links like ads
# [ ] Download all pages found with 200 status code
# [ ] Check robots.txt for links
# [x] Maintain a set or list of already-crawled URLs to prevent loops
# [x] Output file
# [x] Verbose output
# [x] Recursive functionality
# [x] Depth functionality
# [ ] Crawl subdomains?
# [x] Separate into functions to make code more readable
# [ ] Ignore local anchors (#)
# [ ] Ignore files (for now)
# [ ] Add file type specification
# [ ] Filter out mailto, etc.

# Import libraries
from os import system,name # For screen clear function
from bs4 import BeautifulSoup # For easy web scraping
from urllib.parse import urlparse,urljoin # For easy URL parsing
import requests
import argparse
import re # Regex

# Clear screen function for clean output
def clear():
    if name == "nt":
        _ = system("cls")
    else: 
        _ = system("clear")


# Request webpage
def get_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Crawling {url}...") # DEBUG
            return response.text
        else:
            print(f"Received status code {response.status_code} from {url}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error reaching {url}: {e}")


# Normalize domains for consistency
def normalize_domain(domain):
    return domain.lower().lstrip("www.")


# Web crawling function
def crawl(current_url, args, visited, recursive, depth):
    if depth > args.depth: # Implement a check to end crawling at appropriate depth
        return
    
    url_list = []

    # Set url to variable
    html_document = (get_url(current_url))
    if not html_document:
        return

    # Parse the html source code
    soup = BeautifulSoup(html_document, 'html.parser')
    parsed_url = urlparse(current_url)
    target_domain = normalize_domain(parsed_url.netloc) # Process the user-specified link

    # For all links in source code
    for link in soup.find_all('a', href=True):
        link_url = urljoin(current_url, link.get('href'))
        link_domain = normalize_domain(urlparse(link_url).netloc) # Process the link for each link found

        #print(parsed_url.netloc) #(DEBUG - prints domain name)

        if link_url in visited:
            continue
        visited.add(link_url) # Add URL to visited set to avoid endless loops
        
        # If it's part of the domain, pull links from page
        if link_domain == target_domain: # Compare user-specified link with discovered link
            url_list.append(link_url) # Add the valid link to an array
        
            if args.verbose:
                #print(link_url)
                print(f"[Depth {depth}] {link_url}")

            if args.output:
                args.output.write(link_url + '\n')

            # RECURSE
            if recursive:
                # 1. search initial specified domain for links 
                # 2. search all disovered links for more links
                crawl(link_url, args, visited, recursive, depth + 1)  

# Main
def main():
    # Initialize arrays
    visited = set()

    while True:
        clear()

        parser = argparse.ArgumentParser(
            usage="crawler.py -u target [options]",
            description="crawler.py -h for help",
            add_help=True,
            allow_abbrev=True,
        )

        # Argument options
        parser.add_argument("-u", "--url", type=str, required=True, help="Specify target URL")
        parser.add_argument("-p", "--port", type=int, help="Specify target port")
        parser.add_argument("-o", "--output", type=argparse.FileType('w', encoding='latin-1'), help="Specify output location")
        parser.add_argument("-r", "--recursive", action="store_true",help="Enable recursive crawling")
        parser.add_argument("-d", "--depth", type=int, default=1,  help="Depth for recursive crawling")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

        args = parser.parse_args()

        if args.depth > 1 and not args.recursive:
            parser.error("--depth requires --recursive to be specified")

        # Error handling. If URL does not include protocol, include it for consistency
        if not args.url.startswith(("http://", "https://")):
            if args.port == 443:
                args.url = "https://" + args.url
            else:
                args.url = "http://" + args.url

        # Append port to URL if specified
        if args.port is not None and (args.port not in range(1,65536)):
            parser.error("Port must be between 1 and 65535")
        break

    if args.port is not None:
        args.url += f":{args.port}"

    # Call crawl function
    crawl(args.url, args, visited, args.recursive, 0)

    # Close output file if it was opened
    if args.output:
        args.output.close()

main()