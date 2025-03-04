# gui.py
import os
import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QPushButton, QVBoxLayout, QLabel, 
    QFileDialog, QRadioButton, QButtonGroup, QListWidget, 
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtCore import QUrl
from converter import convert_pdf_to_word, convert_word_to_pdf

DB_PATH = "history.db"

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    # Emit a message and the output file path once conversion is finished.
    finished = pyqtSignal(str, str)

    def __init__(self, conversion_func, input_file, output_file):
        super().__init__()
        self.conversion_func = conversion_func
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        self.progress.emit(10)
        try:
            self.conversion_func(self.input_file, self.output_file)
            self.progress.emit(100)
            self.finished.emit("Conversion complete!", self.output_file)
        except Exception as e:
            self.finished.emit("Error: " + str(e), "")

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Converter App")
        self.resize(600, 400)
        # (Optional) Set an application icon if available.
        # self.setWindowIcon(QIcon("assets/icon.png"))
        self.stacked_widget = QStackedWidget(self)
        self.current_output_file = ""  # Holds the most recent converted file path.
        self.initUI()

    def initUI(self):
        self.welcome_page = self.create_welcome_page()
        self.conversion_page = self.create_conversion_page()
        self.history_page = self.create_history_page()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.conversion_page)
        self.stacked_widget.addWidget(self.history_page)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to the PDF Converter App")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        start_button = QPushButton("Start Converting")
        start_button.clicked.connect(self.go_to_conversion_page)
        layout.addWidget(start_button)

        history_button = QPushButton("View History")
        history_button.clicked.connect(self.go_to_history_page)
        layout.addWidget(history_button)

        page.setLayout(layout)
        return page

    def create_conversion_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.pdf_to_word_radio = QRadioButton("Convert PDF to Word")
        self.word_to_pdf_radio = QRadioButton("Convert Word to PDF")
        self.pdf_to_word_radio.setChecked(True)

        radio_group = QButtonGroup(page)
        radio_group.addButton(self.pdf_to_word_radio)
        radio_group.addButton(self.word_to_pdf_radio)

        layout.addWidget(self.pdf_to_word_radio)
        layout.addWidget(self.word_to_pdf_radio)

        file_select_button = QPushButton("Select Files")
        file_select_button.clicked.connect(self.select_files)
        layout.addWidget(file_select_button)

        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)

        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(convert_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Back button to return to the welcome page.
        back_button = QPushButton("Back to Welcome")
        back_button.clicked.connect(self.go_to_welcome_page)
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Conversion History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        refresh_button = QPushButton("Refresh History")
        refresh_button.clicked.connect(self.load_history)
        layout.addWidget(refresh_button)

        back_button = QPushButton("Back to Welcome")
        back_button.clicked.connect(self.go_to_welcome_page)
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def go_to_conversion_page(self):
        self.stacked_widget.setCurrentWidget(self.conversion_page)

    def go_to_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def go_to_history_page(self):
        self.load_history()
        self.stacked_widget.setCurrentWidget(self.history_page)

    def select_files(self):
        if self.pdf_to_word_radio.isChecked():
            files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")
        else:
            files, _ = QFileDialog.getOpenFileNames(self, "Select Word Files", "", "Word Files (*.docx)")
        if files:
            self.file_list_widget.clear()
            for f in files:
                self.file_list_widget.addItem(f)

    def start_conversion(self):
        count = self.file_list_widget.count()
        if count == 0:
            QMessageBox.warning(self, "No Files", "Please select at least one file to convert.")
            return

        # Process files one by one (sequentially for simplicity)
        for i in range(count):
            item = self.file_list_widget.item(i)
            input_file = item.text()
            if self.pdf_to_word_radio.isChecked():
                output_file = input_file.rsplit(".", 1)[0] + "_converted.docx"
                conversion_func = convert_pdf_to_word
            else:
                output_file = input_file.rsplit(".", 1)[0] + "_converted.pdf"
                conversion_func = convert_word_to_pdf

            self.current_output_file = output_file
            self.thread = ConversionThread(conversion_func, input_file, output_file)
            self.thread.progress.connect(self.progress_bar.setValue)
            self.thread.finished.connect(self.on_conversion_finished)
            self.thread.start()
            # In a real-world scenario, you might want to wait for each conversion to finish
            # before starting the next one, especially for batch processing.

    def on_conversion_finished(self, message, output_file):
        # Prompt the user with the conversion status and offer to open the file.
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Conversion Status")
        msg_box.setText(message)
        if output_file:
            view_button = msg_box.addButton("View File", QMessageBox.ButtonRole.ActionRole)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        if output_file and msg_box.clickedButton() == view_button:
            # Open the converted file with the system default application.
            QDesktopServices.openUrl(QUrl.fromLocalFile(output_file))

        self.progress_bar.setValue(0)

    def load_history(self):
        """Load conversion history from the SQLite database."""
        self.history_list.clear()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT file_name, conversion_type, timestamp FROM history ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            display_text = f"{row[2]}: {row[0]} ({row[1]})"
            self.history_list.addItem(display_text)

