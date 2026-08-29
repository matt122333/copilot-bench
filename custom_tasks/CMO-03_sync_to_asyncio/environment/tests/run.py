import sys, os, time
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from fetcher import main
urls = ['a','b','c']
results = main(urls)
assert results == ['ok','ok','ok'], results
print('ASYNC_OK')
