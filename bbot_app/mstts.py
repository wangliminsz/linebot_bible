import os, requests, time
from xml.etree import ElementTree

from b_bot.settings import MEDIA_ROOT

subscription_key = 'a57492ce5fda417f87989ad82e806b86'

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        # self.tts = input("What would you like to convert to speech: ")
        # self.tts = '这是 Line Bot 的测试，你好我来了，你好'

        #2021-09-06---------------------------

        #2021-09-06---------------------------

        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        response.encoding = 'utf-8'
        self.access_token = str(response.text)

        print('token-----------')
        print(response.encoding)
        print('token-----------')
        print(self.access_token)
        print('token-----------')


    def save_audio(self,strPara):

        #---------------------2021-09-06

        self.tts = strPara

        #---------------------2021-09-06
        #  
        base_url = 'https://southeastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            # 'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'X-Microsoft-OutputFormat': 'audio-48khz-192kbitrate-mono-mp3',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        # voice.set('name', 'zh-CN-XiaoxiaoNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.set('name', 'en-US-JennyNeural')
        prosody = ElementTree.SubElement(voice, 'prosody')
        prosody.set('rate', '-20%')

        prosody.text = self.tts

        #2021-09-06----------------
        # <prosody rate="+30.00%">
 
        body = ElementTree.tostring(xml_body)
        # print(body)

        print('-----------------')

        print(constructed_url)
        print('-----------------')
        print(headers)
        print('-----------------')
        print(body)
        print('-----------------')

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            fileName = 'sample-' + self.timestr + '.wav'
            filePath = MEDIA_ROOT + fileName
            
            # with open(MEDIA_ROOT + 'sample-' + self.timestr + '.wav', 'wb') as audio:
            with open(filePath, 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")

        return fileName

    def get_voices_list(self):
        base_url = 'https://southeastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

# if __name__ == "__main__":
#     app = TextToSpeech(subscription_key)
#     app.get_token()
#     app.save_audio()
#     # Get a list of voices https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
#     # app.get_voices_list()
