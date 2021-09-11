import warnings
import pyttsx3 as p
import speech_recognition as sr
from selenium import webdriver
import datetime
from gtts import gTTS
import wikipedia
import randfacts
import pyjokes
import random
import playsound
import os
import webbrowser
import time
from time import sleep
import passwrd


warnings.filterwarnings("ignore")

engine = p.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 110)
engine.setProperty("volume", 3)
# print(voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def talk():
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        recog.energy_threshold = 10000
        recog.adjust_for_ambient_noise(source, 1)
        print("Listening.........")
        init_time = time.time()
        audio = recog.listen(source)
        text = " "
        try:
            text = recog.recognize_google(audio)
            fin_time = time.time()
        except sr.UnknownValueError as e:
            print("I can't understand that ")
        except sr.RequestError as er:
            print("say that again" + er)
    return text


def wake_call(text):
    wake_up = "assistance"

    text = text.lower().split()
    if wake_up in text:
        return True

    return False


def greeting(text):
    greet = ["hi", "hello", "wassup", "hey", "yo", "what's up", "what's good"]
    resp = ["hi", "hello", "wassup", "hey", "yo", "what's up", "what's good"]

    text1 = text.lower().split()
    for word in text1:
        if word in greet:
            return random.choice(resp)
    return " "


def daily_greeting():
    hour = datetime.datetime.now().hour
    if 12 < hour < 15:
        return "afternoon"
    elif 0 <= hour < 12:
        return "morning"
    else:
        return "evening"


def gtt_talk(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        audio = "audio.mp3"
        tts.save(audio)
        playsound.playsound("audio.mp3")
        os.remove(audio)
    except gTTS.gTTSError as e:
        print("gtts error" + " " + e)


def wiki_search(text):
    text = text.lower().split()
    print("search query called")
    if "who" in text and text[(text.index("who")+1)] == "is":
        index_is = text.index("is")
        if index_is + 2 <= len(text) - 1:
            print(text[index_is + 1] + " " + text[index_is + 2])
            return text[index_is + 1] + " " + text[index_is + 2]


def today():
    now = datetime.datetime.now()
    date_today = now.strftime("%A, %B %d, %Y")
    time_now = now.strftime("%I:%M %p")
    print(date_today, time_now)
    return [date_today, time_now]


def check_balance():
    speak("Checking your Ecash wallet")
    driver = webdriver.Chrome(r"C:\Users\DELL\Downloads\chromedriver.exe")

    driver.maximize_window()
    url = "https://www.quickteller.com/dashboard"

    try:
        speak("Opening quickteller website")
        driver.get(url)
        sleep(2)
    except:
        print("Check your connection")

    speak("Opening Login page")
    driver.find_element_by_xpath(r'//*[@id="account"]/section/section/button[1]').click()
    sleep(2)

    email = "asimi.ojewola@gmail.com"
    passwd = passwrd.passwd()
    driver.find_element_by_xpath('//*[@id="accountLoginFormUsername"]').send_keys(email)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="accountLoginFormPassword"]').send_keys(passwd)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="accountLoginFormButton"]/span[1]').click()
    speak("Logged in")
    sleep(4)
    balance = driver.find_element_by_xpath('//*[@id="dashboardContainer"]/section[2]/section[1]/section/section[1]/section/section[1]/section[1]/section/section[1]/span[1]/span')
    bal = balance.text
    print(bal, "balance")
    naira, kobo = str(bal).split(".")
    # speak(str(bal))
    speak(f"Your account balance is, {naira}, Naira and, {kobo}, kobo")


def run_assist():
    words = talk().lower()
    print(words)

    if wake_call(words):
        speak(greeting(words) + " " + "good" + daily_greeting())

        while True:
            words = talk().lower()
            print(words)
            try:
                if "who are you" in words:
                    output = "I am Assistance!, am here to assist you on any information you need on " \
                                    "your Ecash wallet"
                    gtt_talk(output)

                elif "how are you" in words:
                    speak("I am fine, thank you")
                    speak("how are you too?")
                    response = talk().lower()

                    if "fine" in response or "good" in response:
                        speak("It is good to know that you are fine")

                elif "what is your name" in words:
                    speak("My name is Assistance")

                elif "who am i" in words:
                    speak("You must probably be a human")

                elif "what" in words and "date" in words:
                    today = today()[0]
                    speak(str(today))

                elif "what" in words and "time" in words:
                    time = today()[1]
                    speak(str(time))

                elif "wikipedia" in words:
                    print("wiki..............")
                    search_word = wiki_search(words)
                    print(search_word)
                    wiki = wikipedia.summary(search_word, sentences=2)
                    print(wiki, "none")
                    speak(wiki)
                    break

                elif "jokes" in words or "joke" in words:
                    joke = pyjokes.get_joke()
                    gtt_talk(joke)
                    break

                elif "fact" in words or "facts" in words:
                    fact = randfacts.getFact()
                    gtt_talk(fact)
                    break

                elif "open" in words:
                    if "quickteller" in words:
                        speak("Opening Quicteller")
                        url = "https://www.quickteller.com/"
                        webbrowser.open(url)

                    elif "chrome" in words:
                        speak("Opening google chrome")
                        os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
                        break
                    elif "youtube" in words:
                        word_arr = words.split()
                        you_index = word_arr.index("youtube")
                        if word_arr[you_index + 1] == "and":
                            search = word_arr[you_index + 4:]
                            query = " ".join(search)
                            print(query)
                            speak(f"Searching for {query} on youtube")
                            url = f"https://www.youtube.com/results?search_query={query}"
                            webbrowser.open(url)
                            break

                    else:
                        speak("Application is not available")

                elif "play video" in words:
                    video = r"C:\Users\DELL\Downloads\Videos"
                    video_dir = os.listdir(video)
                    vid = random.choice(video_dir)
                    video_path = os.path.join(video, vid)
                    playsound.playsound(video_path)

                elif "check my account balance" in words or "my ecash balance" in words or "account balance" in words:
                    check_balance()
                    break

                elif "exit" in words or "quit" in words or "stop" in words:
                    print("program")
                    exit()

            except:
                speak("I can't understand that")


while True:
    run_assist()