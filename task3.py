
import time
import sys
import os
import csv
from flask import Flask,render_template,request,flash
import random
import pandas as pd
from pandas import Series,DataFrame
from nltk.classify import NaiveBayesClassifier


def validate():
	global features
	global selected
	global app	
	validdict = dict(zip(features, selected))	
	for k,v in validdict.items():		
		if k == 'AGE':			
			try:
				vi = int(v)	
			except ValueError:
				message = "<h2>AGE shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			if((vi < 0) | (vi > 9) ):
				print("errorof age")
				message = "<h2>AGE VALUE IS BETWEEN 0 AND 9</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'SEX':
			try:
				vi = int(v)	
			except ValueError:
				message = "<h2>SEX shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			if((vi < 1) | (vi > 2) ):				
				message = "<h2>SEX VALUE IS BETWEEN 1 AND 2</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'RACE':
			try:			
				vi = int(v)	
			except ValueError:
				message = "<h2>RACE shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			if((vi < 1) | (vi > 5) ):				
				message = "<h2>RACE VALUE IS BETWEEN 1 AND 5</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'DAY_OF_ADMISSION':
			try:
				vi = int(v)		
			except ValueError:
				message = "<h2>DAY_OF_ADMISSION shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			if((vi < 1) | (vi > 7) ):				
				message = "<h2>DAY_OF_ADMISSION VALUE IS BETWEEN 1 AND 7</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'DISCHARGE_STATUS':
			vi = v				
			abc = (vi in ['A','B'])			
			if(abc == False):				
				message = "<h2>DISCHARGE_STATUS VALUE IS A OR B</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'STAY_INDICATOR':
			vi = v			
			abc = (vi in ['L','S'])			
			if(abc == False):				
				message = "<h2>STAY_INDICATOR VALUE IS L OR S</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'SOURCE_OF_ADMISSION':
			try:
				vi = int(v)		
			except ValueError:
				message = "<h2>SOURCE_OF_ADMISSION shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			if((vi < 1) | (vi > 9) ):				
				message = "<h2>SOURCE_OF_ADMISSION VALUE IS BETWEEN 1 AND 9</h2>"
				flash(message)
				return render_template('main.html')
			
		if k == 'TYPE_OF_ADMISSION':
			try:
				vi = int(v)	
			except ValueError:
				message = "<h2>TYPE_OF_ADMISSION shld be numeric</h2>"
				flash(message)
				return render_template('main.html')			
			abc = (vi in [1,2,3,5,9])			
			if(abc == False):
				print("si error")
				message = "<h2>TYPE_OF_ADMISSION VALUE IS 1 OR 2 OR 3 OR 5 OR 9</h2>"
				flash(message)
				return render_template('main.html')
		
	return None


#@app.route('/classify',methods=['GET','POST'])	
def getimpf(featuresi):
	global classifier	
	global features
	
	train2 = pd.read_csv('C:/Users/chetan/Desktop/TASK3(updated)/TASK3/6339_Dataset.csv',encoding="iso-8859-1")
	rows = random.sample(list(train2.index), 1000)
	train = train2.ix[rows]
	test = train2.drop(rows)	
	train_id_list = []
	train_id = train['AGE']
	train_id_dict = train_id.to_dict()
	train_id_list = list(train_id_dict.keys())
	
	#forming classes based on percentile
	tc1max = 13034
	tc2max = 23809
	tc3max = 43266	
		
	test_id_list = []
	test_id = test['AGE']
	test_id_dict = test_id.to_dict()
	test_id_list = list(test_id_dict.keys())
	
	trainnew = train[featuresi]
	testnew = test[featuresi]	
	Serlabels = train['TOTAL_CHARGES']
	labelsdict = Serlabels.to_dict()
	labels = list(labelsdict.values())
	
	labeled_featuresets = []
	k = 0
	for i in train_id_list:
		features3 = trainnew.ix[i]
		featureset = features3.to_dict()
		label = labels[k]
		k = k + 1		
		if (label > 43266):
			labelc = "High"
		elif (label > 23809):
			labelc = "Medium"
		elif (label > 13034	):
			labelc = "Fair"
		else:
			labelc = "Low"		
		labeled_featureset = (featureset,labelc)
		labeled_featuresets.append(labeled_featureset)
	
	classifier = NaiveBayesClassifier.train(labeled_featuresets)
	miflist = classifier.most_informative_features(50)
	mifdict = dict(miflist)
	mifdict_keys = list(mifdict.keys())	
	mifdict_keys_unique = set(mifdict_keys)
	mifdict_keys_unique_list = list(mifdict_keys_unique)			
	features = mifdict_keys_unique_list	
	
	return None
	

# user defined functions
def readfile(filename):
	reader = csv.DictReader(open(filename))
	result = {}
	for row in reader:
	    for column, value in row.items():
	        result.setdefault(column, []).append(value)
	return result


#global app
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# Program execution starts here 
app.secret_key = '46303939'
@app.route("/")  
def hello():
	print("i m at beg of hello")
	header=readfile('6339_Dataset.csv')
	header=sorted(header.keys())
	if header:
		header_list=[]
		for key in range(len(header)):
			header_list.append(dict([('name',header[key])]))
	return render_template('main.html', bucket_list=header_list)
	
	
@app.route('/task',methods=['GET','POST'])
def task4():	
	result={}
	global features
	features=request.form.getlist("features")		
	getimpf(features)
		
	if features:
		rules_list=[]		
		for row in features:
			rules_list.append(dict([('name',row)]))			
		return render_template('copy.html', rules_list	=rules_list)
	else:
		message = "<h1>Invalid selection provided</h1>"
		flash(message)
		return render_template('main.html')
	
	
@app.route('/classify',methods=['GET','POST'])
def classify():
	global classifier
	global selected	
	selected=request.form.getlist("selected")
	
	validate()
	
	testfsl= dict(zip(features, selected))	
	totcharge = classifier.classify(testfsl)
	
	if selected:
		selected_list=[]
		for row in range(len(selected)):
			selected_list.append(dict([('name',selected[row]),('id',features[row])]))			
			
		return render_template('new.html', selected_list=selected_list)		
	
	print("totcharge below",totcharge)	
	flash("<h1>"+str(totcharge)+"</h1>")	
	return render_template('new3.html')


if __name__ == "__main__":
    app.debug = True 
    # app.run()        
    app.run(host='localhost')
