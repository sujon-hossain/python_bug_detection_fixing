# Step-by-Step: How to Solve This Project by Debugging

Spoiler notice: the worked examples in Part 3 solve bugs 1, 2, 5, 4 and 26. Skip Part 3 if you want to find
those yourself, and use only Parts 1 and 2.

---

## Part 1: The method (use it for every bug)

### Step 1: Take a baseline
```bash
python progress.py -v
```
Note how many tests fail (about 67). Your goal is 0. Every fix should lower the number and never raise it.

### Step 2: Pick ONE failing test, earliest pipeline stage first
The calculator is a pipeline: `tokenizer -> parser -> evaluator -> functions -> calculator -> cli`.
A bug early in the pipeline makes later tests fail for the wrong reason, so fix in this order:

1. `test_tokenizer`
2. `test_parser`
3. `test_evaluator`, `test_functions`
4. `test_memory`, `test_history`, `test_converter`, `test_bases`, `test_stats`
5. `test_calculator`, `test_cli` (last, they use everything)

### Step 3: Run only that test and read the failure
```bash
python -m unittest tests.test_parser.ParserTests.test_subtraction_is_left_associative
```
Read it bottom-up:
- Last line = what went wrong (`AssertionError: 4.0 != 1` means actual vs expected)
- Line above = which line of YOUR code or the test failed
- Is it an **AssertionError** (wrong answer) or an **exception** such as `ValueError` / `KeyError` (a crash)?

### Step 4: Reproduce it in 1 line, outside the tests
```bash
python -c "from calculator.parser import parse; print(parse('8/4/2'))"
```
A tiny reproduction removes all noise.

### Step 5: Find the FIRST stage that goes wrong
Print each stage. The first wrong output is where the bug lives.
```bash
python -c "
from calculator.tokenizer import tokenize
from calculator.parser import parse
from calculator.evaluator import evaluate
from calculator.environment import Environment
t = '2^3^2'
print(tokenize(t)); n = parse(t); print(n); print(evaluate(n, Environment()))"
```

### Step 6: Write a hypothesis, then test it
Write one sentence: "I think X is wrong because Y." Then prove or disprove it with a print or the debugger.
Change **one thing at a time**. If you change three things and it works, you do not know which one fixed it.

### Step 7: Fix, re-run, then run EVERYTHING
```bash
python -m unittest tests.test_parser      # the file you worked on
python progress.py                        # nothing else broke, count went down
```

### Step 8: Record it
Add a row in `debug_journal.md`: symptom, hypothesis, root cause, fix, lesson. Then ask:
"Could the same mistake exist somewhere else?" (e.g. an off-by-one in one function often appears in another).

---

## Part 2: Tools

| Tool | Use it when | How |
|------|-------------|-----|
| Read the traceback | A crash | Bottom line = error type, the line above = where |
| `print(repr(x))` | You want to see a value | Use `repr`, so `'1'` vs `1` and spaces are visible |
| One-line reproduction | Always | `python -c "..."` |
| `python -m calculator` | Behaviour looks wrong | Type the expression by hand |
| `pdb` debugger | You need to step through code | see below |
| Hand calculation | Wrong number | Compute the expected result on paper first |
| Binary search | Large function | Disable half the logic to see which half has the bug |

### pdb in 6 commands
```bash
python -m pdb -m unittest tests.test_evaluator.ArithmeticTests.test_chained_division_and_subtraction
```
At the `(Pdb)` prompt:
- `b calculator/parser.py:88` set a breakpoint (use the line number of the code you suspect)
- `c` continue to the breakpoint
- `n` next line, `s` step into a call
- `p node` / `pp node` print a value, `l` list nearby code
- `q` quit

---

## Part 3: Worked examples (real output from this project)

### Example A: a crash (Bug 1, tokenizer)
1. Run `python -m unittest tests.test_tokenizer` -> `FAILED (failures=1, errors=3)`.
2. Pick `test_two_dots_is_an_error` (it expects a `TokenizeError`).
3. Reproduce:
   ```
   python -c "from calculator.tokenizer import tokenize; print(tokenize('1.2.3'))"
   ValueError: could not convert string to float: '1.2.3'
   ```
4. Read the traceback: the crash is on the `float(raw)` line in `tokenize`, so `raw` already contains `1.2.3`.
   A number with two dots should have been rejected earlier.
5. Hypothesis: "the dot-count check before `float()` lets two dots through."
6. Look at the line above it: `if dot > 2 or raw == "."`. With `1.2.3`, `dot` is 2, and `2 > 2` is false.
7. Fix: the maximum allowed is ONE dot, so the check must be `dot > 1`. Re-run the test file: that test passes.
8. Lesson: *a raw Python exception means validation is missing or too weak earlier in the code.*

