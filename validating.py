def validate_episodes(db, episodes):
    stored_episodes = db.get_all_episodes()
    stored_episodes = {
        stored_episode["link"]: stored_episode["sitemap_date"]
        for stored_episode in stored_episodes
    }
    urls = [episode["url"] for episode in episodes]
    new_urls = [url for url in urls if url not in stored_episodes]
    modified_urls = []
    for episode in episodes:
        if episode["url"] in episodes:
            if episode["sitemap_date"] > stored_episodes[episode["url"]]:
                modified_urls.append(episode["url"])
    return {"new_urls": new_urls, "modified_urls": modified_urls}
