"""Q6: Staircase recurrence, call counts, memoization, and iterative redesign."""

from functools import lru_cache
import sys
import time

plain_calls = 0
memo_calls = 0


def ways_plain(n: int) -> int:
    global plain_calls
    plain_calls += 1
    if n <= 2:
        return n
    return ways_plain(n - 1) + ways_plain(n - 2)


@lru_cache(maxsize=None)
def _ways_cached(n: int) -> int:
    if n <= 2:
        return n
    return _ways_cached(n - 1) + _ways_cached(n - 2)


def ways_memo(n: int) -> int:
    global memo_calls
    memo_calls += 1
    return _ways_cached(n)


def ways_loop(n: int) -> int:
    if n <= 0:
        return 0
    previous, current = 1, 2
    if n == 1:
        return previous
    for _ in range(3, n + 1):
        previous, current = current, previous + current
    return current


def timed(function, n: int) -> tuple[int, float]:
    start = time.perf_counter()
    result = function(n)
    return result, time.perf_counter() - start


def main() -> None:
    global plain_calls, memo_calls
    print("hand-check n=1..6:", [ways_loop(n) for n in range(1, 7)])
    print("plain recursive call counts")
    for n in (10, 20, 25, 30):
        plain_calls = 0
        result = ways_plain(n)
        print(f"n={n}: ways={result}, calls={plain_calls}")
    print("memoized calls (cache cleared per n)")
    for n in (10, 20, 25, 30):
        _ways_cached.cache_clear()
        memo_calls = 0
        result = ways_memo(n)
        print(f"n={n}: ways={result}, wrapper_calls={memo_calls}, "
              f"computed_states={_ways_cached.cache_info().misses}")
    print("recursion limit:", sys.getrecursionlimit())
    plain_calls = 0
    try:
        print("plain recursive n=1000:", ways_plain(1000))
    except RecursionError as error:
        print(f"plain recursive n=1000 raised: {type(error).__name__} after {plain_calls} calls")
    _ways_cached.cache_clear()
    try:
        print("memoized n=1000:", ways_memo(1000))
    except RecursionError as error:
        print("memoized n=1000 raised:", type(error).__name__)
    print("iterative n=1000 digits:", len(str(ways_loop(1000))))


if __name__ == "__main__":
    main()
