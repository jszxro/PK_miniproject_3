# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5 import uic
# from config import DB_CONFIG  # DB_CONFIG 임포트
# import cx_Oracle as oci
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # from PyQt5.QtCore import QSize

# # DB 연결 정보
# # DB_INFO = {
# #     "sid": "XE",
# #     "host": "210.119.14.73",
# #     "port": 1521,
# #     "username": "bookrentalshop",
# #     "password": "12345"
# # }


# class bookQT(QMainWindow):
#     def __init__(self, book=None, user_email=None):  # 수정: book 인수를 받을 수 있도록 변경
#         super(QMainWindow, self).__init__()
#         self.initUI()
#         self.loadData()
#         self.user_email = user_email
#         if book:
#             self.populate_fields(book)  # 전달받은 책 데이터를 필드에 채우기

#     # 전달받은 책 데이터를 필드에 채우는 메서드
#     def populate_fields(self, book):
#         self.input_std_name.setText(book[0])  # 책 제목
#         self.input_std_author.setText(book[1])  # 저자
#         self.input_std_pub.setText(book[2])  # 출판사

#     def initUI(self):
#         basedir = os.path.dirname(os.path.abspath(__file__))
#         ui_path = os.path.join(basedir, 'book_qt_3.ui')
#         uic.loadUi(ui_path, self)
#         self.setWindowTitle('도서대출 예약 반납 서비스')
#         self.statusbar.showMessage('도서대출 예약 반납 service')

#         # 🔹 초기 상태에서 대출/반납 버튼 비활성화
#         self.btn_bor.setEnabled(False)
#         self.btn_ret.setEnabled(False)


        
#         # 테이블 위젯 설정
#         self.tblbook.setSelectionMode(QAbstractItemView.SingleSelection)
#         self.tblbook.setColumnCount(5)
#         self.tblbook.setHorizontalHeaderLabels(['제목', '저자', '출판사', '대출 여부', '대출자'])

#         # 🔹 더블 클릭 시 편집 방지
#         self.tblbook.setEditTriggers(QAbstractItemView.NoEditTriggers)

#         # # ✅ 고객 정보 테이블 추가
#         # self.tblCustomer.setSelectionMode(QAbstractItemView.SingleSelection)
#         # self.tblCustomer.setColumnCount(1)
#         # self.tblCustomer.setHorizontalHeaderLabels(['고객 이름'])
#         # self.tblCustomer.setEditTriggers(QAbstractItemView.NoEditTriggers)

#         # 버튼에 아이콘 추가
#         # self.btn_sea.setIcon(QIcon('./image/book_sea.png'))
#         # self.btn_sea.setIconSize(QSize(50, 50))
#         # self.btn_bor.setIcon(QIcon('./image/book_bor.png'))
#         # self.btn_ret.setIcon(QIcon('./image/book_ret.png'))
#         # self.btn_clr.setIcon(QIcon('./image/reset.png'))
        
#         # 버튼 이벤트 연결
#         self.btn_sea.clicked.connect(self.btnSeaClick)
#         self.btn_bor.clicked.connect(self.btnBorClick)
#         self.btn_ret.clicked.connect(self.btnRetClick)
#         self.btn_clr.clicked.connect(self.btnClearClick)
        
#         self.tblbook.doubleClicked.connect(self.tblbookDoubleClick)
#         self.show()

    
#     def connectDB(self):
#         return oci.connect(**DB_CONFIG)
    
#     def loadData(self):
#         conn = self.connectDB()
#         cursor = conn.cursor()
#         query = '''SELECT BOOK_NAME, AUTHOR, PUBLISHER, LOAN_YN, LOAN_USER FROM BOOKINFO''' 
#         cursor.execute(query)
        
#         books = cursor.fetchall()
#         self.tblbook.setRowCount(len(books))
        
#         for i, row in enumerate(books):
#             for j, col in enumerate(row):
#                 if j == 3:  # 🔹 대출 여부 변환
#                     loan_status = "가능" if col != "불가능" else "가능"
#                     self.tblbook.setItem(i, j, QTableWidgetItem(loan_status))
#                 else:
#                     self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))
#                 #self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))
        
#         cursor.close()
#         conn.close()

#     def loadCustomerData(self):
#         conn = self.connectDB()
#         cursor = conn.cursor()
#         query = "SELECT CST_NAMES FROM CUSTOMERINFO"
#         cursor.execute(query)
    
#         customers = cursor.fetchall()
#         self.tblCustomer.setRowCount(len(customers))  # 행 개수 설정
    
