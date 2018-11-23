Search Engine ~ Michael Macari

(i) Trie Data Structure: The Trie in the search engine program is a simple Trie. The data structure supports functionality in adding and searching for words
in the Trie. At the end of a given word, is an occurrence list, where we have an object containing the name of the web page containing the
word, and a count of how many times the word occurred. This value is incrimented if the same word occurs twice on a web page. All words entered
into the Trie are in lower case. The resulting structure looks something like this: 
root - a - p - p - l - e - {web-page1: 2, web-page2: 4}

(ii) Ranking: The ranking mechanism I chose to use in this case is to obtain all VISIBLE text from the website that is mainly in the body tags of the html.
To do this I wrote a function within my web crawler class that filters out all HTML tags with text that would otherwise not be used as 
relavent keywords. Then my program takes this array of key words (ignoring stop words etc. and changing them to lowercase) and 
begins to add them to the Trie as afformentioned above. The ranking itself takes place in the FullSearchFunction of the web crawler class. 
An empty dictionary is created {} and we run a word search on each of the key words in our phrase. The occurrence list for each of the words 
is added to our accumulative occurence list. For each of the words we do this, and we add the keys and values to our accumulative occurence list. 
Example search phrase: "Apple Banana" SearchWord(Apple) -> {WebPage1: 1, WebPage2: 2, WebPage3: 1}, SearchWord(Banana) -> {WebPage1: 2, WebPage2: 1}
The accumulative dictionary would then be: {WebPage1: 3, WebPage2: 3, WebPage3: 1}. This gets returned and sorted in decreasing order by value.
The resulting web pages are then displayed:
WebPage1
WebPage2
WebPage3

(iii) Web-Page-Selection: The pages I chose and placed into the directory /crawled_pages are mainly wikipedia pages, and then a few other random pages. I chose these 
pages because all of them share hyperlinks between them. I also chose them specifically because they are very dense in content, and embedded HTML, 
so my program would have to work with complicated HTML and a lot of words. List of the pages I chose in the directory are:
Dragon_SpaceX.html <- information on new model they're working on
Michaelson_MorleyExperiment_Wikipedia.html <- Experiment done by Michaelson Morley
NavigationControl_SpaceX.html <- information on navigational control by Space-X
OpticalCavity_Wikipedia.html <- Wikipedia page on optical cavities
Spacetime_Wikipedia.html <- Wikipedia page on space time
SpecialRelativity_Wikipedia.html <- Wikipedia page on Special Relativity
UnstableResonators_Nature.html <- Nature document on unstable resonators

(iv) SAMPLE OUTPUT: Can also be found in sample_output-(LOCKED).txt. An output text file whenever the program is used is generated for a given search session called
sample_output.txt. I added the name (LOCKED) to the sample_output.txt file to show the boundary conditions and search engine working properly.
Another sample_output.txt file may be present in the package of the program which is the very last session that occurred. This file is overwritten for each session 
when the program is run. 

Scraped page 1 of 8: Dragon_SpaceX.html
Scraped page 2 of 8: Michelson_MorleyExperiment_Wikipedia.html
Scraped page 3 of 8: NavigationControl_SpaceX.html
Scraped page 4 of 8: OpticalCavity_Wikipedia.html
Scraped page 5 of 8: QuantumLeap_Wikipedia.html
Scraped page 6 of 8: Spacetime_Wikipedia.html
Scraped page 7 of 8: SpecialRelativity_Wikipedia.html
Scraped page 8 of 8: UnstableResonators_ Nature.html

Searched for: '                                      '
Results: Search terms contain no keywords. Please try again.

Searched for: 'this the; that. I, am THE' 
Results: Search terms contain no keywords. Please try again.

Searched for: 'NUCLEAR'
SpecialRelativity_Wikipedia.html: 2 
Spacetime_Wikipedia.html: 2 
Michelson_MorleyExperiment_Wikipedia.html: 1 

