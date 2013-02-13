# googleDriver.py
#
# An interface for using google to find information

import mechanize
import re
from bs4 import BeautifulSoup
import html5lib


# googleSearch(string search):
#
# Takes the search string, and does a google search on it. Should
# return a list of top level URL's(string) that are returned from google.
NUMBER_OF_URLS_RETURNED=10 # Return the top 10 hits from google

def googleSearch(search):
    # Convert search term into valid URL
    search = search.replace(" ", "+")
    url = "http://www.google.com/search?q=" + search

    br = mechanize.Browser()

    # Pretend to not be a robot 
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0')]

    html = br.open(url).read()
    soup = BeautifulSoup(html, "html5lib")

    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/url\?q=")}):
        links.append(re.split("\/url\?q=([^&]+)\&.*", link['href'])[1])
    
    return links[:NUMBER_OF_URLS_RETURNED]


# googleImageSearch(string search):
#
# Takes the search string, and does a google image search on it.
# Should return the URLs for the top few images.
NUMBER_OF_IMAGE_URLS_RETURNED=10

def googleImageSearch(search):
    pass 


if __name__ == "__main__":
    print googleSearch("Joseph Mama")

