import os
import dotenv
from dotenv import load_dotenv
import fileManagement as FM
import utils as UTILS

files = FM.FileHandler()
screenShot_util = UTILS.ScreenShot()

import serpapi
import json
load_dotenv()
API_KEY = os.getenv("API_KEY")
#API_KEY = "126fb128af6a14d562d9aca48d49e90d4568485940bdae9b0fcf032619a0196a"
MAX_PAGE_SEARCH = os.getenv("MAX_PAGE_SEARCH")

class Parameter:
    search_parameter: str
    language: str
    country: str
    engine: str
    parameters = {
        "api_key": API_KEY,
        "engine": "engine",
        "q": "search_query",
        "location": "Virginia, United States",
        "output": "html",
    }

    def __init__(self, param: str, engine: str, language: str, country: str) -> None:
        self.search_parameter = param
        self.engine = engine
        self.country = country
        self.language = language

        self.parameters["engine"] = self.engine
        self.parameters["q"] = self.search_parameter

        if engine == "google":
            self.googleParams()

    def googleParams(self):
        self.parameters["start"] = "0"
        self.parameters["gl"] = self.country
        self.parameters["hl"] = self.language

    def getParams(self):
        return self.parameters


class webSearch:
    google_pages = ("0", "10", "20", "30", "40","50", "60","70")
    bing_pages = ("1","11","21","31","41","51","61","71")
    FOUND_POSITION:int
    FOUND_PAGE:int
    def __init__(
        self, engine: str = "google", language: str = "en", country: str = "us"
    ):
        self.engine = engine
        self.language = language
        self.country = country
        self.search_page = 0

    def test_search(self, search_parameter: str = "", page: int = 0):
        self.search_page = page
        print(f"Looking for: {search_parameter} on page {self.google_pages[page-1]}")

    def do_full_search(self, search_parameter: str = "", link: str = "",engine:str = "google"):
        page = 0
        self.link = link
        try:
            self.webSearch(search_parameter,page,engine)
            print(MAX_PAGE_SEARCH)
            while page < int(MAX_PAGE_SEARCH):
                if self.wasFound()[0] == True:
                    self.FOUND_POSITION = self.wasFound()[1]
                    self.FOUND_PAGE = page+1
                    print(f"Found on page {self.FOUND_PAGE} at position {self.FOUND_POSITION}\n")

                    term = search_parameter.replace(" ","_")
                    filename = f"{self.engine}_{term}_page_{self.FOUND_PAGE}_result_{self.FOUND_POSITION}"
                    files.create_file(filename, "html", self.getHtmlResult())
                    files.create_file(filename, "json", self.getJSONResult())
                    screenShot_util.take_screenshot(
                        filename, f"/src/html/{filename}.html"
                    )
                    return [self.FOUND_PAGE,self.FOUND_POSITION]
                else:
                    print(f"Not found in the first {page+1} pages.")
                page += 1
                self.webSearch(search_parameter, page, engine)
        except Exception as e:

            print("There was an error connecting to the API, check internet connection")
            print(e)

    def webSearch(self, search_parameter: str = "", page: int = 0, engine: str = "google"):
        self.engine = engine
        self.search_parameter = search_parameter

        ##BING
        engine = self.engine
        bing_params = {
            "api_key": API_KEY,
            "engine": "bing",
            "q": self.search_parameter,
            "hl": self.language,
            "gl": self.country,
            "location": "Virginia, United States",
            "cc": "US",
            "first": self.bing_pages[page],
            "output": "html"
        }
        ##GOOGLE
        google_params = {
            "currentUser": "[object Object]",
            "api_key": API_KEY,
            "engine": "google",
            "q": self.search_parameter,
            "location": "Virginia, United States",
            "gl": "us",
            "hl": "en",
            "start": self.google_pages[page],
            "output": 'html'
        }
        
        print(f"Doing search on page {page+1}")
        if engine.lower() == "google":
            self.searchResult = serpapi.search(google_params)
            self.html_output = self.searchResult
            #Setup the output to json to get the readable data in JSON format, working as a dict
            google_params["output"]="json"
            self.searchResult = serpapi.search(google_params)
            self.json_output = self.searchResult
            
        elif engine.lower() == "bing":
            self.searchResult = serpapi.search(bing_params)
            self.html_output = self.searchResult
            #Setup the output to json to get the readable data in JSON format, working as a dict
            bing_params["output"]="json"
            self.searchResult = serpapi.search(bing_params)
            self.json_output = self.searchResult

        
    def getHtmlResult(self):
        return self.html_output

    def getJSONResult(self):
        data = json.dumps(self.json_output.as_dict(), indent=2)
        return data

    def getDictResult(self):
        return self.searchResult.as_dict()

    def wasFound(self):
        for item in self.getDictResult()["organic_results"]:
            print(item["link"])
            if item["link"] == self.link:
                return [True,item['position']]
        return [False,0]

    def set_engine(self, engine: str):
        self.engine = engine

    def set_language(self, language: str):
        self.language = language

    def set_country(self, country: str):
        self.country = country

    def nextPage(self):
        # code to set parameters to the next page
        # search on the new page
        self.search_page += 1
        pass


if __name__ == "__main__":
    ws = webSearch()
    term = "best grounding sheets alternatives"
    searchLink = "https://www.facebook.com/groups/earthinggroundingheals/posts/2948820395256425/"
    ws.do_full_search(term, searchLink)
    """     #pages = ["0","10","20","30","40"]
    pages = (0,1,2,3,4)
    for page in pages:
        ws.webSearch(term,page,searchLink)
        files.create_file(f"{ws.engine}_{term}_page_{page}", "html", ws.getHtmlResult())
        files.create_file(f"{ws.engine}_{term}_page_{page}", "json", ws.getJSONResult()) """
    # ws.webSearch(term)

    # result = ws.getDictResult()
    # print(result)
