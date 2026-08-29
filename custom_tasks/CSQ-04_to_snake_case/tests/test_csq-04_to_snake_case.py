import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    to_snake_case = ns['to_snake_case']
    assert to_snake_case("HelloWorld") == "hello_world", 'to_snake_case("HelloWorld")'
    assert to_snake_case("fooBar") == "foo_bar", 'to_snake_case("fooBar")'
    assert to_snake_case("a-b") == "a_b", 'to_snake_case("a-b")'
    assert to_snake_case("X Y") == "x_y", 'to_snake_case("X Y")'
