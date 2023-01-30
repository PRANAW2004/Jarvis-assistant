from __future__ import print_function
try:
    import selenium.common.exceptions
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pyttsx3
    import speech_recognition as sr
    import datetime
    import wikipedia
    import webbrowser
    import os
    import json
    import re
    import threading
    import time
    import requests
    import pytz
    import wolframalpha
    import smtplib
    from bs4 import BeautifulSoup
    from googletrans import Translator
    from pytube import YouTube
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import mechanize
    from selenium import webdriver
    try:
        import pickle
        import pywhatkit as kit
    except Exception as e:
        pass

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        #print(voices[1].id)
        engine.setProperty('voice', voices[0].id)
    except RuntimeError as e:
        print("Exception")

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    # try:
    #     import pickle
    #     import pywhatkit as kit
    # except Exception as e:
    #     pass

    def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            speak("Good Morning!")
            speak("I am jarvis")
            speak("Welcome back sir")
        if hour>=12 and hour<18:
            speak("Good Afternoon!")
            speak("I am jarvis")
            speak("Welcome back sir")
        if hour>=18:
            speak("Good Evening")
            speak("I am jarvis")
            speak("Welcome back sir")

    def takeCommand(ask = False):

        r = sr.Recognizer()
        with sr.Microphone() as source:
            if ask:
                print(ask)
            #print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        #try:
            #print("Recognizing...")
            #query = input("Your Query: ")
            #query = input("Your Query: ")#r.recognize_google(audio, language='en')#input("Your Query: ")
            #print(f"You said: , {query}\n")

        #except Exception as e:
            #print(e)
            #print("Say that again please...")
            #return "None"
        #return query


    timeZ_Kl = pytz.timezone('Asia/Kolkata')
    timeZ_Ny = pytz.timezone('America/New_York')
    timeZ_Ma = pytz.timezone('Africa/Maseru')
    timeZ_Ce = pytz.timezone('US/Central')
    timeZ_At = pytz.timezone('Europe/Athens')

    END_PHRASE = "exit"

    client = wolframalpha.Client('R3LGY6-4G22PPVU86')
    wishMe()
    def main():
        if __name__ == "__main__":
            #wishMe()
            while True:
                try:
                    query = input("Your Query: ").lower()#takeCommand().lower()

                    if 'wikipedia' in query:
                            try:
                                speak('Searching wikipedia...Please Wait')
                                query = query.replace("wikipedia", "")
                                results = wikipedia.summary(query, sentences=3)
                                speak("According to Wikipedia")
                                print(results)
                                speak(results)
                            except Exception:
                                print("Exception")
                                print("sorry I dont know the answer for that, check your word and try again")
                                speak("sorry I dont know the answer for that, check your word and try again")

                    elif 'play' in query:
                        kit.playonyt(f"{query}")
                        pass

                    elif 'what is your name' in query:
                        print("My name is Jarvis. My name is kept by the inspiration of jarvis from the iron man movie.")
                        speak("My name is Jarvis. My name is kept by the inspiration of jarvis from the iron man movie.")

                    elif 'where' in query:
                            url = f"https://www.google.com/search?q=which+state+is+'{query}'&oq=which+state+is+'+{query}+'&aqs=chrome.0.69i59j69i57j69i59.3674j0j1&sourceid=chrome&ie=UTF-8"
                            url1 = f"https://www.google.com/search?q=what+is+the+latitude+and+longitude+of+'{query}'&oq=what+is+the+latitude+and+longitude+of+'{query}'&aqs=chrome..69i57.15052j0j1&sourceid=chrome&ie=UTF-8"
                            req = requests.get(url)
                            req1 = requests.get(url1)
                            sor = BeautifulSoup(req.text, "html.parser")
                            sor1 = BeautifulSoup(req1.text, "html.parser")
                            location = sor.find("div", class_ = "BNeawe").text
                            location1 = sor1.find("div", class_ = "BNeawe").text
                            print(location)
                            print(location1)
                            speak(f"It is in {location} at an latitude and longitude of {location1}")

                    elif 'which' in query:
                            url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.7232j0j1&sourceid=chrome&ie=UTF-8"
                            req = requests.get(url)
                            sor = BeautifulSoup(req.text, "html.parser")
                            statement = sor.find("div", class_="BNeawe").text
                            print(statement)
                            speak(statement)

                    elif 'temperature' in query:
                            speak("wait a minute while I fetch data")
                            url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome.1.69i57j69i59l2.5184j0j1&sourceid=chrome&ie=UTF-8"
                            req = requests.get(url)
                            sor = BeautifulSoup(req.text, "html.parser")
                            temperature = sor.find("div", class_="BNeawe").text
                            print(temperature)
                            speak(f"The temperature is {temperature}")

                    elif 'what do i have' in query:
                            creds = None

                            if os.path.exists('token.pickle'):
                                with open('token.pickle', 'rb') as token:
                                    creds = pickle.load(token)

                            if not creds or not creds.valid:
                                if creds and creds.expired and creds.refresh_token:
                                    creds.refresh(Request())
                                else:
                                    flow = InstalledAppFlow.from_client_secrets_file(
                                        'credentials.json', SCOPES)
                                    creds = flow.run_local_server(port=0)

                                with open('token.pickle', 'wb') as token:
                                    pickle.dump(creds, token)

                            service = build('calendar', 'v3', credentials=creds)

                            now = datetime.datetime.utcnow().isoformat() + 'Z'
                            print('Getting your today events')
                            speak('Getting your today events')
                            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                                  maxResults=10, singleEvents=True,
                                                                  orderBy='startTime').execute()
                            events = events_result.get('items', [])

                            if not events:
                                print('No upcoming events found.')
                                speak('No upcoming events found.')
                            for event in events:
                                start = event['start'].get('dateTime', event['start'].get('date'))
                                print(start, event['summary'])

                            speak("These are your events for today")

                    elif 'when' in query:
                            url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.8348j0j1&sourceid=chrome&ie=UTF-8"
                            req = requests.get(url)
                            sor = BeautifulSoup(req.text, "html.parser")
                            statement = sor.find("div", class_="BNeawe").text
                            print(statement)
                            speak(statement)

                    elif 'latest news in india' in query:
                            main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=a0401349f43f47fb8daedfbd0a04dc24"
                            open_news_page = requests.get(main_url).json()
                            article = open_news_page["articles"]
                            results = []

                            for ar in article:
                                results.append((ar["title"]))
                            for i in range(len(results)):
                                print(i + 1, results[i])
                            speak(results)

                    elif 'latest news' in query:
                            main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=a0401349f43f47fb8daedfbd0a04dc24"
                            open_bbc_page = requests.get(main_url).json()
                            article = open_bbc_page["articles"]
                            results = []

                            for ar in article:
                                results.append((ar["title"]))
                            for i in range(len(results)):
                                print(i + 1, results[i])
                            speak(results)


                    elif 'weather' in query:
                            try:
                                speak("wait a minute, while I fetch data")
                                query = query.replace("wolframalpha", "")
                                res = client.query(query)
                                output = next(res.results).text
                                print(output)
                                speak(output)
                            except StopIteration or KeyError or AttributeError or ValueError as e:
                                try:
                                    a = f"{query}"
                                    a1 = a[7:]
                                    query = query.replace("wolframalpha","")
                                    res1 = client.query(a1)
                                    output = next(res1.results).text
                                    print(output)
                                    speak(output)
                                except StopIteration or KeyError or AttributeError or ValueError as e:
                                    print("Sorry sir we did'nt get you please tell again")
                                    speak("Sorry sir we did'nt get you please tell again")

                    elif 'date and time in india' in query:
                        current_datetime = datetime.datetime.now(timeZ_Kl)
                        print(current_datetime)
                        speak(f"The current date in india is {current_datetime}")

                    elif 'date and time in america' in query:
                        current_datetime = datetime.datetime.now(timeZ_Ny)
                        print(current_datetime)
                        speak(f"Today date is {current_datetime}")

                    elif 'date and time in africa' in query:
                        current_datetime = datetime.datetime.now(timeZ_Ma)
                        print(current_datetime)
                        speak(f"Sir the time is {current_datetime}")

                    elif 'date and time in us central' in query:
                        current_datetime = datetime.datetime.now(timeZ_Ce)
                        print(current_datetime)
                        speak(f"Sir the time is {current_datetime}")

                    elif 'date and time in europe' in query:
                        current_datetime = datetime.datetime.now(timeZ_At)
                        print(current_datetime)
                        speak(f"Sir the time is {current_datetime}")

                    elif 'date in india' in query:
                        current_date = datetime.datetime.now(timeZ_Kl).date()
                        print(current_date)
                        speak(f"The current date in india is {current_date}")

                    elif 'date in america' in query:
                        current_date = datetime.datetime.now(timeZ_Ny).date()
                        print(current_date)
                        speak(f"The current date in america us {current_date}")

                    elif 'date in europe' in query:
                        current_date = datetime.datetime.now(timeZ_At).date()
                        print(current_date)
                        speak(f"The current date in europe is {current_date}")

                    elif 'date in africa' in query:
                        current_date = datetime.datetime.now(timeZ_Ma).date()
                        print(current_date)
                        speak(f"The current date in africa is {current_date}")

                    elif 'date in us central' in query:
                        current_date = datetime.datetime.now(timeZ_Ce).date()
                        print(current_date)
                        speak(f"The current date in us central is {current_date}")

                    elif 'time in india' in query:
                        current_time = datetime.datetime.now(timeZ_Kl).time()
                        print(current_time)
                        speak(f"The current time in india is {current_time}")

                    elif 'time in america' in query:
                        current_time = datetime.datetime.now(timeZ_Ny).time()
                        print(current_time)
                        speak(f"The current time in america is {current_time}")

                    elif 'the time in africa' in query:
                        current_time = datetime.datetime.now(timeZ_Ma).time()
                        print(current_time)
                        speak(f"The current time in africa is {current_time}")

                    elif 'the time in europe' in query:
                        current_time = datetime.datetime.now(timeZ_At).time()
                        print(current_time)
                        speak(f"The current time in eurpe is {current_time}")

                    elif 'the time in us central' in query:
                        current_time = datetime.datetime.now(timeZ_Ce).time()
                        print(current_time)
                        speak((f"The current time in us central is {current_time}"))

                    elif 'what' in query:
                        url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.8348j0j1&sourceid=chrome&ie=UTF-8"
                        req = requests.get(url)
                        sor = BeautifulSoup(req.text, "html.parser")
                        statement = sor.find("div", class_="BNeawe").text
                        print(statement)
                        speak(statement)

                    elif 'answer for' in query:
                        try:
                            query = query.replace("wolframalpha", "")
                            res = client.query(query)
                            output = next(res.results).text
                            print(output)
                            speak(output)
                        except StopIteration or KeyError or AttributeError:
                            try:
                                print("Exception")
                                print("Sorry Sir, I dont know the answer for that")
                                speak("Sorry Sir, I dont know the answer for that")
                                speak("try typing the query")
                                query = str(input("Your question = "))
                                query = query.replace("wolframalpha", "")
                                res = client.query(query)
                                output = next(res.results).text
                                print(output)
                                speak(output)
                            except StopIteration or KeyError or AttributeError:
                                print("Exception")
                                print("Sorry sir, I dont know the answer for that, I will search google for the answer")
                                speak("Sorry sir, I dont know the answer for that, I will search google for the answer")
                                url = 'https://google.com/search?q=' + query
                                webbrowser.get().open(url)
                                print('Here is what I found for ' + query)
                                speak("here is what I found for " + query)

                    elif 'is there rain' in query:
                        try:
                            query = query.replace("wolframalpha", "")
                            res = client.query(query)
                            speak(f"wait a minute, I will see wether rain {query}")
                            output = next(res.results).text
                            print(output)
                            speak(output)
                        except StopIteration or KeyError or AttributeError:
                            try:
                                a = f"{query}"
                                a1 = a[7:]
                                query = query.replace("wolframalpha","")
                                res1 = client.query(a1)
                                output = next(res1.results).text
                                print(output)
                                speak(output)
                            except StopIteration or KeyError or AttributeError:
                                print("Sorry sir we were not able to find whether rain is there or not")
                                speak("Sorry sir we were not able to find whether rain is there or not")

                    elif 'who is the' in query:
                        url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.8348j0j1&sourceid=chrome&ie=UTF-8"
                        req = requests.get(url)
                        sor = BeautifulSoup(req.text, "html.parser")
                        statement = sor.find("div", class_="BNeawe").text
                        print(statement)
                        speak(statement)

                    elif 'who is pranav' in query:
                        print("He is the founder and ceo of grampro company and founder of me, I think he is my daddy")
                        speak("He is the founder and ceo of grampro company and founder of me, I think he is my daddy")

                    elif 'translate' in query:
                        try:
                            speak("Tell the source language")
                            content1 = takeCommand("Tell the language to translate")
                            speak("Tell the destined language or type the destined language")
                            content2 = str(input("Enter the destined language: "))
                            content21 = takeCommand("Tell the destined language")
                            speak("Tell the word to translate")
                            content = takeCommand("Tell the word to translate")
                            translator = Translator()
                            translated_sentence = translator.translate(content,src=content1,dest=(content2 or content21))
                            result = translated_sentence.text
                            print(result)
                            speak(f"Here is what I translated for {content} in {content2 or content21}")
                        except Exception as e:
                            print("Sorry sir, an unknown error occured")
                            speak("Sorry sir, an unknown error occured")

                    elif 'hi' in query:
                        print("Hi sir. How are you?")
                        speak("Hi sir. How are you?")

                    elif 'how are you' in query:
                        print("I am fine sir. How may I help you?")
                        speak("I am fine sir. How may I help you?")

                    elif 'how' in query:
                        url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.8348j0j1&sourceid=chrome&ie=UTF-8"
                        req = requests.get(url)
                        sor = BeautifulSoup(req.text, "html.parser")
                        statement = sor.find("div", class_="BNeawe").text
                        print(statement)
                        speak(statement)

                    elif 'f***' in query:
                        print("Fuck you 2")
                        speak("Fuck you 2")

                    elif 'automate chrome' in query:
                        try:
                            driver = webdriver.Chrome()
                        except selenium.common.exceptions.SessionNotCreatedException as e:
                            print("sorry sir ur browser is up to date but webdriver is in lower version, kindly use up to date version webdriver of ur browser")
                            speak("sorry sir ur browser is up to date but webdriver is in lower version, kindly use up to date version webdriver of ur browser")


                    elif 'what is your name' in query:
                        print("My name is Jarvis")
                        speak("My name is Jarvis")

                    elif 'how are you jarvis' in query:
                        print("I am fine sir. thanks for asking")
                        speak("I am fine sir, thanks for asking")

                    elif 'who are you' in query:
                        print("My name is Jarvis, An Artificial Intelligent programme , I am here to help you")
                        speak("My name is Jarvis, An Artificial Intelligent programme , I am here to help you")

                    elif 'how are you' in query:
                        print("I am fine Sir, Thanks for asking")
                        speak("I am fine Sir, Thanks for asking")

                    elif 'who is your father' in query:
                        print("Sorry, I dont have father, I am AI A computer based programme, I am created by Mr.pranaw")
                        speak("Sorry, I dont have father, I am AI A computer based programme, I am created by Mr.pranaw")

                    elif 'hello' in query:
                        print("Hello sir how may I help you")
                        speak("Hello sir how may I help you")

                    elif 'who founded you' in query:
                        print("I was founded my Mr.Pranaw, I think he is my GOD")
                        speak("I was founded my Mr.Pranaw, I think he is my GOD")

                    elif 'who is your mother' in query:
                        print("I am created but not born, I dont have any family or feelings")
                        speak("I am created but not born, I dont have any family or feelings")

                    elif 'who is your sister' in query:
                        print("AS I told I dont have have family but I have communication AI relanship, My sisters are google, cortana, alexis, and I have more sisters in future")
                        speak("AS I told I dont have have family but I have communication AI relanship, My sisters are google, cortana, alexis, and I have more sisters in future")

                    elif 'can you help me' in query:
                        print("yes sir, of course, I am here only to help and guide you sir and make your work easy")
                        speak("yes sir, of course, I am here only to help and guide you sir and make your work easy")

                    elif 'i love you' in query:
                        print("I Love you too sir")
                        speak("I Love you too sir")

                    elif 'who is' in query:
                        url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.4931j0j1&sourceid=chrome&ie=UTF-8"
                        req = requests.get(url)
                        sor = BeautifulSoup(req.text, "html.parser")
                        statement = sor.find("div", class_="BNeawe").text
                        print(statement)
                        speak(statement)

                    elif 'who' in query:
                        url = f"https://www.google.com/search?q='+{query}+'&oq='+{query}+'&aqs=chrome..69i57.4931j0j1&sourceid=chrome&ie=UTF-8"
                        req = requests.get(url)
                        sor = BeautifulSoup(req.text, "html.parser")
                        statement = sor.find("div", class_="BNeawe").text
                        print(statement)
                        speak(statement)

                    elif 'open youtube' in query:
                        speak("opening youtbe for you sir" )
                        url = 'https://www.youtube.com/'
                        webbrowser.get().open(url)

                    elif 'open google' in query:
                        speak("opening goole for you sir")
                        url = 'https://www.google.com/'
                        webbrowser.get().open(url)

                    elif 'open facebook' in query:
                        speak("opening facebook for you sir")
                        url = "https://www.facebook.com/"
                        webbrowser.get().open(url)

                    elif 'open instagram' in query:
                        speak("sir opening instagram")
                        url = "https://www.instagram.com/"
                        webbrowser.get().open(url)

                    elif 'open doubtnet' in query:
                        speak("opening doubtnet for you sir")
                        url = "https://doubtnut.com/"
                        webbrowser.get().open(url)

                    elif 'open teachoo' in query:
                        speak("opening teachoo.com for you sir")
                        url = "https://www.teachoo.com/"
                        webbrowser.get().open(url)

                    elif 'play music' in query:
                        music_dir = 'C:\\Users\\TOSHIBA\\Music\\songs'
                        songs = os.listdir(music_dir)
                        speak('playing music for you sir')
                        print(songs)
                        os.startfile(os.path.join(music_dir, songs[0]))

                    elif 'play videos' in query:
                            videos_dir = 'C:\\Users\\TOSHIBA\\Videos\\videos'
                            videos = os.listdir(videos_dir)
                            speak('playing videos for you sir')
                            print(videos)
                            os.startfile(os.path.join(videos_dir, videos[0]))

                    elif 'shutdown' in query:
                        speak("shutting down the computer in 10 seconds")
                        os.system('shutdown /s /t 10')

                    elif 'restart' in query:
                        os.system('shutdown /r /t 10')

                    elif 'search youtube' in query:
                        speak("what do you want me to search in youtube ?")
                        search = takeCommand("what do you want me to search in youtube ?")
                        url = 'https://www.youtube.com/results?search_query=' + search
                        webbrowser.get().open(url)
                        print('Here is what I found for' + search)
                        speak('Here is what I found for' + search)

                    elif 'search' in query:
                        speak("what do you want to search for ? ")
                        search = takeCommand("what do you want to search for ?")
                        url = 'https://google.com/search?q=' + search
                        webbrowser.get().open(url)
                        print('Here is what I found for ' + search)
                        speak("here is what I found for " + search)

                    elif 'find location' in query:
                        speak("what is the location you want to find ?")
                        location = takeCommand("what is the location ?")
                        url = 'https://www.google.com/maps/search/'+ location +'/@13.2248681,80.1048075,12z/data=!3m1!4b1'
                        webbrowser.get().open(url)
                        print("Here is the location of " + location)
                        speak("Here is the location of " + location)

                    elif 'open code' in query:
                        try:
                            speak("opening code for you sir")
                            codepath = "C:\\Users\\SMALL TO BIG\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Code.exe"
                            os.startfile(codepath)
                        except FileNotFoundError:
                            print("File is not found, so not able to open the file")
                            speak("File is not found, so not able to open the file")

                    elif 'guna deep' in query:
                        speak("guna deep is a frined of you sir")

                    elif 'open brave' in query:
                        speak("opening brave for you sir")
                        codepath = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                        os.startfile(codepath)

                    elif 'open zoom' in query:
                        speak("opening zoom for you sir")
                        codepath = "C:\\Users\\SMALL TO BIG\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
                        os.startfile(codepath)

                    elif 'open chrome' in query:
                        speak("opening chrome for you sir")
                        codepath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                        os.startfile(codepath)

                    elif 'open firefox' in query:
                        speak("opening firefox for you sir")
                        codepath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                        os.startfile(codepath)

                    elif 'open opera' in query:
                        speak("opening opera for you sir")
                        codepath = "C:\\Users\\SMALL TO BIG\\AppData\\Local\\Programs\\Opera\\launcher.exe"
                        os.startfile(codepath)

                    elif 'open file explorer'in query:
                        speak("opening explorer for you sir")
                        os.system('explorer')

                    elif 'open' in query:
                        try:
                            a = f"{query}"
                            a1 = a[5:]
                            dir = f"C:\\Users\\TOSHIBA\\{a1}"
                            print(f"opening {a1}")
                            speak(f"opening {a1}")
                            os.startfile(dir)
                        except FileNotFoundError:
                            try:
                                dir1 = f"C:\\Users\\TOSHIBA\\Videos\\{a1}"
                                os.startfile(dir1)
                            except FileNotFoundError:
                                try:
                                    dir2 = f"C:\\Users\\TOSHIBA\\Pictures\\{a1}"
                                    os.startfile(dir2)
                                except FileNotFoundError:
                                    try:
                                        dir3 = f"C:\\Users\\TOSHIBA\\Music\\{a1}"
                                        os.startfile(dir3)
                                    except FileNotFoundError:
                                        try:
                                            dir4 = f"C:\\Users\\TOSHIBA\\Downloads\\{a1}"
                                            os.startfile(dir4)
                                        except FileNotFoundError:
                                            try:
                                                dir5 = f"C:\\Users\\TOSHIBA\\Documents\\{a1}"
                                                os.startfile(dir5)
                                            except FileNotFoundError:
                                                pass

                        try:
                            dir6 = f"C:\\{a1}"
                            os.startfile(dir6)
                        except FileNotFoundError:
                            try:
                                dir7 = f"C:\\Program Files\\{a1}"
                                os.startfile(dir7)
                            except FileNotFoundError:
                                try:
                                    dir8 = f"C:\\Program Files (x86)\\{a1}"
                                    os.startfile(dir8)
                                except FileNotFoundError:
                                    try:
                                        dir9 = f"C:\\Users\\TOSHIBA\\{a1}"
                                        os.startfile(dir9)
                                    except FileNotFoundError:
                                        try:
                                            dir10 = f"C:\\Users\\TOSHIBA\\AppData{a1}"
                                            os.startfile(dir10)
                                        except FileNotFoundError:
                                            try:
                                                dir11 = f"C:\\Users\\TOSHIBA\\AppData\\Local\\{a1}"
                                                os.startfile(dir11)
                                            except FileNotFoundError:
                                                print("Sorry sir, File not found")
                                                speak("Sorry sir, File not found")

                        #Continue From here_______________________________________________________________




                    elif 'download youtube video' in query:
                        speak("Enter the link of the youtube video: ")
                        link = input("Enter link of youtube video: ")
                        yt = YouTube(link)
                        videos = yt.streams.all()

                        i = 1
                        for stream in videos:
                            print(str(i) +""+str(stream))
                            i += 1

                        print("These are the quality of this video, selact any number")
                        speak("These are the quality of this video, selact any number")

                        stream_number = int(input("enter number: "))

                        video = videos[stream_number]

                        video.download("C:\\Users\\TOSHIBA\\Videos\\videos")
                        print("video downloaded")
                        speak("video downloaded")

                    elif 'send email' in query:
                        try:
                            speak("To whom I should send the email")
                            content = str(input("Enter the reciever email: "))
                            toaddr = content
                            me = 'pranawrk1@gmail.com'
                            speak("Type the subject down")
                            subject = str(input("Enter the Subject here: "))

                            msg = MIMEMultipart()
                            msg['Subject'] = subject
                            msg['From'] = me
                            msg['To'] = toaddr
                            msg.preamble = "test "

                            speak("what should I say or type the message down")
                            content1 = str(input("TYPE THE MESSAGE HERE: "))
                            content2 = takeCommand("what should I say or type the message down")

                            s = smtplib.SMTP('smtp.gmail.com', 587)
                            s.ehlo()
                            s.starttls()
                            s.ehlo()
                            s.login(user = 'pranawrk1@gmail.com', password = 'dfgtyu567')
                            s.sendmail(me, toaddr, content1 or content2, msg.as_string())
                            s.quit()
                            print("EMAIL SENT")
                            speak("EMAIL SENT")
                        except FileNotFoundError or smtplib.SMTPAuthenticationError:
                            print("Exception")
                            print("sorry sir there is some problem please try later")


                    elif 'thank you jarvis' in query:
                        print("Its ok sir, thats my pleasure")
                        speak("Its ok sir, thats my pleasure")

                    elif query.find(END_PHRASE) != -1:
                        speak("Good Bye sir have a good day")
                        print("Exit")
                        break
                    else:
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=3)
                        print(results)
                        speak(results)

                except KeyboardInterrupt:
                    pass
                    # print("Dont touch the keyboard Boss, It may Interrupt our speech recognition")
                    # speak("Dont touch the keyboard Boss, It may Interrupt our speech recognition")
                except Exception:
                    print("Some error occured so please try again later")
                    speak("Some error occured so please try again later")
    main()
except Exception as e:
    print(e)
    print("An unknown error occured")
    speak("An unknown error occured")
    main()



