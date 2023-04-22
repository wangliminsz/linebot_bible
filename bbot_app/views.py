from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage
from linebot.models import *

#models.py資料表
from bbot_app.models import *

from bbot_app.biblebklist import *
from bbot_app.hello import *
from bbot_app.biblelist import *

from bbot_app.mstts import *
from bbot_app.mstts2 import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# print(bklist)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message=[]
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        #在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        #message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            #如果事件為訊息
            if isinstance(event, MessageEvent):
                #print(event.message.type)
                if event.message.type=='text':
                    # message.append(TextSendMessage(text='文字訊息'))

                    myContent = ''  # 回覆使用者的內容
                    myContent1 = ''
                    myContent2 = ''

                    ifVerse = False

                    #print(event.message.text)

                    if ("old" in event.message.text.lower()):

                        print("old")
                        for i in range(len(bkoldlist)):
                            myContent =  myContent + bkoldlist[i] + '\n'
                        myContent = 'The Old Testament \n\n' + myContent + '\n' + 'Input book number for chapter list' + '\n\n' + 'Example: 39'
                        # print(myContent)

                    elif ("new" in event.message.text.lower()):
                        for i in range(len(bknewlist)):
                            myContent =  myContent + bknewlist[i] + '\n'
                        myContent = 'The New Testament \n\n' + myContent + '\n' + 'Input book number for chapter list' + '\n\n' + 'Example: 66'

                    elif (event.message.text.isdigit()):
                        # myContent = 'Chapter'
                        # print(event.message.text)
                        if (int(event.message.text)>=1) and (int(event.message.text)<=66):
                            mySequence = int(event.message.text)
                            for i in range(len(bkchlist[mySequence-1])):
                                if i == (len(bkchlist[mySequence-1])-1):
                                    myContent =  myContent + bkchlist[mySequence-1][i] + '\n\n' + 'Format example: \n' +  event.message.text + '-1-1'
                                elif i == 0:
                                    myContent =  myContent + event.message.text + '\n' + bkchlist[mySequence-1][i] + '\n\n'
                                else:
                                    myContent =  myContent + bkchlist[mySequence-1][i] + '\n'
                        else:
                            myContent = "Book number from 1 to 66, please try again..."

                    elif ("-" in event.message.text):
                        theCount = 0
                        thePos = []
                        thePara1 = ''
                        thePara2 = ''
                        thePara3 = ''

                        eventStr = event.message.text.strip()
                        eventStr = ''.join(eventStr.split())
                        print(eventStr)

                        str_list=list(eventStr)
                        for each_char in str_list:
                            theCount+=1
                            if each_char=="-":
                                # print(each_char,theCount-1)
                                thePos.append(theCount-1)
                                # print(thePos)
                                # print(len(thePos))

                        if(len(thePos)>=2):
                            thePara1=eventStr[:thePos[0]]
                            thePara2=eventStr[thePos[0]+1:thePos[1]]
                            thePara3=eventStr[thePos[1]+1:]
                            # print(thePara1)
                            # print(thePara2)
                            # print(thePara3)
                            # myContent=thePara1+"---"+ thePara2+"***"+ thePara3
                            myContent1=theContent(thePara1,thePara2,thePara3,'basicenglish')
                            myContent2=theContent(thePara1,thePara2,thePara3,'cus')
                            #去上游网站取内容

                            if ("No such" in myContent1):
                                myContent = myContent1
                            else:
                                myContent = thePara1 + '\n' + bkchlist[int(thePara1)-1][0] + '\n' + thePara2 + ':' + thePara3 + '\n\n' + myContent1+ '\n\n'+ myContent2
                                ifVerse = True


                        else:
                            myContent = 'Format: **-**-**' + '\n\n' + 'Book-Chapter-Verse' + '\n' + 'Example: 40-5-10' + '\n\n' + 'Input "old" or "new" for the book list'

                    else:
                        myContent = 'Format: **-**-**' + '\n\n' + 'Book-Chapter-Verse' + '\n' + 'Example: 40-5-10' + '\n\n' + 'Input "old" or "new" for the book list'

                    #------------------------------------------------

                    if ifVerse:

                        urlPath = speech_synthesis_to_wave_file(myContent1)
                        durationTime = round(len(myContent1)*9/100)*1000
                        # print(urlPath)
                        # print('-----------url coming')
                        # urlPath = 'https://django9999.herokuapp.com/media/'+urlPath
                        # urlPath = 'https://mybiblecloud.herokuapp.com/static/'+urlPath

                        # -------------2021-09-11

                        # urlPath = 'https://mybiblecloud.herokuapp.com/static/'+urlPath
                        urlPath = 'https://mybiblecloud.herokuapp.com/media/'+urlPath
                        # https://d829-34-96-149-38.ngrok.io

                        # urlPath = 'https://d829-34-96-149-38.ngrok.io/media/'+urlPath

                        # -------------2021-09-11

                        # print('why--------------')
                        # print(urlPath)
                        # print('why--------------')

                        # ------- SDK --------

                        # ##
                        ##
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=myContent))
                        ##
                        # line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=myContent), AudioSendMessage(original_content_url=urlPath, duration=durationTime)])
                        # ##

                        #上面这个是正式的(Verse，带语音)
                    else:
                        #
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=myContent))
                        #
                        #上面这个是正式的(非 Verse)

        return HttpResponse()

    else:
        return HttpResponseBadRequest()