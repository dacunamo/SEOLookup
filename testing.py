import os
import platform
import sys
print(os.getcwd())
print(sys.platform)

test='HTTPSConnectionPool(host=\'serpapi.com\', port=443): ' \
'Max retries exceeded with url: ' \
'/search?currentUser=%5Bobject+Object%5D&api_key=126fb128af6a14d562d9aca48d49e90d4568485940bdae9b0fcf032619a0196a&engine=' \
'google&q=s&location=Virginia%2C+United+States&gl=us&hl=en&start=0&output=html ' \
'(Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x0000021371796710>: ' \
'Failed to resolve \'serpapi.com\' ([Errno 11001] getaddrinfo failed)"))'

result = test.split(":")[-1].split("(")[0].strip()
print(test.find("Failed to resolve") != -1)
