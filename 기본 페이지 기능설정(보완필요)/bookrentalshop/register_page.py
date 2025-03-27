from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox
import cx_Oracle
import re

class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 20)
        layout.setSpacing(12)

        self.inputs = {}
        fields = ["이름", "주소", "전화번호", "이메일", "비밀번호","비밀번호 확인"]
        for field in fields:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"{field} 입력")
            if field in ["비밀번호", "비밀번호 확인"]:
                input_field.setEchoMode(QLineEdit.Password)
            input_field.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc;")
            layout.addWidget(input_field)
            self.inputs[field] = input_field

        self.admin_check = QCheckBox("관리자로 가입")
        layout.addWidget(self.admin_check)

        register_button = QPushButton("회원가입")
        register_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #CDE8B4;")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        home_button = QPushButton("홈으로")
        home_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #FFCCCC;")
        home_button.clicked.connect(self.go_home)

        back_button = QPushButton("뒤로가기")
        back_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #FFCCCC;")
        back_button.clicked.connect(self.go_back)

        layout.addWidget(home_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def register(self):
        data = {key: field.text().strip() for key, field in self.inputs.items()}

        # 입력 검증
        if not data["이름"] or not data["비밀번호"]:
            QMessageBox.warning(self, "경고", "이름 또는 비밀번호는 필수입니다!")
            return

        # 이메일 형식 검증
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data["이메일"]):
            QMessageBox.warning(self, "경고", "올바른 이메일 형식을 입력하세요!")
            return

        # 이메일 중복 확인
        if self.is_email_exists(data["이메일"]):
            QMessageBox.warning(self, "경고", "이미 등록된 이메일입니다!")
            return

        # 비밀번호 확인
        if data["비밀번호"] != data["비밀번호 확인"]:
            QMessageBox.warning(self, "경고", "비밀번호가 일치하지 않습니다!")
            return

        try:
            conn = cx_Oracle.connect("bookrentalshop/12345@210.119.14.73:1521/XE")
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
            self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            cursor.close()
            conn.close()

    def is_email_exists(self, email):
        """이메일 중복 확인"""
        try:
            conn = cx_Oracle.connect("bookrentalshop/12345@210.119.14.73:1521/XE")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM CUSTOMERINFO WHERE CST_EMAIL = :1", (email,))
            result = cursor.fetchone()[0]
            return result > 0

        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
            return False

        finally:
            cursor.close()
            conn.close()

    def go_home(self):
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0) # 로그인 페이지로 전환