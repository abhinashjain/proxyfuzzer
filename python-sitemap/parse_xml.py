import sys
from bs4 import BeautifulSoup as Soup

def parseLog(file):
    file = sys.argv[1]
    handler = open(file).read()
    soup = Soup(handler,"lxml")
    for message in soup.findAll('url'):
        url = message.find('loc').contents[0]
        print url

if __name__ == "__main__":
    parseLog(sys.argv[1])
