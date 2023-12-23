from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
import server 
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas




class Graphe_Item(HeaderCardWidget) :
    def __init__(self, title : str, list_x : list, list_y : list) :
        super(Graphe_Item, self).__init__()   
        self.data_x = list_x
        self.data_y = list_y
        self.vbox = VBoxLayout(self)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.figure.patch.set_facecolor((95/255, 95/255, 95/255))
        hb = QHBoxLayout()
        self.combo = ComboBox(self)
        hb.addWidget(CaptionLabel('Sélectionnez le type de Diagramme  : '))
        hb.addWidget(self.combo)
        self.vbox.addLayout(hb)
        self.vbox.addWidget(self.canvas)

        self.setFixedSize(QSize(500, 500))
        setTheme(Theme.DARK)    
        self.setStyleSheet(open("/home/chikatsi/Bureau/INFL3/COURS/TP_INF321/setting_interface.qss", 'r').read())
        self.viewLayout.addLayout(self.vbox)
        self.setTitle("Tracer en cercle compte supprimés..")
        
        self.combo.addItems(["Diagramme en Batons", 'Diagramme en Cercle'])
        self.diagramme_baton()
        
        self.combo.currentTextChanged.connect(self.poss)
        
    def poss(self) :
        if self.combo.currentText() == 'Diagramme en Batons' :
            self.diagramme_baton()
        else :
            self.diagramme_cercle()
            
    def diagramme_baton(self) :
        self.ax.clear()
        self.ax.bar(self.data_x, self.data_y)
        self.ax.legend()
        self.canvas.draw()
        
        
    def diagramme_cercle(self) :
        self.ax.clear()
        self.ax.pie(self.data_x, labels=self.data_y, autopct='%1.1f%%')
        self.ax.legend()
        self.canvas.draw()
