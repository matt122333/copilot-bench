import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    semver_compare = ns['semver_compare']
    assert (semver_compare("1.2.3", "1.2.3")) == 0, 'semver_compare("1.2.3", "1.2.3")'
    assert (semver_compare("2.0.0", "1.9.9")) == 1, 'semver_compare("2.0.0", "1.9.9")'
    assert (semver_compare("1.0.0", "1.0.1")) == -1, 'semver_compare("1.0.0", "1.0.1")'
    assert (semver_compare("1.10.0", "1.9.0")) == 1, 'semver_compare("1.10.0", "1.9.0")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
