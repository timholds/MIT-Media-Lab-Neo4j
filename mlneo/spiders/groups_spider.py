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

        for group in response.css('.module-title::text').extract():
            yield {
                'group': group,
            }

        #yield {
            #'group' : response.css('.module-title::text').extract()
            #'topics' : response.css('a::text').re('^#.*'),
            #'name': response.css('.module-title::text').extract_first(),
        #}

        #next_page = response.css('li.next a::attr(href)').extract_first()
        #if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)