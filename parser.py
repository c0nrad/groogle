# parser.py
#
# Given the html of a page, the parser takes all important information, and adds it to the ui.

import nltk # TODO: Look into licensing issues

class Parser:
    
    def __init__(self):
        self.nouns = []

    def parse(self, words):
        words = nltk.word_tokenize(words)
        words = nltk.pos_tag(words)
        for word in words:
            if(word[1] == "NN"):
                self.nouns.append(word[0])


def main():
    """Simple main method for testing purposes"""
    parser = Parser()
    parser.parse("Adam Funkenbusch is the coolest dude on planet earth")
    print parser.nouns

if __name__ == "__main__":
    main()

