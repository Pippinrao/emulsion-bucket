import ui.init
from service import transfer_service as ts
from ui.transfer_window import Ui_MainWindow
from ui.tree_view_tools import *
from PyQt6 import QtWidgets


class HomePage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init = ui.init.Init(self.ui)
        self.init.ext_init()
        self.service = ts.Service()
        self.connect()

    def connect(self):
        self.ui.src_open.clicked.connect(self.src_btn_clicked)
        self.ui.src_tree.itemDoubleClicked.connect(self.src_tree_clicked)

    def src_btn_clicked(self):
        self.ui.src_tree.clear()
        addr = os.path.abspath(self.ui.src_addr.text())
        if not addr:
            addr = os.path.abspath(os.path.curdir)
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "..")
        self.ui.src_tree.addTopLevelItem(item)
        self.ui.src_tree.addTopLevelItems(list_dir(addr))
        self.ui.src_tree.show()

    def src_tree_clicked(self, item: QtWidgets.QTreeWidgetItem, col):
        if item.data(1, 0):
            return
        try:
            data = item.data(0, 1)
            if os.path.isdir(data):
                item.addChildren(list_dir(data))
            else:
                os.startfile(data)
        except IOError:
            QtWidgets.QMessageBox.critical(self, "", "打开文件失败！")
            return 
        finally:
            print("error")
        item.setData(1, 0, True)