#         for i, row in enumerate(customers):
#             for j, col in enumerate(row):
#                 self.tblCustomer.setItem(i, j, QTableWidgetItem(str(col)))
    
#         cursor.close()
#         conn.close()

#         # ✅ 데이터 로드
#         self.loadData()  # 도서 데이터
#         self.loadCustomerData()  # 고객 데이터

#         self.show()

    
#     def getInputValues(self):
#         return (
#             self.input_std_name.text(),
#             self.input_std_author.text(),
#             self.input_std_pub.text()
#             # self.input_std_div.text()
#         )
    
#     def tblbookDoubleClick(self):
#         selected = self.tblbook.currentRow()
#         if selected < 0:
#             return
        
#         input_fields = [
#             self.input_std_name,  # 제목
#             self.input_std_author,  # 저자
#             self.input_std_pub,  # 출판사
#             None,  # 대출 여부 (입력 필드 없음)
#             None   # 대출자 (입력 필드 없음)
#         ]

#         for i in range(len(input_fields)):
#             if input_fields[i] is not None:  # 입력 필드가 있는 경우만 설정
#                 item = self.tblbook.item(selected, i)
#                 if item:
#                     input_fields[i].setText(item.text())

#         self.statusbar.showMessage(f'도서 선택됨: {self.tblbook.item(selected, 0).text()}')


#         # for i in range(6):
#         #     getattr(self, f"input_std_{['name', 'author'][i]}").setText(self.tblbook.item(selected, i).text())
        
#         # self.statusbar.showMessage('도서정보 선택됨')

#     def btnClearClick(self):
#         # 확인 메시지 표시
#         reply = QMessageBox.question(self, '초기화 확인', '정말로 초기화 하시겠습니까?', 
#                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

#         if reply == QMessageBox.No:
#             return  # 사용자가 "아니오"를 선택하면 초기화 취소
#     # 입력 필드 초기화
#         self.input_std_name.clear()
#         self.input_std_name.clear()
#         self.input_std_author.clear()
#         self.input_std_pub.clear()
#         # self.input_std_div.clear()

#         # 🔹 대출/반납 버튼 비활성화
#         self.btn_bor.setEnabled(False)
#         self.btn_ret.setEnabled(False)
    
#     # 전체 도서 데이터 다시 불러오기
#         self.loadData()

#         self.statusbar.showMessage('입력 필드 초기화 및 전체 데이터 로드 완료')

    
#     def btnSeaClick(self):
#         values = self.getInputValues()
#         search_book_name, search_author, search_publisher = values[0], values[1], values[2]

#         if not search_book_name and not search_author:
#             QMessageBox.warning(self, '경고', '조회할 제목, 저자 중 하나를 입력하세요!')
#             return

#         conn = self.connectDB()
#         cursor = conn.cursor()

#     # 조건문 동적으로 설정
#         query = "SELECT BOOK_NAME, AUTHOR, PUBLISHER, LOAN_YN, LOAN_USER FROM BOOKINFO WHERE 1=1"
#         params = []

#         if search_book_name:
#             query += " AND BOOK_NAME LIKE '%' || :1 || '%'".format(len(params) + 1)
#             params.append(search_book_name)

#         if search_author:
#             query += " AND AUTHOR LIKE '%' || :2 || '%'".format(len(params) + 1)
#             params.append(search_author)

#         if search_publisher:
#             query += " AND PUBLISHER LIKE '%' || :3 || '%'".format(len(params) + 1)
#             params.append(search_publisher)

#         cursor.execute(query, tuple(params))
#         books = cursor.fetchall()

#         if not books:
#             QMessageBox.warning(self, '조회 실패', '해당 도서를 찾을 수 없습니다!')

#             # 전체 데이터 다시 조회
#             cursor.execute("SELECT BOOK_NAME, AUTHOR, PUBLISHER, LOAN_YN, LOAN_USER FROM BOOKINFO")
#             books = cursor.fetchall()

#         if not books:
#             QMessageBox.warning(self, '조회 실패', '해당 도서를 찾을 수 없습니다!')
#             self.btn_bor.setEnabled(False)  # 조회 실패 시 버튼 비활성화
#             self.btn_ret.setEnabled(False)
#         else:
#         # 🔹 조회 성공하면 대출/반납 버튼 활성화
#             self.btn_bor.setEnabled(True)
#             self.btn_ret.setEnabled(True)

#         # 테이블 초기화 후 데이터 출력
#         self.tblbook.clearContents()
#         self.tblbook.setRowCount(len(books))


