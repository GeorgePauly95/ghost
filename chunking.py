import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import extract_episode_number, extract_episode_title

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200, chunk_overlap=200, length_function=len, is_separator_regex=False
)


def _get_episode_metadata(episode):
    episode_number_and_title = episode.get("title")
    title = extract_episode_title(episode_number_and_title)
    episode_number = extract_episode_number(episode_number_and_title)
    episode_metadata = {
        "title": title,
        "date": episode.get("date"),
        "link": episode.get("link"),
        "episode_number": float(episode_number),
    }
    return episode_metadata


def _stringify_episode_metadata(episode_metadata):
    return (
        f"This is episode {episode_metadata['episode_number']}, titled {episode_metadata['title']}. "
        f"It was published on {episode_metadata['date']}. The link to the episode is {episode_metadata['link']}"
    )


def _create_episode_chunks(episode):
    episode_metadata = _get_episode_metadata(episode)
    show_notes = episode.get("show_notes")
    metadata_string = _stringify_episode_metadata(episode_metadata)
    if show_notes is None:
        return [
            {
                **episode_metadata,
                "text_to_embed": f"{metadata_string}",
            }
        ]
    show_notes_chunks = splitter.split_text(show_notes)
    episode_chunks = []
    for show_notes_chunk in show_notes_chunks:
        episode_chunk = {
            **episode_metadata,
            "text_to_embed": f"{metadata_string}\n\n{show_notes_chunk}",
        }
        episode_chunks.append(episode_chunk)
    return episode_chunks


def create_podcast_chunks(episodes):
    podcast_chunks = []
    for episode in episodes:
        podcast_chunks += _create_episode_chunks(episode)
    return podcast_chunks
