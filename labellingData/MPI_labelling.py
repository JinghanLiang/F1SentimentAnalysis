# -*- coding: UTF-8 -*-

###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is MPI for accelerating the rate of data processing. 
## The dataset can be spilited into numbers of small datasets and arraged to number of size usable processes.

from mpi4py import MPI
import json
from labellingData import labellingData
from textblob import TextBlob

comm = MPI.COMM_WORLD
rank = comm.Get_rank() #current process id
size = comm.Get_size() #current the num of processes

#process data
length = 642484
splitLength = int(length/(size))
labellingData("../Data/rawTweets.json",splitLength,rank)
