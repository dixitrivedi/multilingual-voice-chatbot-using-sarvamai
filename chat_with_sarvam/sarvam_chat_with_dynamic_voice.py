from collections import deque

from sarvamai import SarvamAI
from sarvamai.play import play, save

import os
from dotenv import load_dotenv
load_dotenv()

from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich import print as pprint

import sounddevice as sd
from scipy.io.wavfile import write

import time

import numpy as np


# ------------------------------------------------------------
# Initilization
# ------------------------------------------------------------

console = Console()

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))


# ------------------------------------------------------------
# Sarvam Speech to text
# ------------------------------------------------------------

# def record_audio(filename="recorded_audio.wav", duration=5, sample_rate=44100):
#     """
#     Record audio from the microphone and save as a WAV file.
#     """
#     print(f"Recording for {duration} seconds...")
#     recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
#     sd.wait()
#     write(filename, sample_rate, recording)
#     # print(f"Recording saved to {filename}")
#     return filename

def record_audio(filename="recorded_audio.wav", duration=60, sample_rate=44100):
    """
    Record with Enter key control (no root required on Linux).
    
    Args:
        filename: Output file name
        sample_rate: Audio sample rate
        max_duration: Maximum recording duration (seconds)
    """
    print("🎤 Press ENTER to start recording...")
    input()  # Wait for Enter
    
    print("🔴 Recording started! Press ENTER again to stop...")
    
    recording = []
    is_recording = True
    
    def audio_callback(indata, frames, time, status):
        if is_recording:
            recording.extend(indata[:, 0])
    
    # Start recording in a separate thread
    import select
    import sys
    
    stream = sd.InputStream(samplerate=sample_rate, channels=1, 
                          callback=audio_callback, dtype='float32')
    
    with stream:
        start_time = time.time()
        
        while is_recording:
            # Check if Enter was pressed (Linux/Mac compatible)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()  # Consume the Enter
                print("⏹️ Recording stopped by user\n\n")
                break
                
            # Check max duration
            if time.time() - start_time > duration:
                print("⏰ Maximum duration reached")
                break
                
            time.sleep(0.1)
    
    if recording:
        recording_array = np.array(recording, dtype=np.float32)
        recording_int16 = (recording_array * 32767).astype(np.int16)
        write(filename, sample_rate, recording_int16)
        
        duration = len(recording) / sample_rate
        # print(f"✅ Saved recording. Duration: {duration:.1f}s")
        return filename
    else:
        print("❌ No audio recorded")
        return None

def transcribe_audio(audio_file_path, model="saarika:v2.5", language_code="unknown", client=None):
    """
    Send the audio file to the transcription service and print the result.
    """
    if not client:
        raise ValueError("Speech-to-text client is not initialized!")

    if audio_file_path and os.path.exists(audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model=model,
                language_code=language_code
            )
        # print("Transcription Response:")
        # print(response)
        return response
    else:
        print("No audio file found. Transcription aborted.")
        return None


# ------------------------------------------------------------
# Sarvam Text to speech
# ------------------------------------------------------------

def sarvam_tts(text,target_language_code):
    response = client.text_to_speech.convert(
    text=text,
    target_language_code=target_language_code,
    speaker="anushka",
    enable_preprocessing=True,
    )

    play(response)


# ------------------------------------------------------------
# Sarvam Text Translations
# ------------------------------------------------------------

def translate_text(text):
    response_list = []
    for lang_code in ["gu-IN", "en-IN"]:
        response = client.text.translate(
            input=text,
            source_language_code="hi-IN",
            target_language_code=lang_code,
            speaker_gender="Male",
            mode="formal",
            model="sarvam-translate:v1",
        )
        response_list.append(response.translated_text)
    return response_list


def chat():
    ## Welcome panel
    welcome_panel = Panel(
        Text(
            """
    Welcome to the Multilingual AI chat.
    Type your messsage to get started!

    How to use:
    1. Choose the language.
    2. To start recording press 'Enter' and to stop recording press 'Enter'.
    3. Enjoy!
            """,
            justify="left",
            style="bold"
        ),
        title="AI Chatbot",
        border_style="yellow"
    )
    console.print(welcome_panel)


    ## Choose Language Panel
    lang_panel = Panel(
        Text(
            """
   Choose Language.
   1. Hindi
   2. Gujarati
   3. English
            """,
            justify="left",
            style="bold"
        ),
        title="AI Chatbot",
        border_style="yellow"
    )
    console.print(lang_panel)

    lang_input = input("Choose a number: ")

    if "1" in lang_input:
        lang = "Hindi"
    elif "2" in lang_input:
        lang = "Gujarati"
    elif "3" in lang_input:
        lang = "English"
    else:
        raise "Choose number propely."

    SYSTEM_PROMPT = f"""You are a friendly AI. 
    Your task is to give a proper response to users.
    Your always output your response in {lang} language.
    """

    transcript = deque(maxlen=5)

    while True:
        # user_input = input("You: ")

        audio_path = record_audio(duration=60)
        try:
            user_input = transcribe_audio(audio_file_path=audio_path, client=client)
            user_input = user_input.transcript
            pprint(f"[bold yellow]User: {user_input}[/bold yellow]")
        except Exception as e:
            print("Error during transcription:", e)
            user_input = ""

        if user_input == 'q':
            break

        transcript.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": t['role'], "content": t['content']} for t in transcript
        ]

        assistant_response = client.chat.completions(
            messages=messages,
            temperature=0.7
        )
        assistant_response = assistant_response.choices[0].message.content
        transcript.append({"role": "assistant", "content": assistant_response})

        if "1" in lang_input:
            lang_code = "hi-IN"
        elif "2" in lang_input:
            lang_code = "gu-IN"
        elif "3" in lang_input:
            lang_code = "en-In"
        else:
            raise "Choose number propely."

        sarvam_tts(assistant_response, lang_code)

        pprint(f"[bold yellow]Assistant: {assistant_response}[/bold yellow]")

        # gu, en = translate_text(assistant_response)

        # translation_panel = Panel(
        #     f"[bold yellow]Gujarati:[/bold yellow] {gu}\n[bold magenta]English:[/bold magenta] {en}",
        #     title="Translations",
        #     border_style="yellow"
        #     )
    
        # console.print(translation_panel)

        print("\n\n")


## Example usage
if __name__ == "__main__":
    chat()
    














