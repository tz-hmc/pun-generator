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
from nltk import corpus
from string import digits
#import gensim.models
#from gensim.models.keyedvectors import KeyedVectors
#from itertools import groupby
# model_org = KeyedVectors.load_word2vec_format('../GoogleNews-vectors-negative300.bin', binary=True)
# nltk.download()
arpabet = corpus.cmudict.dict()

def get_best_matches(query, corpus):
    ngs = ngrams( list(corpus), len(query) )
    ngrams_text = [''.join(x) for x in ngs]
    return difflib.get_close_matches(query, ngrams_text, n=1, cutoff=0)

# Longest common subsequence
# Dynamic programming implementation of LCS problem
def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])
    return lcs_set

def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))
    return results

def str_syllables(s):
    k = ['V' if x in list('aeiouy') else 'C' for x in s]
    k = ''.join(k)
    syl_list = []
    while k:
        end = 0
        if(k.startswith('CVCC') or k.startswith('CCCV')):
            end = 4
        elif(k.startswith('CCV') or k.startswith('CVC') or k.startswith('VCC')):
            end = 3
        elif(k.startswith('VC') or k.startswith('CV')):
            end = 2
        elif(k.startswith('V')):
            end = 1
        else:
            print "Syllables couldn't be computed: ", k, s
            return None
        syl_list.append(s[0:end])
        s = s[end:]
        k = k[end:]
    return syl_list

def phoneme_syllables(l):
    arp_vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH',
                    'IY','OW','OY','UH','UW']
    pk = ['V' if any(v in x for v in arp_vowels) else 'C' for x in l]
    pk = ''.join(pk)
    syl_list = []
    while pk:
        end = 0
        if(pk.startswith('CVCC') or pk.startswith('CCCV')):
            end = 4
        elif(pk.startswith('CCV') or pk.startswith('CVC') or pk.startswith('VCC')):
            end = 3
        elif(pk.startswith('VC') or pk.startswith('CV')):
            end = 2
        elif(pk.startswith('V')):
            end = 1
        else:
            print "Syllables couldn't be computed: ", pk, syl_list, l
            return None
        # Remove the stress digit
        syl_list.append([filter(lambda x: not x.isdigit(), s) for s in l[0:end]])
        l = l[end:]
        pk = pk[end:]
    return syl_list

def str_phonem_match(s, p_list):
    """
    Input: string
    Output:
        Break s into syllables, break p_list into syllables
        Match syllables to phoneme syllables, return as list of tuples like so:
        [('per', [P, ER0]), ('fect', [F, EH1, K, T])]

    """
    #syl_list = []
    # syl_p_list = [list(group) for k, group in groupby(p_list[0], lambda x: x[-1].isdigit()) if not k]
    syl_list = str_syllables(s)
    syl_p_list = phoneme_syllables(p_list[0])
    if len(syl_p_list) == len(syl_list):
        return zip(syl_list, syl_p_list)
    print p_list, s, syl_p_list, syl_list, len(syl_p_list), len(syl_list)
    return [(None, None)]

#for i in range(5):
a = 'treble'
b = 'trouble'
s1 = str_phonem_match(a, arpabet[a])
s2 = str_phonem_match(b, arpabet[b])
print s1,s2
possibles = []
for x in range(len(s1)):
    tup1 = s1[x]
    for y in range(len(s2)):
        tup2 = s2[y]
        s1s = set(tup1[1])
        s2s = set(tup2[1])
        i = s1s.intersection(s2s)
        if len(i) >= 2:
            print (s1[0:x], s2[y], s1[min(len(s1)-1, x+1):])
            print (s2[0:y], s1[x], s2[min(len(s2)-1, y+1):])

"""
# Use top 50 relevant words from each word
rel1 = model_org.most_similar('cat', topn=50)
rel2 = model_org.most_similar('perfect', topn=50)
print rel1
print rel2
min_score = 15
possible_puns = []

# Basic af example: s1 = purr, s2 = perfect
for s1, r1 in rel1: # n^2 (at very least) because you kinda have to
    for s2, r2 in rel2:
        score = 0
        a = arpabet[s1.lower()] if s1 in arpabet else None
        b = arpabet[s2.lower()] if s2 in arpabet else None
        # Longest sublist
        if a and b:
            sub = lcs(a, b)
            print s1, s2, a, b, sub
        else:
            print s1, s2, a, b

        if sub:
            possiblePun = s1
            possiblePun.replace()
            # These lists might not return anything
            score2 = r1 + r2 + 3*len(sub2) + len(possiblePun2)

            if len(possiblePun1) > min_score:
                possible_puns.append((possiblePun1, score1))

print possible_puns
"""
