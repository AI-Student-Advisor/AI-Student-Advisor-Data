# uottawa_catalog_spider.py
import scrapy
from scrapy.crawler import CrawlerProcess
import unicodedata
import uuid
from items.items import UottawaCatalogItem, VectorStoreItem

class UottawaCatalogSpider(scrapy.Spider):
    name = "uottawa_catalog"
    start_urls = ["https://catalogue.uottawa.ca/en/courses"]

    def parse(self, response):
        # Use XPath to select anchor elements with href starting with "/en"
        en_links = response.xpath('//a[starts-with(@href, "/en")]')

        yield from response.follow_all(en_links, self.parseCourse)

    def parseCourse(self, response):
        item = UottawaCatalogItem()
        item["subject"] = response.css("div.page-title-area h1::text").get()

        for quote in response.css("div.courseblock"):
            yield self.parseCourseBlock(quote, item)

    def parseCourseBlock(self, courseblock, item):
        
        course_code, course_name, course_units = self.parseTitle(courseblock)

        item["course_code"] = course_code
        item["course_name"] = course_name
        item["course_units"] = course_units
        
        item["course_description"] = self.parseCourseDescription(courseblock)
        item["course_components"] = courseblock.css("p.courseblockextra::text")[0].get()
        item["course_prerequisites"] = self.parsePreRequisites(courseblock)
        
        vcText = f"Course code: {course_code}, course name: {course_name}, description: {item['course_description']} Credits: {course_units}. Course components: {item['course_components']}. Prerequisites, if any: {item['course_prerequisites']}"

        vcItem = VectorStoreItem(
            id=str(uuid.uuid4()),
            text=vcText,
            source=f"https://catalogue.uottawa.ca/en/courses/{course_code[:3].lower()}",
            metadata={
                "subject": item["subject"],
                "course_name": course_name, 
                "course_code": course_code, 
                "course_components": item["course_components"],
                "course_prerequisites": item["course_prerequisites"],
                "course_units": course_units},
        )

        return vcItem
    
    def parseTitle(self, courseblock):
        course_title = courseblock.css("p.courseblocktitle strong::text").get()
        open_parenthesis_index = course_title.find("(")
        course_units = self.parseCourseUnits(course_title)

        course_title = course_title[:open_parenthesis_index - 1]
        course_title = unicodedata.normalize("NFKD", course_title)

        course_title_split = course_title.split(" ")
        course_code = " ".join(course_title_split[:2])
        course_name = " ".join(course_title_split[2:])

        return course_code, course_name, course_units
    
    def parseCourseUnits(self, course_title):
        paran_idx = course_title.find("(")
        course_units = 0

        while paran_idx != -1 and not self.isParsableToInteger(course_title[paran_idx + 1]):
            paran_idx = course_title.find("(", paran_idx + 1)

        if paran_idx != -1:
            course_units = int(course_title[paran_idx + 1:paran_idx + 2])
    
        return course_units
    
    def isParsableToInteger(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
        
    def parseCourseDescription(self, courseblock):
        course_description = courseblock.css("p.courseblockdesc::text").get()
        if course_description is not None:
            course_description = course_description.replace("Prerequisite: ", "")
            return unicodedata.normalize("NFKD", course_description)
        else:
            return "course description not available"

    def parsePreRequisites(self, courseblock):
        result = ""
        for content in courseblock.css("p.courseblockextra.highlight"):
            a_tag = content.css("a::text").get()
            if a_tag is not None:
                result += a_tag
            else:
                result += content.css("::text").get()

        return unicodedata.normalize("NFKD", result) if result != "" else "None"

process = CrawlerProcess(
    settings={
      "FEEDS": {
        "../data/uottawa_catalog_data.jsonl": {
          "overwrite": True,
          "format": "jsonlines",
          "encoding": "utf8",
          },
        },
      }
    )
process.crawl(UottawaCatalogSpider)
process.start()