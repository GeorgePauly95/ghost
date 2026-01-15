import psycopg
import os

connection_string = f"dbname={os.getenv('dbname')} user={os.getenv('user')}"
