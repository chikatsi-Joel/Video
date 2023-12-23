from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
import Setup, PDF_Edit, Decorator, server, Download_
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget
        

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
        
class Video_SRT(HeaderCardWidget) :
    def __init__(self ) :
        super(Video_SRT, self).__init__()
        self.setTitle("Generer Fichier")
        self.lang_cible = ComboBox(self)
        self.lang_dep = ComboBox(self)
        self.name = LineEdit()
        self.evolution = ProgressRing()
        self.typ = ComboBox()
        self.valider, self.visionner = PushButton("Valider"), PushButton("visionner", self, FIF.MOVIE)
        self.lang_cible.addItems(list(map(str.capitalize, list(Setup.Setup.lang.keys())[1:])))
        self.lang_dep.addItems(list(map(str.capitalize, Setup.Setup.lang.keys())))
        self.grid = QGridLayout()
        hbox = QHBoxLayout()
        self.montant_tarifaire = BodyLabel("")
        self.montant = TitleLabel("")
        b = QHBoxLayout()
        self.sep = CardSeparator(self)
        self.typ.addItems(["SRT", "PDF"])
        b.addWidget(self.montant_tarifaire), b.addStretch(), b.addWidget(VerticalSeparator()), b.addStretch(), b.addWidget(self.montant)
        self.precision, self.val_precis  = LineEdit(), TransparentToolButton(FIF.ACCEPT)
        hbox.addWidget(self.evolution, 1, Qt.AlignmentFlag.AlignLeft), hbox.addStretch() ,hbox.addWidget(self.precision),  hbox.addStretch(), hbox.addWidget(self.val_precis)
        self.evolution.setTextVisible(True)
        self.grid.addWidget(BodyLabel("Définir le type de fichier : "), 0, 0), self.grid.addWidget(self.typ, 0, 1)
        self.grid.addWidget(BodyLabel("Language De la Video : "), 1, 0), self.grid.addWidget(self.lang_dep, 1, 1)
        self.grid.addWidget(BodyLabel("Language Cible : "), 2, 0), self.grid.addWidget(self.lang_cible, 2, 1)
        self.grid.addWidget(BodyLabel("Nom du fichier : "), 3, 0), self.grid.addWidget(self.name, 3, 1)
        self.grid.addWidget(BodyLabel("Entrer la Precision : "), 4, 0), self.grid.addLayout(hbox, 4, 1)
        self.grid.addWidget(self.visionner, 6, 1, alignment = Qt.AlignmentFlag.AlignRight), self.grid.addWidget(self.valider, 6, 0, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addLayout(b, 5, 1), b.addSpacing(20)
        self.visionner.setFixedWidth(120), self.valider.setFixedWidth(120)
        self.visionner.setFixedHeight(45), self.valider.setFixedHeight(45)
        self.viewLayout.addLayout(self.grid)
        self.vBoxLayout.addWidget(self.sep)
        h = QHBoxLayout()
        h.addStretch(), h.addWidget(CaptionLabel("site web")), h.addWidget(TransparentToolButton(FIF.SHARE))
        h.setContentsMargins(10, 10, 10, 10)
        self.value = 0
        self.vBoxLayout.addLayout(h)
        self.precision.setValidator(QIntValidator())
        self.precision.setFixedWidth(80)
        
        self.val_precis.clicked.connect(self.evolution_slot)
        self.val_precis.clicked.connect(self.tarif_slot)
        
    def evolution_slot(self) :
        self.value = self.evolution.value()
        self.timer = QTimer()
        if self.precision.text().strip() == '':
            return
        if(self.value == int(self.precision.text().strip())) :
            return
        self.timer.timeout.connect(self.count if self.value < int(self.precision.text()) else self.decount)
        self.timer.start(30)
        
    def count(self) :
        self.value  += 1 
        self.evolution.setValue(self.value)
        if(self.value == int(self.precision.text().strip())) :
            self.timer.stop()
            
    def decount(self) :
        self.value  -= 1 
        self.evolution.setValue(self.value)
        if(self.value == int(self.precision.text().strip())) :
            self.timer.stop()
            
    def tarif_slot(self) :
        if (montant :=Setup.Setup.tarif(int(self.precision.text()))) == 0 :
            self.montant_tarifaire.setText(""), self.montant.setText("")
        else :
            self.montant_tarifaire.setText(f"Le coût sera de  : ")
            self.montant.setText(f'  {montant} $')
            self.beta_mode()
            
    def beta_mode(self) :
        InfoBar.warning(
            "Mode Payant",
            content = "La précision que vous avez \nsélectionnez est payante car, elle \nnécessite une grande puissance de \ncalcul",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 5000
        )


class Pres(ElevatedCardWidget) :
    def __init__(self, image_path : str, title : str, text : str) :
        super(Pres, self).__init__()
        self.title = TitleLabel(title)
        self.text = BodyLabel(text)
        self.image = ImageLabel(image_path)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.image)
        self.vbox.addStretch()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.text)
        self.image.scaledToHeight(130)
        self.setLayout(self.vbox)
        self.setFixedSize(200, 200)
        
        
