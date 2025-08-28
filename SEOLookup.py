from imports import *
import api
# ─────────────────────────────
# GUI (PyQt6)
# ─────────────────────────────
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
QLabel, QDialog, QSpinBox, QListWidget, QAbstractItemView, QListWidgetItem )
from PyQt6.QtCore import pyqtSignal


SYSTEM = sys.platform
WEBAPI = api.webSearch()


def open_folder(folder_path: str = ""):
    path = folder_path
    if SYSTEM == "win32":
        os.startfile(path)  # type: ignore
    elif SYSTEM == "linux":
        subprocess.call(["xdg-open", folder_path.replace("\\", "/")])


class ResultDialog(QDialog):
    def __init__(self, result_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Results")
        self.setMinimumSize(300, 150)

        layout = QVBoxLayout()
        label = QLabel(result_text)
        layout.addWidget(label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        folder_button = QPushButton("Open Containing Folder")
        folder_button.clicked.connect(self.open_screenshotfolder)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def open_screenshotfolder(self):
        open_folder(f'{os.path.expanduser("~")}\\Pictures\\SEOLookup')


class SearchGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle("SEOLookup Beta 1")
        self.setGeometry(580, 300, 600, 350)

        # Layout
        layout = QVBoxLayout()
        options_layout = QHBoxLayout()

        # Page Selection
        self.pages_select = QSpinBox()
        self.pages_select.setValue(int(dotenv.get_key(".env", "MAX_PAGE_SEARCH")))  # type: ignore

        # Engine Selection
        self.engine_select = QListWidget()
        self.engine_select.addItems(["Google", "Bing"])
        self.engine_select.setFixedHeight(75)

        # Preselecting google as engine
        item = self.engine_select.item(0)
        item.setSelected(True)  # type: ignore
        self.engine_select.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        options_layout.addWidget(QLabel("Pages to search"))
        options_layout.addWidget(self.pages_select)
        options_layout.addWidget(QLabel("Engine to use"))
        options_layout.addWidget(self.engine_select)
        layout.addLayout(options_layout)

        # Input fields
        self.search_term_input = QLineEdit()
        self.search_link_input = QLineEdit()
        self.search_link_input.textEdited.connect(self.check_clear_input)
        self.search_term_input.textEdited.connect(self.check_clear_input)
        layout.addWidget(QLabel("Search Term"))
        layout.addWidget(self.search_term_input)
        layout.addWidget(QLabel("Search Link"))
        layout.addWidget(self.search_link_input)

        # Buttons
        self.search_button = QPushButton("Search")
        self.search_button.setDisabled(True)
        self.search_button.setToolTip("Term and Link are required to search")
        #Set up the behavoiur of the Directory Button, either open selected one or set up the folder.
        self.directory_button = QPushButton()
        self.directory_button.setToolTip(
            "Select where you want to save your Screenshots \nDefault location is Pictures -> SEOLookup"
        )
        self.directory_button.setText("Select Directory")
        """if dotenv.get_key(".env","IMAGE_DIRECTORY") == "None" or dotenv.get_key(".env","IMAGE_DIRECTORY") == "S":
            self.directory_button.setText("Select Image Directory")
            self.directory_button.setToolTip(
            "Select where you want to save your Screenshots \nDefault location is Pictures -> SEOLookup"
        )

        else:
            self.directory_button.setText("Open Image Directory")
            self.directory_button.setToolTip("Open Selected Screenshot folder") """

        self.open_image_button = QPushButton("Open Image")

        
        layout.addWidget(self.search_button)
        layout.addWidget(self.open_image_button)
        #layout.addWidget(self.directory_button)

        # Connect signals and slots
        self.pages_select.valueChanged.connect(self.set_page)
        self.engine_select.itemSelectionChanged.connect(self.set_engine)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.directory_button.clicked.connect(self.directory_handler)
        self.open_image_button.clicked.connect(self.on_open_image_clicked)

        # Set the layout
        self.setLayout(layout)

    def check_clear_input(self):
        
        if self.search_link_input.text() != "" and self.search_term_input.text() != "":
            self.search_button.setDisabled(False)
        else:
            self.search_button.setDisabled(True)

    def set_directory(self):
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            dotenv.set_key(".env", "IMAGE_DIRECTORY", selected_files[0])
            print("Selected File:", selected_files[0])
        self.directory_button.setText("Open Image Directory")

    def set_engine(self):
        engine = list()
        for item in self.engine_select.selectedItems():
            engine.append(item.text())
        dotenv.set_key(".env", "ENGINE", ":".join(engine))

    def set_page(self):
        page = self.pages_select.value()
        dotenv.set_key(".env", "MAX_PAGE_SEARCH", str(page))

    def on_search_clicked(self):
        search_term = self.search_term_input.text()
        search_link = self.search_link_input.text()
        print(self.engine_select.selectedItems())
        if self.engine_select.selectedItems() == []:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Selection Error: You need to select at least 1 Engine to search")
            msg.setWindowTitle("Selection Error")
            msg.exec()
        else:  
            self.searchWeb(search_term, search_link)
        
    def directory_handler(self):
        if dotenv.get_key(".env","IMAGE_DIRECTORY") == "None" or dotenv.get_key(".env","IMAGE_DIRECTORY") == "":
            self.set_directory()
        else:
            self.on_open_image_clicked()
    def on_open_image_clicked(self):
        try:
            path = dotenv.get_key(".env","IMAGE_DIRECTORY")
            open_folder(path)
        except Exception as e:
            print(e)
            open_folder(f'{os.path.expanduser("~")}\\Pictures\\SEOLookup')

    def searchWeb(self, search_term: str, search_link: str):
        print(f"Search Term: {search_term}")
        print(f"Search Link: {search_link} \n")
        results = list()
        for item in self.engine_select.selectedItems():
            search_engine = item.text()
            print(f"Doing search for {search_engine} engine")
            api.set_maxpage(str(self.pages_select.value()))
            result = WEBAPI.do_full_search(
                search_term, search_link, search_engine.lower()
            )
            results.append([search_engine, result])
        dialog = ResultDialog(f"""Results {results}""")
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(""".QLabel, .QListWidget, .QSpinBox, .QPushButton, .QLineEdit { font-size: 14pt; }
                        """)
    ex = SearchGui()
    ex.show()
    sys.exit(app.exec())
