"""@package parser

The parser is used to take plain html and return the important words.

@note This really doesn't need to be used as a class, it's only used in a
      static context form.
"""
import nltk # @TODO Look into licensing issues
import string
import pdb
from debug import *

class Parser:
    
    def __init__(self):
        """pass"""
        pass

    def parse(self, words):
        """ Main parser function for parser class, removes all the cluter, 
        and returns all the important words.

        @param words Single string of html
        @retval Histogram in the form { word(string) : count (int) }
        """
        infoMessage("Parsing words, count: ", len(words.split()))

        words = str(self.cleanHTML(words)).split()
        words = self.removeDirtyContains(words)
        words = self.removeDirtyWords(words)

        wordsHist = dict()
        for word in words:
            if not word in wordsHist:
                wordsHist[word] = 1
            else:
                wordsHist[word] += 1

        wordsHist = sorted([(key,value) for (key,value) in wordsHist.items()], reverse=True)
        infoMessage("After parsing: ", len(wordsHist))

        return wordsHist

    def cleanHTML(self, words):
        """
        A wrapper for a nltk 'clean_html' function. Cuts out all the 
        html tags and other crap.

        @param words A string of the html
        @retval Nice clean user text
        """
        return nltk.clean_html(words)

    def selectNLTKNouns(self, words):
        """
        A wrapper for the nltk tag methods. Currently one grabs "NN" which
        are nouns.

        @param words A string of text
        @retval A list([string]) of the nouns
        """
        out = []
        words = " ".join(words)
        words = nltk.word_tokenize(words)
        words = nltk.pos_tag(words)

        out = [word for word in words if word[1] == "NN"]
        return out

    def removeDirtyContains(self, words):
        """
        Check to see if any of the words contain punctuation, and if so
        it removes those words from the list.

        @param words The words to be looked over ([string])
        @retval The clean words ([string])
        """

        out = []
        dirtyContains = string.punctuation
        dirtyContains += string.digits

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
        """
        Removes words that are commonly known to be bad
        
        @param words The word list to be cleaned ([string])
        @retval The cleaned words ([string])
        """
        WORDS_FILE = "dirtyWords.txt"
        dirtyWords = [ str(word).strip() for word in open(WORDS_FILE) ]
            
        return [ word for word in words if not word.lower() in dirtyWords]
        
def main():
    """For testing purposes"""
    parser = Parser()
    parser.parse("Adam Funkenbusch is the c\"oolest dude on pl.anet earth!")

if __name__ == "__main__":
    main()

    