#         for i, row in enumerate(books):
#             for j, col in enumerate(row):
#                 self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))

#         cursor.close()
#         conn.close()

#     def btnBorClick(self):
#         values = self.getInputValues()
#         search_book_name, search_author, search_publisher = values[0], values[1], values[2]
#         loan_user = self.input_std_username.text().strip()

#         if not search_book_name:
#             QMessageBox.warning(self, '경고', '도서 제목을 입력하세요!')
#             return
#         if not loan_user:
#             QMessageBox.warning(self, '경고', '대출자를 입력하세요!')
#             return

#         conn = self.connectDB()
#         cursor = conn.cursor()

#         try:
#         # 🔹 고객 존재 여부 확인
#             cursor.execute("SELECT CST_NAMES FROM CUSTOMERINFO WHERE CST_NAMES = :1", (loan_user,))
#             customer = cursor.fetchone()

#             if not customer:
#                 QMessageBox.warning(self, '대출 불가', '해당 이름의 고객이 존재하지 않습니다!')
#                 return

#         # 🔹 도서의 대출 가능 여부 확인
#             cursor.execute("SELECT LOAN_YN FROM BOOKINFO WHERE BOOK_NAME = :1", (search_book_name,))
#             book = cursor.fetchone()

#             if not book:
#                 QMessageBox.warning(self, '대출 실패', '해당 도서가 존재하지 않습니다.')
#                 return
#             elif book[0] == '불가능':  # 이미 대출된 상태
#                 QMessageBox.warning(self, '대출 실패', '이미 대출 중인 도서입니다.')
#                 return

#         # 🔹 대출 처리 (BOOKINFO 테이블 업데이트)
#             query_update_book = """
#                 UPDATE BOOKINFO
#                 SET LOAN_YN = '불가능', LOAN_USER = :1
#                 WHERE BOOK_NAME = :2
#             """
#             cursor.execute(query_update_book, (loan_user, search_book_name))

#             # ✅ BORROWINFO 테이블에 INSERT 추가!
#             query_insert_borrow = """
#                 INSERT INTO BORROWINFO (BOOK_ID, CST_ID, BORROW_DATE, DUE_DATE, STATUS)
#                 VALUES (
#                     (SELECT BOOK_ID FROM BOOKINFO WHERE BOOK_NAME = :book_name),
#                     (SELECT CST_ID FROM CUSTOMERINFO WHERE CST_NAMES = :loan_user),
#                     SYSDATE,
#                     SYSDATE + 7,
#                     '대출 중'
#                 )
#             """
#             cursor.execute(query_insert_borrow, {'book_name': search_book_name, 'loan_user': loan_user})


#         # 🔹 RENTAL 테이블에 대출 기록 추가
#             # query_insert_rental = """
#             #     INSERT INTO RENTAL (BOOK_NAME, CUST_NAME, RENT_DATE)
#             #     VALUES (:1, :2, SYSDATE)
#             # """
#             # cursor.execute(query_insert_rental, (search_book_name, loan_user))

#             conn.commit()  # 변경 사항 저장

#             QMessageBox.about(self, '대출 완료', f'"{search_book_name}" 도서가 "{loan_user}"님께 대출되었습니다!')

#             # 🔹 대출 여부 자동 업데이트 (대출되지 않은 도서는 '가능'으로 설정)
#             self.updateLoanStatus()

#         # UI 업데이트
#             self.loadData()

#         except Exception as e:
#             conn.rollback()  # 오류 발생 시 롤백
#             QMessageBox.critical(self, '오류 발생', f'오류 내용: {str(e)}')

#         finally:
#             cursor.close()
#             conn.close()

#     def updateLoanStatus(self):
#         """ 대출 여부(LOAN_YN) 업데이트: 대출자가 있으면 '불가능', 없으면 '가능' """
#         conn = self.connectDB()
#         cursor = conn.cursor()

#         try:
#             query_update_status = """
#                 UPDATE BOOKINFO
#                 SET LOAN_YN = CASE 
#                     WHEN LOAN_USER IS NULL OR LOAN_USER = '' THEN '가능'
#                     ELSE '불가능'
#                 END
#             """
#             cursor.execute(query_update_status)
#             conn.commit()

#         except Exception as e:
#             QMessageBox.warning(self, '오류 발생', f'오류 내용: {str(e)}')

#         finally:
#             cursor.close()
#             conn.close()


    
#     def btnRetClick(self):
#         """도서 반납 기능"""
#         search_book_name = self.input_std_name.text().strip()

