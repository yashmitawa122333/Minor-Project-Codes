from PyQt5 import QtWidgets, QtCore
import sys
import mysql.connector as mc


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login with database")
        self.resize(500, 300)

        self.lg = None
        self.sg = None

        self.Horizontal_layout = QtWidgets.QHBoxLayout()
        self.Vertical_layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('<h2>Hi</h2>', self)
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.login_pushbutton = QtWidgets.QPushButton('Log in')
        self.login_pushbutton.clicked.connect(self.login_btn)
        self.signup_pushbutton = QtWidgets.QPushButton('Sign up')
        self.signup_pushbutton.clicked.connect(self.signup_btn)

        self.Horizontal_layout.addWidget(self.login_pushbutton)
        self.Horizontal_layout.addWidget(self.signup_pushbutton)

        self.Vertical_layout.addWidget(self.label, stretch=1)
        self.Vertical_layout.addLayout(self.Horizontal_layout, stretch=3)

        self.setLayout(self.Vertical_layout)

    def login_btn(self):
        self.lg = Login()
        self.lg.sendLoginName.connect(self.check_send_signal)
        self.lg.show()

    def signup_btn(self):
        self.sg = Signup()
        self.sg.sendLoginName.connect(self.check_send_signal)
        self.sg.show()

    def check_send_signal(self, msg: str):
        if msg == 'Failed to Login':
            self.label.setText(f'<h2>Hi, {msg}</h2>')
        else:
            self.label.setText(f'<h2>Hi, {msg}</h2>')
            self.login_pushbutton.close()
            self.signup_pushbutton.close()


class Login(QtWidgets.QDialog):
    sendLoginName = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(400, 200)

        self.Grid_layout = QtWidgets.QGridLayout()

        self.popup_label = QtWidgets.QLabel('<h2>Please login here</h2>')
        self.label1 = QtWidgets.QLabel('Email :-')
        self.label2 = QtWidgets.QLabel('Password :-')

        self.line_edit_email = QtWidgets.QLineEdit()
        self.line_edit_password = QtWidgets.QLineEdit()

        self.push_button_login = QtWidgets.QPushButton("Log in")
        self.push_button_login.resize(150, 50)
        self.push_button_login.clicked.connect(self.get_database)

        self.Grid_layout.addWidget(self.popup_label, 0, 1)
        self.Grid_layout.addWidget(self.label1, 1, 0)
        self.Grid_layout.addWidget(self.line_edit_email, 1, 1)
        self.Grid_layout.addWidget(self.label2, 2, 0)
        self.Grid_layout.addWidget(self.line_edit_password, 2, 1)
        self.Grid_layout.addWidget(self.push_button_login, 3, 1)

        self.setLayout(self.Grid_layout)

    def get_database(self):
        try:
            connection = mc.connect(host='localhost',
                                    database='user',
                                    user='root',
                                    password='yash')
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM data;')
            output = cursor.fetchall()

            if len(output) == 0:
                self.sendLoginName.emit('Please create your account!')
                self.close()

            elif '@gmail.com' not in self.line_edit_email.text():
                self.popup_label.setText('<h2>Please enter valid mail</h2>')
            else:
                check = None
                for row in output:
                    if row[0] == str(self.line_edit_email.text()) and row[1] == str(self.line_edit_password.text()):
                        print(row)
                        check = row
                    else:
                        check = None
                if check is None:
                    self.popup_label.setText('<h2>Email not registered!</h2>')
                    self.line_edit_email.clear()
                    self.line_edit_password.clear()
                else:
                    self.sendLoginName.emit(check[2])
                    self.close()

        except mc.Error:
            self.sendLoginName.emit('Failed to login')
            self.close()


class Signup(QtWidgets.QDialog):
    sendLoginName = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(400, 250)
        self.setWindowTitle('Update the Sql database')

        self.grid_layout = QtWidgets.QGridLayout()
        self.Horizontal_layout = QtWidgets.QHBoxLayout()
        self.Vertical_layout = QtWidgets.QVBoxLayout()

        self.popup_label = QtWidgets.QLabel()
        self.popup_label.setText('<h2>Please enter your detail</h2>')
        self.popup_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        self.label1 = QtWidgets.QLabel('Name :-')
        self.line_edit_name = QtWidgets.QLineEdit()

        self.label2 = QtWidgets.QLabel('Email :-')
        self.line_edit_email = QtWidgets.QLineEdit()

        self.label3 = QtWidgets.QLabel('Password:-')
        self.line_edit_password = QtWidgets.QLineEdit()

        self.label4 = QtWidgets.QLabel('Confirm Password:-')
        self.line_edit_confirm_password = QtWidgets.QLineEdit()

        self.push_button = QtWidgets.QPushButton("Sign up")
        self.push_button.clicked.connect(self.update_sql_database)

        self.grid_layout.addWidget(self.popup_label, 0, 1)

        self.grid_layout.addWidget(self.label1, 1, 0)
        self.grid_layout.addWidget(self.line_edit_name, 1, 1)
        self.grid_layout.addWidget(self.label2, 2, 0)
        self.grid_layout.addWidget(self.line_edit_email, 2, 1)
        self.grid_layout.addWidget(self.label3, 3, 0)
        self.grid_layout.addWidget(self.line_edit_password, 3, 1)
        self.grid_layout.addWidget(self.label4, 4, 0)
        self.grid_layout.addWidget(self.line_edit_confirm_password, 4, 1)
        self.grid_layout.addWidget(self.push_button, 5, 1)

        self.setLayout(self.grid_layout)

    def update_sql_database(self):
        try:
            connection = mc.connect(host='localhost',
                                    database='user',
                                    user='root',
                                    password='yash')
            cursor = connection.cursor()
            value = (self.line_edit_name.text(), self.line_edit_email.text(),
                     self.line_edit_password.text(), self.line_edit_confirm_password.text())
            cursor.execute(f'SELECT * FROM data;')
            output = cursor.fetchall()
            if len(output) == 0:
                cursor.execute(f'INSERT INTO data (Name, Email, Password, Confirm) VALUES {value}')
                connection.commit()
                self.sendLoginName.emit(self.line_edit_name.text())
                self.close()
            elif self.line_edit_confirm_password.text() != self.line_edit_password.text():
                self.popup_label.setText('<h2>Please match the password!</h2>')
                self.line_edit_confirm_password.clear()
            elif '@gmail.com' not in self.line_edit_email.text():
                self.popup_label.setText('<h2>Please enter valid mail!</h2>')
                self.line_edit_email.clear()
            else:
                for row in output:
                    if row[0] == str(self.line_edit_email.text()) or row[1] == str(self.line_edit_password.text()):
                        self.popup_label.setText('<h2>Email already occupied!</h2>')
                        connection.commit()
                        self.line_edit_email.clear()
                        self.line_edit_name.clear()
                        self.line_edit_password.clear()
                        self.line_edit_confirm_password.clear()
                    else:
                        cursor.execute(f'INSERT INTO data (Name, Email, Password, Confirm) VALUES {value}')
                        connection.commit()
                        self.sendLoginName.emit(self.line_edit_name.text())
                        self.close()
                        break

        except mc.Error:
            self.sendLoginName.emit('Failed to Login')
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = MainWindow()
    login.show()
    sys.exit(app.exec_())
