# Bisnis Crawler

## Overview
The Bisnis Crawler is a web crawler and scraper designed to retrieve articles from bisnis.com. It operates in two modes: **backtrack** and **standard**. The backtrack mode allows users to fetch articles published within a specific date range, while the standard mode continuously retrieves the latest articles.

## Project Structure
```
bisnis-crawler
├── src
│   ├── crawler.py       # Contains the Crawler class with backtrack and standard methods
│   ├── scraper.py       # Contains the Scraper class for extracting article details
│   ├── main.py          # Entry point for executing the crawler
│   └── utils
│       └── __init__.py  # Utility functions and constants
├── requirements.txt      # Lists project dependencies
├── Dockerfile             # Docker configuration for the project
└── README.md              # Project documentation
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Crawler
You can run the crawler in either backtrack or standard mode using the command line.

### Backtrack Mode
To run the crawler in backtrack mode, specify the start and end dates:

```bash
python src/main.py backtrack --start YYYY-MM-DD --end YYYY-MM-DD
```

### Standard Mode
To run the crawler in standard mode, simply execute:

```bash
python src/main.py standard
```

## Architecture
The project is structured to separate concerns between crawling and scraping. The `Crawler` class handles the logic for fetching articles, while the `Scraper` class is responsible for parsing the HTML content and extracting relevant details. Utility functions are provided in the `utils` module to support various operations, such as date formatting.

## Docker
To build and run the project using Docker, use the following commands:

```bash
docker build -t bisnis-crawler .
docker run bisnis-crawler
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.