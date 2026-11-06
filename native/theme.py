"""Own a complete control palette; never mix OS-dark surfaces with fixed dark text."""
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
from PySide6 import QtSvg  # Include the SVG image plugin in standalone builds.
from native import resources_rc  # Registers original chevron assets.

TEXT = "#243443"
SURFACE = "#ffffff"
WINDOW = "#eef2f5"

STYLE = """
QWidget {font-family:'Segoe UI';font-size:13px;color:#243443;}
QMainWindow,QToolBar,QMenuBar,QStatusBar {background:#eef2f5;color:#243443;}
QToolBar {border:0;border-bottom:1px solid #becad4;spacing:6px;padding:5px;}
QPushButton,QComboBox,QDoubleSpinBox,QLineEdit {
 background:#ffffff;color:#243443;border:1px solid #91a3b2;border-radius:3px;min-height:27px;
}
QPushButton {padding:2px 11px;}
QPushButton:hover,QToolButton:hover {background:#e5eff8;color:#173e60;border-color:#3979ae;}
QPushButton:pressed,QToolButton:pressed {background:#c9dff1;color:#153a5a;}
QPushButton:focus,QComboBox:focus,QDoubleSpinBox:focus,QTextEdit:focus {border:2px solid #236ba4;}
QPushButton:disabled,QComboBox:disabled,QDoubleSpinBox:disabled {
 background:#e5eaf0;color:#627180;border:1px solid #b8c4ce;
}
QPushButton#analyse {background:#1c608f;color:#ffffff;border-color:#174f77;font-weight:600;}
QPushButton#analyse:hover {background:#174f77;}
QPushButton#run {background:#e3f1e8;color:#165232;border-color:#7b9f89;font-weight:600;}
QPushButton#run:disabled {background:#e5eaf0;color:#627180;border-color:#b8c4ce;}
QToolButton {background:#eef2f5;color:#243443;border:1px solid transparent;padding:4px;}
QComboBox {padding:2px 25px 2px 7px;}
QComboBox::drop-down {background:#e8eef3;border-left:1px solid #b0beca;width:22px;}
QComboBox::down-arrow {image:url(:/owon/down.svg);width:12px;height:8px;}
QDoubleSpinBox::up-arrow {image:url(:/owon/up.svg);width:10px;height:6px;}
QDoubleSpinBox::down-arrow {image:url(:/owon/down.svg);width:10px;height:6px;}
QDoubleSpinBox {padding:2px 20px 2px 6px;}
QDoubleSpinBox::up-button,QDoubleSpinBox::down-button {background:#e8eef3;border-left:1px solid #b0beca;width:18px;}
QComboBox QAbstractItemView,QMenu {background:#ffffff;color:#243443;selection-background-color:#d6e8f6;selection-color:#173e60;}
QMenu::item:selected {background:#d6e8f6;color:#173e60;}
QMenu::item:disabled {color:#627180;}
QMenuBar::item:selected {background:#d6e8f6;color:#173e60;}
QTabWidget::pane {border:1px solid #becad4;background:#f8fafb;}
QTabBar::tab {padding:7px 15px;background:#e5ebf0;color:#394d5e;border:1px solid #b9c6d0;}
QTabBar::tab:selected {background:#ffffff;color:#173e60;border-bottom:3px solid #236ba4;}
QTabBar::tab:hover {background:#edf5fb;}
QTextEdit,QListWidget,QTableWidget {background:#ffffff;color:#243443;selection-background-color:#d6e8f6;selection-color:#173e60;border:1px solid #becad4;}
QHeaderView::section {background:#e8eef3;color:#243443;padding:6px;border:1px solid #c2cdd6;}
QScrollArea,QScrollArea>QWidget>QWidget {background:#f8fafb;border:0;}
QToolTip {background:#fffbe8;color:#243443;border:1px solid #9c9273;padding:5px;}
QLabel#source {color:#715000;background:#fff0c9;padding:5px 10px;font-weight:600;}
QLabel#safety {background:#fff6df;color:#665024;border-bottom:1px solid #dfd0a8;padding:6px 10px;}
QLabel#metrics {font-family:Consolas,'DejaVu Sans Mono';font-size:12px;background:#e7edf2;padding:8px;color:#243443;}
QLabel#state {font-weight:600;color:#165232;padding:3px 0;}
QLabel#hint {color:#42596c;padding:3px 0;}
QSplitter::handle {background:#d4dfe7;}
QSlider::groove:horizontal {background:#c7d3de;height:5px;border-radius:2px;}
QSlider::handle:horizontal {background:#437ba6;border:1px solid #244e70;width:14px;margin:-5px 0;border-radius:3px;}
"""

def configure_theme(app):
    app.setStyle("Fusion")
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    palette = QPalette()
    colors = {
        QPalette.Window: WINDOW, QPalette.WindowText: TEXT,
        QPalette.Base: SURFACE, QPalette.AlternateBase: "#f1f5f8",
        QPalette.ToolTipBase: "#fffbe8", QPalette.ToolTipText: TEXT,
        QPalette.Text: TEXT, QPalette.Button: SURFACE, QPalette.ButtonText: TEXT,
        QPalette.BrightText: "#ffffff", QPalette.Highlight: "#236ba4",
        QPalette.HighlightedText: "#ffffff", QPalette.Link: "#1c608f",
        QPalette.Accent: "#236ba4", QPalette.LinkVisited: "#6552a0",
        QPalette.Light: "#ffffff", QPalette.Midlight: "#e5ebf0",
        QPalette.Mid: "#9aaab7", QPalette.Dark: "#667b8d", QPalette.Shadow: "#34485a",
        QPalette.PlaceholderText: "#657786",
    }
    for group in (QPalette.Active,QPalette.Inactive,QPalette.Disabled):
        for role,color in colors.items():
            palette.setColor(group,role,QColor(color))
    for role in (QPalette.Text,QPalette.ButtonText,QPalette.WindowText):
        palette.setColor(QPalette.Disabled,role,QColor("#627180"))
    for role in (QPalette.Base,QPalette.Button):
        palette.setColor(QPalette.Disabled,role,QColor("#e5eaf0"))
    app.setPalette(palette)
    app.setStyleSheet(STYLE)
