import ollama
import os
from dotenv import load_dotenv
from chunking import create_podcast_chunks

load_dotenv()

podcast_name = os.getenv("podcast_name")
embedding_model = os.getenv("embedding_model")


def create_embedded_podcast_chunks(podcast_name):
    podcast_chunks = create_podcast_chunks(podcast_name)
    podcast_text_to_be_embeded = [
        podcast_chunk.get("text_to_embed") for podcast_chunk in podcast_chunks
    ]

    podcast_text_embeddings = ollama.embed(
        model=embedding_model, input=podcast_text_to_be_embeded
    )

    embedded_podcast_chunks = [
        {**podcast_chunk, "text_embedding": podcast_text_embedding.embeddings[0]}
        for podcast_chunk, podcast_text_embedding in zip(
            podcast_chunks, podcast_text_embeddings
        )
    ]
    return embedded_podcast_chunks


def create_embedded_episode_chunks(podcast_name):
    episode_chunks = create_podcast_chunks(podcast_name)[7]
    episode_text_to_be_embedded = episode_chunks.get("text_to_embed")
    episode_text_embeddings_object = ollama.embed(
        model=embedding_model, input=episode_text_to_be_embedded
    )
    episode_text_embeddings = episode_text_embeddings_object.embeddings[0]
    embedded_episode_chunks = {
        **episode_chunks,
        "text_embedding": episode_text_embeddings,
    }
    return embedded_episode_chunks


def create_query_embedding(query_text):
    query_text_embeddings_object = ollama.embed(model=embedding_model, input=query_text)
    query_text_embeddings = query_text_embeddings_object.embeddings[0]
    return query_text_embeddings
