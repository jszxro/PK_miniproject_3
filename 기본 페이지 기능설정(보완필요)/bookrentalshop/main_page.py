from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from subprocess import Popen
import sys
import os
from config import DB_CONFIG
import cx_Oracle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "ref", "book_image.jpg")
icon_path = os.path.join(BASE_DIR, "ref", "icon_image.png")  # 아이콘 위치
sys.path.append("C:/Users/jszxr/MyJupyter/PK_miniproject_3/기본 페이지 기능설정(보완필요)/bookrentalshop")
from bookregistermain import BookRegisterPage
from admin_manage import CustomerManager

class MainPage(QWidget):
    def __init__(self, stacked_widget, cst_role=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cst_role = cst_role
        self.initUI()

    def initUI(self):
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setSpacing(10)
        self.render_navbar(initial=True)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("도서 검색")
        self.search_input.setStyleSheet("padding: 6px;")
        search_btn = QPushButton("검색")
        search_btn.setStyleSheet("background-color: #cdeac0; border: none; border-radius: 6px; padding: 6px 12px;")
        search_btn.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setMinimumSize(1, 1)

        overlay_text = QLabel(self.image_label)
        # overlay_text.setText("<div style='font-size:28px; color: white; font-family: Arial; line-height:130%;'>"
        #                      "대출과 반납을 간편하게,<br>Book에서</div>")
        # overlay_text.setStyleSheet("background-color: rgba(0, 0, 0, 80); padding: 16px; border-radius: 12px;")
        overlay_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        overlay_text.setFixedWidth(400)
        overlay_text.move(40, 40)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.nav_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(scroll_area)
        scroll_area.setAlignment(Qt.AlignCenter)

        self.setLayout(main_layout)

    def render_navbar(self, initial=False):
        while self.nav_layout.count():
            widget = self.nav_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        # logo = QLabel("📗 Bukjeokx2")
        # logo.setFont(QFont("Arial", 16, QFont.Bold))
        # self.nav_layout.addWidget(logo)
        # self.nav_layout.addStretch(1)

        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignVCenter)

        text_label = QLabel("Bukjeokx2")
        text_label.setFont(QFont("Arial", 16, QFont.Bold))
        text_label.setAlignment(Qt.AlignVCenter)

        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(6)
        logo_layout.addWidget(icon_label)
        logo_layout.addWidget(text_label)

        logo_widget = QWidget()
        logo_widget.setLayout(logo_layout)

        self.nav_layout.addWidget(logo_widget)
        self.nav_layout.addStretch(1)

        if initial:
            buttons = [("로그인", self.show_login_page)]
        else:
            buttons = [
                ("도서", self.booklist),
                ("로그아웃", self.logout)
            ]
            if self.cst_role == 'admin':
                buttons.insert(1, ("관리자용 도서 관리", self.open_book_register))

            if self.cst_role == 'admin':
                buttons.insert(2, ("관리자용 유저 관리", self.open_user_register))
            if self.cst_role == 'user':
                buttons.insert(1, ("마이페이지", self.open_my_page)) 

        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #cdeac0;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #b5ddb0;
                }
            """)
            btn.clicked.connect(slot)
            self.nav_layout.addWidget(btn)

    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃 되었습니다.")
        self.render_navbar(initial=True)

    def search_books(self):
        book_name = self.search_input.text().strip() # 책 제목으로 검색
        if not book_name:
            QMessageBox.warning(self, "경고", "검색어를 입력하세요!")
            return

        try:
            conn = cx_Oracle.connect("bookrentalshop/12345@210.119.14.73:1521/XE")
            cursor = conn.cursor()

            query = """
                SELECT DIVISION,BOOK_NAME, AUTHOR, PUBLISHER, RELEASE_DT,BOOK_PRICE,LOAN_YN
                FROM BOOKINFO
                WHERE LOWER(BOOK_NAME) LIKE :book_name
            """
            cursor.execute(query, {"book_name": f"%{book_name.lower()}%"})
            results = cursor.fetchall()

            # 검색 결과를 SearchPage로 전달
            book_info_page = self.stacked_widget.widget(3)  # SearchPage 가져오기
            book_info_page.update_results(results)
            self.stacked_widget.setCurrentIndex(3)  # SearchPage로 전환
            
        except cx_Oracle.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃 되었습니다.")
        self.render_navbar(initial=True)

         # 로그인 페이지의 입력 필드 초기화
        login_page = self.stacked_widget.widget(0)  # 로그인 페이지 가져오기
        login_page.clear_inputs()
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def booklist(self):
        self.stacked_widget.setCurrentIndex(4)  # ListPage로 전환

    def open_book_register(self):
        self.book_register_window = BookRegisterPage()
        self.book_register_window.show()

    def open_user_register(self):
        self.user_register_window = CustomerManager()
        self.user_register_window.show()

    def open_my_page(self):
        print("마이페이지 이동")