from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from tqdm import tqdm

class Scraper:
    BASE_URL = "https://www.bisnis.com"

    def check_connection(self, url=None, retries=3):
        for attempt in range(1, retries + 1):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                try:
                    target_url = url if url else self.BASE_URL
                    page.goto(target_url, timeout=30000)
                    page.wait_for_selector("body", timeout=30000)
                    print(f"Connection to {target_url} successful. Page title:", page.title())
                    page.close()
                    browser.close()
                    return True
                except Exception as e:
                    print(f"Attempt {attempt}: Failed to connect to bisnis.com: {e}")
                    page.close()
                    browser.close()
                    if attempt == retries:
                        return False
                    print("Retrying connection...")

    def get_articles_by_date_range(self, start_date, end_date, max_articles=10):
        indeks_url = f"{self.BASE_URL}/index?categoryId=0&type=indeks&date={start_date}&page=1"
        if not self.check_connection(indeks_url):
            print("Cannot connect to bisnis.com indeks page. Aborting scraping.")
            return []
        
        all_articles = []
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            while current_date <= end_date_dt:
                date_articles = []
                date_str = current_date.strftime("%Y-%m-%d")
                page = 1
                while True:
                    url = f"{self.BASE_URL}/index?categoryId=0&type=indeks&date={date_str}&page={page}"
                    page_obj = context.new_page()
                    page_obj.goto(url)
                    items = page_obj.query_selector_all("div.artItem")
                    if not items:
                        page_obj.close()
                        break
                    for item in tqdm(items, desc=f"Scraping {date_str}", total=min(len(items), max_articles)):
                        if len(date_articles) >= max_articles:
                            break
                        content_link_tag = item.query_selector("div.artContent > a.artLink")
                        link = content_link_tag.get_attribute("href") if content_link_tag else ""
                        title_tag = item.query_selector("div.artContent > a.artLink > h4.artTitle")
                        title = title_tag.inner_text().strip() if title_tag else ""
                        category_tag = item.query_selector("div.artContent > div.artChannel a")
                        category = category_tag.inner_text().strip() if category_tag else ""
                        date_tag = item.query_selector("div.artContent > div.artDate")
                        date_str_item = date_tag.inner_text().strip() if date_tag else ""
                        published_date = self._parse_date(date_str_item)
                        content = self._get_article_content(context, link)
                        date_articles.append({
                            "link": link,
                            "title": title,
                            "category": category,
                            "content": content,
                            "published_date": published_date
                        })
                    page_obj.close()
                    if len(date_articles) >= max_articles:
                        break
                    page += 1
                all_articles.extend(date_articles)
                current_date += timedelta(days=1)
            browser.close()
        return all_articles

    def get_latest_articles(self, max_articles=10):
        if not self.check_connection():
            print("Cannot connect to bisnis.com. Aborting scraping.")
            return []
        
        articles = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page_obj = context.new_page()
            page_obj.goto(self.BASE_URL)
            items = page_obj.query_selector_all("div.artItem")
            for item in tqdm(items, desc="Scraping latest articles", total=max_articles):
                if len(articles) >= max_articles:
                    break
                link_tag = item.query_selector("a.artLink")
                link = link_tag.get_attribute("href") if link_tag else ""
                title_tag = item.query_selector("h4.artTitle")
                title = title_tag.inner_text().strip() if title_tag else ""
                date_tag = item.query_selector("div.artDate")
                date_str = date_tag.inner_text().strip() if date_tag else ""
                category_tag = item.query_selector("div.artChannel a")
                category = category_tag.inner_text().strip() if category_tag else ""
                published_date = self._parse_date(date_str)
                content = self._get_article_content(context, link)
                articles.append({
                    "link": link,
                    "title": title,
                    "category": category,
                    "content": content,
                    "published_date": published_date
                })
            page_obj.close()
            browser.close()
        return articles

    def _get_article_content(self, context, link):
        if not link.startswith("http"):
            link = self.BASE_URL + link
        page_obj = context.new_page()
        try:
            page_obj.goto(link, timeout=60000)
            content_tag = page_obj.query_selector("article.detailsContent")
            content = content_tag.inner_text().strip() if content_tag else ""
        except Exception as e:
            print(f"Failed to load article: {link}\nError: {e}")
            content = ""
        page_obj.close()
        return content

    def _parse_date(self, date_str):
        # Try to parse "1 menit yang lalu" or "22 Jul 2025, 10:00 WIB"
        try:
            if "menit yang lalu" in date_str or "jam yang lalu" in date_str:
                # Use current time for relative dates
                return datetime.now().isoformat()
            dt = datetime.strptime(date_str, "%d %b %Y, %H:%M WIB")
            return dt.isoformat()
        except Exception:
            return date_str