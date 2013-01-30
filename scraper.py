# scraper.py
#
# Given a url, the scraper finds more urls and information about a page. Generally used after a googleDriver search.


mUrlQueue # FIFO queue for url depth searches


# getPlain(string url):
#   
# Takes the string url, and returns all the text (string []). All newly
# found urls are added to the url queue for later sorting through. 
# If the depth is already at the max, then new urls should not 
# be added to the queue
MAX_URL_DEPTH=2

def getPlain(url, depth):
    continue


# getImage(string url):
#   
# Takes the string url and returns the image (pyImage?). 

def getImage(url):
    continue
