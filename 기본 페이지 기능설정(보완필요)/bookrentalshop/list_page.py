from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QLabel  # QHeaderView, QLabel 추가
from book_qt_3 import bookQT  # 수정: 올바른 클래스 이름으로 임포트
from config import DB_CONFIG  # DB_CONFIG 임포트
import cx_Oracle as oci # cx_Oracle 추가
import requests  # URL에서 이미지를 다운로드하기 위해 추가
from io import BytesIO  # 이미지 데이터를 메모리에서 처리하기 위해 추가

class ListPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget # 스택 위젯
        self.logged_in_user = None  # 로그인한 유저 이름 저장
        self.current_page = 1  # 현재 페이지
        self.items_per_page = 15  # 페이지당 항목 수
        self.total_items = 0  # 총 항목 수
        self.book_data = []  # 책 데이터 리스트
        self.initUI() # UI 초기화
        self.loadBooksFromDB()  # DB에서 책 데이터 로드

    def set_logged_in_user(self, user_name):
        """로그인한 유저 이름 설정"""
        self.logged_in_user = user_name

    def initUI(self):
        layout = QVBoxLayout()  # 수직 박스 레이아웃
        layout.setSpacing(15) # 위젯 간격 설정

        # 테이블 위 간격 추가
        layout.addSpacing(20)

        # 도서 리스트 테이블
        self.result_table = QTableWidget() # 테이블 생성
        self.result_table.setColumnCount(8)  # "책 상세보기" 열 추가
        self.result_table.setHorizontalHeaderLabels(["이미지", "장르", "책 이름", "저자", "출판사", "출간일", "가격", "대여상태"]) # 테이블 헤더 설정
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 모든 열 균일 크기 설정
        self.result_table.setStyleSheet("border: 1px solid #ccc;") 
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 셀 수정 비활성화
        self.result_table.setStyleSheet("""
            QTableWidget::item {
                padding: 5px;  /* 셀 내부 간격 조정 */
            }
            QTableWidget::item:selected {
                background-color: #D3E4CD;  /* 선택된 셀의 배경색 */
            }
        """) # 테이블 스타일 설정
        layout.addWidget(self.result_table)

        # 행 높이 조정
        self.result_table.verticalHeader().setDefaultSectionSize(50)  # 기본 행 높이를 50으로 설정

        # 테이블 아래 간격 추가
        layout.addSpacing(20)

        # 페이지네이션 버튼 영역
        pagination_layout = QHBoxLayout()

        self.first_button = QPushButton("처음")
        self.first_button.setEnabled(False)
        self.first_button.clicked.connect(self.firstPage)
        pagination_layout.addWidget(self.first_button)

        self.prev_button = QPushButton("이전")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.prevPage)
        pagination_layout.addWidget(self.prev_button)

        self.page_label = QLabel(f"페이지 {self.current_page}")
        self.page_label.setAlignment(Qt.AlignCenter)
        pagination_layout.addWidget(self.page_label)

        self.next_button = QPushButton("다음")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.nextPage)
        pagination_layout.addWidget(self.next_button)

        self.last_button = QPushButton("마지막")
        self.last_button.setEnabled(False)
        self.last_button.clicked.connect(self.lastPage)
        pagination_layout.addWidget(self.last_button)

        layout.addLayout(pagination_layout)

        # 버튼 영역
        button_layout = QHBoxLayout()
        back_button = QPushButton("뒤로가기")
        back_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #FFCCCC;")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


    # DB에서 책 데이터 로드
    def loadBooksFromDB(self):  
        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = '''
                SELECT BOOK_IMG, DIVISION, BOOK_NAME, AUTHOR, PUBLISHER, TO_CHAR(RELEASE_DT, 'YYYY-MM-DD'), BOOK_PRICE
                FROM BOOKINFO
                ORDER BY BOOK_ID
            '''
            cursor.execute(query)
            self.book_data = cursor.fetchall()  # DB에서 가져온 데이터를 리스트로 저장
            self.total_items = len(self.book_data)  # 총 항목 수 저장
            self.current_page = 1  # 현재 페이지 초기화
            self.updateTable()  # 테이블 업데이트
            self.updatePaginationButtons()  # 페이지네이션 버튼 업데이트
        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"도서 데이터를 불러오는 중 오류가 발생했습니다.\n{str(e)}")
        finally:
            cursor.close()
            conn.close()


    # 테이블 업데이트
    def updateTable(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_data = self.book_data[start_index:end_index]

        self.result_table.setRowCount(len(page_data))
        self.result_table.verticalHeader().setDefaultSectionSize(120)  # 셀 높이를 120으로 설정
        for row_index, row_data in enumerate(page_data):

            # 이미지 URL을 가져와서 QPixmap으로 변환
            # 이미지 셀 추가
            image_url = row_data[0]  # book_img 컬럼의 URL 사용
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 이미지 크기 조정
                    image_label = QLabel()  # QLabel 사용
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignCenter)  # 가운데 정렬
                    self.result_table.setCellWidget(row_index, 0, image_label)
                else:
                    no_image_label = QLabel("이미지 없음")
                    no_image_label.setAlignment(Qt.AlignCenter)  # 가운데 정렬
                    self.result_table.setCellWidget(row_index, 0, no_image_label)
            except Exception:
                no_image_label = QLabel("이미지 없음")
                no_image_label.setAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.result_table.setCellWidget(row_index, 0, no_image_label)


            # 나머지 데이터 셀 추가
            for col_index, value in enumerate(row_data[1:], start=1):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)  # 셀 내용 가운데 정렬
                self.result_table.setItem(row_index, col_index, item)


            # "책 상세보기" 버튼 추가
            detail_button = QPushButton("책 정보")
            detail_button.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    background-color: #CDE8B4;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #b5ddb0;
                }
            """)
        
            detail_button.setFixedSize(100, 40)  # 버튼 크기 조정
            detail_button.clicked.connect(lambda _, book=row_data: self.open_book_qt(book[2]))  # 책 이름 전달
            
             # 버튼을 가운데 정렬
            button_layout = QHBoxLayout()
            button_layout.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(detail_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.result_table.setCellWidget(row_index, 7, button_widget)  # "책 상세보기" 버튼 추가


    # 페이지네이션 버튼 업데이트
    def updatePaginationButtons(self):
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"페이지 {self.current_page} / {total_pages}")
        self.first_button.setEnabled(self.current_page > 1)
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)
        self.last_button.setEnabled(self.current_page < total_pages)

        
    # 처음 페이지로 이동
    def firstPage(self):
        if self.current_page > 1:
            self.current_page = 1
            self.updateTable()
            self.updatePaginationButtons()

    # 마지막 페이지로 이동
    def lastPage(self):  
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page = total_pages
            self.updateTable()
            self.updatePaginationButtons()

    # 이전 페이지로 이동
    def prevPage(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.updateTable()
            self.updatePaginationButtons()

    # 다음 페이지로 이동
    def nextPage(self):
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.updateTable()
            self.updatePaginationButtons()


    # 책 상세보기 버튼 클릭 시 DB에서 책 정보를 조회하고 bookQT 창에 전달
    def open_book_qt(self, book_name): 
        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()

            query = """
                SELECT BOOK_NAME, AUTHOR, PUBLISHER
                FROM BOOKINFO
                WHERE BOOK_NAME = :book_name
            """
            cursor.execute(query, {"book_name": book_name})
            book_data = cursor.fetchone()

            if book_data:
                self.user_register_window = bookQT(book_data)
                if self.logged_in_user:  # 로그인한 유저 이름이 있으면 전달
                    self.user_register_window.input_std_username.setText(self.logged_in_user)
                self.user_register_window.show()
            else:
                QMessageBox.warning(self, "경고", "책 정보를 찾을 수 없습니다.")

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


    # 뒤로가기 버튼 클릭 시 메인 페이지로 이동
    def go_back(self): 
        if self.current_page > 1:
            self.current_page = 1
            self.updateTable()
            self.updatePaginationButtons()
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환

