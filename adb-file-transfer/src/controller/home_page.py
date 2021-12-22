from PyQt6 import QtWidgets

import ui.init
from service import adb_shell_cmd
from service import transfer_service as ts
from ui.transfer_window import Ui_MainWindow
from ui.tree_view_tools import *
from PyQt6.QtCore import Qt


class HomePage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init = ui.init.Init(self.ui)
        self.init.ext_init()
        self.service = ts.Service()
        adb_shell_cmd.adb = self.ui.adb_addr.text()
        self.adb_tool = adb_shell_cmd.Path
        self.connect()

    def connect(self):
        self.ui.src_open.clicked.connect(self.src_btn_clicked)
        self.ui.src_tree.itemDoubleClicked.connect(self.src_tree_clicked)
        self.ui.device_open.clicked.connect(self.device_btn_clicked)
        self.ui.device_tree.itemDoubleClicked.connect(self.device_tree_item_clicked)
        self.ui.device_tree.itemClicked.connect(self.device_tree_item_choose)
        self.ui.src_tree.itemClicked.connect(self.src_tree_item_choose)
        self.ui.pull_btn.clicked.connect(self.pull_clicked)
        self.ui.push_btn.clicked.connect(self.push_clicked)

    def pull_clicked(self):
        device_addr = self.ui.device_addr.text()
        local_addr = self.ui.src_addr.text()
        if not os.path.isdir(local_addr):
            local_addr = os.path.dirname(local_addr)
            self.ui.src_addr.setText(local_addr)
        self.adb_tool.pull(device_addr, local_addr)
        self.src_btn_clicked()

    def push_clicked(self):
        device_addr = self.ui.device_addr.text()
        local_addr = self.ui.src_addr.text()
        if not self.adb_tool.is_dir(device_addr):
            device_addr = self.adb_tool.dir_name(device_addr)
            self.ui.device_addr.setText(device_addr)
        self.adb_tool.push(local_addr, device_addr)
        self.device_btn_clicked()

    def src_tree_item_choose(self, item: QtWidgets.QTreeWidgetItem, col):
        data: str = item.data(0, Qt.ItemDataRole.UserRole)
        self.ui.src_addr.setText(data)

    def device_tree_item_choose(self, item: QtWidgets.QTreeWidgetItem, col):
        data: str = item.data(0, Qt.ItemDataRole.UserRole)
        self.ui.device_addr.setText(data)

    def device_btn_clicked(self):
        addr = self.ui.device_addr.text()
        if not addr:
            addr = "/"
        if self.adb_tool.is_dir(addr):
            self.pull_clicked()
        items = self.adb_tool.list_dir(addr)
        self.ui.device_tree.clear()
        self.ui.device_tree.addTopLevelItems(list_device_dir(items))
        self.ui.device_tree.show()

    def device_tree_item_clicked(self, item: QtWidgets.QTreeWidgetItem, col):
        try:
            data: str = item.data(0, Qt.ItemDataRole.UserRole)
            self.ui.device_addr.setText(data.replace("//", "/"))
            self.device_btn_clicked()
        except IOError:
            QtWidgets.QMessageBox.critical(self, "", "打开文件失败！")
            return

    def src_btn_clicked(self):
        addr = os.path.abspath(self.ui.src_addr.text())
        if not addr:
            addr = os.path.abspath(os.path.curdir)
        if not os.path.isdir(addr):
            os.startfile(addr)
            self.ui.src_addr.setText(os.path.dirname(addr))
        else:
            self.ui.src_tree.clear()
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, "..")
            item.setData(0, Qt.ItemDataRole.UserRole, os.path.dirname(addr))
            item.setIcon(0, QtGui.QIcon("res/image/icon/dir.jfif"))
            self.ui.src_tree.addTopLevelItem(item)
            self.ui.src_tree.addTopLevelItems(list_dir(addr))
            self.ui.src_tree.show()

    def src_tree_clicked(self, item: QtWidgets.QTreeWidgetItem, col):
        try:
            data = item.data(0, Qt.ItemDataRole.UserRole)
            self.ui.src_addr.setText(data)
            self.src_btn_clicked()
        except IOError:
            QtWidgets.QMessageBox.critical(self, "", "打开文件失败！")
            return
