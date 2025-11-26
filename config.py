import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "lifesphere.db"

class Config:
    SECRET_KEY = os.environ.get("LIFESPHERE_SECRET", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
