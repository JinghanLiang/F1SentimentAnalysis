###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is for creating the object of tweets with customized segments.

from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, BooleanField, DictField
class Tweet(Document):
	_id = TextField()
	texts = TextField()
	TextBlobSen = TextField()
	TextBlobScore = TextField()
	myClass = TextField()
	coordinates = TextField()
	user_location = TextField()
	created_at = TextField()


class Result(Document):
	_id = TextField()
	result = DictField()

class Bunch:
	def __init__(self, d):
		for k, v in d.items():
			if isinstance(v, dict):
				v = Bunch(v)
			self.__dict__[k] = v

