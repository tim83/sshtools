from pathlib import Path

PROJECT_DIR = Path(__file__).parent

src_config_dir = PROJECT_DIR.parent / "config"
user_config_dir = Path.home() / ".config/sshtools"
CONFIG_DIR: Path
if user_config_dir.is_dir():
    CONFIG_DIR = user_config_dir
else:
    CONFIG_DIR = src_config_dir
