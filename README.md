# Debug Practice Project: Scientific Calculator (36 hidden bugs)

A realistic ~900-line, 12-module calculator (expression parser, functions, memory, history, unit converter,
number bases, statistics, command-line interface) in which **36 bugs have been planted**.
Your job: make all 148 tests pass by finding and fixing the bugs in `calculator/`.

## Quick start

```bash
python progress.py                      # progress bar + failing tests per module
python progress.py -v                   # list every failing test
python -m unittest tests.test_parser -v # run one test file
python -m calculator                    # try the calculator by hand
```
Python 3.9+, no extra packages.

## How the calculator works

```
text --tokenizer--> tokens --parser--> syntax tree --evaluator--> number --format_number--> text
                                          |-- functions.py (sqrt, sin, round, ...)
cli.py ---> Calculator (calculator.py) ---> Environment (variables, angle mode), Memory, History
         \-> converter.py   bases.py   stats.py
```

Calculator commands: `2+3*4`, `sqrt(16)`, `x = 5`, `ans*2`, `mode deg`, `convert 5 km mi`, `stats 1 2 3`,
`hex 255`, `frombase ff 16`, `m+ 5`, `mr`, `history`, `help`, `quit`.

## Rules of the game
1. Only edit files in `calculator/`. Do **not** edit the tests (they are the specification).
2. Fix ONE failing test at a time; re-run after every change.
3. Start with tests in the earliest pipeline stage (tokenizer -> parser -> evaluator) - bugs there break everything after them.
4. Keep `debug_journal.md` as you go.
5. Stuck? Read `HINTS.md` (two hints per bug, grouped by file). Last resort: `instructor/ANSWER_KEY.md`.

## Debugging toolbox
- **Read the failure**: `AssertionError: 4 != 1` tells you expected vs. actual; a traceback tells you *where* it crashed.
- **Reproduce in the REPL**: `python -c "from calculator.parser import parse; print(parse('2^3^2'))"`
- **Print the intermediate stage**: tokens (`tokenize`), tree (`parse`), value (`evaluate`) - find the first stage that is wrong.
- **Debugger**: `python -m pdb -m unittest tests.test_parser.ParserTests.test_power_is_right_associative`
  (`n` next, `s` step into, `p expr` print, `l` list, `c` continue, `q` quit).
- **Check the boundaries**: 0, 1, -1, empty input, exactly-at-the-limit values (many bugs hide there).
- **Binary search**: comment out half the suspicious code to see which half contains the bug.
- Once the test passes, ask: *could the same mistake exist elsewhere?*

## Difficulty guide
Easy (15 bugs): single wrong operator, name or missing line.  
Medium (20 bugs): logic that looks right but fails for edge cases or specific inputs.  
Hard (1 bug): the traceback points far from the real cause.  
Bugs are spread across all modules and span these categories: off-by-one, wrong operator/comparison, swapped
arguments, missing validation, wrong constant, missing normalisation, wrong order/associativity, and no-op code.

## Project layout
```
calculator/        <- buggy code you fix
tests/             <- 148 tests (do not edit)
progress.py        <- progress tracker
DEBUGGING_WALKTHROUGH.md <- step-by-step method with worked examples
HINTS.md           <- two hints per bug
debug_journal.md   <- template for your notes
instructor/        <- spoilers! solution/, ANSWER_KEY.md, build_bugs.py
```

## For instructors
`python instructor/build_bugs.py` re-injects the bugs into `instructor/solution/` and verifies that every
single bug is caught by at least one test. Add your own bug by appending a `B(...)` entry in that file.
