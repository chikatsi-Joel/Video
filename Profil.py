
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from qfluentwidgets import *
from qframelesswindow import *
from qfluentwidgets import FluentIcon as FIF


class MicaWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(MSFluentTitleBar(self))
        

class StatisticsWidget(QWidget):

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))
  
class Prof(SimpleCardWidget) :
    def __init__(
        self,
        name : str,
        path_git : str, 
        stat : int,
        mail  : str, 
        descript : str,
        path_image : str = None
    ) :
        super(Prof, self).__init__()
        self.image_ic = ImageLabel(path_image if path_image is not None else "Images/user.png", self)
        self.image_ic.setBorderRadius(8, 8, 8, 8)
        self.image_ic.scaledToWidth(120)
        
        self.name_label = TitleLabel(name, self)
        self.mail = PrimaryPushButton(mail, self, FIF.MAIL)
        self.lien_git = HyperlinkButton(path_git, "Lien Git", self, FIF.GITHUB)
        self.share = TransparentToolButton(FIF.SHARE, self)
        self.stat_1, self.stat_2, self.stat_3 = StatisticsWidget("Grade", "9K", self), StatisticsWidget("Tokens", '200K$.', self), StatisticsWidget("Manager", "30", self)
        self.body_lab = BodyLabel(
            descript, self
        )
        self.tagButton = PillPushButton("Abonner", self, icon = QIcon("Images/like.png"))
        self.tagButton.setCheckable(False)
        setFont(self.tagButton, 12)
        #self.tagButton.setFixedSize(100, 32)
        vert = VerticalSeparator(self)
        self.body_lab.setWordWrap(True)
        vbox, hbox = QVBoxLayout(), QHBoxLayout()
        vbox_stat, s_hbox =  QHBoxLayout(), QHBoxLayout()
        vbox_stat.addWidget(self.stat_1), vbox_stat.addWidget(vert), vbox_stat.addWidget(self.stat_2), vbox_stat.addWidget(VerticalSeparator()), vbox_stat.addWidget(self.stat_3)
        self.vbox = QVBoxLayout()
        s_hbox.addWidget(self.tagButton, 0, Qt.AlignmentFlag.AlignLeft),  s_hbox.addWidget(self.share, 0, Qt.AlignmentFlag.AlignRight)
        vbox.addWidget(self.name_label), vbox.addWidget(self.lien_git), vbox.addSpacing(10), vbox.addLayout(vbox_stat) ,vbox.addWidget(self.body_lab)
        hbox.addWidget(self.image_ic), hbox.addLayout(vbox), hbox.addStretch(1), hbox.addWidget(self.mail)
        self.vbox.addLayout(hbox), self.vbox.addLayout(s_hbox)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.vbox)
        
        self.share.clicked.connect(self.successInfo)
        
        
    def successInfo(self) :
        InfoBar.success(
            title = "Copy Réussie",
            content = f"\nVous avez copié le lien vers \nle compte Git de M/Mme {self.name_label.text()} avec succès.",
            isClosable = True,
            duration = 2000,
            position = InfoBarPosition.TOP_RIGHT,
            parent = self
        )
        
    
class Gallery(HeaderCardWidget) :
    def __init__(self, images : list[str], parent = None) :
        super(Gallery, self).__init__(parent)
        self.setTitle('Gallery')
        self.horizontal = HorizontalFlipView(self)
        self.expandButton = TransparentToolButton(
            FIF.CHEVRON_RIGHT_MED, self)
        self.horizontal.addImages(images= images)
        self.horizontal.setBorderRadius(8)
        self.horizontal.setSpacing(10)
        self.headerLayout.addWidget(self.expandButton, 0, Qt.AlignRight)
        self.viewLayout.addWidget(self.horizontal)
        
class SystemReq(HeaderCardWidget) :
    def __init__(self) :
        super(SystemReq, self).__init__()    
        self.setTitle('Information Contact')
        self.facebook_link = HyperlinkButton("https://www.facebook.com/gradi.piedjou", "Facebook", self, "Images/facebook.png")
        self.youtub = HyperlinkButton("https://www.youtube.com/channel/UCmITTbMFloRiLhW2QCkci-A", "Youtube", self, "Images/you.png")
        self.twitter = HyperlinkButton("https://www.facebook.com/gradi.piedjou", "twitter", self, "Images/twitter.png")
        self.vbox = QHBoxLayout()
        self.vbox.addWidget(self.facebook_link), self.vbox.addWidget(self.twitter)
        self.vbox.addWidget(self.youtub)
        
        self.viewLayout.addLayout(self.vbox)
        
class A_propos(HeaderCardWidget) :
    def __init__(self) :
        super(A_propos, self).__init__()
        self.setTitle("A propos de Moi.") 
        setTheme(Theme.DARK)
        self.body_lab = BodyLabel("Etudiant en Informatique L3 à l'université de Yaoundé 1, \n J'ai eu a travaillé sur des projets divers notamment en intelligence Artificielle\n Egalement sur des projets en tant que Bénévolt")
        self.viewLayout.addWidget(self.body_lab)
        
class Profile(SmoothScrollArea) :
    def __init__(
        self, 
        path_name : str,
        name : str, 
        path_git : str,
        stat: str, 
        mail : str, 
        descript : str, 
        images : list[str],
        parent=None
    ):
        super(Profile, self).__init__(parent)
        self.view = QWidget(self)
        h_back = QHBoxLayout()
        self.back = TransparentToolButton(FIF.RETURN)
        h_back.addWidget(self.back), h_back.addStretch()
        self.prof = Prof(path_image=path_name, name=name, path_git = path_git, stat= stat, mail = mail, descript= descript)
        self.prop = A_propos()
        self.gall = Gallery(images = images)
        self.sys = SystemReq()
        self.setObjectName("profile")
        with open(f'setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        self.vbox = VBoxLayout(self.view)
        self.vbox.addLayout(h_back)
        self.vbox.addWidget(self.prof), self.vbox.addWidget(self.prop), self.vbox.addWidget(self.gall), self.vbox.addWidget(self.sys)
        self.setWidget(self.view)
        
        self.setContentsMargins(40, 40, 40, 40)
        #self.resize(670, 580)

class Profill(QWidget) :
    def __init__(
        self,
        path_name : str,
        name : str,
        path_git : str,
        stat: str,
        mail : str,
        descript : str,
        images : list[str]
    ) :
        super(Profill, self).__init__()
        self.vbox = QHBoxLayout(self)
        self.prof = Profile(path_name=path_name, name=name, path_git = path_git, stat= stat, mail = mail, descript= descript, images = images)
        self.prof.setScrollAnimation(Qt.Horizontal, duration = 2000)
        self.vbox.addSpacing(100), self.vbox.addWidget(self.prof)
        with open(f'setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
        
if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    ma = Profill("Images/moi.png", "Joel", "https://beta.theb.ai/home", 500, "kappachikatsi@gmail.com", "Promotteur en chef du projet et Etudiant en licence 3 à l'université de Yaoundé 1", "im6.png")
    ma.show()
    app.exec()