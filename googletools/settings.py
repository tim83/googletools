from pathlib import Path

import xdg

PROJECT_DIR: Path = Path(__file__).parent.parent
CACHE_DIR: Path = xdg.xdg_cache_home() / "googletools"

CONFIG_DIR: Path = xdg.xdg_config_home() / "googletools"
if not CONFIG_DIR.is_dir():
    code_src_config_dir: Path = PROJECT_DIR / "config"
    if code_src_config_dir.is_dir():
        CONFIG_DIR = code_src_config_dir

GOOGLE_CLIENT_SECRET_FILE: Path = CONFIG_DIR / "client_secret.json"
