"""
Michael Macari
Class module for testing the functionality of the search engine project
"""
import unittest
import main
import os
class TestSearchEngine(unittest.TestCase):
    # Tests if my web-crawl properly extracts text from the html files
    directory = os.getcwd() + '/test_webPages/'
    testCrawler = main.WebCrawl(directory)
    expected_page1_words = ['header', 'tag', '1', 'random', 'content', 'page2dragon', '2nd', 'header', 'please',
                            'unique', 'word', 'pile', 'knight', 'dragon', 'castle']
    expected_page2_words = ['header', 'tag', '1', 'test', 'page', '2', 'random', 'content', 'test',
                            'page', '2', 'making', 'words', 'utilize', 'nuclear', 'header', 'tag', '2', 'text',
                            'page2', 'unique', 'word', 'taco', 'would', 'dinosaur', 'meteor', 'prehistoric']
    expected_page3_words = ['one', 'simple', 'time', 'fruit', 'unique', 'fruit', 'apples',
                            'bananas', 'oranges', 'favorite']
    expected_page4_words = ['best', 'never', 'imagination', 'key', 'vikings', 'always', 'true',
                            'warriors', 'early', 'years', 'tren2ban', 'ultimate']

    """Tests that the text in the web crawler is being properly scraped and filtered by tag"""
    def test_text_from_html(self):
        """Testing web page 1 for returned filtered text"""
        # Filtered list of words extracted from test html page 1
        test_page1_text = self.__class__.testCrawler.text_from_html(self.__class__.directory + 'test_page1.html')

        # Tests if our expected returning array is the same as the array after passing through the text extraction
        # and filter
        self.assertEqual(self.__class__.expected_page1_words, test_page1_text)


        """Testing web page 2 for returned filtered text"""
        # Filtered list of words extracted from test html page 2
        test_page2_text = self.__class__.testCrawler.text_from_html(self.__class__.directory + 'test_page2.html')
        # Tests if our expected returning array is the same as the array after passing through the text extraction
        # and filter
        self.assertEqual(self.__class__.expected_page2_words, test_page2_text)



        """Testing web page 3 for returned filtered text"""
        # Filtered list of words extracted from test html page 2
        test_page3_text = self.__class__.testCrawler.text_from_html(self.__class__.directory + 'test_page3.html')
        # Tests if our expected returning array is the same as the array after passing through the text extraction
        # and filter
        self.assertEqual(self.__class__.expected_page3_words, test_page3_text)



        """Testing web page 4 for returned filtered text"""
        # Filtered list of words extracted from test html page 2
        test_page4_text = self.__class__.testCrawler.text_from_html(self.__class__.directory + 'test_page4.html')
        # Tests if our expected returning array is the same as the array after passing through the text extraction
        # and filter
        self.assertEqual(self.__class__.expected_page4_words, test_page4_text)

    """Confirms that our Trie is generated and able to add and search for words properly"""
    def test_search_all_words_in_Trie(self):
        """Creates an array of all words with no duplicates"""
        allWords = list(set(self.__class__.expected_page1_words + self.__class__.expected_page2_words +
                            self.__class__.expected_page3_words + self.__class__.expected_page4_words))

        """Next 4 for loops are to add our expected words to an occurrence list with each websites word count by 
        the key as word. This will be tested to be equal to the occurrence list returned by the Trie for each word"""
        expectedOccList = {}
        for word in self.__class__.expected_page1_words:
            if(word not in expectedOccList.keys()):
                expectedOccList[word] = {'test_page1.html': 1}
            elif('test_page1.html' not in expectedOccList[word].keys()):
                expectedOccList[word]['test_page1.html'] = 1
            else:
                expectedOccList[word]['test_page1.html'] += 1

        for word in self.__class__.expected_page2_words:
            if(word not in expectedOccList.keys()):
                expectedOccList[word] = {'test_page2.html': 1}
            elif('test_page2.html' not in expectedOccList[word].keys()):
                expectedOccList[word]['test_page2.html'] = 1
            else:
                expectedOccList[word]['test_page2.html'] += 1

        for word in self.__class__.expected_page3_words:
            if(word not in expectedOccList.keys()):
                expectedOccList[word] = {'test_page3.html': 1}
            elif('test_page3.html' not in expectedOccList[word].keys()):
                expectedOccList[word]['test_page3.html'] = 1
            else:
                expectedOccList[word]['test_page3.html'] += 1

        for word in self.__class__.expected_page4_words:
            if(word not in expectedOccList.keys()):
                expectedOccList[word] = {'test_page4.html': 1}
            elif('test_page1.html' not in expectedOccList[word].keys()):
                expectedOccList[word]['test_page4.html'] = 1
            else:
                expectedOccList[word]['test_page4.html'] += 1

        # Creates a bool that is true and will be sent through 'and' operation for if the two returned
        # occurrence lists are equal is true
        startTrue = True

        """Next for loop will test that every word is inserted
        in the Trie and that it is returning the proper occurrence list"""
        for word in allWords:
            # Returns the occurrence list from the trie for the searched word
            retOccList = self.testCrawler.searchTrie.searchForWord(word)
            # Returns the expected occurrence list for the word
            exOccList = expectedOccList[word]

            startTrue = startTrue and retOccList == exOccList

        self.assertTrue(startTrue)



if __name__ == '__main__':
    unittest.main()