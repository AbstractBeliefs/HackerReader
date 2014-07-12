import urllib2
from bs4 import BeautifulSoup
import json

from flask import Flask
app = Flask(__name__)

def titleFinder(tag):
    return not tag.has_attr("valign") and "title" in tag.get('class', [])

@app.route("/")
def index():
    return "HackerReader API Source"

@app.route("/page/<path:next>")
def pageAPI(next):
    if next == "0":
        hnpath = ""
    elif next == "news2":
        hnpath = next
    else:
        hnpath = "x?fnid=%s" %next

    req = urllib2.Request("https://news.ycombinator.com/%s" %hnpath, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(urllib2.urlopen(req).read())
    titleTags = soup.find_all(titleFinder)

    stories = []
    for titleTag in titleTags:
        stories.append({
            "title": titleTag.text,
            "url": titleTag.a['href']
        })
    try:
        page = {
            "status": 200,
            "stories": stories[:-1],
            "next": stories[-1]["url"].split("=")[-1]
        }
    except IndexError:  # No stories
        return json.dumps({"status": 404}), 404
    return json.dumps(page)

if __name__ == "__main__":
    app.run(debug=True)
