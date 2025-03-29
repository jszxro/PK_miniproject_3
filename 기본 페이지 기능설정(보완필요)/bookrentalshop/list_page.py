from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView  # QHeaderView 추가
import cx_Oracle as oci # cx_Oracle 추가

class ListPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget # 스택 위젯
        self.current_page = 1  # 현재 페이지
        self.items_per_page = 15  # 페이지당 항목 수
        self.total_items = 0  # 총 항목 수
        self.book_data = []  # 책 데이터 리스트
        self.initUI() # UI 초기화
        self.loadBooksFromDB()  # DB에서 책 데이터 로드

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
                padding: 15px;  /* 셀 내부 간격 조정 */
            }
            QTableWidget::item:selected {
                background-color: #D3E4CD;  /* 선택된 셀의 배경색 */
            }
        """) # 테이블 스타일 설정
        self.result_table.cellClicked.connect(lambda row, col: self.show_book_details(self.book_data[row]))  # 셀 클릭 시 책 상세 정보 표시
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

    def loadBooksFromDB(self):  # DB에서 책 데이터 로드
        try:
            conn = oci.connect('bookrentalshop/12345@210.119.14.73:1521/XE')
            cursor = conn.cursor()
            query = '''
                SELECT BOOK_ID, DIVISION, BOOK_NAME, AUTHOR, PUBLISHER, TO_CHAR(RELEASE_DT, 'YYYY-MM-DD'), BOOK_PRICE
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

    def updateTable(self):  # 테이블 업데이트
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_data = self.book_data[start_index:end_index]

        self.result_table.setRowCount(len(page_data))
        for row_index, row_data in enumerate(page_data):
            # 이미지 셀 추가
            image_path = f"images/{row_data[2]}.jpg"  # 책 이름을 기반으로 이미지 경로 설정
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                icon = QIcon(pixmap)
                image_item = QTableWidgetItem()
                image_item.setIcon(icon)
                self.result_table.setItem(row_index, 0, image_item)
            else:
                self.result_table.setItem(row_index, 0, QTableWidgetItem("이미지 없음"))

            # 나머지 데이터 셀 추가
            for col_index, value in enumerate(row_data[1:], start=1):
                self.result_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def updatePaginationButtons(self):  # 페이지네이션 버튼 업데이트
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        self.page_label.setText(f"페이지 {self.current_page} / {total_pages}")
        self.first_button.setEnabled(self.current_page > 1)
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)
        self.last_button.setEnabled(self.current_page < total_pages)

    def firstPage(self):  # 처음 페이지로 이동
        if self.current_page > 1:
            self.current_page = 1
            self.updateTable()
            self.updatePaginationButtons()

    def lastPage(self):  # 마지막 페이지로 이동
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page = total_pages
            self.updateTable()
            self.updatePaginationButtons()

    def prevPage(self): # 이전 페이지로 이동
        if self.current_page > 1:
            self.current_page -= 1
            self.updateTable()
            self.updatePaginationButtons()

    def nextPage(self): # 다음 페이지로 이동
        total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.updateTable()
            self.updatePaginationButtons()

    def show_book_details(self, book):  # 책 상세 정보 표시
        QMessageBox.information(self, "책 상세 정보", f"책 이름: {book[2]}\n저자: {book[3]}\n출판사: {book[4]}\n출간일: {book[5]}\n가격: {book[6]} 원")

    def go_back(self):  # 뒤로가기
        if self.current_page > 1:
            self.current_page = 1
            self.updateTable()
            self.updatePaginationButtons()
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환

