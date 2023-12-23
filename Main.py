from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from requests import ConnectionError

from qfluentwidgets import *
import sys, Profil, Video_widg, YouApp, Home, Stream_Vid, Music, Form, Decorator, Setup, server, Settings, Download_
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from pysrt import SubRipFile


class CustomTitleBar(TitleBar) :
    def __init__(self, parent = None) :
        super(CustomTitleBar, self).__init__(parent = parent)
        self.search = SearchLineEdit(self)
        self.search.setPlaceholderText("Rechercher")
    
    
class App(FluentWindow) :
    def __init__(self, user_info :  dict) :
        super(App, self).__init__()
        
        self.inter_home = Home.Home(self)
        self.inter_video = Video_widg.UTILS_video(parent = self)
        self.joel, self.rudy, self.dawai, self.orlane, self.brice = Profil.Profill("Images/moi.png", "Joel", "https://beta.theb.ai/home", 500, "kappachikatsi@gmail.com", "Promotteur en chef du projet et Etudiant en licence 3 à l'université de Yaoundé 1", [f"Images/im{i}.jpg" for i in range(1, 9)]), QWidget(), QWidget(), QWidget(), QWidget()
        self.song = Music.Music_box()
        self.profil = QWidget()
        self.user = user_info
        self.youtube = YouApp.youtTube()
        self.movie = Stream_Vid.Video_Stream(self)
        self.help, self.parametres = QWidget(), QWidget()

        self.parametres.setObjectName("params")
        self.inter_home.setObjectName('Home'), self.joel.setObjectName('joel')
        self.inter_video.setObjectName('video'), self.song.setObjectName("mucis")
        self.youtube.setObjectName("you"), self.dawai.setObjectName("daw"), self.rudy.setObjectName('rudy')
        self.orlane.setObjectName("orlane"), self.brice.setObjectName('brice')
        self.help.setObjectName("help"), self.movie.setObjectName("movie")
        
        
        self.addSubInterface(
            interface= self.inter_home,
            icon = FIF.HOME, 
            text = "Home")
        
        self.addSubInterface(
            interface = self.inter_video,
            icon = FIF.VIDEO,
            text = "Video Managment"
        )
        self.addSubInterface(
            interface = self.song,
            icon = FIF.MUSIC,
            text = "Music"
        )
        
        self.addSubInterface(
            interface = self.youtube,
            icon = "Images/you.png",
            text = "Parametres",
        )
        
        self.addSubInterface(
            interface = self.movie,
            icon = FIF.MOVIE,
            text = "Movie",
        )
        self.navigationInterface.addSeparator()
        
        self.navigationInterface.addSeparator(position = NavigationItemPosition.BOTTOM)
        
        
        self.addSubInterface(
            interface = self.parametres,
            icon = FIF.SETTING,
            text = "Paramètres",
            position = NavigationItemPosition.BOTTOM
        )
        
        
        self.addSubInterface(
            interface = self.help,
            icon = FIF.HELP,
            text = "Aide",
            position = NavigationItemPosition.BOTTOM
        )
        
        setTheme(Theme.DARK)
        self.setFixedHeight(650)
        self.setFixedWidth(1200)
        self.setWindowIcon(QIcon("Images/logo.png"))
        
        self.youtube.video_widg.visionner.clicked.connect(self.Visionner)
        self.inter_video.video.visionner.clicked.connect(self.visionner_vido)
        
        self.youtube.video_widg.valider.clicked.connect(self.valider_slots_srt)
        
    def valider_slots_srt(self) :
        self.thread_down = Download_.Down(
            server = self.youtube.server,
            file_path = self.youtube.get_url_video(),
            lang_dep = Setup.Setup.lang[self.youtube.video_widg.lang_dep.currentText().lower()],
            lang_cible = Setup.Setup.lang[self.youtube.video_widg.lang_cible.currentText().lower()],
            type = Setup.Setup.Convert(int(self.youtube.video_widg.precision.text())),
            name = self.youtube.video_widg.name.text(),
            endpoint_file = 'video',
            path_srt = f'srt/{self.youtube.video_widg.name.text()}',
            id_user = self.user['id']
        )
        self.thread_down.start()
        self.thread_down.status_code.connect(self.youtube.status_slots)
        self.srt_path = f'srt/{self.youtube.video_widg.name.text()}.srt'
        self.video_path = self.youtube.get_url_video()
        print(self.video_path)
        
    def Visionner(self) :
        self.switchTo(self.movie)
        if self.video_path != "" :
            self.movie.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.video_path)))
        if self.movie.path_srt != "" :
            self.movie.subtitles = SubRipFile.open(self.movie.path_srt)
            self.movie.current_subtitle_index = None
            
    def visionner_vido(self) :
        self.switchTo(self.movie)
        if self.inter_video.video_path != "" :
            self.movie.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.inter_video.video_path)))
        if self.inter_video.srt_path != "" :
            self.movie.subtitles = SubRipFile.open(self.inter_video.srt_path)
            self.movie.current_subtitle_index = None
        
