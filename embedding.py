import ollama
from chunking import create_podcast_chunks

podcast_name = "seenunseen"
model = "qwen3-embedding:4b"


# def create_embedded_podcast_chunks(podcast_name):
#     podcast_chunks = create_podcast_chunks(podcast_name)
#     podcast_text_to_be_embeded = [
#         podcast_chunk.get("text_to_embed") for podcast_chunk in podcast_chunks
#     ]
#
#     podcast_text_embeddings = ollama.embed(
#         model=model, input=podcast_text_to_be_embeded
#     )
#
#     embedded_podcast_chunks = [
#         {**podcast_chunk, "text_embedding": podcast_text_embedding.embeddings[0]}
#         for podcast_chunk, podcast_text_embedding in zip(
#             podcast_chunks, podcast_text_embeddings
#         )
#     ]
#     return embedded_podcast_chunks


def create_embedded_episode_chunks(podcast_name):
    episode_chunks = create_podcast_chunks(podcast_name)[0]
    episode_text_to_be_embedded = episode_chunks.get("text_to_embed")
    print(type(episode_text_to_be_embedded))
    episode_text_embeddings = ollama.embed(
        model=model, input=episode_text_to_be_embedded
    ).embeddings[0]
    embedded_episode_chunks = {
        **episode_chunks,
        "text_embedding": episode_text_embeddings,
    }
    return embedded_episode_chunks
