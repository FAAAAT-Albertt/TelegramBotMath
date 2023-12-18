"""file for gpt model"""
import asyncio
import openai
from typing import *

from config import API_KEY

openai.api_key = API_KEY

async def generate_response(messages:  List[Dict[str, Union[str, Any]]]) -> Awaitable[str]:
    """function answer gpt model"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']
