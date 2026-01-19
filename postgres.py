import psycopg
import os
from pathlib import Path
from dotenv import load_dotenv
from embedding import create_embedded_episode_chunks

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
