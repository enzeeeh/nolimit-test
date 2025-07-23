import argparse
from crawler import Crawler

def main():
    parser = argparse.ArgumentParser(description='Run the bisnis.com web crawler.')
    parser.add_argument('--mode', choices=['backtrack', 'standard'], required=True,
                        help='Mode to run the crawler in: backtrack or standard.')
    parser.add_argument('--start-date', type=str, help='Start date for backtrack mode (YYYY-MM-DD).')
    parser.add_argument('--end-date', type=str, help='End date for backtrack mode (YYYY-MM-DD).')
    parser.add_argument('--interval', type=int, default=300,
                        help='Interval in seconds for standard mode (default: 300).')

    args = parser.parse_args()

    crawler = Crawler(interval=args.interval)

    if args.mode == 'backtrack':
        if not args.start_date or not args.end_date:
            print("Please provide both start and end dates for backtrack mode.")
            return
        crawler.backtrack(args.start_date, args.end_date)
    elif args.mode == 'standard':
        crawler.standard()

if __name__ == '__main__':
    main()