import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
import Setup, PDF_Edit, Decorator, Profil
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget


"""class Contr_Widg(ElevatedCardWidget) :
    def __init__(self, icon_path : str, name : str, description : str, path_git : str, name_git : str, contribution : str) :
        super(Contr_Widg, self).__init__()
        self.fly = FlyoutView(name, description, icon_path, icon_path, False)
        self.path_git = HyperlinkButton("www.google.com", name_git, icon = FIF.GITHUB)
        self.contrib = CaptionLabel(contribution)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.fly)
        self.vbox.addWidget(self.contrib, 0, Qt.AlignmentFlag.AlignCenter), self.vbox.addWidget(self.path_git, 0, Qt.AlignmentFlag.AlignCenter)
       """ 
       
class Item(ElevatedCardWidget, QFrame) :
    def __init__(
        self,
        path_im : str,
        title : str,
        description : str,
        parent : QWidget | None = None
    ) :
        super(Item, self).__init__(parent)
        self.vbox = VBoxLayout(self)
        self.image = ImageLabel(path_im)
        self.title = SubtitleLabel(title)
        self.description = BodyLabel(description)
        self.description.setWordWrap(True)
        self.image.scaledToWidth(200)
        self.setBorderRadius(20)
        self.vbox.addWidget(self.image, 0, Qt.AlignmentFlag.AlignCenter), self.vbox.addWidget(self.title, 0, Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.description, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vbox)
        self.setFixedSize(QSize(250, 400))
        self.setFrameShape(QFrame.Shape.Panel)
        self.setObjectName("frame")
        self.setStyleSheet(open("style.qss", 'r').read())
       
class Items(HeaderCardWidget) :
    def __init__(self) :
        super(Items, self).__init__()   
        self.setTitle("Qu'est ce que l'application offre??")
        
        self.hbox = QHBoxLayout()
        self.it_1 = Item("Images/you.png", "Sous Titre Youtube", "Vous pouvez sous-titrer vos vidéos Youtube en 2 cliques. Il suffit juste de copier le lien youtube de la vidéo et coller dans la zone alloué.", self)
        
        self.it_2 = Item("Images/srt.png", "SRT Video", "Vous pouvez récupérer le SRT des vidéos de toutes natures en la langue que vous désirez. Bien quelle ne prends pas en charge toutes les langues, vous avez néanmoins une diversité..", self)
        self.it_3 = Item("Images/play.png", "Stream Movie", "Vous pouvez gratuitement, visionner les vidéos que vous aurez sous-tirés, en incluant simplement les sous-titres et le tour est joué. Et tout cela gratuitement", self)
        
        #self.it_1.setContentsMargins(50, 50, 50, 50), self.it_2.setContentsMargins(50, 50, 50, 50)
        #self.it_3.setContentsMargins(50, 50, 50, 50)
        self.hbox.addWidget(self.it_1), self.hbox.addWidget(self.it_2)
        self.hbox.addWidget(self.it_3)
        self.viewLayout.addLayout(self.hbox)
        self.setContentsMargins(90, 30, 30, 30)
        self.setFixedWidth(1000)
        
        """self.timer = QTimer()
        self.timer.timeout.connect(self.movee)
        self.timer.start(80)"""
        
    def movee(self) :
        it_1 = [self.it_1.x(), self.it_1.y()]
        it_2 = [self.it_2.x(), self.it_2.y()]
        it_3 = [self.it_3.x(), self.it_3.y()]
        if it_1[0] > self.x() :
            it_1[0] = 0
        if it_2[0] > self.x() :
            it_2[0] = 0
        if it_3[0] > self.x() :
            it_3[0] = 0
        self.it_1.move(it_1[0] + 30, it_1[1])
        self.it_2.move(it_2[0] + 30, it_2[1])
        self.it_3.move(it_3[0] + 30, it_3[1])
        
        
