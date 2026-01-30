from scraping import Scraper
from validating import validate_episodes
from chunking import create_podcast_chunks
from embedding import create_embedding
from postgres import Postgres


def sync():
    scraper = Scraper()
    pg = Postgres()
    episodes = scraper.get_episodes()
    validated_episodes = validate_episodes(pg, episodes)
    update_episodes(pg, scraper, validated_episodes)


def update_episodes(db, scraper, validated_episodes):
    modified_urls = validated_episodes["modified_urls"]
    new_urls = validated_episodes["new_urls"]
    if modified_urls == [] and new_urls == []:
        print(
            "No new episodes have been released and past episodes haven't been updated"
        )
    elif modified_urls != [] and new_urls == []:
        db.delete_episodes(modified_urls)
        print(f"The following episodes have been modified: {modified_urls}")
    elif modified_urls == [] and new_urls != []:
        print(f"The following episodes have been released: {new_urls}")
    else:
        print(f"""The following episodes have been modified: {modified_urls}\n\n
                The following episodes have been released: {new_urls}""")
    urls_to_be_scraped = modified_urls + new_urls
    episodes = scraper.get_episode_details(urls_to_be_scraped)
    chunks = create_podcast_chunks(episodes)
    chunk_count = len(chunks)
    counter = 0
    for chunk in chunks:
        embedded_chunk = create_embedding(chunk)
        db.add_episode(embedded_chunk)
        counter += 1
        print(f"Percentage Embedding and Storing done: {(counter * 100) / chunk_count}")
