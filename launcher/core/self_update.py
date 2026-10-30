"""
launcher/core/self_update.py
Cơ chế tự động cập nhật trực tiếp (Seamless In-App Self-Update) cho Reverse: 1999 Windows Launcher.
Tuân thủ quy chuẩn kỹ thuật 4 bước xử lý File Lock của Windows:
1. Ghi nhận parent_pid.
2. Helper đợi và kết liễu cha (taskkill /F /PID <parent_pid>).
3. Đổi tên trước khi ghi đè (rename-before-replace sang .old_uuid).
4. Khởi chạy tiến trình mới độc lập.
"""

import os
import subprocess
import sys
import uuid
from pathlib import Path

HELPER_SCRIPT_TEMPLATE = '''
import os
import sys
import time
import subprocess
from pathlib import Path

parent_pid = int(sys.argv[1])
old_exe = Path(sys.argv[2])
new_exe = Path(sys.argv[3])

# 1. Đợi tiến trình cha thoát hoặc cưỡng chế dừng sau 3s
time.sleep(1.0)
try:
    subprocess.run(["taskkill", "/F", "/PID", str(parent_pid)], capture_output=True)
except Exception:
    pass

time.sleep(0.5)

# 2. Rename-before-replace (Đổi tên file cũ sang uuid rồi chuyển file mới vào)
temp_old = old_exe.with_suffix(f".old_{uuid.uuid4().hex[:8]}")
try:
    if old_exe.exists():
        old_exe.rename(temp_old)
    new_exe.rename(old_exe)
    if temp_old.exists():
        try:
            temp_old.unlink()
        except Exception:
            pass
except Exception as e:
    print(f"Lỗi thay thế file: {e}", file=sys.stderr)
    sys.exit(1)

# 3. Khởi chạy launcher mới
subprocess.Popen([str(old_exe)])
sys.exit(0)
'''

def trigger_self_update(downloaded_new_exe: Path) -> bool:
    """
    Kích hoạt tiến trình helper để cập nhật tự động.
    """
    current_exe = Path(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]).resolve()
    parent_pid = os.getpid()

    helper_py = downloaded_new_exe.parent / "update_helper.py"
    helper_py.write_text(HELPER_SCRIPT_TEMPLATE, encoding="utf-8")

    cmd = [
        sys.executable,
        str(helper_py),
        str(parent_pid),
        str(current_exe),
        str(downloaded_new_exe)
    ]

    print(f"[SELF-UPDATE] Đang kích hoạt Helper cập nhật tự động cho PID={parent_pid}...")
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    sys.exit(0)
