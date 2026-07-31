import os
from pathlib import Path

# Ensure project root is the working directory for storage/* relative paths.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'app.db'}")
if DATABASE_URL.startswith("sqlite:///"):
    db_path = Path(DATABASE_URL.replace("sqlite:///", "", 1))
    if not db_path.is_absolute():
        db_path = PROJECT_ROOT / db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    DATABASE_PATH = str(db_path)
else:
    DATABASE_PATH = str(PROJECT_ROOT / "data" / "app.db")

AUTH_USER = os.getenv("PROPHITBET_USER", "admin")
AUTH_PASSWORD = os.getenv("PROPHITBET_PASSWORD", "changeme")
AUTH_DISABLED = os.getenv("PROPHITBET_AUTH_DISABLED", "").lower() in {"1", "true", "yes"}

SECRET_KEY = os.getenv("PROPHITBET_SECRET", "prophitbet-dev-secret")

# Optional URL prefix when reverse-proxied (e.g. "/prophitbet" on gibbonsai.com).
ROOT_PATH = os.getenv("ROOT_PATH", "").rstrip("/")


def app_url(path: str = "/") -> str:
    """Build an absolute app path including ROOT_PATH."""
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{ROOT_PATH}{path}"
