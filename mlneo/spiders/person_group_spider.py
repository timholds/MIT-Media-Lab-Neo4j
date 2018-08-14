import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "person group"

    def start_requests(self):
        for i in range(1, 25):
            urls = [
            'https://www.media.mit.edu/search/?page={}&filter=person'.format(i),
            ]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        names = response.css('.module-title::text').extract()
        # TODO get links to each person's individual page
        name_links = response.css('').extract()

        people = zip(names, name_links)

        for person in people:
            yield scrapy.Request(url=person[1], callback=self.parse_people, meta={'name': person[0]})



    def parse_people(self, response):

        name = response.meta['name']

        # TODO figure out how to grab position and group from someone's page
        position = response.css('').extract()
        group = response.css('').extract()
        active = response.css('').extract()

        yield {
            'person': name,
            'position' : position,
            'group' : group,
            'active' : active,

        }
