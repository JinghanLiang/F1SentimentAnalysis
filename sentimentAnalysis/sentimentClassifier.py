# -*- coding: UTF-8 -*-

###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is the function to do machine learnings.
## It firstly initialize some parameters which can be changed later.
## Machine learning started by preprocessing the labelled tweets by invoking preprocessor2
## It then loads the train and test dataset into lists
## It then extract and vectorize texts into digital symbols by invoking a set of Scikit learn packages
## It then select the best num of features via CHI2 
## It then train classifier and predict test dataset
## Finally output the results



#===========================loading modules=========================#
#regular expression module: clear noises in text
import re

#natural language toolkits: processing texts (tokenise)
import nltk

#To use the characters: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
import string

# convert the string to JSON format
import json

#from mpi4py import MPI
import sys
sys.path.append("../preprocessor")
from preprocess2 import separateWord
import testResultOut

from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_selection.univariate_selection import chi2, SelectKBest
from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import naive_bayes, svm, preprocessing
from sklearn import metrics
##################### Initialization #####################
write_to_json = True

# term_vector_type = {"TFIDF", "Binary", "Int"}
# {"TFIDF", "Int", "Binary","HV"}: Bag-of-words model with {tf-idf, word counts, presence/absence,hashing vectorizer} representation
vector_type = "Int"

# training_model = {"NB", "SVM","no"}
training_model = "NB"

# feature scaling = {"standard", "signed", "unsigned", "no"}
# Note: Scaling is needed for SVM
scaling = "no"

# dimension reduction = {"SVD", "chi2", "no"}
# Note: For NB models, we cannot perform truncated SVD as it will make input negative
# chi2 is the feature selectioin based on chi2 independence test
dim_reduce = "chi2"
num_dim = 10000

##################### End of Initialization #####################



########################### Main Program ###########################


#Initialize the tweet and sentiment lists by reading from rawFile and by cleaning the tweet
train_tweets = []
temp = []
test_tweets = []
train_sentiment = [] 
# test_sentiment = []
docDic = []
if(vector_type == "Int" or vector_type == "TFIDF" or vector_type == "HV"):
    with open("../Data/train_tweets200000.json", 'r') as f:
        print ("Start reading train tweets")
        count = 0
        for line in f:
            # try:
            _line = json.loads(line)
            tweet = _line['doc']['texts']
            label = _line['doc']['Label']

            if(label == 'NEU'):
                continue
            else:
                # # remove the duplicate tweet
                # count = count+1
                # if(count > 300):
                #     if(check_duplicate(temp,tweet) == True):
                #         count = count -1
                #         continue
                #     else:
                #         del temp[0]
                # temp.append(tweet)

                #Append raw texts rather than lists as Count/TFIDF vectorizers take raw texts as inputs
                tweet = separateWord(tweet,output_format = "string")
                train_tweets.append(tweet)
                #print (tweet)
                if(label == 'NEG'):
                    train_sentiment.append(0)
                elif(label == 'POS'):
                    train_sentiment.append(1)
            # except:
            #     print("error")
    print ("End reading train tweets")


    with open("../Data/test_tweets200000.json", 'r') as f:
        print ("Start reading test tweets")
        for line in f:
            _line = json.loads(line)
            tweet = _line['doc']['texts']
            label = _line['doc']['Label']
            # Append raw texts rather than lists as Count/TFIDF vectorizers take raw texts as inputs
            # if(label == 'NEU'):
            #     continue
            # elif(label == 'NEG'):
            #     test_sentiment.append(0)
            # elif(label == 'POS'):
            #     test_sentiment.append(1)
            tweet = separateWord(tweet,output_format = "string")
            test_tweets.append(tweet)

            _line['doc']['texts'] = separateWord(tweet,output_format = "string")
            docDic.append(_line['doc'])
    print ("End reading test tweets")

# Generate vectors from words
if(vector_type == "TFIDF"):
    # Unit of gram is "word", only top 5000/10000 words are extracted
        count_vec = TfidfVectorizer(analyzer="word", max_features=10000, ngram_range=(1,1), sublinear_tf=True)

