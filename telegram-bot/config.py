import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file(env_path: Path) -> None:
    """Load simple KEY=VALUE pairs from a local .env file."""
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def resolve_storage_path(raw_value: str | None, default_path: Path) -> Path:
    if not raw_value:
        return default_path

    candidate = Path(raw_value).expanduser()
    if candidate.is_absolute():
        return candidate
    return (BASE_DIR / candidate).resolve()


def resolve_data_dir() -> Path:
    explicit = os.getenv("DATA_DIR")
    if explicit:
        return resolve_storage_path(explicit, BASE_DIR / "data")

    preferred = BASE_DIR / "data"
    legacy_db = BASE_DIR / "service_logs.db"

    if preferred.exists() or not legacy_db.exists():
        return preferred

    return BASE_DIR


load_env_file(ENV_FILE)

DATA_DIR = resolve_data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = resolve_storage_path(os.getenv("DB_PATH"), DATA_DIR / "service_logs.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

EXPORT_DIR = resolve_storage_path(os.getenv("EXPORT_DIR"), DATA_DIR / "exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
