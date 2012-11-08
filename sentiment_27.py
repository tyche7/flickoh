'''
@FlickOh
INFO 290 Final Project

some libraries are compatible with Python 3.0 or later
'''

import json
import urllib
import urllib2
import re
import sys

response = ''
MAX_ITEMS = 8000
API_URI = "http://www.sentiment140.com/api/bulkClassifyJson?appid=natth@math.berkeley.edu"

def get_sentiment(filename, query):
    """ Get sentiment analysis of tweets in the specified file

    This function makes use of the API provided by sentiment140.com.

    filename - the file is assumed to be in the json format where
    the first line can be discarded ({ "data" : [\n')
    and each item is in a separate line.
    query - a term or terms that should not be used to determine
    the sentiment of tweets. 
    """
    
    #infile = open("bigger_test", "r")
    infile = open(filename, 'r')
    infile.readline()  # discard the header
    
    #out = open("test2_with_sen", "w")
    out = open(filename+'_q_'+query, 'w')
    out.write('{ "data" : [\n')
    reached_EOF = False

    while (not reached_EOF):               
        first = True
        count = 0
        POST_data = ''
        global MAX_ITEMS
        while (count < MAX_ITEMS):            
            tweet = infile.readline().decode("utf-8", "replace")      
            if (not tweet):             
                reached_EOF = True
                break
            tweet = extract_text(tweet, query)           
            #print(newline+"\n")
            if (tweet == ''): continue
            if (first):
                POST_data = '{ "data" : [\n' + tweet            
                first = False
            else :
                POST_data = POST_data + ',\n' + tweet
            count = count + 1
        
        global response
        if (POST_data == ''): continue
        POST_data = POST_data + ']}'

        global API_URI
        req = urllib2.Request(API_URI, POST_data)
        response = urllib2.urlopen(req)
        #response = urllib.request.urlopen(API_URI, POST_data.encode('utf8'))
        results = response.read()

        results_json = json.loads(results)
        print(len(results_json['data']))
        for item in results_json['data'][:-1]:
            out.write(json.dumps(item) +',\n')
            
        out.write(json.dumps(results_json['data'][-1]))
        if (reached_EOF): out.write(']}\n')
        else : out.write(',\n')
                
        #start = results.find('[{')
        #if (reached_EOF):
        #    out.write(results[(start+1):])
        #else : out.write(results[(start+1):-3]+',\n')

    print("done")
    infile.close()
    out.close()
    
"""
Internal Function: extract_text
Take a full tweet (a line from the tweet file which ends with
either ',\n' or ']}\n') and return a json item with only three
fields i.e. texts,id, and query. Also in the text field, replace
any URL with <URL>
hashtag with <HT>
user_mentions with <UM>
"""

def extract_text(fulltweet, query):
    data = {}
    if (fulltweet.find(',\n') != -1):
        data = json.loads(fulltweet[:-2])
    else :
        data = json.loads(fulltweet[:-2])

    newtext = data['text']    
    # won't need this after the filtering is done
    if (newtext.lower().find(query.lower()) == -1):
        return ''
    
    for item in data['entities']['hashtags']:
        newtext = newtext.replace('#'+item['text'], '<HT>')
    for item in data['entities']['urls']:
        newtext = newtext.replace(item['url'], '<URL>')
    for item in data['entities']['user_mentions']:
        newtext = newtext.replace('@'+item['screen_name'], '<UM>')

    newtext = re.sub("[^a-zA-Z0-9<>\\s]", "", newtext)
    # format : { "id":239011567, "text":"hello world!", "query":"skyfall" }
    return ('{\"id\":'+str(data['id'])+',\"text\":'+'\"'+newtext+
            '\", \"query\":\"'+query+'\"}')


if __name__ == '__main__':
    get_sentiment(str(sys.argv[1]), str(sys.argv[2]))    
