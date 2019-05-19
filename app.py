from flask import Flask, render_template, request, jsonify, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image, ExifTags, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import urllib
import requests
import json
from flask_cors import CORS, cross_origin
import os
#import filetype
import pdf2image
import time
import fileinput
import base64
import numpy as np
import cv2

from werkzeug import secure_filename
import string
import re
from pprint import pprint
import sys
import operator
import io
import random
from flask_sslify import SSLify
import cv2
from flask_mysqldb import MySQL
import matchfiles as match
import yaml

#pages = convert_from_path('bscit.pdf', 500)
#page[0].save('out.jpg', 'JPEG')

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/.keys/key.json"

def saveImage(imgstring, filename):
    #print imgstring
    imgdata = base64.b64decode(imgstring.split(",")[1])
    #print imgdata
    with open(filename, 'wb') as f:
        f.write(imgdata)



application = Flask(__name__,static_url_path='/static')

CORS(application, support_credentials=True)

@application.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

db = yaml.load(open('db.yaml'))

application.config['MySQL_HOST'] = db['mysql_host']
application.config['MySQL_USER'] = db['mysql_user']
application.config['MySQL_PASSWORD'] = db['mysql_password']
application.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(application)


@application.route('/index', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        contact = userDetails['contact']
        location = userDetails['location']
        base64img = userDetails['base64img']

        filepath = 'static/img/signups/'  # I assume you have a way of picking unique filenames
        full_filename = filepath+''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.jpg'
        saveImage(base64img, full_filename)

        cur = mysql.connection.cursor()
        x = cur.execute("SELECT photo FROM users WHERE name =%s", [name])
        if int(x)>0:
            #flash("Username taken")
            print "Username taken"
            return render_template("usernametaken.html")
        else:
            cur.execute("INSERT INTO users(name,email,contact,location,photo) VALUES(%s, %s, %s, %s, %s)",(name,email,contact,location,full_filename))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')

    return render_template('landing2.html')

@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/loginemail')
def loginemail():
	return render_template('emaillogin.html')

@application.route('/users')
def users():
        return render_template('users.html')


@application.route('/upload_FID', methods=['GET', 'POST'])
def upload_FID():
    if request.method == 'POST':
        username = request.form['name']
        base64img = request.form['base64img']
        cur = mysql.connection.cursor()

        filepath = 'static/img/logins/'  # I assume you have a way of picking unique filenames
        full_filename = filepath+''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.jpg'
        saveImage(base64img, full_filename)


        cur.execute("SELECT photo FROM users WHERE name =%s", [username])
        userDetails = cur.fetchone()
        try:
        	oldimg = userDetails[0]
        except TypeError:
        	stmt = 'No such username found'
        	return json.dumps(stmt)
        #oldimg = userDetails[0]
        mysql.connection.commit()
        cur.close()
        verified1 = match.verify(full_filename, oldimg)
        #verified = "[" + verified1.replace("}", "},", verified1.count("}")-1) + "]"
        json_data = json.loads(verified1)
        result = json.dumps({"result": json_data},sort_keys = True, indent = 4, separators = (',', ': '))
        #resp = json_data.to_dict()
       # print json_data['score']
        percent = json_data['score'] *100
        if percent>90:
             return render_template("index2.html", result = result)
        else:
             return render_template("matchfailed.html")

@application.route('/upload_EID', methods=['GEET', 'POST'])
def upload_EID():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT * FROM users WHERE email =%s AND password = %s", [email,password])
      	#print value
        if int(value)>0:
        	stmt = "Welcome to the page. Verified Successfully."
        	return json.dumps(stmt)
        else:
        	stmt = "Authentication error"
        	return json.dumps(stmt)
        mysql.connection.commit()
        cur.close()

@application.route('/viewdatabase', methods=['GET', 'POST'])
def test():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()

    return render_template('userdatabaselist.html',userDetails = userDetails)

@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('index.html')
#@application.route('/', methods=['GET', 'POST'])
#def landing():
 #   return render_template('clm_emotiondetection.html')

@application.route('/facemap', methods=['GET', 'POST'])
def facemap():
    return render_template('index.html')

if __name__ == '__main__':
  context = ('ssl/cert.pem', 'ssl/privkey.pem')
  SSLify(application)
  application.run(debug=True, port=8080, host="0.0.0.0", ssl_context=context)
