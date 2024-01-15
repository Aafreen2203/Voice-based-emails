import os
import tkinter
import tkinter as tk
import speech_recognition as sr
import pyttsx3
import imaplib
import email
import time
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter
import smtplib

# from google_auth_httplib2 import Request
# from googleapiclient.discovery import build

import config
import face_recognition  # Face recognition library
import cv2
from gmail_api_new import get_gmail_labels
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow

# Initialize the Tkinter GUI
root = customtkinter.CTk()
root.geometry("640x440")
root.title("Voice-Controlled Email Client")


# background image
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

img1 = ImageTk.PhotoImage(Image.open("C:\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\bg1_resize.jpg"))
l1 = customtkinter.CTkLabel(master=root, image=img1)
l1.pack()

# Initialize the speech recognition engine
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Create a global mail object to store the IMAP connection
mail = None

# Create a function to handle Gmail-related actions
def handle_gmail_action():
    # Call the Gmail API function to get Gmail labels
    labels = get_gmail_labels()
    if not labels:
        labels = ["No labels found"]

        # Create a Listbox widget to display the labels
    label_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    label_listbox.pack()

    # Insert each label into the Listbox
    for label in labels:
        label_listbox.insert(tk.END, label)


# Add a button to trigger the function to display labels
fetch_labels_button = tk.Button(root, text="Fetch Gmail Labels", command=handle_gmail_action)
fetch_labels_button.pack()

# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']  # Adjust the scope as needed
#
# def authenticate_gmail():
#     flow = InstalledAppFlow.from_client_secrets_file("C\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\credentials.json",SCOPES)
#     if os.path.exists("C\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\credentials.json"):
#         print("File exists.")
#     else:
#         print("File does not exist.")
#     creds = flow.run_local_server(port=0)
#
#     # Save credentials for future use
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())


# Load known faces for recognition
known_faces = [face_recognition.load_image_file("C:\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\my_face.jpg")]
known_face_encodings = [face_recognition.face_encodings(face)[0] for face in known_faces]


# Capture video from a camera (0 is the default camera)
def capture_video():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Capture the user's face
def capture_face():
    # Capture a single frame
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Find face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if face_encodings:
        return face_encodings[0]  # Return the first detected face
    else:
        return None


# Recognize faces in the captured video
def recognize_faces(known_faces, unknown_face):
    results = face_recognition.compare_faces(known_faces, unknown_face)
    return any(results)


# Function for face-based login
def login_with_face():
    global mail
    speak("Please show your face for authentication.")
    unknown_face = capture_face()

    if unknown_face is not None:  # Check if face was detected
        if recognize_faces(known_face_encodings, unknown_face):
            speak("Face recognized. Please speak your Gmail email address.")
            email_address = listen()

            if email_address:
                speak("Please speak your Gmail password.")
                password = listen()
                try:
                    mail = imaplib.IMAP4_SSL("imap.gmail.com")
                    mail.login("coco22jojo@gmail.com", "fwwl wjdd bymz cfvx")
                    speak("Login successful.")
                except Exception as e:
                    speak(f"Login failed. Error: {str(e)}")
        else:
            speak("Face recognition failed. Access denied.")
    else:
        speak("No face detected. Please try again.")

# Add an initial instruction to click anywhere on the screen
engine.say("Please click anywhere on the screen to activate voice commands.")
engine.runAndWait()
engine.say("""
             Say Login to log into your gmail account.
             Compose to compose an email.
             Read to read your inbox.
             Exit to exit the application.""")

unm='coco22jojo@gmail.com'
pswd='fwwl wjdd bymz cfvx'

# Define a function to speak text
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Define a function to listen to voice input
def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak("Speak now:")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return None


# Define email login function
# def login_to_gmail():
#     global mail
#     speak("Please speak your Gmail email address")
#     # mail.login(config.username, config.password)
#     email_address = listen()
#     if email_address:
#         speak("Please speak your Gmail password")
#         password = listen()
#         try:
#             mail = imaplib.IMAP4_SSL("imap.gmail.com")
#             # mail.login(config.username, config.password, config.unm, config.psw)
#             mail.login('coco22jojo@gmail.com', 'fwwl wjdd bymz cfvx')
#             speak("Login successful.")
#         except Exception as e:
#             speak(f"Login failed. Error: {str(e)}")

# Define email read function
def read_email():
    if mail is None:
        speak("Please log in to your Gmail account first.")
    else:
        mail.select("inbox")
        result, data = mail.uid("search", None, "ALL")
        latest_email_uid = data[0].split()[-1]
        result, email_data = mail.uid("fetch", latest_email_uid, "(RFC822)")
        raw_email = email_data[0][1].decode("utf-8")
        msg = email.message_from_string(raw_email)
        str = "Please say the serial number of the email you wanna read starting from latest"
        speak(str)
        listen()
        subject = msg["subject"]
        from_address = msg["from"]
        speak(f"Subject: {subject}")
        speak(f"From: {from_address}")
        speak("Email content:")
        email_content = msg.get_payload()
        speak(email_content)
        speak("Email reading complete. Please choose another action. Click anywhere on the screen and say 'compose' to compose an email, 'read' to read your inbox, or 'exit' to exit.")
