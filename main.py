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
from bs4.element import Comment
# Imports NLTK to filter stop words, conjunctions, prepositions, articles determiners etc.
from nltk.corpus import stopwords
output_file = open('sample_output.txt', 'w')
# Creates a Trie Node Class
class TrieNode:
    def __init__(self):
        self.children = {}
        self.occList = {}
# Creates the class for our Trie
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Function for adding a word into the Trie takes in the web page string and word as parameters
    def addWord(self, word, webPage):
        curNode = self.root
        for c in word:
            if(c not in curNode.children.keys()):
                curNode.children[c] = TrieNode()
            curNode = curNode.children[c]
        # End of word
        if(webPage not in curNode.occList.keys()):
            curNode.occList[webPage] = 1
        else:
            curNode.occList[webPage] += 1

    # Function for searching the Trie for a key word
    def searchForWord(self, word):
        rootSearch = self.root
        # for each character in the word
        for c in word:
            if c not in rootSearch.children:
                return None
            rootSearch = rootSearch.children[c]
        if(not rootSearch.occList):
            return None
        return(rootSearch.occList)

# Creates a class for our web crawler
class WebCrawl:
    def __init__(self, directory):
        self.directory = directory
        self.searchTrie = self.genTrie()

    # Function to generate the Trie from our web pages
    def genTrie(self):
        newTrie = Trie()
        count = 1
        webPageCount = len([name for name in os.listdir(self.directory)])
        for filename in os.listdir(self.directory):
            fullDir = self.directory + filename
            print('Scraping page ' + str(count) + ' of ' + str(webPageCount) + ': ' + filename)
            output_file.write('Scraped page ' + str(count) + ' of ' + str(webPageCount) + ': ' + filename + '\n')
            wordArrAfterFilter = self.text_from_html(fullDir)
            for word in wordArrAfterFilter:
                # Add the word to our Trie
                newTrie.addWord(word, filename)
            count += 1
        return newTrie

    # Function to filter the text
    def tag_visible_text(self, page_text):
        # Filters these HTML tags
        if(page_text.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']):
            return(False)
        if isinstance(page_text, Comment):
            return False
        # Filters HTML specific text
        elif re.match('<!--.*-->', str(page_text.encode('utf-8'))):
            return False
        # Filters new line characters
        elif re.match('\n', str(page_text.encode('utf-8'))):
            return False
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
        for phrase in visible_text:
            phrase = u"".join(phrase.strip())
            if(phrase):
                # Filter out the stop words from our phrase
                wordFilter = self.phrase_punc_filt(phrase)
                if(wordFilter):
                    # Extend and adds words to the array to be returned
                    wordArray.extend(wordFilter)
        return(wordArray)

    # Function used to search an entire phrase and return pages by rank
    def fullSearch(self, searchTerms):
        # Initializes an accumulative total occurrence list
        accumOccList = {}
        for term in searchTerms:
            # Search for the word in the trie
            resList = self.searchTrie.searchForWord(term)
            if(resList):
                for webPage,occurrenceNumber in resList.items():
                    # If a web page in the occurrence list is not in our accumulative occurrence list
                    if(webPage not in accumOccList.keys()):
                        # Add it to our accumulative occurrence list and set its value to the occurrence of the word
                        accumOccList[webPage] = occurrenceNumber
                    else:
                        # If the page is in the list, then add the occurrence value to the total value
                        accumOccList[webPage] += occurrenceNumber
        # Return our accumulative occurrence list
        return accumOccList
    
    # Function used to filter the input phrase, or phrase being put in Trie
    def phrase_punc_filt(self, phraseToFilter, user_input = False):
        # Regex expression to split phrase by white space, and punctuation and store it in the array
        phraseToFilter = re.findall(r"[\w']+|[.,!?;]", phraseToFilter.lower())
        if(user_input == True):
            # We return an array containing all the words that aren't stop words, punctuation and remove duplicates
            return(list(set([word for word in phraseToFilter if word not in stopwords.words('english')
                and word not in ['!', '?', '.', ';', ',']])))
        # Otherwise if it isn't user input, meaning it was scraped from the page
        # Then we do the same as above returning an array of the words that aren't stop words or punctuation
        # But we leave duplicates because duplicate words scraped from the page should be added to the Trie
        return([word for word in phraseToFilter if word not in stopwords.words('english')
                and word not in ['!', '?', '.', ';', ',']])
# Program Main
if (__name__ == "__main__"):
    # Gets the directory of where our web pages are stored
    directory = os.getcwd() + '/crawled_pages/'
    print('One moment while we scrape the web and develop the database....')
    # Creates an instance of the web crawler passing in the directory of web pages
    myCrawler = WebCrawl(directory)
    # Try except to allow for CTRL-C Keyboard interrupt to end program
    try:
        while(True):
            print('\n Enter search term or press Ctrl-C to exit: ')
            # Gets the users search phrase
            userIn = input()
            # Removes stop words, and punctuation from user input, passing user_input=True removing duplicate words
            parsed_userIn = myCrawler.phrase_punc_filt(userIn, user_input=True)
            output_file.write('\n')
            output_file.write('Searched for: ' + userIn + '\n')
            if(not parsed_userIn):
                output_file.write('Results: ' + "Search terms contain no keywords. Please try again." + '\n')
                print("Search terms contain no keywords. Please try again.")
            # Otherwise there must be valid terms to search
            else:
                # Search all of the keywords in the Trie and get accumulative occurrence list
                search_result = myCrawler.fullSearch(parsed_userIn)
                if(not search_result):
                    output_file.write('Results: No web-page results \n')
                    print("No web-page results")
                else:
                    # Sorts the search results dictionary in decreasing order by value
                    search_result_sorted = sorted(((v, k) for k,v in search_result.items()), reverse=True)
                    for v,k in search_result_sorted:
                        output_file.write("%s: %d \n" % (k,v))
                        print("%s: %d" % (k, v))
    # CTRL-C Keyboard interrupt to end program
    except KeyboardInterrupt:
        # Close the output file for session
        output_file.close()
        exit()
