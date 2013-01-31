# parser.py
#
# Given the html of a page, the parser takes all important information, and adds it to the ui.

import nltk # TODO: Look into licensing issues

class Parser:
    
    def __init__(self):
        self.nouns = []

    # Wayyyy to slow. This needs to be fast as lightning
    def parse(self, words):
        print "[*] Parsing words len:", len(words)

        words = set(words.split()) # Remove duplicates
        print "[+] After removing duplicates:", len(words)
        
        words = self.removeDirtyContains(words)
        print "[+] After removing dirty contains:", len(words)

        words = " ".join(words)
        print "[+] Starting the word tokenizer"
        words = nltk.word_tokenize(words)
        words = nltk.pos_tag(words)
        for word in words:
            if(word[1] == "NN"):
                self.nouns.append(word[0])

    def removeDirtyContains(self, words):
        out = set()
        dirtyContains = [",", ".", "/", "\\", "\"", "(", ")", "{", "}", ">", "<", ";", "-", "="]
        for word in words:

            wasDirty = False
            for dirty in dirtyContains:
                if (dirty in word):
                    wasDirty = True
                    break
                
            if not wasDirty:
                out.add(word)

        return out
        
def main():
    """Simple main method for testing purposes"""
    parser = Parser()
    parser.parse("Adam Funkenbusch is the c\"oolest dude on pl.anet earth")
    print parser.nouns

if __name__ == "__main__":
    main()

