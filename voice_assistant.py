import streamlit as st
import pywhatkit
import datetime
import wikipedia
import pyjokes
import speech_recognition as sr
import time
import webbrowser
import os
import google.generativeai as genai
import pyttsx3
import threading

st.set_page_config(page_title="Praveen Voice Assistant", page_icon="🤖", layout="centered")

# --- Gemini API Configuration ---
# Get API key from environment variable or Streamlit secrets
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY', '')

if not GEMINI_API_KEY:
    st.error("""
    ⚠️ **Gemini API Key Not Found!**
    
    Please set your Gemini API key using one of these methods:
    
    **Method 1: Environment Variable**
    ```bash
    # Windows
    set GEMINI_API_KEY=your_api_key_here
    
    # macOS/Linux
    export GEMINI_API_KEY=your_api_key_here
    ```
    
    **Method 2: Streamlit Secrets (for deployment)**
    Create `.streamlit/secrets.toml` file:
    ```toml
    GEMINI_API_KEY = "your_api_key_here"
    ```
    
    **Method 3: Direct Input (temporary)**
    Enter your API key below:
    """)
    
    # Temporary API key input (for development only)
    temp_api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if temp_api_key:
        GEMINI_API_KEY = temp_api_key
        st.success("API Key set successfully!")
    else:
        st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Text-to-Speech Setup ---
speech_engine = None
speech_thread = None

def init_speech_engine():
    global speech_engine
    try:
        speech_engine = pyttsx3.init()
        speech_engine.setProperty('rate', 170)
        voices = speech_engine.getProperty('voices')
        speech_engine.setProperty('voice', voices[1].id)  # Use female voice
    except Exception as e:
        st.error(f"Speech engine error: {str(e)}")

def speak_text(text):
    """Function to convert text to speech"""
    global speech_engine
    try:
        if speech_engine:
            speech_engine.say(text)
            speech_engine.runAndWait()
    except Exception as e:
        st.error(f"Speech error: {str(e)}")

def stop_speech():
    """Function to stop current speech"""
    global speech_engine
    try:
        if speech_engine:
            speech_engine.stop()
    except Exception as e:
        pass

# Initialize speech engine
init_speech_engine()

# --- Header ---
st.markdown("<h1 style='color:#eebbc3; margin-bottom:0; text-align:center;'>Praveen Voice Assistant</h1>", unsafe_allow_html=True)

# --- Sidebar with Info ---
st.sidebar.markdown("""
# Praveen
Your personal voice assistant 🤖

- Play YouTube songs
- Tell jokes
- Wikipedia answers
- Time queries
- Open applications
- Social media links
- AI-powered responses

**Connect with me:**
- [GitHub](https://github.com/Praveen1425)
- [LinkedIn](https://www.linkedin.com/in/praveen-muccharla-977302289/)

**🔮 AI Features:**
- Smart conversations
- Code generation
- Creative writing
- Problem solving
""")

# --- Main Area ---
st.markdown("<p style='text-align:center; color:#b8c1ec;'>Talk to Praveen using text or your microphone!</p>", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'assistant', 'content': "Yo! I'm Praveen – your personal voice assistant 💡"}
    ]
if 'input_key' not in st.session_state:
    st.session_state['input_key'] = 0
if 'voice_processing' not in st.session_state:
    st.session_state['voice_processing'] = False
if 'speak_responses' not in st.session_state:
    st.session_state['speak_responses'] = True

# --- Chat Bubble Styles ---
CHAT_CSS = '''
<style>
.praveen-bubble {
    background: #232946;
    color: #eebbc3;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin-bottom: 8px;
    max-width: 80%;
    font-size: 1.1em;
    box-shadow: 0 2px 8px #0001;
}
.user-bubble {
    background: #b8c1ec;
    color: #232946;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin-bottom: 8px;
    margin-left: auto;
    max-width: 80%;
    font-size: 1.1em;
    box-shadow: 0 2px 8px #0001;
}
.chat-row {
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    margin-bottom: 2px;
}
</style>
'''
st.markdown(CHAT_CSS, unsafe_allow_html=True)

