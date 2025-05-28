import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="go2web: Simple HTTP client using raw sockets."
    )
    parser.add_argument('-u', '--url', type=str, help="Make an HTTP request to the specified URL")
    parser.add_argument('-s', '--search', type=str, nargs='+', help="Search a term using a search engine")
    return parser.parse_args()
