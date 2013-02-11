import Queue
import time
from threading import Thread

import scraper
import parser
import query
import googleDriver
import analyzer
from debug import *


class Model:
    def __init__(self, view):
        self.mQueue = Queue.Queue()
        self.mView = view

#        for x in range(NUM_WORKER_THREADS):
        t = Thread(target=self.queryConsumer)
        t.daemon = True
        t.start()
    
        self.mGoogleToAnalyzerMap = dict()

    # Producer function, multithreaded
    def generateQuery(self, url, name, googleSearch, depth, numID):
        q = query.Query()
        q.mGoogleQuery = googleSearch
        q.mDepth = depth
        q.mURL = url
        q.mName = name
        
        infoMessage("Grabbing html for:", q.mURL)
        scrape = scraper.Scraper(q.mURL)
        if not scrape.isHTML(q.mURL):
            warningMessage("Skipping, not html:", q.mURL, "\n", NORMAL)
            return
        if scrape.isBad:
            warningMessage("Skipping bad url:", q.mURL)
            return
        
        q.mTitle = scrape.getTitle()
        
        links = scrape.getLinks();
        q.mHTMLURLs = scrape.getHTMLLinks(links)
        q.mImageURLs = scrape.getImageLinks(links)
        q.mVideoURLs = scrape.getVideoLinks(links)
        
        parse = parser.Parser()
        q.mKeywordHist = parse.parse(scrape.mHTML)
            
        self.mQueue.put(q)        
        #infoMessage("Finished query for:", q.mURL)


    # Called on a node double click
    def generateQueries(self, name, googleSearch, depth):
        goodMessage("buildQuery: ", googleSearch, "depth: ", depth)

        googleURLs = googleDriver.googleSearch(googleSearch)
        infoMessage("[+] googleDriver found hits: ", len(googleURLs))

        idCount = 0
        for url in googleURLs:
            t = Thread(target=self.generateQuery, args=(url, name, googleSearch, depth, idCount))
            t.start()
            idCount += 1
        
        self.mQueue.join()

        time.sleep(5)
        analyze = self.mGoogleToAnalyzerMap[googleSearch]
        self.mView.addNodes(name, analyze.getTopWords(100))
      
    # Threaded!
    def queryConsumer(self):
        print "[*] Query Consumer Started!"
        while True:
            query = self.mQueue.get()
            print "\n[+] Processing item title:\"", query.mTitle, "\"googleSearch:", query.mGoogleQuery
            if query.mGoogleQuery in self.mGoogleToAnalyzerMap:
                analyze = self.mGoogleToAnalyzerMap[query.mGoogleQuery]
            else:
                analyze = analyzer.Analyzer()
                self.mGoogleToAnalyzerMap[query.mGoogleQuery] = analyze

            analyze.addQuery(query)

            self.mQueue.task_done()            
            

if __name__ == "__main__":
    m = Model()
    m.generateQueries("Apple", 0)

    m.mQueue.join()

    time.sleep(5)
