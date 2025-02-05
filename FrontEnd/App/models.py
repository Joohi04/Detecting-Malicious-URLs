from django.db import models
from django.contrib.auth.models import User
import numpy as np
import pickle
import pandas as pd 

from django.db import models

# Create your models here.
import pickle
import pandas as pd
from io import StringIO
#Importing dependencies
from urllib.parse import urlparse
from tld import get_tld
import os.path
import re


log = pickle.load(open('malicious_log.pkl', 'rb'))
dt = pickle.load(open('malicious_dt.pkl', 'rb'))
rf = pickle.load(open('Malicious_rf.pkl', 'rb'))



#First Directory Length
def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')


#Use of IP or not in domain
def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1


def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1


def predict(algo,url):
    StringData = StringIO(url) 
    urldata = pd.DataFrame(StringData)
    print(urldata)
    urldata.rename(columns = {0:'url'}, inplace = True) 
    print(urldata)
    #Length of URL
    urldata['url_length'] = urldata['url'].apply(lambda i: len(str(i)))
    #Hostname Length
    urldata['hostname_length'] = urldata['url'].apply(lambda i: len(urlparse(i).netloc))
    #Path Length
    urldata['path_length'] = urldata['url'].apply(lambda i: len(urlparse(i).path))

    urldata['fd_length'] = urldata['url'].apply(lambda i: fd_length(i))

    #Length of Top Level Domain
    urldata['tld'] = urldata['url'].apply(lambda i: get_tld(i,fail_silently=True))

    urldata['tld_length'] = urldata['tld'].apply(lambda i: tld_length(i))


    urldata['count-'] = urldata['url'].apply(lambda i: i.count('-'))
    urldata['count@'] = urldata['url'].apply(lambda i: i.count('@'))
    urldata['count?'] = urldata['url'].apply(lambda i: i.count('?'))
    urldata['count%'] = urldata['url'].apply(lambda i: i.count('%'))
    urldata['count.'] = urldata['url'].apply(lambda i: i.count('.'))
    urldata['count='] = urldata['url'].apply(lambda i: i.count('='))
    urldata['count-http'] = urldata['url'].apply(lambda i : i.count('http'))
    urldata['count-https'] = urldata['url'].apply(lambda i : i.count('https'))
    urldata['count-www'] = urldata['url'].apply(lambda i: i.count('www'))

    urldata['count-digits']= urldata['url'].apply(lambda i: digit_count(i))

    urldata['count-letters']= urldata['url'].apply(lambda i: letter_count(i))

    urldata['count_dir'] = urldata['url'].apply(lambda i: no_of_dir(i))

    urldata['use_of_ip'] = urldata['url'].apply(lambda i: having_ip_address(i))

    urldata['short_url'] = urldata['url'].apply(lambda i: shortening_service(i))
    #Predictor Variables
    print(urldata)

    x = urldata[['hostname_length','path_length', 'fd_length', 'tld_length', 'count-', 'count@', 'count?','count%', 'count.', 'count=', 'count-http','count-https', 'count-www', 'count-digits','count-letters', 'count_dir', 'use_of_ip']]
    print(x.shape)

    if algo == 'log':
        y_pred = log.predict_proba(x)
    elif algo == 'dt':
        y_pred = dt.predict_proba(x)
    elif algo == 'rf':
        y_pred = rf.predict_proba(x)
    return y_pred[0]


class UserPredictModel(models.Model):
    image = models.ImageField(upload_to = 'images/')
    label = models.CharField(max_length=20,default='data')

    def __str__(self):
        return str(self.image)
    