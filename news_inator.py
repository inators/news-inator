import requests
from guizero import App, Text
from pprint import pprint
import textwrap
import webbrowser

storyCounter = -1

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
    
    showNews()
    
    app.repeat(15*1000,showNews)
    app.repeat(10*60*1000,refreshNews)
    newsText.when_clicked = openURL
    newsDesc.when_clicked = openURL
    app.display()

   

def refreshNews():
    global stories
    global apiKey
    url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=%s' % apiKey)
    response = requests.get(url)
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



if __name__ == '__main__':
    main()
