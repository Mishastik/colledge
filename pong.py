from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        lbl_field = QLabel(widget)
        lbl_field.setStyleSheet('background-color: black')
        lbl_field.setGeometry(100, 100, 800, 400)

        lbl_line = QLabel(lbl_field)
        lbl_line.setStyleSheet('background-color: white')
        lbl_line.setGeometry(399, 0, 2, 400)

        self.lbl_ball = QLabel(lbl_field)
        self.lbl_ball.setStyleSheet('background-color: white')
        self.lbl_ball.setGeometry(395, 195, 10, 10)
        self.ball = {}
        self.ball['speedX'] = 3
        self.ball['speedY'] = 2

        self.panel_player = QLabel('0', lbl_field)
        self.panel_player.setStyleSheet('''background-color: transparent;
                                        color: white;''')
        self.panel_player.setGeometry(199, 5, 200, 15)
        self.score_player = 0

        self.racket_player = QLabel(lbl_field)
        self.racket_player.setStyleSheet('background-color: white')
        self.racket_player.setGeometry(20, 175, 20, 50)
        self.player = {}

        self.panel_enemy = QLabel('0', lbl_field)
        self.panel_enemy.setStyleSheet('''background-color: transparent;
                                        color: white;''')
        self.panel_enemy.setGeometry(599, 5, 200, 15)
        self.score_enemy = 0

        self.racket_enemy = QLabel(lbl_field)
        self.racket_enemy.setStyleSheet('background-color: white')
        self.racket_enemy.setGeometry(760, 175, 20, 50)
        self.enemy = {}

        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.playerMove)
        # self.timer.timeout.connect(self.enemyMove)
        self.timer.timeout.connect(self.ballMove)
        self.timer.start(20)

    def keyPressEvent(self, event):
        key = event.key()
        self.player['up'] = self.racket_player.geometry().y()
        self.player['down'] = self.player['up'] + self.racket_player.height()
        self.player['left'] = self.racket_player.geometry().x()
        self.player['right'] = self.player['left'] + self.racket_player.width()
        if key == Qt.Key.Key_W:
            if self.player['up'] > 0:
                self.racket_player.move(self.player['left'], self.player['up'] - 5)
        if key == Qt.Key.Key_S:
            if self.player['down'] < 400:
                self.racket_player.move(self.player['left'], self.player['up'] + 5)

        self.enemy['up'] = self.racket_enemy.geometry().y()
        self.enemy['down'] = self.enemy['up'] + self.racket_enemy.height()
        self.enemy['left'] = self.racket_enemy.geometry().x()
        self.enemy['right'] = self.enemy['left'] + self.racket_enemy.width()
        if key == Qt.Key.Key_Up:
            if self.enemy['up'] > 0:
                self.racket_enemy.move(self.enemy['left'], self.enemy['up'] - 5)
        if key == Qt.Key.Key_Down:
            if self.enemy['down'] < 400:
                self.racket_enemy.move(self.enemy['left'], self.enemy['up'] + 5)

    def ballMove(self):
        self.ball['up'] = self.lbl_ball.geometry().y()
        self.ball['down'] = self.ball['up'] + self.lbl_ball.height()
        self.ball['left'] = self.lbl_ball.geometry().x()
        self.ball['right'] = self.ball['left'] + self.lbl_ball.width()
        self.lbl_ball.move(self.ball['left'] + self.ball['speedX'], self.ball['up'] + self.ball['speedY'])
        if self.ball['up'] < 2:
            self.ball['speedY'] = 2
        if self.ball['down'] > 398:
            self.ball['speedY'] = -2
        if self.ball['left'] == 41:
            if self.ball['down'] > self.player['up'] and self.ball['up'] < self.player['down']:
                self.ball['speedX'] = 3
        if self.ball['right'] == 759:
            if self.ball['down'] > self.enemy['up'] and self.ball['up'] < self.enemy['down']:
                self.ball['speedX'] = -3
        if self.lbl_ball.geometry().x() < 2:
            self.score_enemy += 1
            self.panel_enemy.setText(str(self.score_enemy))
            self.lbl_ball.move(395, 195)
        if self.lbl_ball.geometry().x() > 798:
            self.score_player += 1
            self.panel_player.setText(str(self.score_player))
            self.lbl_ball.move(395, 195)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(300, 200, 1000, 600)
    window.show()
    app.exec()
