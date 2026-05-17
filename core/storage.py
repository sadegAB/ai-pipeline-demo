import json
import uuid
from pathlib import Path

DB_PATH = Path("db.json")


def load_db() -> dict:
    if not DB_PATH.exists():
        save_db({})
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_db(data: dict) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


def generate_id() -> str:
    return str(uuid.uuid4())
