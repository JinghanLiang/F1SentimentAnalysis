COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis

================================== tweets_harvester ===========================================
search.py
## This is for crawling historical tweets based on specified tweetsID or date. The API is provided by Twitter that requiring authentication written in "twitter_auth.py"
## The query term and track users are separately defined in track list and follow list.
## The tweets are stored into the database "tweets_new" into Couchdb

streaming.py
## This is for crawling real-time tweets by initializing a stream listener. The API is provided by Twitter that requiring authentication written in "twitter_auth.py"
## The query term and track users are separately defined in track list and follow list.
## The tweets are stored into the database "tweets_new" into Couchdb

twitter_auth.py
## This is for authentication with secret keys

twitter_data.py
## This is for creating the object of tweets with customized segments.
===================================== Preprocessor ======================================
preprocess1.py
## This is preprocessor 1 that should be used before labelling data 
## It includes non-english tweets removals, noisy symbol removals

preprocess2.py
## This is preprocessor 2 that should be used before training classifiers
## It includes tokenization, stop word and punctuation removals, repeating letters removals.

==================================== Labelling Data ===========================================
LabellingData.py
## This is the function for generating train and test dataset by adding labels for raw tweets.
## It utilized TextBlob and VaderSentiment to calculate sentiment score
MPI_Labelling.py
## This is the MPI implementation for accelerating the rate of labelling data 
## The dataset is evenly spilited into numbers of small datasets and arraged to all usable processes.
================================== Sentiment Analysis =====================================
testResultOut.py
## This is a helper function to write classifed results in file.

sentimentClassifier
## This is the function to do machine learnings.
## It firstly initialize some parameters which can be changed later.
## Machine learning started by preprocessing the labelled tweets by invoking preprocessor2
## It then loads the train and test dataset into lists
## It then extract and vectorize texts into digital symbols by invoking a set of Scikit learn packages
## It then select the best num of features via CHI2 
## It then train classifier and predict test dataset
## Finally output the results

=============================== Dic ========================================
The dictionaries need to be used in project.
================================== Data =========================================
The dataset need to be used to train classifiers.
================================ Web Application ======================================
The web application is based on Flask infrastructure where client browser sends requests to web server for 
acquiring data views, then server obtains a JSON format response from CouchDB, parses and draws an intuitive 
chart on web page with the usage of Google charts API. 
The page is finally sent back and shown on client's browser.
