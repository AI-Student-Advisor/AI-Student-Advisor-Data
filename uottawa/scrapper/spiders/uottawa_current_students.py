import scrapy
from scrapy.crawler import CrawlerProcess
import unicodedata
import uuid
from items.items import VectorStoreItem

class UottawaCurrentStudentsSpider(scrapy.Spider):
    name = 'uottawa_current_students'
    start_urls = ['https://www.uottawa.ca/current-students']

    def parse(self, response):
        # Use XPath to select anchor elements with href starting with "https://www.uottawa.ca/"
        uottawa_links = response.xpath('//a[starts-with(@href, "https://www.uottawa.ca/")]')
        # Follow all the links
        yield from response.follow_all(uottawa_links, self.parse_subpage)

    def parse_subpage(self, response):
        # Select all text within div, p, span, headings
        text_elements = response.xpath("//div//text() | //p//text() | //span//text() | //h1//text() | //h2//text() | //h3//text() | //h4//text() | //h5//text() | //h6//text()")
        # Parse the text elements
        for text in text_elements:
            if self.validate_text(text):
                yield from self.parse_text(text, response)
    
    def validate_text(self, text):
        """
        Text should:
        - not be empty
        - have more than 200 characters
        - start with a letter, number or quotation marks
        - not be a link
        """
        text = text.get().strip()
        if not text:
            return False
        if len(text) < 200:
            return False
        if not text[0].isalnum() and text[0] not in ['"', "'"]:
            return False
        if text.startswith("http"):
            return False
        return True

    def parse_text(self, text, response):
        text = text.get()
        text = unicodedata.normalize("NFKD", text)
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = text.replace("\r", " ")
        text = text.replace("  ", " ")
        text = text.strip()
        yield VectorStoreItem(
            id=str(uuid.uuid4()),
            text=text,
            source=response.url,
            metadata={},
        )

process = CrawlerProcess(
    settings={
      "FEEDS": {
        "../data/uottawa_current_students_data.jsonl": {
          "overwrite": True,
          "format": "jsonlines",
          "encoding": "utf8",
          },
        },
      }
    )
process.crawl(UottawaCurrentStudentsSpider)
process.start()