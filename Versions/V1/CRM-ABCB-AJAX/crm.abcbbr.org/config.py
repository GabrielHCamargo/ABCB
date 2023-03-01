import os.path

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 3600,
    "pool_pre_ping": True,
}

SECRET_KEY = "33fcbcd394a5314d4dfc964eb21680ae886dd8bfeb301e24340e1712671c29b6"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "upload", "D.SUB.GER.151")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "upload", "D.SUB.GER.151", "EXPORTED")
DOCUMENT_FOLDER = os.path.join(BASE_DIR, "app", "static", "upload", "DATA", "DOCUMENT")
MAX_CONTENT_LENGTH = 16 * 1000 * 1000

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"