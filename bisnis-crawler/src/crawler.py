import json
import time
from datetime import datetime
from scraper import Scraper

class Crawler:
    def __init__(self, interval=300):
        self.scraper = Scraper()
        self.interval = interval  # seconds, for standard mode

    def backtrack(self, start_date, end_date):
        print(f"Backtrack mode: {start_date} to {end_date}")
        articles = self.scraper.get_articles_by_date_range(start_date, end_date)
        if articles:  # Only save if articles were scraped
            filename = f"bisnis_backtrack_{start_date}_to_{end_date}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(articles)} articles to {filename}")
        else:
            print("No articles scraped. Nothing saved.")

    def standard(self):
        print("Standard mode: running periodic crawl (press Ctrl+C to stop)")
        try:
            while True:
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                articles = self.scraper.get_latest_articles()
                if articles:  # Only save if articles were scraped
                    filename = f"bisnis_latest_{now}.json"
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(articles, f, ensure_ascii=False, indent=2)
                    print(f"[{now}] Saved {len(articles)} articles to {filename}")
                else:
                    print(f"[{now}] No articles scraped. Nothing saved.")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Stopped standard mode.")