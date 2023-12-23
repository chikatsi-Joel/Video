from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import typing, sys
from pathlib import Path
from qfluentwidgets import *
from qframelesswindow import *
from qfluentwidgets import FluentIcon as FIF
import Video_widg, video_yoututbe, Decorator, server, Setup
from threading import Thread


class CardSeparator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setPen(QColor(255, 255, 255, 46))
        else:
            painter.setPen(QColor(0, 0, 0, 12))

        painter.drawLine(2, 1, self.width() - 2, 1)
        
class Barre(HeaderCardWidget) :
    def __init__(self) :
        super(Barre, self).__init__()
        self.central = QHBoxLayout()
        self.frame, self.vbox = QFrame(), QVBoxLayout()
        self.youtu, self.path = None, None
        self.edit, self.label = LineEdit(), BodyLabel("Entrer le lien youtube  : ")
        self.definition, label = ComboBox(), BodyLabel("Choisissez le format : ")
        self.edit_nom_video, label_name = LineEdit(), BodyLabel("Nom de la Video : ") 
        self.send = PushButton("Telecharger", self, FIF.DOWNLOAD)
        grid = QGridLayout()
        self.tit = SubtitleLabel("File")
        self.butt = PushButton("Select", self, FIF.FOLDER_ADD)
        self.emplacement = QHBoxLayout()
        self.emplacement.addWidget(self.tit), self.emplacement.addStretch(), self.emplacement.addWidget(self.butt)
        self.definition.addItems(["1080p", "720p", "360p", "240p"])
        #self.definition.setFixedSize(QSize(200, 30)), self.edit.setFixedSize(QSize(200, 30))
        
        self.center_icon = ImageLabel("Images/you.png")
        self.name = TitleLabel("YouApp")
        self.descript = SubtitleLabel("Téléchargez vos Videos")
        self.center_icon.setFixedSize(80, 80)
        v, h = QVBoxLayout(), QHBoxLayout()
        v.addWidget(self.name), v.addWidget(self.descript)
        h.addWidget(self.center_icon), h.addLayout(v)
        
        self.vbox.addLayout(h)
        self.vbox.addStretch()
        self.vbox.addLayout(self.emplacement)
        grid.addWidget(self.label, 1, 0), grid.addWidget(self.edit, 1, 1)
        grid.addWidget(label, 2, 0), grid.addWidget(self.definition, 2, 1)
        grid.addWidget(label_name, 3, 0), grid.addWidget(self.edit_nom_video, 3, 1)
        grid.addWidget(self.send, 4, 1)
        self.vbox.addLayout(grid), self.vbox.addStretch() 
        self.send.setIcon(QIcon('Images/down.png')), self.send.setFixedSize(QSize(200, 40))
        self.frame.setLayout(self.vbox)
        self.central.addWidget(self.frame)
        
        self.setTitle("Telecharger sur Youtube")
        self.last = TransparentPushButton(text = "E-mail",  parent = self, icon = QIcon('Images/gmail.png'))
        self.last_2 = TransparentPushButton(text = "twitter", parent = self, icon = QIcon('Images/twitter.png'))
        
        self.wha = TransparentPushButton(text = "Whatsapp", parent = self, icon = QIcon('Images/whatsapp.png'))
        self.last.setObjectName('com'), self.last_2.setObjectName('com')
        vbox = QGridLayout()
        vbox.addWidget(self.last, 0, 0), vbox.addWidget(self.last_2, 0, 1), vbox.addWidget(self.wha, 1, 0)
        self.vbox.addStretch(1)
        sep = CardSeparator(self)
        vbox.setVerticalSpacing(30), vbox.setHorizontalSpacing(20)  
        vbox.setContentsMargins(1, 30, 1, 30)
        self.vBoxLayout.addWidget(sep)
        self.vBoxLayout.addLayout(vbox)
        self.wha.setObjectName('com')
        self.viewLayout.addLayout(self.central)
        self.setFixedHeight(580)
        #self.setStyleSheet(open("Images/style.qss", "r").read())
        setTheme(Theme.DARK)
        self.butt.clicked.connect(self.selectionner_folder)
        self.send.clicked.connect(self.download)
        #self.setContentsMargins(40, 40, 40, 40)
        self.setFixedSize(500, 570)
        
    def selectionner_folder(self) :
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Choisir Le Dossier",
            "Chemin d'accès  : "
        )
        if dir_name:
            self.path = str(Path(dir_name))
            print(str(Path(dir_name)))
    
    @Decorator.Verification("youtube")
    def download(self) :
        path = self.edit.text()
        defs = self.definition.currentText()
        name = self.edit_nom_video.text()
        
        thread = video_yoututbe.Youtt(
            path, 
            name,
            self.path,
            defs,
            self
        )
        InfoBar.info(
            "Début du Téléchargement",
            "Votre téléchargement \na été lancé avec succès",
            isClosable= True,
            position = InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 3000
        )
        thread.start()
        thread.lienInexistant.connect(self.slots_lien_In)
        thread.erreur.connect(self.slots_lien_err)
        thread.endDownload.connect(self.endDown)
        
    def slots_lien_In(self) :
        InfoBar.warning(
                "Lien Youtube Inexistant.",
                "Le lien que vous avez entrer n'existe pas.",
                duration = 6000,
                parent = self
        )
    
    def slots_lien_err(self, erreur : str) :
        InfoBar.warning(
                "Une Erreur c'est produite.",
                f"Une erreur interne c'est produite.\nSuite à une erreur  {erreur}",
                duration = 6000,
                parent = self
        )
        
    def information(self) :
        answer = QMessageBox.question(
                self,
            'Confirmation',
            'Do you want to quit?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        
    def endDown(self) :
        InfoBar.success(
            "Téléchargement terminé",
            "Votre téléchargement c'est achevé avec succès",
            isClosable= True,
            position = InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 3000
        )
        
    def champ_nr(self, name : str) :
        InfoBar.warning(
            f"Champ non remplis",
            content = f"\nVous devez obligatoirement\nremplir le champ :\n{name}",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 5000
        )
        
    
class youtTube(QWidget) :
    def __init__(self) :
        super(youtTube, self).__init__()
        title = SubtitleLabel("Generer le SRT de la video téléchargé")
        self.vbox = QHBoxLayout(self)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        self.video_widg =Video_widg.Video_SRT()
        self.barr = Barre()
        vbox.addWidget(self.video_widg)
        vbox.addStretch(1)
        self.vbox.addWidget(self.barr), self.vbox.addSpacing(50) ,self.vbox.addLayout(vbox)
        self.setContentsMargins(20, 10, 20, 50)
        self.server = self.server = server.requester(Setup.Setup.get_url(), Setup.Setup.get_port())
        
        
    def status_slots(self, status : int) :
        if status == 200 :
            InfoBar.success(
                "Retranscription Réussie.",
                "Votre Retranscription a\nété éffectué avec succès.",
                duration = 5000,
                position = InfoBarPosition.TOP_RIGHT,
                parent = self
            )
        if status == 404 :
            InfoBar.warning(
                "URL Non défini.",
                "L'url spécifié\n n'a pas été trouvé.",
                duration = 5000,
                position = InfoBarPosition.TOP_RIGHT,
                parent = self
            )
        
    def get_url_video(self ) -> str:
        return self.barr.path + '/' + self.barr.edit_nom_video.text() + '.mp4'
    
    def get_url_srt(self) -> str:
        return 


if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    barre = Barre()
    barre.show()
    app.exec()