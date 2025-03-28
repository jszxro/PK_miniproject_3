import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic

# Oracle 모듈 
import cx_Oracle as oci

# Qt 리소스 시스템 사용
import resources

# DB 연결 설정
sid = 'XE'
host = '210.119.14.73'  # 외부에서 접속할 경우 변경
port = 1521
username = 'bookrentalshop'
password = '12345'
basic_msg = 'Bukjeok x 2 Mypage'

class MainWindow(QMainWindow): 
    def __init__(self):       
        super(MainWindow,self).__init__()
        self.initUI()
        self.loadData1()
        self.loadData2()

    def initUI(self):
        uic.loadUi('D:/keh/미니프로젝트(3조;20250325-31)/파일/최종본/ui/mypage.ui', self)
        self.setWindowTitle('북적북적 My Page')
        self.setWindowIcon(QIcon(":/image/img/책든햄찌_nobg.png"))
        self.setWindowIcon(QIcon(":/image/img/책든햄찌_nobg.png"))
        self.setWindowIcon(QIcon(":/profile/img/귀여운 토끼.png"))
        self.setWindowIcon(QIcon(":/icon/img/귀여운_네잎클로버_nobg.png"))

        # 상태바에 메세지 추가
        self.statusbar.showMessage(basic_msg)

    # 버튼 시그널(이벤트) 추가
        self.btn_logout.clicked.connect(self.btnLogOut)
        self.btn_save.clicked.connect(self.btnSave)
        self.btn_clear.clicked.connect(self.btnClear)
        self.btn_write.clicked.connect(self.btnWrite)
        self.btn_mark.clicked.connect(self.btnMark)
        self.show()
        ### 함수를 만들면 반드시 함수선언을 할 것!!!
    

    # 화면의 인풋위젯 데이터 초기화함수
    def clearInput(self):
        self.input_nick.clear()
        self.input_stat.clear()
    

    

    # 로그아웃 버튼 클릭 시그널처리 함수
    def btnLogOut(self):
        QMessageBox.about(self, '알림', '로그아웃 되었습니다 !')
        
        # 상태바에 메세지 추가
        self.statusbar.showMessage(f'{basic_msg} | 로그아웃 완료')

    def btnSave(self):
        nick = self.input_nick.text()
        stat = self.input_stat.text()
        
        if nick and stat:
            QMessageBox.about(self, '알림', f'닉네임: {nick}, 상태 메시지: {stat} 저장 완료!')
            self.statusbar.showMessage(f'{basic_msg} | 닉네임 및 상태 메시지 저장 완료')
        else:
            QMessageBox.warning(self, '경고', '닉네임과 상태 메시지를 입력해주세요!')

    # 초기화 버튼 클릭 시그널처리 함수
    def btnClear(self):
        self.input_nick.clear()
        self.input_stat.clear()
        self.statusbar.showMessage(f'{basic_msg} | 닉네임 및 상태메세지 초기화 완료')


    #  감상문 쓰기 클릭 시그널처리 함수
    def btnWrite(self):
        QMessageBox.about(self, '알림', '감상문을 추가하였습니다 !')

        # 상태바에 메세지 추가
        self.statusbar.showMessage(f'{basic_msg} | 감상문 작성 완료')

    # 즐겨찾기 클릭 시 시그널 함수
    def btnMark(self):
        QMessageBox.about(self, '알림', '책을 즐겨찾기에 추가하였습니다 !')
    


    # 테이블 위젯 데이터와 연관해서 화면 설정 !!
    def makeTable1(self, lst_books1):
        self.tblbook_rect.setSelectionMode(QAbstractItemView.SingleSelection) # 단일row 선택모드
        self.tblbook_rect.setEditTriggers(QAbstractItemView.NoEditTriggers) #컬럼수정금지모드
        self.tblbook_rect.setColumnCount(5)
        self.tblbook_rect.setRowCount(len(lst_books1))  # 커서에 들어있는 데이터의 길이만큼 row 생성 !!
        self.tblbook_rect.setHorizontalHeaderLabels(['분류','책제목','저자','출판사', '반납일'])

        # 전달받은 cursor를 반복문(for문)으로 테이블위젯에 적용하는 작업
        ## 테이블 위젯은 문자로 된 단어만 받으므로 숫자는 전부 str 작업을 해줘야 함!!! 꼭 기억하기 !! (20250326)
        for i, (division, book_name, author, publisher, return_date) in enumerate(lst_books1):
            self.tblbook_rect.setItem(i,0,QTableWidgetItem(division))
            self.tblbook_rect.setItem(i,1,QTableWidgetItem(book_name))
            self.tblbook_rect.setItem(i,2,QTableWidgetItem(author))
            self.tblbook_rect.setItem(i,3,QTableWidgetItem(publisher))
            self.tblbook_rect.setItem(i,4,QTableWidgetItem(str(return_date)))

    def makeTable2(self, lst_books2):
        self.tblbook_borr.setSelectionMode(QAbstractItemView.SingleSelection) # 단일row 선택모드
        self.tblbook_borr.setEditTriggers(QAbstractItemView.NoEditTriggers) #컬럼수정금지모드
        self.tblbook_borr.setColumnCount(7)
        self.tblbook_borr.setRowCount(len(lst_books2))  # 커서에 들어있는 데이터의 길이만큼 row 생성 !!
        self.tblbook_borr.setHorizontalHeaderLabels(['분류','책제목','저자','출판사', '빌린날','반납기한','상태'])

        # 전달받은 cursor를 반복문(for문)으로 테이블위젯에 적용하는 작업
        for i, (division, book_name, author, publisher, borrow_date, due_date, status) in enumerate(lst_books2):
            self.tblbook_borr.setItem(i,0,QTableWidgetItem(division))
            self.tblbook_borr.setItem(i,1,QTableWidgetItem(book_name))
            self.tblbook_borr.setItem(i,2,QTableWidgetItem(author))
            self.tblbook_borr.setItem(i,3,QTableWidgetItem(publisher))
            self.tblbook_borr.setItem(i,4,QTableWidgetItem(str(borrow_date)))
            self.tblbook_borr.setItem(i,5,QTableWidgetItem(str(due_date)))
            self.tblbook_borr.setItem(i,6,QTableWidgetItem(status))

    # R(SELECT)
    def loadData1(self):
        # DB연결
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            query = '''SELECT i.DIVISION
	                       , i.BOOK_NAME
	                       , i.AUTHOR
	                       , i.PUBLISHER
	                       , b.RETURN_DATE
                         FROM bookinfo i, BORROWINFO b
                        WHERE i.BOOK_ID = b.BOOK_ID
                        ORDER BY DIVISION ASC'''
            cursor.execute(query)

            lst_books1 = []  # 리스트 생성
            for item in cursor:
                lst_books1.append(item)

            self.makeTable1(lst_books1) # 새로 생성한 리스트를 파라미터로 전달
        
        except Exception as e:
            print(f"데이터를 불러오는 데 실패했습니다. : {e}")
        
        finally:
            cursor.close()
            conn.close()

    def loadData2(self):
        # DB연결
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            query = '''SELECT i.DIVISION
	                        , i.BOOK_NAME
	                        , i.AUTHOR
	                        ,   i.PUBLISHER
	                        , b.BORROW_DATE
	                        , b.DUE_DATE
	                        , b.STATUS
                        FROM bookinfo i, BORROWINFO b
                       WHERE i.BOOK_ID = b.BOOK_ID
                       ORDER BY DIVISION ASC'''
            cursor.execute(query)

            lst_books2 = []  # 리스트 생성
            for item in cursor:
                lst_books2.append(item)

            self.makeTable2(lst_books2) # 새로 생성한 리스트를 파라미터로 전달
        
        except Exception as e:
            print(f"데이터를 불러오는 데 실패했습니다. : {e}")
        
        finally:
            cursor.close()
            conn.close()


       
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()                 
    app.exec_()
