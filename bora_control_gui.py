import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QCheckBox, QColorDialog, QMessageBox,
    QRadioButton, QButtonGroup, QGroupBox, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from bora_control.config import get_base_config
from bora_control.utils import BoraControl

class BoraControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bora Control Utility (258a:0016)")
        self.setFixedSize(450, 480)

        self.config = get_base_config()
        self.current_color = QColor(255, 255, 255) # default white

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)

        # 1. Animation Dropdown
        self.anim_layout = QHBoxLayout()
        self.anim_label = QLabel("Animation:")
        self.anim_combo = QComboBox()
        self.animations = [
            "retro_snake", "neon_stream", "reaction", "sine_wave",
            "steady", "breathing", "rainbow", "flash_away",
            "raindrops", "rainbow_wheel", "ripples_shining",
            "stars_twinkle", "shadow_disappear"
        ]
        self.anim_combo.addItems([a.replace("_", " ").title() for a in self.animations])
        self.anim_combo.wheelEvent = lambda e: None # Prevent accidental scroll wheel changes
        self.anim_layout.addWidget(self.anim_label)
        self.anim_layout.addWidget(self.anim_combo)
        self.layout.addLayout(self.anim_layout)

        # 2. Brightness Radio Buttons (1 to 4)
        self.bright_group_box = QGroupBox("Brightness")
        self.bright_layout = QHBoxLayout()
        self.bright_group = QButtonGroup(self)
        brightness_levels = [("25%", 1), ("50%", 2), ("75%", 3), ("100%", 4)]
        for text, val in brightness_levels:
            rb = QRadioButton(text)
            self.bright_group.addButton(rb, val)
            self.bright_layout.addWidget(rb)
        self.bright_group.button(4).setChecked(True) # default 100%
        self.bright_group_box.setLayout(self.bright_layout)
        self.layout.addWidget(self.bright_group_box)

        # 3. Speed Radio Buttons (1 to 5)
        self.speed_group_box = QGroupBox("Speed")
        self.speed_layout = QHBoxLayout()
        self.speed_group = QButtonGroup(self)
        for i in range(1, 6):
            rb = QRadioButton(str(i))
            self.speed_group.addButton(rb, i)
            self.speed_layout.addWidget(rb)
        self.speed_group.button(3).setChecked(True) # default 3
        self.speed_group_box.setLayout(self.speed_layout)
        self.layout.addWidget(self.speed_group_box)

        # 4. Color Picker
        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Global Color:")
        self.color_btn = QPushButton("Pick Color")
        self.update_color_btn_style()
        self.color_btn.clicked.connect(self.pick_color)
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_btn)
        self.layout.addLayout(self.color_layout)

        # 5. Rainbow Mode Checkbox
        self.rainbow_cb = QCheckBox("Enable Hardware Rainbow Mode (Overrides Color)")
        self.layout.addWidget(self.rainbow_cb)

        # 6. Generated CLI Command
        self.cli_layout = QVBoxLayout()
        self.cli_label = QLabel("Generated CLI Command:")
        self.cli_text = QLineEdit()
        self.cli_text.setReadOnly(True)
        self.cli_layout.addWidget(self.cli_label)
        self.cli_layout.addWidget(self.cli_text)
        self.layout.addLayout(self.cli_layout)

        # 7. Apply Button
        self.apply_btn = QPushButton("Apply Configuration")
        self.apply_btn.setMinimumHeight(40)
        self.apply_btn.clicked.connect(self.apply_config)
        self.layout.addStretch()
        self.layout.addWidget(self.apply_btn)

        # Initialize Signals for CLI text updates
        self.anim_combo.currentIndexChanged.connect(self.update_cli_command)
        self.bright_group.buttonToggled.connect(self.update_cli_command)
        self.speed_group.buttonToggled.connect(self.update_cli_command)
        self.rainbow_cb.toggled.connect(self.update_cli_command)

        # Initialize CLI text
        self.update_cli_command()

    def update_color_btn_style(self):
        r, g, b, _ = self.current_color.getRgb()
        luminance = (0.299*r + 0.587*g + 0.114*b) / 255
        text_color = "black" if luminance > 0.5 else "white"
        self.color_btn.setStyleSheet(f"background-color: rgb({r}, {g}, {b}); color: {text_color}; font-weight: bold;")

    def pick_color(self):
        color = QColorDialog.getColor(self.current_color, self, "Pick Keyboard Color")
        if color.isValid():
            self.current_color = color
            self.update_color_btn_style()
            self.update_cli_command()

    def update_cli_command(self):
        anim = self.animations[self.anim_combo.currentIndex()]
        speed = self.speed_group.checkedId()
        bright = self.bright_group.checkedId()
        r = self.current_color.red()
        g = self.current_color.green()
        b = self.current_color.blue()

        cmd = f"sudo venv/bin/python bora_control.py -an {anim} -sp {speed} -br {bright} -r {r} -g {g} -b {b}"
        if self.rainbow_cb.isChecked():
            cmd += " -rb"

        self.cli_text.setText(cmd)
        # Move cursor to beginning so user sees the start
        self.cli_text.setCursorPosition(0)

    def apply_config(self):
        try:
            self.apply_btn.setText("Applying...")
            QApplication.processEvents()

            var = {
                'animation': self.animations[self.anim_combo.currentIndex()],
                'speed': self.speed_group.checkedId(),
                'brightness': self.bright_group.checkedId(),
                'red': self.current_color.red(),
                'green': self.current_color.green(),
                'blue': self.current_color.blue(),
                'rainbow': self.rainbow_cb.isChecked(),
                'sleep': 5
            }

            self.config.update(var)
            rk = BoraControl(0x258a, 0x0016)
            rk.apply_config(self.config)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply configuration:\n{str(e)}\n\nMake sure you run this script as root (sudo).")
        finally:
            self.apply_btn.setText("Apply Configuration")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = BoraControlGUI()
    window.show()
    sys.exit(app.exec())
