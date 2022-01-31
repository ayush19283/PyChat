
from pickle import NONE
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QScrollArea, QVBoxLayout, QHBoxLayout, QSplitter, QStyleFactory, QWidget, QLabel, QLineEdit,QDesktopWidget, QGraphicsDropShadowEffect,
                             QTextEdit, QGridLayout, QApplication, QInputDialog, QPushButton, QFrame, QSplashScreen, QMessageBox, QFileDialog)

from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QPlainTextEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy)
from PyQt5.QtCore import Qt

import sys
import requests
import threading

USER=None
CHAT=None
val1=None
MAJ=None
title_area=None

host="https://chatstorage.herokuapp.com/"

usr_name=None

class check_msg(QtCore.QThread):
    c_value=QtCore.pyqtSignal(list)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            if val1:
                # print(1)
                try:
                    ab=requests.get(f"{host}pwd=1234/newmessage/{val1}/{usr_name}").json()
                except:
                    pass
                    # print('3')
                # print(ab)
                # ab=ab.json()
                
                
                # try:
                if ab:
                    u=requests.get(f"{host}pwd=1234/conversation/{val1}/{usr_name}").json()
                    self.c_value.emit(u)
                    
                    
                else:
                    continue
                    


class user(QScrollArea):
    def __init__(self,parent,width,height,a):
        super().__init__(parent)
        self.widget=QWidget()
        self.vbox=QVBoxLayout()
        # a='button'
        for i in a:
            bt=QPushButton(i)
            bt.setStyleSheet("""background-color: rgb(34,139,34);""")
            bt.setFixedSize(340,50)
            bt.clicked.connect(lambda evt,val=i : self.clicked(val))
                    # bt.move(0,i*50)
            self.vbox.addWidget(bt)
        self.widget.setLayout(self.vbox)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

    def clicked(self,val):
        global val1
        val1=val
        print("value is ",val)
        title_area.setText(val)
        d=requests.get(f"{host}pwd=1234/conversation/{usr_name}/{val}").json()
        d1=[]
        # for i in d:
            # d1.append(i[0])
        # print(d1)
        CHAT.load(d)
        
        
    def click(self,val):
        d=requests.get(f"{host}pwd=1234/conversation/{usr_name}/{val}").json()
        CHAT.load(d)

     
class chat(QScrollArea):
    def __init__(self,parent,width=None,height=None,a=None):
        super().__init__(parent)
        self.load(a)
        

    def load(self,a):
        self.widget=QWidget()
        self.vbox=QVBoxLayout()
        # lb1=QLabel()
        # lb1.setStyleSheet("background-color: rgb(255,211,0);")
        # j=requests.get(f'{host}pwd=1234/conversation/{usr_name}/{val1}').json()
        # h=[]
        # k=0
        # for i in j:
            # h.append(i[1])
        # print(h)
        for i in a:
            # lb=QLabel(i)
            # lb.setFixedSize(200,30)
            
            # lb.setStyleSheet("background-color: rgb(255,211,0);")
            # lb.setWordWrap(True)
            # self.vbox.addWidget(lb)
            
            lb=QLabel("")
            lb1=QLabel(i[0],lb)
            # # lb1.setMinimumHeight(30)
            # # lb1.setMaximumWidth(300)
            lb1.setWordWrap(True)
            if i[1]==usr_name:
                lb1.setStyleSheet("background-color: rgb(135,206,235);")
                lb1.move(500,0)
            else:
                lb1.setStyleSheet("background-color: rgb(235,237,131);")
                lb1.move(0,0)
                
            lb.setMinimumSize(890,40)
            
            self.vbox.addWidget(lb)
            # k=k+1
        self.widget.setLayout(self.vbox)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    # def ld_chat(self,a)




