from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView  # QHeaderView 추가
from book_qt_3 import bookQT  # 수정: 올바른 클래스 이름으로 임포트
from config import DB_CONFIG  # DB_CONFIG 임포트
import cx_Oracle as oci # 추가: DB 연결을 위해 cx_Oracle 임포트
import requests  # URL에서 이미지를 다운로드하기 위해 추가
from io import BytesIO  # 이미지 데이터를 메모리에서 처리하기 위해 추가

class SearchPage(QWidget):
    def __init__(self, stacked_widget, user_email=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.logged_in_user = None  # 로그인한 유저 이름 저장
        self.user_email = user_email
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)  # 레이아웃 간격을 20으로 설정

        # 테이블 위 간격 추가
        layout.addSpacing(20)

        # 검색 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)  # "대여가능여부" 컬럼 삭제
        self.result_table.setHorizontalHeaderLabels(["이미지", "장르", "책 이름", "저자", "출판사", "출간일", "가격", "책 상세보기"])
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
        """)
        layout.addWidget(self.result_table)

        # 행 높이 조정
        self.result_table.verticalHeader().setDefaultSectionSize(70)  # 기본 행 높이를 70으로 설정

        # 테이블 아래 간격 추가
        layout.addSpacing(20)

        # 버튼 영역
        button_layout = QHBoxLayout()
        back_button = QPushButton("뒤로가기")
        back_button.setStyleSheet("padding: 10px; border-radius: 10px; background-color: #FFCCCC;")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)  # 레이아웃 설정

    def set_logged_in_user(self, user_name):
        """로그인한 유저 이름 설정"""
        self.logged_in_user = user_name

    def update_results(self, results):  # 검색 결과 표시
        self.result_table.setRowCount(0)  # 기존 데이터 초기화
        self.result_table.verticalHeader().setDefaultSectionSize(120)  # 셀 높이를 120으로 설정
        if results:
            for row_data in results:
                row_index = self.result_table.rowCount()
                self.result_table.insertRow(row_index)

                # 행 높이 설정
                self.result_table.setRowHeight(row_index, 120)  # 각 행의 높이를 120으로 설정

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

                # 나머지 데이터 추가
                for col_index, data in enumerate(row_data[1:-1]):  # "대여가능여부" 제외
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)  # 셀 내용 가운데 정렬
                    self.result_table.setItem(row_index, col_index + 1, item)  # 1부터 시작

                # "책 상세보기" 버튼 추가
                detail_button = QPushButton("책 정보")
                detail_button.setStyleSheet("""
                    QPushButton {
                        padding: 10px;
                        background-color: #CDE8B4;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #b5ddb0;
                    }
                """)

                detail_button.setFixedSize(100, 40)  # 버튼 크기 조정
                # 책 이름(row_data[2])을 정확히 전달
                detail_button.clicked.connect(lambda _, book=row_data[2]: self.open_book_qt(book))
                    # 버튼을 가운데 정렬
                button_layout = QHBoxLayout()
                button_layout.setAlignment(Qt.AlignCenter)
                button_layout.addWidget(detail_button)
                button_widget = QWidget()
                button_widget.setLayout(button_layout)

                self.result_table.setCellWidget(row_index, 7, button_widget)  # "책 상세보기" 버튼 추가
        else:
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem("검색된 책이 없습니다."))
            self.result_table.setSpan(0, 0, 1, self.result_table.columnCount())  # 한 줄로 병합

    def open_book_qt(self, book_name):
        """책 정보 버튼 클릭 시 DB에서 책 정보를 조회하고 bookQT 창에 전달"""
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
                self.user_register_window = bookQT(book_data, user_email=self.user_email)  # 책 정보를 전달
                self.user_register_window.show()
            else:
                QMessageBox.warning(self, "경고", f"책 정보를 찾을 수 없습니다: {book_name}")

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"데이터베이스 연결에 실패했습니다.\n{str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def go_back(self):  # 뒤로가기
        self.stacked_widget.setCurrentIndex(1)  # 메인 페이지로 전환

