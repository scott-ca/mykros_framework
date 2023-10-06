from PySide2.QtGui import QIcon, QScreen
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow, QVBoxLayout, QWidget, QTextEdit
from PySide2.QtCore import Signal, QSettings, QPoint
import logging
import platform
import os

#Using appropriate library for keyboard shortcut depending on the os
if platform.system() == 'Linux':
    # Use pynput for Linux
    from pynput import keyboard
elif platform.system() ==  'Windows':
    # Use keyboard module for Windows
    import keyboard

from util.chat_prompt import ChatPrompt

class MainWindow(QMainWindow):
    """Main application window for the Mykros framework."""

    show_signal = Signal()

    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Mykros framework')
        self.resize(600, 400)
        self.setWindowIcon(QIcon("icon.png"))

        # Create the output widget and add it to the layout
        self.output_widget = QTextEdit()
        self.output_widget.setReadOnly(True)
        self.setCentralWidget(self.output_widget)

        # Create the chat prompt widget
        self.chat_prompt = ChatPrompt(self.output_widget)

        # Add the chat prompt widget to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.output_widget)
        layout.addWidget(self.chat_prompt)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create the system tray icon and menu
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        self.tray_icon.setToolTip('Mykros framework')
        self.show_action = QAction('Show', triggered=self.show_chat_prompt)
        self.quit_action = QAction('Quit', triggered=QApplication.instance().quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.ctrl_pressed = False

        if platform.system() == 'Linux':

            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()

        elif platform.system() ==  'Windows':

            keyboard.add_hotkey('ctrl+`', self.emit_show_signal)

        self.show_signal.connect(self.show_chat_prompt)

        self.center_window()

    def on_press(self, key):
        """Callback function for key press events. Linux only.

        Args:
            key (pynput.keyboard.Key): The key that was pressed.
        """
        if key == keyboard.Key.ctrl:
            self.ctrl_pressed = True
        elif key == keyboard.KeyCode.from_char('`') and self.ctrl_pressed:
            self.show_signal.emit()

    def on_release(self, key):
        """Callback function for key release events. Linux only.

        Args:
            key (pynput.keyboard.Key): The key that was released.
        """
        if key == keyboard.Key.ctrl:
            self.ctrl_pressed = False

    def emit_show_signal(self):
        """Emit the show signal to show or hide the chat prompt widget."""
        self.show_signal.emit()

    def show_chat_prompt(self):
        """Show or hide the chat prompt widget based on the window visibility."""
        logging.debug('shortcut activated')
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.chat_prompt.setFocus()

    def center_window(self):
        """Center the window on the screen."""
        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.geometry()
            center_x = screen_geometry.center().x() - window_geometry.width() / 2
            center_y = screen_geometry.center().y() - window_geometry.height() / 2
            self.move(center_x, center_y)
