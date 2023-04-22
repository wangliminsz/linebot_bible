import datetime
import time

import sys
import requests

from thedata import *
from thechpt import *

import random
# from datetime import datetime
from time import sleep

# today = datetime.date.today()
# day_one = datetime.date(today.year, 1, 1)
# num_day = (today - day_one).days + 1

# 指定日期
# specified_date = datetime.datetime(2023, 4, 30)
# # 今天的日期
# today = datetime.datetime.today()
# # 计算时间差
# time_delta = today - specified_date
# # 输出结果
# print("距离指定日期已经过去：", time_delta.days, "天")
# print("Today is day", num_day, "of the year.")

# from datetime import datetime

# date_string = '2023-04-01'
# date_object = datetime.strptime(date_string, '%Y-%m-%d')
# print(date_object)


# ----------------------------------------------------

def myMessage():

    URL = "https://notify-api.line.me/api/notify"

    myLists = notify_data()
    # print(myLists)

    for myRecord in myLists:

        if not myRecord['fields']:

            print("empty record")

        else:

            if 'lineNotifyToken' in (myRecord['fields']):

                ACCESS_TOKEN = myRecord['fields']['lineNotifyToken']

                LINE_HEADERS = {
                "Authorization": "Bearer " + ACCESS_TOKEN
                }

                today = datetime.date.today()
                day_one = myRecord['fields']['startDate']
                date_one = datetime.date(int(day_one[0:4]), int(day_one[5:7]), int(day_one[8:10]))

                num_day = (today - date_one).days
                # num_day = (today - date_one).days + 1
                # print('num ---------------------->', num_day)

                bookNo = myRecord['fields']['bookNo']
                bookChapter = myRecord['fields']['bookChapter']
                theVersion = myRecord['fields']['bookVersion']

                chNo = int(bookChapter) + num_day

                msgContent = theChpt(bookNo, str(chNo), theVersion)

                # ------------------------------

                if msgContent:

                    for i in range(len(msgContent)):

                        MESSAGE = '\r\n\n' + msgContent[i].strip()

                        MESSAGE_FIELD = {"message" : MESSAGE}
                        try:
                            response = requests.post(url=URL,headers=LINE_HEADERS,data=MESSAGE_FIELD)
                            sleepTime = random.randint(1, 3)
                            sleep(sleepTime)
                            print("Response HTTP Status Code: {status_code}".format(status_code=response.status_code))

                        except requests.exceptions.RequestException:
                            print("HTTP Request failed")

                # ------------------------------

            else:

                print("empty content or notify_token")

# ----------------------------------------------------

myMessage()