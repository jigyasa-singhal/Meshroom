from PySide6.QtCore import QObject, Qt, Slot, Property, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class PaletteManager(QObject):
    """
    Manages QApplication's palette and provides Dark, Light and Default themes.
    """
    paletteChanged = Signal()

    def __init__(self, qmlEngine, parent=None):
        super().__init__(parent)
        self.qmlEngine = qmlEngine

        # ---------- DARK PALETTE ----------
        darkPalette = QPalette()
        window = QColor(50, 52, 55)
        text = QColor(200, 200, 200)
        disabledText = text.darker(170)
        base = window.darker(150)
        button = window.lighter(115)
        highlight = QColor(42, 130, 218)

        darkPalette.setColor(QPalette.Window, window)
        darkPalette.setColor(QPalette.WindowText, text)
        darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, disabledText)
        darkPalette.setColor(QPalette.Base, base)
        darkPalette.setColor(QPalette.AlternateBase, QColor(46, 47, 48))
        darkPalette.setColor(QPalette.ToolTipBase, base)
        darkPalette.setColor(QPalette.ToolTipText, text)
        darkPalette.setColor(QPalette.Text, text)
        darkPalette.setColor(QPalette.Disabled, QPalette.Text, disabledText)
        darkPalette.setColor(QPalette.Button, button)
        darkPalette.setColor(QPalette.ButtonText, text)
        darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, disabledText)
        darkPalette.setColor(QPalette.Mid, button.lighter(120))
        darkPalette.setColor(QPalette.Highlight, highlight)
        darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.Shadow, Qt.black)
        darkPalette.setColor(QPalette.Link, highlight.lighter(130))
        self.darkPalette = darkPalette

        # ---------- LIGHT PALETTE ----------
        lightPalette = QPalette()
        lightPalette.setColor(QPalette.Window, Qt.white)
        lightPalette.setColor(QPalette.WindowText, Qt.black)
        lightPalette.setColor(QPalette.Base, QColor(245, 245, 245))
        lightPalette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
        lightPalette.setColor(QPalette.ToolTipBase, Qt.white)
        lightPalette.setColor(QPalette.ToolTipText, Qt.black)
        lightPalette.setColor(QPalette.Text, Qt.black)
        lightPalette.setColor(QPalette.Button, QColor(240, 240, 240))
        lightPalette.setColor(QPalette.ButtonText, Qt.black)
        lightPalette.setColor(QPalette.Highlight, QColor(0, 120, 215))  # blue
        lightPalette.setColor(QPalette.HighlightedText, Qt.white)
        self.lightPalette = lightPalette

        # ---------- DEFAULT PALETTE ----------
        self.defaultPalette = QApplication.instance().palette()

        # Start with default
        self.currentTheme = "default"
        QApplication.instance().setPalette(self.defaultPalette)

    # ---------- THEME SWITCHER ----------
    @Slot(str)
    def setTheme(self, theme: str):
        """Set theme: 'dark', 'light', or 'default'"""
        app = QApplication.instance()
        if theme == "dark":
            app.setPalette(self.darkPalette)
            self.currentTheme = "dark"
        elif theme == "light":
            app.setPalette(self.lightPalette)
            app.setStyleSheet("")  # remove Meshroom's dark stylesheet if applied
            self.currentTheme = "light"
        else:
            app.setPalette(self.defaultPalette)
            self.currentTheme = "default"

        if self.qmlEngine.rootObjects():
            self.qmlEngine.reload()
        self.paletteChanged.emit()

    # ---------- PROPERTIES ----------
    palette = Property(QPalette, lambda self: QApplication.instance().palette(), notify=paletteChanged)
    window = Property(QColor, lambda self: self.palette.color(QPalette.Window), notify=paletteChanged)
    text = Property(QColor, lambda self: self.palette.color(QPalette.Text), notify=paletteChanged)
    button = Property(QColor, lambda self: self.palette.color(QPalette.Button), notify=paletteChanged)
    buttonText = Property(QColor, lambda self: self.palette.color(QPalette.ButtonText), notify=paletteChanged)
    highlight = Property(QColor, lambda self: self.palette.color(QPalette.Highlight), notify=paletteChanged)
