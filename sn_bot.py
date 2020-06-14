# -*- coding: UTF-8 -*-

import requests

import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import re

import time
import os

from config import tg_token
from config import tg_chat_id

from config import vk_access_token
from config import vk_group_id
vk_owner_id = -vk_group_id


title = u"Электрик"
sal = u'100 - 200 m'
desc = u'Чулавек с навыками в электричествах. Можно зверь.'
desc2 = u'Или робототехника. Но не киборги'
#продумать еще desc, сейчас если присылается начало тэга, то не обрезается: <strong style="....
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
caption = title + " (https://hunarmen.com/jobpage?id=" + str(jid) + ")"

img = Image.open("sample_in.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("BebasNeue.ttf", 16)
draw.text((10, 10),title,(255,255,255), font=font)
draw.text((10, 50),sal,(255,255,255), font=font)
draw.text((160, 50),city,(255,255,255), font=font)
draw.text((10, 110),desc,(255,255,255), font=font)
draw.text((10, 130),desc2,(255,255,255), font=font)


try:
  os.makedirs('./www/statics/sn_posted/')
except OSError:
  pass
current_name = './www/statics/sn_posted/' + time.strftime("%Y%m%d-%H%M%S") + '_' + str(jid) + '.png'
img.save(current_name)


#tg part
files = {'photo': open(current_name, 'rb')}
tg_url = "https://api.telegram.org/bot" + tg_token + "/sendPhoto"
data = {'chat_id' : tg_chat_id, 'caption': caption}
requests.post(tg_url, files=files, data=data)


#vk part
#получить адрес загрузки фото
vk_get_wall_url = 'https://api.vk.com/method/photos.getWallUploadServer'
params = (
    ('v', '5.110'),
    ('access_token', vk_access_token),
    ('group_id', vk_group_id),
)
response = requests.get(vk_get_wall_url, params=params)
vk_upload_url = response.json()['response']['upload_url']

files = {'photo': open(current_name, 'rb')}
#отправить фото
response = requests.post(vk_upload_url, files=files)
req2json = response.json()
vk_save_wall_url = 'https://api.vk.com/method/photos.saveWallPhoto'
vk_server1 = req2json['server']
vk_hash1 = req2json['hash']
vk_photo1 = req2json['photo']
params = (
    ('v', '5.110'),
    ('access_token', vk_access_token),
    ('group_id', vk_group_id),
    ('server', vk_server1),
    ('hash', vk_hash1),
    ('photo', vk_photo1),
)
#сохранить что-то там фото на стену?
response = requests.post(vk_save_wall_url, params=params)

vk_pic_id = response.json()['response'][0]['id']
vk_owner_id1 = response.json()['response'][0]['owner_id']
vk_attach1 = 'photo' + str(vk_owner_id1) + '_' + str(vk_pic_id)

params = (
  ('v', '5.110'),
  ('message', caption),
  ('owner_id', vk_owner_id),
  ('from_group', '1'),
  ('access_token', vk_access_token),
  ('attachments', vk_attach1),
)
#сделать пост на стену
requests.get('https://api.vk.com/method/wall.post', params=params)

