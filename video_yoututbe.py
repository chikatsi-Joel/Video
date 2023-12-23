import typing, os
from PyQt5.QtCore import QObject
from pytube import YouTube
from qfluentwidgets import InfoBar, InfoBarPosition
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import youtube_dl


import os
from pytube.exceptions import RegexMatchError

from pytube import YouTube

def Download(url_video : str, url_save : str, file_name : str):
    youtubeObject = YouTube(url_video)
    youtubeObject = youtubeObject.streams.get_lowest_resolution()
    youtubeObject.download(
        url_save,
        filename = file_name + '.mp4'
    )
    
    
class Youtt(QThread) :
    endDownload = pyqtSignal(bool)
    lienInexistant = pyqtSignal()
    erreur = pyqtSignal(str)
    
    def __init__(self, url_video : str, name : str, destination : str | None = None, resolution : str = '720p',  parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.url = url_video
        self.destination = destination
        self.resol = resolution
        self.name = name
        
    def run(self) :
        try :
            Download(
                url_video = self.url,
                file_name = self.name,
                url_save = self.destination,
            )
            self.endDownload.emit(True)
        except RegexMatchError :
            self.lienInexistant.emit()
        except Exception as e :
            self.erreur.emit(str(e))