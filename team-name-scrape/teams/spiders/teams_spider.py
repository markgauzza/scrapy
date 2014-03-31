from scrapy.spider import Spider
from scrapy.selector import Selector

from teams.items import TeamsItem
from teams.items import LetterItem

class TeamSpider(Spider):
    name="teams"
    allowed_domains=["mlb.com", "nhl.com", "nba.com", "nfl.com"]
    start_urls = ["http://mlb.mlb.com/team/index.jsp", "http://www.nhl.com/ice/teams.htm?navid=nav-tms-main", "http://www.nba.com/teams/", "http://www.nfl.com/scores/2013/REG1"]
    items = []
    counts = []
    teamTotal = 0
    def parse(self, response):
        sel = Selector(response)
        mlbteams = sel.xpath('//*[@id="section_navigation_links"]/li[3]/ul/li')
        if (len(mlbteams) > 0):
            print 'MLB teams'
        for team in mlbteams:             
             teamName = team.xpath('a/text()').extract()[0]                          
             self.append(teamName, "MLB")

        nhlteams = sel.xpath('//*[@id="realignmentPage"]//*[@class="teamContainer"]//div[@class="teamName"]')
        if (len(nhlteams) > 0):
            print 'NHL teams'
        for team in nhlteams:
            teamName = team.xpath('span[@class="teamCommon"]/text()').extract()[0]
            print(teamName)
            self.append(teamName, "NHL")
        
        nflteams = sel.xpath('//*[@class="team-info"]/p[@class="team-name"]')
        if (len(nflteams) > 0):
            print 'NFL teams'
        for team in nflteams:
            print team
            teamName = team.xpath('a/text()').extract()[0]
            print(teamName)
            self.append(teamName, "NFL")

        nbateams = sel.xpath('//*[@id="nbateamsTable"]/table//tr/td/table//tr[1]/td/a')
        if (len(nbateams) > 0):
            print 'NBA teams'
        for team in nbateams:
            teamName=team.xpath('@href').extract()[0].strip("/")
            self.append(teamName, "NBA")



        for count in sorted(self.counts, key=lambda count:count["firstLetter"]):            
            #print item["firstLetter"]
            #print item["name"]
            #print item["sport"]
            
            
            percentage = (float(count["count"]) / self.teamTotal) * 100
            print (count["firstLetter"] +": " +  str(count["count"]) + " (" + count["names"] + ") "+ str(percentage) + "%")


    def append(self, teamName, sportName):
        firstLetter = teamName[:1].upper()
        self.teamTotal = self.teamTotal+ 1
        item = TeamsItem()
        item["firstLetter"] = firstLetter
        item["sport"] = sportName
        item["name"] = teamName
        self.items.append(item)
        first_or_default = next((x for x in self.counts if x["firstLetter"] == firstLetter), None)
        count = LetterItem()
        count["firstLetter"] = firstLetter
        count["count"] = 1.0
        count["names"] = teamName
        if(first_or_default == None):            
            self.counts.append(count)       
        else:
            newCount = float(first_or_default["count"]) + 1    
            first_or_default["count"] = newCount
            first_or_default["names"] = first_or_default["names"] + ", " + teamName            
            