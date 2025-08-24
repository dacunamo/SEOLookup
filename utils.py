import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import fileManagement as FM

SYSTEM = sys.platform
WORK_DIR = os.getcwd()
LINUX_CHROME_DRIVER = f'{WORK_DIR}/src/resources/chromedriver-linux64/chromedriver'
WIN_EDGE_DRIVER = f"{WORK_DIR}\\src\\resources\\edgedriver\\msedgedriver.exe"

fileHandler = FM.FileHandler()
def get_correctPath(path):
    return fileHandler.resource_path(path)

def calculate_html_height(filename:str=""):
    HTML_FILE_PATH = f'src/html/{filename}.html'
    REALPATH = get_correctPath(HTML_FILE_PATH)
    FIXED_WIDTH = 1080
    HEIGHT = 0

    if SYSTEM =="linux":
    # --- Setup Headless Chrome for Linux---
        chrome_options = Options()
        chrome_options.binary_location = f"{WORK_DIR}/src/resources/chromiumbin/chromedriver_linux64/chrome-linux64/chrome"
        chrome_options.add_argument("--headless")  # Run without a visible browser window
        chrome_options.add_argument(f"--window-size={FIXED_WIDTH},5000") # Width is fixed, height is temporary
        service = Service(executable_path=LINUX_CHROME_DRIVER)
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif SYSTEM =="win32":
        # --- Setup Headless Edge for Windows---
        edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        options = Options()
        options.binary_location = edge_path
        options.add_argument("--headless")
        options.add_argument(f"--window-size={FIXED_WIDTH},5000")
        options.use_chromium = True  # Required for Chromium-based Edge
        # Create service and driver
        service = Service(executable_path=WIN_EDGE_DRIVER)
        driver = webdriver.Edge(service=service,options=options)
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
    return HEIGHT             

class ScreenShot():
    try:    
        print("Trying to create Pictures\\SEOLookup Directory")
        path = f'{os.path.expanduser("~")}\\Pictures\\SEOLookup'
        if SYSTEM == "win32": 
            os.mkdir(path)
        elif SYSTEM == "linux":
            os.mkdir(path.replace('\\',"/"))
    except Exception as e:
        print(e)
        print("Directory already exists\n")
    def highlight_html(self,raw_html:str,highlight_text:str,engine:str):
        if engine == "google":
            print(f"Replacing {highlight_text}")
            raw_html.replace(f">{highlight_text}<",f"><mark>{highlight_text}</mark><")
        return raw_html

    def take_screenshot(self,file_name:str,html_source:str):
        w_widht = 1080
        w_height = calculate_html_height(file_name)
        size = f"{w_widht},{w_height}"
        chromebinary_path = f"{WORK_DIR}\\src\\resources\\chromiumbin\\chromedriver_linux64\\chrome-linux64\\chrome"
        edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        html_file = f"file://{WORK_DIR}{str(html_source)}"
        
        if SYSTEM == "linux":
            screenshot_fullpath = f"{WORK_DIR}/src/screenshots/{file_name}.png"
            script = f"{chromebinary_path} --headless --disable-gpu --screenshot='{screenshot_fullpath}' --hide-scrollbars --window-size={size} '{html_file}'"
            with open(f"{WORK_DIR}/src/screenshot.sh","w") as scriptFile:
                scriptFile.write(script) 
            subprocess.call(f'chmod +x {WORK_DIR}/src/screenshot.sh && {WORK_DIR}/src/screenshot.sh',shell=True) 

        elif SYSTEM =="win32":
            screenshot_fullpath = os.path.join(os.path.expanduser("~"),"Pictures","SEOLookup",f"{file_name}.png")
            script = f'"{edge_path}" --headless --disable-gpu --screenshot="{screenshot_fullpath}" --hide-scrollbars --window-size={size} "{html_file}"'
            with open(f"{WORK_DIR}\\src\\screenshot.bat","w") as scriptFile:
                scriptFile.write(script) 
            
            script_path = os.path.join(WORK_DIR, "src", "screenshot.bat")
            #subprocess.call(['cmd', "/c",script_path])
            subprocess.run(f'cmd /c "{script_path}"', shell=True)

if __name__ == "__main__":
    sc = ScreenShot()
    #height = calculate_html_height("google_best_grounding_sheets_alternatives_page_1")
    sc.take_screenshot("bing_best_grounding_sheets_alternatives_page_2_result_6",f"\src\html\\bing_best_grounding_sheets_alternatives_page_2_result_6.html")
    #sc.windows_screenshot()