Searched for: 'nuclear'
SpecialRelativity_Wikipedia.html: 2 
Spacetime_Wikipedia.html: 2 
Michelson_MorleyExperiment_Wikipedia.html: 1 

Searched for: 'nuc'
Results: No web-page results 

Searched for: 'NUc'
Results: No web-page results 

Searched for: 'nUcLeAR'
SpecialRelativity_Wikipedia.html: 2 
Spacetime_Wikipedia.html: 2 
Michelson_MorleyExperiment_Wikipedia.html: 1 

Searched for: 'spacetime nuclear'
Spacetime_Wikipedia.html: 188 
SpecialRelativity_Wikipedia.html: 71 
QuantumLeap_Wikipedia.html: 2 
Michelson_MorleyExperiment_Wikipedia.html: 1 

Searched for: 'spacetime the THE; this. nuclear'
Spacetime_Wikipedia.html: 188 
SpecialRelativity_Wikipedia.html: 71 
QuantumLeap_Wikipedia.html: 2 
Michelson_MorleyExperiment_Wikipedia.html: 1 

(v) Dependencies: I used os, re, beautiful-soup, and nltk. The OS (Operating System) dependency was mainly used for OS control and getting directories of files, 
navigating to directories etc. The re (Regular Expression) dependency was mainly used to filter phrases, sentences and paragraphs. I used Regex
to build a filter that takes in an entire search phrase, and splits it by white space, punctuation, and in the case its user input remove duplicate words. 
This gives us a resulting array of key words to add into the Trie, or search for in the Trie. Beautiful-Soup, I utilized in order to actually
read the HTML. I had to create a filter as a means to filter the visible text from the HTML to be added into the Trie. The NLTK library, was only used when filtering
user inputs, or phrases from the HTML, because the NLTK library has a "StopWords" module so I did not have to write my own. My filter merely filters the stop words
based on this NLTK module. The stop words are conjunctions, determiners, prepositions etc. 

(vi) Usage: The only thing the user has to do is run the program, "main.py" the html pages will start to be scraped from the "crawled_pages" folder. All of it is 
autonomous from there. After the data structure is generated the user will be prompted to enter a search. The results of the search are displayed, and the user
will be again prompted to search. If the user wishes to end the program they need only press CTRL-C keyboard interrupt and end the program. This is best run by 
a terminal, in the root of the project foler and typing 'python main.py'. It is common that the CTRL-C interrupt does not work in most IDE's like mine where I use
Pycharm. Running it in the terminal and ending the session with CTRL-C to end the program assures that the sessions outputs are properly saved to the sample_output.txt

