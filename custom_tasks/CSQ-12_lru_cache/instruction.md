# LRU cache simulation

Implement `lru(capacity: int, ops: list[tuple]) -> list` in `/workspace/solution.py`.

**Spec:** simulate an LRU cache. Each op is `("get", key)` or `("put", key, value)`.
`get` returns the value or -1 and marks used; `put` evicts the least-recently-used
key when over capacity. Return the list of get results in order.


<details>
<summary>Reference tests (run against your /workspace/solution.py)</summary>

```python
        assert lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3] == True, 'lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3]'
        assert lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2] == True, 'lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2]'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
