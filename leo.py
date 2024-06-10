import tkinter as tk
from tkinter import simpledialog
import requests
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
from datetime import datetime, timedelta,time
import pywhatkit
import time
from ecapture import ecapture as ec
import cv2
from googlesearch import search
import pyautogui

id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"

def speak(message):
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    engine.say(message)
    engine.runAndWait()

# Function to generate a response
def get_response(input_text, user_name=None):
    input_text = input_text.lower()

    # Check for personalized responses
    if "hey leo" in input_text:
        return "Hello! How can I assist you today?"

    # Handle asking the chatbot's name
    if "what's your name" in input_text or "your name" in input_text:
        if user_name:
            return f"My name is Leo, and I remember you, {user_name}!"
        else:
            return "I'm ChatBot, your virtual assistant! What's your name?"
     # Handle introducing the chatbot when the user provides their name
    if "my name is" in input_text:
        user_name = input_text.split("my name is")[-1].strip()
        save_user_name(user_name)
        return f"Hello, {user_name}! Nice to meet you."
    
    # Check for other responses
    for keyword, response in responses.items():
        if keyword in input_text:
            return response

    # Check for a reminder request
    if "reminder for tomorrow" in input_text:
        set_reminder()
        return "Reminder set for tomorrow!"

    # Check for voice search
    #if "voice search" in input_text.lower():
       # return "Say the search query after the beep."

    #return "Can you ask another question?"

# Function to save user name
def save_user_name(name):
    with open("user_name.txt", "w") as file:
        file.write(name)

# Function to load user name
def load_user_name():
    try:
        with open("user_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Function to handle user input
def handle_user_input():
    global user_name
    user_input = user_input_entry.get()
    response = get_response(user_input, user_name)

    if "voice search" in user_input.lower():
        handle_voice_input()
    else:
        update_chat_history(f"You: {user_input}\nChatbot: {response}\n")

    user_input_entry.delete(0, tk.END)

# Function to handle voice input
def handle_voice_input():
    global user_name  # Add this line
    search_query = handle_voice_search()

    if 'search the internet for' in search_query:
        search_query = search_query.replace('search the internet for', '')
        pywhatkit.search(search_query)
        update_chat_history(f"You (voice): {search_query}\nChatbot: Searching the internet for {search_query}\n")
    elif "open google" in search_query:
        webbrowser.open("https://www.google.com")
        update_chat_history("You (voice): Open Google\nChatbot: Opening Google in your web browser.\n")
    elif "open youtube" in search_query:
        webbrowser.open("https://www.youtube.com")
        update_chat_history("You (voice): Open YouTube\nChatbot: Opening YouTube in your web browser.\n")
    elif "open gmail" in search_query:
        webbrowser.open("https://mail.google.com")
        update_chat_history("You (voice): Open Gmail\nChatbot: Opening Gmail in your web browser.\n")
    elif "open chat gpt" in search_query:
        webbrowser.open("https://openai.com/chatgpt")
        update_chat_history("You (voice): Open chatgpt\nChatbot: Opening chatgpt in your web browser.\n")
    
    elif "play" in search_query:
        pywhatkit.playonyt(search_query)

    elif "take a screenshot" in search_query:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("C:/Users/mmk20/OneDrive/Desktop/Neha's folder/web devp/images/screenshot.png")
        update_chat_history("You (voice): take a screenshot\nChatbot: Done!\n")

    

    elif "weather" in search_query:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            
            update_chat_history("You (voice): what are the weather conditions\nChatbot: what is the city name\n")
            time.sleep(2)
            city_name = handle_voice_search()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                update_chat_history("Chatbot: Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

    elif "take a photo" in search_query:
        # ec.capture(0,"robo camera","C:/Users/mmk20/OneDrive/Desktop/Neha's folder/web devp/images/img.jpg")
        # time.sleep(5)
        cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
        else:
    # Read a frame from the camera
            ret, frame = cap.read()

    # Save the captured frame to an image file
        if ret:
            cv2.imwrite("C:/Users/mmk20/OneDrive/Desktop/Neha's folder/web devp/images/img.jpg", frame)
            print("Image captured successfully.")
            update_chat_history("You (voice): take a photot\nChatbot: Image captured successfully.!\n")
        else:
            print("Error: Could not read a frame from the camera.")
            update_chat_history("You (voice): take a photot\nChatbot: Error: Could not read a frame from the camera.\n")
    # Release the camera capture object
        cap.release()

    # Close any OpenCV windows
        cv2.destroyAllWindows()

    else:
        response = get_response(search_query, user_name)
        update_chat_history(f"You (voice): {search_query}\nChatbot: {response}\n")

def handle_voice_search():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("You can now speak")
        audio = r.listen(source)

        try:
            search_query = r.recognize_google(audio, language="en-gb")
            print("You said: " + search_query)
            return search_query.lower()
        except sr.UnknownValueError:
            print("Didn't understand audio.")
            return "I am still waiting"
        except sr.RequestError:
            print("Couldn't request results. There is no service.")
            return "I am still waiting"
        except Exception as e:
            print(f"Something went wrong: {e}")
            return "I am still waiting"


# Function to set a reminder for tomorrow
def set_reminder():
    tomorrow = datetime.now() + timedelta(days=1)
    reminder_time = tomorrow.replace(hour=9, minute=0, second=0)  # Set the time for the reminder
    now = datetime.now()

    time_difference = reminder_time - now
    seconds_in_a_day = 24 * 60 * 60
    time_in_seconds = int(time_difference.total_seconds() % seconds_in_a_day)

    # Use the `after` method to trigger the reminder after the calculated time difference
    root.after(time_in_seconds * 1000, remind_user)

# Function to remind the user
def remind_user():
    update_chat_history("Chatbot: Reminder: Don't forget about your appointment tomorrow!\n")

# Function to update chat history
def update_chat_history(message):
    chat_history_text.insert(tk.END, message)

# Create the main window
root = tk.Tk()
root.title("Leo")

# If user_name is not set, ask for it
user_name = load_user_name()
if user_name is None:
    user_name = simpledialog.askstring("Input", "Hello! May I know your name?")
    if user_name:
        save_user_name(user_name)

# Define a dictionary of keyword-response pairs
responses = {
    "hi": "Hello!",
    "how are you": "I am fine, thanks for asking!",
    "how was the day": "My day was great, thanks for asking!",
    "bye": "Goodbye!",
}

# Create and configure the chat history display
chat_history_text = tk.Text(root, height=10, width=40)
chat_history_text.pack()

# Create and configure the user input entry field
user_input_entry = tk.Entry(root, width=30)
user_input_entry.pack()

# Create and configure the send button
send_button = tk.Button(root, text="Send", command=handle_user_input)
send_button.pack()

# Create and configure the voice input button
voice_input_button = tk.Button(root, text="Voice Input", command=handle_voice_input)
voice_input_button.pack()

# Run the GUI application




# ... (rest of the code remains unchanged)

# Create the main window
root = tk.Tk()
root.title("Hey Leo")

# ... (rest of the code remains unchanged)

# Run the GUI application
root.mainloop()
