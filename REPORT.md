# Python Programming Assignment 2 CO2

**Student:** [Enter full name]  
**Register number:** [Enter register number]  
**GitHub repository:** [Paste `https://github.com/...` here]  
**Python used for execution evidence:** Python 3.14.7  
**Libraries:** Python standard library only

## Submission note

This report accompanies the seven runnable Python task folders. Replace the student and repository placeholders on this page and in `README.md` before submitting. The GitHub repository must be created and shared by the student, and the course requires screenshots of code execution and output in the task folders.

## Q1 Decisions with many boundaries

### Predictions before execution

| Units | Ration card | Member over 80 | Predicted exclusive decision |
|---:|:---:|:---:|---|
| 99 | No | No | Full subsidy |
| 100 | Yes | No | Full subsidy |
| 101 | No | No | No subsidy |
| 101 | Yes | No | Partial subsidy |
| 199 | Yes | No | Partial subsidy |
| 200 | No | No | No subsidy |
| 201 | No | No | No subsidy |
| 201 | No | Yes | Senior exception subsidy |

### Implementations and observations

`Q1/subsidy.py` implements the intended decision as an exclusive `if`/`elif`/`else`, and also provides match-case and an upper-limit lookup. The separate-if version intentionally uses a broad second condition (`units <= 200 and ration_card`). At 100 units with a ration card it returns both full and partial subsidy. The exclusive chain stops at the first true branch and returns exactly one decision. Boundary observations at 100, 101, 200, and 201 match the prediction table.

Combined Boolean conditions are clearest here: each slab is explicit, and `101 <= units <= 200` shows both bounds directly. Nesting would add indentation without reducing complexity. The final decision should keep age as an exception above 200 so it cannot accidentally override the low-use rule.

### Alternative and complexity

For k slabs, a direct if/elif or match-case decision has O(k) worst-case checks and O(1) auxiliary space. A sequential lookup over `(upper_limit, decision)` pairs also takes O(k) worst case and O(k) space for its table (or O(1) extra space if the table is pre-existing). Match-case guards can express the same decision, although numeric ranges require guards rather than a compact range pattern. See `match_decision` and `lookup_decision` in the program.

## Q2 Loops that count attempts

`Q2/otp_attempts.py` includes a while loop and a `for range(3)` loop. Blank input uses `continue` before increasing the attempt count. A correct OTP uses `break`. The `for` loop's `else` executes only when the loop completes without `break`, so it locks after three counted wrong OTPs. `pass` is shown as a deliberate no-op placeholder in an empty policy branch; it is not needed for the verification algorithm itself.

A while loop is natural when the number of attempts can change while the loop runs, such as granting two more tries after a security check. A fixed `for` loop is simpler for exactly three counted iterations. Incrementing the counter before checking for a blank input causes blank submissions to consume attempts; incrementing it only on wrong answers without a separate success break can allow too many attempts. Updating the counter in the wrong place can also skip the limit or loop forever.

The changed-condition demonstration grants two additional attempts after three failures when the answer is `blue`. A recursive version is also included; each attempt calls the function for the next input. All versions use O(a) time for a attempts. Loops use O(1) auxiliary space; the recursive form uses O(a) call-stack space and is less suitable for a small, stateful kiosk workflow.

## Q3 Vehicle registration validator

### Predictions before execution

| Input | Predicted normalized form | Predicted result |
|---|---|---|
| `tn 09 ab 1234` | `TN09AB1234` | Valid; `TN 09 AB 1234` |
| `TN-09-AB-1234` | `TN09AB1234` | Valid; `TN 09 AB 1234` |
| `Tn09Ab1234` | `TN09AB1234` | Valid; `TN 09 AB 1234` |
| `MH 12 C 9876` | `MH12C9876` | Valid; `MH 12 C 9876` |
| `A 09 AB 1234` | `A09AB1234` | Rejected: state code is not two letters |
| `TN-9-AB-1234` | `TN9AB1234` | Rejected: district is not two digits |

`normalize`, `is_valid`, and `receipt_format` perform normalization, structural validation, and display formatting using string operations and slicing; no regular expressions are used. The observed results match the predictions. The validator accepts 9-character values with a one-letter series or 10-character values with a two-letter series. Python strings are immutable: operations such as `upper()` return a new string and leave the original unchanged, so the returned value must be assigned if it is to be kept. For `TN09A1234`, `s[-4:]` is `1234` and `s[4:-4]` is `A`; for `TN09AB1234`, the same slices return `1234` and `AB`.

A `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)` alternative takes O(L) time in input length L and O(1) auxiliary space for this fixed pattern. Regex is concise for a compact format; explicit slicing makes each field boundary visible and can be easier for a beginner to debug. Both approaches need separate normalization and receipt formatting.

## Q4 Building long text

Three implementations were timed with `time.perf_counter()`, three repetitions each, for 1,000, 10,000, and 200,000 lines. Each produced the same output length; the implementations also compare equal at 1,000 lines. The table reports measured means from this machine; the raw three readings are in `evidence/Q4_benchmarks.csv`.

| Lines | Repeated `+=` mean (s) | List + `join` mean (s) | f-string parts + `join` mean (s) |
|---:|---:|---:|---:|
| 1,000 | 0.000070 | 0.000054 | 0.000050 |
| 10,000 | 0.000673 | 0.000526 | 0.000510 |
| 200,000 | 0.013747 | 0.011616 | 0.010955 |

