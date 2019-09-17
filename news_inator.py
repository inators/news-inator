import requests
from guizero import App, Text
from pprint import pprint
import textwrap
import webbrowser

storyCounter = 0

def main():
    global newsText
    global stories
    global apiKey
    global newsDesc
    
    f = open('apiKey.txt','r')
    apiKey = f.read()
    f.close()

    refreshNews()
    
    app = App(title='News-inator', width=600, height=400)
    newsText = Text(app,size=16)
    newsDesc = Text(app,size=12)
    
    lines = textwrap.wrap(stories[0]['title'], 54)
    newsText.value = ('\n'.join(lines))
    lines = textwrap.wrap(stories[0]['description'],72)
    newsDesc.value = ('\n'.join(lines))
    
    app.repeat(15*1000,showNews)
    app.repeat(10*60*1000,refreshNews)
    newsText.when_clicked = openURL
    app.display()

   

def refreshNews():
    global stories
    global apiKey
    url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=%s' % apiKey)
    response = requests.get(url)
    articles =  response.json()
    stories = articles['articles']

def showNews():
    global storyCounter
    global newsText
    global stories
    storyCounter += 1
    if storyCounter >= len(stories):
        storyCounter = 0
    story = stories[storyCounter]['title']
    story = "%d of %d - %s" % ((storyCounter + 1),(len(stories)), story ) 
    lines = textwrap.wrap(story, 54)
    newsText.value = ('\n'.join(lines))
    lines = textwrap.wrap(stories[storyCounter]['description'],72)
    newsDesc.value = ('\n'.join(lines))

    
def openURL():
    global storyCounter
    global stories
    url = stories[storyCounter]['url']
    webbrowser.open(url)



if __name__ == '__main__':
    main()
