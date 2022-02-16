from pathlib import Path

import timtools.locations

PROJECT_DIR: Path = Path(__file__).parent.parent
CACHE_DIR: Path = timtools.locations.get_user_cache_dir() / "googletools"

CONFIG_DIR: Path = timtools.locations.get_user_config_dir() / "googletools"
if not CONFIG_DIR.is_dir():
    code_src_config_dir: Path = PROJECT_DIR / "config"
    if code_src_config_dir.is_dir():
        CONFIG_DIR = code_src_config_dir

GOOGLE_CLIENT_SECRET_FILE: Path = CONFIG_DIR / "client_secret.json"
