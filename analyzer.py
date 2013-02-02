# analysis.py
#
# Does analysis on queries and adds them to the view
import query

class Analyzer:

    def __init__(self, queries):
        self.mQueries = queries
        self.mKeywordHist = self.combineKeywords(self.mQueries)

    def combineKeywords(self, queries):
        print "[*] Combining keywords for queries, query count:", len(queries)
        keywordHist = dict()
        for q in queries:
            for keyword in q.mKeywordHist:
                
                if keyword[1] in keywordHist:
                    keywordHist[keyword[1]] += keyword[0]
                else:
                    keywordHist[keyword[1]] = keyword[0]

        keywordHist = sorted([(value,key) for (key,value) in keywordHist.items()], reverse=True)
        return keywordHist

    def getTopWords(self, count):
        words = []
        for x in range(0, count):
            words.append(self.mKeywordHist[x][1])
        return words

    def getTopImages(self, count):
        pass

    def getTopVideos(self, count):
        pass

    def updateView(self, view):
        pass

    
