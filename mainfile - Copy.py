import datetime
import sys

import MySQLdb
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

from play import Ui_MainWindow as Program

# Program, _ = loadUiType('play.ui')

my_db = MySQLdb.connect(host='localhost', user='root', password='159753852456', db='project')
my_db.set_character_set('utf8')


class MainApp(QMainWindow, Program):
    def __init__(self):
        super(MainApp, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.showMaximized()
        self.db = my_db
        self.ui_changes()
        self.buttons()
        self.init_tabs()
        self.all_bus()
        self.show_all_students()
        self.show_all_employees()
        self.show_questions()
        self.show_operations()
        self.show_all_operations()
        self.deadline_notification()
        self.all_daily_login()

        self.cur.execute('''SELECT * FROM students''')
        self.std = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM bus''')
        self.b = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM questions''')
        self.q = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM daily''')
        self.d = self.cur.fetchall()

        # Time Display
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.today)
        self.timer.start()

        # Other DB users
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()

    def ui_changes(self):
        # Hiding Tab head
        self.tabWidget.tabBar().setVisible(False)
        # Show sorting
        self.tableWidget_5.setSortingEnabled(True)
        self.tableWidget_11.setSortingEnabled(True)
        self.tableWidget_6.setSortingEnabled(True)
        # init calender
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_3.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_5.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_6.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_7.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_8.setDateTime(QDateTime.currentDateTime())

        self.groupBox.setHidden(True)
        self.groupBox_2.setHidden(False)

        # in & out students Numbers
        # Fetch Data from Database
        self.absent = 0
        self.come = 0
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT * FROM students ''')
        data = self.cur.fetchall()
        self.absent = len(data)
        self.lcdNumber_2.display(int(self.absent))
        self.lcdNumber.display(int(self.come))

    def init_tabs(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(0)
        self.tabWidget_6.setCurrentIndex(0)
        self.tabWidget_7.setCurrentIndex(0)
        self.tabWidget_8.setCurrentIndex(0)

    def buttons(self):
        # Opening Tabs ( Employer)
        self.pushButton.clicked.connect(self.open_daily)
        self.pushButton_2.clicked.connect(self.open_students)
        self.pushButton_31.clicked.connect(self.open_activities)
        self.pushButton_4.clicked.connect(self.open_employees)
        self.pushButton_3.clicked.connect(self.open_financial)
        self.pushButton_7.clicked.connect(self.open_history)
        self.pushButton_6.clicked.connect(self.open_settings)
        self.pushButton_28.clicked.connect(self.open_bus)

        # ---------------
        # Employer Tasks
        # ---------------

        # Daily Activities
        self.pushButton_5.clicked.connect(self.daily_sign)
        self.pushButton_8.clicked.connect(self.daily_pay)
        self.pushButton_32.clicked.connect(self.questions)

        # dealing with Students
        self.pushButton_12.clicked.connect(self.new_student)
        self.pushButton_14.clicked.connect(self.search_student_for_edit)
        self.pushButton_11.clicked.connect(self.student_search)
        self.pushButton_13.clicked.connect(self.edit_student)
        self.pushButton_30.clicked.connect(self.delete_student)

        # dealing with employees
        self.pushButton_15.clicked.connect(self.new_employee)
        self.pushButton_29.clicked.connect(self.delete_employee)
        # ----------
        self.pushButton_21.clicked.connect(self.new_coach)
        self.pushButton_25.clicked.connect(self.training_search)

        # dealing with trainees
        self.pushButton_22.clicked.connect(self.new_trainee)
        self.pushButton_26.clicked.connect(self.trainees_search)
        self.pushButton_24.clicked.connect(self.search_trainee_for_edit)
        self.pushButton_23.clicked.connect(self.edit_trainee)
        self.pushButton_33.clicked.connect(self.delete_trainee)

        # Dealing with financial
        self.pushButton_16.clicked.connect(self.add_operation)

        # Bus
        self.pushButton_34.clicked.connect(self.new_bus)
        # dealing with users
        self.pushButton_17.clicked.connect(self.new_user)
        self.pushButton_18.clicked.connect(self.delete_user)
        self.pushButton_19.clicked.connect(self.edit_user)
        self.pushButton_20.clicked.connect(self.search_user)

        # login
        self.pushButton_27.clicked.connect(self.login)

    def today(self):
        day = datetime.datetime.today().strftime('%A')
        date = datetime.datetime.now().strftime("%m/%d/%Y   %H:%M:%S")
        self.label_65.setText(f'{day}  {date}')
    # *******************************
    #   Opening  Tabs
    # *******************************

    def open_daily(self):
        self.tabWidget.setCurrentIndex(0)

    def open_students(self):
        self.tabWidget.setCurrentIndex(1)

    def open_activities(self):
        self.tabWidget.setCurrentIndex(2)

    def open_employees(self):
        self.tabWidget.setCurrentIndex(3)

    def open_financial(self):
        self.tabWidget.setCurrentIndex(4)

    def open_history(self):
        self.tabWidget.setCurrentIndex(5)

    def open_settings(self):
        self.tabWidget.setCurrentIndex(6)

    def open_bus(self):
        self.tabWidget.setCurrentIndex(7)

    # *******************************
    #   Daily Activities
    # *******************************

    def daily_pay(self):
        self.cur = self.db.cursor()

        # Getting Info from UI
        student_code = self.lineEdit_2.text()
        if len(self.lineEdit_3.text()) > 0:
            paid = int(self.lineEdit_3.text())
        else:
            paid = 0

        start = self.dateEdit_5.date().toPyDate()
        finish = self.dateEdit_6.date().toPyDate()

        # Fetch Data from Database
        self.cur.execute('''SELECT name,paid_money,monthly_pay FROM students WHERE id=%s''', [student_code])
        data = self.cur.fetchone()
        if data:
            self.cur.execute('''UPDATE students SET paid_money=%s WHERE id=%s''', ((data[1] + paid), student_code))
            self.cur.execute('''UPDATE students SET starting_date=%s,ending_date=%s  WHERE id=%s''', (start, finish))
            self.cur.execute('''UPDATE students SET paid_money=%s,monthly_pay=%s WHERE id=%s''',
                             ((data[1] + paid), paid, student_code))

            row_pos = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pos)
            self.tableWidget_2.setItem(row_pos, 0, QTableWidgetItem(str(data[0])))
            self.tableWidget_2.setItem(row_pos, 1, QTableWidgetItem(str(paid)))
            self.tableWidget_2.setItem(row_pos, 2, QTableWidgetItem(str(datetime.datetime.now())))

            # date = datetime.datetime.now()
            # today = datetime.datetime.today().strftime('%A')
            # day_name = ''
            # if today == 'Saturday':
            #     day_name = 'السبت'
            # elif today == 'ٍSunday':
            #     day_name = 'الاحد'
            # elif today == 'Monday':
            #     day_name = 'الاثنين'
            # elif today == 'Tuesday':
            #     day_name = 'الثلاثاء'
            # elif today == 'Wednesday':
            #     day_name = 'الاربعاء'
            # elif today == 'Thursday':
            #     day_name = 'الخميس'
            # elif today == 'Friday':
            #     day_name = 'الجمعه'
            #
            # self.cur.execute('''INSERT INTO financial (operation, amount, date, text, day) VALUES (%s,%s,%s,%s,%s)''',
            #                  ('مقبوضات', paid, date, 'اشتراك تلميذ', day_name))
        else:
            self.statusBar().showMessage('Not Found!')

        # Commit Changes
        self.db.commit()

        self.show_operations()
        self.show_all_operations()
        self.show_all_students()

    def daily_sign(self):
        self.cur = self.db.cursor()

        # Getting Info from UI
        student_code = self.lineEdit.text()
        date = datetime.date.today()
        # Fetch Data from Database

        self.cur.execute('''SELECT name FROM students WHERE id=%s''', [student_code])
        data = self.cur.fetchone()
        if data:
            name = data[0]
            self.cur.execute('''SELECT name from daily WHERE date =%s AND name=%s''', (date, name))
            data = self.cur.fetchone()
            if data:
                print(data)
                pass

            else:
                self.cur.execute('''INSERT INTO daily (name,date) VALUES (%s,%s)''', (name, date))

                row_pos = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_pos)
                self.tableWidget.setItem(row_pos, 0, QTableWidgetItem(str(name)))
                self.tableWidget.setItem(row_pos, 1, QTableWidgetItem(str(datetime.datetime.now())))
                self.absent -= 1
                self.come += 1
                self.lcdNumber_2.display(int(self.absent))
                self.lcdNumber.display(int(self.come))
                self.statusBar().showMessage('تم تسجيل الحضور')

                self.cur.execute('''SELECT subscription_type,days_number FROM students WHERE id=%s''', [student_code])
                data = self.cur.fetchone()
                if data:
                    if data[0] == '1/2 شهر':
                        remaining = int(data[1]) - 1
                        self.cur.execute('''UPDATE students SET days_number=%s WHERE id=%s''',
                                         (remaining, student_code))
                self.db.commit()
                self.deadline_notification()
                self.all_daily_login()

        else:
            self.statusBar().showMessage('Not Found!')

    def questions(self):
        self.cur = self.db.cursor()

        # Getting info from UI
        name = self.lineEdit_75.text()
        phone = self.lineEdit_18.text()
        question = self.lineEdit_29.text()
        date = datetime.datetime.now()
        datetime.datetime.now()
        self.cur.execute('''INSERT INTO questions (name, phone, question, date) VALUES (%s,%s,%s,%s)''',
                         (name, phone, question, date))
        self.db.commit()

        self.show_questions()
        # Clear input fields
        self.lineEdit_75.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_29.setText("")

    def show_questions(self):
        self.cur = self.db.cursor()

        # Fetching Data from Database

        self.cur.execute('''SELECT * FROM questions ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_16.setRowCount(0)
            self.tableWidget_16.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form[1:]):
                    self.tableWidget_16.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.tableWidget_16.rowCount()
                self.tableWidget_16.insertRow(row_pos)

    # *******************************
    #   Notifications
    # *******************************
    def deadline_notification(self):
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name,ending_date FROM students''')
        data = self.cur.fetchall()
        today = datetime.date.today()
        self.tableWidget_8.setRowCount(0)
        if data:
            for i in data:
                name = i[0]
                end_date = i[1]
                remaining_days = int((end_date - today).days)
                if remaining_days < 4:
                    row_pos = self.tableWidget_8.rowCount()
                    self.tableWidget_8.insertRow(row_pos)
                    self.tableWidget_8.setItem(row_pos, 0, QTableWidgetItem(str(name)))
                    self.tableWidget_8.setItem(row_pos, 1, QTableWidgetItem(str(end_date)))
                    self.tableWidget_8.setItem(row_pos, 2, QTableWidgetItem(str(remaining_days)))
        self.cur.execute('''SELECT days_number,name FROM students WHERE subscription_type=%s ''', ['1/2 شهر'])
        data = self.cur.fetchall()
        if data:
            for i in data:
                days = int(i[0])
                st_name = i[1]
                if days < 1:
                    row_pos = self.tableWidget_8.rowCount()
                    self.tableWidget_8.insertRow(row_pos)
                    self.tableWidget_8.setItem(row_pos, 0, QTableWidgetItem(str(st_name)))
                    self.tableWidget_8.setItem(row_pos, 1, QTableWidgetItem('اليوم'))
                    self.tableWidget_8.setItem(row_pos, 2, QTableWidgetItem(str(days)))

    # *******************************
    #   Students
    # *******************************

    def new_student(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        name = self.lineEdit_4.text()
        birthday = self.lineEdit_5.text()
        address = self.lineEdit_7.text()
        phone = self.lineEdit_6.text()
        mother_name = self.lineEdit_11.text()
        mother_id = self.lineEdit_8.text()
        mother_phone = self.lineEdit_9.text()
        mother_job = self.lineEdit_10.text()
        father_name = self.lineEdit_12.text()
        father_id = self.lineEdit_13.text()
        father_phone = self.lineEdit_14.text()
        father_job = self.lineEdit_15.text()
        authorized_name = self.lineEdit_17.text()
        authorized_phone = self.lineEdit_20.text()
        emergency = self.lineEdit_16.text()
        emergency_relationship = self.lineEdit_19.text()
        subscription_type = self.comboBox_10.currentText()
        starting_date = self.dateEdit.date().toPyDate()
        e_or_f = self.comboBox_3.currentText()
        added_time = datetime.datetime.now()
        if len(self.lineEdit_53.text()) > 0:
            paid_money = int(self.lineEdit_53.text())
        else:
            paid_money = int(0)

        type_idx = self.comboBox_10.currentIndex()
        duration = 0
        if type_idx == 0:
            duration = 30
        elif type_idx == 1:
            duration = 30
        elif type_idx == 2:
            duration = 60
        elif type_idx == 3:
            duration = 90
        elif type_idx == 4:
            duration = 180
        elif type_idx == 5:
            duration = 365

        ending_date = starting_date + datetime.timedelta(days=duration)

        # Bus
        if self.checkBox_49.isChecked():
            bus = "Yes"
        else:
            bus = "No"

        # Shirt
        if self.checkBox_46.isChecked():
            shirt = "Yes"
        else:
            shirt = "No"

        # sweet shirt
        if self.checkBox_51.isChecked():
            sweet = "Yes"
        else:
            sweet = "No"

        # pants
        if self.checkBox_52.isChecked():
            pants = "Yes"
        else:
            pants = "No"

        # study books
        if self.checkBox_54.isChecked():
            books = "Yes"
        else:
            books = "No"

        # Day_by_day
        if self.checkBox_53.isChecked():
            day_by_day = "Yes"
        else:
            day_by_day = "No"
        # Application
        if self.checkBox_55.isChecked():
            app = "Yes"
        else:
            app = "No"

        # Inserting info into the DB
        warning = QMessageBox.warning(self, 'Warning', 'اضافه تلميذ جديد؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''
               INSERT INTO students (name,birthday,address,phone,mother_name,mother_id,mother_number,mother_job,
               father_name,father_id,father_number,father_job,authorized_person,authorized_number,emergency,
               emergency_relationship,starting_date,paid_money,subscription_type,e_or_f,added_time,ending_date,
               bus,shirt,sweet,pants,study,day_by_day,application) 
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', (
                name, birthday, address, phone, mother_name, mother_id, mother_phone, mother_job,
                father_name, father_id, father_phone, father_job, authorized_name, authorized_phone,
                emergency, emergency_relationship, starting_date, int(paid_money), subscription_type, e_or_f,
                added_time, ending_date, bus, shirt, sweet, pants, books, day_by_day, app))
            self.cur.execute('''INSERT INTO students days_number=13''')
            # Financial Operation
            # date = datetime.datetime.now()
            # today = datetime.datetime.today().strftime('%A')
            # day_name = ''
            # if today == 'Saturday':
            #     day_name = 'السبت'
            # elif today == 'ٍSunday':
            #     day_name = 'الاحد'
            # elif today == 'Monday':
            #     day_name = 'الاثنين'
            # elif today == 'Tuesday':
            #     day_name = 'الثلاثاء'
            # elif today == 'Wednesday':
            #     day_name = 'الاربعاء'
            # elif today == 'Thursday':
            #     day_name = 'الخميس'
            # elif today == 'Friday':
            #     day_name = 'الجمعه'
            #
            # self.cur.execute('''INSERT INTO financial (operation, amount, date, text, day) VALUES (%s,%s,%s,%s,%s)''',
            #                  ('مقبوضات', paid_money, date, 'اشتراك تلميذ', day_name))
            # Commit Changes
            self.db.commit()
            # Show the student ID
            self.cur.execute('''SELECT MAX(id) FROM students''')
            student_id = self.cur.fetchone()[0]
            self.statusBar().showMessage(f"ID :{student_id}")
            # Clear input lines
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_8.setText('')
            self.lineEdit_9.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_12.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_17.setText('')
            self.lineEdit_20.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_19.setText('')
            self.lineEdit_53.setText('')

            self.checkBox_46.setChecked(False)
            self.checkBox_49.setChecked(False)
            self.checkBox_51.setChecked(False)
            self.checkBox_52.setChecked(False)
            self.checkBox_53.setChecked(False)
            self.checkBox_54.setChecked(False)
            self.checkBox_55.setChecked(False)

        self.show_operations()
        self.show_all_operations()
        self.show_all_students()

    def show_all_students(self):
        # getting info from Database
        self.cur = self.db.cursor()
        self.cur.execute(
            '''SELECT id,name,birthday,added_time,starting_date,ending_date,subscription_type,books,uniform,monthly_pay,paid_money 
            FROM students''')
        data = self.cur.fetchall()

        # Displaying Data in all students Table
        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_pos)

    def student_search(self):
        self.cur = self.db.cursor()
        student_id = self.lineEdit_55.text()
        # Fetching Data from Database
        self.cur.execute('''SELECT * FROM students WHERE id = %s''', [student_id])
        data = self.cur.fetchone()

        # Displaying Data in all student Table
        if data:
            row = 0
            for i in data[1:]:
                self.tableWidget_3.setItem(row, 0, QTableWidgetItem(str(i)))
                row += 1

    def search_student_for_edit(self):
        self.cur = self.db.cursor()
        student_id = self.lineEdit_38.text()
        # Fetching Data from Database
        self.cur.execute('''SELECT * FROM students WHERE id = %s''', [student_id])
        data = self.cur.fetchone()
        # Displaying Data
        if data:
            self.lineEdit_32.setText(data[1])
            self.lineEdit_25.setText(data[2])
            self.lineEdit_37.setText(data[3])
            self.lineEdit_36.setText(data[4])
            self.lineEdit_23.setText(data[5])
            self.lineEdit_33.setText(data[6])
            self.lineEdit_34.setText(data[7])
            self.lineEdit_26.setText(data[8])
            self.lineEdit_31.setText(data[9])
            self.lineEdit_35.setText(data[10])
            self.lineEdit_27.setText(data[11])
            self.lineEdit_22.setText(data[12])
            self.lineEdit_21.setText(data[13])
            self.lineEdit_30.setText(data[14])
            self.lineEdit_24.setText(data[15])
            self.lineEdit_28.setText(data[16])
            self.dateEdit_2.setDate(data[17])

            # E or F
            if data[19] == 'English':
                self.comboBox_5.setCurrentIndex(0)
            elif data[19] == 'French':
                self.comboBox_5.setCurrentIndex(1)

            # Subscription Type
            if data[18] == '1 شهر':
                self.comboBox_11.setCurrentIndex(1)
            elif data[18] == '1/2 اشهر':
                self.comboBox_11.setCurrentIndex(0)
            elif data[18] == '2 اشهر':
                self.comboBox_11.setCurrentIndex(2)
            elif data[18] == '3 اشهر':
                self.comboBox_11.setCurrentIndex(3)
            elif data[18] == '6 اشهر':
                self.comboBox_11.setCurrentIndex(4)
            elif data[18] == 'سنه':
                self.comboBox_11.setCurrentIndex(5)

            # bus
            if data[31] == 'Yes':
                self.checkBox_50.setChecked(True)
            elif data[31] == 'No':
                self.checkBox_50.setChecked(False)
            # shirt
            if data[25] == 'Yes':
                self.checkBox_61.setChecked(True)
            elif data[25] == 'No':
                self.checkBox_61.setChecked(False)
            # sweet shirt
            if data[26] == 'Yes':
                self.checkBox_57.setChecked(True)
            elif data[26] == 'No':
                self.checkBox_57.setChecked(False)
            # pants
            if data[27] == 'Yes':
                self.checkBox_60.setChecked(True)
            elif data[27] == 'No':
                self.checkBox_60.setChecked(False)
            # books
            if data[28] == 'Yes':
                self.checkBox_58.setChecked(True)
            elif data[28] == 'No':
                self.checkBox_58.setChecked(False)
            # Day_by_day
            if data[29] == 'Yes':
                self.checkBox_56.setChecked(True)
            elif data[29] == 'No':
                self.checkBox_56.setChecked(False)
            # Application
            if data[30] == 'Yes':
                self.checkBox_59.setChecked(True)
            elif data[30] == 'No':
                self.checkBox_59.setChecked(False)
        else:
            self.statusBar().showMessage('Not Found!')
            # Clear input lines
            self.lineEdit_32.setText('')
            self.lineEdit_25.setText('')
            self.lineEdit_37.setText('')
            self.lineEdit_36.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_33.setText('')
            self.lineEdit_34.setText('')
            self.lineEdit_26.setText('')
            self.lineEdit_31.setText('')
            self.lineEdit_35.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_22.setText('')
            self.lineEdit_21.setText('')
            self.lineEdit_30.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_28.setText('')
            self.checkBox_50.setChecked(False)
            self.checkBox_61.setChecked(False)
            self.checkBox_60.setChecked(False)
            self.checkBox_59.setChecked(False)
            self.checkBox_58.setChecked(False)
            self.checkBox_57.setChecked(False)
            self.checkBox_56.setChecked(False)

    def delete_student(self):
        id = self.lineEdit_55.text()
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM students WHERE id=%s''', [id])
        data = self.cur.fetchone()
        if data:
            warning = QMessageBox.warning(self, 'Warning', f'حذف التلميذ {data[0]}؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM students WHERE id=%s''', [id])
                self.statusBar().showMessage('تم الحذف')
                self.lineEdit_84.setText('')
                self.show_all_employees()
        else:
            self.statusBar().showMessage('لا يوجد')

    def edit_student(self):
        self.cur = self.db.cursor()
        student_id = self.lineEdit_38.text()

        # Getting the Updated info from the UI
        name = self.lineEdit_32.text()
        birthday = self.lineEdit_25.text()
        address = self.lineEdit_37.text()
        phone = self.lineEdit_36.text()
        mother_name = self.lineEdit_23.text()
        mother_id = self.lineEdit_33.text()
        mother_phone = self.lineEdit_34.text()
        mother_job = self.lineEdit_26.text()
        father_name = self.lineEdit_31.text()
        father_id = self.lineEdit_35.text()
        father_phone = self.lineEdit_27.text()
        father_job = self.lineEdit_22.text()
        authorized_name = self.lineEdit_21.text()
        authorized_phone = self.lineEdit_30.text()
        emergency = self.lineEdit_24.text()
        emergency_relationship = self.lineEdit_28.text()
        subscription_type = self.comboBox_11.currentText()
        e_or_f = self.comboBox_5.currentText()
        starting_date = self.dateEdit_2.date().toPyDate()
        type_idx = self.comboBox_11.currentIndex()

        duration = 0
        if type_idx == 0:
            duration = 30
        elif type_idx == 1:
            duration = 30
        elif type_idx == 2:
            duration = 60
        elif type_idx == 3:
            duration = 90
        elif type_idx == 4:
            duration = 180
        elif type_idx == 5:
            duration = 365

        ending_date = starting_date + datetime.timedelta(days=duration)

        # Bus
        if self.checkBox_50.isChecked():
            bus = "Yes"
        else:
            bus = "No"

        # Shirt
        if self.checkBox_61.isChecked():
            shirt = "Yes"
        else:
            shirt = "No"

        # sweet shirt
        if self.checkBox_57.isChecked():
            sweet = "Yes"
        else:
            sweet = "No"

        # pants
        if self.checkBox_60.isChecked():
            pants = "Yes"
        else:
            pants = "No"

        # study books
        if self.checkBox_58.isChecked():
            books = "Yes"
        else:
            books = "No"

        # Day_by_day
        if self.checkBox_56.isChecked():
            day_by_day = "Yes"
        else:
            day_by_day = "No"
        # Application
        if self.checkBox_59.isChecked():
            app = "Yes"
        else:
            app = "No"

        # Inserting info into the DB
        warning = QMessageBox.warning(self, 'Warning', 'تعديل بيانات التلميذ؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''
                UPDATE students SET name=%s,birthday=%s,address=%s,phone=%s,mother_name=%s,mother_id=%s,
                mother_number=%s,mother_job=%s,father_name=%s,father_id=%s,father_number=%s,father_job=%s,
                authorized_person=%s,authorized_number=%s,emergency=%s,
                emergency_relationship=%s,starting_date=%s,subscription_type=%s,e_or_f=%s,ending_date=%s
                ,bus=%s,study=%s,application=%s,day_by_day=%s,pants=%s,sweet=%s,shirt=%s
                WHERE id=%s
            ''', (name, birthday, address, phone, mother_name, mother_id, mother_phone, mother_job,
                  father_name, father_id, father_phone, father_job, authorized_name, authorized_phone,
                  emergency, emergency_relationship, starting_date, subscription_type, e_or_f,
                  ending_date, bus, books, app, day_by_day, pants, sweet, shirt, student_id))

            # Commit Changes
            self.db.commit()

            # show a message
            self.statusBar().showMessage(f"Information Updated")

            # Clear input lines
            self.lineEdit_32.setText('')
            self.lineEdit_25.setText('')
            self.lineEdit_37.setText('')
            self.lineEdit_36.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_33.setText('')
            self.lineEdit_34.setText('')
            self.lineEdit_26.setText('')
            self.lineEdit_31.setText('')
            self.lineEdit_35.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_22.setText('')
            self.lineEdit_21.setText('')
            self.lineEdit_30.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_28.setText('')
            # self.checkBox_48.setChecked(False)
            # self.checkBox_47.setChecked(False)

        self.show_all_students()

    def all_daily_login(self):
        self.cur.execute('''SELECT name,date FROM daily ORDER BY date ASC''')
        info = self.cur.fetchall()

        if info:
            x = str(info[0][1])
            dt = [str(info[0][1])]

            self.tableWidget_10.setColumnCount(0)
            self.tableWidget_10.setRowCount(0)
            col_pos = self.tableWidget_10.columnCount()
            row_pos = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertColumn(0)
            self.tableWidget_10.insertRow(0)
            for i in info:
                name = i[0]
                date = str(i[1])
                if self.tableWidget_10.rowCount() <= row_pos:
                    self.tableWidget_10.insertRow(row_pos)

                if date == x:
                    self.tableWidget_10.setItem(row_pos, col_pos, QTableWidgetItem(name))
                else:
                    x = date
                    dt.append(date)
                    row_pos = 0
                    col_pos = self.tableWidget_10.columnCount()
                    self.tableWidget_10.insertColumn(col_pos)
                    self.tableWidget_10.setItem(row_pos, col_pos, QTableWidgetItem(name))
                row_pos += 1
            self.tableWidget_10.setHorizontalHeaderLabels(dt)

    # *******************************
    #   Trainees
    # *******************************

    def new_trainee(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        name = self.lineEdit_70.text()
        birthday = self.lineEdit_71.text()
        address = self.lineEdit_63.text()
        phone = self.lineEdit_69.text()
        mother_name = self.lineEdit_73.text()
        mother_id = self.lineEdit_60.text()
        mother_phone = self.lineEdit_68.text()
        mother_job = self.lineEdit_59.text()
        father_name = self.lineEdit_67.text()
        father_id = self.lineEdit_62.text()
        father_phone = self.lineEdit_57.text()
        father_job = self.lineEdit_72.text()
        authorized_name = self.lineEdit_61.text()
        authorized_phone = self.lineEdit_64.text()
        emergency = self.lineEdit_58.text()
        emergency_relationship = self.lineEdit_65.text()
        subscription_type = self.comboBox_12.currentText()
        added_time = datetime.datetime.now()
        starting_date = self.dateEdit_3.date().toPyDate()
        if len(self.lineEdit_74.text()) > 0:
            paid_money = int(self.lineEdit_74.text())
        else:
            paid_money = int(0)

        type_idx = self.comboBox_12.currentIndex()

        duration = 0
        if type_idx == 0:
            duration = 30
        elif type_idx == 1:
            duration = 30
        elif type_idx == 2:
            duration = 60
        elif type_idx == 3:
            duration = 90
        elif type_idx == 4:
            duration = 180
        elif type_idx == 5:
            duration = 365

        ending_date = starting_date + datetime.timedelta(days=duration)

        #  '''***********'''
        #   '' الاشتراكات ''
        #  '''***********'''

        # Inserting info into the DB
        warning = QMessageBox.warning(self, 'Warning', 'اضافه متدرب جديد؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''
                INSERT INTO trainees (name,birthday,address,phone,mother_name,mother_id,mother_number,mother_job,
                father_name,father_id,father_number,father_job,authorized_person,authorized_number,emergency,
                emergency_relationship,starting_date,paid_money,subscription_type,ending_date) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (name, birthday, address, phone, mother_name, mother_id, mother_phone, mother_job,
                  father_name, father_id, father_phone, father_job, authorized_name, authorized_phone,
                  emergency, emergency_relationship, starting_date, int(paid_money), subscription_type,
                  ending_date))

            # ---------
            # Activity Check
            # ---------

            # Karate
            if self.checkBox_18.isChecked():
                self.cur.execute('''INSERT INTO karate (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # GYM
            if self.checkBox_19.isChecked():
                self.cur.execute('''INSERT INTO gym (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # Zumba
            if self.checkBox_17.isChecked():
                self.cur.execute('''INSERT INTO zumba (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # Ballet
            if self.checkBox_31.isChecked():
                self.cur.execute('''INSERT INTO ballet (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # Fitness
            if self.checkBox_32.isChecked():
                self.cur.execute('''INSERT INTO fitness (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # Drawing
            if self.checkBox_39.isChecked():
                self.cur.execute('''INSERT INTO drawing (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # music
            if self.checkBox_20.isChecked():
                self.cur.execute('''INSERT INTO music (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # Etiquette
            if self.checkBox_41.isChecked():
                self.cur.execute('''INSERT INTO etiquette (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))
            # Cooking
            if self.checkBox_40.isChecked():
                self.cur.execute('''INSERT INTO cooking (trainee_name,trainee_age,added_time,starting_date,ending_date,
                        subscription_type,money) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                 (name, birthday, added_time, starting_date, ending_date, subscription_type,
                                  paid_money))

            # date = datetime.datetime.now()
            # today = datetime.datetime.today().strftime('%A')
            # day_name = ''
            # if today == 'Saturday':
            #     day_name = 'السبت'
            # elif today == 'ٍSunday':
            #     day_name = 'الاحد'
            # elif today == 'Monday':
            #     day_name = 'الاثنين'
            # elif today == 'Tuesday':
            #     day_name = 'الثلاثاء'
            # elif today == 'Wednesday':
            #     day_name = 'الاربعاء'
            # elif today == 'Thursday':
            #     day_name = 'الخميس'
            # elif today == 'Friday':
            #     day_name = 'الجمعه'
            #
            # self.cur.execute('''INSERT INTO financial (operation, amount, date, text, day) VALUES (%s,%s,%s,%s,%s)''',
            #                  ('مقبوضات', paid_money, date, 'اشتراك تلميذ', day_name))
            # Commit Changes
            self.db.commit()
            self.statusBar().showMessage('تم اضافه متدرب جديد')
            self.lineEdit_70.setText('')
            self.lineEdit_71.setText('')
            self.lineEdit_63.setText('')
            self.lineEdit_69.setText('')
            self.lineEdit_73.setText('')
            self.lineEdit_60.setText('')
            self.lineEdit_68.setText('')
            self.lineEdit_59.setText('')
            self.lineEdit_67.setText('')
            self.lineEdit_62.setText('')
            self.lineEdit_57.setText('')
            self.lineEdit_72.setText('')
            self.lineEdit_61.setText('')
            self.lineEdit_64.setText('')
            self.lineEdit_58.setText('')
            self.lineEdit_65.setText('')
            self.comboBox_12.setCurrentIndex(0)
            self.dateEdit_3.setDateTime(QDateTime.currentDateTime())
            self.lineEdit_74.setText('')
            self.checkBox_18.setChecked(False)
            self.checkBox_19.setChecked(False)
            self.checkBox_17.setChecked(False)
            self.checkBox_31.setChecked(False)
            self.checkBox_32.setChecked(False)
            self.checkBox_39.setChecked(False)
            self.checkBox_20.setChecked(False)
            self.checkBox_41.setChecked(False)
            self.checkBox_40.setChecked(False)

        self.show_operations()
        self.show_all_operations()

    def trainees_search(self):
        self.cur = self.db.cursor()

        training_idx = self.comboBox_4.currentIndex()
        training = self.comboBox_4.currentText()

        if training_idx == 0:
            name = 'karate'
        elif training_idx == 1:
            name = 'zumba'
        elif training_idx == 2:
            name = 'ballet'
        elif training_idx == 3:
            name = 'gym'
        elif training_idx == 4:
            name = 'fitness'
        elif training_idx == 5:
            name = 'drawing'
        elif training_idx == 6:
            name = 'music'
        elif training_idx == 7:
            name = 'etiquette'
        elif training_idx == 8:
            name = 'cooking'

        # Fetching Trainees from Database
        self.cur.execute(
            f'''SELECT trainee_name,trainee_age,added_time,starting_date,ending_date,subscription_type,money
             FROM {name} ''')
        data = self.cur.fetchall()

        # Displaying Data
        if data:
            self.tableWidget_11.setRowCount(0)
            self.tableWidget_11.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_11.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.tableWidget_11.rowCount()
                self.tableWidget_11.insertRow(row_pos)
        else:
            self.tableWidget_11.setRowCount(0)

        # Trainees Number
        number = len(data)
        self.lineEdit_138.setText(str(number))

        # Getting The Coach Name
        self.cur.execute('''SELECT name FROM coaches WHERE training = %s''', [training])
        data = self.cur.fetchone()
        if data:
            self.lineEdit_99.setText(str(data[0]))
        else:
            self.lineEdit_99.setText('')

    def search_trainee_for_edit(self):
        self.cur = self.db.cursor()
        trainee_name = self.lineEdit_87.text()
        # Fetching Data from Database
        self.cur.execute('''SELECT * FROM trainees WHERE name = %s''', [trainee_name])
        data = self.cur.fetchone()
        # Displaying Data
        if data:
            self.lineEdit_133.setText(data[1])
            self.lineEdit_80.setText(data[2])
            self.lineEdit_92.setText(data[3])
            self.lineEdit_91.setText(data[4])
            self.lineEdit_78.setText(data[5])
            self.lineEdit_88.setText(data[6])
            self.lineEdit_89.setText(data[7])
            self.lineEdit_81.setText(data[8])
            self.lineEdit_86.setText(data[9])
            self.lineEdit_90.setText(data[10])
            self.lineEdit_82.setText(data[11])
            self.lineEdit_77.setText(data[12])
            self.lineEdit_76.setText(data[13])
            self.lineEdit_85.setText(data[14])
            self.lineEdit_79.setText(data[15])
            self.lineEdit_83.setText(data[16])
            self.dateEdit_4.setDate(data[17])

            if data[19] == '1 شهر':
                self.comboBox_15.setCurrentIndex(1)
            elif data[19] == '1/2 اشهر':
                self.comboBox_15.setCurrentIndex(0)
            elif data[19] == '2 اشهر':
                self.comboBox_15.setCurrentIndex(2)
            elif data[19] == '3 اشهر':
                self.comboBox_15.setCurrentIndex(3)
            elif data[19] == '6 اشهر':
                self.comboBox_15.setCurrentIndex(4)
            elif data[19] == 'سنه':
                self.comboBox_15.setCurrentIndex(5)

            # ---------
            # Activity Check
            # ---------

            # Karate
            self.cur.execute('''SELECT trainee_name FROM karate WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_35.setChecked(True)

            # gym
            self.cur.execute('''SELECT trainee_name FROM gym WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_37.setChecked(True)

            # zumba
            self.cur.execute('''SELECT trainee_name FROM zumba WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_36.setChecked(True)

            # ballet
            self.cur.execute('''SELECT trainee_name FROM ballet WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_38.setChecked(True)

            # fitness
            self.cur.execute('''SELECT trainee_name FROM fitness WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_34.setChecked(True)

            # drawing
            self.cur.execute('''SELECT trainee_name FROM drawing WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_42.setChecked(True)

            # music
            self.cur.execute('''SELECT trainee_name FROM music WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_33.setChecked(True)

            # etiquette
            self.cur.execute('''SELECT trainee_name FROM etiquette WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_44.setChecked(True)

            # cooking
            self.cur.execute('''SELECT trainee_name FROM cooking WHERE trainee_name=%s''', [trainee_name])
            data = self.cur.fetchall()
            if data:
                for name in data:
                    if name[0] == trainee_name:
                        self.checkBox_43.setChecked(True)
        else:
            self.statusBar().showMessage('Not Found!')

    def edit_trainee(self):
        self.cur = self.db.cursor()
        trainee_name = self.lineEdit_87.text()
        name = self.lineEdit_133.text()
        birthday = self.lineEdit_80.text()
        address = self.lineEdit_92.text()
        phone = self.lineEdit_91.text()
        mother_name = self.lineEdit_78.text()
        mother_id = self.lineEdit_88.text()
        mother_phone = self.lineEdit_89.text()
        mother_job = self.lineEdit_81.text()
        father_name = self.lineEdit_86.text()
        father_id = self.lineEdit_90.text()
        father_phone = self.lineEdit_82.text()
        father_job = self.lineEdit_77.text()
        authorized_name = self.lineEdit_76.text()
        authorized_phone = self.lineEdit_85.text()
        emergency = self.lineEdit_79.text()
        emergency_relationship = self.lineEdit_83.text()
        subscription_type = self.comboBox_15.currentText()
        starting_date = self.dateEdit_4.date().toPyDate()

        type_idx = self.comboBox_15.currentIndex()

        duration = 0
        if type_idx == 0:
            duration = 30
        elif type_idx == 1:
            duration = 30
        elif type_idx == 2:
            duration = 60
        elif type_idx == 3:
            duration = 90
        elif type_idx == 4:
            duration = 180
        elif type_idx == 5:
            duration = 365

        ending_date = starting_date + datetime.timedelta(days=duration)

        #  '''***********'''
        #   '' الاشتراكات ''
        #  '''***********'''

        # Inserting info into the DB
        warning = QMessageBox.warning(self, 'Warning', 'تعديل البيانات؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:

            # ---------
            # Activity Check
            # ---------

            # Karate
            one_at_least = False
            if self.checkBox_35.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM karate WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE karate SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO karate (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM karate WHERE trainee_name=%s''', [name])

            # GYM
            if self.checkBox_37.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM gym WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE gym SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO gym (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM gym WHERE trainee_name=%s''', [name])

            # Zumba
            if self.checkBox_36.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM zumba WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE zumba SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO zumba (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM zumba WHERE trainee_name=%s''', [name])

            # Ballet
            if self.checkBox_38.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM ballet WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE ballet SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO ballet (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM ballet WHERE trainee_name=%s''', [name])

            # Fitness
            if self.checkBox_34.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM fitness WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE fitness SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO fitness (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM fitness WHERE trainee_name=%s''', [name])

            # Drawing
            if self.checkBox_42.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM drawing WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE drawing SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO drawing (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM drawing WHERE trainee_name=%s''', [name])

            # music
            if self.checkBox_33.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM music WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE music SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO music (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM music WHERE trainee_name=%s''', [name])

            # Etiquette
            if self.checkBox_44.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM etiquette WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE etiquette SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO etiquette (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM etiquette WHERE trainee_name=%s''', [name])

            # Cooking
            if self.checkBox_43.isChecked():
                one_at_least = True
                self.cur.execute('''SELECT trainee_name FROM cooking WHERE trainee_name=%s''', [name])
                data = self.cur.fetchone()
                if data:
                    self.cur.execute('''UPDATE cooking SET trainee_name=%s,trainee_age=%s,starting_date=%s,ending_date=%s,
                                        subscription_type=%s WHERE trainee_name=%s''',
                                     (name, birthday, starting_date, ending_date, subscription_type, name))
                else:
                    self.cur.execute('''INSERT INTO cooking (trainee_name,trainee_age,starting_date,ending_date,
                                subscription_type) VALUES (%s,%s,%s,%s,%s)''',
                                     (name, birthday, starting_date, ending_date, subscription_type))
            else:
                self.cur.execute('''DELETE FROM cooking WHERE trainee_name=%s''', [name])

            if one_at_least:
                self.cur.execute('''UPDATE trainees SET name=%s,birthday=%s,address=%s,phone=%s,mother_name=%s,mother_id=%s,
                mother_number=%s,mother_job=%s,father_name=%s,father_id=%s,father_number=%s,father_job=%s,
                authorized_person=%s,authorized_number=%s,emergency=%s,emergency_relationship=%s,starting_date=%s,
                subscription_type=%s,ending_date=%s
                    WHERE name=%s
                        ''', (name, birthday, address, phone, mother_name, mother_id, mother_phone, mother_job,
                              father_name, father_id, father_phone, father_job, authorized_name, authorized_phone,
                              emergency, emergency_relationship, starting_date, subscription_type,
                              ending_date, trainee_name))

            # Commit Changes
            self.db.commit()
            self.statusBar().showMessage('تم تعديل البيانات')

    def delete_trainee(self):
        name = self.lineEdit_87.text()
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT name FROM trainees WHERE name=%s''', [name])
        data = self.cur.fetchone()
        if data:
            warning = QMessageBox.warning(self, 'Warning', f'حذف {data[0]}?', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM trainees WHERE name=%s''', [name])
                self.cur.execute('''DELETE FROM ballet WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM cooking WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM drawing WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM etiquette WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM fitness WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM gym WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM karate WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM music WHERE trainee_name=%s''', [name])
                self.cur.execute('''DELETE FROM zumba WHERE trainee_name=%s''', [name])
        else:
            self.statusBar().showMessage('لا يوجد')

    # *******************************
    #   Employees
    # *******************************

    def new_employee(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        name = self.lineEdit_41.text()
        address = self.lineEdit_39.text()
        phone = self.lineEdit_40.text()
        national_id = self.lineEdit_43.text()
        job = self.comboBox.currentText()
        added_time = datetime.datetime.now()
        if len(self.lineEdit_44.text()) > 0:
            salary = int(self.lineEdit_44.text())
        else:
            salary = int(0)

        # Inserting info into the DB
        self.cur.execute(''' SELECT name FROM employees WHERE name=%s''', [name])
        data = self.cur.fetchone()
        if data:
            warning = QMessageBox.warning(self, 'Warning', 'تعديل بيانات الموظف ؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute(
                    '''UPDATE employees SET name=%s,address=%s,phone=%s,national_id=%s,job_salary=%s WHERE =%s''',
                    (name, address, phone, national_id, salary, name))

        else:
            warning = QMessageBox.warning(self, 'Warning', 'اضافه موظف جديد؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''
                           INSERT INTO employees (name,address,phone,national_id,job,salary,added_time) 
                           VALUES (%s,%s,%s,%s,%s,%s,%s)
                           ''', (name, address, phone, national_id, job, int(salary), added_time))
        # Commit Changes
        self.db.commit()
        self.show_all_employees()
        self.statusBar().showMessage('تم')

    def show_all_employees(self):
        # getting info from Database
        self.cur = self.db.cursor()
        self.cur.execute(
            '''SELECT name,address,phone,national_id,job,salary,added_time
            FROM employees''')
        data = self.cur.fetchall()

        # Displaying Data in all students Table
        if data:
            self.tableWidget_6.setRowCount(0)
            self.tableWidget_6.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_6.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(row_pos)

        # ------------------------

    def delete_employee(self):
        self.cur = self.db.cursor()
        phone = self.lineEdit_84.text()
        self.cur.execute('''SELECT name FROM employees WHERE phone=%s''', [phone])
        data = self.cur.fetchone()
        if data:
            warning = QMessageBox.warning(self, 'Warning', f'حذف الموظف {data[0]}؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM employees WHERE phone=%s''', [phone])
                self.statusBar().showMessage('تم الحذف')
                self.lineEdit_84.setText('')
                self.show_all_employees()
        else:
            self.statusBar().showMessage('لا يوجد')

    def new_coach(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        name = self.lineEdit_95.text()
        address = self.lineEdit_96.text()
        phone = self.lineEdit_56.text()
        national_id = self.lineEdit_94.text()
        job = self.comboBox_7.currentText()
        added_time = datetime.datetime.now()
        if len(self.lineEdit_93.text()) > 0:
            salary = int(self.lineEdit_93.text())
        else:
            salary = int(0)

        # Inserting info into the DB
        self.cur.execute('''SELECT name FROM coaches WHERE training=%s''', [job])
        data = self.cur.fetchone()
        if data:
            warning = QMessageBox.warning(self, 'Warning', f'حذف المدرب {data[0]}؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM coaches WHERE training=%s''', [job])
                self.cur.execute('''DELETE FROM employees WHERE job=%s''', [job])

        warning = QMessageBox.warning(self, 'Warning', 'اضافه مدرب جديد؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''
                   INSERT INTO coaches (name,address,phone,national_id,training,subscription_money)
                   VALUES (%s,%s,%s,%s,%s,%s)
               ''', (name, address, phone, national_id, job, int(salary)))
            self.cur.execute('''
                   INSERT INTO employees (name,address,phone,national_id,job,salary,added_time) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s)
               ''', (name, address, phone, national_id, job, int(salary), added_time))
            # Commit Changes
            self.db.commit()
        self.show_all_employees()

    def training_search(self):
        self.cur = self.db.cursor()
        training_idx = self.comboBox_6.currentIndex()
        training = self.comboBox_6.currentText()

        if training_idx == 0:
            name = 'karate'
        elif training_idx == 1:
            name = 'zumba'
        elif training_idx == 2:
            name = 'ballet'
        elif training_idx == 3:
            name = 'gym'
        elif training_idx == 4:
            name = 'fitness'
        elif training_idx == 5:
            name = 'drawing'
        elif training_idx == 6:
            name = 'music'
        elif training_idx == 7:
            name = 'etiquette'
        elif training_idx == 8:
            name = 'cooking'

        # Fetching Trainees from Database
        self.cur.execute(
            f'''SELECT trainee_name,trainee_age,added_time,starting_date,ending_date,subscription_type,money
             FROM {name} ''')
        data = self.cur.fetchall()
        # Displaying Data

        # Trainees Number
        number = len(data)
        self.lineEdit_141.setText(str(number))

        # Getting The Coach Name
        self.cur.execute('''SELECT name,subscription_money FROM coaches WHERE training = %s''', [training])
        data = self.cur.fetchone()
        if data:
            self.lineEdit_140.setText(str(data[0]))
            self.lineEdit_142.setText(str(data[1]))

            total = number * data[1]
            self.lineEdit_143.setText(str(total))

            coach_percentage = total * 0.4
            self.lineEdit_144.setText(str(coach_percentage))
        else:
            self.lineEdit_140.setText('')
            self.lineEdit_142.setText('')
            self.lineEdit_143.setText('')
            self.lineEdit_144.setText('')

        # Total

    # *******************************
    #   Financial
    # *******************************

    def add_operation(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        # money = self.lineEdit_45.text()
        txt = self.lineEdit_46.text()
        operation = self.comboBox_2.currentText()

        if len(self.lineEdit_45.text()) > 0:
            money = int(self.lineEdit_45.text())
        else:
            money = int(0)

        date = datetime.datetime.now()
        today = datetime.datetime.today().strftime('%A')
        day_name = ''
        if today == 'Saturday':
            day_name = 'السبت'
        elif today == 'ٍSunday':
            day_name = 'الاحد'
        elif today == 'Monday':
            day_name = 'الاثنين'
        elif today == 'Tuesday':
            day_name = 'الثلاثاء'
        elif today == 'Wednesday':
            day_name = 'الاربعاء'
        elif today == 'Thursday':
            day_name = 'الخميس'
        elif today == 'Friday':
            day_name = 'الجمعه'

        self.cur.execute('''INSERT INTO financial (operation, amount, date, text, day) VALUES (%s,%s,%s,%s,%s)''',
                         (operation, money, date, txt, day_name))
        self.db.commit()
        self.show_operations()
        self.show_all_operations()

    def show_operations(self):
        self.cur = self.db.cursor()

        self.cur.execute(
            '''SELECT * FROM financial''')
        data = self.cur.fetchall()

        total_save = 0
        diff = 0
        today = datetime.datetime.today()
        today_name = datetime.datetime.today().strftime('%A')
        if data:
            # Calc the total Money
            for ope in data:
                ope_type = ope[1]
                ope_money = ope[2]
                if ope_type == 'مقبوضات':
                    total_save += ope_money
                elif ope_type == 'مدفوعات':
                    total_save -= ope_money

            if today_name == 'Saturday':
                diff = 0
            elif today_name == 'Sunday':
                diff = 1
            elif today_name == 'Monday':
                diff = 2
            elif today_name == 'Tuesday':
                diff = 3
            elif today_name == 'Wednesday':
                diff = 4
            elif today_name == 'Thursday':
                diff = 5
            elif today_name == 'Friday':
                diff = 6

        target = today - datetime.timedelta(days=diff)

        self.lineEdit_42.setText(str(total_save))
        self.cur.execute('''SELECT * FROM financial WHERE date>=%s ORDER BY date ASC''', [target.date()])
        info = self.cur.fetchall()

        total = 0
        if info:
            x = info[0][3]
            self.tableWidget_9.setRowCount(0)
            for i in info:
                operation = i[1]
                money = int(i[2])
                txt = i[4]
                day = i[5]
                # self.tableWidget_9.insertRow(0)
                if x == i[3]:
                    row_pos = self.tableWidget_9.rowCount()
                    self.tableWidget_9.insertRow(row_pos)
                    if operation == 'مقبوضات':
                        self.tableWidget_9.setItem(row_pos, 1, QTableWidgetItem(str(money)))
                        total += money
                    elif operation == 'مدفوعات':
                        self.tableWidget_9.setItem(row_pos, 2, QTableWidgetItem(str(money)))
                        total -= money
                    self.tableWidget_9.setItem(row_pos, 3, QTableWidgetItem(str(txt)))
                    self.tableWidget_9.setItem(row_pos, 4, QTableWidgetItem(str(total)))
                    self.tableWidget_9.setItem(row_pos, 0, QTableWidgetItem(day))
                else:
                    x = i[3]
                    row_pos = self.tableWidget_9.rowCount()
                    self.tableWidget_9.insertRow(row_pos)
                    self.tableWidget_9.setItem(row_pos, 3, QTableWidgetItem('الاجمالي'))
                    self.tableWidget_9.setItem(row_pos, 4, QTableWidgetItem(str(total)))
                    row_pos = self.tableWidget_9.rowCount()
                    self.tableWidget_9.insertRow(row_pos)
                    self.tableWidget_9.setItem(row_pos, 1, QTableWidgetItem('-------'))
                    self.tableWidget_9.setItem(row_pos, 2, QTableWidgetItem('-------'))
                    self.tableWidget_9.setItem(row_pos, 3, QTableWidgetItem('-------'))

                    row_pos = self.tableWidget_9.rowCount()
                    self.tableWidget_9.insertRow(row_pos)

                    if operation == 'مقبوضات':
                        self.tableWidget_9.setItem(row_pos, 1, QTableWidgetItem(str(money)))
                        total += money
                    elif operation == 'مدفوعات':
                        self.tableWidget_9.setItem(row_pos, 2, QTableWidgetItem(str(money)))
                        total -= money
                    self.tableWidget_9.setItem(row_pos, 3, QTableWidgetItem(str(txt)))
                    self.tableWidget_9.setItem(row_pos, 4, QTableWidgetItem(str(total)))
                    self.tableWidget_9.setItem(row_pos, 0, QTableWidgetItem(day))

    def show_all_operations(self):
        self.cur = self.db.cursor()

        self.cur.execute(
            '''SELECT * FROM financial''')
        data = self.cur.fetchall()
        if data:
            self.tableWidget_7.setRowCount(0)
            for row in data:
                operation = row[1]
                money = row[2]
                date = row[3]
                txt = row[4]

                row_pos = self.tableWidget_7.rowCount()
                self.tableWidget_7.insertRow(row_pos)
                self.tableWidget_7.setItem(row_pos, 0, QTableWidgetItem(str(operation)))
                self.tableWidget_7.setItem(row_pos, 1, QTableWidgetItem(str(money)))
                self.tableWidget_7.setItem(row_pos, 2, QTableWidgetItem(str(txt)))
                self.tableWidget_7.setItem(row_pos, 3, QTableWidgetItem(str(date)))

    # *******************************
    #   Bus
    # *******************************

    def new_bus(self):
        code = self.lineEdit_97.text()
        start = self.dateEdit_7.date().toPyDate()
        end = self.dateEdit_8.date().toPyDate()

        if len(self.lineEdit_100.text()) > 0:
            money = self.lineEdit_100.text()
        else:
            money = 0

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT name FROM students WHERE id=%s''', [code])
        data = self.cur.fetchone()
        if data:
            name = data[0]
            self.cur.execute('''INSERT INTO bus (code, name, money, starts, finish) VALUES (%s,%s,%s,%s,%s)''',
                             (code, name, money, start, end))

            self.statusBar().showMessage('تم الاشتراك')
        else:
            self.statusBar().showMessage('الكود غير صحيح')
        self.db.commit()
        self.all_bus()

    def all_bus(self):
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT code,name,money,starts,finish FROM bus''')
        data = self.cur.fetchall()
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_pos)

    # *******************************
    #   Settings
    # *******************************

    def new_user(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        user_name = self.lineEdit_47.text()
        password = self.lineEdit_49.text()
        password_2 = self.lineEdit_51.text()
        permission = self.comboBox_13.currentText()

        if password == password_2:
            warning = QMessageBox.warning(self, 'Warning', 'اضافه مستخدم جديد؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''SELECT username FROM users ''')
                data = self.cur.fetchone()
                if not data:
                    self.cur.execute('''
                        INSERT INTO users (username,password,permission) 
                        VALUES (%s,%s,%s)''', (user_name, password, permission))
                    self.db.commit()
                    self.statusBar().showMessage('New user Added!')
                else:
                    self.statusBar().showMessage('User Already exist!')

        else:
            self.label_53.setText('Password Don\'t Match!')

    def search_user(self):
        username = self.lineEdit_48.text()
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT username FROM users WHERE username=%s''', [username])
        data = self.cur.fetchone()
        if data:
            self.statusBar().showMessage('User Found, Edit Info')

        else:
            self.statusBar().showMessage('No User Found !')

    def edit_user(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_48.text()
        password = self.lineEdit_50.text()
        password_2 = self.lineEdit_52.text()
        permission = self.comboBox_14.currentText()

        if password == password_2:
            warning = QMessageBox.warning(self, 'Warning', 'تعديل البيانات ؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''
                            UPDATE users SET password=%s,permission=%s
                            WHERE username=%s''', (password, permission, username))
                self.db.commit()
                self.statusBar().showMessage('تم تعديل البيانات')
        else:
            self.label_97.setText('Password Don\'t Match!')

    def delete_user(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_48.text()
        warning = QMessageBox.warning(self, 'Warning', 'حذف المستخدم ؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''DELETE FROM users WHERE username=%s''', [username])
            self.statusBar().showMessage('تم حذف المستخدم')

    def login(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_54.text()
        password = self.lineEdit_66.text()
        self.cur.execute('''SELECT * FROM users WHERE username=%s''', [username])
        data = self.cur.fetchone()
        if data:
            if data[2] == password:
                if data[3] == 'موظف':
                    self.groupBox.setHidden(False)
                    self.groupBox_2.setHidden(True)
                    self.statusBar().showMessage('Welcome')
                    self.pushButton_3.setVisible(False)
                    self.pushButton_4.setVisible(False)
                    self.pushButton_6.setVisible(False)
                elif data[3] == 'مدير':
                    self.groupBox.setHidden(False)
                    self.groupBox_2.setHidden(True)
                    self.statusBar().showMessage('Welcome')
                else:
                    self.statusBar().showMessage('!!!!!')

            else:
                self.statusBar().showMessage('Wrong Username and Password!')

        else:
            self.statusBar().showMessage('Not Found !')

    ############
    def refresh(self):
        self.cur = self.db.cursor()

        # Students
        self.cur.execute('''SELECT * FROM students''')
        data = self.cur.fetchall()
        if data != self.std:
            self.show_all_students()
        # Bus
        self.cur.execute('''SELECT * FROM bus''')
        data = self.cur.fetchall()
        if data != self.b:
            self.all_bus()
        # Questions
        self.cur.execute('''SELECT * FROM questions''')
        data = self.cur.fetchall()
        if data != self.q:
            self.show_questions()
        # daily_login
        self.cur.execute('''SELECT * FROM daily''')
        data = self.cur.fetchall()
        if data != self.d:
            self.all_daily_login()


        # self.cur.execute('''SELECT * FROM trainees''')
        # data = self.cur.fetchall()
        # if data != self.tr:
        #     self.show_all_students()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle('TA-System')
    window.setWindowIcon(QIcon('pic\ico.jpg'))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
