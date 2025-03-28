import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cx_Oracle as oci
# from PyQt5.QtCore import QSize

# DB 연결 정보
DB_INFO = {
    "sid": "XE",
    "host": "210.119.14.73",
    "port": 1521,
    "username": "bookrentalshop",
    "password": "12345"
}

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        uic.loadUi('book_qt_3.ui', self)
        self.setWindowTitle('도서대출 예약 반납 서비스')
        self.statusbar.showMessage('도서대출 예약 반납 service')

        # 🔹 초기 상태에서 대출/반납 버튼 비활성화
        self.btn_bor.setEnabled(False)
        self.btn_ret.setEnabled(False)


        
        # 테이블 위젯 설정
        self.tblbook.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblbook.setColumnCount(5)
        self.tblbook.setHorizontalHeaderLabels(['제목', '저자', '출판사', '대출 여부', '대출자'])

        # 🔹 더블 클릭 시 편집 방지
        self.tblbook.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 버튼에 아이콘 추가
        # self.btn_sea.setIcon(QIcon('./image/book_sea.png'))
        # self.btn_sea.setIconSize(QSize(50, 50))
        # self.btn_bor.setIcon(QIcon('./image/book_bor.png'))
        # self.btn_ret.setIcon(QIcon('./image/book_ret.png'))
        # self.btn_clr.setIcon(QIcon('./image/reset.png'))
        
        # 버튼 이벤트 연결
        self.btn_sea.clicked.connect(self.btnSeaClick)
        self.btn_bor.clicked.connect(self.btnBorClick)
        self.btn_ret.clicked.connect(self.btnRetClick)
        self.btn_clr.clicked.connect(self.btnClearClick)
        
        self.tblbook.doubleClicked.connect(self.tblbookDoubleClick)
        self.show()

    
    def connectDB(self):
        return oci.connect(f"{DB_INFO['username']}/{DB_INFO['password']}@{DB_INFO['host']}:{DB_INFO['port']}/{DB_INFO['sid']}")
    
    def loadData(self):
        conn = self.connectDB()
        cursor = conn.cursor()
        query = '''SELECT BOOK_NAME, AUTHOR, PUBLISHER FROM BOOKINFO''' 
        cursor.execute(query)
        
        books = cursor.fetchall()
        self.tblbook.setRowCount(len(books))
        
        for i, row in enumerate(books):
            for j, col in enumerate(row):
                self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))
        
        cursor.close()
        conn.close()

    
    def getInputValues(self):
        return (
            self.input_std_name.text(),
            self.input_std_author.text(),
            self.input_std_pub.text(),
            self.input_std_div.text()
        )
    
    def tblbookDoubleClick(self):
        selected = self.tblbook.currentRow()
        if selected < 0:
            return
        
        input_fields = [
            self.input_std_name,  # 제목
            self.input_std_author,  # 저자
            self.input_std_pub,  # 출판사
            None,  # 대출 여부 (입력 필드 없음)
            None   # 대출자 (입력 필드 없음)
        ]

        for i in range(len(input_fields)):
            if input_fields[i] is not None:  # 입력 필드가 있는 경우만 설정
                item = self.tblbook.item(selected, i)
                if item:
                    input_fields[i].setText(item.text())

        self.statusbar.showMessage(f'도서 선택됨: {self.tblbook.item(selected, 0).text()}')


        # for i in range(6):
        #     getattr(self, f"input_std_{['name', 'author'][i]}").setText(self.tblbook.item(selected, i).text())
        
        # self.statusbar.showMessage('도서정보 선택됨')

    def btnClearClick(self):
        # 확인 메시지 표시
        reply = QMessageBox.question(self, '초기화 확인', '정말로 초기화 하시겠습니까?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            return  # 사용자가 "아니오"를 선택하면 초기화 취소
    # 입력 필드 초기화
        self.input_std_name.clear()
        self.input_std_author.clear()
        self.input_std_pub.clear()
        self.input_std_div.clear()

        # 🔹 대출/반납 버튼 비활성화
        self.btn_bor.setEnabled(False)
        self.btn_ret.setEnabled(False)
    
    # 전체 도서 데이터 다시 불러오기
        self.loadData()

        self.statusbar.showMessage('입력 필드 초기화 및 전체 데이터 로드 완료')

    
    def btnSeaClick(self):
        values = self.getInputValues()
        search_book_name, search_author, search_publisher = values[0], values[1], values[2]

        if not search_book_name and not search_author:
            QMessageBox.warning(self, '경고', '조회할 제목, 저자 중 하나를 입력하세요!')
            return

        conn = self.connectDB()
        cursor = conn.cursor()

    # 조건문 동적으로 설정
        query = "SELECT BOOK_NAME, AUTHOR, PUBLISHER FROM BOOKINFO WHERE 1=1"
        params = []

        if search_book_name:
            query += " AND BOOK_NAME LIKE '%' || :1 || '%'".format(len(params) + 1)
            params.append(search_book_name)

        if search_author:
            query += " AND AUTHOR LIKE '%' || :2 || '%'".format(len(params) + 1)
            params.append(search_author)

        if search_publisher:
            query += " AND PUBLISHER LIKE '%' || :3 || '%'".format(len(params) + 1)
            params.append(search_publisher)

        cursor.execute(query, tuple(params))
        books = cursor.fetchall()

        if not books:
            QMessageBox.warning(self, '조회 실패', '해당 도서를 찾을 수 없습니다!')

            # 전체 데이터 다시 조회
            cursor.execute("SELECT BOOK_NAME, AUTHOR, PUBLISHER FROM BOOKINFO")
            books = cursor.fetchall()

        if not books:
            QMessageBox.warning(self, '조회 실패', '해당 도서를 찾을 수 없습니다!')
            self.btn_bor.setEnabled(False)  # 조회 실패 시 버튼 비활성화
            self.btn_ret.setEnabled(False)
        else:
        # 🔹 조회 성공하면 대출/반납 버튼 활성화
            self.btn_bor.setEnabled(True)
            self.btn_ret.setEnabled(True)

        # 테이블 초기화 후 데이터 출력
        self.tblbook.clearContents()
        self.tblbook.setRowCount(len(books))


        for i, row in enumerate(books):
            for j, col in enumerate(row):
                self.tblbook.setItem(i, j, QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

  
    
    def btnBorClick(self):
        values = self.getInputValues()
        search_book_name, search_author, search_publisher = values[0], values[1], values[2]
        if not search_book_name and not search_author and not search_publisher:
            QMessageBox.warning(self, '경고', '도서 제목이나 저자를 입력하세요!')
            return
        
        # 🔹 대출 확인 메시지
        reply = QMessageBox.question(self, '대출 확인', '정말 대출하시겠습니까?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return  # 사용자가 "아니오"를 선택하면 대출 취소

        conn = self.connectDB()
        cursor = conn.cursor()

    # 먼저 해당 도서의 대출 가능 여부 확인
        cursor.execute("SELECT LOAN_YN FROM BOOKINFO WHERE BOOK_NAME = :1", (search_book_name, search_author, search_publisher))
        book = cursor.fetchone()

        if not book:
            QMessageBox.warning(self, '대출 실패', '해당 도서가 존재하지 않습니다.')
        elif book[0] == 'Y':  # 이미 대출된 상태
            QMessageBox.warning(self, '대출 실패', '대출이 불가능합니다.')
        else:
        # 대출 가능하면 대출 처리
            query = "UPDATE BOOKINFO SET LOAN_YN='Y', LOAN_USER='사용자' WHERE BOOK_NAME = :1"
            cursor.execute(query, (search_book_name, search_author, search_publisher))
            conn.commit()

            QMessageBox.about(self, '대출 완료', '도서가 대출되었습니다!')

        cursor.close()
        conn.close()
    
        self.loadData()  # 테이블 최신화

    
    def btnRetClick(self):
        book_name = self.input_std_name.text()
        if not book_name:
            QMessageBox.warning(self, '경고', '도서 제목이나 저자를 입력하세요!')
            return
        
         # 🔹 반납 확인 메시지
        reply = QMessageBox.question(self, '반납 확인', '정말 반납을 완료하시겠습니까?', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return  # 사용자가 "아니오"를 선택하면 반납 취소
        
        conn = self.connectDB()
        cursor = conn.cursor()
        query = "UPDATE BOOKINFO SET LOAN_YN='N', LOAN_USER=NULL WHERE BOOK_NAME = :1"
        cursor.execute(query, (book_name))
        conn.commit()
        
        if cursor.rowcount:
            QMessageBox.about(self, '반납 완료', '도서가 반납되었습니다!')
        else:
            QMessageBox.warning(self, '반납 실패', '해당 도서를 반납할 수 없습니다.')
        
        cursor.close()
        conn.close()
        self.loadData()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()
