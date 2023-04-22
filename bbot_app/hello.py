import requests
import ast
import json
import demjson3

from bbot_app.biblelist import *


def theContent(bookNo, chNo, verseNo, theVersion):

    bookStr = ''
    urlStr = ''

    # print(bookStr)
    # print(len(bibleList[int(bookNo)-1]["bookChapter"]))
    # print(int(bibleList[int(bookNo)-1]["bookChapter"][int(chNo)-1]["verseno"]))

    if (not(bookNo.isdigit()) or (int(bookNo) <= 0 or int(bookNo) > 66)):
        return("No such book, please try again...")
    elif (not(chNo.isdigit()) or (int(chNo) <= 0 or int(chNo) > (len(bibleList[int(bookNo)-1]["bookChapter"])))):
        return("No such chapter, please try again...")
    elif (not(verseNo.isdigit()) or int(verseNo) <= 0 or int(verseNo) > (int(bibleList[int(bookNo)-1]["bookChapter"][int(chNo)-1]["verseno"]))):
        return("No such verse, please try again...")
    else:
        bookStr = bibleList[int(bookNo)-1]["bookName"]
        urlStr = 'http://getbible.net/json?scrip=' + bookStr + \
            chNo + ':' + verseNo + '&ver=' + theVersion
        # print(urlStr)

        requests.adapters.DEFAULT_RETRIES = 5 #重连次数

        s = requests.session()
        s.keep_alive = False

        t = s.get(url=urlStr)

        txt = '[' + t.text[1:len(t.text)-2] + ']'

        json = demjson3.decode(txt)

        # print(type(json))
        # print(json[0])
        # print(json[0]['book'])
        # print(json[0]['book'][0])
        # print(json[0]['book'][0]['chapter'][verseNo]['verse'])
        # print(urlStr)

        # print(txt)

        # r = json.loads(t.text)

        # print(r)

        # r = requests.get(url=urlStr) 会引起 getbible 回应问题(可能链接数量太多了)

        # print(r.text[1:-2])

        # print(r.text)

        # #---------------------------------------------------
        # #session 里面有啥
        # #mes_dict = ast.literal_eval(r.text[1:-2])

        # # print(mes_dict)

        # myStr = ''

        # prevVerseNr = 0
        # verseNr = 0

        # for val in range(len(mes_dict['book'])):

        #     # print(mes_dict['book'][val]['chapter'])

        #     for mykey, myval in mes_dict['book'][val]['chapter'].items():
        #         if val > 0:
        #             myprevKey = mes_dict['book'][val-1]['chapter'].keys()
        #             prevVerseNr = (list((myprevKey))[0])
        #             verseNr = mykey
        #             # print('---',prevVerseNr,verseNr)

        #         if val == 0:
        #             myStr = myStr + ' ' + myval['verse']
        #         elif val > 0:
        #             if int(verseNr) == int(prevVerseNr) + 1:
        #                 myStr = myStr + ' ' + myval['verse']
        #             else:
        #                 myStr = myStr + ' ... ' + myval['verse']

        # myStr = myStr.replace('\n', '').replace('\r', '').lstrip()
        # # print(myStr)

        # #---------------------------------------------------

        import re

        myStr = json[0]['book'][0]['chapter'][verseNo]['verse']
        newStr = re.sub(r"&lt;", "<", myStr)
        myStr = re.sub(r"&gt;", ">", newStr)

        myStr = myStr.strip()

        return(myStr)

# print(len(bibleList))

# theStr = theContent('66', '22', 'aa', 'basicenglish')
# print(theStr)

# theStrThai = theContent('66', '22', 'bb', 'cut')
# print(theStrThai)
