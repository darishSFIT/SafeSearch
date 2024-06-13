from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from search.models import Profile
import requests
from bs4 import BeautifulSoup as bs
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import random
import smtplib
import time
import threading
import multiprocessing

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', rate-50)

def run_voice_assistant():
    # your voice assistant code here

    if __name__ == '__main__':
        p = multiprocessing.Process(target=run_voice_assistant)
        p.start()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! This is OK Google")
    elif hour>=12 and hour<18:
        speak("Good Afternoon! ")   
    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you") 
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User said: {query}\n")
        print(query)
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'search' in query:
            webbrowser.open(f"www.google.com/search?q= {query}")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("https://www.stackoverflow.com")

        elif 'open college website' in query:
            webbrowser.open("https://www.sfit.ac.in/")    

        elif 'play music' in query:
            music_dir = 'C:\\Users\\shawn dsilva\\Music\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir,the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'send email to shawn' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "shawndsilva2003@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")    

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('shawntrial98@gmail.com', 'shawn2003')
    server.sendmail('shawntrial98@gmail.com', to, content)
    server.close()

# Create your views here.
def index(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception as e:
        profile = None
        print('Exception : ', e)

    context = {
        'profile': profile,
    }

    return render(request, 'index.html')

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render (request,'login_page.html')

def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup_page.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def random_redirect(request):
    if request.method=='POST':
        websites = ["https://www.google.com", 
                    "https://www.wikipedia.org", 
                    "https://www.github.com",
                    "https://www.youtube.com/",
                    "https://open.spotify.com/",
                    "https://mrdoob.com/#/150/beach_balls",
                    "https://mrdoob.com/#/147/google_space",
                    "https://www.speedtest.net/run",
                    "https://mrdoob.com/#/142/winning_solitaire",
                    "https://mrdoob.com/#/137/voxels_liquid",
                    "https://mrdoob.com/#/129/voxels",
                    "https://mrdoob.com/#/117/fire",
                    "https://mrdoob.com/#/112/branching",
                    "https://mrdoob.com/#/92/google_gravity",
                    "https://mrdoob.com/#/91/ball_pool",
                    ]
        random_website = random.choice(websites)
    return redirect(random_website)

def right(request):
    return render(request, 'rightside.png')

def google_logo(request):
    return render(request, 'google_logo.png')


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        API_KEY = "AIzaSyCMOIOCw_LHYJyj6R69siO3siaJiSssqcE"
        SEARCH_ENGINE_ID = "95da3749e074d4cff"
        # search = "python"
        page = 1
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search}&start={start}"
        data = requests.get(url).json()
        search_items = data.get("items")
        final_result = []
        for i, search_item in enumerate(search_items, start=1):
            try:
                long_description = search_item["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"
            result_title = search_item.get("title")
            snippet = search_item.get("snippet")
            html_snippet = search_item.get("htmlSnippet")
            result_url = search_item.get("link")
            print("="*10, f"Result #{i+start-1}", "="*10)
            print("Title:", result_title)
            print("Description:", snippet)
            print("Long description:", long_description)
            print("URL:", result_url, "\n")
            final_result.append((result_title, result_url, snippet))
        context = {
            'final_result': final_result
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

def voice(response):
    if response.method=='POST':
        takeCommand()
        #return render(response, 'index.html')
        return redirect('/')
    else:
        return HttpResponse(voice)
    
def filesearch(response):
    if response.method=='POST':

        import PySimpleGUI as sg
        import os
        global results
        def search(values, window):
            """Perform a search based on term and type"""
            
            # reset the results list
            results.clear()
            window['-RESULTS-'].update(values=results)
            window['-INFO-'].update(value='Searching for matches...')
            
            # search for term and save new results
            for root, _, files in os.walk(values['-PATH-']):
                for file in files:
                    if values['-ENDSWITH-'] and file.lower().endswith(values['-TERM-'].lower()):
                        results.append(f'{root}\\{file}'.replace('\\', '/'))
                        window['-RESULTS-'].update(results)
                    if values['-STARTSWITH-'] and file.lower().startswith(values['-TERM-'].lower()):
                        results.append(f'{root}\\{file}'.replace('\\', '/'))
                        window['-RESULTS-'].update(results)
                    if values['-CONTAINS-'] and values['-TERM-'].lower() in file.lower():
                        results.append(f'{root}\\{file}'.replace('\\', '/'))
                        window['-RESULTS-'].update(results)
            window['-INFO-'].update('Enter a search term and press `Search`')
            sg.PopupOK('Finished!')

        def open_file(file_name):
            """Attempt to open the file with the default program"""
            # probably should add error handling here for when a default program cannot be found.
            os.system(file_name)

        # create the main file search window
        results = []
        sg.change_look_and_feel('Black')
        layout = [
            [sg.Text('Search Term', size=(11, 1)), sg.Input('', size=(40, 1), key='-TERM-'), 
            sg.Radio('Contains', group_id='search_type', size=(10, 1), default=True, key='-CONTAINS-'),
            sg.Radio('StartsWith', group_id='search_type', size=(10, 1), key='-STARTSWITH-'),
            sg.Radio('EndsWith', group_id='search_type', size=(10, 1), key='-ENDSWITH-')],
            [sg.Text('Search Path', size=(11, 1)), sg.Input('/..', size=(40, 1), key='-PATH-'),
            sg.FolderBrowse(size=(10, 1), key='-BROWSE-'), 
            sg.Button('Search', size=(10, 1), key='-SEARCH-')],
            [sg.Text('Enter a search term and press `Search`', key='-INFO-')],
            [sg.Listbox(values=results, size=(100, 28), enable_events=True, key='-RESULTS-')]]

        window = sg.Window('File Search Engine', layout=layout, finalize=True, return_keyboard_events=True)
        window['-RESULTS-'].expand(expand_x=True, expand_y=True)

        # main event loop
        while True:
            event, values = window.read()
            if event is None:
                break
            if event == '-SEARCH-':
                search(values, window)
            if event == '-RESULTS-':
                file_name = values['-RESULTS-']
                if file_name:
                    open_file(file_name[0])

        #return render(response, 'index.html')
        return redirect('/')
    else:
        return HttpResponse(filesearch)




"""
<script async src="https://cse.google.com/cse.js?cx=95da3749e074d4cff">
</script>
<div class="gcse-search"></div>

<script async src="https://cse.google.com/cse.js?cx=25fc77fe79fb24664">
</script>
<div class="gcse-search"></div>
"""

"""
API_KEY = "AIzaSyCMOIOCw_LHYJyj6R69siO3siaJiSssqcE"
SEARCH_ENGINE_ID = "95da3749e074d4cff"
search = "python"
page = 1
start = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
data = requests.get(url).json()

search_items = data.get("items")
for i, search_item in enumerate(search_items, start=1):
    try:
        long_description = search_item["pagemap"]["metatags"][0]["og:description"]
    except KeyError:
        long_description = "N/A"
    title = search_item.get("title")
    snippet = search_item.get("snippet")
    html_snippet = search_item.get("htmlSnippet")
    link = search_item.get("link")
    print("="*10, f"Result #{i+start-1}", "="*10)
    print("Title:", title)
    print("Description:", snippet)
    print("Long description:", long_description)
    print("URL:", link, "\n")
"""

"""
    if request.method == 'POST':
        search = request.POST['search']
        url = 'https://www.ask.com/web?q='+search
        res = requests.get(url)
        soup = bs(res.text, 'lxml')

        result_listings = soup.find_all('div', {'class': 'PartialSearchResults-item'})

        final_result = []

        for result in result_listings:
            result_title = result.find(class_='PartialSearchResults-item-title').text
            result_url = result.find('a').get('href')
            result_desc = result.find(class_='PartialSearchResults-item-abstract').text

            final_result.append((result_title, result_url, result_desc))

        context = {
            'final_result': final_result
        }

        return render(request, 'search.html', context)

    else:
        return render(request, 'search.html')
    """

