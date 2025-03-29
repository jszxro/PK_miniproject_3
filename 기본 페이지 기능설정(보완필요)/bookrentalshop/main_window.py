from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys
from login_page import LoginPage
from main_page import MainPage
from register_page import RegisterPage
from config import DB_CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bukjeokx2")
        self.resize(1000, 700)

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 로그인 페이지와 메인 페이지 추가
        self.login_page = LoginPage(self.stacked_widget, self.set_user_role)
        self.main_page = MainPage(self.stacked_widget)
        self.register_page = RegisterPage(self.stacked_widget)

        self.stacked_widget.addWidget(self.login_page)  # 인덱스 0
        self.stacked_widget.addWidget(self.main_page)   # 인덱스 1
        self.stacked_widget.addWidget(self.register_page)  # 인덱스 2

        # 초기 페이지 설정
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 시작

    def set_user_role(self, role):
        self.main_page.cst_role = role # 사용자 역할 설정
        self.main_page.render_navbar(initial=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
