import setproctitle
setproctitle.setproctitle('Mykros framework')
from transformers import AutoTokenizer, AutoModel
from PySide2.QtWidgets import QApplication, QMenu, QAction
import logging

from util.main_window import MainWindow


logging.basicConfig(level=logging.DEBUG)

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

main_window = MainWindow()

# Create the menu.
menu = QMenu()
show_action = QAction('Show', triggered=main_window.show_chat_prompt)
custom_actions_action = QAction('Custom actions', triggered=main_window.show_custom_actions)
about_action = QAction('About', triggered=main_window.show_about)
quit_action = QAction('Quit', triggered=app.quit)
menu.addAction(show_action)
menu.addAction(custom_actions_action)
menu.addAction(about_action)
menu.addAction(quit_action)

# Add the menu to the tray icon.
main_window.tray_icon.setContextMenu(menu)

# Start the event loop.
app.exec_()
