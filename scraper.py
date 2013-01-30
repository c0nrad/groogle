#!/usr/bin/env python2.7
# scraper.py
#
# Given a url, the scraper finds more urls and information about a page. Generally used after a googleDriver search.

import mechanize
import re
from BeautifulSoup import BeautifulSoup

class Scraper:

    def __init__(self):
        self.urlQueue = []
        
    def getHtml(self, url):
        print "[+] Gathering html for:", url
        response = mechanize.urlopen(url)
        return response.read()        

    def getLinks(self, html):
        print "[+] Gathering all links on page"
        out = []
        soup = BeautifulSoup(html)
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            out += link
        return out

if __name__ == "__main__":
    scraper = Scraper()
    html = scraper.getHtml("http://www.google.com")
    print scraper.getLinks(html)


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
