import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import QTimer
from PySide6.QtCore import QThread
from PySide6 import QtGui
from datetime import datetime
from datetime import timedelta
from win10toast import ToastNotifier
import webbrowser
import time

_ICON_PATH = 'notification_icon.ico'
_BUTTON_TEXTS = ['上班打卡', '更正時間']
_HOURS = 9
_URL = ''

# 根據需求調整
def go_home_check_in():
    webbrowser.open(_URL)

class WorkerThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.show_toast()

    def show_toast(self):
        toaster = ToastNotifier()
        toaster.show_toast('下班打卡', '是時候打下班卡了', icon_path=_ICON_PATH, duration=1000)

class MainWindow(QMainWindow):
    def __init__(self):
        self.adjusted_time = None
        self.buttons = []
        self.labels = []
        self.window_setting()
        self.init_widget()
        self.init_timer()

    def window_setting(self):
        super().__init__()
        self.setWindowTitle('打卡倒數')
        self.resize(1024, 768)
        self.setFixedSize(1024, 768)
        self.setWindowIcon(QtGui.QIcon(_ICON_PATH))

    def init_widget(self):
        self.init_button()
        self.init_label()
        self.init_line_edit()

    def init_button(self):
        self.create_button()
        self.set_button_location()
        self.set_button_text()
        self.set_button_font()
        self.bind_button_clicked()

    def create_button(self):
        self.button_check_in = QPushButton(self)
        self.button_fix_time = QPushButton(self)
        self.buttons = [self.button_check_in, self.button_fix_time]

    def set_button_location(self):
        self.button_check_in.setGeometry(300, 200, 200, 50)
        self.button_fix_time.setGeometry(550, 100, 200, 50)

    def set_button_text(self):
        for index, button in enumerate(self.buttons):
            button.setText(_BUTTON_TEXTS[index])

    def set_button_font(self):
        font = self.button_check_in.font()
        font.setPointSize(20)
        for button in self.buttons:
            button.setFont(font)

    def bind_button_clicked(self):
        self.button_check_in.clicked.connect(self.on_button_check_clicked)
        self.button_fix_time.clicked.connect(self.on_button_fix_time_clicked)

    def on_button_check_clicked(self):
        self.button_check_in.setEnabled(False)
        current_time = datetime.now()
        self.adjusted_time = current_time + timedelta(hours=_HOURS)
        str_time = self.adjusted_time.strftime('%H:%M:%S')
        QMessageBox.information(self, '下班時間', f'今天下班時間為{str_time}')
        self.check_in_time.setText(f'下班時間:{str_time}')
        self.timer.start(1000)

    def on_button_fix_time_clicked(self):
        str_correction_time = self.input_field.text().strip()
        try:
            correction_time = datetime.strptime(str_correction_time, '%H:%M:%S').time()
        except Exception as e:
            QMessageBox.information(self, '格式有誤', '更新下班時間格式：HH:MM:SS')
            return
        correction_datetime = datetime.combine(datetime.now().date(), correction_time)
        self.adjusted_time = correction_datetime + timedelta(hours=_HOURS)
        str_time = self.adjusted_time.strftime('%H:%M:%S')
        self.check_in_time.setText(f'下班時間:{str_time}')
        self.button_fix_time.setEnabled(False)
        self.input_field.setReadOnly(True)
        QMessageBox.information(self, '更正下班時間', f'更正今天下班時間為{str_time}')

    def init_label(self):
        self.create_label()
        self.set_label_location(        )
        self.set_label_font()

    def create_label(self):
        self.check_in_time = QLabel(self)
        self.go_home_time = QLabel(self)
        self.labels = [self.check_in_time, self.go_home_time]

    def set_label_location(self):
        self.check_in_time.setGeometry(300, 300, 500, 50)
        self.go_home_time.setGeometry(300, 350, 500, 50)

    def set_label_font(self):
        font = self.check_in_time.font()
        font.setPointSize(30)
        for label in self.labels:
            label.setFont(font)

    def init_line_edit(self):
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(300, 100, 200, 50)
        self.input_field.setPlaceholderText('更正打卡時間（格式：HH:MM:SS')
        font = self.input_field.font()
        font.setPointSize(10)
        self.input_field.setFont(font)

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        current_time = datetime.now()
        remaining_time = self.adjusted_time - current_time
        if remaining_time.total_seconds() <= 0:
            self.timer.stop()
            worker_thread = WorkerThread()
            worker_thread.start()
            go_home_check_in()
            QApplication.alert(self, 0)
            result = QMessageBox.warning(self, '下班打卡', '是時候打下班卡了')
            if result == QMessageBox.Ok:
                sys.exit()

        else:
            str_remaining = str(remaining_time).split('.')[0]  # 去除毫秒部分
            str_remaining = '0' + str_remaining
            self.go_home_time.setText(f'剩餘時間:{str_remaining}')


    def closeEvent(self, event):
        result = QMessageBox.question(self, '確認', '你確定要關閉嗎？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
