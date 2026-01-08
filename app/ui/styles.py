# app/ui/styles.py

DARK_THEME_QSS = """
/* Global Styles */
QMainWindow {
    background-color: #2b2b2b;
}

QWidget {
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', 'Helvetica', sans-serif;
    font-size: 14px;
}

/* Sidebar (QTreeView) */
QTreeView {
    background-color: #222222;
    border: none;
    padding: 5px;
}

QTreeView::item {
    height: 30px;
    padding: 2px;
}

QTreeView::item:hover {
    background-color: #333333;
    border-radius: 4px;
}

QTreeView::item:selected {
    background-color: #4facfe;
    color: white;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #333333;
    color: #cccccc;
    border: none;
    padding: 5px;
}

/* Sidebar Header */
#sidebarHeader {
    background-color: #333333;
    color: #ffffff;
    padding: 10px;
    font-weight: bold;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #2b2b2b;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #555555;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Content Area */
QLabel {
    color: #e0e0e0;
}

/* Buttons */
QPushButton {
    background-color: #3a3a3a;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 12px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #4a4a4a;
    border-color: #4facfe;
}

QPushButton:pressed {
    background-color: #4facfe;
    color: white;
}

/* Sliders */
QSlider::groove:horizontal {
    border: 1px solid #3a3a3a;
    height: 2px; /* Very thin */
    background: #202020;
    margin: 0px 0;
    border-radius: 1px;
}

QSlider::handle:horizontal {
    background: #4facfe;
    border: 1px solid #4facfe;
    width: 10px;
    height: 10px;
    margin: -5px 0; /* Center alignment: (10 - 2)/2 + 1 adjustment approx -4 or -5 */
    border-radius: 5px;
}

QSlider::handle:horizontal:hover {
    background: #66b3ff;
    width: 12px;
    height: 12px;
    margin: -6px 0;
    border-radius: 6px;
}

/* Text Editor */
QTextEdit {
    background-color: #1e1e1e;
    color: #dcdcdc;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 5px;
}

/* Dock Widget */
QDockWidget::title {
    text-align: left;
    background: #222222;
    padding-left: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
}

/* Menu Bar */
QMenuBar {
    background-color: #2b2b2b;
}

QMenuBar::item:selected {
    background-color: #4facfe;
}

QMenu {
    background-color: #2b2b2b;
    border: 1px solid #444444;
}

QMenu::item:selected {
    background-color: #4facfe;
}

/* Dialogs and Popups */
QDialog, QMessageBox {
    background-color: #2b2b2b;
    color: #e0e0e0;
}

QMessageBox QLabel {
    color: #e0e0e0;
}

QFileDialog {
    background-color: #2b2b2b;
}

QFileDialog QListView, QFileDialog QTreeView {
    background-color: #222222;
    color: #e0e0e0;
}

QFileDialog QLineEdit {
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #444444;
    padding: 4px;
    border-radius: 4px;
}

QFileDialog QComboBox {
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #444444;
    padding: 4px;
    border-radius: 4px;
}

QFileDialog QComboBox::drop-down {
    border: none;
}

QFileDialog QComboBox QAbstractItemView {
    background-color: #2b2b2b;
    color: #e0e0e0;
    selection-background-color: #4facfe;
}
"""

LIGHT_THEME_QSS = """
/* Global Styles */
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    color: #333333;
    font-family: 'Segoe UI', 'Roboto', 'Helvetica', sans-serif;
    font-size: 14px;
}

/* Sidebar (QTreeView) */
QTreeView {
    background-color: #ffffff;
    border: none;
    padding: 5px;
}

QTreeView::item {
    height: 30px;
    padding: 2px;
}

QTreeView::item:hover {
    background-color: #e8e8e8;
    border-radius: 4px;
}

QTreeView::item:selected {
    background-color: #4facfe;
    color: white;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #e0e0e0;
    color: #333333;
    border: none;
    padding: 5px;
}

/* Sidebar Header */
#sidebarHeader {
    background-color: #e0e0e0;
    color: #333333;
    padding: 10px;
    font-weight: bold;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Content Area */
QLabel {
    color: #333333;
}

/* Buttons */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 6px 12px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #e8e8e8;
    border-color: #4facfe;
}

QPushButton:pressed {
    background-color: #4facfe;
    color: white;
}

/* Sliders */
QSlider::groove:horizontal {
    border: 1px solid #cccccc;
    height: 2px;
    background: #e0e0e0;
    margin: 0px 0;
    border-radius: 1px;
}

QSlider::handle:horizontal {
    background: #4facfe;
    border: 1px solid #4facfe;
    width: 10px;
    height: 10px;
    margin: -5px 0;
    border-radius: 5px;
}

QSlider::handle:horizontal:hover {
    background: #66b3ff;
    width: 12px;
    height: 12px;
    margin: -6px 0;
    border-radius: 6px;
}

/* Text Editor */
QTextEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
}

/* Dock Widget */
QDockWidget::title {
    text-align: left;
    background: #e0e0e0;
    padding-left: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
}

/* Menu Bar */
QMenuBar {
    background-color: #f5f5f5;
}

QMenuBar::item:selected {
    background-color: #4facfe;
    color: white;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #cccccc;
}

QMenu::item:selected {
    background-color: #4facfe;
    color: white;
}

/* Dialogs and Popups */
QDialog, QMessageBox {
    background-color: #f5f5f5;
    color: #333333;
}

QMessageBox QLabel {
    color: #333333;
}

QFileDialog {
    background-color: #f5f5f5;
}

QFileDialog QListView, QFileDialog QTreeView {
    background-color: #ffffff;
    color: #333333;
}

QFileDialog QLineEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #cccccc;
    padding: 4px;
    border-radius: 4px;
}

QFileDialog QComboBox {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #cccccc;
    padding: 4px;
    border-radius: 4px;
}

QFileDialog QComboBox::drop-down {
    border: none;
}

QFileDialog QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #333333;
    selection-background-color: #4facfe;
    selection-color: white;
}
"""

# Theme dictionary for easy access
THEMES = {
    "dark": DARK_THEME_QSS,
    "light": LIGHT_THEME_QSS,
}

