import speech_recognition as sr
import time
import os
import random
from gtts import gTTS
from audioplayer import AudioPlayer
from transformers import pipeline
from googletrans import Translator

context = """My name is Harry. I am 24 years old. I am a male. 
My favourite sports are football and basketball. I am currently
studying at Vellore Institute of Technology. My favourite colour 
is red."""

r = sr.Recognizer()

question_answerer = pipeline("question-answering")
flag = 1
translator = Translator()

print("Welcome! Language choice: English(0) Hindi (1)")
n = int(input())


def record_audio_to_speech(ask=False):
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            if (n == 0):
                voice_data = r.recognize_google(audio)
            if (n == 1):
                voice_data = r.recognize_google(audio, language='hi-In')
                print(voice_data)
                voice_data = translator.translate(voice_data)
                voice_data = voice_data.text
        except sr.UnknownValueError:
            melon_speak('Sorry, I did not get that')
        except sr.RequestError:
            melon_speak('Sorry, my speech service is unavailable at the moment')
        return voice_data


def melon_speak(audio_string):
    if (n == 0):
        tts = gTTS(text=audio_string, lang='en', tld='co.uk')
    else:
        tts = gTTS(text=audio_string, lang='hi', tld='co.in')
    r = random.randint(1, 10000)
    audio_file = 'audio' + str(r) + '.wmv'
    tts.save(audio_file)
    print(audio_string)
    AudioPlayer(audio_file).play(block=True)
    os.remove(audio_file)


def respond(voice_data):
    if voice_data == 'exit':
        exit()
    if voice_data == None or voice_data == '':
        return
    else:
        voice_data = voice_data + "?"
        result = question_answerer(question=voice_data, context=context)
        if (n == 0):
            melon_speak(result['answer'])
        else:
            dd = translator.translate(result['answer'], src='en', dest='hi')
            dd = dd.text
            melon_speak(dd)


if (n == 0):
    melon_speak('How can I help you?')
else:
    melon_speak('मैं आपकी मदद कैसे कर सकता हूँ ')
while 1:
    print("Prompt to speak>>")
    voice_data = record_audio_to_speech()
    if (n == 0):
        print(voice_data)
    if voice_data != '':
        respond(voice_data)
    time.sleep(1)
    flag = 1
