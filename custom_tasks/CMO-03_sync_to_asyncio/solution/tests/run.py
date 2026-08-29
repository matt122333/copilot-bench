import sys, os, time
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from fetcher import main
urls = ['a','b','c']
t0=time.time()
results = main(urls)
t=time.time()-t0
assert results == ['ok','ok','ok'], results
assert t < 0.35, f'should be concurrent, took {t:.2f}s'
print('ASYNC_OK')
