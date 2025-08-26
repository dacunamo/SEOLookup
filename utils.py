from imports import *
# ─────────────────────────────
# Web Automation (Selenium)
# ─────────────────────────────
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.edge.service import Service as EService
from selenium.webdriver.edge.options import Options as EOptions
# ─────────────────────────────
# File Handling
# ─────────────────────────────
import fileManagement as FM

SYSTEM = sys.platform
WORK_DIR = os.getcwd()
LINUX_CHROME_DRIVER = f'{WORK_DIR}/src/resources/chromedriver-linux64/chromedriver'
WIN_EDGE_DRIVER = f"{WORK_DIR}\\src\\resources\\edgedriver\\msedgedriver.exe"

fileHandler = FM.FileHandler()
FM.create_folders()

def get_correctPath(path):
    return fileHandler.resource_path(path)

def calculate_html_height(filename:str=""):
    HTML_FILE_PATH = f'src/html/{filename}.html'
    REALPATH = get_correctPath(HTML_FILE_PATH)
    FIXED_WIDTH = 1080
    HEIGHT = 0
    
    if SYSTEM =="linux":
    # --- Setup Headless Chrome for Linux---
        chrome_options = COptions()
        print(WORK_DIR)
        chrome_options.binary_location = f"{WORK_DIR}/src/resources/chromiumbin/chromedriver_linux64/chrome-linux64/chrome"
        chrome_options.add_argument("--headless")  # Run without a visible browser window
        chrome_options.add_argument(f"--window-size={FIXED_WIDTH},5000") # Width is fixed, height is temporary
        chrome_service = CService(executable_path=LINUX_CHROME_DRIVER)
        driver = webdriver.Chrome(service=chrome_service,options=chrome_options)
        
    elif SYSTEM =="win32":
        # --- Setup Headless Edge for Windows---
        edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        edge_options = EOptions()
        edge_options.binary_location = edge_path
        edge_options.add_argument("--headless")
        edge_options.add_argument(f"--window-size={FIXED_WIDTH},5000")
        edge_options.use_chromium = True  # Required for Chromium-based Edge
        # Create service and driver
        service = EService(executable_path=WIN_EDGE_DRIVER)
        driver = webdriver.Edge(service=service,options=edge_options)
    try:
        # Get the full, absolute path to the HTML file
        full_path = os.path.abspath(HTML_FILE_PATH)
        print(full_path)
        
        # Load the local HTML file
        driver.get(f"file:///{full_path}")

        # Use JavaScript to get the full scrollable height of the page
        # This is the most reliable way to measure the rendered content
        if filename.split("_")[0] == "google":
            height = driver.execute_script("""return document.getElementById('rcnt').offsetHeight
                                       """)
        elif filename.split("_")[0] == "bing":
            height = driver.execute_script("""return document.getElementById('b_content').offsetHeight
                                       """)
        print(f"HTML file: {HTML_FILE_PATH}")
        print(f"Calculated height: {height+350}px")
        HEIGHT = height+350
    finally:
        # Clean up and close the browser
        driver.quit()
    """_summary_

    Returns:
        _type_: _description_
    """
    return HEIGHT 
         

class ScreenShot():
    
    def highlight_html(self,raw_html:str,highlight_text:str,engine:str):
        """Function to highlight the text of the raw html that will be used later as a screenshot candidate

        Args:
            raw_html (str): Raw html input from an API response.
            highlight_text (str): Text to be highlighted, due to multiple occurencies this function will check for the text
            contained in labels ...> highlight_text <...
            engine (str): depending on the engine the HTML format may vary. 

        Returns:
            new_html (str): Highlighted html for file creation
        """
        if engine == "google":
            # Use word boundaries (\b) and ensure we don't break inside tags
            # Matches >text< and replaces with ><mark>text</mark><
            escaped_text = re.escape(highlight_text)
            pattern = f'>([^<]*?{escaped_text}[^<]*)<'
            replacement = r'><mark>\1</mark><'
            new_html = re.sub(pattern, replacement, raw_html)
        return new_html  # type: ignore

    def take_screenshot(self,file_name:str,html_source:str):
        """Take a screenshot of a local HTML file

        Args:
            file_name (str): String of the filename
            html_source (str): Relative path of the html file, in this code located at src/html
        """
        w_widht = 1080
        w_height = calculate_html_height(file_name)
        size = f"{w_widht},{w_height}"
        chromebinary_path = f"{WORK_DIR}/src/resources/chromiumbin/chromedriver_linux64/chrome-linux64/chrome"
        edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        html_file = f"file://{WORK_DIR}{str(html_source)}"
        pictures_path = FM.get_pictures_path()
        
        if SYSTEM == "linux":
            screenshot_fullpath = os.path.join(pictures_path,f"{file_name}.png")
            #screenshot_fullpath = os.path.join(os.path.expanduser("~"),"Pictures","SEOLookup",f"{file_name}.png")
            script = f"{chromebinary_path} --headless --disable-gpu --screenshot='{screenshot_fullpath}' --hide-scrollbars --window-size={size} '{html_file}'"

        elif SYSTEM =="win32":
            screenshot_fullpath = os.path.join(pictures_path,f"{file_name}.png")
            #screenshot_fullpath = os.path.join(os.path.expanduser("~"),"Pictures","SEOLookup",f"{file_name}.png")
            script = f'"{edge_path}" --headless --disable-gpu --screenshot="{screenshot_fullpath}" --hide-scrollbars --window-size={size} "{html_file}"'

        subprocess.run(script,shell=True)
if __name__ == "__main__":
    sc = ScreenShot()
    sc.take_screenshot("google_car_rental_page_2_result_4",f"\src\html\\google_car_rental_page_2_result_4.html")