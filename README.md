# Bisnis.com News Scraper

## Overview
This project is a Python-based web scraper for [bisnis.com](https://www.bisnis.com) that collects news articles using Playwright.

## Features:
* Scrapes latest articles from the homepage (standard mode)
* Scrapes articles by date range from the indeks page (backtrack mode)
* Extracts: link, title, category, content, published date
* Saves results as JSON files

## Main Components

### Scraper Class (src/scraper.py)
* `check_connection`: Checks if the target page is reachable, with retry logic.
* `get_latest_articles`: Scrapes up to N latest articles from the homepage.
* `get_articles_by_date_range`: Scrapes up to N articles per day for a given date range from the indeks page.
* `_get_article_content`: Opens each article link and extracts the main content.
* `_parse_date`: Converts date strings to ISO format.

### Crawler Class (src/crawler.py)
* `standard`: Periodically scrapes the latest articles and saves them. Stops with Ctrl+C.
* `backtrack`: Scrapes articles for a given date range and saves them.

## How to Run

1.  **Install dependencies**

    ```bash
    pip install playwright tqdm
    python -m playwright install
    ```

2.  **Run in Standard Mode (latest articles)**

    ```bash
    python src/main.py --mode standard
    ```
    * Scrapes the latest articles from the homepage.
    * Saves results as `bisnis_latest_YYYYMMDD_HHMMSS.json`.

3.  **Run in Backtrack Mode (by date range)**

    ```bash
    python src/main.py --mode backtrack --start-date YYYY-MM-DD --end-date YYYY-MM-DD
    ```
    **Example:**
    ```bash
    python src/main.py --mode backtrack --start-date 2025-01-01 --end-date 2025-01-02
    ```
    * Scrapes articles for each date in the range.
    * Saves results as `bisnis_backtrack_STARTDATE_to_ENDDATE.json`.

4.  **Output**
    Scraped articles are saved as JSON files in the project folder. Each file contains a list of articles with all extracted fields.

## Notes
* If the connection fails, no file is saved.
* Progress bars are shown during scraping.
* For debugging, you can set `headless=False` in the code to see the browser window.

## Troubleshooting
* If you get timeout errors, check your internet connection or try increasing the timeout value.
* Some articles may not load due to website restrictions; these are skipped.
