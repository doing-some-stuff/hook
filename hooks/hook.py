from discord_webhook import DiscordWebhook,DiscordEmbed
import requests
import json
import re
import os
from dotenv import load_dotenv as env
import datetime
from selenium import webdriver as wdr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

sentlogs="./hooks/hook/contentlist.log"
errlogs="./hooks/hook/err.log"

if not os.path.exists(sentlogs):
  with open(sentlogs,"w") as ff:
    pass
if not os.path.exists(errlogs):
    with open(errlogs,"w") as ff:
        pass

env()
try:
  idexclude = eval(os.getenv("Showswatching"))
  rune=os.getenv('Rune')
  hooklink=os.environ['Hooksecret']
except Exception as ee:
  with open(errlogs,"a+") as ff:
    err=f"{datetime.datetime.today()}||Err: {ee}\n"
    ff.write(err)
    exit()
      
def new():
    link = 'https://animepahe.com/api?m=airing&page=1'
    options = Options()
    options.add_argument("--headless")
    pageviewer = wdr.Firefox(options=options)
    pageviewer.get(link)
    WebDriverWait(pageviewer, 8)
    pageviewer.refresh()
    rawcontent=pageviewer.page_source

    jsoncontent=re.findall('<div id="json">(.*?)</div></div>', rawcontent, re.DOTALL)[0]
    response =json.loads(jsoncontent)
    allshowsreleased=[
        [
            '{}/{}'.format(x['anime_session'], x['session']),
            x['episode'],
            x['anime_title'],x['snapshot']
        ] for x in response['data']
    ]
    showsreleased=[]
    for entry in allshowsreleased:
        if entry[2] in idexclude:
            showsreleased.append(entry)
    return showsreleased


def hookgenerate(contentlist):
  with open(sentlogs,"+r") as ff:
    sentshows=ff.readlines()
  for show in contentlist:
    if f"{show[2]} - Episode {show[1]}\n" in sentshows:
      continue
    try:
      text=f"# {rune}  |  [{show[2]} - Episode {show[1]}](<https://animepahe.com/play/{show[0]}>)\n[Main Page](https://animepahe.com/play/{show[0]}*)"
      webhook = DiscordWebhook(url=hooklink,content=text)
      webhook.execute()
      entrno=len(sentshows)
      title=f"{show[2]} - Episode {show[1]}\n"
      if entrno>18:
        with open(sentlogs,"w") as ff:
          newsshow=''.join(sentshows[8:])
          ff.write(newsshow)
        with open(errlogs,"w") as ff:
          pass
        
      with open(sentlogs,"a+") as ff:
        ff.write(title)
    except Exception as ee:
      with open(errlogs,"a+") as ff:
                err=f"{datetime.datetime.today()}||Webhook Err: {ee}\n"
                ff.write(err)



try:
  hookgenerate(new())
except Exception as ee:
  with open(errlogs,"a+") as ff:
    err=f"{datetime.datetime.today()}||Err: {ee}\n"
    ff.write(err)
