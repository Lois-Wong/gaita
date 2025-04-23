from typing import Any, Dict, List
import openai
from openai import OpenAI
import os

def stream_completion(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Make the API call with streaming enabled
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True  # Enable streaming
    )
    
    # Process the streaming response
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content