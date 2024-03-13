from PyQt6.QtCore import QSize, QRectF, QEvent, Qt, QPoint
from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow)
from PyQt6 import uic

from LaserMachine import LaserMachine
from QZoomStageView import QZoomStageView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.image = QImage()
        self.userIsResizing = False
        self.resize(320, 240)
        self.init_image(self.size())
        self.stageView = QZoomStageView()
        self.setWindowTitle("My App")
        self.setCentralWidget(self.stageView)
        self.installEventFilter(self)
        self.__connectedMachine: LaserMachine = None
        self.stageView.signals.mouseStageClicked.connect(self.mouse_stage_clicked)

    def mouse_stage_clicked(self, wpos: QPoint):
        self.__connectedMachine.setDestination(wpos.x(), wpos.y())
    def connectMachine(self, machine : LaserMachine):
        if self.__connectedMachine is not None:
            self.__connectedMachine.positionChanged.changed.disconnected(self.machine_position_changed)
        self.__connectedMachine = machine
        self.__connectedMachine.positionChanged.changed.connect(self.machine_position_changed)
        self.stageView.setStageLimits(machine.getBounds())

    def machine_position_changed(self):
        self.stageView.setCurrentPosition(self.__connectedMachine.getPosition())

    def eventFilter(self, object, event) -> bool:
        if event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton and self.userIsResizing:
            self.complete_resize()
        elif event.type() == QEvent.Type.NonClientAreaMouseButtonRelease and self.userIsResizing:
            self.complete_resize()
        return super().eventFilter(object, event)

    def resizeEvent(self, e) -> None:
        self.userIsResizing = True

    def complete_resize(self):
        self.userIsResizing = False
        self.init_image(self.size())
        self.update()

    def init_image(self, size: QSize):
        self.image = QImage(size.width(), size.height(), QImage.Format.Format_ARGB32)
'''
    def paintEvent(self, event):
        width = self.image.width()
        height = self.image.height()
        for x in range(width):
            for y in range(height):
                self.image.setPixel(x, y,
                                    QColor(255 - int(255 * x / width), int(255 * x / width), int(255 * y / height),
                                           255).rgb())
        painter = QPainter(self)
        painter.drawImage(QRectF(0, 0, width, height), self.image)
'''
def dest_changed():
    print(f"destination changed to {machine.getDestination()}")

app = QApplication([])

window = MainWindow()
window.show()
machine = LaserMachine()
window.connectMachine(machine)
machine.destinationChanged.changed.connect(dest_changed)
machine.setDestination(100, 30)
app.exec()


