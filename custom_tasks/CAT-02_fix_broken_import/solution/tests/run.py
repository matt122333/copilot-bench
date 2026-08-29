import sys, os
sys.path.insert(0, os.getcwd())
import pkg
assert pkg.greet('Ada') == 'Hello, Ada!'
print('OK')
