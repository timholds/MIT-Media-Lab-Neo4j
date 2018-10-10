import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "group_projects"

    def start_requests(self):
        urls = ['http://www.media.mit.edu/search/?page=1&filter=group',
                'http://www.media.mit.edu/search/?page=2&filter=group']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):


        group_names = response.css('.module-title::text').extract()
        group_links_end = response.xpath('//div/@data-href').extract()

        group_proj_links = []

        for item in group_links_end:
            link = 'http://www.media.mit.edu{}projects'.format(item[:-9])
            group_proj_links.append(link)
            print('Group links for {} is {}'.format(item, link))


        assert len(group_names) == len(group_proj_links)

        groups = zip(group_names, group_proj_links)

        for group in groups:
            yield scrapy.Request(url=group[1], callback=self.parse_group, meta={'group_name': group[0]})



    def parse_group(self, response):

        group_name = response.meta['group_name']
        proj_titles = response.css('.module-title::text').extract()


        #active = response.css('').extract()

        for project_title in proj_titles:
            yield {
                'group_name': group_name,
                'project_title': project_title,
                #'active': active,

            }

