from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image, ExifTags, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import pytesseract
import urllib
import requests
import json
from flask_cors import CORS, cross_origin
import os
#import filetype
import pdf2image
import time
import fileinput
import paralleldots;
from werkzeug import secure_filename
import string
import re
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
from pprint import pprint
import sys
import operator
import io
import random

import cv2
import label_image
import label

#pages = convert_from_path('bscit.pdf', 500)
#page[0].save('out.jpg', 'JPEG')

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/.keys/key.json"


application = Flask(__name__,static_url_path='/static')
CORS(application, support_credentials=True)

@application.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response



@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('index.html')

@application.route('/camera', methods=['GET', 'POST'])
def camera():
   label.opencamera()


if __name__ == '__main__':

  application.run(debug=True, port=8001, host="0.0.0.0")
