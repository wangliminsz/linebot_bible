import azure.cognitiveservices.speech as speechsdk
import os, requests, time
from datetime import datetime
from b_bot.settings import MEDIA_ROOT
from b_bot.settings import STATIC_ROOT

from xml.etree import ElementTree

def speech_synthesis_to_wave_file(strPara):

    # speech_key, service_region = "a57492ce5fda417f87989ad82e806b86", "southeastasia"
    speech_key, service_region = "75e5cc9b5d124cdcb9a6d6a62ac6faca", "southeastasia"

    # -------------2021-09-11
    # timestr = time.strftime("%Y%m%d-%H%M")
    # timestr = time.strftime('%Y%m%d-%H%M%S-%f')[:-3]

    timestr = datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')[:-3]
    print(timestr)
    print('time------------------')
    # -------------2021-09-11

    """performs speech synthesis to a wave file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.

    fileName = 'sample-' + timestr + '.wav'

    # -------------2021-09-11
    #filePath = STATIC_ROOT + fileName
    filePath = MEDIA_ROOT + fileName
    # -------------2021-09-11

    # file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=filePath)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to wave file.

    print("-----------Start------------")

    try:
        # text = "Hello World Hello Microsoft Hello Everyone" #input()

        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        # voice.set('name', 'zh-CN-XiaoxiaoNeural') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.set('name', 'en-US-JennyNeural')
        prosody = ElementTree.SubElement(voice, 'prosody')
        prosody.set('rate', '-20%')

        prosody.text = strPara
        #prosody.text = 'Hello World Hello Microsoft Hello Everyone'

        ssmlBody = ElementTree.tostring(xml_body)
        ssml = ssmlBody.decode("utf-8", errors="ignore")
        print(ssml)

    except EOFError:
        return

    #plaintext
    #result = speech_synthesizer.speak_text_async(text).get()

    #ssml = "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'><voice name='Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)'><bookmark mark='bookmark_one'/> one. <bookmark mark='bookmark_two'/> two. three. four.</voice></speak>";
    #result = speech_synthesizer.speak_ssml_async(ssmlBody).get()
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text,filePath))
        print("good")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return fileName