#         if not search_book_name:
#             QMessageBox.warning(self, '경고', '반납할 도서 제목을 입력하세요!')
#             return

#         conn = self.connectDB()
#         cursor = conn.cursor()

#         try:
#         # 🔹 해당 도서가 대출 중인지 확인
#             cursor.execute("SELECT LOAN_USER FROM BOOKINFO WHERE BOOK_NAME = :1", (search_book_name,))
#             book = cursor.fetchone()

#             if not book:
#                 QMessageBox.warning(self, '반납 실패', '해당 도서가 존재하지 않습니다.')
#                 return
#             elif book[0] is None or book[0] == '':
#                 QMessageBox.warning(self, '반납 실패', '이 도서는 이미 반납된 상태입니다.')
#                 return

#         # 🔹 반납 처리 (BOOKINFO 테이블 업데이트)
#             query_return_book = """
#                 UPDATE BOOKINFO
#                 SET LOAN_YN = '가능', LOAN_USER = ''
#                 WHERE BOOK_NAME = :1
#             """
#             cursor.execute(query_return_book, (search_book_name,))

#             conn.commit()  # 변경 사항 저장

#             QMessageBox.about(self, '반납 완료', f'"{search_book_name}" 도서가 반납되었습니다!')

#         # 🔹 대출 여부 자동 업데이트
#             self.updateLoanStatus()

#         # UI 업데이트
#             self.loadData()

#         except Exception as e:
#             conn.rollback()  # 오류 발생 시 롤백
#             QMessageBox.critical(self, '오류 발생', f'오류 내용: {str(e)}')

