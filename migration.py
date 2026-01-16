import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def run_migration(connection_string, migration_file):
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            sql = Path(migration_file).read_text()
            cur.execute(sql)
            conn.commit()


connection_string = f"dbname={os.getenv('dbname')} user={os.getenv('user')}"
migration_file = "migrations/01_create_episodes.sql"
run_migration(connection_string, migration_file)
