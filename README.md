# 🎙️ **Voicemail Pro** – *Voice-Based Email System for the Visually Challenged*

## 📌 **Overview**

**Voicemail Pro** is a Python-based voice-controlled email system specifically designed to assist *visually challenged individuals* in accessing, managing, and sending emails through speech. This project removes the reliance on traditional visually-driven interfaces by integrating **speech recognition** and **text-to-speech** technologies, providing an inclusive, hands-free communication experience.

---

## 🧠 **Problem Statement**

The *visually challenged community* faces significant obstacles when interacting with standard email platforms that are predominantly visual. Reading, composing, and managing emails independently becomes difficult due to these design limitations.

---

## 🎯 **Objective**

To build a **voice-based email solution** that allows visually impaired users to:

- 🗣️ Listen to received emails  
- ✍️ Compose and send emails through voice  
- 📨 Navigate their inbox using voice commands  
- 🔓 Perform basic email operations independently

---

## 🛠️ **Technologies Used**

- **Python 3**
- **SpeechRecognition** – for converting speech to text
- **pyttsx3 / gTTS** – for converting text to speech
- **smtplib** – for sending emails
- **imaplib & email** – for reading emails
- **pyAudio / SpeechInput APIs** – for voice command input

---

## 🧩 **Features**

- 🔊 **Text-to-Speech**: System reads out emails for the user  
- 🎙️ **Speech-to-Text**: Compose and send emails by speaking  
- 📬 **Inbox Navigation**: Listen to email subjects and content  
- 🗣️ **Command-Based System**: Voice commands for email actions (e.g., *"Read inbox"*, *"Send mail"*)  
- 🔐 **Secure Authentication**: Email login using credentials

---

## 🔁 **Workflow**

1. **Login** with email credentials  
2. **Voice-driven menu**: Choose to read inbox, compose mail, etc.  
3. **Speech recognition** interprets user commands  
4. **Email content** is read aloud via TTS  
5. **Voice input** is transcribed and sent as mail

---

## 🧪 **How to Run**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/voicemail-pro.git
   cd voicemail-pro

2. Install dependencies:

pip install -r requirements.txt


3. Run the main script:

python main.py




---

📁 Folder Structure

<pre>
```plaintext
voicemail-pro/
│
├── main.py                  # Main executable script
├── README.md                # Project documentation
├── requirements.txt         # Project dependencies
│
├── modules/                 # All functionality modules
│   ├── listener.py          # Speech-to-text functions
│   ├── speaker.py           # Text-to-speech functions
│   ├── email_reader.py      # Read inbox logic
│   └── email_sender.py      # Send email logic
│
├── assets/                  # (Optional) Sounds or logs
│   └── welcome.mp3
```
</pre>
---

🔮 Future Improvements

✅ Integrate Gmail/Outlook OAuth login

🌐 Add support for multiple languages

🔎 Enable voice-based filtering/searching

🖥️ UI fallback for partially sighted users



---

🙌 Acknowledgements

This project was developed as a step toward digital inclusivity, aiming to empower the visually impaired community through accessible technology.


---
