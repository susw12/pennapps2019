from flask import Flask, request, render_template, jsonify, json, redirect
from werkzeug.utils import secure_filename
import os, sys, random, json, requests
from json import dumps
import mysql.connector #pip install mysql-connector

app = Flask(__name__)

sql_config = {}

with open('sql_config.json', "r") as file:
	sql_config = json.load(file)
	
def login(username, password, dbname):
	str = "select * from %s where uname=%s and pword=%s"
	ext = (dbname, username, password)
	records = []
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor(buffered=True)
		cursor.execute(str, ext)
		conn.commit()
		records = cursor.fetchall()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()
	return records

def unused_login(username, password, dbname):
	res = login(username, password, dbname)
	if (len(res) > 0):
		return False
	else:
		return True
	
def register(username, password, dbname, nodup=True):
	str = "insert into %s (uname, pword)\n \
	values(%s, %s)"
	ext = (dbname, username, password)
	res = unused_login(username, password, dbname)
	print(res)
	if (not res):
		return
	try:
		conn = mysql.connector.connect(**sql_config)
		cursor = conn.cursor()
		cursor.execute(str, ext)
		conn.commit()
	except mysql.connector.Error as error:
		print("db error:", error)
	finally:
		conn.close()
		cursor.close()

#DONE
#Home
@app.route('/')
def root():
	return render_template('index.html')
	
@app.route('/login_business', methods = ["POST"])
def logbusiness():
	json = request.get_json()
	register(json['uname'], json['pword'], 'business_users')

@app.route('/login_investor', methods = ["POST"])
def loginvestor():
	json = request.get_json()
	register(json['uname'], json['pword'], 'investor_users')
	


'''
table <generic>_users (
	uname varchar(50),
	pword varchar(50)
)
'''