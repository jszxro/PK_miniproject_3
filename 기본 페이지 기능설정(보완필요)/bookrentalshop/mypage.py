from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QColor, QBrush
from PyQt5.QtCore import Qt
import cx_Oracle as oci
from config import DB_CONFIG

class MyPage(QWidget):
    def __init__(self, user_email):
        super().__init__()
        self.user_email = user_email
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 상단 타이틀
        title = QLabel("📚 나의 대출 내역")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(title)

        self.info_label = QLabel()  # 대출 수나 유저 이름 나오는 곳
        self.layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["도서명", "저자", "대출일", "반납예정일", "상태", "반납"])
        self.layout.addWidget(self.table)

        self.load_data()

         # 뒤로가기 버튼
        back_btn = QPushButton("← 뒤로가기")
        back_btn.setFixedWidth(100)
        back_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                border-radius: 8px;
                background-color: #FFCCCC;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f2a6a6;
            }
        """)
        back_btn.clicked.connect(self.go_back)

        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(back_btn)
        self.layout.addLayout(back_layout)

    def load_data(self):
        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # 유저 이름 가져오기
            cursor.execute("SELECT CST_ID, CST_NAMES FROM CUSTOMERINFO WHERE CST_EMAIL = :email", {'email': self.user_email})
            user_info = cursor.fetchone()
            if not user_info:
                return

            cst_id, cst_name = user_info

            # 대출 정보 조회
            query = """
                SELECT B.BOOK_NAME, B.AUTHOR, TO_CHAR(BI.BORROW_DATE, 'YYYY-MM-DD'), 
                       TO_CHAR(BI.DUE_DATE, 'YYYY-MM-DD'), BI.STATUS, BI.BORROW_ID
                FROM BORROWINFO BI
                JOIN BOOKINFO B ON BI.BOOK_ID = B.BOOK_ID
                WHERE BI.CST_ID = :cst_id
                ORDER BY BI.BORROW_DATE DESC
            """
            cursor.execute(query, {'cst_id': cst_id})
            results = cursor.fetchall()

            self.info_label.setText(f"{cst_name}님의 대출 내역 📖 총 {len(results)}권")

            self.table.setRowCount(len(results))
            for row_idx, row in enumerate(results):
                for col_idx, val in enumerate(row[:5]):  # 상태 전까지
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignCenter)
                    if col_idx == 4 and val == "대출 중":
                        item.setForeground(QBrush(QColor("green")))
                    elif col_idx == 4:
                        item.setForeground(QBrush(QColor("gray")))
                    self.table.setItem(row_idx, col_idx, item)

                # 반납 버튼
                status = row[4]
                borrow_id = row[5]
                btn = QPushButton("반납")
                btn.setEnabled(status == "대출 중")
                btn.clicked.connect(lambda _, bid=borrow_id: self.return_book(bid))
                self.table.setCellWidget(row_idx, 5, btn)

        except Exception as e:
            QMessageBox.critical(self, "DB 오류", str(e))
        finally:
            cursor.close()
            conn.close()

    def return_book(self, borrow_id):
        try:
            conn = oci.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE BORROWINFO
                SET RETURN_DATE = SYSDATE, STATUS = '반납 완료'
                WHERE BORROW_ID = :borrow_id
            """, {'borrow_id': borrow_id})
            conn.commit()
            QMessageBox.information(self, "반납 완료", "도서가 정상적으로 반납되었습니다.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))
        finally:
            cursor.close()
            conn.close()

    def go_back(self):
        self.parent().setCurrentIndex(1)  # 메인 페이지 인덱스 (보통 1번)
