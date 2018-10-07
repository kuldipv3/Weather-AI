import json
import requests
import speech_recognition as sr
from gtts import gTTS
import os
import sys
import time
import vlc
import pyttsx
phrase = ""
r=sr.Recognizer()
with sr.Microphone() as source:
    print("What do you want?")
    input_mic=r.listen(source)
try:
    phrase = r.recognize_google(input_mic)
except:
    print("Agli baar zor se bolio")

phrase=phrase.split()

if "temperature" in phrase:
    removals = ["temperature","what","is","the","of","tell"]
    for i in removals:
        if i in phrase:
            phrase.remove(i)

    for city_name in phrase:
        url_start="https://api.openweathermap.org/data/2.5/weather?q="
        url_end="&appid=896aae4bcc99d5c210494fdb989319d0"
        url=url_start+city_name+url_end
        try:
            response = requests.get(url)
            details = json.loads(response.text)
            temperature=details["main"]["temp"]-273
            place = details["name"]
        except:
            pass
    callback="the temperature of "+place+" is "+str(temperature)+" degree celsius"
    tts = gTTS(text=callback,lang="en")
    tts.save("temperature_request.mp3")
    os.system("vlc temperature_request.mp3 vlc://quit")

if "time" in phrase:
    removals = ["time","what","is","the","of","tell","ka","kya","me"]
    for i in removals:
        if i in phrase:
            phrase.remove(i)

    for city_name in phrase:
        url_start="https://api.openweathermap.org/data/2.5/weather?q="
        url_end="&appid=896aae4bcc99d5c210494fdb989319d0"
        url=url_start+city_name+url_end
        try:
            response = requests.get(url)
            details = json.loads(response.text)
            lon=details["coord"]["lon"]
            lat=details["coord"]["lat"]
            place=details["name"]
        except:
            pass
    time_url="http://api.timezonedb.com/v2/get-time-zone?key=O4Y6LNUKMH2Y&format=json&by=position&lat="+str(lat)+"&lng="+str(lon)
    time_response=requests.get(time_url)
    time_details = json.loads(time_response.text)
    time = time_details["formatted"]
    t=time.split()
    time=t[-1]
    time=time.split(":")
    time_callback="the local time of "+place+" is "+str(time[0])+" hours "+str(time[1])+" minutes"
    time_tts = gTTS(text=time_callback,lang="en")
    time_tts.save("time_request.mp3")
    os.system("vlc time_request.mp3 vlc://quit")


'''#using pyttsx
    engine=pyttsx.init()
    engine.say(callback)
    engine.runAndWait()'''
