from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QCheckBox, QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from config import DB_CONFIG  # DB_CONFIG 임포트
import cx_Oracle as oci  # cx_Oracle 추가
import re
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# image_path = os.path.join(BASE_DIR, "ref", "book_image.jpg")
# image_path_css = image_path.replace("\\", "/")
icon_path = os.path.join(BASE_DIR, "ref", "icon_image.png")
icon2_path = os.path.join(BASE_DIR, "ref", "icon_image2.png")

class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 왼쪽 배경 영역
        image_side = QFrame()
        image_side.setStyleSheet("""
            QFrame {
                background-color: #CDE8B4;
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
        image_side.setMinimumWidth(500)

        # ⛅️ 말풍선 라벨
        speech_label = QLabel("""회원가입을 해주세요 
                                       ₊˚ ⭒ ˚˖°⋆ """)
        speech_label.setFixedSize(450, 200)
        speech_label.setStyleSheet("""
            background-color: white;
            border: 3px solid black;
            border-radius: 12px;
            font-size: 22px;
            font-weight: bold;
            padding: 12px;
        """)
        speech_label.setFont(QFont("D2Coding", 16, QFont.Bold))
        speech_label.setAlignment(Qt.AlignCenter)
        speech_label.setWordWrap(True)

        # 🐹 곰돌이 아이콘
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon2_path).scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(350, 350)
        icon_label.setAlignment(Qt.AlignCenter)

        # 수직 레이아웃으로 말풍선 + 아이콘
        speech_layout = QVBoxLayout()
        speech_layout.setAlignment(Qt.AlignHCenter)
        speech_layout.addWidget(speech_label)
        speech_layout.addSpacing(10)
        speech_layout.addWidget(icon_label)

        # 전체 이미지 영역에 추가
        left_layout = QVBoxLayout(image_side)
        left_layout.setContentsMargins(30, 30, 30, 30)
        left_layout.addStretch(1)
        left_layout.addLayout(speech_layout)
        left_layout.addStretch(1)
        # 오른쪽 폼 영역
        form_container = QWidget()
        form_container.setStyleSheet("background-color: white;")
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(60, 60, 60, 60)
        form_layout.setSpacing(20)

        # 제목
        title = QLabel("회원가입")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)

        # 입력 필드
        self.inputs = {}
        fields = ["이름", "주소", "전화번호", "이메일", "비밀번호", "비밀번호 확인"]
        for field in fields:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"{field} 입력")
            input_field.setFixedWidth(600)
            input_field.setStyleSheet("padding: 15px; border-radius: 10px; border: 1px solid #ccc;")
            if "비밀번호" in field:
                input_field.setEchoMode(QLineEdit.Password)
            form_layout.addWidget(input_field)
            self.inputs[field] = input_field

        # 관리자 체크박스
        self.admin_check = QCheckBox("관리자로 가입")
        form_layout.addWidget(self.admin_check)

        # 회원가입 버튼
        register_btn = QPushButton("회원가입")
        register_btn.setFixedWidth(600)
        register_btn.setStyleSheet("""
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
        register_btn.clicked.connect(self.register)
        form_layout.addWidget(register_btn)

        # 홈으로 / 뒤로가기 버튼
        for text, slot in [("홈으로", self.go_home), ("뒤로가기", self.go_back)]:
            btn = QPushButton(text)
            btn.setFixedWidth(600)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFCCCC;
                    padding: 15px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #f7bdbd;
                }
            """)
            btn.clicked.connect(slot)
            form_layout.addWidget(btn)

        # 전체 배경 설정
        self.setStyleSheet("background-color: #f2f2f2;")

        # 메인 레이아웃에 이미지와 폼 추가
        main_layout.addWidget(image_side)
        main_layout.addWidget(form_container)

        # 비율 맞추기
        main_layout.setStretch(0, 7)
        main_layout.setStretch(1, 3)

    # 회원가입 기능
    def register(self):
        data = {key: field.text().strip() for key, field in self.inputs.items()}

        if not data["이름"] or not data["비밀번호"]:
            QMessageBox.warning(self, "경고", "이름 또는 비밀번호는 필수입니다!")
            return

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data["이메일"]):
            QMessageBox.warning(self, "경고", "올바른 이메일 형식을 입력하세요!")
            return

        if self.is_email_exists(data["이메일"]):
            QMessageBox.warning(self, "경고", "이미 등록된 이메일입니다!")
            return

        if data["비밀번호"] != data["비밀번호 확인"]:
            QMessageBox.warning(self, "경고", "비밀번호가 일치하지 않습니다!")
            return

        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("SELECT NVL(MAX(CST_ID), 0) + 1 FROM CUSTOMERINFO")
            new_id = cursor.fetchone()[0]
            role = 'admin' if self.admin_check.isChecked() else 'user'

            cursor.execute("""
                INSERT INTO CUSTOMERINFO (CST_ID, CST_NAMES, CST_ADDRESS, CST_MOBILE, CST_EMAIL, CST_PWD, CST_ROLE)
                VALUES (:1, :2, :3, :4, :5, :6, :7)
            """, (new_id, data["이름"], data["주소"], data["전화번호"], data["이메일"], data["비밀번호"], role))

            conn.commit()
            QMessageBox.information(self, "성공", "회원가입이 완료되었습니다.")
            self.stacked_widget.setCurrentIndex(0)

        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    def is_email_exists(self, email):
        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM CUSTOMERINFO WHERE CST_EMAIL = :1", (email,))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def go_home(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)