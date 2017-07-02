import re
import heapq
import json
from flask import Flask, request

app = Flask(__name__)


word_dict = {}
list_of_reviews=[]
stop_words = {'a',
 'about',
 'above',
 'after',
 'again',
 'against',
 'ain',
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',
 'aren',
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 'couldn',
 'd',
 'did',
 'didn',
 'do',
 'does',
 'doesn',
 'doing',
 'don',
 'down',
 'during',
 'each',
 'few',
 'for',
 'from',
 'further',
 'had',
 'hadn',
 'has',
 'hasn',
 'have',
 'haven',
 'having',
 'he',
 'her',
 'here',
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 'i',
 'if',
 'in',
 'into',
 'is',
 'isn',
 'it',
 'its',
 'itself',
 'just',
 'll',
 'm',
 'ma',
 'me',
 'mightn',
 'more',
 'most',
 'mustn',
 'my',
 'myself',
 'needn',
 'no',
 'nor',
 'not',
 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',
 'shan',
 'she',
 'should',
 'shouldn',
 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 've',
 'very',
 'was',
 'wasn',
 'we',
 'were',
 'weren',
 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',
 'won',
 'wouldn',
 'y',
 'you',
 'your',
 'yours',
 'yourself',
 'yourselves'}


def preparing_word_dict():
    for i in range(len(list_of_reviews)):
        review_text = list_of_reviews[i][7]
        review_text = re.sub(r'(?<!\S)[^\s\w]+|[^\s\w]+(?!\S)', '', review_text)
        temp = set(review_text.split()[1:]) - stop_words
        for j in temp:
            word_dict.setdefault(j,set()).add(i)


def frequency(words):
    frequency_score = {}
    for word in words:
        for review in word_dict.get(word, []):
            if review in frequency_score:
                frequency_score[review]+=1
            else:
                frequency_score[review]=1
    return frequency_score


def get_top_reviews(frequency_score, k=20):
    temp_list=[]
    for key,value in frequency_score.iteritems():
         temp_list.append((value,list_of_reviews[key][4],key))
    result = heapq.nlargest(k,temp_list)
    output = ''
    for i in result:
        req_review = list_of_reviews[i[2]]
        temp = ''
        for j in req_review:
            temp = temp + "{} <br>".format(j)
        output = output + "<p>{}</p>".format(temp)
    return output


def start_aplication():
    with open("finefoods.txt",'r') as f:
        for i in range(100000):
            review =[]
            for i in range(8):
                review.append(f.readline())
            f.readline()
            list_of_reviews.append(review)
    preparing_word_dict()


def query_api(query_string):
    try:
        query_string = re.sub(r'(?<!\S)[^\s\w]+|[^\s\w]+(?!\S)', '', query_string)
        query_string = query_string.split()
        frequency_score = frequency(query_string)
        if frequency_score == 0:
            return '''<p>"No results found"</p>'''
        return '''<html>
                    <h2> Top 20 Reviews are: </h2> 
                    {}
                </html>'''.format(get_top_reviews(frequency_score))
    except Exception as ex:
        return '''<p>"Failure due to: {}"'''.format(ex)


@app.route('/')
def hello_world():
    return '''
        <form action="/query" method="get">
            <p><input type=text name=que>
            <p><input type=submit value=Submit>
        </form>
    '''

@app.route('/query')
def query_method():
    return query_api(request.args.get('que'))

if __name__ == '__main__':
    start_aplication()
    app.run('127.0.0.1',8060)


