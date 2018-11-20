"""
Michael Macari
Main program to run the search engine
"""
# Imports OS for computer file access
import os
# Imports regular expression for filtering
import re
# Imports beautiful soup
from bs4 import BeautifulSoup
# Imports comment element from beautiful soup to filter comment tags if any
from bs4.element import Comment
# Imports NLTK to filter stop words, conjunctions, prepositions, articles determiners etc.
from nltk.corpus import stopwords
# Creates a Trie Node Class
class TrieNode:
    def __init__(self):
        # Trie Nodes children are initialized for character as key and TrieNode as value
        self.children = {}
        # Creates an occurrence list object for the Trie Node where the Key is the web page string and value the count
        self.occList = {}
# Creates the class for our Trie
class Trie:
    def __init__(self):
        # Initializes the root as a new Trie Node
        self.root = TrieNode()

    # Function for adding a word into the Trie takes in the web page string and word as parameters
    def addWord(self, word, webPage):
        # Creates another pointer to the root of the Trie / root Trie Node
        curNode = self.root
        # For each character in the word being passed
        for c in word:
            # If the character is not in the Trie Nodes children
            if(c not in curNode.children.keys()):
                # Add the character to the nodes children
                curNode.children[c] = TrieNode()
            # Go to child Trie node at character
            curNode = curNode.children[c]
        # End of word
        # If the web page containing word is not in the occurrence list of the last node character of word
        if(webPage not in curNode.occList.keys()):
            # Add it and set the first occurrence of word to 1
            curNode.occList[webPage] = 1
        else:
            # Otherwise increment the count of the word at web page key
            curNode.occList[webPage] += 1

    # Function for searching the Trie for a key word
    def searchForWord(self, word):
        # Creates an pointer / instance of root for searching the phrase
        rootSearch = self.root
        # for each character in the word
        for c in word:
            if c not in rootSearch.children:
                # TODO: Not sure what to return if word / char is not in Trie. For now return False
                return None
            rootSearch = rootSearch.children[c]
        if(not rootSearch.occList):
            return None
        return(rootSearch.occList)

    # # Function used to search an entire phrase and return pages by rank
    # def fullSearch(self, searchPhrase):
    #     return




        # TODO: Possiblty impliment ranking algorithm every time a word is added, make the occ list a list of webpage:
        # TODO: occurence but in an array? Current rank is number of occurences
# Creates a class for our web crawler
class WebCrawl:

    def __init__(self, directory):
        # Gets passed the directory where the web pages are
        self.directory = directory
        self.webPageLinks = {}
        # Calls the genTrie function which will generate our Trie from the pages
        self.searchTrie = self.genTrie()

    # Function to generate the Trie from our web pages
    def genTrie(self):
        # Creates a new instance of the Trie class / new Trie
        newTrie = Trie()
        # Starts a counter
        count = 1
        # Gets number of files in directory to be scraped
        webPageCount = len([name for name in os.listdir(self.directory)])
        # Iterates through the web pages in the directory
        for filename in os.listdir(self.directory):
            # Gets the full directory path of the current web-page
            fullDir = self.directory + filename
            # Progress statement to indicate progress of scrape
            print('Scraping page ' + str(count) + ' of ' + str(webPageCount) + ': ' + filename)
            # Calls function to get all visible text filtered and return resulting array of words for page
            wordArrAfterFilter = self.text_from_html(fullDir)
            # For each of the words in the array from the page
            for word in wordArrAfterFilter:
                # Add the word to our Trie
                newTrie.addWord(word, filename)
            # Increment the counter
            count += 1
        # Returns the Trie just created from the web scrape
        return newTrie

    # Function to filter the text
    def tag_visible_text(self, page_text):
        # Filters these HTML tags
        if(page_text.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']):
            return(False)
        # Filters comments if any
        if isinstance(page_text, Comment):
            return False
        # Filters HTML specific text
        elif re.match('<!--.*-->', str(page_text.encode('utf-8'))):
            return False
        # Filters new line characters
        elif re.match('\n', str(page_text.encode('utf-8'))):
            return False
        # Returns True if text is true visible text
        return True

    # Function to extract the visible text from the HTML
    def text_from_html(self, html_file):
        wordArray = []
        # Creates our beautiful soup object and parses the html file
        soup = BeautifulSoup(open(html_file, encoding='utf8'), 'html.parser')
        # Extracts / finds all text in the soup object / web page
        texts = soup.findAll(text=True)
        # Applies our filter to the text, leaving us with only the visible text in the html file
        visible_text = filter(self.tag_visible_text, texts)
        # Iterates through each and every string phrase in the visible text
        for phrase in visible_text:
            # Remove trailing and leading white space of string phrase
            phrase = u"".join(phrase.strip())
            # Triggers event only if the string phrase is not empty or None
            if(phrase):
                # Splits the phrase string up by space for individual words and punctuation and converts phrase to lower
                phrase = re.findall(r"[\w']+|[.,!?;]", phrase.lower())
                # Filter out the stop words from our phrase
                wordFilter = [word for word in phrase if word not in stopwords.words('english')]
                # Assure that the filtered array is not empty
                if(wordFilter):
                    # Extend and adds words to the array to be returned
                    wordArray.extend(wordFilter)
        # Returns our array of words
        return(wordArray)

        # Function used to search an entire phrase and return pages by rank
    def fullSearch(self, searchTerms):
        return self.searchTrie.searchForWord('nuclear')

if (__name__ == "__main__"):
    # Gets the directory of where our web pages are stored
    directory = os.getcwd() + '/crawled_pages/'  # Gets the directory of where the web pages are stored
    print('One moment while we scrape the web and develop the database....')
    myCrawler = WebCrawl(directory)

    print('Enter search term:')
    userIn = input().lower().split(' ')
    print(userIn)
    print(myCrawler.fullSearch(userIn))
    # print(myCrawler.searchTrie.fullSearch(userIn))
    #
    # print(myCrawler.searchTrie.searchForWord(userIn))
