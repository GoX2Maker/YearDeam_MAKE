import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic   # ui 파일을 사용하기 위한 모듈 import

#UI파일 연결 코드
UI_class = uic.loadUiType("main.ui")[0]


class WindowClass(QMainWindow, UI_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_selectedIMG.clicked.connect(self.btn_selectedIMG_clicked)

    def btn_selectedIMG_clicked(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        qPixmapVar = QPixmap()
        qPixmapVar.load(fname[0])
        qPixmapVar = qPixmapVar.scaled(self.img_view.width(), self.img_view.height(), Qt.KeepAspectRatio)
        self.img_view.setPixmap(qPixmapVar)

    


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()