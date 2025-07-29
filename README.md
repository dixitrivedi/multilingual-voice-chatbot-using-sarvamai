
# 🎙️ Multilingual Voice Chatbot using SarvamAI

This is a terminal-based multilingual voice chatbot built using [SarvamAI](https://sarvam.ai/). It supports **Hindi**, **Gujarati**, and **English** for both speech input and text/voice output.

---

## 🚀 Features

- 🎧 Record audio input from microphone
- 🧠 Transcribe speech using SarvamAI's ASR (`saarika:v2.5`)
- 💬 Chat with AI assistant in Hindi, Gujarati, or English
- 🔊 Assistant replies are spoken using SarvamAI's TTS
- 🌍 Dynamically select input/output languages
- 🛑 Press `Enter` to start/stop recording manually
- 🧵 Maintains short conversation history for context

---

## 🛠 Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install directly:

```bash
pip install sarvamai sounddevice scipy python-dotenv rich numpy
```

---

## 🧪 Setup

1. Get your [SarvamAI API Key](https://sarvam.ai/)
2. Create a `.env` file:

```
SARVAM_API_KEY=your_sarvam_api_key_here
```

3. Run the script:

```bash
python your_script_name.py
```

---

## 🎛️ How to Use

### 1. Start the Chat

When you run the script, you'll see a welcome message.

```bash
Welcome to the Multilingual AI chat.
```

### 2. Select Language

Choose from:

```
1. Hindi
2. Gujarati
3. English
```

Your selection controls both:
- The **assistant’s output language**
- The **TTS language** for replies

### 3. Record and Talk

- Press `Enter` to **start recording**
- Speak into your microphone
- Press `Enter` again to **stop recording**

### 4. Hear & Read the AI Reply

- The assistant will reply in the chosen language
- The reply is printed and **spoken aloud**

---

## 🧠 Tech Stack

| Component     | Technology           |
|---------------|----------------------|
| STT (Speech-to-Text) | SarvamAI `saarika:v2.5` |
| TTS (Text-to-Speech) | SarvamAI `anushka` |
| Chat Completion | SarvamAI Chat API |
| UI             | Terminal using Rich |
| Audio          | `sounddevice`, `scipy` |
| Language Config | Dynamic (via user input) |

---

## 📝 Code Structure

- `record_audio`: Record voice using `sounddevice`
- `transcribe_audio`: Convert voice to text using Sarvam STT
- `sarvam_tts`: Speak assistant reply
- `translate_text`: (optional) Translate output to English/Gujarati
- `chat()`: Main loop with conversation memory

---

## 📦 Optional Enhancements

- Add support for real-time transcription
- Streamline conversation via Streamlit UI
- Extend to more languages
- Add voice or speaker gender selector

---
