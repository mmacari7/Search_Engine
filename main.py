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
# Creates a text output file for the session
output_file = open('sample_output.txt', 'w')
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
            # if the character is not in the nodes children, the word isn't in the trie
            if c not in rootSearch.children:
                # Then we return None
                return None
            # Otherwise set the node to the child node at the character
            rootSearch = rootSearch.children[c]
        # If there is no occurrence list when completing the search of a word
        if(not rootSearch.occList):
            # Return None
            return None
        # Otherwise we return the occurrence list found at the end of the word
        return(rootSearch.occList)

# Creates a class for our web crawler
class WebCrawl:
    def __init__(self, directory):
        # Gets passed the directory where the web pages are
        self.directory = directory
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
            # Progress gets written to the output file
            output_file.write('Scraped page ' + str(count) + ' of ' + str(webPageCount) + ': ' + filename + '\n')
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
                # Filter out the stop words from our phrase
                wordFilter = self.phrase_punc_filt(phrase)
                # Assure that the filtered array is not empty
                if(wordFilter):
                    # Extend and adds words to the array to be returned
                    wordArray.extend(wordFilter)
        # Returns our array of words
        return(wordArray)

    # Function used to search an entire phrase and return pages by rank
    def fullSearch(self, searchTerms):
        # Initializes an accumulative total occurrence list
        accumOccList = {}
        # For each term in the array of search terms passed in
        for term in searchTerms:
            # Search for the word in the trie
            resList = self.searchTrie.searchForWord(term)
            # If there is an occurrence list and its not None
            if(resList):
                # Iterate through the occurrence list
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
        # If the phrase is from the user input
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
        # Keep running searches unless keyboard interrupt is pressed
        while(True):
            print('Enter search term or press Ctrl-C to exit: ')
            # Gets the users search phrase
            userIn = input()
            # Removes stop words, and punctuation from user input, passing user_input=True removing duplicate words
            parsed_userIn = myCrawler.phrase_punc_filt(userIn, user_input=True)
            output_file.write('\n')
            output_file.write('Searched for: ' + userIn + '\n')
            # If the user input array is returned empty, it means that there were no valid keywords to search
            if(not parsed_userIn):
                output_file.write('Results: ' + "Search terms contain no keywords. Please try again." + '\n')
                print("Search terms contain no keywords. Please try again.")
            # Otherwise there must be valid terms to search
            else:
                # Search all of the keywords in the Trie and get accumulative occurrence list
                search_result = myCrawler.fullSearch(parsed_userIn)
                # If the word isn't in the Trie, there are no search results
                if(not search_result):
                    output_file.write('Results: No web-page results \n')
                    print("No web-page results")
                else:
                    # Sorts the search results dictionary in decreasing order by value
                    search_result_sorted = sorted(((v, k) for k,v in search_result.items()), reverse=True)
                    # We then iterate through our sorted results
                    for v,k in search_result_sorted:
                        # And we output the web pages in descending order of occurrence
                        output_file.write(k + '\n')
                        print("%s: %d" % (k, v))
    # CTRL-C Keyboard interrupt to end program
    except KeyboardInterrupt:
        # Close the output file for session
        output_file.close()
        exit()
