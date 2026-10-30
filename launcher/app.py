"""
launcher/app.py
Giao diện đồ họa PC Launcher cho Reverse: 1999 Việt Hóa (PySide6).
"""

import sys
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar, QMessageBox
)

from core.config import LAUNCHER_VERSION, GITHUB_REPO
from core.game_detection import detect_reverse1999_installation
from core.installer import install_patch
from core.network import check_for_updates

class UpdateCheckerThread(QThread):
    update_found = Signal(dict)

    def run(self):
        result = check_for_updates()
        if result and result.get("has_update"):
            self.update_found.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Reverse: 1999 — Trình Khởi Chạy Việt Hóa v{LAUNCHER_VERSION}")
        self.resize(750, 480)
        self.game_path = detect_reverse1999_installation()
        self.init_ui()
        self.start_update_check()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Tiêu đề
        title_label = QLabel("REVERSE: 1999 — BẢN VIỆT HÓA LIGHT NOVEL")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Trạng thái game
        self.status_label = QLabel()
        if self.game_path:
            self.status_label.setText(f"✓ Đã tìm thấy game: {self.game_path}")
            self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.status_label.setText("✗ Chưa phát hiện thư mục cài đặt game Reverse: 1999")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(self.status_label)

        # Log hiển thị
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.append("Chào mừng bạn đến với bản Việt Hóa Reverse: 1999 phong cách Light Novel!")
        self.log_box.append(f"Kho lưu trữ GitHub: https://github.com/{GITHUB_REPO}")
        self.log_box.append("—" * 50)
        layout.addWidget(self.log_box)

        # Nút chức năng
        btn_layout = QHBoxLayout()
        self.install_btn = QPushButton("Cài Đặt / Cập Nhật Việt Hóa")
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; font-weight: bold;
                padding: 12px; border-radius: 6px; font-size: 14px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.install_btn.clicked.connect(self.on_install_clicked)
        btn_layout.addWidget(self.install_btn)

        self.launch_btn = QPushButton("Vào Game (Khởi Chạy)")
        self.launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; font-weight: bold;
                padding: 12px; border-radius: 6px; font-size: 14px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.launch_btn.clicked.connect(self.on_launch_clicked)
        btn_layout.addWidget(self.launch_btn)

        layout.addLayout(btn_layout)

    def start_update_check(self):
        self.checker_thread = UpdateCheckerThread()
        self.checker_thread.update_found.connect(self.on_update_found)
        self.checker_thread.start()

    def on_update_found(self, update_info):
        new_ver = update_info.get("new_version")
        self.log_box.append(f"\n[THÔNG BÁO] Đã có phiên bản cập nhật mới v{new_ver} trên GitHub!")
        self.log_box.append(f"Nội dung: {update_info.get('release_notes')}")
        QMessageBox.information(
            self,
            "Cập Nhật Mới",
            f"Phát hiện bản cập nhật mới: v{new_ver}\n"
            f"Bấm OK để tự động tải và cập nhật trực tiếp!"
        )

    def on_install_clicked(self):
        if not self.game_path:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy thư mục cài đặt game để cài đặt!")
            return
        
        self.log_box.append("[TIẾN TRÌNH] Bắt đầu cài đặt bản dịch...")
        success = install_patch(self.game_path)
        if success:
            self.log_box.append("[THÀNH CÔNG] Đã cài đặt bản Việt Hóa hoàn tất!")
            QMessageBox.information(self, "Thành Công", "Đã cài đặt bản Việt Hóa thành công!")
        else:
            self.log_box.append("[LỖI] Cài đặt thất bại hoặc chưa có file patch trong dist/.")

    def on_launch_clicked(self):
        if not self.game_path:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy game để khởi chạy!")
            return
        
        import subprocess
        exe_path = self.game_path / "reverse1999.exe"
        if exe_path.exists():
            subprocess.Popen([str(exe_path)], cwd=str(self.game_path))
            self.log_box.append("[KHỞI CHẠY] Đã mở game Reverse: 1999!")
        else:
            QMessageBox.critical(self, "Lỗi", f"Không tìm thấy file: {exe_path}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
