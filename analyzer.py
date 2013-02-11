# analysis.py
#
# Does analysis on queries and adds them to the view
import query
from collections import Counter

class Analyzer:

    def __init__(self):
        self.mQueries = []
        self.mKeywordHist = dict()
        
    def addQuery(self, query):
        print "[*] Starting addQuery"
        for keyword in query.mKeywordHist:
            if keyword[0] in self.mKeywordHist:
                self.mKeywordHist[keyword[0]] += keyword[1]
            else:
                self.mKeywordHist[keyword[0]] = keyword[1]

#        self.mKeywordHist = sorted([(key,value) for (key,value) in self.mKeywordHist.items()], reverse=True)
        
        self.mQueries.append(query)

    def getTopWords(self, count):
        c = Counter(self.mKeywordHist)
        return c.most_common()[0:count]

    def getTopImages(self, count):
        pass

    def getTopVideos(self, count):
        pass


    
