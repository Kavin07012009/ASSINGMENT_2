"""Q7: Replace recursive memoization with a constant-space iterative design."""

import statistics
import time
from functools import lru_cache


@lru_cache(maxsize=None)
def _ways_cached(n: int) -> int:
    if n <= 2:
        return n
    return _ways_cached(n - 1) + _ways_cached(n - 2)


def ways_loop(n: int) -> int:
    if n <= 0:
        return 0
    previous, current = 1, 2
    if n == 1:
        return previous
    for _ in range(3, n + 1):
        previous, current = current, previous + current
    return current


def benchmark(function, n: int, repetitions: int = 9) -> tuple[int, float, list[float]]:
    readings = []
    answer = None
    for _ in range(repetitions):
        if function is _ways_cached:
            _ways_cached.cache_clear()
        start = time.perf_counter()
        answer = function(n)
        readings.append(time.perf_counter() - start)
    return answer, statistics.median(readings), readings


def main() -> None:
    print("n,recursive_memo_median_s,iterative_median_s,answers_equal")
    for n in (10, 100, 900):
        original, old_time, old_raw = benchmark(_ways_cached, n)
        redesigned, new_time, new_raw = benchmark(ways_loop, n)
        print(f"{n},{old_time:.8f},{new_time:.8f},{original == redesigned}")
        print(f"  memo_raw={[round(x, 8) for x in old_raw]}")
        print(f"  loop_raw={[round(x, 8) for x in new_raw]}")
    answer = ways_loop(1000)
    print(f"n=1000 iterative success: digits={len(str(answer))}")


if __name__ == "__main__":
    main()
