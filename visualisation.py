import numpy as np
import sys, database
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QGridLayout()
        self.centralWidget.setLayout(layout)

        self.win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        self.win.resize(1000, 600)
        layout.addWidget(self.win)

        pg.setConfigOptions(antialias=True)

        self.p1 = self.win.addPlot(title="Tracé (ID, Solde)")
        self.p1.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()])

        self.lr_1 = pg.LinearRegionItem([400, 700])
        self.lr_1.setZValue(-10)
        self.p1.addItem(self.lr_1)
        
        self.p2 = self.win.addPlot(title="Zoom Tracé (ID, Solde)")
        self.p2.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()], symbolBrush=(39, 39, 39), symbolPen='w')

        
        self.p3 = self.win.addPlot(title="Tracé  GAIN(ID_USER, Video)")
        self.x_ =[video.id_user for video in database.Video.get_all_video()]
        self.y_ = [video.price for video in database.Video.get_all_video()]
        y, x = np.histogram(self.x_, bins = len(self.y_))
        self.lr_3 = pg.LinearRegionItem([400, 700])
        self.lr_3.setZValue(-10)
        self.p3.addItem(self.lr_3)
        self.win.nextRow()
        bgi = pg.BarGraphItem(x0=x[:-1], x1=x[1:], height=y, pen='w', brush=(0,0,255,150))
        self.p3.addItem(bgi)

        self.p7 = self.win.addPlot(title="Tracé Zoom GAIN(ID_USER, Video)")
        bgi_7 = pg.BarGraphItem(x0=x[:-1], x1=x[1:], height=y, pen='w', brush=(0,0,255,150))
        self.p7.addItem(bgi_7)

        self.p8 = self.win.addPlot(title="(Age, Nombre Video)")
        self.p8.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()], pen=(255, 255, 255, 200))
        self.lr = pg.LinearRegionItem([400, 700])
        self.lr.setZValue(-10)
        self.p8.addItem(self.lr)

        self.p9 = self.win.addPlot(title="Zoom sur la région sélect. (Age, Nombre Video)")
        self.p9.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()])

        def updatePlot():
            self.p9.setXRange(*self.lr.getRegion(), padding=0)

        def updateRegion():
            self.lr.setRegion(self.p9.getViewBox().viewRange()[0])

        def updatePlot_1():
            self.p2.setXRange(*self.lr_1.getRegion(), padding=0)

        def updateRegion_1():
            self.lr_1.setRegion(self.p2.getViewBox().viewRange()[0])
            
        def updatePlot_3():
            self.p7.setXRange(*self.lr_3.getRegion(), padding=0)

        def updateRegion_3():
            self.lr_3.setRegion(self.p7.getViewBox().viewRange()[0])  
            
        self.lr_1.sigRegionChanged.connect(updatePlot_1)
        self.p2.sigXRangeChanged.connect(updateRegion_1)
        
        self.lr.sigRegionChanged.connect(updatePlot)
        self.p9.sigXRangeChanged.connect(updateRegion)
        
        self.lr_3.sigRegionChanged.connect(updatePlot_3)
        self.p7.sigXRangeChanged.connect(updateRegion_3)
        
        
    def mise_a_jour(self) :
        self.p1.clear(), self.p2.clear()
        self.p7.clear(), self.p8.clear(), self.p9.clear()
        self.p1.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()],  brush=(50, 50, 200, 100), pen=(200, 200, 200), symbolBrush=(39, 39, 39), symbolPen='w')
        self.p2.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()], symbolBrush=(39, 39, 39), symbolPen='w')
        self.x_ =[video.id_user for video in database.Video.get_all_video()]
        self.y_ = [video.price for video in database.Video.get_all_video()]
        y, x = np.histogram(self.x_, bins = len(self.y_))
        bgi_7 = pg.BarGraphItem(x0=x[:-1], x1=x[1:], height=y, pen='w', brush=(0,0,255,150))
        self.p7.addItem(bgi_7)
        self.p9.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()])
        self.p8.plot(x = [user.id for user in database.User.get_all_user()], y = [user.age for user in database.User.get_all_user()])
        self.p8.addItem(self.lr)
        self.p1.addItem(self.lr_1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()