"""
launcher/core/config.py
Cấu hình hệ thống cho Reverse: 1999 PC Launcher.
"""

from pathlib import Path

LAUNCHER_VERSION = "0.1.0"
GITHUB_REPO = "doubleD1302/r1999VH"
GITHUB_API_RELEASES_LATEST = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# File name quy chuẩn cho Windows Launcher
LAUNCHER_EXE_NAME = f"Reverse1999-Windows_v{LAUNCHER_VERSION}.exe"

# Đường dẫn mặc định
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BACKUPS_DIR = PROJECT_ROOT / "backups"
