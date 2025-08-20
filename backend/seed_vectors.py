import os
import logging
import argparse
import json

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Force semantic retrieval for this one-off script (doesn't persist)
os.environ.setdefault("USE_SEMANTIC_RETRIEVAL", "true")

from retrieval import init_pgvector, seed_static_kb_from_list, upsert_kb_from_list
from app import LEGAL_KNOWLEDGE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("seed_vectors")


def parse_args():
    parser = argparse.ArgumentParser(description="Seed or upsert legal knowledge into pgvector")
    parser.add_argument("--json", dest="json_path", help="Path to JSON file with items to ingest (list of {title, content, category, keywords?})")
    return parser.parse_args()


def load_items_from_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
        return data["items"]
    if isinstance(data, list):
        return data
    raise SystemExit("JSON must be a list of items or an object with an 'items' array")


def main():
    args = parse_args()
    logger.info("Starting vector store initialization and seeding...")

    if not os.getenv("DATABASE_URL"):
        raise SystemExit("DATABASE_URL not set. Configure backend/.env first.")

    ready = init_pgvector()
    if not ready:
        raise SystemExit("pgvector init failed. Check DATABASE_URL and permissions.")

    if args.json_path:
        items = load_items_from_json(args.json_path)
        logger.info(f"Upserting {len(items)} items from JSON: {args.json_path}")
        attempted = upsert_kb_from_list(items)
        logger.info(f"Upsert attempted for: {attempted} items (existing ids ignored)")
    else:
        inserted = seed_static_kb_from_list(LEGAL_KNOWLEDGE)
        logger.info(f"Seeding complete. Inserted: {inserted}")


if __name__ == "__main__":
    main()
