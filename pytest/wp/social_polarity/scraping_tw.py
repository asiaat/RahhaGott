# -*- coding: utf-8 -*-

import re
import string
import time
import tweepy
import credentials
import csv
import nltk
from datetime import datetime
import requests
import subprocess
import numpy as np
import geohash
from textblob import TextBlob
import ConfigParser
import argparse


def geo_centroid(data):
    x, y = zip(*data)
    l = len(x)
    return sum(x) / l, sum(y) / l


ckey    = credentials.consumer_key
csecret = credentials.consumer_secret
atoken  = credentials.access_token
asecret = credentials.access_token_secret

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

        
def post_req_geo(inp_url,inp_eindx,inp_edoc,inp_str,inp_geocode):
    
    wtest = ""
    for tweet in tweepy.Cursor(api.search,q=inp_str,count=100,geocode=inp_geocode).items():
        
        if len(tweet.text) < 4:
            continue
        
        time.sleep(0.11)
        #print tweet.user.location.encode('utf8')
        #print tweet.place._api
        geo_loc = '{"lat": 0, "lon": 0}'
        if tweet.place != None:
            #print tweet.place.url
            gg = tweet.place.bounding_box.coordinates[0]
            geo_loc = '{"lat": %s, "lon": %s}' % (geo_centroid(gg)[1], geo_centroid(gg)[0])
            #print geo_loc

        eindex = inp_eindx
        edoc   = inp_edoc
        
        # 2015-10-01T01:30:00Z
        kibn_time = tweet.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        print kibn_time
        
        # text sentiment
        testimonial = TextBlob(tweet.text)
        #print(testimonial.sentiment)
        text_sentim = ()
        text_transl = ""
        
        detect_lang = testimonial.detect_language()
        #print ("Detect lang: ",detect_lang)
        if detect_lang != "en" and len(tweet.text) > 3:
            
            try:
            
                text_en = testimonial.translate(from_lang=detect_lang,to='en')
                #print(testimonial,'\n',text_en)
                text_sentim = text_en.sentiment
                #print("Text sentim: ",text_sentim)
                text_transl = str(text_en)
            except:
                print "Translation API exception"
        else:
            #print(tweet.text)
            text_sentim = TextBlob(tweet.text).sentiment
            #print("Text sentim: ",text_sentim)
            
        #print("Text sentim: ",text_sentim)
        sentiment_pol = 0.0
        sentiment_sub = 0.0
        try:
            sentiment_pol = text_sentim.polarity
            sentiment_sub = text_sentim.subjectivity
        except:
            print "Cant' detect sentiment polarity or subjectivity"
        
        print (sentiment_pol,sentiment_sub)
        
        str_polarity = "neutral"
        if sentiment_pol < -0.65:
            str_polarity = "angry"
        elif sentiment_pol >= 0.5:
            str_polarity = "happy"
         
        try:      
            el_url = inp_url
            url = "%s/%s/%s/%s" % (el_url,eindex,edoc,tweet.id)
            str_test = """{"author": "%s","screen_name":"%s",
                        "location": "%s",
                        "coords": %s,
                        "text": "%s",
                        "text_en": "%s",
                        "sentiment_pol": "%.3f",
                        "str_polarity" : "%s",
                        "sentiment_sub": "%.3f",
                        "detect_lang": "%s",
                        "timestamp": "%s" }""" \
            % (tweet.user.name,
               tweet.user.screen_name,
               tweet.user.location,
               geo_loc,
               tweet.text,
               text_transl,
               sentiment_pol,
               str_polarity,
               sentiment_sub,
               detect_lang,
               kibn_time)
            send = ['curl', '-XPOST', url, '-d',str_test ]
            
            print send
            res = subprocess.check_call(send)
            print res
            
        except:
            print "Can't sent to nosql db"
     
        
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Twitter scraping ')
    
    #parser.add_argument('--noarg',  action="store_true",    default=False)
    parser.add_argument('--ini',    action="store",         dest="ini")
    parser.add_argument('--query',  action="store",         dest="query")
    
    arguments =  parser.parse_args()
    
    config = ConfigParser.ConfigParser()
    config.readfp(open(arguments.ini))
    geo_area     = config.get('twitter', 'area', 0) 
    elastic_url  = config.get('elasticsearch', 'elastic_url', 0)
    elastic_indx = config.get('elasticsearch', 'elastic_index', 0) 
    elastic_doc  = config.get('elasticsearch', 'elastic_doc', 0)
    
    if arguments.query != None:
        
        query_fh = open(arguments.query)
        lines    = query_fh.readlines()
        query_fh.close()
        
        query = []
        for line in lines:
            #print line.replace('\n',''),line
            s = query.append(line.replace('\n',''))
            post_req_geo(elastic_url,elastic_indx,elastic_doc,s,geo_area)
            
        
        #print query
    else: 
        s = ['*']
        post_req_geo(elastic_url,elastic_indx,elastic_doc,s,geo_area)
    
    
    
    
    
