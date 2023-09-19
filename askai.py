import os, openai
from dotenv import load_dotenv

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")
openai.api_key = apikey


def ask(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        n=1,
    )
    output = [k["text"].strip() for k in response["choices"]]
    return output
