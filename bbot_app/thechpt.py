import requests
import ast
import json
import demjson3

# from bbot_app.biblelist import *
from biblelist import *

def theChpt(bookNo, chNo, theVersion):

    bookStr = ''
    urlStr = ''

    # myContent1=theContent(thePara1,thePara2,thePara3,'basicenglish')

    if (not(bookNo.isdigit()) or (int(bookNo) <= 0 or int(bookNo) > 66)):
        # return("No such book, please try again...")
        return False
    elif (not(chNo.isdigit()) or (int(chNo) <= 0 or int(chNo) > (len(bibleList[int(bookNo)-1]["bookChapter"])))):
        # return("No such chapter, please try again...")
        return False
    # elif (not(verseNo.isdigit()) or int(verseNo) <= 0 or int(verseNo) > (int(bibleList[int(bookNo)-1]["bookChapter"][int(chNo)-1]["verseno"]))):
    #     return("No such verse, please try again...")
    else:
        bookStr = bibleList[int(bookNo)-1]["bookName"]
        urlStr = 'http://getbible.net/json?text=' + bookStr + \
            chNo + '&ver=' + theVersion
        print('urlStr----------------------------->',urlStr)

        requests.adapters.DEFAULT_RETRIES = 5 #重连次数

        s = requests.session()
        s.keep_alive = False

        t = s.get(url=urlStr)

        txt = '[' + t.text[1:len(t.text)-2] + ']'

        json = demjson3.decode(txt)

        # myStr = json[0]['book'][0]['chapter'][verseNo]['verse']
        myBook = json[0]['book_name']
        myChapter = json[0]['chapter_nr']
        # myStr = json[0]['chapter']
        myStr = ''
        myLen = len(json[0]['chapter'])

        for vNo in range(myLen):
            vIdx =  str(vNo+1)
            myStr = myStr + myBook + " " + str(myChapter) + ":" + str(vIdx) + "\r\n" + json[0]['chapter'][vIdx]['verse'] + "\r\n"

        import re

        # my_string = "The quick brown fox jumps over the lazy dog."
        newStr = re.sub(r"&lt;", "<", myStr)
        myStr = re.sub(r"&gt;", ">", newStr)

        print('return myLen--------------------->', myLen)
        # print(myStr)

        if myStr:

            # big_string = "This is a big string with more than 990 characters. It needs to be split into smaller strings."
            chunk_size = 990
            chunks = [(myStr[i:i+chunk_size]) for i in range(0, len(myStr), chunk_size)]

            # nM = 990
            # myStr1 = myStr[0:nM*1]
            # myStr2 = myStr[nM*1:nM*2]
            # myStr3 = myStr[nM*2:nM*3]
            # myStr4 = myStr[nM*3:nM*4]
            # myStr5 = myStr[nM*4:nM*5]
            # myStr6 = myStr[nM*5:nM*6]
            # myStr7 = myStr[nM*6:nM*7]
            # myStr8 = myStr[nM*7:nM*8]
            # myStr9 = myStr[nM*8:nM*9]
            # myStra = myStr[nM*9:nM*10]
            # myStrb = myStr[nM*10:nM*11]
            # myStrc = myStr[nM*11:nM*12]
            # myStrd = myStr[nM*12:nM*13]
            # myStre = myStr[nM*13:nM*14]
            # myStrf = myStr[nM*14:nM*15]
            # myStrg = myStr[nM*15:nM*16]
            # myStrh = myStr[nM*16:nM*17]
            # myStri = myStr[nM*17:nM*18]

            print('chunks size------------------->', len(chunks))
            # print(chunks[10])

            return(chunks)


# theChpt('19','119','basicenglish')
# theChpt('19','119','cut')
# print(theChpt('77','100','cnt'))

