Search Engine ~ Michael Macari
(i) The Trie in the search engine program is a simple Trie. The data structure supports functionality in adding and searching for words
in the Trie. At the end of a given word, is an occurrence list, where we have an object containing the name of the web page containing the
word, and a count of how many times the word occurred. This value is incrimented if the same word occurs twice on a web page. All words entered
into the Trie are in lower case. The resulting structure looks something like this: 
root - a - p - p - l - e - {web-page1: 2, web-page2: 4}

(ii) The ranking mechanism I chose to use in this case is to obtain all VISIBLE text from the website that is mainly in the body tags of the html.
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

(iii) The pages I chose and placed into the directory /crawled_pages are mainly wikipedia pages, and then a few other random pages. I chose these 
pages because all of them share hyperlinks between them. I also chose them specifically because they are very dense in content, and embedded HTML, 
so my program would have to work with complicated HTML and a lot of words. List of the pages I chose in the directory are:
Dragon_SpaceX.html <- information on new model they're working on
Michaelson_MorleyExperiment_Wikipedia.html <- Experiment done by Michaelson Morley
NavigationControl_SpaceX.html <- information on navigational control by Space-X
OpticalCavity_Wikipedia.html <- Wikipedia page on optical cavities
Spacetime_Wikipedia.html <- Wikipedia page on space time
SpecialRelativity_Wikipedia.html <- Wikipedia page on Special Relativity
UnstableResonators_Nature.html <- Nature document on unstable resonators

(iv) SAMPLE OUTPUT also found in sample_output.txt

(v) Dependencies I used were os, re, beautiful-soup, and nltk. The OS (Operating System) dependency was mainly used for OS control and getting directories of files, 
navigating to directories etc. The re (Regular Expression) dependency was mainly used to filter phrases, sentences and paragraphs. I used Regex
to build a filter that takes in an entire search phrase, and splits it by white space, punctuation, and in the case its user input remove duplicate words. 
This gives us a resulting array of key words to add into the Trie, or search for in the Trie. Beautiful-Soup, I utilized in order to actually
read the HTML. I had to create a filter as a means to filter the visible text from the HTML to be added into the Trie. The NLTK library, was only used when filtering
user inputs, or phrases from the HTML, because the NLTK library has a "StopWords" module so I did not have to write my own. My filter merely filters the stop words
based on this NLTK module. The stop words are conjunctions, determiners, prepositions etc. 

(vi) Usage: The only thing the user has to do is run the program, "main.py" the html pages will start to be scraped from the "crawled_pages" folder. All of it is 
autonomous from there. After the data structure is generated the user will be prompted to enter a search. The results of the search are displayed, and the user
will be again prompted to search. If the user wishes to end the program they need only press CTRL-C keyboard interrupt and end the program.

(vii) Program Flow Detailed: 