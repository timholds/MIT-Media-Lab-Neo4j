import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "projects"

    def start_requests(self):
        for i in range(0, 47):
            urls = [
            'https://www.media.mit.edu/search/?page={}&filter=project'.format(i),
            ]

            for url in urls:
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        for title in response.css('.module-title::text').extract():
            yield {
                'title': title,
            }

        page_long = response.url.split("/")[-1]
        page = page_long[6:8]
        filename = 'projects-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    #custom_settings = {
        #"DOWNLOAD_DELAY": 1,
        #"CONCURRENT_REQUESTS_PER_DOMAIN": 2
    #}

