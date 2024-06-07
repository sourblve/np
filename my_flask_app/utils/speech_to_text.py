import openai

def speech_to_text(audio_data):
    response = openai.Audio.transcribe("whisper-1", audio_data)
    return response['text']
