from bs4 import BeautifulSoup
import requests
import pandas

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
response = requests.get("https://seenunseen.in/sitemap.xml", headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
links = [link_tag.text for link_tag in soup.find_all("loc")]


def get_episode_link(link):
    if "episodes" in link:
        return True
    return False


episode_links = list(filter(get_episode_link, links))

df = pandas.Series(episode_links)

df.to_csv("episode_links.csv")

