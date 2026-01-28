from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
import json
from postgres import Postgres

load_dotenv()


class Scraper:
    def __init__(self):
        self.headers = json.loads(os.getenv("headers"))
        self.podcast_sitemap_url = os.getenv("podcast_sitemap_url")
        self.browser = os.getenv("browser")

    def _create_driver(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.self.browser(options=options)
        return driver

    def get_episode_links(self, parser):
        response = requests.get(self.podcast_sitemap_url, headers=self.headers)
        soup = BeautifulSoup(response.text, parser)
        urls = soup.find_all("url")
        episodes = [
            {"url": url.find("loc").text, "sitemap_date": url.find("lastmod").text}
            for url in urls
            if "https://seenunseen.in/episodes" in url.find("loc").text
        ]
        return episodes

    # should return a dictionary
    def get_episode_details(self, episode_urls):
        driver = self._create_driver()
        episodes_data = []
        counter = 0
        for url in episode_urls:
            driver.implicitly_wait(5)
            driver.get(url)
            title_element = driver.find_element(By.TAG_NAME, "h1")
            time_element = driver.find_element(By.CSS_SELECTOR, ".entry-date.published")
            show_notes_element = driver.find_element(By.CLASS_NAME, "entry-content")
            episode_data = f"""'title': {title_element.text}\n
                'date': {time_element.get_attribute("datetime")}\n
                'show_notes': {show_notes_element.text}\n
                """
            counter += 1
            print(f"Percentage Done: {(counter * 100) / len(episode_urls)}")
            episodes_data.append(episode_data)


class Validator:
    def __init__(self, episodes):
        self.episodes = episodes
        self.pg = Postgres()

    def update_episodes(self):
        stored_episodes = self.pg.get_all_episodes()
        for episode in self.episodes:
            if episode["link"] in [stored_episode["link"] in stored_episodes]:
                return "links"
