# HackerOne  Scraper

A Python scraper that downloads and filters disclosed HackerOne vulnerability reports, organized by bug type category. Built on top of the report list from [reddelexc/hackerone-reports](https://github.com/reddelexc/hackerone-reports).

> **Special thanks** to [@reddelexc](https://github.com/reddelexc/hackerone-reports)

## What It Does

The scraper reads the markdown files from `hackerone-reports/tops_by_bug_type/`, extracts all report URLs, fetches each report's JSON from HackerOne, and saves a filtered version locally. Only reports with actual vulnerability information are saved.


## Usage

#### 1. Clone the hackerone-reports repo inside this project

```
git clone https://github.com/reddelexc/hackerone-reports
```

#### 2. Run the scraper

```
python3 scrapper.py`
```

A `reports/` folder will be created with one subfolder per bug type category. Each subfolder contains the filtered JSON files for the reports in that category.
