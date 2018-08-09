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
        for student in response.css('.module-head'):
            yield {
                'name': student.css('.module-title::text').extract_first(),
                'position': student.css('.module-subtitle::text').extract_first(),
            }

        page_long = response.url.split("/")[-1]
        page = page_long[6:]
        filename = 'students-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)