# --- Chat UI ---
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"<div class='chat-row'><div class='user-bubble'>🧑‍💻 {msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-row'><div class='praveen-bubble'>🤖 {msg['content']}</div></div>", unsafe_allow_html=True)

# --- Gemini AI Functions ---
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process that with AI: {str(e)}"

def generate_code_with_gemini(prompt):
    try:
        code_prompt = f"Generate Python code for: {prompt}. Provide only the code with comments."
        response = model.generate_content(code_prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't generate code: {str(e)}"

# --- Improved Wikipedia Search ---
def search_wikipedia(query):
    try:
        # Set language to English
        wikipedia.set_lang("en")
        
        # Try direct search first
        try:
            page = wikipedia.page(query)
            return wikipedia.summary(page.title, sentences=2)
        except wikipedia.exceptions.PageError:
            pass
        
        # Try search with suggestions
        search_results = wikipedia.search(query, results=3)
        if search_results:
            # Try the first result
            try:
                page = wikipedia.page(search_results[0])
                return wikipedia.summary(page.title, sentences=2)
            except:
                # Try the second result if first fails
                if len(search_results) > 1:
                    try:
                        page = wikipedia.page(search_results[1])
                        return wikipedia.summary(page.title, sentences=2)
                    except:
                        pass
        
        return f"Sorry, I couldn't find information about '{query}' on Wikipedia."
        
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]
        return f"I found multiple results for '{query}'. Did you mean: {', '.join(options)}?"
    except Exception as e:
        return f"Sorry, there was an error searching for '{query}': {str(e)}"

# --- Improved YouTube Search ---
def play_youtube_video(song_name):
    try:
        # Add "song" or "music" to improve search results
        search_query = f"{song_name} song official"
        pywhatkit.playonyt(search_query)
        return True
    except Exception as e:
        return False

# --- Praveen Logic ---
def praveen_reply(command):
    command = command.lower()
    
    # Music & Entertainment
    if "play" in command:
        song = command.replace("play", "").strip()
        reply = f"Playing {song} on YouTube 🎶"
        if not play_youtube_video(song):
            reply = f"Sorry, couldn't play {song} on YouTube."
    
    # Time queries
    elif "what's the time" in command or "time" in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        reply = f"It's {time_now} ⏰"
    
    # Wikipedia searches - Improved functionality
    elif "who is" in command:
        person = command.replace("who is", "").strip()
        reply = search_wikipedia(person)
    
    # Jokes
    elif "joke" in command:
        reply = pyjokes.get_joke()
    
    # Gemini AI Commands
    elif "ai" in command or "gemini" in command:
        # Remove trigger words and get the actual question
        ai_prompt = command.replace("ai", "").replace("gemini", "").replace("ask", "").strip()
        if ai_prompt:
            reply = get_gemini_response(ai_prompt)
        else:
            reply = "What would you like me to help you with using AI?"

    elif "generate code" in command or "code" in command:
        code_request = command.replace("generate code", "").replace("code", "").strip()
        if code_request:
            reply = generate_code_with_gemini(code_request)
        else:
            reply = "What kind of code would you like me to generate?"
    
    # Application opening commands
    elif "open chrome" in command:
        reply = "Opening Chrome browser 🚀"
        try:
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(chrome_path):
                os.startfile(chrome_path)
            else:
                reply = "Chrome not found on your system."
        except:
            reply = "Couldn't open Chrome."
    
    elif "open spotify" in command:
        reply = "Opening Spotify 🎵"
        try:
            spotify_path = "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe"
            if os.path.exists(os.path.expandvars(spotify_path)):
                os.startfile(os.path.expandvars(spotify_path))
            else:
                # Try to open Spotify via URL
                webbrowser.open("https://open.spotify.com")
                reply = "Opening Spotify in browser 🎵"
        except:
            reply = "Couldn't open Spotify."
    
    elif "open settings" in command:
        reply = "Opening Windows Settings ⚙️"
        try:
            os.system("start ms-settings:")
        except:
            reply = "Couldn't open Settings."
    
    elif "open instagram" in command:
        reply = "Opening Instagram 📸"
        try:
            webbrowser.open("https://www.instagram.com")
        except:
            reply = "Couldn't open Instagram."
    
    elif "open whatsapp" in command:
        reply = "Opening WhatsApp 💬"
        try:
            webbrowser.open("https://web.whatsapp.com")
        except:
            reply = "Couldn't open WhatsApp Web."
    
    elif "open github" in command:
        reply = "Opening your GitHub profile 👨‍💻"
        try:
            webbrowser.open("https://github.com/Praveen1425")
        except:
            reply = "Couldn't open GitHub."
    
    elif "open linkedin" in command:
        reply = "Opening your LinkedIn profile 💼"
        try:
            webbrowser.open("https://www.linkedin.com/in/praveen-muccharla-977302289/")
        except:
            reply = "Couldn't open LinkedIn."
    
    elif "open vs code" in command or "open code" in command:
        reply = "Opening VS Code 💻"
        try:
            os.system("code")
        except:
            reply = "Couldn't open VS Code."
    
    elif command.strip() == "":
        reply = "Sorry, I didn't catch that."
    else:
        # If no specific command matches, use Gemini for general conversation
        reply = get_gemini_response(command)
    
    return reply

