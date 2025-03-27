from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from subprocess import Popen
import sys
sys.path.append("C:/Users/jszxr/MyJupyter/PK_miniproject_3/기본 페이지 기능설정(보완필요)/bookrentalshop")
from bookregistermain import BookRegisterPage

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
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("ref/book_image.jpg")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        overlay_text = QLabel(self.image_label)
        overlay_text.setText("<div style='font-size:28px; color: white; font-family: Arial; line-height:130%;'>"
                             "대출과 반납을 간편하게,<br>Book에서</div>")
        overlay_text.setStyleSheet("background-color: rgba(0, 0, 0, 80); padding: 16px; border-radius: 12px;")
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

        self.setLayout(main_layout)

    def render_navbar(self, initial=False):
        while self.nav_layout.count():
            widget = self.nav_layout.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        logo = QLabel("📗 Book")
        logo.setFont(QFont("Arial", 16, QFont.Bold))
        self.nav_layout.addWidget(logo)
        self.nav_layout.addStretch(1)

        if initial:
            buttons = [("로그인", self.show_login_page)]
        else:
            buttons = [
                ("도서", lambda: print("도서 페이지")),
                ("마이페이지", lambda: print("마이페이지 이동")),
                ("로그아웃", self.logout)
            ]
            if self.cst_role == 'admin':
                buttons.insert(1, ("관리자용 도서 관리", self.open_book_register))

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

         # 로그인 페이지의 입력 필드 초기화
        login_page = self.stacked_widget.widget(0)  # 로그인 페이지 가져오기
        login_page.clear_inputs()

        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def open_book_register(self):
        self.book_register_window = BookRegisterPage()
        self.book_register_window.show()