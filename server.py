from postgres import Postgres
from embedding import create_query_embedding
from dotenv import load_dotenv
import ollama
import os

pg = Postgres()

load_dotenv()


def create_context(query):
    query_text_search = pg.text_search(query)
    query_text_search_context = [
        chunk[5] if chunk is not None else None for chunk in query_text_search
    ]
    query_embedding = create_query_embedding(query)
    query_embedding_search = pg.embedding_search(query_embedding)
    query_embedding_search_context = [chunk[5] for chunk in query_embedding_search]
    return query_text_search_context + query_embedding_search_context


def generate_response(query):
    system_prompt = f"""The user wants to learn through the podcast they listen to since they
    trust the podcast as a source of information. Provide a response based on the
    context provided from the podcast's show notes only. If you cannot, answer with a 'I do not know'. 
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

