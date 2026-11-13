"""Q4: Compare repeated concatenation, list+join, and f-string line creation."""

import statistics
import time


def build_plus(n: int) -> str:
    statement = ""
    for i in range(n):
        statement += f"SMS {i + 1}: charge 1.00\n"
    return statement


def build_join(n: int) -> str:
    parts = []
    for i in range(n):
        parts.append(f"SMS {i + 1}: charge 1.00\n")
    return "".join(parts)


def build_fstring_parts(n: int) -> str:
    parts = [f"SMS {i + 1}: charge 1.00\n" for i in range(n)]
    return "".join(parts)


def time_call(function, n: int, repeats: int = 3) -> tuple[float, list[float], int]:
    readings = []
    length = 0
    for _ in range(repeats):
        start = time.perf_counter()
        result = function(n)
        readings.append(time.perf_counter() - start)
        length = len(result)
    return statistics.mean(readings), readings, length


def main() -> None:
    print("n,method,seconds_mean,raw_seconds,characters")
    for n in (1_000, 10_000, 200_000):
        for label, function in (("plus", build_plus), ("list_join", build_join),
                                ("fstring_list_join", build_fstring_parts)):
            mean, raw, length = time_call(function, n)
            print(f"{n},{label},{mean:.6f},{[round(x, 6) for x in raw]},{length}")
    print("all outputs equal at 1000:",
          build_plus(1000) == build_join(1000) == build_fstring_parts(1000))


if __name__ == "__main__":
    main()
