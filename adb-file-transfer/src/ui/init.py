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
        self.ui.device_addr.setText("/")
        self.ui.adb_addr.setText("adb.exe")

    def init_src_tree(self):
        src_tree = self.ui.src_tree
        src_tree.setHeaderLabel(os.path.abspath(os.curdir))
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "..")
        self.ui.src_tree.addTopLevelItem(item)
        src_tree.addTopLevelItems(list_dir(os.curdir))
        self.ui.src_tree.show()

    def init_device_tree(self):
        self.ui.device_tree.setHeaderLabel("/")
