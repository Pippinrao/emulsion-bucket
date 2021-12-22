import os
from typing import List

from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets, QtGui

import service.adb_shell_cmd as adb


def list_dir(path_to_list):
    ret = []
    real_path = os.path.abspath(path_to_list)
    paths = os.listdir(real_path)
    for path in paths:
        full_path = os.path.join(real_path, path)
        if os.path.isdir(os.path.join(full_path)):
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, Qt.ItemDataRole.UserRole, full_path)
            item.setText(0, path)
            item.setIcon(0, QtGui.QIcon("res/image/icon/dir.jfif"))
            ret.append(item)
    for path in paths:
        full_path = os.path.join(real_path, path)
        if not os.path.isdir(full_path):
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, Qt.ItemDataRole.UserRole, full_path)
            item.setText(0, path)
            item.setIcon(0, QtGui.QIcon("res/image/icon/file.png"))
            ret.append(item)
    return ret


def list_device_dir(items: List[adb.File]):
    ret = []
    for item in items:
        if item.is_dir():
            tree_item = QtWidgets.QTreeWidgetItem()
            tree_item.setText(0, item.name)
            tree_item.setText(1, item.mode)
            tree_item.setText(2, item.time)
            tree_item.setText(3, item.size)
            tree_item.setData(0, Qt.ItemDataRole.UserRole, item.path)
            tree_item.setIcon(0, QtGui.QIcon("res/image/icon/dir.jfif"))
            ret.append(tree_item)

    for item in items:
        if not item.is_dir():
            tree_item = QtWidgets.QTreeWidgetItem()
            tree_item.setText(0, item.name)
            tree_item.setText(1, item.mode)
            tree_item.setText(2, item.time)
            tree_item.setText(3, item.size)
            tree_item.setData(0, Qt.ItemDataRole.UserRole, item.path)
            if item.is_link():
                tree_item.setIcon(0, QtGui.QIcon("res/image/icon/link.svg"))
            else:
                tree_item.setIcon(0, QtGui.QIcon("res/image/icon/file.png"))
            ret.append(tree_item)
    return ret