elif vector_type == "Binary" or vector_type == "Int":       
        count_vec = CountVectorizer(analyzer="word", max_features=10000, \
                                    binary = (vector_type == "Binary"), \
                                    ngram_range=(1,2))

# Return a scipy sparse term-document matrix
print ("Vectorizing input texts")
train_vec = count_vec.fit_transform(train_tweets)
test_vec = count_vec.transform(test_tweets)
# feature_name = count_vec.get_feature_names()
# print (feature_name)
# print (train_vec.toarray())

# if(vector_type == "HV"):
#     hv_vec = HashingVectorizer(ngram_range=(1,2),non_negative = True)
#     idfTrans = TfidfTransformer()

# print ("Vectorizing input texts")

# train_vec = hv_vec.transform(train_tweets)
# test_vec = hv_vec.transform(test_tweets)
# use TFIDF transformer has slight incresement on accuracy about 1%
# train_vec = idfTrans.fit_transform(train_vec)
# test_vec = idfTrans.transform(test_vec)


# Dimemsion Reduction
if dim_reduce == "SVD":
    print ("Performing dimension reduction based on SVD")
    svd = TruncatedSVD(n_components = num_dim)
    train_vec = svd.fit_transform(train_vec)
    test_vec = svd.transform(test_vec)
    print ("Explained variance ratio =", svd.explained_variance_ratio_.sum())

elif dim_reduce == "chi2":
    print ("Performing feature selection based on chi2 independence test")
    fselect = SelectKBest(chi2, k=num_dim)
    train_vec = fselect.fit_transform(train_vec, train_sentiment)
    test_vec = fselect.transform(test_vec)
    #print(train_vec.toarray())

# Transform into numpy arrays
if "numpy.ndarray" not in str(type(train_vec)):
    train_vec = train_vec.toarray() 
    test_vec = test_vec.toarray()

# Feature Scaling
if scaling != "no":

    if scaling == "standard":
        scaler = preprocessing.StandardScaler()
    else: 
        if scaling == "unsigned":
            scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        elif scaling == "signed":
            scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
    
    print ("Scaling vectors")
    train_vec = scaler.fit_transform(train_vec.astype(float))
    test_vec = scaler.transform(test_vec)

    
# Model training 
if training_model == "NB":
    nb = naive_bayes.MultinomialNB()
    cv_score = cross_val_score(nb, train_vec, train_sentiment, cv=10)
    print ("Training Naive Bayes")
    print ("CV Score = ", cv_score.mean())
    nb = nb.fit(train_vec, train_sentiment)
    pred = nb.predict(test_vec)
    #print("accuracy: ",metrics.accuracy_score(test_sentiment, pred))

elif training_model == "SVM":
    svc = svm.LinearSVC()
    #param = {'C': [1e15,1e13,1e11,1e9,1e7,1e5,1e3,1e1,1e-1,1e-3,1e-5]}
    param = {'C': [1e1]}
    print ("Training SVM")
    svc = GridSearchCV(svc, param, cv=10)
    #svc = RandomizedSearchCV(svc, param,cv=10)
    svc = svc.fit(train_vec, train_sentiment)
    print ("End training, start to predict")
    pred = svc.predict(test_vec)
    print ("Optimized parameters:", svc.best_estimator_)
    print ("Best CV score:", svc.best_score_)
    #print ("accuracy: ",metrics.accuracy_score(test_sentiment, pred))



# Output the results
if write_to_json:
    print(len(test_tweets))
    print(len(pred))
    #print(len(test_sentiment))
    for i in range(0,len(test_tweets)):
        testResultOut.outputToFile("../Data/classifiedTweets.json",docDic[i],pred[i])
    # with open("classifierPredict.json", 'a') as f_write:
    #     for i in range(0,len(test_tweets)):
    #         output = {"test_texts":test_tweets[i],,"originS":test_sentiment[i]}
    #         f_write.write(json.dumps(output))
    #         f_write.write('\n')

    print ("Finished Write")

#performance