### Example B: wrong value, compared with the expected one (Bug 2, tokenizer)
1. Output of the test: `AssertionError: Lists differ: ['SQRT', 'Pi'] != ['sqrt', 'pi']`.
2. The first list is actual, the second is expected. The tokenizer does not lowercase names.
3. Look at the identifier branch in `tokenize`: it builds `text[start:i]` and nothing normalises it.
4. Fix: lowercase the identifier. Check `python -c "from calculator.tokenizer import tokenize; print(tokenize('SQRT'))"`.

### Example C: use the tree to see the problem (Bug 5, parser)
1. Failing test: `ArithmeticTests.test_chained_division_and_subtraction` -> `AssertionError: 4.0 != 1`.
2. Compute by hand: 8/4/2 = (8/4)/2 = 1. The program says 4.
3. Which stage is wrong? Tokens are fine, so print the tree:
   ```
   Binary(op='/', left=Num(value=2), right=Binary(op='/', left=Num(value=4), right=Num(value=8)))
   ```
4. Read it: it means `2 / (4 / 8)`. The numbers appear in the wrong order: 2, 4, 8 instead of 8, 4, 2.
5. Hypothesis: "when `term()` builds a Binary node, left and right are swapped." (`*` hides this because
   `a*b == b*a`, which is why `6*7` tests passed.)
6. Fix: the accumulated `node` must be the LEFT child. Test file passes, and `python progress.py` goes down.
7. Lesson: *test with operations that are not commutative (`-`, `/`, `%`, `^`).*

### Example D: grammar bug, two symptoms, one cause (Bug 4, parser)
1. Failures: `test_power_is_right_associative`, `test_negative_exponent`, and in the evaluator `test_power`.
2. Stage-by-stage print of `2^3^2` showed: `Binary('^', Binary('^', 2, 3), 2)` and result `64`.
   The correct tree is `2^(3^2)` = 512.
3. Hypothesis: "`power()` loops and parses only an atom on the right, so it groups to the left and
   cannot accept `-1` after `^`."
4. Look at the grammar comment at the top of `parser.py`: `power := atom ('^' unary)?`. The code should
   match it: one optional `^`, and the right side is `unary()`.
5. Fix by rewriting `power()` to follow the grammar. All three tests pass at once.
6. Lesson: *when several tests fail in one area, one root cause is likely. Fix it once.*

### Example E: the traceback points far from the cause (Bug 26, converter, "hard")
1. `python -c "from calculator.converter import convert; convert(1,'km','kg')"`
   ```
   File ".../converter.py", line 46, in convert
       return round(value * LINEAR[cs][src] / LINEAR[cs][dst], 10)
   KeyError: 'kg'
   ```
2. The crash line is the arithmetic, but it is not the real bug. Ask: "why is `'kg'` being looked up in the
   length table?" Because `cs` (the category of km) is `length`, while `kg` belongs to `mass`.
3. The code must stop BEFORE this line when the categories differ. Read the lines above: it computes `cs` and `cd`
   and then never compares them.
4. Fix: compare the two categories and raise `UnitError`. The test expects `UnitError`, not `KeyError`.
5. Lesson: *the line that crashes is only where the problem becomes visible. Find where the bad state began.*

---

## Part 4: Symptom -> likely cause cheat sheet

| What you see | Look for |
|--------------|----------|
| Raw `ValueError`/`TypeError`/`KeyError`/`ZeroDivisionError` instead of `CalcError` | Missing validation or guard clause earlier |
| `AssertionError: X != Y` with X very close to Y | Wrong constant or wrong rounding |
| Wrong only for `-`, `/`, `%`, `^` | Swapped operands, wrong associativity |
| Correct for most inputs, wrong at 0 / 1 / empty / exactly the limit | Off-by-one, `<` vs `<=`, missing special case |
| Works once, wrong the second time | State not reset, shared mutable data |
| Right answer, wrong order | Missing `reversed`, loop running backwards |
| Case-related ("SQRT", "X") | Missing `.lower()` |
| Output text slightly wrong | f-string format specifier, `enumerate` start value, prefix/sign order |
| Function does nothing | Body is `pass` or the key line was removed |

---

## Part 5: When you are stuck (escalation ladder)

1. Re-read the test: it is the specification. What EXACTLY does it expect?
2. Compute the expected value by hand and compare each intermediate value with the program's.
3. Explain the code line by line out loud (rubber-duck debugging).
4. Take a 5-minute break; many bugs are obvious afterwards.
5. Open `HINTS.md`, read **Hint 1 only**, go back to the code. Then Hint 2.
6. Only after that, check `instructor/ANSWER_KEY.md`, and write in your journal why you missed it.

## Part 6: Finish line
```bash
python progress.py          # should say: All tests pass. Every bug is fixed
python -m calculator        # try: 8/4/2, 2^3^2, round(2.5), convert 1 km m, hex -255, mode deg then sin(90)
```
Then compare your fixes with `instructor/solution/` and finish the score card in `debug_journal.md`.
