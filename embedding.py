import ollama
import os
from dotenv import load_dotenv

load_dotenv()

embedding_model = os.getenv("embedding_model")


def create_embedding(chunk):
    text_to_embed = chunk.get("text_to_embed")
    text_embedding_object = ollama.embed(model=embedding_model, input=text_to_embed)
    text_embedding = text_embedding_object.embeddings[0]
    embedded_chunk = {
        **chunk,
        "text_embedding": text_embedding,
    }
    return embedded_chunk


def create_embeddings(chunks):
    embedded_chunks = [create_embedding(chunk) for chunk in chunks]
    return embedded_chunks


def create_query_embedding(query_text):
    query_text_embeddings_object = ollama.embed(model=embedding_model, input=query_text)
    query_text_embeddings = query_text_embeddings_object.embeddings[0]
    return query_text_embeddings
