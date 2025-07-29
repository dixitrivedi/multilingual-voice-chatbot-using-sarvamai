from collections import deque

from sarvamai import SarvamAI
from sarvamai.play import play, save

import os
from dotenv import load_dotenv
load_dotenv()

from rich.panel import Panel
from rich.console import Console
from rich.text import Text

import sounddevice as sd
from scipy.io.wavfile import write


# ------------------------------------------------------------
# Initilization
# ------------------------------------------------------------

console = Console()

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))


# ------------------------------------------------------------
# Sarvam Speech to text
# ------------------------------------------------------------

def record_audio(filename="recorded_audio.wav", duration=5, sample_rate=44100):
    """
    Record audio from the microphone and save as a WAV file.
    """
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(filename, sample_rate, recording)
    # print(f"Recording saved to {filename}")
    return filename


def transcribe_audio(audio_file_path, model="saarika:v2.5", language_code="en-IN", client=None):
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

def sarvam_tts(text):
    response = client.text_to_speech.convert(
    text=text,
    target_language_code="hi-IN",
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
    SYSTEM_PROMPT = """You are a friendly AI. 
    Your task is to give a proper response to users.
    Your always output your response in 'Hindi' language.
    """

    welcome_panel = Panel(
        Text(
            """
    Welcome to the Multilingual AI chat.
    Type your messsage to get started!
            """,
            justify="left",
            style="bold"
        ),
        title="AI Chatbot",
        border_style="yellow"
    )
    console.print(welcome_panel)

    transcript = deque(maxlen=5)

    while True:
        # user_input = input("You: ")

        audio_path = record_audio(duration=5)
        try:
            user_input = transcribe_audio(audio_file_path=audio_path, client=client)
            user_input = user_input.transcript
            print(f"User: {user_input}")
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

        sarvam_tts(assistant_response)

        print(f"Assistant: {assistant_response}")

        gu, en = translate_text(assistant_response)

        translation_panel = Panel(
            f"[bold yellow]Gujarati:[/bold yellow] {gu}\n[bold magenta]English:[/bold magenta] {en}",
            title="Translations",
            border_style="yellow"
            )
    
        console.print(translation_panel)

        print("\n\n")


## Example usage
if __name__ == "__main__":
    chat()
    














