# -*- coding: UTF-8 -*-

##  COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis ###
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is preprocessor 2 that should be used before training classifiers
## It includes tokenization, stop word and punctuation removals, repeating letters removals.


#===========================loading modules=========================#
#regular expression module: clear noises in text
import re

import json
#To use the characters: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
import string

######################################## Function Defination ######################################
####tokenize the text list####
#Input：one raw tweet in text list
#Output：tokenized text list（all char to lower case，punctuation removed）        
def separateWord(text,output_format="string"):

    #emoticons cannot turn to lowercase so need to process seperately
    emoticons_str = r"""
    (?:
        [:=;xX] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
        
    )"""

    regex_str2 = [
        emoticons_str,
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z\-_]+[a-z])", # words with -
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]

    tokens_re = re.compile(r'('+'|'.join(regex_str2)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    tokensList = []
    tokens_lower = []

    tokens = tokens_re.findall(text)
    tokens = remove_duplicate(tokens)
    tokens_lower = [token if emoticon_re.search(token) else (token.lower()) for token in tokens] #emoticons cannot turn to lowercase so need to process seperately
    tokensList = tokens_lower
    tokensList = deStopWord (tokensList)

    # Return a cleaned string or list
    if output_format == "string":
        return " ".join(tokensList)
        
    elif output_format == "list":
        return tokensList

    

###Repeating words like hurrrryyyyyy
def remove_duplicate(tweet):
    removed_tweet = []
    for token in tweet:
        token = re.sub(r'(.)\1{3,}', r'\1{1,}', token)
        removed_tweet.append(token)
    return removed_tweet

####remove stopwords and punctuation####
#Input：tokenized list （list）
#Output：tokenized list without stopwords     
def deStopWord(tokensList):

    punctuation = list(string.punctuation)
    stopwords = punctuation
    with open("../Dic/english") as f:
        line = f.readline()
        while line:
            stopwords.append(line.strip())
            line = f.readline()
    f.close()
    
    #stop = text_read_write.readFormFile1DList('/Users/Jinghan/tweets_harvester/Dic/english')+ punctuation
    #print stop
    deStopList = []
    for word in tokensList:
        if word not in stopwords:
            deStopList.append(word)
    return deStopList
