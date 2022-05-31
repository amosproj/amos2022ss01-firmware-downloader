


import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/?docType=1555893-Firmware&language=en_GB-English&sortByField=Popularity']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

def main():
    print("Schneider Electric py")

main()