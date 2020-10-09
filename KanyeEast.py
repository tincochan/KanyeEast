# coding: utf-8

# # Markov Chain

# **Learning Objectives:** Learn how to build Markov Chains from n-grams and generate Kanye West sequences from the Markov Chains.

# In[1]:

import types
from itertools import islice
import random


# ## n-grams

# In[2]:

def build_ngrams(itr, n=2):
    """Return the sequence of n-grams from the source iterator."""
    things = itr
    n_grams = []
    
    for i in range(0,len(list(things))-(n-1)):
        offset = 0
        current_list = []
        while offset < n:
            current_list.append(things[i+offset])
            offset += 1
        n_grams.append(current_list)
    
    for n_gram in n_grams:
        n_gram_tuple = tuple(n_gram)
        yield n_gram_tuple
        


# In[3]:

a = build_ngrams(range(10), n=2)
assert hasattr(a, '__iter__') and not isinstance(a, list)
al = list(a)
assert al == [(i,i+1) for i in range(9)]

b = build_ngrams(range(10), n=5)
assert hasattr(b, '__iter__') and not isinstance(b, list)
bl = list(b)
assert bl == [(i,i+1,i+2,i+3,i+4) for i in range(6)]

assert list(build_ngrams('one two three four five six seven'.split(' '), n=5)) ==     [('one','two','three','four','five'),
     ('two','three','four','five','six'),
     ('three','four','five','six','seven')]


# ## Markov chain

# You can read about the background of Markov Chains [here](https://en.wikipedia.org/wiki/Markov_chain). Write a function `build_chain`, that returns a Markov Chain for a sequence of n-grams. This function should return a `dict` with:
# 
# * The keys will be the source node in the Markov Chain, which is the first `n-1` elements in each n-gram, as a `tuple`.
# * The values will be a *list* of possible targets in the Markov Chain. As you find new values for a single key, you will need to append to the list.

# word1 word2
# (word1,word2) -> word3
# 
# word1 word2 word3
# (word2,word3) -> word4
# 
# word1 word2 word3 word4
# (word3,word4) -> word5
# 
# use random.choice to pick an array

# [(0,1),(1,4),(4,5),(5,3),(3,4),(4,7)]
# m = {
#     0:[1]
#     1:[4]
#     4:[5,7]
# }
# 
# [(0,1,2),(1,2,5),()]

# In[4]:

def build_chain(ngrams, chain=None):
    
    if chain == None:
        markov_chain = {}
    else:
        markov_chain = chain
        
    ngrams_list = list(ngrams)
    ngram_length = len(ngrams_list[0])
    key_length = ngram_length-2
    last_val = ngram_length-1
        
    for ngram in ngrams_list:
        key_list = []
        i = 0
        while i <= key_length:
            key_list.append(ngram[i])
            i += 1
        key = tuple(key_list)
        if key not in markov_chain:
            markov_chain[key] = []
        markov_chain[key].append(ngram[last_val])
    return markov_chain

ngrams = [(1,2,3),(3,4,5),(5,3,2),(2,3,1),(1,2,4),(4,3,3),(3,4,7)]
build_chain(ngrams, chain=None)

ngrams = [(1,2),(2,5),(5,3),(3,2),(2,2),(2,1),(1,7)]
build_chain(ngrams, chain=None)
        


# In[5]:

random.seed(0)
seq1 = [random.randint(0,10) for i in range(200)]
chain = build_chain(build_ngrams(seq1, n=3))
seq2 = [random.randint(0,10) for i in range(200)]
chain = build_chain(build_ngrams(seq2, n=3), chain=chain)
assert chain[(0,0)]==[7, 10, 0, 3, 4]
assert chain[(4,2)]==[1, 3, 8, 3, 7, 1, 10, 2, 8]
assert len(chain.keys())==111


# Write a function, `generate_sequence`, that can generate new sequences of length `m` from a trained Markov Chain (in the `dict` format described above). For the initial part of the sequence, randomly choose one of the keys in the Markov Chain `dict`.

# In[6]:

import random
d = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
list(d.keys())


# In[7]:

import random


def generate_sequence(chain, m):

    sequence = []
    keys = list(chain.keys())
    random_start_key = random.choice(keys)
    
    current_list = []
    for r in random_start_key:
        sequence.append(r)
        current_list.append(r)
    
    count = len(random_start_key)
    while count < m:
        next_key = tuple(current_list)
        if next_key in chain:
            next_word = random.choice(chain[next_key])
            sequence.append(next_word)
            current_list = current_list[1:]
            current_list.append(next_word)
            count += 1
        else:
            current_list = []
            random_key = random.choice(keys)
            for r in random_key:
                sequence.append(r)
                current_list.append(r)
            count += len(random_key)
    return sequence

ngrams = [(1,2),(2,3),(3,5),(5,7),(8,0),(0,3),(3,2),(2,5),(5,7),(8,1),(1,6),(6,5),(7,2)]
chain = build_chain(ngrams, chain=None)
print(chain)
generate_sequence(chain, 5)


# In[8]:

