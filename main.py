from llm import generate_response_openrouter
from utils import format_openrouter_response
from sync import sync

sync()

while True:
    query = input("\n\nWhat can I help with?\n\n")
    response = generate_response_openrouter(query)
    print(format_openrouter_response(response))
