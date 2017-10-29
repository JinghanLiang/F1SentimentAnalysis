# -*- coding: UTF-8 -*-

###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is the function for generating train and test dataset by adding labels for raw tweets.
## It utilized TextBlob and VaderSentiment to calculate sentiment score

#===========================loading modules=========================#
#regular expression module: clear noises in text
import re
#natural language toolkits: processing texts (tokenise)
import nltk
#To use the characters: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
import string
import json
import sys
sys.path.append("../preprocessor")
from preprocess1 import clearText
#Sentiment analysis package
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#=============Preprocessor 1=============#

####readFiles####
#input：filename path（string）
#output：clearedText without various noisy symbols（list）
def labellingData(fileName,splitLength,rank):
    count = 0
    with open(fileName, 'r') as f:
        for line in (f.readlines()[splitLength*(rank):splitLength*(rank+1)]):
            try:
                count = count + 1
                line = line.strip()
                line = line.strip(',')
                _line = json.loads(line)
                tweet = _line['doc']['texts']
                # put raw tweets into preprocessor 1
                tweet = clearText(tweet)
                if (tweet == ""):
                    continue
                else:
                    # add sentiment label to tweets
                    senti_dicTB = generateSentimentTB(tweet) #dictionary with sentiment type and polarity score
                    senti_dicV = generateSentimentVader(tweet) #dictionary with sentiment type and polarity score
                    
                    _line['doc'].update(senti_dicTB)
                    _line['doc'].update(senti_dicV)
                    line = json.dumps(_line)

                    print ("rank =" + str(rank))
                    print(count)
                    with open("../Data/rawTweets_labelled.json", 'a') as f_write:
                        f_write.write(line)
                        f_write.write('\n')
                    
                    print("write done!")
            except:               
                line = ""
                continue


####Using TextBlob(TB) to generate the sentiment of tweets####
#Input：cleared text list （list）
#Output: cleared text dictionary, with added "polarityTB" and "sentimentTB"       
def generateSentimentTB(text):
#for text in clearedTextList:
    sentence = TextBlob(text)
    polarityTB = sentence.sentiment.polarity
    if(polarityTB > 0.0):
        sentimentTB = 'POS'
    elif(polarityTB < 0.0):
        sentimentTB = 'NEG'
    else:
        sentimentTB = 'NEU'
    senti_dicTB = {"texts":sentence.string,"TextBlobSen":sentimentTB,"TextBlobScore":polarityTB}
    return senti_dicTB

####Using vaderSentiment to generate the sentiment of tweets####
#Input：cleared text list （list）
#Output: cleared text dictionary, with added "polarityV" and "sentimentV"       
def generateSentimentVader(text):
#for text in clearedTextList:
    analyzer = SentimentIntensityAnalyzer()
    polarityV = analyzer.polarity_scores(text)['compound']
    if(polarityV >= 0.5):
        sentimentV = 'POS'
    elif(polarityV <= -0.5):
        sentimentV = 'NEG'
    else:
        sentimentV = 'NEU'
    senti_dicV = {"sentimentVader":sentimentV,"polarityVader":polarityV}
    return senti_dicV
