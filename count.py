import os
import re
import json
import random
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv()


CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

'''
For first testing, you can comment the code below after you check your linebot can send you the message below
'''
CHANNEL_ID = os.getenv('LINE_UID')


@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

def handle_textmessage(event):
    message = TextSendMessage(text= event.message.text)
    if message.text.lower() == "anya":
        id = random.randint(1, 40)
        url = f"https://spy-family.net/assets/img/special/anya/{id}.png"
        My_LineBotAPI.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
        )
    else:
        #num = re.sub('[a-zA-z!@#$%^&_= ]','',message.text) # can deal with Letters&Sign
        #if num.find("+")+1 >len(num)-1 or num.find("-")+1 >len(num)-1 or num.find("*")+1 >len(num)-1 or num.find("/")+1 >len(num)-1:    
        if re.findall('[a-zA-z!@#$%^&_]',message.text):
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text = "輸入包含非數值!!")
            )
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(text = eval(str(message.text)))
            )

class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id

my_sticker = [My_Sticker(p_id='446', s_id='1995'), My_Sticker(p_id='446', s_id='2012'),
     My_Sticker(p_id='446', s_id='2024'), My_Sticker(p_id='446', s_id='2027'),
     My_Sticker(p_id='6325', s_id='10979923'), My_Sticker(p_id='789', s_id='10877'),
     My_Sticker(p_id='6362', s_id='11087938'), My_Sticker(p_id='789', s_id='10885'),
     My_Sticker(p_id='6136', s_id='10551391'),
     ]

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ran_sticker = random.choice(my_sticker)
    # Reply Sticker Message
    My_LineBotAPI.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id= ran_sticker.packageID,
            sticker_id= ran_sticker.stickerID
        )
    )



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='count:app', reload=True, host='0.0.0.0', port=1234)