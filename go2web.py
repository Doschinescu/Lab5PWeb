import socket
import ssl
import sys
import re

def print_help():
    print("""
Usage:
  go2web -u <URL>         # make an HTTP request to the specified URL and print the response
  go2web -s <search-term> # search using DuckDuckGo and print top 10 results
  go2web -h               # show this help
""")

def fetch_raw_http(host, path="/", redirect_count=0):
    if redirect_count > 3:
        print("❌ Too many redirects")
        return None

    port = 443
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nUser-Agent: go2web-cli\r\n\r\n"

    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.sendall(request.encode())
            response = b""
            while True:
                chunk = ssock.recv(4096)
                if not chunk:
                    break
                response += chunk

    decoded = response.decode(errors="ignore")

    # Check for redirect status codes
    status_line = decoded.split("\r\n")[0]
    headers = decoded.split("\r\n\r\n")[0]
    status_code = int(status_line.split()[1])

    if status_code in [301, 302]:
        location_match = re.search(r"Location: (.+)", headers)
        if location_match:
            new_url = location_match.group(1).strip()
            print(f"➡️ Redirecting to: {new_url}")

            if new_url.startswith("http"):
                new_url = new_url.replace("http://", "").replace("https://", "")
            parts = new_url.split("/", 1)
            new_host = parts[0]
            new_path = "/" + parts[1] if len(parts) > 1 else "/"
            return fetch_raw_http(new_host, new_path, redirect_count + 1)
    
    return decoded


def search_duckduckgo(query):
    search_term = '+'.join(query)
    host = "html.duckduckgo.com"
    path = f"/html?q={search_term}"

    response = fetch_raw_http(host, path)

    # Extract top 10 search result titles and URLs
    results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', response)
    
    if not results:
        print("No results found or parsing failed.")
        return
    
    print(f"\n🔍 Top results for: {' '.join(query)}\n")
    for i, (url, title) in enumerate(results[:10], start=1):
        clean_title = re.sub('<.*?>', '', title)  # Strip HTML tags
        print(f"{i}. {clean_title}\n   {url}\n")

def fetch_url(url):
    if not url.startswith("http"):
        url = "http://" + url

    try:
        url = url.replace("http://", "").replace("https://", "")
        parts = url.split("/", 1)
        host = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else "/"
        response = fetch_raw_http(host, path)

        if response:
            body = response.split("\r\n\r\n", 1)[1]
            print(body)
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1]

    if cmd == "-h":
        print_help()
    elif cmd == "-u" and len(sys.argv) >= 3:
        fetch_url(sys.argv[2])
    elif cmd == "-s" and len(sys.argv) >= 3:
        search_duckduckgo(sys.argv[2:])
    else:
        print("❌ Invalid arguments.\n")
        print_help()

if __name__ == "__main__":
    main()
