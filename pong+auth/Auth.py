from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QCursor
import hashlib, sys, sqlite3

con = sqlite3.connect('DB.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        password TEXT
)""")
con.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS Records(
        id INTEGER PRIMARY KEY,
        score TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(id)     
)""")
con.commit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.le_name = QLineEdit(self.widget)
        self.le_name.setPlaceholderText("Login")
        self.le_name.setGeometry(40, 40, 400, 25)

        self.le_password = QLineEdit(self.widget)
        self.le_password.setPlaceholderText("Password")
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.le_password.setGeometry(40, 80, 400, 25)

        btn_auth = QPushButton("Авторизация", self.widget)
        btn_auth.setGeometry(60, 110, 100, 25)
        btn_auth.clicked.connect(self.auth)

        btn_reg = QPushButton("Регистрация", self.widget)
        btn_reg.setGeometry(60, 140, 100, 25)
        btn_reg.clicked.connect(self.captcha)
# капча
        self.field_captcha = QLabel(self.widget)
        self.field_captcha.hide()
        self.field_captcha.setGeometry(20, 200, 1100, 600)

        self.lbl_red = QLabel(self.field_captcha)
        self.lbl_red.setGeometry(20, 340, 200, 200)
        self.lbl_red.setStyleSheet("background-color: red")
        self.lbl_red.setObjectName("self.lbl_red")

        self.lbl_blue = QLabel(self.field_captcha)
        self.lbl_blue.setGeometry(20, 130, 200, 200)
        self.lbl_blue.setStyleSheet("background-color: blue")
        self.lbl_blue.setObjectName("self.lbl_blue")

        self.lbl_green = QLabel(self.field_captcha)
        self.lbl_green.setGeometry(230, 130, 200, 200)
        self.lbl_green.setStyleSheet("background-color: green")
        self.lbl_green.setObjectName("self.lbl_green")

        self.lbl_yellow = QLabel(self.field_captcha)
        self.lbl_yellow.setGeometry(230, 340, 200, 200)
        self.lbl_yellow.setStyleSheet("background-color: yellow")
        self.lbl_yellow.setObjectName("self.lbl_yellow")

        self.capcha = None


    def auth(self):
        login = self.le_name.text()
        password = self.le_password.text()
        con = sqlite3.connect('DB.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE name=? AND password=?", [(login), (hashlib.sha256(password.encode('utf-8')).hexdigest())])
        selected = cur.fetchall()
        if selected:
            import pong
            self.pwindow = pong.PongWindow()
            self.pwindow.setGeometry(300, 200, 1000, 600)
            self.pwindow.show()
            self.hide()

    def captcha(self):
        self.field_captcha.show()
        self.capcha = True


    def reg(self):
        login = self.le_name.text()
        password = self.le_password.text()
        con = sqlite3.connect('DB.db')
        cur = con.cursor()
        cur.execute(f'INSERT OR IGNORE INTO Users (name, password) VALUES(?, ?)', [(login), (hashlib.sha256(password.encode('utf-8')).hexdigest())])
        con.commit()

    def mousePressEvent(self, event):
        if self.capcha:
            if event.button() == Qt.MouseButton.LeftButton:
                local_pos = QCursor.pos()
                x, y = local_pos.x(), local_pos.y()
                widget = QApplication.widgetAt(x, y)
                if "self.lbl_" in widget.objectName():
                    self.widget1 = widget.objectName()
                    self.widget1_pos = QPoint(widget.pos().x(), widget.pos().y())

    def mouseReleaseEvent(self, event):
        if self.capcha:
            local_pos = QCursor.pos()
            x, y = local_pos.x(), local_pos.y()
            widget = QApplication.widgetAt(x, y)
            if widget and "self.lbl_" in widget.objectName():
                widget2 = widget.objectName()
                coords = widget.pos()
                widget2_pos = QPoint(coords.x(), coords.y())
                if not self.widget1[0] == widget.objectName():
                    eval(f"{self.widget1}").move(widget2_pos)
                    eval(f"{widget2}").move(self.widget1_pos)
            else:
                self.widget2 = ""
            if not self.field_captcha.childAt(20, 130).objectName() == "self.lbl_red":
                return
            if not self.field_captcha.childAt(20, 340).objectName() == "self.lbl_blue":
                return
            if not self.field_captcha.childAt(230, 130).objectName() == "self.lbl_green":
                return
            if not self.field_captcha.childAt(230, 340).objectName() == "self.lbl_yellow":
                return
            self.reg()
            self.field_captcha.hide()
            self.capcha = False
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(300, 200, 1700, 1100)
    window.show()
    app.exec()
