import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d6955f24e2964fd28997aa5875d2ed32"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    print(f"Processing command: {command}")  # Debug print
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open github" in command.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ", 1)[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in music library.")
    elif "news" in command.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Failed to retrieve news.")

if __name__ == "__main__":
    speak("Initializing JARVIS.....")
    while True:
        try:
            with sr.Microphone() as source:
                speak("Listening for the activation word 'JARVIS'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                print(f"Recognized word: {word}")  
                if word.lower() == "jarvis":
                    speak("Yes, Master. I am listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    speak(f"Command received: {command}")
                    try:
                        process_command(command)
                    except Exception as e:
                        speak(f"Error processing command: {e}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
