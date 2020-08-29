from urllib.request import urlopen
import requests
from collections import Counter
from urllib.parse import urljoin
import string

def freqWords(url):  #cdm homepage url
        '''This function checks the most common 25 words on CDM website'''

        print ('Start')
        
        wordsTotal = []
        links = crawl(url) # a set of links
        print (len(links)) # for testing
        i = 0 # for testing
        
        for link in links:
                text = getText(link)
                
                wordOnePage = words(text)
                wordsTotal += wordOnePage

                print (f'i is {i}', end = ',') # for testing
                i += 1 # for testing

        res = freq(wordsTotal)[:25] # return top 25 words in a list of tuples with word and count

        # formatting
        print('\n{:25} {:12}'.format('Word', 'Count'))
        for item in res:
                print('{:20} {:12} '.format(item[0], item[1]))

        
#---------------------------------------get links-----------------------------------------
visited = set() # initialize visited to an empty set

def crawl(url):
        '''a recursive web crawler that calls getLinks() on every visited web page'''
        # add url to set of visited pages
        global visited # warns the programmer
        visited.add(url)
        
        # getLinks() returns a set of hyperlink URLs in a web page url 
        links = getLinks(url)

        # recursively continue crawl from every link in links
        for link in links:
        # follow link only if not visited
                if link not in visited:
                        try:
                                crawl(link)
                        except:
                                pass
        return visited


def getLinks(url):
        '''obtains links in the web page'''
        req = requests.get(url)
        content = req.text
        collector = Collector(url)
        collector.feed(content)
        urls = collector.getLinks()  # get a set of links

        return urls

#-------------------------------------get text--------------------------------------------
def getText(url):
        '''returns text on a website'''                  
        try:
                req = requests.get(url)
                content = req.text    
                collector = Collector(url)
                collector.feed(content)
                text = collector.getText()
        
                return text
        except:
                pass
     

def words(text):  # a string
        '''return a list of words'''
        words = []
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)  #remove punctuations
        for word in text.split():
                        word = word.strip()
                        if not word.isnumeric():  # remove pure numbers
                                words.append(word.lower()) #lower letters
        return words

                

def freq(words): # a list of words
        '''return a list of requency of each word'''

        counts = Counter(words)
        return counts.most_common()



#------------------------------------------class--------------------------------------------
from html.parser import HTMLParser

class Collector(HTMLParser):
        '''collects hyperlinks and text'''

        def __init__(self, url):
                '''initializes parser'''
                HTMLParser.__init__(self)
                self.url = url
                self.exTag = None
                self.links = []
                self.text = []
                

        def handle_starttag(self, tag, attrs):
                '''collects hyperlinks, collects tags'''
                if tag == 'a':
                        for attr in attrs:
                                if attr[0] == 'href':
                                        self.links.append(attr[1])

                self.exTag = tag.lower()                
                
        def getLinks(self):
                '''returns a list of links (restricted to cdm webpages)'''
                self.reLinks = set()  # avoid repetition 
                for link in self.links:
                        # find only relative pathnames
                        if ('http' not in link) and ('mailto' not in link) and (link[-4:] == 'aspx'):
                                # add scheme and host to an absolute pathname
                                absolute = 'https://www.cdm.depaul.edu/' + link
                                self.reLinks.add(absolute)
                        
                return self.reLinks


        def handle_data(self, data):
                '''collects text'''
                if self.exTag not in ['script', 'style', 'list']:
                        self.text.append(data)


        def getText(self):
                '''returns text in a string format'''
                return ''.join(self.text)
                

#-------------------------Run the main function-------------------------
#Note: It may take 20+ miutes to run the function
if __name__ == '__main__':
	freqWords('https://www.cdm.depaul.edu/Pages/default.aspx')
