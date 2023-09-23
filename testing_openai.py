import openai, dotenv, os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

message = input("Ask away:> ")

response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=message,
    n=1,
)

response = [x["text"].strip() for x in response["choices"]]
print(response)
