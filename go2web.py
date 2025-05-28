import socket
import re

def strip_html_tags(html):
    clean_text = re.sub('<[^<]+?>', '', html)  # Removes all tags like <tag>
    return clean_text.strip()

def handle_url(url):
    if not url.startswith("http://"):
        url = "http://" + url

    host = url.split("//")[1].split("/")[0]
    path = "/" + "/".join(url.split("//")[1].split("/")[1:])

    if path == "/":
        path = "/"

    port = 80
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

    response_text = response.decode(errors='ignore')
    headers, _, body = response_text.partition("\r\n\r\n")
    
    print("Clean Output:")
    print(strip_html_tags(body))
