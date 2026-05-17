from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def not_found(resource: str, id: str):
    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail=f"{resource} with id '{id}' not found")