class Visionner(QWidget) :
    def __init__(self) :
        super(Visionner, self).__init__()
        self.vbox = QVBoxLayout(self)
        self.video_widg = VideoWidget()
        self.vbox.addWidget(self.video_widg)#, self.vbox.addWidget(self.bar)


class  UTILS_video(QWidget) :
    def __init__(self, parent):
        super(UTILS_video, self).__init__(parent)
        self.central = QHBoxLayout()
        self.box = QVBoxLayout(self)
        self.video = Video_SRT()
        self.pdf_ = PDF_Edit.Fichier_Load()
        hbox = QHBoxLayout()
        ico = IconWidget(FIF.VIDEO)
        self.paren = parent
        self.video_path, self.srt_path = "", ""
        self.server = server.requester(Setup.Setup.get_url(), Setup.Setup.get_port())
        self.lab = SubtitleLabel("Vous pourrez Voire et retranscrire Vos Videos")        
        hbox.addWidget(self.lab), hbox.addWidget(ico)
        self.box.addStretch(1), ico.setFixedSize(QSize(50, 50))
        self.lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(10, 10, 10, 10)
        self.central.addWidget(self.pdf_), self.central.addSpacing(30), self.central.addWidget(self.video)
        self.box.addLayout(hbox), self.box.addLayout(self.central)
        self.box.addSpacing(30)

        self.video.valider.clicked.connect(self.valider_slots)
    
    @Decorator.Verification(type = 'retranscript')
    def valider_slots(self) :
        
        self.thread_down = Download_.Down(
            server = self.server,
            file_path = self.pdf_.path,
            lang_dep = Setup.Setup.lang[self.video.lang_dep.currentText().lower()],
            lang_cible = Setup.Setup.lang[self.video.lang_cible.currentText().lower()],
            type = Setup.Setup.Convert(int(self.video.precision.text())),
            name = self.video.name.text(),
            endpoint_file = 'video',
            path_srt = self.pdf_.srt_path,
            id_user = self.paren.user['id']
        )
        self.thread_down.start()
        self.thread_down.status_code.connect(self.status_slots)
        self.srt_path = self.video.name.text() + '.srt'
        self.video_path = self.pdf_.path
        
    def champ_nr(self, name : str) :
        InfoBar.warning(
            "Champ non remplis",
            content = f"\nVous devez obligatoirement\nremplir le champ :\n{name}",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 5000
        )
    def select_nr(self, name : str) :
        InfoBar.warning(
            "Sélection vide",
            content = f"\nVeuillez sélectionner le\n{name}",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self,
            duration = 5000
        )
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
if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    #win = Pres("Images/moi.png", "Presentation", "je suis un putain de programmeur")
    win = UTILS_video()
    win.show()
    app.exec()