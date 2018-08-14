import scrapy
import re

# Plan - start urls for everything is the same but three different paths and three different spreadsheets

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

                group_link = response.urljoin(group_page)
                print('The group page is' + str(group_page))
                yield scrapy.Request(group_link, callback=self.parse_group_projects, meta={'group': group_name})


    # Get group data and for each group call the parse_projects_first method
    def parse_group_projects(self, response):

        # For each group's page, we want info on their status, people, projects, and research topics
        group = response.meta['group']

        # Find if the words "was active" are here to see if the project is archived
        group_archived = str(response.css('.variant-archived::text').extract())
        was_active = re.search('was\sactive', group_archived)
        if bool(was_active) is True:
            active = False
        else:
            active = True


        # Find all topics
        topics = response.css('a::text').re('^#.*')

        projects_link = str('https://www.media.mit.edu/groups/' + response.meta['group']) + '/projects/'
        yield scrapy.Request(projects_link, callback=self.parse_projects_first, meta={'group': response.meta['group'],
                                                                                     'active': active,
                                                                                     'topics': topics})

    # Get the names and links for a group's projects and call the parse_projects_second method
    def parse_projects_first(self, response):

        # Variables which we want to pass to other methods
        group = response.meta['group']
        active = response.meta['active']
        topics = response.meta['topics']

        # Gets the names of all projects for this group
        project_names = response.css('.module-title::text').extract()

        # Get the project links for all projects for this group
        proj_links_end_dirty = response.xpath('//a/@href').extract()
        selector = 'projects/.+'

        proj_links_end = []
        for item in proj_links_end_dirty:
            if re.search(selector, item) is not None:
                print('Project link ending is ' + item)
                proj_links_end.append(item)

        assert len(proj_links_end) == len(project_names)

        print(type(proj_links_end))
        projects = zip(project_names, proj_links_end)

        # TODO turn all of these ^ into either CSS or xpath

        # Make the data for each of the projects
        for project in projects:
            print('The proj_link end is ' + project[1])
            proj_link = 'https://www.media.mit.edu' + project[1]

            print('The proj_link is ' + proj_link)
            print('Calling parse_projects_second')
            yield scrapy.Request(proj_link, callback=self.parse_projects_second, meta={'group': response.meta['group'],
                                                                                     'active': active,
                                                                                     'topics': topics,
                                                                                     'proj_name': project[0]})

    # Get data on each individual project and yield the results
    def parse_projects_second(self, response):

        # Get links to everyone who works for this group
        # people_links = response.xpath('//div/@data-href').extract()

        # Things we will want to put into the spreadsheet that were generated from other methods
        group = response.meta['group']
        group_active = response.meta['active']
        group_topics = response.meta['topics']
        proj_name = response.meta['proj_name']


        # Find out of the project was archived - if the words "was
        proj_archived = str(response.css('.variant-archived::text').extract())
        inactive = re.search('was\sactive', proj_archived)
        if bool(inactive) is True:
            proj_active = False
        else:
            proj_active = True

        pass
        # Get the research topics of this project
        proj_topics = response.css('a::text').re('^#.*')

        # Get links to every person who worked on this project
        #people_links =

        #yield scrapy.Request(people_link, callback=self.parse_people, meta={'group': response.meta['group'],
                                                                                     #'active': active,
                                                                                     #'topics': topics,
                                                                                     #'proj_name': project[0]})

        yield {
            'group': group,
            'group_active': group_active,
            'proj' : proj_name,
            'proj_active': proj_active,
            'proj_topics': proj_topics,
            'group_topics': group_topics,
            # 'people' : people

        }


    # TODO write this method
    def parse_group_people(self, response):

        # Get links to everyone who works for this group
        group = response.meta['group']
        active = response.meta['active']
        topics = response.meta['topics']
        proj_name = response.meta['proj_name']

        people_links_end_dirty = response.xpath('//a/@href').extract()
        selector = 'people/.+'

        people_links_end = []
        for item in people_links_end_dirty:
            if re.search(selector, item) is not None:
                print('Project link ending is ' + item)
                people_links_end.append(item)

        for person in people_links_end:
            person_link = 'https://www.media.mit.edu' + person
            yield scrapy.Request(person_link, callback=self.parse_projects_second, meta={'group': response.meta['group'],
                                                                                   'active': active,
                                                                                   'topics': topics,
                                                                                   'proj_name': proj_name})

    # Return group name, if the group is active, and the research topics
    def parse_group_old(self, response):
        # For each group's page, we want info on their status, people, projects, and research topics

        # Get links to everyone who works for this group
        # people_links = response.xpath('//div/@data-href').extract()
        # Get links to all projects that are part of this group
        # projects_links = response.xpath('//div/@data-href').extract()

        # Find if the words "was active" are here to see if the project is archived
        # Check if the project was archived
        archived_data = response.css('.variant-archived::text').extract()
        selector = 'was\sactive'

        if bool(re.search(selector, str(archived_data))) is True:
            active = False
        else:
            active = True

        # Return the group (string), if the group is active (boolean), and the research topics (array)
        yield {
            'group': response.meta['group'],
            # 'people' : scrapy.Request(group_page, callback=self.parse_people)
            # 'projects' : response.css(''),
            'active': active,
            'topics': response.css('a::text').re('^#.*'),
        }




