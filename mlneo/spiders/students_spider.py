import scrapy

class StudentSpider(scrapy.Spider):
    name = "students"

    def start_requests(self):

        urls = [
            'https://www.media.mit.edu/people/?filter=student',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #student_urls in response.css
        for student in response.css('.module-head'):
            yield {
                'name': student.css('.module-title::text').extract_first(),
                'position': student.css('.module-subtitle::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)