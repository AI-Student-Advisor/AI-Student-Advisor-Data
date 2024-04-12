# University of Ottawa Scrapper

Scrapy based utility program to scrape the University of Ottawa's data and output the data in a JSON output file, which can be used to create vector store on hosted vector database.

## Installation

All commands from `uottawa/scrapper` directory level.

1. Setup virtual python environment

```bash
python3 -m venv .venv
```

2. Activate the virtual environment

```bash
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run crawler script

```bash
python crawler.py
```

1. Output generated in directory `uottawa\data` as `uottawa_data.jsonl`

## Overview

This scrapper is meant to scrap data related to University of Ottawa from its various websites and webpages. For each of the websites or webpages scrapped, a seperate scrapping logic is defined in the `spiders` directory in individual files. These scrappers are then run from the `crawler.py` file. The combined output is then stored in the `data` directory as a JSON line file.

The output JSON line file follows the Open AI embedding format. The format is as follows:

```json
{
  "id": "unique id",
  "text": "text to be embedded",
  "source": "source of text"
  "metadata": "additional information"
}
```

## Scrappers

The following scrappers are defined in the `spiders` directory:

- `uottawa_catalog.py`: This scrapper is meant to recursively scrap the course catalog of the University of Ottawa. The course catalog is available at [https://catalogue.uottawa.ca/en/courses/](https://catalogue.uottawa.ca/en/courses/). The scrapper extracts the details related to all the courses available on the catalog website.
- `uottawa_current_students.py`: This scrapper is meant to recursively scrap the current students page of the University of Ottawa. The current students page is available at [https://www.uottawa.ca/current-students](https://www.uottawa.ca/current-students). This scrapper recursively extracts all the links available on the page and then extracts the text from the links as well, for example, it includes CO-OP info, Financial Aid, Library, etc.
- `uottawa_faculty_staff.py`: This scrapper is meant to recursively scrap the faculty and staff page of the University of Ottawa. The faculty and staff page is available at [https://www.uottawa.ca/about-us/faculty-staff](https://www.uottawa.ca/about-us/faculty-staff). This scrapper recursively extracts all the links available on the page and then extracts the text from the links as well, for example, it includes technical support resources for professors, Teaching and Learning Support Service (TLSS), etc.
