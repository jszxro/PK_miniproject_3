from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from subprocess import Popen
import sys
import os
import cx_Oracle as oci  # cx_Oracle 추가
from config import DB_CONFIG
import cx_Oracle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "ref", "book_image.jpg")
icon_path = os.path.join(BASE_DIR, "ref", "icon_image.png")  # 아이콘 위치
sys.path.append("C:/Users/jszxr/MyJupyter/PK_miniproject_3/기본 페이지 기능설정(보완필요)/bookrentalshop")
from bookregistermain import BookRegisterPage
from admin_manage import CustomerManager
from config import DB_CONFIG  # DB_CONFIG 임포트

class MainPage(QWidget):
    def __init__(self, stacked_widget, cst_role=None): 
        super().__init__()
        self.stacked_widget = stacked_widget 
        self.cst_role = cst_role # 사용자 역할 (admin, user 등)
        self.user_email = None

        from search_page import SearchPage
        self.search_page = SearchPage(self.stacked_widget, user_email=self.user_email)

        self.initUI()

    def initUI(self):
        self.nav_layout = QHBoxLayout() # 네비게이션 바 레이아웃
        self.nav_layout.setSpacing(10) # 위젯 간격 설정
        self.render_navbar(initial=True) # 초기 네비게이션 바 렌더링

        search_layout = QHBoxLayout() # 검색 레이아웃
        self.search_input = QLineEdit() # 검색 입력 필드
        self.search_input.setPlaceholderText("도서 검색") 
        self.search_input.setStyleSheet("padding: 6px;") 
        search_btn = QPushButton("검색") # 검색 버튼
        search_btn.setStyleSheet("background-color: #cdeac0; border: none; border-radius: 6px; padding: 6px 12px;") 
        search_btn.clicked.connect(self.search_books) # 검색 버튼 클릭 시 search_books 메서드 호출
        search_layout.addWidget(self.search_input) # 검색 입력 필드 추가
        search_layout.addWidget(search_btn) # 검색 버튼 추가

        self.image_label = QLabel() # 이미지 레이블
        self.image_label.setAlignment(Qt.AlignCenter) # 중앙 정렬
        pixmap = QPixmap(image_path) # 이미지 로드
        self.image_label.setPixmap(pixmap) # 이미지 설정
        self.image_label.setScaledContents(True) # 이미지 크기 조정
        self.image_label.setMinimumSize(1, 1) # 최소 크기 설정

        overlay_text = QLabel(self.image_label) 
        # overlay_text.setText("<div style='font-size:28px; color: white; font-family: Arial; line-height:130%;'>"
        #                      "대출과 반납을 간편하게,<br>Book에서</div>")
        # overlay_text.setStyleSheet("background-color: rgba(0, 0, 0, 80); padding: 16px; border-radius: 12px;")
        overlay_text.setAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 상단 정렬
        overlay_text.setFixedWidth(400) # 고정 너비 설정
        overlay_text.move(40, 40) # 위치 설정

        scroll_area = QScrollArea() # 스크롤 영역 생성
        scroll_area.setWidgetResizable(True) # 위젯 크기 조정 가능
        scroll_area.setWidget(self.image_label) # 이미지 레이블을 스크롤 영역에 추가

        main_layout = QVBoxLayout() # 메인 레이아웃 생성
        main_layout.addLayout(self.nav_layout) # 네비게이션 바 레이아웃 추가
        main_layout.addLayout(search_layout) # 검색 레이아웃 추가
        main_layout.addWidget(scroll_area) # 스크롤 영역 추가
        scroll_area.setAlignment(Qt.AlignCenter) # 중앙 정렬

        self.setLayout(main_layout) # 레이아웃 설정

    def render_navbar(self, initial=False): 
        while self.nav_layout.count(): 
            widget = self.nav_layout.takeAt(0).widget() # 네비게이션 바 초기화
            if widget:
                widget.setParent(None) # 부모 위젯 제거

        # logo = QLabel("📗 Bukjeokx2")
        # logo.setFont(QFont("Arial", 16, QFont.Bold))
        # self.nav_layout.addWidget(logo)
        # self.nav_layout.addStretch(1)

        icon_label = QLabel() # 아이콘 레이블
        icon_pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation) # 아이콘 이미지 로드 및 크기 조정
        icon_label.setPixmap(icon_pixmap) # 아이콘 설정
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignVCenter)

        text_label = QLabel("Bukjeokx2") # 텍스트 레이블
        text_label.setFont(QFont("Arial", 16, QFont.Bold)) 
        text_label.setAlignment(Qt.AlignVCenter)

        logo_layout = QHBoxLayout() # 로고 레이아웃 생성
        logo_layout.setSpacing(6) # 위젯 간격 설정
        logo_layout.addWidget(icon_label)
        logo_layout.addWidget(text_label)

        logo_widget = QWidget() # 로고 위젯 생성
        logo_widget.setLayout(logo_layout) # 로고 레이아웃 설정

        self.nav_layout.addWidget(logo_widget) # 로고 위젯 추가
        self.nav_layout.addStretch(1) # 네비게이션 바 오른쪽 정렬

        if initial: # 초기 상태일 때
            buttons = [("로그인", self.show_login_page)] # 로그인 버튼
        else: # 로그인 후 상태일 때
            buttons = [
                ("도서", self.booklist), 
                ("로그아웃", self.logout)
            ]
            if self.cst_role == 'admin':
                buttons.insert(1, ("관리자용 도서 관리", self.open_book_register)) # 관리자용 도서 관리 버튼

            if self.cst_role == 'admin':
                buttons.insert(2, ("관리자용 유저 관리", self.open_user_register)) # 관리자용 유저 관리 버튼
            if self.cst_role == 'user':
                buttons.insert(1, ("마이페이지", self.open_my_page)) # 사용자용 마이페이지 버튼

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
            btn.clicked.connect(slot) # 버튼 클릭 시 슬롯 연결
            self.nav_layout.addWidget(btn) # 버튼 추가

    def show_login_page(self): 
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃 되었습니다.") # 로그아웃 메시지 박스
        self.render_navbar(initial=True) # 네비게이션 바 초기화

    def search_books(self): 
        book_name = self.search_input.text().strip() # 책 제목으로 검색
        if not book_name:
            QMessageBox.warning(self, "경고", "검색어를 입력하세요!")
            return

        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()

            query = """
                SELECT BOOK_IMG,DIVISION,BOOK_NAME, AUTHOR, PUBLISHER, RELEASE_DT,BOOK_PRICE,LOAN_YN
                FROM BOOKINFO
                WHERE LOWER(BOOK_NAME) LIKE :book_name
            """
            cursor.execute(query, {"book_name": f"%{book_name.lower()}%"}) # 대소문자 구분 없이 검색
            results = cursor.fetchall() # 검색 결과 가져오기

            # 검색 결과를 SearchPage로 전달
            book_info_page = self.stacked_widget.widget(3)  # SearchPage 가져오기
            book_info_page.update_results(results) # 검색 결과 업데이트
            self.stacked_widget.setCurrentIndex(3)  # SearchPage로 전환
            
        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}") # DB 오류 메시지 박스
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def logout(self):
        QMessageBox.information(self, "로그아웃", "로그아웃 되었습니다.") # 로그아웃 메시지 박스
        self.render_navbar(initial=True) # 네비게이션 바 초기화

         # 로그인 페이지의 입력 필드 초기화
        login_page = self.stacked_widget.widget(0)  # 로그인 페이지 가져오기
        login_page.clear_inputs()
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지로 전환

    def booklist(self):
        self.stacked_widget.setCurrentIndex(4)  # ListPage로 전환

    def open_book_register(self):
        self.book_register_window = BookRegisterPage() # 도서 등록 페이지
        self.book_register_window.show()

    def open_user_register(self):
        self.user_register_window = CustomerManager() # 유저 관리 페이지
        self.user_register_window.show()

    # def open_my_page(self):
    #     # 로그인한 사용자의 이메일이 필요해요!
    #     login_page = self.stacked_widget.widget(0)
    #     user_email = login_page.email_input.text().strip()

    #     # 이미 추가된 마이페이지 위젯을 찾거나 새로 생성
    #     from mypage import MyPage  # MyPage import

    #     self.mypage = MyPage(user_email)
    #     self.stacked_widget.addWidget(self.mypage)
    #     self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.mypage))

    def open_my_page(self):
        if hasattr(self, 'mypage_index'):
            self.stacked_widget.setCurrentIndex(self.mypage_index)
        else:
            QMessageBox.warning(self, "오류", "마이페이지를 불러올 수 없습니다.")
