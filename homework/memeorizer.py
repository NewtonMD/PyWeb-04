'''______________________________________________________
Mike Newton
newton33@uw.edu
Web Programming With Python 100
University of Washington, Spring 2016
Last Updated:  27 April 2016
Python Version 3.5.1
______________________________________________________'''

"""The MEMEORIZER acquires a phrase from one of two sources, and applies it
to one of two meme images.

The two possible sources are:

  1. A fact from http://unkno.com
  2. One of the 'Top Stories' headlines from http://www.cnn.com

For the CNN headline you can use either the current FIRST headline, or
a random headline from the list. I suggest starting by serving the FIRST
headline and then modifying it later if you want to.

The two possible meme images are:

  1. The Buzz/Woody X, X Everywhere meme
  2. The Ancient Aliens meme

  You options are:
        http://localhost:8080/fact/buzz
        http://localhost:8080/fact/aliens
        http://localhost:8080/news/buzz
        http://localhost:8080/news/aliens

        Just type one of those in your address bar and enjoy."""

from bs4 import BeautifulSoup
import requests
import random


def meme_it(text,image):
    url = 'http://cdn.meme.am/Instance/Preview'
    if image == 'buzz':
        image_id = 2097248
    elif image == 'aliens':
        image_id = 627067
   
    params = {
        'imageID': image_id,
        'text1': text
    }

    response = requests.get(url, params)

    return response.content


def parse_fact(body):
    parsed = BeautifulSoup(body, 'html5lib')
    fact = parsed.find('div', id='content')
    return fact.text.strip()

def get_fact():
    response = requests.get('http://unkno.com')
    return parse_fact(response.text)

def parse_news(body):
    parsed = BeautifulSoup(body, 'html5lib')
    hlines_set = parsed.find_all('span', class_='cd__headline-text')

    #turn bs4 set into a list of strings
    hlines_list = []
    for x in hlines_set:
        hlines_list.append(x.text.strip())

    #select a random headline from CNN    
    news = random.choice(hlines_list)

    return news

def get_news():
    response = requests.get('http://cnn.com')
    return parse_news(response.text)

def process(path):
    args = path.strip("/").split("/")
    if args[0] == 'fact':
        meme_text = get_fact()
        meme = meme_it(meme_text,args[1])
    elif args[0] == 'news':
        meme_text = get_news()
        meme = meme_it(meme_text,args[1])

    return meme

def application(environ, start_response):
    headers = [('Content-type', 'image/jpeg')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        body = process(path)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
