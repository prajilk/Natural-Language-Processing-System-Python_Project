import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyaudio
import subprocess
import time
import os
from googletrans import Translator
from playsound import playsound
import langcodes
from bs4 import BeautifulSoup


#import pyrebase

import webbrowser
from googlesearch import search

import pytesseract

from gtts import gTTS

from pygame import mixer

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


listener = sr.Recognizer()

mixer.init()

language = 'en'

mic_name = "USB2.0 PC CAMERA: Audio (hw:2,0)"

sample_rate = 48000

chunk_size = 2048

mic_list = sr.Microphone.list_microphone_names()
print(mic_list)

##for i, microphone_name in enumerate(mic_list): 
##    if microphone_name == mic_name: 
##        device_id = i


command = ''
flag = 1

import pyttsx3
engine = pyttsx3.init()

def talk(text):

    engine.say(text)
    engine.runAndWait()


def take_command():
    global command,flag
    '''with sr.Microphone(device_index = device_id, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source:'''
    with sr.Microphone() as source:
        print('listening...')
        
        listener.adjust_for_ambient_noise(source)#, duration=0.5)
        voice = listener.listen(source)
        #print('ok')
        
        try:
            
            instruction = listener.recognize_google(voice)
            
            instruction = instruction.lower()
            print('Output: \n')
            print(instruction)

            command = instruction


        except:
            pass
        
    return command


def run_main():
    global command,flag

    time = datetime.datetime.now().strftime('%I:%M %p')

    if(time == '03:33 PM'):
        print('ok')
        pywhatkit.playonyt('music')

    #03:28 PM
    
    command = take_command()
    
    print(command)


    if(command != ''):

        flag = 0
    
    
    kwords = {
        'hi':'hi. its good to hear from you',
        'hai':'hi. its good to hear from you',
        'hello':'hey',
        'good morning':'hello,',
        'good afternoon':'hi! a good afternoon to you, too',
        'good evening':'good evening'
        }
    

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        
    elif 'time' in command or 'date' in command and 'birth' not in command:
        time = datetime.datetime.now().strftime('%y-%m-%d %I:%M %p')
        print(time)
        talk('Current date and time is ' + time)

    elif command in kwords:
        kreply = kwords[command]
        print(kreply)
        talk(kreply)
        
    elif 'who is' in command:
        person = command#.replace('who is', '')
        try:
            info = wikipedia.summary(person, 2)
            print(info)
            talk(info)
        except:
            pass
            
    elif 'what is' in command:
        data = command#.replace('what is', '')
        try:
            result = wikipedia.summary(data, 2)
            print(result)
            talk(result)
        except:
            pass

    elif 'tell' in command and 'joke' in command:
        joke = pyjokes.get_joke(language='en',category='all')
        print(joke)
        talk(joke)

    elif 'translate' in command:
               
        try:
            
            text = command.replace('translate ','')
            
            #identifying language 
            word_list = text.split()
            langname = word_list[-1]


            #find langauge code
            langcd = langcodes.find(langname)

            
            text = text.replace(' to '+langname, '')
            
            #translate the sentence
            translator = Translator()
            tlword = translator.translate(str(text),dest=str(langcd))
            #getting translated audio from google translate
            x = requests.get('https://translate.google.com/translate_tts?ie=UTF-&&client=tw-ob&tl='+str(langcd)+'&q='+str(tlword.text)).content

            #save trasnlated audio
            file = open('music.mp3','wb')
            file.write(x)
            file.close()
                
            print(text+' in '+langname+' is '+str(tlword.text))
            talk(text+' in '+langname+' is ')

            #play translated audio
            playsound('music.mp3')
            #remove audio from storage
            os.remove('music.mp3')
            
    
        except (AttributeError, FileNotFoundError):
            print("Sorry an Error occured")

        except (ValueError, LookupError):
            print('Translation not completed! cannot translate to given language')
            talk('Translation not completed! cannot translate to given language')



    elif 'open' in command or 'go to' in command:

        query = command.replace('open ','')
        query = command.replace('go to ','')

        if 'open' in command:
            appname = command.replace('open ','')
        elif 'go to' in command:
            appname = command.replace('go to ','')

        apps = {
            'paint':'mspaint.exe',
            'notepad':'notepad.exe',
            'calculator':'calc.exe',
            'cmd':'cmd.exe',
            'command prompt':'cmd.exe',
            'word':'C://Program Files//Microsoft Office//root//Office16//WINWORD.EXE',
            'power point':'C://Program Files//Microsoft Office//root//Office16//POWERPNT.EXE"',
            'excel':'C://Program Files//Microsoft Office//root//Office16//EXCEL.EXE'
            }
                
        if appname in apps:
            talk('Opening'+appname.upper())
            appexe = apps[appname]
            subprocess.call(appexe)

        elif appname == 'vlc':
            try:
                try:
                    subprocess.call(r'C:\Program Files\VideoLAN\VLC\vlc.exe')
                except FileNotFoundError:
                    subprocess.call(r'D:\Program Files\VideoLAN\VLC\vlc.exe')
            except FileNotFoundError:
                print('File location of vlc is unknown or vlc is not installed on this system')
                talk('File location of vlc is unknown or vlc is not installed on this system')
                    
        else:
            url_list = []
            for j in search(query, tld="co.in", num=5, stop=5, pause=2):
                url_list.append(j)
                print(j)

            url = url_list[0]

            #webbrowser.register('chrome', None, webbrowser.BackgroundBrowser('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'))
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser('C:/Program Files/Google/Chrome/Application/chrome.exe'))
            talk('Opening'+query)
            webbrowser.get('chrome').open(url)

        
    else:
        URL = "https://www.google.com/search?q=" + command

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            result = soup.find(class_='Z0LcW').get_text()
            print(result)
            talk(result)
        except AttributeError:
            pass

        try:
            result = soup.find(class_='hgKElc').get_text()
            print(result)
            talk(result)
        except AttributeError:
            talk(command)

    command = ''

time = datetime.datetime.now().strftime('%I:%M %p')
print(time)

while True:
    
    run_main()
