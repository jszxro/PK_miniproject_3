from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView  # QHeaderView 추가

class SearchPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 테이블 위 간격 추가
        layout.addSpacing(20)

        # 검색 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(9)  # "책 상세보기" 열 추가
        self.result_table.setHorizontalHeaderLabels(["이미지", "장르", "책 이름", "저자", "출판사", "출간일", "가격", "대여상태", "책 상세보기"])
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
        """)
        layout.addWidget(self.result_table)

        # 행 높이 조정
        self.result_table.verticalHeader().setDefaultSectionSize(50)  # 기본 행 높이를 50으로 설정

        # 테이블 아래 간격 추가
        layout.addSpacing(20)

        # 버튼 영역
        button_layout = QHBoxLayout()
        back_button = QPushButton("뒤로가기")
        back_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #FFCCCC;")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_results(self, results): # 검색 결과 표시
        self.result_table.setRowCount(0)  # 기존 데이터 초기화
        if results:
            for row_data in results:
                row_index = self.result_table.rowCount()
                self.result_table.insertRow(row_index)

                # 행 높이 설정
                self.result_table.setRowHeight(row_index, 50)  # 각 행의 높이를 50으로 설정

                # 이미지 셀 추가
                image_path = f"images/{row_data[1]}.jpg"  # 책 이름을 기반으로 이미지 경로 설정
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    icon = QIcon(pixmap)
                    image_item = QTableWidgetItem()
                    image_item.setIcon(icon)
                    self.result_table.setItem(row_index, 0, image_item)
                else:
                    self.result_table.setItem(row_index, 0, QTableWidgetItem("이미지 없음"))

                # 나머지 데이터 추가
                for col_index, data in enumerate(row_data):
                    self.result_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(data)))

                # "책 상세보기" 텍스트 링크 추가
                detail_link = QLabel(f"<a href='#'>상세보기</a>")
                detail_link.setAlignment(Qt.AlignCenter)
                detail_link.setStyleSheet("color: blue; text-decoration: underline;")
                detail_link.linkActivated.connect(lambda _, book=row_data: self.show_book_details(book))
                self.result_table.setCellWidget(row_index, 8, detail_link)
        else:
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem("검색된 책이 없습니다."))
            self.result_table.setSpan(0, 0, 1, self.result_table.columnCount())  # 한 줄로 병합

    def show_book_details(self, book): # 책 상세 정보 표시
        QMessageBox.information(self, "책 상세 정보", f"장르: {book[0]}\n책 이름: {book[1]}\n저자: {book[2]}\n출판사: {book[3]}\n출간일: {book[4]}\n가격: {book[5]} 원\n대출 가능 여부: {book[6]}")

    def go_back(self): # 뒤로가기
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환