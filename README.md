🚀 go2web – A Minimal Web Client using Raw Sockets
This command-line tool performs HTTP GET requests using raw TCP sockets, with no built-in or third-party HTTP libraries.

📜 Features
go2web -u <URL>
Makes a raw HTTP request to the specified URL and prints a readable response (HTML stripped).

go2web -s <search-term>
Sends a search query to DuckDuckGo and prints the top 10 clean search results.

go2web -h
Displays usage help.

✅ Human-readable output (HTML stripped)

✅ Caching of fetched pages to improve speed and efficiency

✅ Custom CLI using sys.argv

✅ Fully compliant with lab requirements (no HTTP libs, CLI only)

⚙️ How It Works
TCP Sockets are used to send HTTP/1.1 requests to servers on port 80.

The HTML response is split into header and body.

HTML tags are removed using regular expressions, making the response easy to read.

A basic cache is implemented using hashed filenames in a local directory.

The search feature uses DuckDuckGo’s HTML-only interface (html.duckduckgo.com), scraping anchor tags for results.

🛠 Technologies & Concepts
Python 3

socket for networking

sys for CLI parsing

re for HTML parsing

hashlib & os for cache management

DuckDuckGo as search engine provider (no API key needed)

📦 Usage
bash
python go2web.py -h
python go2web.py -u example.com
python go2web.py -s mercedes cars
⚠️ If you get a "Python not found" error, ensure Python is installed and added to your system PATH.

📁 Project Structure
php-template
go2web.py
cache/
  └── <hashed-urls>.txt
✅ Lab Requirements Checklist
Feature	Status
CLI with -h, -u, -s options	✅ Done
Raw socket HTTP request	✅ Done
Human-readable HTML response	✅ Done
Search engine integration (DuckDuckGo)	✅ Done
Top 10 search results parsed	✅ Done
HTTP Caching	✅ Done
Good Git commit history	✅ You followed step-by-step development!
