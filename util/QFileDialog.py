import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DialogDemo(QMainWindow):
    
    def __init__(self, parent=None):
        super(DialogDemo, self).__init__(parent)
        self.setWindowTitle("Dialog demo")
        self.resize(600, 400)
        
        self.button = QPushButton(self)
        self.button.setText("点击弹出文件对话框")
        self.button.move(50, 50)
        self.button.clicked.connect(self.showDialog)
    
    def showDialog(self):
        # 文件打开窗口，路径"D:\\"是窗口打开默认显示的路径，最后一个参数文件的过滤，不满足条件的不会显示
        filename, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Image Files (*.xls *.xlsx)")
        if filename:
            print(f"file: {filename}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DialogDemo()
    demo.show()
    sys.exit(app.exec_())