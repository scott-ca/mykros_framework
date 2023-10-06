import setproctitle
setproctitle.setproctitle('Mykros assist')
from transformers import AutoTokenizer, AutoModel
from PySide2.QtWidgets import QApplication, QMenu, QAction
import logging

from util.main_window import MainWindow


logging.basicConfig(level=logging.DEBUG)

# Features to add
# TODO: Add privacy-focused features that can handle non-private tasks.
# TODO: List all functionalities that require internet access and explain when and why it connects.


app = QApplication([])
app.setQuitOnLastWindowClosed(False)

main_window = MainWindow()

# Create the menu.
menu = QMenu()
show_action = QAction('Show', triggered=main_window.show_chat_prompt)
quit_action = QAction('Quit', triggered=app.quit)
menu.addAction(show_action)
menu.addAction(quit_action)

# Add the menu to the tray icon.
main_window.tray_icon.setContextMenu(menu)

# Start the event loop.
app.exec_()
