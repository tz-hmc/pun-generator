#!/usr/bin/python
"""
" Author: tz-hmc
" Date: 10/13/17
" Note: Pun generator using ngrams / word2vec approach
"   scores puns based on length and relevance because
"   it has standards
"   Also it's good to reduce search space
"   Unsurprisingly it's extremely slow.
" For the lazy: install the dependencies with
"   sudo pip install --upgrade gensim
"   sudo pip install -U nltk
"""

import difflib
from nltk.util import ngrams
import gensim.models
from gensim.models.keyedvectors import KeyedVectors
model_org = KeyedVectors.load_word2vec_format('../GoogleNews-vectors-negative300.bin', binary=True)

def get_best_matches(query, corpus):
    ngs = ngrams( list(corpus), len(query) )
    ngrams_text = [''.join(x) for x in ngs]
    return difflib.get_close_matches(query, ngrams_text, n=1, cutoff=0)

# Use top 50 relevant words from each word
rel1 = model_org.most_similar('cat', topn=40)
rel2 = model_org.most_similar('perfect', topn=40)
print rel1
print rel2
min_score = 15
possible_puns = []

# Basic af example: s1 = purr, s2 = perfect
for s1, r1 in rel1: # n^2 (at very least) because you kinda have to
    for s2, r2 in rel2:
        score1 = 0
        score2 = 0
        # Closest substring (of purr query) in perfect (per)
        print s1, s2
        sub1 = get_best_matches(s1, s2)
        # Closest substring (of perfect query) in purr (purr)
        sub2 = get_best_matches(s2, s1)
        if sub1 and sub2:
            possiblePun1 = s1
            possiblePun2 = s2
            print sub1, sub2

            # These lists might not return anything
            if sub1 and sub2:
                sub1 = sub1[0]
                sub2 = sub2[0]
                possiblePun2.replace(sub1, sub2) # purrfect
                possiblePun1.replace(sub2, sub1) # per
                # Figure weights out later when im not drunk
                score1 = r1 + r2 + 3*len(sub1) + len(possiblePun1)
                score2 = r1 + r2 + 3*len(sub2) + len(possiblePun2)

            if len(possiblePun1) > min_score:
                possible_puns.append((possiblePun1, score1))
            if len(possiblePun1) > min_score:
                possible_puns.append((possiblePun1, score2))

print possible_puns
