from postgres import Postgres
from embedding import create_query_embedding
from dotenv import load_dotenv
import ollama
import os
import requests
import json

pg = Postgres()

load_dotenv()

openrouter_api_key = os.getenv("openrouter_api_key")
openrouter_model = os.getenv("openrouter_model")


def create_context(query):
    query_text_search_context = pg.text_search(query)
    query_embedding = create_query_embedding(query)
    query_embedding_search_context = pg.embedding_search(query_embedding)
    return query_text_search_context + query_embedding_search_context


def generate_response_local(query):
    system_prompt = f"""The user wants to learn through the podcast they listen to since they
    trust it as a source of information. Provide a response based on the
    context provided below only. If you cannot, answer with a 'I do not know'. 
    <context>
    {create_context(query)}
    </context>
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    response = ollama.chat(model=os.getenv("llm_model"), messages=messages)
    return response.message.content


def generate_response_openrouter(query):
    system_prompt = f"""The user wants to learn through the podcast they listen to since they
    trust it as a source of information. Provide a response based on the
    context provided below only. If you cannot, answer with a 'I do not know'. 
    <context>
    {create_context(query)}
    </context>
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "ghost",
        },
        data=json.dumps(
            {
                "model": openrouter_model,  # Optional
                "messages": messages,
            }
        ),
    )
    return response