def compose_email():
    rec = 'jojo25coco@gmail.com'
    str = "please speak receiver's email"
    speak(str)
    msg = listen()

    str = "You have spoken the email"
    speak(str)
    speak(msg)

    str = "please speak the body of your email"
    speak(str)
    msg = listen()

    str = "You have spoken the message"
    speak(str)
    speak(msg)

    # button_function()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(config.unm, config.psw)
    server.sendmail(config.unm, rec, msg)
    server.quit()

    str = "The email has been sent. Please choose another action. Click anywhere on the screen and say 'compose' to compose another email, 'read' to read your inbox, or 'exit' to exit."
    speak(str)


# Define a function to open an email (for future use)
def open_email():
    speak("This feature will be implemented in the future.")

# Define email send function
def send_email(recipient, subject, message):
    if mail is None:
        speak("Please log in to your Gmail account first.")
    else:
        try:
            message = f"Subject: {subject}\nTo: {recipient}\n\n{message}"
            mail.append("inbox", "", imaplib.Time2Internaldate(time.time()), message.encode('utf-8'))
            speak("Email sent successfully.")
        except Exception as e:
            speak(f"Email sending failed. Error: {str(e)}")

# Define functions to show the inbox and compose frames
def show_inbox():
    speak("You have chosen to access your Gmail inbox.")
    read_email()

def show_compose():
    speak("You have chosen to compose an email.")
    compose_email()

# Create a function to list email labels
# def list_labels():
#     creds = None
#     # The file token.json stores the user's access and refresh tokens
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json')
#
#     # If there are no (valid) credentials available, let the user log in
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             authenticate_gmail()
#
#     service = build('gmail', 'v1', credentials=creds)
#     results = service.users().labels().list(userId='me').execute()
#     labels = results.get('labels', [])
#
#     if not labels:
#         speak('No labels found.')
#     speak('Labels:')
#     for label in labels:
#         speak(label['name'])
#
# # Example: Call the function to list labels
# list_labels()

# Define function to process voice commands
def on_voice_command():
    command = listen().lower()
    if "click anywhere on the screen" in command:
        show_inbox()
    if "inbox" in command:
        show_inbox()
    elif "compose" in command:
        show_compose()
    elif "read" in command:
        read_email()
    elif "open email" in command:
        open_email()
    elif "login" in command:
        speak("Please provide your login information.")
        login_with_face()
    elif "send email" in command:
        show_compose()
    elif "exit" in command:
        speak("You have chosen to exit. Goodbye!")
        root.quit()
    else:
        speak("Invalid command. Please speak 'inbox', 'compose', 'read', 'open email', 'login', 'send email', or 'exit'.")


# Ask the user for their desired action (login, compose, or read)
def ask_for_action():
    speak("Please say 'login' to login into your Gmail account, 'compose' to compose an email, or 'read' to read your inbox.")
    action = listen().lower()
    if action == "login":
        login_with_face()
    elif action == "compose":
        show_compose()
    elif action == "read":
        read_email()
    else:
        speak("Invalid choice. Please click anywhere on the screen and choose again.")

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create File menu
menu_bar.add_cascade(label="Read",command=show_inbox)
menu_bar.add_cascade(label="Compose",command=show_compose)
menu_bar.add_cascade(label="Login",command=login_with_face())
menu_bar.add_cascade(label="Exit",command=root.quit)
mButton=Menubutton(root,text="Click")
mButton.pack()

# Define the button's shape (an oval in this example)
button_shape = PhotoImage(file="C:\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\button5.png")

# Create a Canvas widget to hold the custom-shaped button
canvas = Canvas(root, width=button_shape.width(), height=button_shape.height(),highlightthickness=0)
canvas.create_image(0, 0, anchor=NW,image=button_shape)
canvas.place(x=300, y=400)  # Adjust the x and y coordinates as needed

# Load the button image
voice_button = PhotoImage(file="C:\\Users\\AAFREEN\\OneDrive\\Desktop\\python mini proj\\button5.png")

def on_enter(event):
    canvas.itemconfig(voice_button, fill="red")

def on_leave(event):
    canvas.itemconfig(voice_button, fill="blue")


canvas.tag_bind(voice_button, "<Enter>", on_enter)
canvas.tag_bind(voice_button, "<Leave>", on_leave)


# Create Voice Command button with a transparent shape
voice_command_button = Button(canvas, image=voice_button, command=on_voice_command, borderwidth=0)
voice_command_button.place(x=0, y=0)

# Define a function to handle the "click anywhere on the screen" event
def on_screen_click(event):
    on_voice_command()  # Trigger the voice command function when a click event occurs

# Bind a click event to the entire application window
root.bind("<Button-1>", on_screen_click)

root.mainloop()