from ast import main
import sys
from PyQt5 import QtWidgets
import subUi
from loguru import logger



logger.add(".log/main.log", format="{time} | {level} | {name} | {message}", level="DEBUG",
           rotation="1 KB", encoding="utf-8",enqueue=True, backtrace=True, diagnose=True)


if __name__ == "__main__":
    #获取UIC窗口操作权限
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    qtTest=subUi.subUi()
    
    # 调用自定义的界面（即刚刚转换的py对象）
    ui=qtTest.setupUi(MainWindow)
    # MainWindow.resize(1500, 500)

    MainWindow.show()
    
    sys.exit(app.exec_())