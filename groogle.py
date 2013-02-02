# google.py
# 
# Top level file, serves as connector for three main modules (ui, scrapper, analysis)
import scraper
import parser
import query
import googleDriver
import analyzer
import sys


def buildQuery(googleSearch, depth):
    WARNING = '\033[93m'
    NORMAL = '\033[0m'

    print "[*] buildQuery:", googleSearch, "depth:", depth
    queries = []
    
    googleURLs = googleDriver.googleSearch(googleSearch)
    print "[+] googleDriver found hits:", len(googleURLs)
    for url in googleURLs:
        q = query.Query()
        q.mGoogleQuery = googleSearch
        q.mDepth = depth
        q.mURL = url
        
        print "[+] Grabbing html for:", q.mURL
        scrape = scraper.Scraper(q.mURL)
        if not scrape.isHTML(q.mURL):
            print WARNING + "[-] Skipping, not html:", q.mURL, "\n", NORMAL
            continue
        if scrape.isBad:
            print WARNING + "[-] Skipping bad url:", q.mURL, "\n", NORMAL
            continue

        print "[+] Grabbing title for:", q.mURL
        q.mTitle = scrape.getTitle()
        
        print "[+] Grabbing urls for:", q.mURL
        links = scrape.getLinks();
        q.mHTMLURLs = scrape.getHTMLLinks(links)
        q.mImageURLs = scrape.getImageLinks(links)
        q.mVideoURLs = scrape.getVideoLinks(links)

        print "[+] Parsing Keywords"
        parse = parser.Parser()
        q.mKeywordHist = parse.parse(scrape.mHTML)

        print "[+] Finished query for:", q.mURL
        print q, "\n"

        queries.append(q)

    return queries

def buildQueryProgressBar(googleSearch, depth):
    
    queries = []
    googleURLs = googleDriver.googleSearch(googleSearch)[0:10]
    
    print "Progress: [",
    sys.stdout.flush()
    for url in googleURLs:
        q = query.Query()
        q.mGoogleQuery = googleSearch
        q.mDepth = depth
        q.mURL = url
        
        scrape = scraper.Scraper(q.mURL)
        if not scrape.isHTML(q.mURL):
            continue
        if scrape.isBad:
            continue

        q.mTitle = scrape.getTitle()
        
        links = scrape.getLinks();
        q.mHTMLURLs = scrape.getHTMLLinks(links)
        q.mImageURLs = scrape.getImageLinks(links)
        q.mVideoURLs = scrape.getVideoLinks(links)

        parse = parser.Parser()
        q.mKeywordHist = parse.parse(scrape.mHTML)
        
        queries.append(q)
        print "*",
        sys.stdout.flush()

    print "]"
    return queries

if __name__ == "__main__":

    googleSearch = " +\"Adam Funkenbusch\" MTU "    
    print "[*] Doing analysis on the google search:", googleSearch
    
    # TRY USING THE PROGRESS BAR. It's dumb but maybe
    queries = buildQueryProgressBar(googleSearch, 0)
    #queries = buildQuery(googleSearch, 0)
    
    anal = analyzer.Analyzer(queries)
    topWords = anal.getTopWords(10)
    print "[*] Top words for", googleSearch,  ":", topWords
