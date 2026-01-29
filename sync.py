from scraping import Scraper
from validating import validate_episodes
from postgres import Postgres
from chunking import create_podcast_chunks
from embedding import create_embedding


def sync():
    scraper = Scraper()
    pg = Postgres()
    episodes = scraper.get_episodes()
    validated_episodes = validate_episodes(pg, episodes)
    modified_episodes = validated_episodes["modified_urls"]
    pg.delete_episodes(modified_episodes)
    urls_to_be_scraped = modified_episodes + validated_episodes["new_urls"]
    episodes = scraper.get_episode_details(urls_to_be_scraped)
    print(f"Episodes are: {episodes}")
    chunks = create_podcast_chunks(episodes)
    chunk_count = len(chunks)
    counter = 0
    for chunk in chunks:
        embedded_chunk = create_embedding(chunk)
        pg.add_episode(embedded_chunk)
        counter += 1
        print(f"Percentage Embedding and Storing done: {(counter * 100) / chunk_count}")


sync()