random.seed(0)
seq3 = [random.randint(0,10) for i in range(200)]
chain2 = build_chain(build_ngrams(seq1, n=3))
assert list(generate_sequence(chain2, 10))==[8, 0, 1, 8, 10, 6, 8, 4, 8, 9]
chain3 = build_chain(build_ngrams(seq1, n=5))
assert list(generate_sequence(chain3, 10))==[4, 1, 8, 5, 8, 3, 9, 8, 9, 4]


# ## Scrape the web to find lyrics

# For this part of the exercise, you will need to find lyrics from one of your favorite bands, and use the [requests](http://docs.python-requests.org/en/latest/) and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) packages to scrape the lyrics from a website. Some guidance:
# 
# 1. The more songs the better (many dozens).
# 2. No hand downloading or editing of the files, you must do everything from code.
# 3. Save all of the lyrics in a single text file in this directory.
# 
# I provide an example here of doing this for all of U2's lyrics. You will have to modify this code significantly for the band of your choice.

# In[20]:

import requests
from bs4 import BeautifulSoup


# First get the page that has an index of all the lyrics and create a list of the URLs of those pages:

# In[21]:

def get_lyric_urls():
    index = requests.get("http://www.u2.com/discography/lyrics/index/ltr/all/")
    soup = BeautifulSoup(index.text, 'html.parser')
    lyric_paths = [link.get('href') for link in
                   soup.find_all('div', class_='lyrics_list')[0].find_all('a')]
    lyric_urls = ['http://www.u2.com'+path for path in lyric_paths]
    return lyric_urls


# In[22]:

def get_lyric_urls1():
    index = requests.get("http://ohhla.com/YFA_kanye.html")
    soup = BeautifulSoup(index.text, 'html.parser')
    lyric_paths = []
    for a in soup.find_all('a', href=True):
        lyric_paths.append(a['href'])
    lyric_urls = ['http://www.ohhla.com/'+path for path in lyric_paths if 'anonymous' in path]
    return lyric_urls

get_lyric_urls1()


# In[23]:

lyric_urls = get_lyric_urls1()


# Here is a function that takes the URL of a single lyric page and scrapes the actual lyric as text:

# In[24]:

def get_lyric(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    html_lyrics = soup.find_all('pre')
    html_lyrics = [l.getText() for l in html_lyrics]
    return '\n'.join(html_lyrics)


# This gets all of the lyrics. Note the `time.sleep(1.0)`. When scraping websites, it is often important to throttle your requests so as to not get banned from the website.

# In[25]:

import time

def get_all_lyrics(lyric_urls):
    for url in lyric_urls:
        time.sleep(1.0)
        yield get_lyric(url)


# In[26]:

lyrics = get_all_lyrics(lyric_urls)


# In[27]:

lyrics


# Now save all the lyrics to a text file:

# In[ ]:

with open('all_u2_lyrics.txt', 'w') as f:
    for lyric in lyrics:
        f.write(lyric.replace('\r\n', '\n'))
        f.write('\n')


# In[28]:

with open('all_kanye_lyrics.txt', 'w') as f:
    for lyric in lyrics:
        f.write(lyric.replace('\r\n', '\n'))
        f.write('\n')


# Leave the following cell to grade your code for this section:

# In[ ]:

assert True


# ## Generate new lyrics with the Markov chain

# Here is the fun part!

# In[9]:

import textwrap


# Here are some simple function for tokenizing the lyrics:

# In[10]:

from quicktoken import tokenize_lines, tokenize_line


# In[11]:

PUNCTUATION = '`~!@#$%^&*()_-+={[}]|\:;"<,>.?/}\t\n'
def remove_punctuation_list(words, punctuation=PUNCTUATION):
    final_words = []
    for word in words:
        new_word = ""
        valid = False
        
        for i in range(0,len(word)):
            if word[i] == '-':
                final_words.append(new_word)
                new_word = ""
            
            if word[i] not in punctuation:
                new_word += word[i]
                valid = True
        if valid:
            final_words.append(new_word)
    return final_words

def lower_words_list(words):
    final_words = []
    for word in words:
        new_word = word.lower()
        final_words.append(new_word)
    return final_words

def remove_stop_words_list(words, stop_words=None):
    final_words = []
    for word in words:
        if stop_words == None or word not in stop_words:
            final_words.append(word)
    return final_words

def tokenize_line(line, stop_words=None, punctuation=PUNCTUATION):
    words = line.split(" ")
    words = remove_punctuation_list(words, punctuation)
    words = lower_words_list(words)
    words = remove_stop_words_list(words, stop_words)
    for word in words:
        yield word


# Read in your lyric file, tokenize the text (no stop words!) and generate new song lyrics. Some things to think about:
# 
# * This will work best if you generate new lines of text of some finite length (10-30 words).
# * Use `textwrap.wrap` to format these lines and separate them using newlines.
# * To get interesting results, you may need to run it multiple times.

# In[12]:

def generate_song(file, song_length):
    words = []
    with open(file,'r') as f:
        for line in f:
            cur_words = tokenize_line(line, None, punctuation=PUNCTUATION)
            for w in cur_words:
                words.append(w)
    ngrams = build_ngrams(words, n=3)
    chain = build_chain(ngrams)
    sequence = generate_sequence(chain, song_length)
    space = " "
    song = space.join(sequence)
    return textwrap.wrap(song, width=40)
        


# In[16]:

generate_song('all_kanye_lyrics.txt', 30)


# In[ ]: