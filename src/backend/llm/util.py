from pathlib import Path


def is_local_path(path: str) -> bool:
    p = Path(path)
    return p.exists()
