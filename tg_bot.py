# -*- coding: UTF-8 -*-

import requests

import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import re

from config import tg_token
from config import chat_id

url = "https://api.telegram.org/bot" + tg_token + "/sendPhoto"

title = u"Электрик"
sal = u'100 - 200 m'
desc = u'Чулавек с навыками в электричествах. Можно зверь.'
desc2 = u'Или робототехника. Но не киборги'
city = u'London'
jid = -1

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

if len(sys.argv) > 1:
  title = sys.argv[1].decode('string_escape').decode('utf-8')
if len(sys.argv) > 2:
  sal = sys.argv[2].decode('string_escape').decode('utf-8')
if len(sys.argv) > 3:
  desc = cleanhtml(sys.argv[3].decode('string_escape').decode('utf-8'))
if len(sys.argv) > 4:
  desc2 = cleanhtml(sys.argv[4].decode('string_escape').decode('utf-8'))
if len(sys.argv) > 5:
  city = sys.argv[5].decode('string_escape').decode('utf-8')
if len(sys.argv) > 6:
  jid = sys.argv[6].decode('string_escape').decode('utf-8')
img = Image.open("sample_in.png")
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("BebasNeue.ttf", 16)


draw.text((10, 10),title,(255,255,255), font=font)
draw.text((10, 50),sal,(255,255,255), font=font)
draw.text((160, 50),city,(255,255,255), font=font)
draw.text((10, 110),desc,(255,255,255), font=font)
draw.text((10, 130),desc2,(255,255,255), font=font)
img.save('./../sample-out.png')


files = {'photo': open('./../sample-out.png', 'rb')}

data = {'chat_id' : chat_id, 'caption': title + " (https://hunarmen.com/jobpage?id=" + jid + ")"}

r = requests.post(url, files=files, data=data)