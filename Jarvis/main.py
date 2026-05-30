import pyttsx3
import speech_recognition as sr
import pyjokes
import random
import datetime
import webbrowser
import randfacts
import subprocess
import google.generativeai as genai
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#Volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def speak(text):
     print(f"Jarvis : {text}")
     pyttsx3.speak(str(text))

recognizer = sr.Recognizer()
def take_voice_command(active=False):

    with sr.Microphone() as source:

        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)

        try:
            audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)

        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower().strip()

    except sr.UnknownValueError:
        if active:
            speak("Sorry, I could not understand")
        return ""

    except sr.RequestError:
        speak("Network error")
        return ""

    except Exception as e:
        print(e)
        speak("Something went wrong")
        return ""


command = ["hi", "hello", "hey"]
reply = ["yes sir", "what can i help you"]

active = False
user = take_voice_command()

while True:

    # If empty input, listen again
    if user == "":
        user = take_voice_command()
        continue

    # Sleep mode
    if active == False:

        if "jarvis" in user.lower() or "jar" in user.lower():
            speak("Yes,Sir")
            speak("How can i help you")
            active = True

        user = take_voice_command()
        continue

    # EXIT
    if "exit" in user.lower():
        speak("Going to sleep")
        active = False

        user = take_voice_command()
        continue

    # GREETINGS
    elif user.lower() in command:
        speak(random.choice(reply))

    # DATE
    elif "date" in user.lower():
        speak(datetime.date.today())

    # TIME
    elif "time" in user.lower():
        speak(datetime.datetime.now().strftime("%I:%M %p"))

    # DAY
    elif "day" in user.lower():
        speak(datetime.datetime.now().strftime("%A"))

    # JOKE
    elif "joke" in user.lower():
        speak(pyjokes.get_joke())

    # FACT
    elif "fact" in user.lower():
        speak("Did you know that")
        speak(randfacts.get_fact())

    # WEBSITES
    elif "youtube" in user.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "google" in user.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif (
        "chatgpt" in user
        or "chat gpt" in user
        or "chat gbt" in user):
        speak("Opening ChatGPT")
        webbrowser.open("https://chatgpt.com")
    
    elif "github" in user.lower() or "git hub" in user.lower():
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    elif "chrome" in user.lower():
        speak("Opening Chrome")
        subprocess.Popen(r"C:\Users\perfect\AppData\Local\Google\Chrome\Application\chrome.exe")

    elif "vs code" in user.lower() or "visual studio code" in user.lower():
        speak("Opening Visual Studio Code")
        subprocess.Popen(r"C:\Users\perfect\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    
    elif "obs studio" in user.lower() or "open studio" in user.lower():
        speak("Opening OBS Studio")
        subprocess.Popen(r"C:\Program Files\obs-studio\bin\64bit\obs64.exe")
        

    elif "notepad" in user.lower():
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")

    elif "calculator app" in user.lower():
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")
    
    # Open any website
    elif user.startswith("open "):
        site = user.replace("open ", "").strip()

        speak(f"Opening {site}")

        webbrowser.open(f"https://www.{site}.com")

    # System controls
    elif "shutdown" in user.lower():
            speak("Shutting down computer")
            subprocess.call("shutdown /s /t 5")

    elif("sleep" in user.lower()):
        speak("PC is going to sleep")
        subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    # Google search
    elif "search" in user:
        search_query = user.replace("search", "").strip()
        speak(f"Searching {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    
    # Play music/videos on YouTube
    elif "play" in user:
        song = user.replace("play", "").strip()
        speak(f"Playing {song}")

        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    
    # volume setting 
    elif "volume" in user:
        words = user.split()

        for word in words:
            if word.isdigit():
                percent = int(word)

                if 0 <= percent <= 100:
                    volume.SetMasterVolumeLevelScalar(percent / 100, None)
                    speak(f"Volume set to {percent} percent")
                else:
                    speak("Please choose a value between 0 and 100")

                break
    elif "volume up" in user:
        speak("Increasing volume")
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)

    elif "volume down" in user:
        speak("Decreasing volume")
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)

    elif "mute" in user:
        speak("Muting volume")
        volume.SetMute(1, None)

    elif "unmute" in user:
        speak("Unmuting volume")
        volume.SetMute(0, None)

    else:
        speak("I did not understand that command")
    #Listen again
    user = take_voice_command()
        # try:
        #     genai.configure(api_key="AIzaSyCdpzhwwCUIK3weVZZpJlm4XtHFTsFR_Pc")
        #     model = genai.GenerativeModel("gemini-2.0-flash")
        #     response = model.generate_content(user)
        #     speak(response.text)

        # except Exception as e:
        #     print(e)
        #     speak("AI is not working")                              