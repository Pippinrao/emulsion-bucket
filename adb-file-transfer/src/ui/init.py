import ui.transfer_window
from ui.tree_view_tools import *


class Init:
    def __init__(self, raw_ui: ui.transfer_window.Ui_MainWindow):
        self.ui = raw_ui

    def ext_init(self):
        self.init_addr()
        self.init_src_tree()
        self.init_device_tree()

    def init_addr(self):
        self.ui.src_addr.setText(os.path.abspath(os.path.curdir))
        self.ui.adb_addr.setText("adb.exe")

    def init_src_tree(self):
        src_tree = self.ui.src_tree
        src_tree.setHeaderLabel(os.path.abspath(os.curdir))
        src_tree.addTopLevelItems(list_dir(os.curdir))
        self.ui.src_tree.show()

    def init_device_tree(self):
        lables = ["name", "mode", "date", "size"]
        self.ui.device_tree.setHeaderLabels(lables)
        self.ui.device_tree.setColumnCount(4)
        self.ui.device_tree.setColumnWidth(0, 300)
        self.ui.device_tree.setColumnWidth(1, 80)
        self.ui.device_tree.setColumnWidth(2, 120)
