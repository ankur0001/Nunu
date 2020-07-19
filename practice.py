# -*- coding: utf-8 -*-
import wikipedia
import speech_recognition as sr 
import pyttsx3 

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        SpeakText('Say something')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
    engine.say(command)  
    engine.runAndWait()


   
try:
    topic = myCommand()
    ny = wikipedia.page(topic)
    #print(ny.content[:1500].encode('utf-8'))
    #print("===============================================================================")
    print(ny.summary.encode('utf-8'))
    SpeakText(ny.summary[:500].encode('utf-8'))
except Exception as e:
    print(e)
