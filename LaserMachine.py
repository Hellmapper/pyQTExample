import time
from math import sqrt

from PyQt6.QtCore import QTimer, QPoint, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QMainWindow

from MarkerState import MarkerState

class PropertyEvent(QObject):
    changed = pyqtSignal()
class LaserMachine():
    def __init__(self):
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__processOneThing)
        self.__laserState = MarkerState.HIDE
        self.__position = QPoint(0,0)
        self.__destination = QPoint(0,0)
        self.__isMoving = False;
        self.__maxSpeed = 5;
        self.__bounds = QSize(500, 500);
        self.laserStateChanged = PropertyEvent()
        self.positionChanged = PropertyEvent()
        self.destinationChanged = PropertyEvent()
        self.isMovingChanged = PropertyEvent()
        self.__nextMoveTime = 0
        self.__error = int(0);

    def __setIsMoving(self, value):
        self.__isMoving = value
        if(self.__isMoving):
            self.__timer.start()
        else:
            self.__timer.stop()
        self.isMovingChanged.changed.emit()

    def getLaserState(self) -> MarkerState: return self.__laserState

    def getPosition(self) -> QPoint: return self.__position

    def getDestination(self) -> QPoint: return self.__destination

    def getMaxSpeed(self) -> float: return self.__maxSpeed

    def getBounds(self) -> QSize: return self.__bounds

    def setDestination(self, x, y):
        self.__destination = QPoint(x, y)
        self.destinationChanged.changed.emit()
        self.__setIsMoving(True)

    def __setPosition(self, x, y):
        self.__position.setX(x)
        self.__position.setY(y)
        self.positionChanged.changed.emit()

    def __processOneThing(self):
        step_time = 1.0 / self.__maxSpeed;
        #deltaTime = time.time() - self.__lastTimerTick
        self.__lastTimerTick = time.time()
        print(self.__position)
        if self.__isMoving and self.__lastTimerTick > self.__nextMoveTime:
            self.__doMove()
            self.__nextMoveTime = self.__lastTimerTick + step_time

    def __doMove(self):
        x0 = self.__position.x()
        y0 = self.__position.y()
        x1 = self.__destination.x()
        y1 = self.__destination.y()
        steep = abs(y1 - y0) > abs(x1 - x0);
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx : int = x1 - x0
        dy : int = abs(y1 - y0)
        self.__error = dx / 2
        ystep = 1 if y0 < y1 else -1
        y = y0
        x = self.__position.x()

        self.__error -= dy
        if self.__error < 0:
            y += ystep
            self.__error += dx
        self.__setPosition(y if steep else x, x if steep else y)
        if self.__position == self.__destination:
            self.__setIsMoving(False)