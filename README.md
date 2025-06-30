# 🎤 Praveen Voice Assistant

A modern, AI-powered voice assistant built with Streamlit that combines traditional voice commands with cutting-edge Gemini AI capabilities.

## 📹 Demo Video

Watch the voice assistant in action! [(https://github.com/Praveen1425/MyPersonalAssitant/blob/main/Sample%20Video.mp4)]

**Demo Features:**
- Voice command recognition
- YouTube music playback
- AI-powered conversations
- System application control
- Real-time voice responses

## ✨ Features

### 🎵 **Music & Entertainment**
- Play any song on YouTube with voice commands
- "Play [song name]" - Instantly plays music on YouTube

### 🤖 **AI-Powered Conversations**
- Powered by Google's Gemini AI
- Smart responses to any question
- Code generation capabilities
- Creative writing assistance

### 📚 **Information & Knowledge**
- Wikipedia searches with "who is [person]"
- Real-time time queries
- Random jokes on demand

### 🎯 **System Control**
- Open applications (Chrome, Spotify, VS Code, Settings)
- Launch social media platforms (Instagram, WhatsApp)
- Access professional profiles (GitHub, LinkedIn)

### 🎤 **Voice & Text Interface**
- Voice recognition using Google Speech Recognition
- Text-to-speech responses
- Modern chat bubble interface
- Real-time voice processing

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone for voice input
- Speakers for voice output
- Internet connection
- Gemini API key from Google AI Studio

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Praveen1425/voice-assistant.git
   cd voice-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Gemini API Key (Choose one method)**

   **Method 1: Environment Variable (Recommended)**
   ```bash
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # macOS/Linux
   export GEMINI_API_KEY=your_api_key_here
   ```

   **Method 2: Streamlit Secrets (For deployment)**
   ```bash
   # Copy the example file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit the file and add your API key
   # Replace "your_gemini_api_key_here" with your actual key
   ```

   **Method 3: Direct Input (Development only)**
   - Run the app and enter your API key when prompted
   - This is temporary and not recommended for production

6. **Get your Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and use it in one of the methods above

7. **Run the application**
   ```bash
   streamlit run voice_assistant.py
   ```

## 🔒 Security Notes

- **Never commit your API key to git**
- The `.streamlit/secrets.toml` file is automatically ignored
- Use environment variables for production deployments
- The app will guide you if no API key is found

## 🎯 Voice Commands

### Music & Entertainment
- **"Play [song name]"** - Plays music on YouTube
- **"Tell me a joke"** - Gets a random joke

### Information Queries
- **"What's the time?"** - Shows current time
- **"Who is [person]?"** - Searches Wikipedia
- **"Ask AI [question]"** - Uses Gemini AI for smart responses
- **"Generate code [description]"** - Creates Python code

### System Control
- **"Open Chrome"** - Launches Chrome browser
- **"Open Spotify"** - Opens Spotify application
- **"Open VS Code"** - Launches Visual Studio Code
- **"Open Settings"** - Opens Windows Settings
- **"Open Instagram"** - Opens Instagram in browser
- **"Open WhatsApp"** - Opens WhatsApp Web
- **"Open GitHub"** - Opens your GitHub profile
- **"Open LinkedIn"** - Opens your LinkedIn profile

## 🛠️ Technical Details

### Dependencies
- **streamlit** - Web interface framework
- **google-generativeai** - Gemini AI integration
- **speechrecognition** - Voice recognition
- **pyttsx3** - Text-to-speech
- **pywhatkit** - YouTube integration
- **wikipedia** - Wikipedia API
- **pyjokes** - Joke generation
- **pyaudio** - Audio processing

### File Structure
```
voice-assistant/
├── voice_assistant.py      # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore patterns
├── demo.mp4               # Demo video (add your video here)
└── venv/                  # Virtual environment
```

### Performance Tips
- Use a quiet environment for better voice recognition
- Speak clearly and at normal pace
- Keep the application updated
- Use wired headphones for better audio quality

## 📞 Support

- **GitHub**: [Praveen1425](https://github.com/Praveen1425)
- **LinkedIn**: [Praveen Muccharla](https://www.linkedin.com/in/praveen-muccharla-977302289/)



**Made with ❤️ by Praveen Muccharla** 
