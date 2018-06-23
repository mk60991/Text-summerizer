# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 15:49:11 2018

@author: hp
"""
#1st step or 1st run


from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in list(freq):
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get) 




#2nd step or 2nd run




#The FrequencySummarizer tokenizes the input into sentences then computes the term frequency map of the words. Then, the frequency map is filtered in order to ignore very low frequency and highly frequent words, this way it is able to discard the noisy words such as determiners, that are very frequent but don't contain much information, or words that occur only few times. And finally, the sentences are ranked according to the frequency of the words they contain and the top sentences are selected for the final summary. 
#To test the summarizer, let's create a function that extract the natural language from a html page using BeautifulSoup:
import urllib.request
from bs4 import BeautifulSoup

def get_only_text(url):
 """ 
  return the title and the text of the article
  at the specified url
 """
 page = urllib.request.urlopen(url).read().decode('utf8')
 soup = BeautifulSoup(page)
 text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
 return soup.title.text, text




#3rd step or 3rd run


#We can finally apply our summarizer on a set of articles extracted any website or pages:
url=input("enter url : ")
#only take ".XML" type URL
#http://feeds.bbci.co.uk/news/rss.xml
feed_xml = urllib.request.urlopen(url).read()
feed = BeautifulSoup(feed_xml.decode('utf8'))
to_summarize = list(map(lambda p: p.text, feed.find_all('guid')))

fs = FrequencySummarizer()
#it shows number of title's summary contents from website or pages
for article_url in to_summarize[:3]:
  title, text = get_only_text(article_url)
  print ('----------------------------------')
  print (title)
  #number of summary from ecah title's from webpages
  for s in fs.summarize(text, 3):
   print ('*',s)