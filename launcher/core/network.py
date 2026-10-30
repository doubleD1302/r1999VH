"""
launcher/core/network.py
Quản lý giao tiếp mạng, kiểm tra bản cập nhật mới trên GitHub Releases,
hỗ trợ kiểm tra wildcard resource_version (*).
"""

import hashlib
import json
import urllib.request
from typing import Dict, Any, Optional

from .config import GITHUB_API_RELEASES_LATEST, LAUNCHER_VERSION

def check_for_updates() -> Optional[Dict[str, Any]]:
    """
    Kiểm tra xem có phiên bản Launcher hoặc Patch mới trên GitHub hay không.
    """
    try:
        req = urllib.request.Request(
            GITHUB_API_RELEASES_LATEST,
            headers={"User-Agent": "Reverse1999-VietHoa-Launcher"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                remote_tag = data.get("tag_name", "").lstrip("v")
                
                # So sánh phiên bản
                if remote_tag and remote_tag != LAUNCHER_VERSION:
                    return {
                        "has_update": True,
                        "new_version": remote_tag,
                        "release_name": data.get("name", remote_tag),
                        "release_notes": data.get("body", ""),
                        "assets": data.get("assets", [])
                    }
    except Exception as e:
        print(f"[NETWORK] Kiểm tra cập nhật thất bại: {e}")
        
    return None

def verify_file_sha256(file_path, expected_hash: str) -> bool:
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest().lower() == expected_hash.lower()
