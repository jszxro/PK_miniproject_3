from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import cx_Oracle
from main_page import MainPage 
from register_page import RegisterPage

# DB 연결 설정
DB_CONFIG = {
    'user': 'bookrentalshop',
    'password': '12345',
    'dsn': cx_Oracle.makedsn('210.119.14.73', 1521, service_name='XE')
}


class LoginPage(QWidget):
    def __init__(self, stacked_widget,set_cst_role):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.set_cst_role = set_cst_role
        self.initUI()

    def clear_inputs(self):
        # 로그인 입력 필드 초기화
        self.email_input.clear()
        self.password_input.clear()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setSpacing(15)

        title = QLabel("로그인")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("이메일 입력")
        self.email_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("비밀번호 입력")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc;")

        login_button = QPushButton("로그인")
        login_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #CDE8B4;")
        login_button.clicked.connect(self.verify_credentials)

        home_button = QPushButton("홈으로")
        home_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #CDE8B4;")
        home_button.clicked.connect(self.go_home)

        register_label = QLabel("<a href='#'>회원가입</a>  |  ID/PW 찾기  |  관리자 로그인")
        register_label.setOpenExternalLinks(False)
        register_label.linkActivated.connect(self.show_register_page)
        register_label.setAlignment(Qt.AlignCenter)
        register_label.setStyleSheet("color: gray; font-size: 22px")

        layout.addWidget(title)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(home_button)
        layout.addWidget(register_label)

        self.setLayout(layout)

    def verify_credentials(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        try:
            connection = cx_Oracle.connect(**DB_CONFIG)
            cursor = connection.cursor()

            query = """
                SELECT CST_ROLE FROM CUSTOMERINFO
                WHERE CST_EMAIL = :email AND CST_PWD = :password
            """
            cursor.execute(query, {'email': email, 'password': password})
            result = cursor.fetchone()

            if result:
                role = result[0] # 사용자 역할 (admin 또는 user)
                self.set_cst_role(role)  # 사용자 역할 설정
                QMessageBox.information(self, "로그인 성공", "환영합니다!")
                main_page = self.stacked_widget.widget(1)  # 메인 페이지 가져오기
                main_page.render_navbar(initial=False)  # 네비게이션 바 업데이트
                self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환
            else:
                QMessageBox.warning(self, "로그인 실패", "이메일 또는 비밀번호가 잘못되었습니다.")

        except cx_Oracle.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def go_home(self):
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환

    def show_register_page(self):
        self.stacked_widget.setCurrentIndex(2)  # 회원가입 페이지로 전환