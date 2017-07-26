#!/usr/bin/python
import re
import sys
from crawler import Crawler, CrawlerCache

file = open(sys.argv[1], "r")
for line in file:
    line='https://olamoney.com'
    crawler = Crawler()
    try:
        crawler.crawl(line)
    except:
        pass
    else:
        (scheme,domain)=map(str,line.split('://'))
        # displays the urls
        print crawler.content['olamoney.com'].keys()



'''

Basic Usage

from crawler import Crawler
crawler = Crawler()
crawler.crawl('http://techcrunch.com/')
# displays the urls
print crawler.content['techcrunch.com'].keys()

Advanced Usage

The following is using a cache (in sqlalchemy, crawler.db) and crawl to a depth of 3 from the home page. The no_cache parameter prevent '/' to be cached, enforcing new pull of the homepage each time the crawler is launched.

import re
from crawler import Crawler, CrawlerCache
crawler = Crawler(CrawlerCache('crawler.db'), depth=3)
crawler.crawl('http://techcrunch.com/', no_cache=re.compile('^/$').match)
# displays the urls
print crawler.content['techcrunch.com'].keys()


'''
