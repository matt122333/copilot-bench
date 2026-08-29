import argparse
p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['tokenize','stats'], default='tokenize')
p.add_argument('args', nargs='*')
a = p.parse_args()
if a.mode == 'tokenize':
    print(','.join(a.args[0].split() if a.args else []))
else:
    print(sum(int(x) for x in a.args))
