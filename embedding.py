import ollama
from chunking import create_podcast_chunks

podcast_name = "seenunseen"
model = "qwen3-embedding:4b"


def create_embedded_podcast_chunks(podcast_name):
    podcast_chunks = create_podcast_chunks(podcast_name)
    podcast_text_to_be_embeded = [
        podcast_chunk.get("text_to_embed") for podcast_chunk in podcast_chunks
    ]

    podcast_text_embeddings = ollama.embed(
        model=model, input=podcast_text_to_be_embeded
    )

    embedded_podcast_chunks = [
        {**podcast_chunk, "text_embedding": podcast_text_embedding}
        for podcast_chunk, podcast_text_embedding in zip(
            podcast_chunks, podcast_text_embeddings
        )
    ]
    return embedded_podcast_chunks
