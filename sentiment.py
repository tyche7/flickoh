'''
@FlickOh
INFO 290 Final Project

'''

import codecs
import glob
import json
import os
import re
import time
import sys
import urllib
import urllib2

class Sentiment():    
    @staticmethod
    def get_sentiment(filename):
        """ Get sentiment analysis of tweets in the specified file

        This function makes use of the API provided by sentiment140.com.

        @param filename - the file is assumed to be in the json format and
        the first line will be discarded ({ "data" : [\n')
        and each item is in a separate line. 
        """

        MAX_ITEMS = 8000               
        infile = codecs.open(filename, 'r', 'utf8', 'replace')
        infile.readline()  # discard the header
        
        out = open('sentiment_of_'+filename.split('/')[-1], 'w')
        out.write('{ "data" : [\n')
        reached_EOF = False

        while (not reached_EOF):               
            first = True
            count = 0
            POST_data = ''
            while (count < MAX_ITEMS):            
                tweet = infile.readline()
                if (not tweet):             
                    reached_EOF = True
                    break
                tweet = Sentiment.__extract_text(tweet)           
                if (tweet == ''): continue
                if (first):
                    POST_data = '{ "data" : [\n' + tweet            
                    first = False
                else :
                    POST_data = POST_data + ',\n' + tweet
                count += 1
            
            if (POST_data == ''): continue
            POST_data = POST_data + ']}'

            results = Sentiment.__connect_API(POST_data)
            print(len(results['data']))            
            for item in results['data'][:-1]:
                out.write(json.dumps(item) +',\n')               
            out.write(json.dumps(results['data'][-1]))
            
            if (reached_EOF): out.write(']}\n')
            else : out.write(',\n')
                    
        print("done")
        infile.close()
        out.close()

    @staticmethod
    def __connect_API(POST_data):
        API_URI = "http://www.sentiment140.com/api/bulkClassifyJson?appid=--your app id---"
        req = urllib2.Request(API_URI, POST_data)
        response = urllib2.urlopen(req)
        results = response.read()
        return json.loads(results)
    
    
    @classmethod
    def __extract_text(cls, fulltweet):
        """Converts a full tweet to a format suitable for sentiment API

        Take a full tweet (a line from the tweet file which ends with
        either ',\n' or ']}\n') and return a json item with only three
        fields i.e. texts,id, and query. Also in the text field, replace
        any URL with <URL>
        hashtag with <HT>
        user_mentions with <UM>
        """
        data = {}
        try:
            if (fulltweet.find(',\n') != -1):
                data = json.loads(fulltweet[:-2])
            else :
                data = json.loads(fulltweet[:-3])
        except ValueError:
            data = json.loads(fulltweet[:-2])
        #else:
            #print(repr(fulltweet))

        newtext = data['text']            
        for item in data['entities']['hashtags']:
            newtext = newtext.replace('#'+item['text'], '<HT>')
        for item in data['entities']['urls']:
            newtext = newtext.replace(item['url'], '<URL>')
        for item in data['entities']['user_mentions']:
            newtext = newtext.replace('@'+item['screen_name'], '<UM>')

        newtext = re.sub("[^a-zA-Z0-9<>\\s]", "", newtext)
        # format : { "no":1,"id":239011567, "text":"hello world!", "query":"skyfall" }
        return ("{\"no\":%s, \"id\":%s, \"text\":\"%s\", \"query\":\"%s\"}" %
                (str(data['no']), str(data['id']), newtext, cls.movies[int(data['no'])]) )

    @classmethod
    def process_sentiment(cls, directory):
        """Summarize the sentiment polarity for each movie in the list

        This method will process all the files with extension .json
        in the given directory and will count the total number of tweets
        with negative, neutral, positive sentiments for each movie.
        """
        def process(file, sentiment):
            infile = open(file, 'r')
            data = json.loads(infile.read())
            data = data['data']

            for item in data:               
                sentiment[item['no']][item['polarity']//2] += 1
                
        sentiment = {}
        for i in range(0, 69):
            sentiment[i] = [0,0,0]#[neg, neu, pos]
            
        os.chdir(directory)
        for file in os.listdir("."):
            if file.endswith(".json"): 
                process(file, sentiment)
                    
        fw = open('summary_sentiment', 'w')
        for key, value in sentiment.items():
            fw.write(str(key)+','+cls.movies[key]+','+str(value[0])+','+
                     str(value[1])+','+str(value[2])+','+str(sum(value))+'\n')
        
        fw.close()
        
                                                       
    
    movies = {  0:"Frankenweenie",
                1:"Butter",
                2:"Taken 2",
                3:"The House I Live In",
                4:"The Paperboy",
                5:"V/H/S",
                6:"Argo",
                7:"Atlas Shrugged: Part 2",
                8:"Here Comes the Boom",
                9:"Seven Psychopaths",
                10:"Sinister",
                11:"Nobody Walks",
                12:"Smashed",
                13:"War of the Buttons",
                14:"Holy Motors",
                15:"Alex Cross",
                16:"Paranormal Activity 4",
                17:"The First Time",
                18:"The Sessions",
                19:"Tai Chi 0",
                20:"Chasing Mavericks",
                21:"Cloud Atlas",
                22:"Fun Size",
                23:"Silent Hill: Revelation 3D",
                24:"Flight",
                25:"The Man with the Iron Fists",
                26:"Wreck-It Ralph",
                27:"The Bay",
                28:"The Details",
                29:"High Ground",
                30:"Jack and Diane",
                31:"A Late Quartet",
                32:"This Must Be the Place",
                33:"Skyfall",
                34:"The Comedy",
                35:"Nature Calls",
                36:"Silver Linings Playbook",
                37:"The Twilight Saga: Breaking Dawn - Part 2",
                38:"Anna Karenina",
                39:"Dangerous Liaisons",
                40:"Price Check",
                41:"Red Dawn",
                42:"Rise of the Guardians",
                43:"The Central Park Five",
                44:"Rust & Bone",
                45:"Killing Them Softly",
                46:"The Collection",
                47:"Playing for Keeps",
                48:"Deadfall",
                49:"Hyde Park on Hudson",
                50:"Lay the Favorite",
                51:"The Hobbit: An Unexpected Journey",
                52:"Save the Date",
                53:"The Guilt Trip",
                54:"Monsters Inc",
                55:"Amour",
                56:"Zero Dark Thirty",
                57:"Cirque Du Soleil: Worlds Away",
                58:"Jack Reacher",
                59:"This is 40",
                60:"The Impossible",
                61:"Not Fade Away",
                62:"On the Road",
                63:"Django Unchained",
                64:"Les Miserables",
                65:"Parental Guidance",
                66:"Promised Land",
                67:"Quartet",
                68:"Hotel Transylvania"}

