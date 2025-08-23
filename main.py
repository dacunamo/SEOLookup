import api
import fileManagement as FM
import utils as UTILS

files = FM.FileHandler()
screenShot_util = UTILS.ScreenShot()

search_term = "best grounding sheets alternatives"
search_link="https://www.facebook.com/groups/earthinggroundingheals/posts/2948820395256425/"
LookupSearch = api.webSearch(engine="bing")
LookupSearch.webSearch(search_term)

files.create_file("myResult","html",LookupSearch.getHtmlResult())
files.create_file("myResult","json",LookupSearch.getJSONResult())

work_object = LookupSearch.getDictResult()

for result in work_object['organic_results']:
    if result['link'] == "https://www.facebook.com/dacunamo": 
        
        print(result['title'])
        print("Exact Match at position: ",result['position'])
        print("Taking screenshot.")
        screenShot_util.take_screenshot(search_term,f"/src/html/myResult.html")
      
    
#print(work_object['organic_results']) # type: ignore