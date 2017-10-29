# -*- coding: UTF-8 -*-

###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is a helper function to write classifed results in file.

import json

def outputToFile(FileName,_doc,classResult):
    id = _doc['_id']
    rev = _doc['_rev']
    tweet = _doc['texts']     
    time = _doc['created_at']
    location = _doc['user_location']
    coordinates = _doc['coordinates']
    sentimentVader = _doc['sentimentVader']
    polarityVader = _doc['polarityVader']
    sentimentTB = _doc['TextBlobSen']
    polarityTB = _doc['TextBlobScore']
    if(classResult == 0):
        myClass = "NEG"
    elif(classResult == 1):
        myClass = "POS"

    newTweetDic = {"id":id,"rev":rev,"create_time":time,
    "location":location,"coordinates":coordinates,
    "vaderSen":sentimentVader,"vaderScore":polarityVader,
    "TextBlobSen":sentimentTB,"TextBlobScore":polarityTB,
    "myClass":myClass,"texts":tweet}

    with open(FileName, 'a') as f_write:
        f_write.write(json.dumps(newTweetDic))
        f_write.write(',\n')