#!/usr/bin/env python3
"""Run all tests and show how far you are. Usage: python progress.py [-v]"""
import sys
import unittest
from collections import Counter


def main():
    verbose = "-v" in sys.argv
    sys.path.insert(0, ".")
    suite = unittest.defaultTestLoader.discover("tests", top_level_dir=".")
    result = unittest.TestResult()
    suite.run(result)

    failing = {t.id().split(" (")[0] for t, _ in result.failures + result.errors}
    total = result.testsRun
    passed = total - len(failing)
    width = 30
    filled = round(width * passed / total) if total else 0
    print(f"[{'#' * filled}{'-' * (width - filled)}] {passed}/{total} tests passing")

    if not failing:
        print("\nAll tests pass. Every bug is fixed - well done!")
        return 0

    per_module = Counter(t.split(".")[1] for t in failing)
    print("\nFailing tests per module:")
    for module, count in sorted(per_module.items()):
        print(f"  {module:<18} {count}")

    if verbose:
        print("\nFailing tests:")
        for t in sorted(failing):
            print("  -", t.replace("tests.", "", 1))
    else:
        print("\n(run 'python progress.py -v' to list every failing test)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
