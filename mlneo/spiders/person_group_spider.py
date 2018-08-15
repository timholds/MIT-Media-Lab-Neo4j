import scrapy

class ProjectsSpider(scrapy.Spider):
    name = "group_person"

    def start_requests(self):
        urls = ['http://www.media.mit.edu/search/?page=1&filter=group',
                'http://www.media.mit.edu/search/?page=2&filter=group']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):


        group_names = response.css('.module-title::text').extract()
        group_links_end = response.xpath('//div/@data-href').extract()

        group_people_links = []

        for item in group_links_end:
            link = 'http://www.media.mit.edu{}people'.format(item[:-9])
            group_people_links.append(link)
            print('People links for {} is {}'.format(item, link))


        assert len(group_names) == len(group_people_links)

        groups = zip(group_names, group_people_links)

        for group in groups:
            yield scrapy.Request(url=group[1], callback=self.parse_group, meta={'group_name': group[0]})



    def parse_group(self, response):

        group_name = response.meta['group_name']
        people = response.css('.module-title::text').extract()


        #active = response.css('').extract()

        for person in people:
            yield {
                'group_name': group_name,
                'person': person,
                #'active': active,

            }


    '''
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
        #active = response.css('').extract()

        yield {
            'person': name,
            'position' : position,
            'group' : group,
            #'active' : active,

        }
    '''
