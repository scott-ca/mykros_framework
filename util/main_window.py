from PySide2.QtGui import QIcon, QScreen
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QMessageBox
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
from util.translator import translate_output
from util.custom_actions_window import CustomActionsWindow

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


        # Wrapping the append method with translation function
        original_append = self.output_widget.append

        def translated_output_widget(message, bypass_translation=False):
            logging.debug(f'\nPrompt Text - Pre Translation: {message} ')
            if bypass_translation == True:
                translated_message = message
                logging.debug(f'Prompt Text - Post(Skip) Translation: {translated_message} ')
            else:
                translated_message = translate_output(message)
                logging.debug(f'Prompt Text - Post Translation: {translated_message} ')
            # Check encoding pre and post-translation
            logging.debug(f'Encoding pre-translation: {str(message.encode())}')
            logging.debug(f'Encoding post-translation: {str(translated_message.encode())}')
            original_append(translated_message)

        self.output_widget.append = translated_output_widget


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
        self.custom_actions_action = QAction('Custom actions', triggered=self.show_custom_actions)
        self.about_action = QAction('About', triggered=self.show_about)
        self.quit_action = QAction('Quit', triggered=QApplication.instance().quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.about_action)
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
    def show_about(self):
        """Show an about window that shows the Mykros version."""
        QMessageBox.about(self, "About Mykros", "Mykros framework\n Version: 0.2.6")

    def show_custom_actions(self):
        """Create and show the custom actions window."""
        self.custom_actions_window = CustomActionsWindow(self)
        self.custom_actions_window.show()