class MainWindow(QMainWindow):
    def __init__(self):
        global CHAT,USER,MAJ
        super().__init__()

        self.widget=QWidget()
        self.vbox=QVBoxLayout()
        self.frame=QFrame()
        self.scroll=QScrollArea()

        self.width = QDesktopWidget().screenGeometry(-1).width()
        self.height = QDesktopWidget().screenGeometry(-1).height()

        self.frame.setStyleSheet("QFrame{background-color: rgb(250,218,221)}")
        self.frame.setFixedSize(self.width,self.height)
        self.vbox.addWidget(self.frame)
        MAJ=self.frame

        self.dvl= QLabel("developed by Ankit Raj and Ayush Sharma",self.frame)
        # self.dvl.setStyleSheet("background-color: (164,116,73);")
        self.dvl.setFixedSize(550,60)
        self.dvl.move(800,self.height-200)
        self.dvl.setAlignment(Qt.AlignCenter)
        font = self.dvl.font()
        font.setPointSize(15)
        self.dvl.setFont(font)

        self.lbl= QLabel("MESSAGING APP",self.frame)
        # self.dvl.setStyleSheet("background-color: (164,116,73);")
        self.lbl.setFixedSize(550,60)
        self.lbl.move(300,self.height-700)
        self.lbl.setAlignment(Qt.AlignCenter)
        font = self.lbl.font()
        font.setPointSize(25)
        self.lbl.setFont(font)

        self.button = QPushButton('>>', self.frame)
        self.button.move(1110,self.height-500)
        self.button.setStyleSheet('background-color: rgb(204,0,102);')
        self.button.resize(70,50)
        self.button.clicked.connect(lambda evt: self.on())


        self.textbox = QLineEdit(self.frame)
        self.textbox.move(200, self.height-500)
        self.textbox.resize(900,50)
        self.textbox.setPlaceholderText("Enter Username to log in")
        self.textbox.returnPressed.connect(self.button.click)


       
        self.add_but = QPushButton("create new account",self.frame)
        self.add_but.move(400,self.height-200)
        self.add_but.setStyleSheet('background-color: rgb(138,3,3);')
        self.add_but.resize(200,60)
        self.add_but.clicked.connect(lambda evt: self.adduser())

        self.widget.setLayout(self.vbox) 

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.scroll)

        self.showMaximized()


        
    def ghj(self):
        global CHAT,USER,title_area
        
        self.c_title=QLabel("chat application",self.frame)
        self.c_title.setFixedSize(self.frame.width(),50)
        self.c_title.move(0,0)
        self.c_title.setAlignment(Qt.AlignCenter)
        font = self.c_title.font()
        font.setPointSize(15)
        self.c_title.setFont(font)
        self.c_title.show()

        self.chat=QLabel("chat",self.frame)
        self.chat.setStyleSheet("""background-color: rgb(135,206,235); """)
        self.chat.setFixedSize(1000,90)
        self.chat.move(355,50)
        self.chat.setAlignment(Qt.AlignCenter)
        font = self.chat.font()
        font.setPointSize(15)
        self.chat.setFont(font)
        self.chat.show()
        title_area=self.chat
       

        self.srch=QPushButton("ADD",self.frame)
        self.srch.setStyleSheet('background-color: rgb(255,176,66);')
        self.srch.setFixedSize(80,40)
        self.srch.move(250,50)
        self.srch.show()


        self.textbox2=QLineEdit(self.frame)
        self.textbox2.move(10,50 )
        self.textbox2.resize(230,40)
        self.textbox2.show()
        self.textbox2.setPlaceholderText("add friends")
        self.srch.clicked.connect(lambda evt: self.add_friend())
        self.textbox2.returnPressed.connect(self.srch.click)


    

        # ch=[]
        # ch1=requests.get(f"{host}pwd=1234/allmessage").json()
        ch1=[['welcome to chat application',1]]

        # for i in ch1:
            # ch.append(i[0])

        self.chats=chat(self.frame,self.frame.width(),self.frame.height(),ch1)
        self.chats.move(self.frame.width()/3.84, self.frame.height()/14+70)
        self.chats.setFixedSize(self.frame.width() - self.frame.width()/3.65-40, self.frame.height()/1.13-120)
        CHAT=self.chats

        self.chats.show()

        
        
        # def chk(self):
        #     print('12')
        #     if val1:
        #         d=requests.get(f"{host}pwd=1234/newmessage/{val1}/{usr_name}").json()
        #         if d:
        #             u=[]
        #             for i in d:
        #                 u.append(i[1:])
        #             CHAT.load(u)

        # self.t1=threading.Thread(self,target=chk)
        # self.t1.start()

        self.button1 = QPushButton('>>', self.frame)
        self.button1.move(1205,self.height-100)
        self.button1.setStyleSheet('background-color: rgb(204,0,102);')
        self.button1.resize(70,40)
        self.button1.clicked.connect(lambda evt: self.on_click())
        self.button1.show()

        self.textbox1 = QLineEdit(self.frame)
        self.textbox1.move(355, self.height-100)
        self.textbox1.resize(850,40)
        self.textbox1.show()
        self.textbox1.setPlaceholderText("enter message !")
        self.textbox1.returnPressed.connect(self.button1.click)

        self.usr_ar()

        # if self.textbox.text():
        #     if self.textbox.text()[-1]=='\n':
        #         self.on_click()

        

        self.thread=check_msg()
        self.thread.c_value.connect(self.update)
        self.thread.start()

    def add_friend(self):
        b=self.textbox2.text()
        self.textbox2.setText("")
        usr=requests.get(f"{host}pwd=1234/username").json()
        
        for i in usr:
            if b in i:
                requests.get(f"{host}pwd=1234/{usr_name}/hi/to/{b}")
        self.usr_ar()
            

    def ad(self):
        print('hi')
        b=self.textbox1.text()
        self.textbox1.setText("")
        temp=0
        us=requests.get(f"{host}pwd=1234/username").json()
        for i in us:
            if b in i:
                temp=1
            
        if temp==0:
            requests.get(f'{host}pwd=1234/add_username={b}')       
        else:
            QMessageBox.about(self, "Title", "user name not unique")


    def adduser(self):
        self.textbox1 = QLineEdit(self.frame)
        self.textbox1.move(200, 500)
        self.textbox1.resize(400,50)
        self.textbox1.show()
        self.textbox1.setPlaceholderText("enter username")

        # print(self.textbox.text())

        self.but1=QPushButton("add",self.frame)
        self.but1.move(610,500)
        self.but1.resize(70,50)
        self.but1.show()
        self.but1.clicked.connect(lambda evt: self.ad())

       
    def usr_ar(self):
        global USER
        l=[]
        a=requests.get(f"{host}pwd=1234/allmessage").json()

       
        for i in range(len(a)):
            if a[i][1]==usr_name:
                if a[i][2] not in l:
                    l.append(a[i][2])

            if a[i][2]==usr_name:
                if a[i][1] not in l:
                    l.append(a[i][1])
            
        print(l)
        self.area = user(self.frame, self.frame.width(), self.frame.height(),l)
        self.area.move(0, self.frame.height()/8+40)
        self.area.setFixedSize(self.frame.width()/3.84, self.frame.height()/1.13-30)
        USER=self.area   
        self.area.show()
   
    


       
    def on_click(self):
        textboxValue = self.textbox1.text()
        print(textboxValue)
        self.textbox1.setText(" ")
        requests.get(f"{host}pwd=1234/{usr_name}/{textboxValue}/to/{val1}")
        USER.click(val1)


    def on(self):
        global usr_name
        usr_name=self.textbox.text()
        # QMessageBox.about(self, "Title", f"{usr_name}")
        z1=[]
        z=requests.get(f"{host}pwd=1234/username").json()
        for i in z:
            z1.append(i[0])
        print(z1)

        if self.textbox.text() in z1:
            usr_name=self.textbox.text()
            self.textbox.setText(" ")
            self.ghj()

        else:
            QMessageBox.about(self, "Title", "user name not found")

    def update(self,val):
        print(2)
        CHAT.load(val)
        


        
   



def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    # t1=threading.Thread(target=run)
    # t1.start()
    sys.exit(app.exec_())

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    try:
        print(exctype, value, traceback)
            
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1)
    except:
        pass
   
if __name__ == '__main__':
    sys.excepthook = exception_hook
    main()


