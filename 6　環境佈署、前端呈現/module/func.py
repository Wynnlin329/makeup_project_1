from django.conf import settings
from pymongo import MongoClient
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction,\
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,\
    ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate,\
    CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn,URIAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendText(event):  #傳送文字
    try:
        conn = MongoClient('mongodb://10.120.38.27:15000/')
        db = conn.teach_data
        collection = db.eyes

        # test if connection success
        collection.stats

        coursor = collection.find_one({})

        message = TextSendMessage(
            text = str(coursor)

        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

# def openCameraRoll(event):  #打開相簿
#     try:
#         message =URIAction(
#
#             uri='line://nv/cameraRoll/single'
#
#         )
#
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendStick(event):  #傳送貼圖
    try:
        message = StickerSendMessage(  #貼圖兩個id需查表
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendMulti(event):  #多項傳送
    try:
        message =ImageSendMessage(  #傳送圖片
                original_content_url = "https://2a9944ea.ngrok.io/static/result.jpg",
                preview_image_url = "https://2a9944ea.ngrok.io/static/result.jpg"
            )

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendMulti_send_image(event):  #我要傳一張化妝圖片
    try:
        message =[TextSendMessage(text="請打開") ,
                  ImageSendMessage(  #傳送圖片
                original_content_url = "https://2a9944ea.ngrok.io/static/result.jpg",
                preview_image_url = "https://2a9944ea.ngrok.io/static/gift.jpg"
            )]

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendPosition(event):  #傳送位置
    try:
        message = LocationSendMessage(
            title='101大樓',
            address='台北市信義路五段7號',
            latitude=25.034207,  #緯度
            longitude=121.564590  #經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQuickreply(event):  #快速選單
    try:
        message = TextSendMessage(
            text='請選擇最喜歡的程式語言',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Python", text="Python")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Java", text="Java")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="C#", text="C#")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Basic", text="Basic")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def openCameraRoll(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',  #顯示的圖片
                title='按鈕樣版示範',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    URITemplateAction(  #開啟相機
                        label='開啟相機',
                        uri='line://nv/camera/'
                    ),
                    URITemplateAction(  #開啟相簿
                        label='開啟相簿',
                        uri='line://nv/cameraRoll/single'
                    ),
                    PostbackTemplateAction(  #執行Postback功能,觸發Postback事件
                        label='回傳訊息',  #按鈕文字
                        #text='@購買披薩',  #顯示文字計息
                        data='action=buy'  #Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))