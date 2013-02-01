# scraper.py
#
# Given a url, the scraper finds more urls and information about a page. Generally used after a googleDriver search.

import mechanize
import re
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self, url):
        # Open a browser and pretend to not be a robot
        self.mBr = mechanize.Browser()
        self.mBr.set_handle_robots(False)
        self.mBr.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.isBad = False
        
        try:
            self.mHTML = self.mBr.open(url).read()
        except:
            self.isBad = True
            return

        self.mSoup = BeautifulSoup(self.mHTML)


    def getTitle(self):
        return self.mSoup.title.string

    def getHtml(self):
        return self.mHTML        

    # getLinks(string html)
    #
    # Returns a list of urls found the html
    def getLinks(self):
        #for link in self.mBr.links():
        #    print link.url
        out = []
        for link in self.mSoup.findAll('a', attrs={'href': re.compile("^http://")}):
            out.append(str(link["href"])) # XXX: Returns unicode
        return out

    def getImageLinks(self):
        out = []
        return out
    # scrapeAll(string url, int depth, int indent)
    # 
    # Given a url, it reqursively finds all urls and retreives all html into one giant chunck of text
    # The depth parameter is used to specify how many urls deep it should search.
    def scrapeAll(self, url, depth, indent = 0):
        print "[*]" + "\t" * indent, "Scraping", url, "with depth", depth
        if depth == 0:
            return self.getHtml(url)
        else:
            outData = ""
            links = self.getLinks(self.getHtml(url))
            for link in links:
                outData += self.scrapeAll(link, depth-1, indent + 1)
            return outData

if __name__ == "__main__":
    scraper = Scraper()
    data= scraper.scrapeAll("http://www.google.com", 2)

# getPlain(string url):
#   
# Takes the string url, and returns all the text (string []). All newly
# found urls are added to the url queue for later sorting through. 
# If the depth is already at the max, then new urls should not 
# be added to the queue
MAX_URL_DEPTH=2

def getPlain(url, depth):
    pass


# getImage(string url):
#   
# Takes the string url and returns the image (pyImage?). 

def getImage(url):
    pass