(vii) Program Flow Detailed: The program begins in if (name == "__main__"). I first create a variable for the directory and the current working directory is
obtained. After this, I create an instance of my WebCrawler class and we pass the directory into the class. The WebCrawler class then takes in the directory,
and makes a call to its self.genTrie() function in order to generate the Trie from the web pages. The genTrie() function, first creates an instance of my Trie class.
The Trie class then initializes by making a call to the TrieNode class which contains a self.children, and self.occList. This is now the root TrieNode of our Trie. 
The genTrie function next creates a variable for the web page count in the directory of web pages as a simple means to show status with the counter. It then iterates
through each of the files within the directory of the web pages '/crawled_pages/'. For each web page in the directory, we then pass through our self.text_from_html
function. This function takes in the full directory of the current web page as a parameter. The text_from_html function, uses beautiful soup to open the web page. 
We then find all text within the web page. After this is done, we pass all the text in the web page through the self.tag_visible_text function filter. The tag
visible text filter, gets rid of any text from the web page that has the HTML tags style, script, head, title, meta, and [document]. It also uses regex to filter
text with <!--.*-->, and any '\n' that is standing alone in the text, and anything that is 'Comment'. After all the text is filtered, the text_from_html function 
goes through each and every substring phrase or 'chunk' of text. We strip white space from the chunk of filtered text, and then pass it into the self.phrase_punc_filt.
This function is used to break up the chunk of text, into an array split by punctuation or space using some regex, and removes stopwords. In this case of the 
self.phrase_punc_filt we do not pass it the optional user_input = True, because we do not want it to remove duplicates from the text, as duplicate key words should be 
added to the Trie. The chunk of text is then returned as key words in lower case filtered properly in an array. Ex: ['cat', 'dog', 'mouse']. This array is then extended to 
the local array variable wordArray. This is done for every chunk of text and the resulting array of key words is added to our wordArray. At the end of the text_from_html 
function we return the entire pages keyword text in the array back to the genTrie function as wordArrAfterFilter. From here the genTrie() function goes through every word
in the array and calls the Trie's addWord(word, filename) function that takes in the word, and the HTML page it is associated with as parameters. The add word function in
our Trie then creates an instance of the Trie root node as curNode. We then go through each character in the word passed in. If the character is not in the TrieNode's
children, then we add that character to the TrieNodes children, and set the curNode pointer from root to the child node at the next character. After adding the 
last character of a word, the addWord function then checks if the WebPage is already in the TrieNode's occurrence list (occList). If it is not, we add the page
as the key, and set the value to 1, as the first occurrence of the word. If the page is already in the TrieNode's occurrence list (occList) then we incriment the 
value += 1 at the page it was found, meaning this word was added before for this page. The genTrie() function does this for every word array returned from every web page
generating our complete Trie with the corresponding occcurrence list at the end of a word. After the genTrie() function is finished in __main__ we then start a try
catch block. The reason for this is so we can utilize the keyboard interrupt CTRL-C as a means to break out of the search function. We then enter a loop that starts
by prompting the user for an input. The userInput is then sent through the WebCrawler.phrase_punc_filt, similar to a chunk of the web page text, only this time, the
user input is passed in with optional field (user_input = True). The reason for this is so that the phrase_punc_filt takes in the phrase and not only returns the array
of words split by punctuation, whitespace, and removes stop words, but also so that it removes duplicate keywords for our search. We do not want to search the Trie for the 
same word more than once, as this will give a false weighted sum of occurrences. The corresponding search terms are returned in an array of key words to search the Trie. 
If the user input after parsing is returned as an empty array of key words, we send a message to the user that the search terms entered contained no key words to search, and
prompt the user to try again. The loop repeats and the user is prompted for search terms. If the array does contain key words to search then we call the WebCrawler.fullSearch, 
passing the array of key word searches in as a parameter. The fullSearch function starts off by creating a weighted sum occurrence list {}. We then iterate through each term in the 
array of search terms. The individual searh term is then sent to the Trie.searchForWord function that takes a single search word as input. The searchForWord function in the Trie 
class starts by creating a pointer to the root as 'rootSearch'. Function then goes through each character of the search word. If the character is not found in the root nodes 
children, then we return None. Otherwise, we set the root node, to the node in the children at the character. We do this for each character in the word. If we reach the last 
character of a word, we first check if there is an occurence list. If there is no occurence list at the last character of the word, then we know that the word must have been a 
sub-string of a word in the Trie. Example: search(diag), word in Trie (diagnol), the occurence list at the last character g would be None, and so the word was not found in the Trie. 
If there is an occurence list at the last character of a word, then we return that occurrence list. The fullSearch function then takes that occurence list, and iterates through its 
keys and values as (webPage, occurrenceNumber). If the web page is not in the weighted sum occurrence list (accumOccList) then we add it to the list, and set it's value equal to 
that of the occurence lists occurrence number at the web page. If it is already in the accumulative occurrence list (accumOccLis) then we add the occurence value to the current 
value of the occurrence at the web page giving us our weighted occurrence sum. If the entire weighted accumulative occurence list returned is empty, then we display and write a 
message to the output stating that there were no web page results for the search. If we did obtain an accumulative occurence list, then we start by sorting it in descending order by
the values (occurrence number). We then send a message to the user and output the web pages in order of the weighted sum of occurrences of the words in the web pages. Each time 
the program is run, a session is created and the results of each search are written to a text file in the project directory called sample_output.txt. When the keyboard interrupt
CTRL-C is pressed, the file containing the search results from the session is saved, and the program ends. 

