import socket
import sys
import re
import hashlib
import os

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)



def print_help():
    print("Usage:")
    print("  go2web -u <URL>         # make an HTTP request to the specified URL and print the response")
    print("  go2web -s <search-term> # search using DuckDuckGo and print top 10 results")
    print("  go2web -h               # show this help")

def extract_text(html):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def url_to_filename(url):
    return hashlib.md5(url.encode()).hexdigest() + ".txt"

def get_from_cache(url):
    filename = os.path.join(CACHE_DIR, url_to_filename(url))
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_to_cache(url, content):
    filename = os.path.join(CACHE_DIR, url_to_filename(url))
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def fetch_raw_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    cached = get_from_cache(url)
    if cached:
        print("⚡ Loaded from cache")
        return cached

    try:
        domain = url.split("//")[1].split("/")[0]
        path = "/" + "/".join(url.split("//")[1].split("/")[1:])

        port = 80
        request = f"GET {path} HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((domain, port))
            s.sendall(request.encode())
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data

        response_text = response.decode(errors="ignore")
        body = response_text.split("\r\n\r\n", 1)[1]

        save_to_cache(url, body)
        return body
    except Exception as e:
        return f"Error fetching data: {e}"

def handle_search(term):
    query = term.replace(" ", "+")
    search_url = f"http://html.duckduckgo.com/html/?q={query}"
    html = fetch_raw_http(search_url)

    # Extract and print top 10 results
    results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', html)
    for i, (link, title) in enumerate(results[:10]):
        print(f"{i+1}. {extract_text(title)}")
        print(f"   {link}\n")

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    option = sys.argv[1]

    if option == "-h":
        print_help()

    elif option == "-u" and len(sys.argv) >= 3:
        url = sys.argv[2]
        html = fetch_raw_http(url)
        print(extract_text(html))

    elif option == "-s" and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        handle_search(term)

    else:
        print("Invalid arguments.\n")
        print_help()

if __name__ == "__main__":
    main()
