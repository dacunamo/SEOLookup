import json
import sys
import os
import pandas as pd


WORKING_DIR = os.getcwd()
class FileHandler:
    def __init__(self):
        
        pass

    def create_file(self, file_name: str, file_type: str, file_data: str | dict):
        path = f"{WORKING_DIR}/src/{file_type}/{file_name}.{file_type}"
        print(path)
        with open(path, "w",encoding='utf-8') as outfile:
            outfile.write(str(file_data))

    def open_file(self, file_name: str, file_type: str):
        path = f"{WORKING_DIR}/src/{file_type}/{file_name}.{file_type}"

        with open(path, "r") as readfile:
            if file_type == "json":
                return json.load(readfile)
            else:
                return readfile.read()
    def resource_path(self,relative_path): #TO PROPERLY RECOGNIZE THE PATH FOR THE EXECUTABLE FILE
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base_path, relative_path)

class ExcelHandler:
    
    def __init__(self) -> None:
        pass
    def open_excel(self,file_path:str):
        data_dict = pd.read_excel(file_path,sheet_name=None)
        return data_dict
    def create_excel(self,file_name:str):
        
        pass


def testingExcel():
    e_hand = ExcelHandler()
    file = e_hand.open_excel("/home/dacunamo/SEOLookup/example files/FSA Store Wins Tracker.xlsx")
    sheet3 = file["Month 3"]
    for item in zip(sheet3['Topic'],sheet3['Type']):
        print("Searching web for:",str(item[0]).strip(),"| Type is:",item[1])

    raw_titles = "Topic	Type	Published Date	Community to Post In	Published Link	Keyword 	Estimated search volume (ahrefs)	Google Ranking	Placement	Ranking Change	Bing Ranking	Placement	Ranking Change	Notes"
    titles= raw_titles.split("\t")


    data = dict()
    data.update({"Daniel":"MORA"})
    print(sheet3.to_dict())
    df = pd.DataFrame(
        {
            "Name": ["Daniel","Juan","Pablo"],
            "Age": [25,33,31]
         }
    )
    df.to_excel("Test.xlsx",sheet_name="test",index=False)
    
    
if __name__ == "__main__":
    FH = FileHandler()
    bing_json = FH.open_file("bing_best_grounding_sheets_alternatives_page_2_result_6","json")

    for item in bing_json['organic_results']:
        print(item["link"])