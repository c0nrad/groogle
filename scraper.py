# scraper.py
#
# Given a url, the scraper finds more urls and information about a page. Generally used after a googleDriver search.

import mechanize
import re
from bs4 import BeautifulSoup
import sys
from debug import *

class Scraper:

    def __init__(self, url):
        # Open a browser and pretend to not be a robot
        self.mURL = url
        self.mBr = mechanize.Browser()
        self.mBr.set_handle_robots(False)
        self.mBr.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.isBad = False
        
        if not self.isHTML(url):
            self.isBad = True
            return

        try:
            self.mHTML = self.mBr.open(url).read()
        except:
            self.isBad = True
            return

        self.mSoup = BeautifulSoup(self.mHTML)

    def getTitle(self):
        if type(self.mSoup.title) == None or self.mSoup.title == None:
            return ""
        else:
            return (self.mSoup.title.string or "")

    def getHtml(self):        
        return self.mHTML        

    def getLinks(self):
        out = []
        for link in self.mSoup.findAll('a', attrs={'href': re.compile("^http://")}):
            try:
                out.append(str(link["href"]))
            except UnicodeEncodeError:
                warningMessage("scraper::getLinks: UnicodeEncodeError")
        return out

    def checkLinkExtensions(self, links):
        for link in links:
            if (not self.isHTML(link)) and (not self.isImage(link)) and (not self.isVideo(link)) and (not self.isDoc(link)):
                warningMessage("scraper::checkLinkExtensions: Unkown link type:", link)

    def getHTMLLinks(self, links):
        out = [link for link in links if self.isHTML(link)]
        return out

    def getImageLinks(self, links):
        out = [link for link in links if self.isImage(link)]
        return out

    def getDocLinks(self):
        out = [link for link in links if self.isDoc(link)]
        return out

    def getVideoLinks(self, links):
        out = [link for link in links if self.isVideo(link)]
        return out

    def isImage(self, url):
        imageTypes = [ "png", "jpg", "jpeg", "gif" ]
        if url.split('.')[-1].lower() in imageTypes:
            return True
        else:
            return False

    # @XXX: Fix me
    def isHTML(self, url):
        if (not self.isImage(url)) and (not self.isDoc(url)) and (not self.isVideo(url)):
            return True
        else:
            return False

    def isVideo(self, url):
        videoTypes = [ "avi", "wmv", "mp4", "wav" ]
        if url.split('.')[-1].lower() in videoTypes:
            return True
        else:
            return False
    
    def isDoc(self, url):
        docTypes = [ "doc", "pdf", "docx", "ppt", "ps" ]
        if url.split('.')[-1].lower() in docTypes:
            return True
        else:
            return False

if __name__ == "__main__":
    scraper = Scraper("http://google.com")

    assert scraper.isVideo("http://www.porn.com/100babesAndAdam.avi")
    assert scraper.isImage("www.adamIsSexy.com/awwYeah.jpg")
    assert scraper.isDoc("http://www.myBankMoney.com/brokeAsShit.doc")
    assert not scraper.isVideo("http://www.google.com/search+=lolololnowd")
    assert not scraper.isDoc("http://www.broomball.mtu.edu/team/view/49904")
    assert not scraper.isVideo("http://www.broomball.mtu.edu/team/view/49904")
    assert not scraper.isImage("http://www.broomball.mtu.edu/team/view/49904")
    assert scraper.isHTML("http://www.broomball.mtu.edu/team/view/49904")
