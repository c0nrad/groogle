# query.py
#
# Structure for holding all information for each url. This structue is passed
# alone the other modules, till it arrives at the analysis module, which
# then reads through them and updates the GUI

class Query:
    def __init__(self):
        self.mTitle = ""
        self.mURL = ""
        self.mImageURLs = []
        self.mVideoURLs = []
        self.mHTMLURLs = []
        self.mKeywordHist = dict()
        self.mGoogleQuery = ""
        self.mDepth = 0

        self.mHTML = ""

    def __str__(self):
        out = repr(self.mTitle) + "\n"
        out += "URL: " + self.mURL + "\n"
        out += "mImageURLs: " + str(self.mImageURLs) + "\n"
        out += "mVideoURLs: " + str(self.mVideoURLs) + "\n"
        out += "mHTMLURLs: " + str(self.mHTMLURLs) + "\n"
        out += "mKeywordHist: " + str(self.mKeywordHist) + "\n"
        out += "mGoogleQuery: " + self.mGoogleQuery + "\n"
        out += "mDepth: " + str(self.mDepth)
        return out

if __name__ == "__main__":
    q = Query()
    q.mTitle = "I am a title!"
    q.mURL = "www.google.com"
    
    print q