#         finally:
#             cursor.close()
#             conn.close()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = bookQT()
#     window.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from config import DB_CONFIG
import cx_Oracle as oci
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class bookQT(QMainWindow):
    def __init__(self, book=None, user_email=None):
        super(QMainWindow, self).__init__()
        self.user_email = user_email
        self.initUI()
        self.loadData()
        if book:
            self.populate_fields(book)

    def populate_fields(self, book):
        self.input_std_name.setText(book[0])
        self.input_std_author.setText(book[1])
        self.input_std_pub.setText(book[2])

    def initUI(self):
        ui_path = os.path.join(BASE_DIR, 'book_qt_3.ui')
        uic.loadUi(ui_path, self)
        self.setWindowTitle('도서대출 예약 반납 서비스')
        self.statusbar.showMessage('도서대출 예약 반납 service')

        self.btn_bor.setEnabled(False)
        self.btn_ret.setEnabled(False)

        self.tblbook.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblbook.setColumnCount(5)
        self.tblbook.setHorizontalHeaderLabels(['제목', '저자', '출판사', '대출 여부', '대출자'])
        self.tblbook.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_sea.clicked.connect(self.btnSeaClick)
        self.btn_bor.clicked.connect(self.btnBorClick)
        self.btn_ret.clicked.connect(self.btnRetClick)
        self.btn_clr.clicked.connect(self.btnClearClick)
        self.tblbook.doubleClicked.connect(self.tblbookDoubleClick)

        self.show()

    def connectDB(self):
        return oci.connect(**DB_CONFIG)

    def loadData(self):
        conn = self.connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT BOOK_NAME, AUTHOR, PUBLISHER, LOAN_YN, LOAN_USER FROM BOOKINFO")
        books = cursor.fetchall()
        self.tblbook.setRowCount(len(books))

        for i, row in enumerate(books):
            for j, col in enumerate(row):
                if j == 3:
                    status = "가능" if col == '가능' else "불가능"
                    self.tblbook.setItem(i, j, QTableWidgetItem(status))
                else:
                    self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

    def getInputValues(self):
        return (
            self.input_std_name.text(),
            self.input_std_author.text(),
            self.input_std_pub.text()
        )

    def tblbookDoubleClick(self):
        row = self.tblbook.currentRow()
        if row < 0:
            return
        self.input_std_name.setText(self.tblbook.item(row, 0).text())
        self.input_std_author.setText(self.tblbook.item(row, 1).text())
        self.input_std_pub.setText(self.tblbook.item(row, 2).text())
        self.statusbar.showMessage(f'도서 선택됨: {self.tblbook.item(row, 0).text()}')

    def btnClearClick(self):
        self.input_std_name.clear()
        self.input_std_author.clear()
        self.input_std_pub.clear()
        self.btn_bor.setEnabled(False)
        self.btn_ret.setEnabled(False)
        self.loadData()
        self.statusbar.showMessage('입력 초기화 완료')

    def btnSeaClick(self):
        name, author, pub = self.getInputValues()
        conn = self.connectDB()
        cursor = conn.cursor()

        query = "SELECT BOOK_NAME, AUTHOR, PUBLISHER, LOAN_YN, LOAN_USER FROM BOOKINFO WHERE 1=1"
        params = []
        if name:
            query += " AND BOOK_NAME LIKE '%' || :1 || '%'"
            params.append(name)
        if author:
            query += " AND AUTHOR LIKE '%' || :2 || '%'"
            params.append(author)
        if pub:
            query += " AND PUBLISHER LIKE '%' || :3 || '%'"
            params.append(pub)

        cursor.execute(query, tuple(params))
        books = cursor.fetchall()

        self.tblbook.setRowCount(len(books))
        for i, row in enumerate(books):
            for j, col in enumerate(row):
                self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))

        self.btn_bor.setEnabled(bool(books))
        self.btn_ret.setEnabled(bool(books))

        cursor.close()
        conn.close()

    def btnBorClick(self):
        book_name = self.input_std_name.text().strip()
        user_name = self.input_std_username.text().strip()
        if not book_name or not user_name:
            QMessageBox.warning(self, '입력 오류', '도서 제목과 대출자명을 입력하세요.')
            return

        conn = self.connectDB()
        cursor = conn.cursor()

        try:
            # 1. 이메일로 고객 ID 조회
            cursor.execute("SELECT CST_ID FROM CUSTOMERINFO WHERE CST_EMAIL = :email", {'email': self.user_email})
            result = cursor.fetchone()
            if not result:
                QMessageBox.warning(self, '오류', '이메일 기반 사용자 정보를 찾을 수 없습니다.')
                return

            cst_id = result[0]

            # 2. 도서 상태 확인
            cursor.execute("SELECT BOOK_ID, LOAN_YN FROM BOOKINFO WHERE BOOK_NAME = :1", (book_name,))
            book = cursor.fetchone()
            if not book:
                QMessageBox.warning(self, '대출 실패', '해당 도서를 찾을 수 없습니다.')
                return
            book_id, loan_yn = book

            if loan_yn == '불가능':
                QMessageBox.warning(self, '대출 실패', '이미 대출 중인 도서입니다.')
                return

            # 3. BOOKINFO 테이블 업데이트
            cursor.execute("""
                UPDATE BOOKINFO
                SET LOAN_YN = '불가능', LOAN_USER = :user
                WHERE BOOK_ID = :book_id
            """, {'user': user_name, 'book_id': book_id})

            # 4. BORROWINFO 테이블에 INSERT
            cursor.execute("""
                INSERT INTO BORROWINFO (BOOK_ID, CST_ID, BORROW_DATE, DUE_DATE, STATUS)
                VALUES (:book_id, :cst_id, SYSDATE, SYSDATE + 7, '대출 중')
            """, {'book_id': book_id, 'cst_id': cst_id})

            conn.commit()
            QMessageBox.information(self, '대출 완료', f'{book_name} 도서가 대출되었습니다.')
            self.updateLoanStatus()
            self.loadData()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, 'DB 오류', str(e))
        finally:
            cursor.close()
            conn.close()


    def updateLoanStatus(self):
        conn = self.connectDB()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE BOOKINFO
                SET LOAN_YN = CASE WHEN LOAN_USER IS NULL OR LOAN_USER = '' THEN '가능' ELSE '불가능' END
            """)
            conn.commit()
        except Exception as e:
            QMessageBox.warning(self, '상태 업데이트 오류', str(e))
        finally:
            cursor.close()
            conn.close()

    def btnRetClick(self):
        book_name = self.input_std_name.text().strip()
        if not book_name:
            QMessageBox.warning(self, '입력 오류', '반납할 도서 제목을 입력하세요.')
            return

        conn = self.connectDB()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT LOAN_USER FROM BOOKINFO WHERE BOOK_NAME = :1", (book_name,))
            book = cursor.fetchone()
            if not book or not book[0]:
                QMessageBox.warning(self, '반납 실패', '이미 반납된 도서입니다.')
                return

            cursor.execute("""
                UPDATE BOOKINFO
                SET LOAN_YN = '가능', LOAN_USER = ''
                WHERE BOOK_NAME = :1
            """, (book_name,))
            conn.commit()
            QMessageBox.information(self, '반납 완료', f'{book_name} 도서가 반납되었습니다.')
            self.updateLoanStatus()
            self.loadData()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, 'DB 오류', str(e))
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = bookQT()
    window.show()
    sys.exit(app.exec_())
