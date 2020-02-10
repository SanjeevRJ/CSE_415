'''wordscraper.py
A utility for obtaining all the words on a web page.
S. Tanimoto, Jan 3, 2020.
'''

from urllib.request import urlopen

def fetch(url="https://courses.cs.washington.edu/courses/cse415/20wi/desc.html"):
  with urlopen(url) as resp:
     html_bytes = resp.read().decode('utf-8')
  #print(html_bytes)
  return html_bytes

import re
def html_bytes_to_word_list(the_bytes):
  ''' Get rid of non-alphabeticals, replacing them by spaces,
  then convert to a list of words, in their original order.
  A single word might occur multiple times in the list.'''
  text = re.sub('[^a-zA-Z]+', ' ', the_bytes)
  #print(text)
  # Now turn the document into a list of words.  
  wordlist = text.split(' ')
  #print(wordlist)
  return wordlist


def make_word_count_dict(wordlist):
  '''Build a dictionary of words and their numbers of occurrences
  in the document.'''
  wordcounts = {}
  for word in wordlist:
    if word=='': continue
    if word in wordcounts:
      oldcount = wordcounts[word]
      wordcounts[word] = oldcount+1
    else:
      wordcounts[word]=1
  return wordcounts

def to_sorted_pairs_list(wordcounts_dict):
  ''' From a word count dictionary, return a sorted list of
  (word, count) pairs.'''
  keys = list(wordcounts_dict.keys())
  keys.sort()
  pairs_list = [(key, wordcounts_dict[key]) for key in keys]
  return pairs_list

# Define a default reference vocabulary:
REF_VOCAB = '''artificial machine system robot
 compute computer computation computing calculate calculator calculation
 input inputted output outputted function convert conversion 
 process processed processing refer reference
 smart intelligence capable able capability ability talent creativity
 create created make made 
 invent invention invented
 design designed innovate innovation novel novelty
 learn learning learnable learned train trained training
 educate educated education
 economy economize efficiency efficient save savings
 time space memory storage bandwidth speed capacity
 data information knowledge skill
 technology component substrate 
 business firm corporation startup enterprise spinoff commercialize
 logic logical reason reasoned reasoning deduce deduced deduction
 infer inferred inference 
 pattern recognize recognized recognition recognizer
 class classify classification classifier classified category
 network networks neuron neurons neural layer layers hidden weight weights
 threshold forward backward propagate propagation backpropagate backpropagation
 stochastic decision value expectation expectimax minimax 
 search heuristic depth breadth uniform best first cost 
 admissible admissibility consistent consistency
'''

def init_counts_for_ref_vocab(ref_vocab=REF_VOCAB):
  ''' Create a dictionary with an entry for each word in the
  reference vocabulary, with its count initialized to 1,
  (as typically used in "Laplace smoothing").'''
  ref_wordcounts = {}
  ref_vocab = re.sub('[^a-zA-Z]+',' ',ref_vocab) # Elim. newlines.
  ref_wordlist = ref_vocab.split(' ')
  for word in ref_wordlist:
    ref_wordcounts[word]=1
  return ref_wordcounts

def combine_page_counts_with_ref_counts(page_counts, ref_counts):
  ''' Update ref_counts by adding in counts from page_counts.
  However, words not already in ref_counts are not added in.'''
  for key in page_counts.keys():
    if key not in ref_counts: continue
    else:
      ref_counts[key]+=page_counts[key]
  # Nothing to return, since the argument ref_counts is modified.

def demo():
  html_bytes=fetch()
  word_list = html_bytes_to_word_list(html_bytes)
  count_dict = make_word_count_dict(word_list)
  pairs_list = to_sorted_pairs_list(count_dict)
  # Print out the word-count pairs, in alphabetical order.
  print("Words and their counts from the fetched page:")
  for (word, count) in pairs_list:
    print(word, '\t', count)

  # Print out the word-count pairs, in alphabetical order,
  # again, but now using only the reference vocabulary words.
  ref_counts = init_counts_for_ref_vocab()
  combine_page_counts_with_ref_counts(count_dict, ref_counts)
  sorted_wordlist = list(ref_counts.keys())
  sorted_wordlist.sort()
  print("-----------------------------------------------------")
  print("Reference vocabulary words, and their biased counts in the fetched page:")
  for word in sorted_wordlist:
    print(word,'\t', ref_counts[word]) 

if __name__=="__main__":
  demo()
