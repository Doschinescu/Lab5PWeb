from parser import parse_args

def main():
    args = parse_args()

    if args.url:
        print(f"Fetching URL: {args.url}")
        # HTTP request code goes here

    elif args.search:
        search_term = ' '.join(args.search)
        print(f"Searching for: {search_term}")
        # Search engine logic goes here

    else:
        print("Use -h to see help.")

if __name__ == "__main__":
    main()