Before timing, I expected `join` to have the clearest advantage because it can allocate the final string once. It was fastest at all three sizes here, but the gap was modest. Although strings are immutable and repeated concatenation can copy accumulated content, CPython can optimize local `+=` loops; therefore these measurements do not show the worst-case quadratic behavior. `join` remains a predictable choice when all parts are available. A file stream or `io.StringIO` can avoid retaining every line as an intermediate list; streaming uses bounded buffering, while `StringIO` keeps the built text in memory. `join` takes O(total output characters) time and O(total output size) memory. Repeated `+=` can copy up to O(n²) characters in a non-optimized implementation. These benchmarks are machine- and interpreter-specific.

## Q5 Functions, parameters, and scope

The bug is that `order=[]` is evaluated once when `add_item_buggy` is defined. Calls without an explicit order mutate that same list, so the second customer sees the first customer's item. The run prints `add_item_buggy.__defaults__` as `(['tea', 'sandwich'],)`, which is direct evidence that the default list persists. The correction uses `None` and creates a new list inside each call. The three corrected customers each receive an independent order.

Use positional arguments for simple required values, keyword arguments when they improve clarity or select optional behavior, and defaults for safe immutable options such as a GST rate. `price_order` returns a tuple containing the total and GST. The scope demonstration increments a module-level counter with `global`; local names exist in a function; `nonlocal` lets an inner function rebind a name from its enclosing function. `global` is needed for rebinding a module-level name because assignment otherwise makes it local. Passing state explicitly is usually easier to test and reason about than changing globals.

An explicit-list design has O(1) append time per item and O(m) storage for m items belonging to that customer. A closure can keep the order list private and expose an `add` function; it still uses O(m) storage, but the state is less directly visible to callers. Both are preferable to a shared mutable default when the intended ownership of the order is clear.

## Q6 Recursion and its limits

The recurrence is `ways(n) = ways(n - 1) + ways(n - 2)`, with base cases `ways(1)=1` and `ways(2)=2`. Hand calculation gives n=1..6: **1, 2, 3, 5, 8, 13**. The plain recursive call tree for n=5 repeats subproblems:

```text
ways(5)
├── ways(4)
│   ├── ways(3)
│   │   ├── ways(2)
│   │   └── ways(1)
│   └── ways(2)
└── ways(3)
    ├── ways(2)
    └── ways(1)
```

The plain recursive version makes exponentially many calls (O(phi^n)); memoization computes each state once, giving O(n) recurrence states and O(n) cache plus call-stack space. The captured counts are:

| n | Plain recursive calls | Memoized computed states |
|---:|---:|---:|
| 10 | 109 | 10 |
| 20 | 13,529 | 20 |
| 25 | 150,049 | 25 |
| 30 | 1,664,079 | 30 |

On the captured Python 3.14.7 runtime, `sys.getrecursionlimit()` is 1,000. Both plain recursion and a fresh `ways_memo(1000)` raise `RecursionError` because the recursive dependency chain approaches the interpreter's recursion limit. The exponential plain version also does vastly more work before reaching that depth. Raising the limit is not the preferred deployment fix: a higher limit increases stack risk and remains finite. The iterative two-value version avoids recursive calls and succeeds for n=1,000; it uses O(n) recurrence steps and O(1) auxiliary values. The result has 209 digits. The ordinary Big-O count treats integer addition as constant cost; because Python integers grow with n, actual bit-level arithmetic costs more as n increases.

## Q7 Diagnose, redesign, and validate

### A–D. Diagnosis, objective, design, and prediction

The selected limitation is the recursive depth of memoized staircase counting. Memoization removes repeated calculations, but the dependency chain still grows linearly with n. At n=1,000, the fresh memoized call fails at the configured recursion limit. The objective is to compute the identical answer for n=1,000 without changing the recursion limit and while using O(1) auxiliary storage.

The redesign exploits the recurrence's dependency on only the previous two values. It retains two integers and updates them once per step; it removes the dictionary cache and the call stack. The trade-off is that intermediate states cannot be inspected later or reused for a different nearby query. Pseudocode: set previous=1 and current=2; repeat for step 3 through n: set previous,current=current,previous+current; return current.

Before implementing, I predicted both designs would return the same result and the iterative version would use less memory and less time because it avoids cache lookups and Python function calls. The validation compares both on identical n values, using nine trials and median elapsed time.

### E–F. Measured comparison and defense

| n | Memoized recursive median (s) | Iterative median (s) | Same result? |
|---:|---:|---:|:---:|
| 10 | 0.00000054 | 0.00000013 | Yes |
| 100 | 0.00000658 | 0.00000133 | Yes |
| 900 | 0.00009325 | 0.00001592 | Yes |

At n=900, the iterative version was about 5.9 times faster in this run. It also computed n=1,000 successfully, where the fresh recursive memoized call raised `RecursionError`. The objective was achieved. Both algorithms perform O(n) recurrence steps; recursion uses O(n) cache and call-stack space, while the iterative redesign uses O(1) auxiliary space. Timing at very small sizes is noisy and all measurements depend on the hardware and Python build. Memoized recursion remains useful for teaching the recurrence and for workloads that repeatedly query shared subproblems; the loop is the better deployment choice for a single large staircase count.

## Files and execution evidence

The seven task programs are under `Q1` through `Q7`. Raw output and timing records are in `evidence/`. All programs use only the standard library. Add the requested execution screenshots to the task folders and insert the actual repository URL before uploading to SIMATS Online Programming Lab Portal and Google Classroom.
