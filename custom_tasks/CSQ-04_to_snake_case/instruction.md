# snake_case converter

Implement `to_snake_case(s: str) -> str` in `/workspace/solution.py`.

**Spec:** convert `camelCase` / `PascalCase` / hyphen-space-delimited strings to
`snake_case`. Lowercase result. Examples: 'HelloWorld'->'hello_world',
'fooBar'->'foo_bar', 'a-b'->'a_b', '  X Y  '->'x_y'.


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (to_snake_case("HelloWorld")) == "hello_world", 'to_snake_case("HelloWorld")'
        assert (to_snake_case("fooBar")) == "foo_bar", 'to_snake_case("fooBar")'
        assert (to_snake_case("a-b")) == "a_b", 'to_snake_case("a-b")'
        assert (to_snake_case("X Y")) == "x_y", 'to_snake_case("X Y")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
