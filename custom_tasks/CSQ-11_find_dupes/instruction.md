# find duplicate integers

Implement `find_dupes(nums: list[int]) -> list[int]` in `/workspace/solution.py`.

**Spec:** return a sorted list of values that appear more than once. Return [] if none.


<details>
<summary>Reference tests (run against your /workspace/solution.py)</summary>

```python
        assert find_dupes([1,2,2,3,3,3]) == [2, 3] == True, 'find_dupes([1,2,2,3,3,3]) == [2, 3]'
        assert find_dupes([1,2,3]) == [] == True, 'find_dupes([1,2,3]) == []'
        assert find_dupes([5,5,5,1]) == [5] == True, 'find_dupes([5,5,5,1]) == [5]'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