class Contr_Widg(ElevatedCardWidget) :
    def __init__(
        self,
        icon_path : str,
        name : str,
        description : str,
        path_git : str,
        name_git : str,
        contribution : str
    ) :
        super(Contr_Widg, self).__init__()
        self.image = ImageLabel(icon_path)
        self.name = SubtitleLabel(name)
        self.description = BodyLabel(description)
        self.path_git = HyperlinkButton(path_git, name_git, icon = FIF.GITHUB)
        self.contrib = CaptionLabel(contribution)
        self.vbox, self.central = QVBoxLayout(), QVBoxLayout(self)
        fr = QFrame()
        self.vbox.addWidget(self.image, 0, Qt.AlignmentFlag.AlignCenter), self.vbox.addWidget(self.name, 0, Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(self.description, 0, Qt.AlignmentFlag.AlignCenter)
        fr.setLayout(self.vbox)
        self.central.addWidget(fr)
        self.central.addWidget(self.contrib, 0, Qt.AlignmentFlag.AlignCenter), self.central.addWidget(self.path_git, 0, Qt.AlignmentFlag.AlignCenter)
        fr.setFrameShape(QFrame.Shape.Panel)
        fr.setObjectName("frame")
        fr.setStyleSheet(open("style.qss", 'r').read())
        self.setFixedSize(270, 450)
        self.image.scaledToWidth(self.width())
        
        with open(f'setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
        
        
class Contributor(HeaderCardWidget) :
    def __init__(self) :
        super(Contributor, self).__init__()
        self.setTitle("Contributeurs du Projet.")
        self.central = QVBoxLayout()
        self.tit = SubtitleLabel("Contributeur du Projet")
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setScrollAnimation(Qt.Horizontal, duration = 1000)
        self.scroll_widget = QWidget()

        self.list_car = QHBoxLayout(self.scroll_widget)
        
        self.joel = Contr_Widg("Images/im8.jpg", "Gradi Joel", "Programmeur Datascientist", "git.chikatsi", "chikatsi-joel", "Developpeur en chef du projet en cours")
        self.orlane = Contr_Widg("Images/orlane.jpg", "Orlane Kabeyene", "Programmeuse et CyberChevalier", "git.chikatsi", "Orlane-joel", "Developpeuse intermédiare du projet")
        self.dawai = Contr_Widg("Images/im8.jpg", "Gradi Joel", "Ingénieur Logiciel", "git.chikatsi", "chikatsi-joel", "Developpeur en chef du projet en cours")
        self.brice = Contr_Widg("Images/brice.jpg", "Brice Koam", "Ingénieur Logiciel", "brice.kouam", "brice-kouam", "Developpeur Intermédiare et Contributeur du Projet")
        self.rudy = Contr_Widg("Images/im8.jpg", "Gradi Joel", "Programmeur Datascientist", "git.chikatsi", "chikatsi-joel", "Developpeur en chef du projet en cours")
        self.list_car.addWidget(self.joel)
        self.list_car.addWidget(self.orlane)
        self.list_car.addWidget(self.brice)
        self.list_car.addWidget(self.rudy)
        self.list_car.addWidget(self.dawai)
        self.scroll_area.setWidget(self.scroll_widget)
        self.central.addWidget(self.tit)
        self.central.addWidget(self.scroll_area)
        self.central.addWidget(hor :=HorizontalSeparator())
        hor.setFixedWidth(1200)
        self.viewLayout.addLayout(self.central)
        path, share = QHBoxLayout(), TransparentToolButton(FIF.SHARE)
        path.addStretch(),  path.addWidget(CaptionLabel("Lien vers le site web")), path.addWidget(share)
        self.central.addLayout(path), self.scroll_area.setFixedHeight(480)
        self.scroll_widget.setAutoFillBackground(True)
        self.setFixedWidth(1000)
        with open(f'setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
        
    def addContributor(self, icon_path : str, name : str, description : str, path_git : str, name_git : str, contribution : str) :
        self.list_car.addWidget(Contr_Widg(icon_path, name , description, path_git , name_git, contribution))

class Entete(QWidget) :
    def __init__(self) -> None:
        super().__init__()
        self.titl = TitleLabel("Bienvenue Dans Notre Application de Retranscription.")
        self.body_lab = BodyLabel("Vous trouverez sur la barre de Naviation, tous les accessoirs mis en évidence par cette application. Le confort Visuel et la bonne expérience IHM a été prise en compte\n")
        self.body_lab.setWordWrap(True)
        self.titl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon = AvatarWidget("Images/logo.png")
        h, v = QHBoxLayout(), QVBoxLayout(self)
        self.icon.setRadius(24)
        h.addWidget(self.icon), h.addWidget(self.titl, 0, Qt.AlignmentFlag.AlignCenter)
        v.addLayout(h), v.addWidget(self.body_lab), v.addWidget(hor :=HorizontalSeparator())
        hor.setFixedWidth(1100)
        path, share = QHBoxLayout(), TransparentToolButton(FIF.SHARE)
        path.addStretch(),  path.addWidget(HyperlinkButton("www.com", "Site web", self, FIF.SHARE))
        v.addLayout(path)
        
        
class Corps(QWidget) :
    def  __init__(self) :
        super(Corps, self).__init__()
        self.vbox = QVBoxLayout(self) 
        self.contrib = Contributor()
        self.entete = Entete()
        self.items = Items()
        
        self.scroll_area = SmoothScrollArea()
        self.scroll_widget = QWidget()
        self.box = VBoxLayout(self.scroll_widget)
        
        self.box.addWidget(self.entete)
        self.box.addWidget(self.items)
        self.box.addWidget(self.contrib)
        self.scroll_area.setWidget(self.scroll_widget)
        
        #self.scroll_area.setScrollAnimation(Qt.Vertical)
        self.scroll_widget.setFixedWidth(1100)
        self.scroll_area.setFixedWidth(1100)
        
        self.vbox.addWidget(self.scroll_area)
        
        
class Home(QWidget) :
    def __init__(self, parent : QWidget | None = None) :
        super(Home, self).__init__(parent)
        self.centrl = QVBoxLayout(self) 
        
        #self.vbox.addWidget(self.entete)
        self.stack = PopUpAniStackedWidget()
        self.contributor = Corps()
        self.joel = Profil.Profill("Images/moi.png", "Joel", "https://beta.theb.ai/home", 500, "kappachikatsi@gmail.com", "Promotteur en chef du projet et Etudiant en licence 3 à l'université de Yaoundé 1", [f"Images/im{i}.jpg" for i in range(1, 9)])
        self.orlane = Profil.Profill("Images/orlane.jpg", "Orlane", "https://beta.theb.ai/home", 500, "oralanekabeyene@gmail.com", "Contributeur Front End du projet et Etudiante à L'université de Yaoundé 1", [f"Images/kab{i}.jpg" for i in range(1, 5)])
        self.brice = Profil.Profill("Images/brice.jpg", "Brice", "https://beta.theb.ai/home", 500, "bricekouam@gmail.com", "Contributeur Back End du projet et Etudiante à L'université de Yaoundé 1", [f"Images/br{i}.jpg" for i in range(1, 4)])
        self.stack.addWidget(self.contributor)
        self.stack.addWidget(self.joel)
        self.stack.addWidget(self.orlane)
        self.stack.addWidget(self.brice)
        self.joel.prof.back.clicked.connect(self.change_slots_menu)
        self.orlane.prof.back.clicked.connect(self.change_slots_menu)
        self.brice.prof.back.clicked.connect(self.change_slots_menu)
        self.contributor.contrib.joel.clicked.connect(self.change_slots)
        self.contributor.contrib.orlane.clicked.connect(self.change_slots_orla)
        self.contributor.contrib.brice.clicked.connect(self.change_slots_brice)
        self.centrl.addWidget(self.stack)
        self.setFixedWidth(1200)
        
        
        with open(f'setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
    def change_slots(self) :
        self.stack.setCurrentWidget(self.joel)
        
    def change_slots_orla(self) :
        self.stack.setCurrentWidget(self.orlane)
        
    def change_slots_brice(self) :
        self.stack.setCurrentWidget(self.brice)
        
    def change_slots_menu(self) :
        self.stack.setCurrentWidget(self.contributor)
        
if __name__ == '__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    #win = Pres("Images/moi.png", "Presentation", "je suis un putain de programmeur")
    win = Home()
    win.show()
    app.exec()