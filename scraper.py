# scraper.py
#
# Given a url, the scraper finds more urls and information about a page. Generally used after a googleDriver search.

import mechanize
import re
from BeautifulSoup import BeautifulSoup

class Scraper:

    def __init__(self):
        pass

    # getHtml(string url)
    #
    # Given a url, it returns the full html
    def getHtml(self, url):
        try :
            response = mechanize.urlopen(url)
        except:
            print "[-] Broken url:", url
            return ""
            
        return response.read()        

    # getLinks(string html)
    #
    # Returns a list of urls found the html
    def getLinks(self, html):
        out = []
        soup = BeautifulSoup(html)
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            out.append(str(link["href"])) # XXX: Returns unicode
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
