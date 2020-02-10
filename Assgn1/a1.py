'''a1.py
CSE 415, Winter 2020, Assignment 1
Sanjeev Janarthanan
'''

def is_multiple_of_3(n):
    "Return True if n is a multiple of 3; False otherwise."
    return n%3 == 0

def next_prime(m):
    '''Return an integer p that is prime, and such that
    p > m, and there does not exist any n, with n > m
    and n < p such that n is prime. In other words, return
    the next prime number after m.'''
    if m <= 0:
        return m  
    found = False
    prime = m+1;
    while not found:
      divisible = 0
      for i in range(1, prime + 1):
          if prime % i == 0:
              divisible = divisible + 1
          if divisible >= 3:
              break
      if divisible == 2:
          found = True
      else:
          prime = prime + 1
    return prime

import wordscraper
import math
url = "http://courses.cs.washington.edu/courses/cse415/20wi/desc.html"
def empirical_probabilities(url):
    '''Return a dictionary whose keys are words in a reference vocabulary,
    and whose values are PROBABILITIES of those words, based on the
    number of occurrences on the webpage at the given URL.'''
    wordlist = wordscraper.html_bytes_to_word_list(wordscraper.fetch())
    wordcount_dict = wordscraper.make_word_count_dict(wordlist)
    ref_wordcounts = wordscraper.init_counts_for_ref_vocab(ref_vocab = 
                                                           wordscraper.REF_VOCAB)
    wordscraper.combine_page_counts_with_ref_counts(wordcount_dict, ref_wordcounts)
    ref_probs = {}
    for word, counts in ref_wordcounts.items():
        ref_probs[word] = 1.0 - math.exp(-counts)
    return ref_probs
        
        
