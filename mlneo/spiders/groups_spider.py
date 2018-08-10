import scrapy

class GroupSpider(scrapy.Spider):
    name = "groups"

    # We want to start on the groups page with all groups
    # Let's get the name of the group and the link to their page
    # For each individual group:
    #   We want to get all their research topics
    #   We want to get all of their projects, with a label for archived or active
    #   We want to get all of their students and professors

    def start_requests(self):

        urls = ['https://www.media.mit.edu/search/?page=1&filter=group',
                'https://www.media.mit.edu/search/?page=2&filter=group']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # We want to get the group name from the page with all the group names
        for group in response.css('.module-title::text').extract():

            yield {
                'group': group
            }

            group_pages = response.xpath('//div/@data-href').extract()
            print(group)
            print(group_pages)
'''
            if group_pages is not None:
                for group_page in group_pages:
                    group_page = response.urljoin(group_page)
                    print(group_page)
                    yield scrapy.Request(group_page, callback=self.parse_group(group))
'''
'''
    def parse_group(self, response, group):

        # For each group's page, we want info on their people, projects, and research fields
        yield {
            'group': group,
            'people' : response.css(''),
            'projects' : response.css(''),
            'topics' : response.css('a::text').re('^#.*')
        }
'''



