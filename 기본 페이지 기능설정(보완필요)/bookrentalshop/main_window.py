from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from login_page import LoginPage
from main_page import MainPage
from register_page import RegisterPage
from config import DB_CONFIG
from search_page import SearchPage
from list_page import ListPage



class MainWindow(QMainWindow): # 메인 윈도우 클래스
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("Bukjeokx2")
        self.resize(1000, 700)

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget() 
        self.setCentralWidget(self.stacked_widget) 

        # 로그인 페이지와 메인 페이지 추가
        self.login_page = LoginPage(self.stacked_widget, self.set_user_role) # 로그인 페이지
        self.main_page = MainPage(self.stacked_widget) # 메인 페이지
        self.register_page = RegisterPage(self.stacked_widget) # 회원가입 페이지
        self.search_page = SearchPage(self.stacked_widget) # 검색 페이지
        self.list_page = ListPage(self.stacked_widget) # 도서 리스트 페이지

        self.stacked_widget.addWidget(self.login_page)  # 인덱스 0
        self.stacked_widget.addWidget(self.main_page)   # 인덱스 1
        self.stacked_widget.addWidget(self.register_page)  # 인덱스 2
        self.stacked_widget.addWidget(self.search_page)  # 인덱스 3
        self.stacked_widget.addWidget(self.list_page) # 인덱스 4

        # 초기 페이지 설정
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 시작

    def set_user_role(self, role):
        self.main_page.cst_role = role # 사용자 역할 설정
        self.main_page.render_navbar(initial=False) # 네비게이션 바 렌더링

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())