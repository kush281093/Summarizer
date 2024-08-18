import openai
from dotenv import load_dotenv
import os
from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Set up OpenAI API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def get_client(self):
        # Return the OpenAI client for chat completions
        return OpenAI().chat.completions