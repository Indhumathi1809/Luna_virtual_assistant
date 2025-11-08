import ctypes
import pyttsx3
import speech_recognition as sr
import pyautogui
import os
import subprocess

# Initialize text-to-speech engine
# Initialize text-to-speech engine with a female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 usually represents a female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

if __name__ == "__main__":
    speak("Hello! I am your assistant Luna. How can I help you today?")

    while True:
        query = take_command().lower()

        if 'open notepad' in query:
            subprocess.Popen('notepad.exe')
        elif 'open browser' in query:
            subprocess.Popen('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        elif 'shutdown' in query:
            speak("Shutting down the computer.")
            os.system("shutdown /s /t 1")
        elif 'restart' in query:
            speak("Restarting the computer.")
            os.system("shutdown /r /t 1")
        elif 'search' in query:
            query = query.replace("search", "")
            pyautogui.hotkey('win', 's')
            pyautogui.typewrite(query)
            pyautogui.press('enter')
        elif 'lock' in query:
            speak("Locking the computer.")
            ctypes.windll.user32.LockWorkStation()
        elif 'volume up' in query:
            pyautogui.press('volumeup')
        elif 'volume down' in query:
            pyautogui.press('volumedown')
        elif 'mute' in query:
            pyautogui.press('volumemute')
        elif 'bye' in query:
            speak("Goodbye!")
            break
        else:
            speak("I am sorry, I did not understand your command.")