import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.tool_bar = self.addToolBar('工具栏')
        self.action_right_rotate = QAction(QIcon("icons/右旋转.png"), "向右旋转90", self)
        self.action_left_rotate = QAction(QIcon("icons/左旋转.png"), "向左旋转90°", self)
        self.action_right_rotate.triggered.connect(self.right_rotate)
        self.action_left_rotate.triggered.connect(self.left_rotate)
        self.tool_bar.addActions((self.action_left_rotate, self.action_right_rotate))

        self.useListWidget = UsedListWidget(self)
        self.funcListWidget = FuncListWidget(self)
        self.stackedWidget = StackedWidget(self)
        self.fileSystemTreeView = FileSystemTreeView(self)
        self.graphicsView = GraphicsView(self)

        self.dock_file = QDockWidget(self)
        self.dock_file.setWidget(self.fileSystemTreeView)
        self.dock_file.setTitleBarWidget(QLabel('目录'))
        self.dock_file.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_func = QDockWidget(self)
        self.dock_func.setWidget(self.funcListWidget)
        self.dock_func.setTitleBarWidget(QLabel('文档图像处理工具'))
        self.dock_func.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(self.useListWidget)
        self.dock_used.setTitleBarWidget(QLabel('已选操作'))
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_attr = QDockWidget(self)
        self.dock_attr.setWidget(self.stackedWidget)
        self.dock_attr.setTitleBarWidget(QLabel('属性'))
        self.dock_attr.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_attr.close()

        self.setCentralWidget(self.graphicsView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_file)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_func)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_used)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_attr)

        self.setWindowTitle('DocImgTool')
        self.setWindowIcon(QIcon('icons/main.png'))
        self.src_img = None
        self.cur_img = None

    def update_image(self):
        print('update_image...')
        if self.src_img is None:
            return
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.update_image(img)

    def change_image(self, img):
        print('change_image...')
        self.src_img = img
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.change_image(img)

    def process_image(self):
        img = self.src_img.copy()
        for i in range(self.useListWidget.count()):
            img = self.useListWidget.item(i)(img)
        return img

    def right_rotate(self):
        self.graphicsView.rotate(90)

    def left_rotate(self):
        self.graphicsView.rotate(-90)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open('./custom/styleSheet.qss', encoding='utf-8').read())
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
