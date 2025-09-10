import os
from io import BytesIO
from openai import OpenAI

def speak(text: str) -> bytes:
    """Return MP3 bytes using OpenAI TTS (correct modern API)."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OpenAI key not configured. Set environment variable OPENAI_API_KEY.")
    client = OpenAI(api_key=key)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        format="mp3",
    ) as resp:
        buf = BytesIO()
        resp.stream_to_file(buf)
        return buf.getvalue()
