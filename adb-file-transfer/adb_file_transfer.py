import sys
from typing import List

from PyQt6.QtWidgets import QApplication

from controller import home_page


def main(args: List[str]):
    app = QApplication(args)
    home = home_page.HomePage()
    home.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)
