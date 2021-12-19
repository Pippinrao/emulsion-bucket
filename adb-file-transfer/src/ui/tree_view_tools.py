import os

from PyQt6 import QtWidgets


def list_dir(path_to_list):
    ret = []
    real_path = os.path.abspath(path_to_list)
    paths = os.listdir(real_path)
    for path in paths:
        if os.path.isdir(path):
            item = QtWidgets.QTreeWidgetItem()
            data = os.path.join(real_path, path)
            item.setData(0, 1, data)
            item.setData(1, 0, False)
            item.setText(0, path)
            ret.append(item)
    for path in paths:
        if not os.path.isdir(path):
            item = QtWidgets.QTreeWidgetItem()
            data = os.path.join(real_path, path)
            item.setData(0, 1, data)
            item.setData(1, 0, False)
            item.setText(0, path)
            ret.append(item)
    return ret
