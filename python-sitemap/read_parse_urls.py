# python read_urls.py ../subdomains.txt
import os
import sys
from bs4 import BeautifulSoup as Soup

file = open(sys.argv[1], "r")
urlfile = open("urls.txt", "wb")
for line in file:
    (scheme,domain)=line.split('://')
    filename=domain.rstrip() + "_sitemap.xml"
    str="python3 main.py --domain " + line.rstrip() + " --output " + filename
    ret=os.system(str)

    if(ret==0):
        handler = open(filename).read()
        soup = Soup(handler,"lxml")
        for tags in soup.findAll('url'):
            url = tags.find('loc').contents[0]
            urlfile.write(url)
            urlfile.write("\n")
        #            print url
        str="rm "+filename
        os.system(str)

file.close()
urlfile.close()
