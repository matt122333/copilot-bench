def work():
    return 7
def main():
    for i in range(3):
        print(f'DEBUG step {i}')
    r = work()
    print(f'computed={r}')
    print('PIPELINE DONE')
main()
