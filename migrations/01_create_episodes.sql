CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS episodes (
  id SERIAL PRIMARY KEY,
  link TEXT NOT NULL,
  title TEXT NOT NULL,
  episode_number NUMERIC(10,2),
  date TIMESTAMPTZ,
  text_to_embed TEXT,
  text_embedding HALFVEC(2560)
);

CREATE INDEX IF NOT EXISTS idx_episodes_text_search
ON episodes USING GIN (to_tsvector('english', text_to_embed));

CREATE INDEX IF NOT EXISTS idx_episodes_embedding
ON episodes USING HNSW (text_embedding halfvec_cosine_ops);
