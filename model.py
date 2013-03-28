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
        self.mCompletedQueue = Queue.Queue()
        self.mURLQueue = Queue.Queue()
        self.mView = view

        self.mThreads = []
        for x in range(10):
            t = Thread(target=self.generateQuery)
            t.daemon = True
            t.start()
            self.mThreads.append(t)
    
        self.mGoogleToAnalyzerMap = dict()

    # Producer function, multithreaded
    def generateQuery(self):
        goodMessage("model::generateQuery: Starting new thread")
        while True:
            (url, name, googleSearch) = self.mURLQueue.get()
            q = query.Query()
            q.mGoogleQuery = googleSearch
            q.mURL = url
            q.mName = name
            
            infoMessage("Grabbing html for:", q.mURL)
            scrape = scraper.Scraper(q.mURL)
            if not scrape.isHTML(q.mURL):
                warningMessage("Skipping, not html:", q.mURL, "\n", NORMAL)
                self.mURLQueue.task_done()
                continue
            if scrape.isBad:
                warningMessage("Skipping bad url:", q.mURL)
                self.mURLQueue.task_done()
                continue
            
            q.mTitle = scrape.getTitle()
            
            links = scrape.getLinks();
            q.mHTMLURLs = scrape.getHTMLLinks(links)
            q.mImageURLs = scrape.getImageLinks(links)
            q.mVideoURLs = scrape.getVideoLinks(links)
            
            parse = parser.Parser()
            q.mKeywordHist = parse.parse(scrape.mHTML)
            
            self.mCompletedQueue.put(q)        
            self.mURLQueue.task_done()


    # 1. Get list of URLS
    # 2. PUt URLS into queue
    # 3. Start threads to grab URLs and process them
    # 4. push queries into new queue
    # 5. add those queues up
    def generateQueries(self, name, googleSearch):
        goodMessage("buildQuery: ", googleSearch)

        googleURLs = googleDriver.googleSearch(googleSearch)
        numberOfHits = len(googleURLs)
        infoMessage("googleDriver found hits: ", numberOfHits)
        
        for url in googleURLs:
            self.mURLQueue.put( (url, name, googleSearch) )
            
        self.mURLQueue.join()

        # Process completed queries's
        self.processQueries()
        
        analyze = self.mGoogleToAnalyzerMap[googleSearch]
        self.mView.addNodes(name, analyze.getTopWords(100))
      
    # Threaded!
    def processQueries(self):
        goodMessage("model::processQueries: processing the queries")
        while not self.mCompletedQueue.empty():
            query = self.mCompletedQueue.get()
            print "\n[+] Processing item title:\"", query.mTitle, "\"googleSearch:", query.mGoogleQuery
            if query.mGoogleQuery in self.mGoogleToAnalyzerMap:
                analyze = self.mGoogleToAnalyzerMap[query.mGoogleQuery]
            else:
                analyze = analyzer.Analyzer()
                self.mGoogleToAnalyzerMap[query.mGoogleQuery] = analyze

            analyze.addQuery(query)

            self.mCompletedQueue.task_done()            
            
if __name__ == "__main__":
    m = Model()
    m.generateQueries("Apple", 0)

    m.mQueue.join()

    time.sleep(5)
