import openai

def text_to_speech(text):
    response = openai.Audio.create(
        model="text-davinci-003",
        text=text,
        voice="your-voice-id",
        format="mp3"
    )
    return response['audio']
