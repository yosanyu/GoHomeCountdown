import sys
import webbrowser
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import QTimer
from PySide6.QtCore import QThread
from datetime import datetime
from datetime import timedelta
from win10toast import ToastNotifier
from localization import get_languages
from localization import get_translations

_USE_LANGUAGE = 'English'
_FILE_PATH = 'language.txt'
_ICON_PATH = 'notification_icon.ico'
_HOURS = 9
_URL = ''

# 根據需求調整
def go_home_clock_in():
    webbrowser.open(_URL)

class WorkerThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.show_toast()

    def show_toast(self):
        toaster = ToastNotifier()
        title = get_translations(_USE_LANGUAGE, 'go_home_clock_in')
        messgae = get_translations(_USE_LANGUAGE, 'is_time_to_go_home')
        toaster.show_toast(title, messgae, icon_path=_ICON_PATH, duration=1000)

class MainWindow(QMainWindow):
    def __init__(self):
        self.adjusted_time = None
        self.buttons = []
        self.labels = []
        self.window_setting()
        self.init_widget()
        self.init_timer()
        self.load_language_setting()
        self.setWindowTitle(get_translations(_USE_LANGUAGE, 'clock_in_countdown'))

    def window_setting(self):
        super().__init__()
        self.resize(1024, 768)
        self.setFixedSize(1024, 768)
        self.setWindowIcon(QtGui.QIcon(_ICON_PATH))

    def init_widget(self):
        self.init_button()
        self.init_label()
        self.init_line_edit()
        self.init_combo_box()

    def init_button(self):
        self.create_button()
        self.set_button_location()
        self.set_button_text()
        self.set_button_font()
        self.bind_button_clicked()

    def create_button(self):
        self.button_clock_in = QPushButton(self)
        self.button_fix_time = QPushButton(self)
        self.buttons = [self.button_clock_in, self.button_fix_time]

    def set_button_location(self):
        self.button_clock_in.setGeometry(300, 200, 180, 50)
        self.button_fix_time.setGeometry(500, 200, 180, 50)

    def set_button_text(self):
        keys = ['clock_in', 'fix_time']
        for index, button in enumerate(self.buttons):
            text = get_translations(_USE_LANGUAGE, keys[index])
            button.setText(text)

    def set_button_font(self):
        font = self.button_clock_in.font()
        font.setPointSize(20)
        for button in self.buttons:
            button.setFont(font)

    def bind_button_clicked(self):
        self.button_clock_in.clicked.connect(self.on_button_clock_in_clicked)
        self.button_fix_time.clicked.connect(self.on_button_fix_time_clicked)

    def on_button_clock_in_clicked(self):
        keys = ['go_home_time', 'today_go_home_time']
        self.button_clock_in.setEnabled(False)
        current_time = datetime.now()
        self.adjusted_time = current_time + timedelta(hours=_HOURS)
        str_time = self.adjusted_time.strftime('%H:%M:%S')
        title = get_translations(_USE_LANGUAGE, keys[0])
        message = get_translations(_USE_LANGUAGE, keys[1]) + str_time
        QMessageBox.information(self, title, message)
        message = get_translations(_USE_LANGUAGE, keys[0])
        self.clock_in_time.setText(f'{message}:{str_time}')
        self.timer.start(1000)

    def on_button_fix_time_clicked(self):
        if not self.adjusted_time:
            key = 'not_clock_in'
            message = get_translations(_USE_LANGUAGE, key)
            QMessageBox.information(self, message, message)
            return
        str_correction_time = self.input_field.text().strip()
        try:
            correction_time = datetime.strptime(str_correction_time, '%H:%M:%S').time()
        except Exception as e:
            keys = ['format_error', 'fix_clock_in_time']
            title = get_translations(_USE_LANGUAGE, keys[0])
            message = get_translations(_USE_LANGUAGE, keys[1])
            QMessageBox.information(self, title, message)
            return
        keys = ['go_home_time', 'fix_go_home_time', 'fix_today_go_home_time']
        correction_datetime = datetime.combine(datetime.now().date(), correction_time)
        self.adjusted_time = correction_datetime + timedelta(hours=_HOURS)
        str_time = self.adjusted_time.strftime('%H:%M:%S')
        message = get_translations(_USE_LANGUAGE, keys[0])
        self.clock_in_time.setText(f'{message}:{str_time}')
        self.button_fix_time.setEnabled(False)
        self.input_field.setReadOnly(True)
        title = get_translations(_USE_LANGUAGE, keys[1])
        message = get_translations(_USE_LANGUAGE, keys[2]) + str_time
        QMessageBox.information(self, title, message)

    def init_label(self):
        self.create_label()
        self.set_label_location()
        self.set_label_font()

    def create_label(self):
        self.clock_in_time = QLabel(self)
        self.go_home_time = QLabel(self)
        self.labels = [self.clock_in_time, self.go_home_time]

    def set_label_location(self):
        self.clock_in_time.setGeometry(300, 300, 500, 50)
        self.go_home_time.setGeometry(300, 350, 500, 50)

    def set_label_font(self):
        font = self.clock_in_time.font()
        font.setPointSize(30)
        for label in self.labels:
            label.setFont(font)

    def init_line_edit(self):
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(300, 100, 380, 50)
        key = 'fix_clock_in_time'
        message = get_translations(_USE_LANGUAGE, key)
        self.input_field.setPlaceholderText(message)
        font = self.input_field.font()
        font.setPointSize(13)
        self.input_field.setFont(font)

    def init_combo_box(self):
        self.combo_box_language = QComboBox(self)
        self.combo_box_language.setGeometry(800, 10, 200, 50)
        languages = get_languages()
        self.combo_box_language.addItems(languages)
        self.combo_box_language.currentIndexChanged.connect(self.on_combo_box_changed)
        font = self.combo_box_language.font()
        font.setPointSize(25)
        self.combo_box_language.setFont(font)

    def on_combo_box_changed(self):
        global _USE_LANGUAGE
        if _USE_LANGUAGE != self.combo_box_language.currentText():
            keys = ['clock_in_countdown', 'clock_in', 'fix_time', 'fix_clock_in_time',
                    'go_home_time' ]
            _USE_LANGUAGE = self.combo_box_language.currentText()
            window_title = get_translations(_USE_LANGUAGE, keys[0])
            self.setWindowTitle(window_title)
            button_clock_in_text = get_translations(_USE_LANGUAGE, keys[1])
            button_fix_time_text = get_translations(_USE_LANGUAGE, keys[2])
            self.button_clock_in.setText(button_clock_in_text)
            self.button_fix_time.setText(button_fix_time_text)
            self.input_field.setPlaceholderText(get_translations(_USE_LANGUAGE, keys[3]))
            message = get_translations(_USE_LANGUAGE, keys[4])
            if self.adjusted_time:
                str_time = self.adjusted_time.strftime('%H:%M:%S')
                self.clock_in_time.setText(f'{message}:{str_time}')
            try:
                with open(_FILE_PATH, 'w', encoding='utf-8') as file:
                    file.write(_USE_LANGUAGE)
            except Exception as e:
                pass

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def load_language_setting(self):
        try:
            with open(_FILE_PATH, 'r', encoding='utf-8') as file:
                language = file.read().strip()
                if language in get_languages():
                    self.combo_box_language.setCurrentText(language)
        except Exception as e:
            pass
                

    def update_time(self):
        current_time = datetime.now()
        remaining_time = self.adjusted_time - current_time
        if remaining_time.total_seconds() <= 0:
            self.timer.stop()
            worker_thread = WorkerThread()
            worker_thread.start()
            go_home_clock_in()
            QApplication.alert(self, 0)
            keys = ['go_home_clock_in', 'is_time_to_go_home']
            title = get_translations(_USE_LANGUAGE, keys[0])
            message = get_translations(_USE_LANGUAGE, keys[1])
            result = QMessageBox.information(self, title, message)
            if result == QMessageBox.Ok:
                sys.exit()

        else:
            key = 'remaining_time'
            str_remaining = str(remaining_time).split('.')[0]
            str_remaining = '0' + str_remaining
            message = get_translations(_USE_LANGUAGE, key) + str_remaining
            self.go_home_time.setText(message)


    def closeEvent(self, event):
        keys = ['confirm', 'close_confirm']
        title = get_translations(_USE_LANGUAGE, keys[0])
        message = get_translations(_USE_LANGUAGE, keys[1])
        result = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