# --- Speech Control ---
st.sidebar.markdown("### 🔊 Speech Settings")
speak_enabled = st.sidebar.checkbox("Enable Voice Responses", value=True, key="speak_enabled")

# --- Input Area ---
st.markdown("<hr>", unsafe_allow_html=True)

# Text input with dynamic key to clear after processing
user_input = st.text_input("Say something to Praveen:", key=f"input_{st.session_state['input_key']}")

# Process text input
if user_input and user_input.strip():
    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    reply = praveen_reply(user_input)
    st.session_state['messages'].append({'role': 'assistant', 'content': reply})
    
    # Speak the response if enabled
    if speak_enabled:
        # Stop any current speech first
        stop_speech()
        # Run speech in a separate thread
        speech_thread = threading.Thread(target=speak_text, args=(reply,))
        speech_thread.start()
    
    # Increment key to clear the input field
    st.session_state['input_key'] += 1
    st.rerun()

# Voice input section
st.markdown("### 🎤 Voice Input")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🎤 Start Voice Recognition", key="voice_button"):
        # Stop any current speech when starting voice recognition
        stop_speech()
        st.session_state['voice_processing'] = True
        st.rerun()

# Voice processing
if st.session_state['voice_processing']:
    with st.spinner("🎧 Listening... Please speak now!"):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Recognize speech
                voice_text = recognizer.recognize_google(audio)
                
                if voice_text:
                    st.success(f"🎤 You said: {voice_text}")
                    st.session_state['messages'].append({'role': 'user', 'content': voice_text})
                    reply = praveen_reply(voice_text)
                    st.session_state['messages'].append({'role': 'assistant', 'content': reply})
                    
                    # Speak the response if enabled
                    if speak_enabled:
                        speech_thread = threading.Thread(target=speak_text, args=(reply,))
                        speech_thread.start()
                    
                    st.session_state['voice_processing'] = False
                    st.rerun()
                    
        except sr.WaitTimeoutError:
            st.error("No speech detected. Please try again.")
            st.session_state['voice_processing'] = False
            st.rerun()
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
            st.session_state['voice_processing'] = False
            st.rerun()
        except sr.RequestError:
            st.error("Network error with Google Speech Recognition.")
            st.session_state['voice_processing'] = False
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state['voice_processing'] = False
            st.rerun()

# Custom styling
st.markdown("<style>div.stTextInput>div>input {background-color: #232946; color: #fffffe;}</style>", unsafe_allow_html=True) 
 