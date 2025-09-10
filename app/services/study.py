import os
from openai import OpenAI

def ask_openai(question: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OpenAI key not configured. Set environment variable OPENAI_API_KEY.")
    client = OpenAI(api_key=key)
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        max_tokens=256,
        messages=[
            {"role":"system","content":"You are a concise, helpful study assistant."},
            {"role":"user","content":question}
        ]
    )
    return r.choices[0].message.content.strip()
