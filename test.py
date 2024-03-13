from PyQt6.QtCore import QSize, QRectF, QEvent, Qt
from PyQt6.QtGui import QPaintEvent, QImage, QColor, QPainter
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.canvas = QImage()
        self.installEventFilter(self)
        self.isInResize = False
        self.setMouseTracking(True)
        self.positions = []

    def mouseMoveEvent(self, e) -> None:
        self.positions.append(e.position().toPoint())
        self.update()

    def showEvent(self, e) -> None:
        self.canvas = QImage(self.size(), QImage.Format.Format_ARGB32)

    def eventFilter(self, obj, e: QEvent) -> bool:
        if self.isInResize:
            if e.type() == QEvent.Type.MouseButtonRelease:
                if(e.button() == Qt.MouseButton.LeftButton):
                    self.endResize()
            elif e.type() == QEvent.Type.NonClientAreaMouseButtonRelease:
                self.endResize()
        return super().eventFilter(obj, e)

    def endResize(self):
        self.isInResize = False
        self.canvas = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.update()

    def changeEvent(self, state) -> None:
        if state.type() == QEvent.Type.WindowStateChange:
            self.endResize()

    def resizeEvent(self, e) -> None:
        self.isInResize = True

    def paintEvent(self, e:QPaintEvent) -> None:
        if self.isInResize:
            return
        width = self.canvas.width()
        height = self.canvas.height()
        for x in range(width):
            for y in range(height):
                self.canvas.setPixel(x, y, QColor(255 - int(255 * x / width), int(255 * x / width), int(255 * y / height),
                                         255).rgb())
        for i in self.positions:
            color = self.canvas.pixelColor(i.x(), i.y())
            color.setRed(255 - color.red())
            color.setGreen(255 - color.green())
            color.setBlue(255- color.blue())
            self.canvas.setPixel(i.x(), i.y(), color.rgb())
        painter = QPainter(self)
        painter.drawImage(QRectF(0,0 ,width, height), self.canvas)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
