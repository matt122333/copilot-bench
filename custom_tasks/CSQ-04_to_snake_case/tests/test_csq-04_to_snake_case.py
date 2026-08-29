import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    to_snake_case = ns['to_snake_case']
    assert (to_snake_case("HelloWorld")) == "hello_world", 'to_snake_case("HelloWorld")'
    assert (to_snake_case("fooBar")) == "foo_bar", 'to_snake_case("fooBar")'
    assert (to_snake_case("a-b")) == "a_b", 'to_snake_case("a-b")'
    assert (to_snake_case("X Y")) == "x_y", 'to_snake_case("X Y")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
