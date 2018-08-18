import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "project_person"

    def start_requests(self):
        for i in range(0, 47):
            urls = [
            'http://www.media.mit.edu/search/?page={}&filter=project'.format(i),
            ]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        proj_titles = response.css('.module-title::text').extract()
        proj_links = response.xpath('//div/@data-href').extract()

        proj_people_links = []

        for item in proj_links:
            link = 'http://www.media.mit.edu{}people'.format(item[:-9])
            proj_people_links.append(link)
            print('People links for {} is {}'.format(item, link))

        assert len(proj_titles) == len(proj_people_links)

        projects = zip(proj_titles, proj_people_links)

        for project in projects:
            yield scrapy.Request(url=project[1], callback=self.parse_project, meta={'title': project[0]})


    def parse_project(self, response):

        proj_title = response.meta['title']
        people = response.css('.module-title::text').extract()
        positions = response.css('.module-subtitle::text').extract()

        for person in people:
            index = 0
            yield {
                'project_title': proj_title,
                'person' : person,
                'position': positions[index],

            }
            index += 1
