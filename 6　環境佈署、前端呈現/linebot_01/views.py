from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, ImageMessage ,TextMessage, PostbackEvent,TextSendMessage ,ImageSendMessage
from module import func
import main_gan
import argparse
from Dlib_faces_cut import face_cut
from urllib.parse import parse_qsl
import os
import time
import requests

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '#我的推薦#':
                        func.sendText(event)

                    elif mtext == '#模擬上妝#':
                        func.openCameraRoll(event)

                    elif mtext == '#教學文章#':
                        # func.sendStick(event)
                        func.sendText(event)
                    elif mtext == '#情境小幫手#':
                        func.sendMulti(event)

                    elif mtext == '#熱門排行#':
                        func.sendPosition(event)

                    if mtext == '#聯絡我們# ':
                        func.sendQuickreply(event)
                elif isinstance(event.message,ImageMessage):
                    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Image has upload'))
                    message_content = line_bot_api.get_message_content(event.message.id)
                    print(message_content)
                    # with open('C:/Users/Big data/Desktop/db104_2_project/templates/' + event.message.id + '.jpg','wb')as fd:
                    with open('C:/Users/Big data/Desktop/db104_2_project/static/123.jpg','wb')as fd:
                        for chunk in message_content.iter_content():
                            fd.write(chunk)
                    temp_pic = 'C:/Users/Big data/Desktop/db104_2_project/static/123.jpg'
                    temp_pic_1 = 'C:/Users/Big data/Desktop/db104_2_project/static/456.jpg'
                    # parser1 = argparse.ArgumentParser()
                    # parser1.add_argument('--static', type=str,default=os.path.join(path=temp_pic_1),help='path to the no_makeup image')
                    # args = parser1.parse_args()
                    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='good'))

                    while True :
                        if os.path.isfile(temp_pic):
                            face_cut.detect_face_landmarks(temp_pic)
                            time.sleep(1)
                            main_gan.make_upup(temp_pic_1)
                            time.sleep(1)
                            func.sendMulti_send_image(event)
                            #line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://2a9944ea.ngrok.io/static/result.jpg', preview_image_url='https://2a9944ea.ngrok.io/static/result.jpg') ,)
                            #time.sleep(5)

                            # time.sleep(8)
                            # send_res = send_image()
                            # print(send_res)


                        else:
                            time.sleep(1)
                        break

        return HttpResponse()

    else:
        return HttpResponseBadRequest()



