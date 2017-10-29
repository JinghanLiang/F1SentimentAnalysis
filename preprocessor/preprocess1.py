# -*- coding: UTF-8 -*-

###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is preprocessor 1 that should be used before labelling data 
## It includes non-english tweets removals, noisy symbol removals

#===========================loading modules=========================#
#regular expression module: clear noises in text
import re
#natural language toolkits: processing texts (tokenise)
import nltk

import json
#Sentiment analysis package
from textblob import TextBlob

#=============Preprocessor 1=============#

####readFiles####
#input：filename path（string）
#output：clearedText without various noisy symbols（list）
def clearText(tweet):
    # detecting tweets language and remove non-english tweets
    sentence = TextBlob(tweet)
    if(sentence.detect_language()!='en'):
        tweet = ""

    else:
        quotation_str = r'('u'\u2018|'u'\u2019)+' # convert chinese quotation marks (‘) to english (')

        negation_str = r'n\'t'

        regex_str1 = [
        r'<[^>]+>', # HTML tags
        r'(?:@\s*[\w_]+)', # @-mentions
        r"(?:\#+\s*[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'RT\s', #RT symbols
        #r'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+' #emoji
        ]

        regex_pattern = re.compile(r'('+'|'.join(regex_str1)+')', re.VERBOSE | re.IGNORECASE)
        quotation_pattern = re.compile(quotation_str,re.VERBOSE | re.IGNORECASE|re.S)
        negation_pattern = re.compile(negation_str,re.VERBOSE | re.IGNORECASE|re.S)
        tweet = quotation_pattern.sub("'",tweet)
        tweet = negation_pattern.sub(" not",tweet)
        tweet = regex_pattern.sub("",tweet).strip()

    return tweet


