# google.py
# 
# Top level file, serves as connector for three main modules (ui, scrapper, analysis)
import scraper
import parser
import query
import googleDriver

def buildQuery(googleSearch, depth):
    print "[*] buildQuery:", googleSearch
    
    print "[+] Running googleDriver"
    googleURLs = googleDriver.googleSearch(googleSearch)
    for url in googleURLs:
        q = query.Query()
        q.mGoogleQuery = googleSearch
        q.mDepth = depth
        q.mURL = url
        
        print "[+] Grabbing html for:", q.mURL
        scrape = scraper.Scraper(q.mURL)
        q.mHTML = scrape.getHtml()

        print "[+] Grabbing title for:", q.mURL
        q.mTitle = scrape.getTitle()
        
        print "[+] Grabbing html urls for:", q.mURL
        q.mHTMLURLs = scrape.getLinks()

        print "[+] Grabbing image urls for:", q.mURL
        q.mImageURLs = scrape.getImageLinks()

        print "[+] Parsing Keywords"
        parse = parser.Parser()
        q.mKeywordHist = parse.parse(scrape.mHTML)

        print "[+] Finished query for:", q.mURL
        print q, "\n"

if __name__ == "__main__":

    buildQuery("google", 0)
