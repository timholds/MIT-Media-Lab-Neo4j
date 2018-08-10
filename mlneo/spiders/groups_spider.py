import scrapy
import re

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

        group_pages = response.xpath('//div/@data-href').extract()

        if group_pages is not None:

            selector = 'groups.*overview'

            for group_page in group_pages:

                group_name_long = re.search(selector, group_page).group(0)
                group_name = group_name_long[7:-9]
                print('Group is ' + group_name)

                group_page = response.urljoin(group_page)
                print('The group page is' + str(group_page))
                yield scrapy.Request(group_page, callback=self.parse_group, meta={'group': group_name})


    def parse_group(self, response):

        # For each group's page, we want info on their status, people, projects, and research topics

        # Find if the words "was active" are here to see if the project is archived
        archived_data = response.css('.variant-archived::text').extract()
        print(str(archived_data))
        selector = 'was\sactive'

        #people_links = response.xpath('//div/@data-href').extract()
        #projects_links = response.xpath('//div/@data-href').extract()

        if bool(re.search(selector, str(archived_data))) is True:
            active = False
        else:
            active = True

        yield {
            'group': response.meta['group'],
            #'people' : response.css(''),
            #'projects' : response.css(''),
            'active' : active,
            'topics' : response.css('a::text').re('^#.*')
        }




