import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cx_Oracle as oci
import os
# from PyQt5.QtCore import QSize

# DB 연결 정보
DB_INFO = {
    "sid": "XE",
    "host": "210.119.14.73",
    "port": 1521,
    "username": "bookrentalshop",
    "password": "12345"
}

# UI 파일 로드
UI_FILE = "customer_ui.ui"

class CustomerManager(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.initUI()
        # self.loadData()

    def initUI(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(basedir, UI_FILE)
        uic.loadUi(ui_path, self)  # UI 로드
        self.setWindowTitle('관리자 유저 관리 페이지')
        self.statusbar.showMessage('관리자 유저 관리 페이지')
    # def __init__(self):
    #     super().__init__()
    #     uic.loadUi('C:/Users/Admin/PK_miniproject_3/customer_ui.ui', self)  # UI 로드

    # def initUI(self):
    #     uic.loadUi('customer_ui.ui', self)
    #     self.setWindowTitle('관리자 유저 관리 페이지')
    #     self.statusbar.showMessage('관리자 유저 관리 페이지')
        
        # 테이블 설정
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["고객번호", "성함", "주소", "휴대폰번호", "이메일", "구분"])
        self.tableWidget.setWordWrap(True)  # ✅ 자동 줄 바꿈 설정

        # 새로고침 버튼 연결
        #self.btn_clr.clicked.connect(self.load_data)

        # 버튼 설정
        self.btn_add.clicked.connect(self.add_row)  # 회원 추가 버튼 클릭 시
        self.btn_save.clicked.connect(self.save_data)  # 저장 버튼 클릭 시
        self.btn_del.clicked.connect(self.delete_row)  # 삭제 버튼 (추가)

        # 초기 데이터 로드
        self.load_data()

    def connectDB(self):
        return oci.connect(f"{DB_INFO['username']}/{DB_INFO['password']}@{DB_INFO['host']}:{DB_INFO['port']}/{DB_INFO['sid']}")

    def load_data(self):
        """데이터베이스에서 고객 정보를 불러와 테이블에 표시"""
        conn = self.connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT CST_ID, CST_NAMES, CST_ADDRESS, CST_MOBILE, CST_EMAIL, CST_ROLE FROM CUSTOMERINFO")
        data = cursor.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                # self.setTextAlignment(0x0001)  # ✅ 좌측 정렬 (Qt.AlignLeft)
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

         # ✅ 컬럼 및 행 크기 자동 조정
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def get_next_customer_id(self):
        """DB에서 가장 큰 고객 번호를 가져와 +1 (없으면 26부터 시작)"""
        conn = self.connectDB()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CST_ID) FROM CUSTOMERINFO")
        max_id = cursor.fetchone()[0]  # 가장 큰 고객번호 가져오기
        conn.close()

        return max_id + 1 if max_id else 26  # 없으면 26부터 시작

    
    def add_row(self):
        """새로운 빈 행 추가"""
        new_customer_id = self.get_next_customer_id()  # 다음 고객 번호 가져오기
        self.tableWidget.insertRow(0)  # 상단에 추가
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(new_customer_id)))  # 고객번호 자동 설정

    def save_data(self):
        """현재 tableWidget의 모든 데이터를 데이터베이스에 저장"""
        try:
            conn = self.connectDB()
            cursor = conn.cursor()

            row_count = self.tableWidget.rowCount()

            for row in range(row_count):
                customer_id_item = self.tableWidget.item(row, 0)
                name_item = self.tableWidget.item(row, 1)
                address_item = self.tableWidget.item(row, 2)
                mobile_item = self.tableWidget.item(row, 3)
                email_item = self.tableWidget.item(row, 4)
                role_item = self.tableWidget.item(row, 5)

                if not customer_id_item or not name_item or not name_item.text().strip():
                    continue  # 고객번호와 성함이 없으면 저장하지 않음

                customer_id = customer_id_item.text().strip()
                name = name_item.text().strip()
                address = address_item.text().strip() if address_item else ""
                mobile = mobile_item.text().strip() if mobile_item else ""
                email = email_item.text().strip() if email_item else ""
                role = role_item.text().strip() if role_item else ""

                default_password = "1234"  # 기본 비밀번호 설정

            # ✅ 고객이 이미 존재하는지 확인
                cursor.execute("SELECT COUNT(*) FROM CUSTOMERINFO WHERE CST_ID = :1", (customer_id,))
                count = cursor.fetchone()[0]

                if count == 0:
                # ✅ 존재하지 않으면 INSERT
                    cursor.execute("""
                        INSERT INTO CUSTOMERINFO (CST_ID, CST_NAMES, CST_PWD, CST_ADDRESS, CST_MOBILE, CST_EMAIL, CST_ROLE)
                        VALUES (:1, :2, :3, :4, :5, :6, :7)
                    """, (customer_id, name, default_password, address, mobile, email, role))
                else:
                # ✅ 존재하면 UPDATE
                    cursor.execute("""
                        UPDATE CUSTOMERINFO 
                        SET CST_NAMES = :1, CST_ADDRESS = :2, CST_MOBILE = :3, CST_EMAIL = :4, CST_ROLE = :5
                        WHERE CST_ID = :6
                    """, (name, address, mobile, email, role, customer_id))

            conn.commit()
            QMessageBox.information(self, "저장 완료", "모든 데이터가 정상적으로 저장되었습니다.")

        except Exception as e:
            QMessageBox.critical(self, "오류 발생", f"저장 중 오류가 발생했습니다:\n{str(e)}")

        finally:
            if 'conn' in locals():
                conn.close()



    def delete_row(self):
        """선택한 회원을 데이터베이스와 UI에서 삭제"""
        try:
            selected_row = self.tableWidget.currentRow()  # 선택된 행 가져오기
            if selected_row == -1:
                QMessageBox.warning(self, "삭제 오류", "삭제할 행을 선택하세요.")
                return

            customer_id_item = self.tableWidget.item(selected_row, 0)
            if customer_id_item is None:
                QMessageBox.warning(self, "삭제 오류", "올바른 행을 선택하세요.")
                return

            customer_id = customer_id_item.text().strip()
            if not customer_id.isdigit():
                QMessageBox.warning(self, "삭제 오류", "올바른 고객 번호가 아닙니다.")
                return

            customer_id = int(customer_id)  # 고객번호 정수 변환

        # 삭제 확인 메시지
            reply = QMessageBox.question(self, "삭제 확인", f"정말 고객번호 {customer_id}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        # ✅ 데이터베이스 연결
            conn = self.connectDB()
            cursor = conn.cursor()

        # ✅ 삭제할 고객이 DB에 존재하는지 확인
            cursor.execute("SELECT COUNT(*) FROM CUSTOMERINFO WHERE CST_ID = :1", (customer_id,))
            count = cursor.fetchone()[0]
            if count == 0:
                QMessageBox.warning(self, "삭제 오류", "해당 고객이 존재하지 않습니다.")
                return

        # ✅ 데이터 삭제
            cursor.execute("DELETE FROM CUSTOMERINFO WHERE CST_ID = :1", (customer_id,))
            conn.commit()

        # ✅ 삭제 후 UI에서도 행 제거
            self.tableWidget.removeRow(selected_row)

            QMessageBox.information(self, "삭제 완료", f"고객번호 {customer_id}가 삭제되었습니다.")

        except Exception as e:
            QMessageBox.critical(self, "오류 발생", f"삭제 중 오류가 발생했습니다:\n{str(e)}")

        finally:
        # ✅ 데이터베이스 연결 닫기
            if 'conn' in locals():
                conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerManager()
    window.show()
    sys.exit(app.exec_())
