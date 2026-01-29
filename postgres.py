import psycopg
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

connection_string = f"dbname={os.getenv('dbname')} user={os.getenv('user')}"
migration_file = os.getenv("migration_file")


class Postgres:
    def __init__(self):
        self.conn = psycopg.connect(connection_string)
        self._migrate()

    def _migrate(self):
        with self.conn.cursor() as cur:
            sql = Path(migration_file).read_text()
            cur.execute(sql)
            self.conn.commit()

    def add_episode(self, episode):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO episodes(link, title, episode_number, date, text_to_embed, text_embedding)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    episode["link"],
                    episode["title"],
                    episode["episode_number"],
                    episode["date"],
                    episode["text_to_embed"],
                    episode["text_embedding"],
                ),
            )
            self.conn.commit()

    def get_all_episodes(self):
        with self.conn.cursor() as cur:
            episodes = cur.execute("SELECT DISTINCT link, sitemap_date FROM episodes;")
            episodes = episodes.fetchall()
            episodes = [
                {"link": episode[0], "sitemap_date": episode[1]} for episode in episodes
            ]
            return episodes

    def delete_episodes(self, episodes):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM episodes WHERE link = ANY(%s)",
                (episodes,),
            )
            self.conn.commit()

    def text_search(self, text):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT text_to_embed FROM episodes WHERE to_tsvector('english', text_to_embed)
                    @@ websearch_to_tsquery('english', %s);
                """,
                (text,),
            )
            return cur.fetchall()

    def embedding_search(self, embedding):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT text_to_embed FROM episodes ORDER BY text_embedding <=> (%s)::halfvec LIMIT 15
                """,
                (embedding,),
            )
            return cur.fetchall()
