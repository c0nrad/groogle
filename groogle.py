# google.py
# 
# Top level file, serves as connector for three main modules (ui, scrapper, analysis)
import scraper
import parser

if __name__ == "__main__":
    scraper = scraper.Scraper()
    data = scraper.scrapeAll("http://www.google.com", 0)
    
    parser = parser.Parser()
    parser.parse(data)
    print parser.nouns
