# parser.py
#
# Given the html of a page, the parser takes all important information, and adds it to the ui.

import nltk # TODO: Look into licensing issues
import string

class Parser:
    
    def __init__(self):
        self.nouns = []
        self.mNounHist = dict()

    def parse(self, words):
        words = words.split()
        print "\n[*] Parsing words, count:", len(words)        

        words = self.removeDirtyContains(words)
        print "[+] After removing dirty contains:", len(words)

        words = self.selectNLTKNouns(words)
        print "[+] After selecting nltk NN tag", len(words)

        for word in words:
            if not word in self.mNounHist:
                self.mNounHist[word] = 1
            else:
                self.mNounHist[word] += 1
        print "[+] After removing duplicates:", len(self.mNounHist)

    def selectNLTKNouns(self, words):
        out = []
        words = " ".join(words)
        words = nltk.word_tokenize(words)
        words = nltk.pos_tag(words)
        for word in words:
            if(word[1] == "NN"):
                out.append(word[0])
        return out

    def removeDirtyContains(self, words):
        out = []
        dirtyContains = string.punctuation

        for word in words:
            isDirty = False
            for dirty in dirtyContains:
                if (dirty in word):
                    isDirty = True
                    break
                
            if not isDirty:
                out.append(str(word))

        return out

    def removeDirtyWords(self, words):
        pass
        
def main():
    """Simple main method for testing purposes"""
    parser = Parser()
    parser.parse("Adam Funkenbusch is the c\"oolest dude on pl.anet earth")
    print parser.nouns

if __name__ == "__main__":
    main()