class Formulaire(AcrylicWindow) :
    def __init__(self) :
        super(Formulaire, self).__init__()
        self.central = VBoxLayout(self)
        self.stack = PopUpAniStackedWidget()
        self.connx = Form.Connexion()
        self.enrg = Form.Form()
        
        self.stack.addWidget(self.connx)
        self.stack.addWidget(self.enrg)
        
        self.setWindowIcon(QIcon("Images/logo.png"))
        self.resize(600, 600)
        setTheme(Theme.DARK)
        self.connx.connex.clicked.connect(self.slotsEnr)
        self.server = server.requester(Setup.Setup.get_url(), Setup.Setup.get_port())
        self.central.addWidget(self.stack)
        self.connx.valider.clicked.connect(self.connex_slots)
        self.enrg.back.clicked.connect(self.back_slot)
        self.enrg.valider.clicked.connect(self.sendValider)
        
        self.setStyleSheet(open("setting_interface.qss", 'r').read())
        
        
    def slotsEnr(self) :
        self.stack.setCurrentWidget(self.enrg)
        
    def connex_slots(self) :
        email = self.connx.mail.text()
        password = self.connx.password.text()
        try :
            response = self.server.send_auth('authentification', {'email' : email, 'password' : password})
        except ConnectionError as e:
            InfoBar.warning(
                "Connexion Error",
                "Vous n'êtes pas connecté\n au serveur",
                duration = 3000,
                position = InfoBarPosition.BOTTOM_RIGHT,
                parent = self
            )
            return
        response = dict(response)
        res = list(response.values())
        if all(res) :
            InfoBar.success(
                'Bienvenue',
                "Authentification réussie",
                duration = 3000,
                parent = self
            )
            self.hide()
            user_info : dict = self.server.get_user_by_mail('get_user', email)
            main = App(user_info)
            main.parametres = Settings.Parametres(
                path_name = "Images/im5.jpg",
                name = main.user['name'],
                path_git = '',
                age = main.user['age'],
                nbre_video = 9,
                tokens = main.user['compte'],
                mail = main.user['mail'],
                descript = "Utilisateur de l'applis Video Processing"
            )
            main.show()
        elif not res[0] :
            InfoBar.warning(
                'Désolé',
                "Votre Mail n'existe pas",
                duration = 3000,
                parent = self
            )
        else :
            InfoBar.warning(
                'Désolé',
                "Votre Mot de passe est érroné",
                duration = 3000,
                parent = self
            )
    
    @Decorator.Verification(type = 'add_user')  
    def sendValider(self) :
        name = self.enrg.name.text()
        password = self.enrg.password.text()
        mail = self.enrg.email.text()
        age = int(self.enrg.age.text())
        self.data = {
            'name' : name,
            'password' : password,
            'email' : mail,
            'age' : age,
            'endpoint' : 'add_user'
        }
        try :
            response = self.server.send_new_user_data(**self.data)
        except ConnectionError as e:
            InfoBar.warning(
                "Connexion Error",
                "Vous n'êtes pas connecté\n au serveur",
                duration = 3000,
                position = InfoBarPosition.BOTTOM_RIGHT,
                parent = self
            )
            return
        except ConnectionRefusedError :
            InfoBar.warning(
                "Connexion Error",
                "Vous n'êtes pas connecté\n au serveur",
                duration = 3000,
                position = InfoBarPosition.BOTTOM_RIGHT,
                parent = self
            )
            return
        data = dict(response)
        if data['status'] :
            InfoBar.success(
                title = list(data.keys())[0],
                content = list(data.values())[0],
                duration = 3000,
                position = InfoBarPosition.BOTTOM_RIGHT,
                parent = self
            )
        if not data['status'] :
            InfoBar.warning(
                title = list(data.keys())[0],
                content = list(data.values())[0],
                duration = 3000,
                position = InfoBarPosition.BOTTOM_RIGHT,
                parent = self
            )
        
    def champ_nr(self, content : str) :
        InfoBar.info(
            "Champ Non Rempli",
            content,
            duration = 3000,
            parent = self
        )
        
    def back_slot(self) :
        self.stack.setCurrentWidget(self.connx)

if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    form = Formulaire()
    form.show()
    app.exec()  