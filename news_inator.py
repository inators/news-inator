#!/usr/bin/python3

import requests
from guizero import App, Text
from pprint import pprint
import textwrap
import webbrowser
import socket
import logging
from time import sleep


logging.basicConfig(level=logging.INFO, filename='news-inator.log')

storyCounter = -1
app = App(title='News-inator', width=600, height=400)

def main():
    global newsText
    global stories
    global apiKey
    global newsDesc
    global app
    
    f = open('apiKey.txt','r')
    apiKey = f.read()
    f.close()

    refreshNews()
    

    newsText = Text(app,size=16)
    newsDesc = Text(app,size=12)
    
    showNews()
    
    app.repeat(15*1000,showNews)
    app.repeat(120*60*1000,refreshNews)
    newsText.when_clicked = openURL
    newsDesc.when_clicked = openURL
    app.display()

   

def refreshNews():
    global stories
    global apiKey
    global app
    
    url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=%s' % apiKey)
    try:    
        response = requests.get(url)
    except requests.ConnectionError:
        app.title = 'News-inator ** Connection Error **'
        print("Connection error")
        logging.exception("connection error")
        return 
    
    app.title = 'News-inator'
    articles =  response.json()
    if 'articles' in articles:
        stories = articles['articles']
    else:
        pprint(articles)


def showNews():
    global storyCounter
    global newsText
    global stories
    storyCounter += 1
    if not "stories" in globals():
        return False
    if storyCounter >= len(stories):
        storyCounter = 0
    story = stories[storyCounter]['title']
    story = "%d of %d - %s" % ((storyCounter + 1),(len(stories)), story ) 
    description = stories[storyCounter]['description']
    if len(story) > 54:
        lines = textwrap.wrap(story, 54)
        newsText.value = ('\n'.join(lines))
    else:
        newsText.value = story
    if description == None:
        newsDesc.value = ""
        return
    charList = [description[x] for x in range(len(description)) if ord(description[x]) in range(65536)]
    description = ''
    for x in charList:
        description += x

    if len(description) > 72:    
        lines = textwrap.wrap(description,72)
        newsDesc.value = ('\n'.join(lines))
    else:
        newsDesc.value = description
    
def openURL():
    global storyCounter
    global stories
    url = stories[storyCounter]['url']
    webbrowser.open(url)

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check for internet connectivity by trying to establish a socket connection.
    :param host: Host to connect to (default is Google's public DNS server).
    :param port: Port to connect to (default is 53, the DNS service port).
    :param timeout: Connection timeout in seconds.
    :return: True if the connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        return True
    except socket.error:
        return False
def wait_for_internet_connection(interval=5):
    """
    Wait for an internet connection, checking periodically.
    :param interval: Time in seconds between checks.
    """
    print("Checking for internet connection...")
    while not check_internet_connection():
        print("No internet connection available. Waiting...")
        time.sleep(interval)
    print("Internet connection established.")




if __name__ == '__main__':
    try:
        wait_for_internet_connection()
        main()
    except Exception as e:
        logging.exception("Something happened")
