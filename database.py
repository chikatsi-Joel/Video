from sqlalchemy import Column, Integer, Float, String, create_engine, Boolean, DateTime, exc
from sqlalchemy.orm import sessionmaker, declarative_base
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import sys

engine = create_engine('sqlite:///Database/database.db')
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()



class User(Base) :
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(60), nullable = False)
    mail  = Column(String(50), nullable = False, unique = True)
    password = Column(String(20), nullable = False)
    compte = Column(Float, nullable = False, default = 0)
    is_delete = Column(Boolean, nullable = False, default = False)
    age = Column(Integer, nullable = False)
    nbre_video = Column(Integer, nullable = False, default = True)
    
    @classmethod
    def addUser(cls, name : str, mail : str, password : str, age : int) :
        try :
            session.add(User(name = name, mail = mail, password = password, age = age))
            session.commit()
        except exc.IntegrityError:
            raise AttributeError("Email déjà utilisé..")
        
    @classmethod
    def delete_user(cls, email : str) :
        user = session.query(User).filter_by(mail = email).first()
        user.is_delete = True
        session.commit()
        
    @classmethod
    def charger_compte(cls, id_user : int, compte : float) :
        user = session.query(User).filter_by(id = id_user).first()
        user.compte += compte
        session.commit() 

    @classmethod
    def change_password(cls, email : str, password : str, last_password : str) :
        user = session.query(User).filter_by(mail = email).first()
        if not user.is_delete :
            if user.password != last_password :
                raise InterruptedError("Mot de passe invalide")
            user.password = password
            session.commit()
        
    @classmethod 
    def change_mail(cls, email : str, new_mail : str) :
        user = session.query(User).filter_by(mail = email).first()
        if not user.is_delete :
            user.mail = new_mail
            session.commit()
        
    @classmethod
    def isDelete(cls, email : str) -> bool:
        return session.query(User).filter_by(mail = email).first().is_delete

    @classmethod
    def get_all_user(cls) :
        return session.query(User).all()
    
    @classmethod
    def get_user_by_mail(cls, email : str) :
        user = session.query(User).filter_by(mail = email).first()
        if user and not user.is_delete :
            return user
        return None
    
    def __repr__(self) :
        return f'-ID : {self.id} Name : {self.name}  password : {self.password}'
    
class Video(Base) :
    __tablename__ = 'video'
    id = Column(Integer, nullable= False, primary_key= True)     
    beta_mode = Column(Boolean, nullable=False, default= False)
    price = Column(Float, nullable=False, default= 0.0)
    model_type = Column(String(30), nullable= False, default = 'tiny')
    id_user = Column(Integer, nullable= False)
    
    @classmethod
    def add_video(cls, beta_mode : bool, price : float, model_type: str, id_user : int) :
        session.add(Video(beta_mode = beta_mode, price = price, model_type = model_type, id_user = id_user))
        session.commit()

    @classmethod
    def get_all_video_user_see(cls, id_user : int) :
        liste_video = session.query(Video).filter_by(id_user = id_user)
        return liste_video.all()
    
    @classmethod
    def get_all_video(cls) :
        liste =  session.query(Video).all()
        return liste
    
    def __repr__(self) :
        return f'-ID : {self.id} Beta_Mode : {self.beta_mode}  price : {self.price}  Model_type : {self.model_type}  id_user : {self.id_user}'
    

