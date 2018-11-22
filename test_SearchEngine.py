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

    def test_phrase_punc_filt(self):
        """Function for testing the phrase filter"""
        test_search_phrase1 = "this would be considered a search phrase. ;; yes. HELLO"
        expected_phrase1 = ['yes', 'hello', 'search', 'phrase', 'considered', 'would']
        test_search_phrase2 = "duplicate duplicate. duplicate. duplicate. duplicate DUPLICATE"
        expected_phrase2 = ['duplicate']
        test_search_phrase3 = "      "
        expected_phrase3 = []
        test_search_phrase4 = ''
        expected_phrase4 = []

        test_nonSearchPhrase1 = "this would be an example of an. a HTML HTML HTML page phrase input"
        expected_nsp1 = ['would', 'example', 'html', 'html', 'html', 'page', 'phrase', 'input']
        test_nonSearchPhrase2 = " "
        expected_nsp2 = []
        test_nonSearchPhrase3 = "      nuclear          warhead"
        expected_nsp3 = ['nuclear', 'warhead']
        test_nonSearchPhrase4 = "these duplicate, should duplicate, keep, duplicate."
        expected_nsp4 = ['duplicate', 'duplicate', 'duplicate', 'keep']

        # Tests that each of the arrays returned contain the same words that the resulting array returned from function
        # No duplicates
        res1 = self.__class__.testCrawler.phrase_punc_filt(test_search_phrase1, user_input=True)
        res1ctd = all(e in res1 for e in expected_phrase1) and len(res1) == len(expected_phrase1)

        res2 = self.__class__.testCrawler.phrase_punc_filt(test_search_phrase2, user_input=True)
        res2ctd = all(e in res2 for e in expected_phrase2) and len(res2) == len(expected_phrase2)

        res3 = self.__class__.testCrawler.phrase_punc_filt(test_search_phrase3, user_input=True)
        res3ctd = all(e in res3 for e in expected_phrase3) and len(res3) == len(expected_phrase3)

        res4 = self.__class__.testCrawler.phrase_punc_filt(test_search_phrase4, user_input=True)
        res4ctd = all(e in res4 for e in expected_phrase4) and len(res4) == len(expected_phrase4)

        # W duplicates for web scraper
        nsp1 = self.__class__.testCrawler.phrase_punc_filt(test_nonSearchPhrase1)
        nsp1ctd = all(e in nsp1 for e in expected_nsp1) and len(nsp1) == len(expected_nsp1)

        nsp2 = self.__class__.testCrawler.phrase_punc_filt(test_nonSearchPhrase2)
        nsp2ctd = all(e in nsp2 for e in expected_nsp2) and len(nsp2) == len(expected_nsp2)

        nsp3 = self.__class__.testCrawler.phrase_punc_filt(test_nonSearchPhrase3)
        nsp3ctd = all(e in nsp3 for e in expected_nsp3) and len(nsp3) == len(expected_nsp3)

        nsp4 = self.__class__.testCrawler.phrase_punc_filt(test_nonSearchPhrase4)
        nsp4ctd = all(e in nsp4 for e in expected_nsp4) and len(nsp4) == len(expected_nsp4)

        self.assertTrue(res1ctd)
        self.assertTrue(res2ctd)
        self.assertTrue(res3ctd)
        self.assertTrue(res4ctd)

        self.assertTrue(nsp1ctd)
        self.assertTrue(nsp2ctd)
        self.assertTrue(nsp3ctd)
        self.assertTrue(nsp4ctd)

if __name__ == '__main__':
    unittest.main()