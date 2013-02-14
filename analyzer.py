# analysis.py
#
# Does analysis on queries and adds them to the view
import query
from collections import Counter

class Analyzer:

    def __init__(self):
        self.mQueries = []
        self.mKeywordHist = dict()
        self.mSorted = []
        self.isSorted = False
        self.mIndex = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.mSorted)

    def next(self):
        if not self.isSorted:
            self.sort()
            self.mIndex = 0
        
        newIndex = self.mIndex
        self.mIndex += 1

        return mSorted[newIndex]
        
    def addQuery(self, query):
        for keyword in query.mKeywordHist:
            if keyword[0] in self.mKeywordHist:
                self.mKeywordHist[keyword[0]] += keyword[1]
            else:
                self.mKeywordHist[keyword[0]] = keyword[1]

        self.mQueries.append(query)
        self.isSorted = False

    def getTopWords(self, count):
        if not self.isSorted:
            self.sort()
        return self.mSorted.most_common()[0:count]

    def sort(self):
        self.mSorted = Counter(self.mKeywordHist)
        self.isSorted = True
        return

    def getTopImages(self, count):
        pass

    def getTopVideos(self, count):
        pass
    
