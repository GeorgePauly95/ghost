from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


df = pd.read_csv("episode_links.csv")
episode_urls = list(df["0"])


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

episodes_data = []
counter = 0
for url in episode_urls:
    driver.implicitly_wait(5)

    driver.get(url)

    title_element = driver.find_element(By.TAG_NAME, "h1")
    print(url)
    time_element = driver.find_element(By.CSS_SELECTOR, ".entry-date.published")
    show_notes_element = driver.find_element(By.CLASS_NAME, "entry-content")
    episode_data = f"""'title': {title_element.text}\n
        'date': {time_element.get_attribute("datetime")}\n
        'show_notes': {show_notes_element.text}\n
        """
    counter += 1
    print(f"Percentage Done: {(counter * 100) / len(episode_urls)}")
    episodes_data.append(episode_data)


driver.quit()

df = pd.Series(episodes_data)
df.to_csv("episodes_data.csv")
