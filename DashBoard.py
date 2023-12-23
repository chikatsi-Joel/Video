from Diagramme import *
import numpy
import visualisation

class ModelTable(QAbstractTableModel):
    
    def __init__(self, data, headers=None):
        super(ModelTable, self).__init__()
        self._data = data
        self._headers = headers  
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row, col = index.row(), index.column()
            data = self._data[row][col]
            return data
        return None
        
    def rowCount(self, parent):
        return len(self._data)
    
    def columnCount(self, parent):
        k=0
        try :
            k= len(self._data[0])
        except :
            k=0
        return k
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if self._headers and 0 <= section < len(self._headers):
                    return self._headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None 
    
class Make_table(QWidget) :
    def __init__(self) :
        super(Make_table, self).__init__()
        self.central = QVBoxLayout(self)
        self.table_widg = TableWidget()
        self.table_widg.setBorderVisible(True)
        self.table_widg.setBorderRadius(10)
        self.table_widg.setBorderVisible(True)
        self.table_widg.setColumnCount(4)
        self.table_widg.setBorderRadius(10)
        self.table_widg.setHorizontalHeaderLabels(['ID', 'Beta_mode', 'Price', 'Model_type'])
        self.central.addWidget(self.table_widg)
        
        
    def setData(self, headers : list[str] | None, data : list[list[str | int]]) :
        self.table_widg.setRowCount(len(data))
        for i, lis in enumerate(data) :
            for j, val in enumerate(lis) :
                self.table_widg.setItem(i, j, QTableWidgetItem(val if type(val)!= str else str(val)))
        
        if headers is not None :
            self.table_widg.setHorizontalHeaderLabels(headers)

        
class BaseView(QWidget) :
    def __init__(self) :
        super(BaseView, self).__init__()
        self.central = QVBoxLayout(self)
        self.hbox = QGridLayout()
        self.table_user_view = TableWidget()
        self.table_video_view = TableWidget()
        spacer = QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.table_user_view.setBorderVisible(True)
        self.table_user_view.setBorderRadius(10)
        self.table_video_view.setBorderVisible(True)
        self.table_user_view.setColumnCount(6)
        self.table_video_view.setBorderRadius(10)
        
        self.table_video_view.setWordWrap(True)
        self.table_user_view.setRowCount(1)
        self.table_user_view.setHorizontalHeaderLabels(['ID', 'Name', 'Email', 'Age', 'Compte', 'Is_Delete'])
        
        self.table_video_view.setWordWrap(True)
        self.table_video_view.setRowCount(1)
        self.table_video_view.setColumnCount(5)
        self.table_video_view.setHorizontalHeaderLabels(['ID', 'Model_Type', 'Price', 'Beta_mode', 'id_user'])
        
        self.server_user = server.Data_Thread('127.0.0.1', '5000', self)
        self.server_user.start()
                
        setTheme(Theme.DARK)    
        self.setStyleSheet(open("/home/chikatsi/Bureau/INFL3/COURS/TP_INF321/setting_interface.qss", 'r').read())
        self.table_user_view.verticalHeader().hide()
        self.table_user_view.resizeColumnsToContents()
        self.table_user_view.setFixedWidth(510)
        
        self.table_video_view.verticalHeader().hide()
        self.table_video_view.resizeColumnsToContents()
        self.table_video_view.setFixedWidth(500)
        self.table_video_view.setColumnWidth(3, 100)
        
        self.central.addLayout(self.hbox), self.central.addSpacerItem(spacer)
        self.hbox.addWidget(SubtitleLabel('Liste Total User'), 0, 0, Qt.AlignmentFlag.AlignCenter), self.hbox.addWidget(SubtitleLabel('Liste Total Video'), 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.hbox.addWidget(self.table_user_view, 1, 0)
        self.hbox.addWidget(self.table_video_view, 1, 1)
        self.hbox.setHorizontalSpacing(80)
        self.resize(1005, 600)
        
        for i in range(6) :
            if i < 5 :
                self.table_video_view.setColumnWidth(i, 100)
            self.table_user_view.setColumnWidth(i, 100 if (i !=1 and i != 2) else 200)

    

class User (QWidget) :
    def __init__(self) :
        super(User, self).__init__()
        self.central = VBoxLayout(self)
        self.base = BaseView()
        self.title = TitleLabel('Welcome in our DashBoard')
        self.scroll_area = SmoothScrollArea()
        self.viewWidget = QWidget()
        self.vbox = VBoxLayout(self.viewWidget)
        setTheme(Theme.DARK)    
        grid = QGridLayout()
        titl = SubtitleLabel("Liste Des Videos Vues Le User Selectionné")
        self.table_user_video = Make_table()
        vb = QVBoxLayout()
        vb.addWidget(titl, 0, Qt.AlignmentFlag.AlignCenter), vb.addWidget(self.table_user_video)
        vb.setSpacing(0)
        
        self.setStyleSheet(open("/home/chikatsi/Bureau/INFL3/COURS/TP_INF321/setting_interface.qss", 'r').read())
        self.vbox.addWidget(self.base, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vbox.addLayout(grid), self.vbox.addLayout(vb)
        self.central.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.viewWidget)
        self.resize(1100, 510)
        self.central.addWidget(self.title, 0, Qt.AlignmentFlag.AlignHCenter)
        self.central.addWidget(self.scroll_area)
        
        self.base.table_user_view.cellClicked.connect(self.cellClick)
        
    def cellClick(self, index : int) :
        id_user = int(self.base.table_user_view.item(index, 0).text())
        liste_video = [vide for vide in visualisation.database.Video.get_all_video() if vide.id_user == id_user]
        header = ['id', 'beta_mode', 'price', 'model type']
        data = [[str(vide.id), str(vide.beta_mode), str(vide.price), vide.model_type] for vide in liste_video]
        self.table_user_video.setData(header, data)
        
        
        
class MainDashBoard(FluentWindow) :
    def __init__(self) :
        super(MainDashBoard, self).__init__()
        self.user = User()
        self.visua = visualisation.MainWindow()
        self.user.setObjectName("user")
        self.visua.setObjectName("sdc")
        self.connec_val = False
        self.user.base.server_user.connection_error.connect(self.no_connection)
        self.user.base.server_user.conn.connect(self.connxion)
        
        self.addSubInterface(
            interface=self.user,
            icon = FIF.CONNECT,
            text = "User Gestion",
        )
        
        
        self.addSubInterface(
            interface= self.visua,
            icon = FIF.CODE,
            text = 'Carte'
        )
        self.setFixedSize(1200, 640)
        self.timer = QTimer()
        self.timer.timeout.connect(self.visualisation)
        self.timer.start(20000)
        
  
    def visualisation(self) :
        self.visua.mise_a_jour()
        self.user.base.server_user.start()
    
    def connxion(self) :
        if not self.connec_val :
            InfoBar.success(
                'Connexion Réussie.',
                "Vous êtes à présent Connecté\n Au serveur Proxy",
                duration = 4000,
                parent = self
            )  
            self.connec_val = True

    def no_connection(self) :
        self.connec_val = False
        InfoBar.warning(
            'Erreur de Connexion',
            "Vous n'êtes pas connecté au serveur\nVotre visualisation ne peux être \nmise à jour..",
            duration = 4000,
            parent = self
        )
if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainDashBoard()
    w.show()
    app.exec()