(viii) Testing: I also created a unittest for the program, which can be found in test_SearchEngine.py. In order to verify the functionality in a lot of the individual pieces of 
my search engine, I had to first create a couple dummy HTML pages I wrote that, can be found in test_webPages: test_page1, test_page2, test_page3, test_page4 contaning some 
simple HTML with meta, title, body, head, doc, and paragraph tags with minimal simple text. The unittest class starts by importing unittest, our main program, and os. We start
by getting the directory and setting it to the destination of the test web pages '/test_webPages/'. I then create a variable called expected_page(x)_words for each of the web pages
I wrote. These variables are array's containing all of the text I would expect to be returned from my text_from_html function in my main program. I also create an instance of the web
crawler class and pass it the directory where the test pages are, so the Trie is generated etc. The first unittest function was test_text_from_html. This function passes each web
page into my WebCrawler.text_from_html function. I then use an assertEqual on each of the web pages returned array's, and the corresponding expected_page_word arrays I created. 
All cases pass with no issues. The next text I created was test_search_all_words_in_Trie, which checks that each of the expected words extracted from the HTML test pages are properly
added to the Trie. I first take all of the words from every web page without duplicates and add them to an array (allWords). I then create an object expectedOccList = {}. I then begin
with a for loop. I use the first for loop to add each word into the expectedOccList as keys. I then set the value of that key word to another object {}, which is the current web pages
words that we are iterating through, setting the value at the word to 1 at the web page if it wasn't in the list at the word, and incrimenting the value at the web page at the key word,
if the web page is already in the value of the key word. I perform this same loop for every web pages words. The resulting data structure is an object with every key word as a key, and
the expected occurrence list of web pages and key word occurences at that word. I then create a boolean variable StartTrue = True. I then iterate through each of the words in my array
(allWords) and search the Trie for the word. The occurrence list found in the Trie at the end of each word is expected to match the expected occurrence list object I created
previously with the for loops. For each iteration searching the Trie for the word, set the value of the startTrue variable = startTrue AND the occurrenceList == exOccList, or the 
expected occurence list of words and web pages. If at any point they are not equal, the resulting startTrue variable would be False. The test function then at the very end does
an assertTrue. If all the words have been added to the Trie succesfully and properly, the startTrue variable should still be True when sent through the assertTrue unittest function. 
The last test function I placed in my unittest is the test_phrase_punc_filt, which is the function afformentioned that filters out stop words, removes and splits by white space and 
punctuation and returns the array of resulting words. Duplicates will be in the array of resulting words, if the user_input paramter is set to false because duplicates are added to 
the Trie, and duplicate words are removed if the user_input parameter is set to True because we do not want a false weighted sum returned. I start by making test_search_phrase
variables 1 2 3 and 4. I set these variables to random search strings. I also then create expected_phrase variables which are set to the expected returned array of words based on the 
input string and should contain no duplicates. I also then create text_nonSearchPhrase variables 1 2 3 and 4, that are set also to strings. This time howoever, I create 
expected_nonSearchPhrase variable arrays, with the expected output of words in the array to contain duplicate words, representing that it is not user input, but rather a 
chunk of text from HTML being filtered for stop words, punctuation etc. For each of the search_phrases that are to represent search terms from user input, I send it through
my phrase_punc_filt and set the user_input parameter = True. I then set the resulting variable equal to a boolean, checking that all the words that exist in the returned array, also
exist in the expected returned array and that they have the same length. I then do the same for all the non-user input strings, but this time I do not pass True into the user_input
parameter. At the end of all of this, I use the assertTrue function to verify that the expected array I created, matches the array of words returned from my function. 