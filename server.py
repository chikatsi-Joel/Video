import requests, database
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from requests import exceptions

class Data_Thread (QThread):
    end_down = pyqtSignal(int)
    connection_error = pyqtSignal()
    conn = pyqtSignal()
    def __init__(self, host : str, port : str, parent : QWidget) :
        super(Data_Thread, self).__init__(parent)
        self.port = port
        self.host = host
        self.paren = parent
        self.data_user = None
        
    def download_bd(self) :
        response = requests.post("http://" + self.host + ':' + self.port + '/get_db')
        open("Database/database.db", 'wb').write(response.content)
        
    def run(self) :
        try :
            self.download_bd()
            self.conn.emit()
        except exceptions.ConnectionError as e :
            self.connection_error.emit()
            
        users = database.User.get_all_user()
        self.paren.table_user_view.setRowCount(len(users))
        for i, user in enumerate(users) :
            self.paren.table_user_view.setItem(i, 0, QTableWidgetItem(str(user.id)))
            self.paren.table_user_view.setItem(i, 1, QTableWidgetItem(user.name))
            self.paren.table_user_view.setItem(i, 2, QTableWidgetItem(user.mail))
            self.paren.table_user_view.setItem(i, 3, QTableWidgetItem(str(user.compte)))
            self.paren.table_user_view.setItem(i, 4, QTableWidgetItem(str(user.age)))
            self.paren.table_user_view.setItem(i, 5, QTableWidgetItem(str(user.nbre_video)))
            self.paren.table_user_view.setItem(i, 6, QTableWidgetItem(str(user.is_delete)))
            
        videos = database.Video.get_all_video()
        self.paren.table_video_view.setRowCount(len(videos))
        for i, video in enumerate(videos) :
            self.paren.table_video_view.setItem(i, 0, QTableWidgetItem(str(video.id)))
            self.paren.table_video_view.setItem(i, 1, QTableWidgetItem(video.model_type))
            self.paren.table_video_view.setItem(i, 2, QTableWidgetItem(str(video.price)))
            self.paren.table_video_view.setItem(i, 3, QTableWidgetItem(str(video.beta_mode)))
            self.paren.table_video_view.setItem(i, 4, QTableWidgetItem(str(video.id_user)))
