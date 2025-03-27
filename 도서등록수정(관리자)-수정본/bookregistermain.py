import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic

# Oracle 모듈 
import cx_Oracle as oci

# DB 연결 설정
sid = 'XE'
host = '210.119.14.73'  # 외부에서 접속할 경우 변경
port = 1521
username = 'bookrentalshop'
password = '12345'
basic_msg = '도서 등록 / 수정 (관리자용) v1.0'

class MainWindow(QMainWindow): 
    def __init__(self):       
        super(MainWindow,self).__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        uic.loadUi('bookregisterdb_ss.ui', self)
        self.setWindowTitle('도서 등록 및 수정(관리자용)')
        self.setWindowIcon(QIcon('book.png'))

        # 상태바에 메세지 추가
        self.statusbar.showMessage(basic_msg)


        # 버튼에 아이콘 추가
        self.btn_add.setIcon(QIcon('plus.png'))
        self.btn_mod.setIcon(QIcon('edit.png'))
        self.btn_del.setIcon(QIcon('minus.png'))
    
    # 버튼 시그널(이벤트) 추가
        self.btn_add.clicked.connect(self.btnAddClick)
        self.btn_mod.clicked.connect(self.btnModClick)
        self.btn_del.clicked.connect(self.btnDelClick)
        # 테이블위젯 더블클릭 시그널 추가
        self.tblBooks.doubleClicked.connect(self.tblBooksDoubleClick)
        self.show()
        ### 함수를 만들면 반드시 함수선언을 할 것!!!
    

    # 화면의 인풋위젯 데이터 초기화함수
    def clearInput(self):
        self.input_book_idno.clear()
        self.input_book_type.clear()
        self.input_book_name.clear()
        self.input_book_edit.clear()
        self.input_book_pubs.clear()
        self.input_book_date.clear()
        self.input_book_cost.clear()

    # 테이블위젯 더블클릭 시그널처리 함수 !
    def tblBooksDoubleClick(self):
        selected = self.tblBooks.currentRow()  # 현재 선택된 row의 index를 반환하는 함수 !!
        book_id = self.tblBooks.item(selected, 0).text()
        division = self.tblBooks.item(selected, 1).text()
        book_name = self.tblBooks.item(selected, 2).text()
        author = self.tblBooks.item(selected, 3).text()
        publisher = self.tblBooks.item(selected, 4).text()
        release_dt = self.tblBooks.item(selected, 5).text()
        book_price = self.tblBooks.item(selected, 6).text()

        self.input_book_idno.setText(book_id)
        self.input_book_type.setText(division)
        self.input_book_name.setText(book_name)
        self.input_book_edit.setText(author)
        self.input_book_pubs.setText(publisher)
        self.input_book_date.setText(release_dt)
        self.input_book_cost.setText(book_price)

        # 상태바에 메세지 추가
        self.statusbar.showMessage(f'{basic_msg} | 도서 정보 확인')

    

    # 추가버튼 클릭 시그널처리 함수
    def btnAddClick(self):
        book_id = self.input_book_idno.text()
        division = self.input_book_type.text()
        book_name = self.input_book_name.text()
        author = self.input_book_edit.text()
        publisher = self.input_book_pubs.text()  
        release_dt= self.input_book_date.text()
        book_price = self.input_book_cost.text()
        print(book_id, division, book_name, author, publisher, release_dt,  book_price)

        # 입력 검증 필수(Validation Check)  ; 반드시 해줘야 할 것 !!
        if book_id == '' or division == '' or book_name == '' :
            QMessageBox.warning(self,'경고', '도서 ID, 분류 또는 도서제목을 반드시 입력해 주세요 !')
            return    # 함수를 탈출해주기 위해서 !!
        
        #elif book_id != '':
            #QMessageBox.warning(self, '경고', '이미 등록된 ID를 다시 등록할 수 없습니다.')

        #elif book_name != '':
            #QMessageBox.warning(self, '경고', '이미 등록된 제목을 다시 등록할 수 없습니다.')
        else:
            print('도서 정보를 입력합니다.')
            values = (book_id, division, book_name, author, publisher, release_dt,  book_price)
            if self.addData(values) == True:
                QMessageBox.about(self, '저장 성공', '도서 정보 등록 성공!')
            else:
                QMessageBox.about(self, '저장 실패', '작성한 ID와 제목이 중복되었는지 확인해 주세요!')

            self.loadData()    # 다시 테이블위젯 데이터를 DB에서 조회
            self.clearInput()  # 인풋값 삭제 함수 호출 !

            # 상태바에 메세지 추가
            self.statusbar.showMessage(f'{basic_msg} | 도서 정보 저장 완료')

    
    # 수정버튼 클릭 시그널처리 함수
    def btnModClick(self):
        book_id = self.input_book_idno.text()
        division = self.input_book_type.text()
        book_name = self.input_book_name.text()
        author = self.input_book_edit.text()
        publisher = self.input_book_pubs.text()  
        release_dt= self.input_book_date.text()
        book_price = self.input_book_cost.text()

        if book_id == '' or book_name == '' or division == '':
            QMessageBox.warning(self, '경고','도서 ID, 도서제목 또는 분류를 반드시 입력해 주세요 !')
            return         # 함수를 탈출!!!!!! (위기탈출 넘버원.)
        else:
            print('도서 정보를 수정합니다.')
            values = (book_id, division, book_name, author, publisher, release_dt,  book_price)

            result = self.modData(values)
            print(f"modData 실행결과 : {result}")  # 결과확인용!!!!

            
            #if self.modData(values) == True:
            if result == True:
                QMessageBox.about(self, '수정 성공', '도서 정보 수정 성공!')
            else:
                QMessageBox.about(self, '수정 실패', '담당 부서에 문의하세요.')
            
            # 수정 후 바로 로드!!
            print("loadData 호출됨 !")
            self.loadData()
            self.clearInput()

            # 상태바에 메세지 추가
            self.statusbar.showMessage(f'{basic_msg} | 도서 정보 수정 완료')

     # 삭제 버튼 클릭 시 시그널 함수
    def btnDelClick(self):
        book_id = self.input_book_idno.text()#.strip()

        #book_name = self.input_book_name.text()
        if book_id == '':
            QMessageBox.warning(self, '경고','도서 ID를 반드시 입력해 주세요 !')
            return    # 함수를 탈출해주기 위해서 !!
        else:
            print(f'도서 정보 삭제를 진행합니다. (ID : {book_id})')

            if self.delData(book_id) == True:
                QMessageBox.about(self, '삭제 성공', '도서 정보 삭제 성공!')
            else:
                QMessageBox.about(self, '삭제 실패', '담당 부서에 문의하세요.')

            self.loadData() 
            self.clearInput()

            # 상태바에 메세지 추가
            self.statusbar.showMessage(f'{basic_msg} | 도서 정보 삭제 완료')


    # 테이블 위젯 데이터와 연관해서 화면 설정 !!
    # 원하는 단어에 드래그 후 f12누르면 그 다음 단어로 이동 !!!!! 대박박이!!!! 
    def makeTable(self, lst_books):
        self.tblBooks.setSelectionMode(QAbstractItemView.SingleSelection) # 단일row 선택모드
        self.tblBooks.setEditTriggers(QAbstractItemView.NoEditTriggers) #컬럼수정금지모드
        self.tblBooks.setColumnCount(7)
        self.tblBooks.setRowCount(len(lst_books))  # 커서에 들어있는 데이터의 길이만큼 row 생성 !!
        self.tblBooks.setHorizontalHeaderLabels(['도서 ID','분류','도서제목','저자','출판기관', '출판일자','가격'])

        # 전달받은 cursor를 반복문(for문)으로 테이블위젯에 적용하는 작업
        ## 테이블 위젯은 문자로 된 단어만 받으므로 숫자는 전부 str 작업을 해줘야 함!!! 꼭 기억하기 !! (20250326)
        # i = 0
        for i, (book_id, division, book_name, author, publisher, release_dt, book_price) in enumerate(lst_books):
            self.tblBooks.setItem(i,0,QTableWidgetItem(str(book_id)))
            self.tblBooks.setItem(i,1,QTableWidgetItem(division))
            self.tblBooks.setItem(i,2,QTableWidgetItem(book_name))
            self.tblBooks.setItem(i,3,QTableWidgetItem(author))
            self.tblBooks.setItem(i,4,QTableWidgetItem(publisher))
            self.tblBooks.setItem(i,5,QTableWidgetItem(str(release_dt)))
            self.tblBooks.setItem(i,6,QTableWidgetItem(str(book_price)))
            # i+=1

    # R(SELECT)
    def loadData(self):
        # DB연결
        try:
            conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
            cursor = conn.cursor()

            query = '''SELECT BOOK_ID, DIVISION, BOOK_NAME, AUTHOR, PUBLISHER, RELEASE_DT, BOOK_PRICE
                         FROM BOOKINFO
                         ORDER BY BOOK_ID ASC'''
            cursor.execute(query)

            lst_books = []  # 리스트 생성
            for item in cursor:
                lst_books.append(item)

            self.makeTable(lst_books) # 새로 생성한 리스트를 파라미터로 전달
        
        except Exception as e:
            print(f"Error loading data: {e}")
        
        finally:
            cursor.close()
            conn.close()

    # C(INSERT)
    def addData(self, tuples):
        isSucceed = False # 성공여부 플래그 변수
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin()   # BEGIN TRANSACTION : 트랜잭션 시작

            # 쿼리 만들기
            query = '''
                    INSERT INTO BOOKRENTALSHOP.BOOKINFO (book_id, division, book_name, author, publisher, release_dt,  book_price)
                    VALUES (:v_book_id, :v_division, :v_book_name, :v_author, :v_publisher, TO_DATE(:v_release_dt, 'YYYY-MM-DD'), :v_book_price)
                    '''
            
            ## GPT의 도움 .... 
            cursor.execute(query,{
            'v_book_id': tuples[0],
            'v_division': tuples[1],
            'v_book_name': tuples[2],
            'v_author': tuples[3],
            'v_publisher': tuples[4],
            'v_release_dt': tuples[5],
            'v_book_price': tuples[6]
        })

            conn.commit()   # DB commit과 동일기능이래 ~
            last_id = cursor.lastrowid  # SEQ_STUDENT.CURRVAL
            print(last_id)
            isSucceed = True # 트랜젝션 성공!! ^_^!!
            #return True     # DB 입력 성공 !!
        except Exception as e:
            print(e)
            conn.rollback()   # DB rollback 동일기능 !!
            isSucceed = False # 트랜잭션 실패!! -_- ; finally에는 isSucced = False 쓰지 말자~
            
        finally:
            cursor.close()
            conn.close()
        
        # 줄맞춤에 항상 주의하자 !!!!
        return isSucceed      # 트랜잭션 여부를 리턴
    
    # U(Update)
    def modData(self, tuples):
        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin()  # 트랜잭션 시작

            print(f"수정할 값 : {tuples}")

            # 날짜 값 변환 (시간 제거)
            if tuples[5]:  
                release_dt = tuples[5].split(" ")[0]  # 'YYYY-MM-DD'만 추출
            else:
                release_dt = None  

            # UPDATE 쿼리
            query = '''
                UPDATE BOOKRENTALSHOP.BOOKINFO
                    SET division =  :v_division
                    , book_name = :v_book_name
                    , author = :v_author
                    , publisher = :v_publisher
                    , release_dt = TO_DATE(:v_release_dt, 'YYYY-MM-DD')
                    , book_price = :v_book_price
                    WHERE book_id = :v_book_id
                '''
        
            # 변환된 release_dt 사용!
            cursor.execute(query, {
            'v_book_id': tuples[0],
            'v_division': tuples[1],
            'v_book_name': tuples[2],
            'v_author': tuples[3],
            'v_publisher': tuples[4],
            'v_release_dt': release_dt,  # ✅ 수정된 값 적용
            'v_book_price': tuples[6]
            })  

            conn.commit()  # 트랜잭션 커밋

            isSucceed = True 
        except Exception as e:
            print(e)
            conn.rollback()  # 에러 발생 시 롤백
            isSucceed = False 
        finally:
            cursor.close()
            conn.close()

        return isSucceed
    
    # D(Delete)

    def delData(self, book_id):
        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            conn.begin()  

            # 쿼리 만들기   -- addData에서 쿼리만 바꾸면 됨 !!
            query = '''
                   DELETE FROM BOOKINFO WHERE book_id = :v_book_id
                    '''
            cursor.execute(query, {'v_book_id' : book_id})  

            conn.commit()  
            isSucceed = True 
        except Exception as e:
            print(e)
            conn.rollback()  
            isSucceed = False 
            
        finally:
            cursor.close()
            conn.close()
    
        return isSucceed

       
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()                 
    app.exec_()
