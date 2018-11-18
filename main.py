import os
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
class TrieNode:
    def __init__(self):

        self.children = {}
        self.occList = {}

class Trie:
    def __init__(self):
       self.root = TrieNode()

    def addWord(self, word, webPage):
        curNode = self.root
        for c in word:
            if(c not in curNode.children.keys()):           # if the character is not in the Trie Nodes children
                curNode.children[c] = TrieNode()                     # add the character to the nodes children
            curNode = curNode.children[c]                   # go to child node at character
        # End of word
        if(webPage not in curNode.occList.keys()):          # If the web page containing word is not in the occurence list
            curNode.occList[webPage] = 1                    # Add it and set the first occurrence of word to 1
        else:
            curNode.occList[webPage] += 1                   # otherwise increment the count of the word at web page

        # TODO: Possiblty impliment ranking algorithm every time a word is added, make the occ list a list of webpage : occurence but in an array? Current rank is number of occurences

class WebCrawl:
    def __init__(self, directory):
        self.directory = directory                          # Takes directory passed in and sets to self.directory
        #self.webPageLinks = {}                              # Creates an object to store web pages and hyperlinks on pages
        self.searchableTrie = self.genTrie()                # Generates the Trie by crawling the pages

    def genTrie(self):
        self.searchableTrie = Trie()
        for filename in os.listdir(self.directory):
            fullDir = directory + filename
            print(fullDir)
            print(self.text_from_html(fullDir))


            #soup = BeautifulSoup(open(fullDir, encoding='utf8'), 'html.parser')
            #links = soup.find_all('a', href=True)
            #texts = soup.find_all(text=True)
            #visible_text = filter(self.tag_visible_text, texts)
            # print(filename)
            # print(links)
            # print(visible_text)
    # Function to filter the text
    def tag_visible_text(self, page_text):
        if(page_text.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']):    # Filters these HTML tags
            return(False)
        if isinstance(page_text, Comment):                                                          # Filters comments if any
            return False
        elif(re.match('<!--.*-->', str(page_text.encode('utf-8')))):                                # Filters HTML specific text
            return(False)
        elif(re.match('\n', str(page_text.encode('utf-8')))):                                       # Filters new line characters
            return(False)
        return(True)                                                                                # Returns True if text is true visible text

    # Function to extract the visible text from the HTML
    def text_from_html(self, html_file):
        resWords = []
        soup = BeautifulSoup(open(html_file, encoding='utf8'), 'html.parser')

        texts = soup.findAll(text=True)
        visible_text = filter(self.tag_visible_text, texts)
        for t in visible_text:
            t = u"".join(t.strip())
            if(len(t) > 1 and re.match('^[\w-]+$', t)):
                print(t)
        #resWords.append(u" ".join(t.strip() for t in visible_text))
        #return(resWords)

if (__name__ == "__main__"):

    directory = os.getcwd() + '/crawled_pages/'  # Gets the directory of where the web pages are stored
    myCrawler = WebCrawl(directory)


