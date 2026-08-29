import argparse
p = argparse.ArgumentParser()
sub = p.add_subparsers(dest='cmd', required=True)
sub.add_parser('tokenize').add_argument('text')
s = sub.add_parser('stats'); s.add_argument('nums', type=int, nargs='+')
a = p.parse_args()
if a.cmd == 'tokenize':
    print(','.join(a.text.split()))
else:
    print(sum(a.nums))
