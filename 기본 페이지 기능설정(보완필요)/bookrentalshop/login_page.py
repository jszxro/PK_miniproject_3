from PyQt5.QtWidgets import QWidget, QSizePolicy, QFrame, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import cx_Oracle
from main_page import MainPage 
from register_page import RegisterPage
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# image_path = os.path.join(BASE_DIR, "ref", "book_image.jpg")
# image_path_css = image_path.replace("\\", "/")
icon_path = os.path.join(BASE_DIR, "ref", "icon_image.png")
icon2_path = os.path.join(BASE_DIR, "ref", "icon_image2.png")

from config import DB_CONFIG

class LoginPage(QWidget):
    def __init__(self, stacked_widget, set_cst_role):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.set_cst_role = set_cst_role
        self.initUI()

    def clear_inputs(self):
        self.email_input.clear()
        self.password_input.clear()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 왼쪽 영역
        image_side = QFrame()
        image_side.setStyleSheet("""
            QFrame {
                background-color: #CDE8B4;
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
        image_side.setMinimumWidth(500)

        # 말풍선 텍스트 라벨 (픽셀 느낌)
        speech_label = QLabel("""로그인을 해주세요 
                                                ‧₊˚ ⭒ ˚˖°⋆ """)
        speech_label.setFixedSize(450, 200)  # 너비 400, 높이 100 픽셀
        speech_label.setStyleSheet("""
            background-color: white;
            border: 3px solid black;
            border-radius: 12px;
            font-size: 22px;
            font-weight: bold;
            padding: 12px;
        """)
        speech_label.setAlignment(Qt.AlignCenter)
        speech_label.setFont(QFont("D2Coding", 16, QFont.Bold))
        speech_label.setAlignment(Qt.AlignCenter)
        speech_label.setWordWrap(True)  # 👉 줄바꿈 허용!

        # 아이콘 (곰돌이)
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon2_path).scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(350, 350)  # 창 크기 조절에도 이미지 고정
        icon_label.setAlignment(Qt.AlignCenter)


        # 말풍선 + 아이콘 수직 배치
        speech_layout = QVBoxLayout()
        speech_layout.setAlignment(Qt.AlignHCenter)
        speech_layout.addWidget(speech_label)
        speech_layout.addSpacing(10)
        speech_layout.addWidget(icon_label)

        # 좌측 전체에 추가
        left_layout = QVBoxLayout(image_side)
        left_layout.setContentsMargins(30, 30, 30, 30)
        left_layout.addStretch(1)
        left_layout.addLayout(speech_layout)
        left_layout.addStretch(1)

        # 오른쪽 로그인 폼 영역
        form_container = QWidget()
        form_container.setStyleSheet("background-color: white;")
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)  # 👉 중앙 정렬!
        form_layout.setContentsMargins(60, 60, 60, 60)
        form_layout.setSpacing(20)

        # 내부 폼 구성
        title = QLabel("로그인")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("이메일 입력")
        self.email_input.setFixedWidth(600)
        self.email_input.setStyleSheet("padding: 15px; border-radius: 10px; border: 1px solid #ccc;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("비밀번호 입력")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(600)
        self.password_input.setStyleSheet("padding: 15px; border-radius: 10px; border: 1px solid #ccc;")

        login_btn = QPushButton("로그인")
        login_btn.setFixedWidth(600)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #CDE8B4;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4dca4;
            }
        """)
        login_btn.clicked.connect(self.verify_credentials)

        # 홈으로 가기 버튼
        back_button = QPushButton("홈으로 가기")
        back_button.setFixedWidth(600)  # 로그인 버튼과 동일한 너비 설정
        back_button.setStyleSheet("""
            QPushButton {
                padding: 15px;
                border-radius: 10px;
                background-color: #FFCCCC;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f2a6a6;
            }
        """)
        back_button.clicked.connect(self.go_home)  # 버튼 클릭 시 메인 페이지로 이동

        register_label = QLabel("<a href='#'>회원가입</a>  |  ID/PW 찾기  |  관리자 로그인")
        register_label.setStyleSheet("color: gray; font-size: 14px")
        register_label.setAlignment(Qt.AlignCenter)
        register_label.linkActivated.connect(self.show_register_page)

        # 레이아웃에 추가
        form_layout.addWidget(title)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_btn)
        form_layout.addWidget(back_button)  # 로그인 버튼 아래에 홈으로 가기 버튼 추가
        form_layout.addWidget(register_label)

        # 전체 배경색
        self.setStyleSheet("background-color: #f2f2f2;")

        # 메인 레이아웃에 이미지와 폼 추가
        main_layout.addWidget(image_side)
        main_layout.addWidget(form_container)

        # 👉 비율 맞추기
        main_layout.setStretch(0, 7)  # 이미지
        main_layout.setStretch(1, 3)  # 폼 (50:50)

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
                role = result[0]
                self.set_cst_role(role)
                if role == 'admin':
                    QMessageBox.information(self, "관리자 로그인", "관리자님, 환영합니다!")
                else:
                    QMessageBox.information(self, "로그인 성공", "Bukjeokx2에 오신 것을 환영합니다 :)")

                main_page = self.stacked_widget.widget(1)
                main_page.render_navbar(initial=False)
                self.stacked_widget.setCurrentIndex(1)
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
        """홈으로 가기 버튼 클릭 시 메인 페이지로 이동"""
        self.stacked_widget.setCurrentIndex(1)

    def show_register_page(self):
        self.stacked_widget.setCurrentIndex(2)