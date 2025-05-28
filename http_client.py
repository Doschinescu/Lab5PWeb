import socket
from urllib.parse import urlparse

def fetch_http(url):
    parsed = urlparse(url if url.startswith("http") else "http://" + url)

    host = parsed.hostname
    port = parsed.port or 80
    path = parsed.path if parsed.path else "/"

    # Create the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

    # Decode and split response
    response_str = response.decode(errors="ignore")
    headers, _, body = response_str.partition("\r\n\r\n")
    return headers, body
