from imports import *

SYSTEM = sys.platform
WEBAPI = api.webSearch()

def open_folder(folder_path:str = ""):
        path =  folder_path
        if SYSTEM == "win32":
            os.startfile(path) # type: ignore
        elif SYSTEM == "linux":
            subprocess.call(["xdg-open", folder_path.replace("\\","/")])

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
        self.setWindowTitle('SEOLookup Beta1')
        self.setGeometry(100, 100, 400, 250)

        # Layout
        layout = QVBoxLayout()
        options_layout = QHBoxLayout()

        # Page Selection
        self.pages_select = QSpinBox()
        self.pages_select.setValue(int(dotenv.get_key(".env","MAX_PAGE_SEARCH"))) # type: ignore
        
        # Engine Selection
        self.engine_select = QListWidget()
        self.engine_select.addItems(["Google","Bing"]) 

        # Preselecting google as engine
        item = self.engine_select.item(0)
        item.setSelected(True) # type: ignore
        self.engine_select.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.engine_select.setFixedHeight(50)

        options_layout.addWidget(QLabel("Pages to search"))
        options_layout.addWidget(self.pages_select)
        options_layout.addWidget(QLabel("Engine to use"))
        options_layout.addWidget(self.engine_select)
        layout.addLayout(options_layout)
        
        # Input fields
        self.search_term_input = QLineEdit()
        self.search_link_input = QLineEdit()
        layout.addWidget(QLabel("Search Term"))
        layout.addWidget(self.search_term_input)
        layout.addWidget(QLabel("Search Link"))
        layout.addWidget(self.search_link_input)

        # Buttons
        self.search_button = QPushButton('Search')
        self.open_image_button = QPushButton('Open Image')
        layout.addWidget(self.search_button)
        layout.addWidget(self.open_image_button)

        # Connect signals and slots
        self.pages_select.valueChanged.connect(self.set_page)
        self.engine_select.itemSelectionChanged.connect(self.set_engine)
        self.search_button.clicked.connect(self.on_search_clicked)
        self.open_image_button.clicked.connect(self.on_open_image_clicked)

        # Set the layout
        self.setLayout(layout)

    def set_engine(self):
        engine = list()
        for item in self.engine_select.selectedItems():
            engine.append(item.text())
        dotenv.set_key(".env","ENGINE",":".join(engine))
    
    def set_page(self):
        page=self.pages_select.value()
        dotenv.set_key(".env","MAX_PAGE_SEARCH",str(page))

    def on_search_clicked(self):
        search_term = self.search_term_input.text()
        search_link = self.search_link_input.text()
        self.searchWeb(search_term,search_link)

    def on_open_image_clicked(self):
        open_folder(f'{os.path.expanduser("~")}\\Pictures\\SEOLookup')
    
    def searchWeb(self,search_term:str,search_link:str):
        print(f"Search Term: {search_term}")
        print(f"Search Link: {search_link} \n")
        results = list()
        for item in self.engine_select.selectedItems():
            search_engine = item.text()
            print(f"Doing search for {search_engine} engine")
            api.set_maxpage(str(self.pages_select.value()))
            result = WEBAPI.do_full_search(search_term,search_link,search_engine.lower())
            results.append([search_engine,result])
        dialog = ResultDialog(f"""Results {results}""")
        dialog.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchGui()
    ex.show()
    sys.exit(app.exec())

        