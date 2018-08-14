import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "project group"

    def start_requests(self):
        for i in range(0, 47):
            urls = [
            'https://www.media.mit.edu/search/?page={}&filter=project'.format(i),
            ]

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        proj_titles = response.css('.module-title::text').extract()
        # TODO figure out how to get links to each project's page
        proj_links = response.css('').extract()

        assert len(proj_titles) == len(proj_links)

        projects = zip(proj_titles, proj_links)

        for project in projects:
            yield scrapy.Request(url=project[1], callback=self.parse_project, meta={'title': project[0]})


    def parse_project(self, response):

        proj_title = response.meta['title']

        # TODO find out if a project is active and what group it belongs to from its project page
        active = response.css('').extract()
        group = response.css('').extract()

        yield {
            'project_title': proj_title,
            'active': active,
            'group': group,

        }
