from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json
import requests
from bs4 import BeautifulSoup
import time
info='A 行政大樓 \nB 商管大樓\nC 鍾靈化學館\nCL 蘭陽校園\nD 台北校園\nE 工學大樓\nED 教育館\nF 會文館\nFL 外國語文大樓\nG 工學館\nH 宮燈教室\nHC 守謙國際會議中心\nI 覺生綜合大樓\nJ 麗澤國際學舍\nM 海事博物館\nN 紹謨紀念游泳館\nO 傳播館\nQ 傳播館\nR 學生活動中心\nS 騮先紀念科學館\nSG 紹謨紀念體育館\nT 驚聲紀念大樓\nU 覺生紀念圖書館\nV 視聽教育館\nZ 松濤館'
lib='《圖書館》\n◆總館\n週一～週五：08:20 ~ 21:50\n週六～週日：08:20 ~ 21:50\n*借還時間為閉館前20分鐘\n◆總館非書資料室\n週一～週五：08:20 ~ 21:50\n週六～週日：13:00 ~ 16:50\n*借還時間為閉館前20分鐘\n◆總館自習室\n週一：12:00-21:45 (上午清潔不開放)\n週二～週六：06:00-21:45\n週日：06:00-16:45\n資料來源：https://www.lib.tku.edu.tw/zh_tw/About_us/hours/Semester'
center='《資中、玻璃屋》\nB201、B203、B204、B206、B213、E314 \n110/2/22～110/6/25\n開放時間：週一至週五：8:20～21:00。\n資料來源：http://www.ipcedu.tku.edu.tw/pcservice/pcservice-open.html'
def weather():
    r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069?Authorization=CWB-EBFEF59A-34C8-49BC-A84F-C95E269549B7&format=XML&locationName=%E6%B7%A1%E6%B0%B4%E5%8D%80&elementName=Wx,AT,T,RH,CI,PoP6h,WS,WD')
    soup = BeautifulSoup(r.text, 'lxml')
    a_tags = soup.find_all(["description","starttime","value","measures"])
    for i in range(len(a_tags)):
        if a_tags[i].string == "天氣現象":
            WX = a_tags[i].string + ' : '+ a_tags[i+2].string
        elif a_tags[i].string == "體感溫度":
            AT = a_tags[i].string + ' : '+a_tags[i+1].string + ' ' + a_tags[i+2].string
        elif a_tags[i].string == "溫度":
            T = a_tags[i].string+' : '+a_tags[i+1].string+' '+a_tags[i+2].string
        elif a_tags[i].string == "相對濕度":
            RH = a_tags[i].string+' : '+a_tags[i+1].string+' '+a_tags[i+2].string
        elif a_tags[i].string == "舒適度指數":
            CI = a_tags[i].string+' : '+a_tags[i+3].string
        elif a_tags[i].string == "6小時降雨機率":
            PoPh6 = a_tags[i].string+' : '+a_tags[i+2].string+' '+a_tags[i+3].string
        elif a_tags[i].string == "風速":
            WS = a_tags[i].string+' : '+a_tags[i+1].string+' '+a_tags[i+2].string
        elif a_tags[i].string == "風向":
            WD = a_tags[i].string+' : '+a_tags[i+1].string+' '+a_tags[i+2].string
    return WX+'\n'+AT+'\n'+T+'\n'+RH+'\n'+CI+'\n'+PoPh6+'\n'+WS+'\n'+WD

    


calendar=TemplateSendMessage(
    alt_text='ImageCarousel template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://i.imgur.com/JHoQ5Xg.png',
                action=PostbackAction(
                    label='2、3月',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url='https://i.imgur.com/PUTvUgG.png',
                action=PostbackAction(
                    label='4、5月',
                    data='action=buy&itemid=2'
                )
            ),
                        ImageCarouselColumn(
                image_url='https://i.imgur.com/isntBij.png',
                action=PostbackAction(
                    label='6、7月',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)
app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('fNUmdwjb36kT5Fv3a2EyPRF+0cIxQIGOz6cqikXxbjsyOg/9zRrna8v3K8VI8etW1eub+ETlBRveDIlCHIA3Nj98aOFUuGhfjparCyovn79K1lq5R7mcZZzwgoy4uCGcShykK9gxJUKp12P64/gS7wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5fae52882c597bdfbd02e56959ff34e2')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    if(message == '建築物對照'):
        text_message = TextSendMessage(text = info)
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '天氣'):
        text_message = TextSendMessage(text = weather())
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '圖書館開放時間'):
        text_message = TextSendMessage(text = lib)
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '資中、玻璃屋開放時間'):
        text_message = TextSendMessage(text = center)
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '行事曆'):
        line_bot_api.reply_message(reply_token, calendar)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)