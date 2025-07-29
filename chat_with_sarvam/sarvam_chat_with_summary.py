from collections import deque
from sarvamai import SarvamAI

import os
from dotenv import load_dotenv
load_dotenv()

from rich.panel import Panel
from rich.console import Console
from rich.text import Text


console = Console()

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

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


def summrize_memory(messages_previous, new_message):

    system_prompt = """You are a transcript compressor.
You are given transcript of conversation and you need to compress it into 3-4 line summary.
Output the summary in bullet points.
Keep the summary in english and no markdown.
    """

    response = client.chat.completions(
            messages=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role":"user",
                    "content":f"Previous Conversation: {messages_previous} \n\n New Messages: {new_message}"
                }
            ],
            temperature=0.7
        )

    return response.choices[0].message.content


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

    transcript_summary = "No summary yet."

    while True:
        user_input = input("You: ")

        if user_input == 'q':
            break

        messages = [
            {
                "role":"system",
                "content": SYSTEM_PROMPT + f"\n\nSummary: {transcript_summary}"
            },
            {
                "role":"user",
                "content":user_input
            }
                
            ]

        assistant_response = client.chat.completions(
            messages=messages,
            temperature=0.7
        )
        assistant_response = assistant_response.choices[0].message.content

        print(f"Assistant: {assistant_response}")

        gu, en = translate_text(assistant_response)

        translation_panel = Panel(
            f"[bold yellow]Gujarati:[/bold yellow] {gu}\n[bold magenta]English:[/bold magenta] {en}",
            title="Translations",
            border_style="yellow"
            )
    
        console.print(translation_panel)

        transcript_summary = summrize_memory(
            transcript_summary,
            f"User: {user_input}\nAI: {assistant_response}"
        )

        print("\n\n")


## Example usage
if __name__ == "__main__":
    chat()





