# Hints

Try each bug on your own first. Hints are grouped by the file the bug lives in, in the order the data flows
(tokenizer -> parser -> evaluator -> functions -> ...). Every bug has two hints; the full answer is in `instructor/ANSWER_KEY.md`.

Open one hint at a time: read Hint 1, go back to the code, and only then read Hint 2.

## tokenizer.py

### Bug 1 - Easy
- **Symptom:** '1.2.3' crashes with a raw ValueError instead of a TokenizeError.
- **Failing tests:** `test_tokenizer::test_two_dots_is_an_error`
- **Hint 1:** Look at how the tokenizer validates a number's decimal points.
- **Hint 2:** The limit in the dot-count check is off by one.

### Bug 2 - Easy
- **Symptom:** SQRT(16) and PI give 'Unknown function/variable'.
- **Failing tests:** `test_calculator::test_variable_names_are_case_insensitive`, `test_evaluator::test_uppercase_names_work`, `test_tokenizer::test_identifiers_are_lowercased`
- **Hint 1:** Try SQRT(16) and sqrt(16) in the CLI and compare.
- **Hint 2:** Something that normalises the spelling of names was removed.

### Bug 3 - Easy
- **Symptom:** '10 % 3' -> 'Unexpected character'.
- **Failing tests:** `test_evaluator::test_modulo`, `test_evaluator::test_modulo_by_zero`, `test_parser::test_modulo_has_multiplication_precedence`, `test_tokenizer::test_all_operators` (+1 more)
- **Hint 1:** The error comes from the very first stage of the pipeline.
- **Hint 2:** Compare the operator characters the tokenizer accepts with the ones the parser handles.

## parser.py

### Bug 4 - Medium
- **Symptom:** 2^3^2 gives 64 (should be 512); 2^-1 is a ParseError.
- **Failing tests:** `test_evaluator::test_power`, `test_evaluator::test_zero_to_negative_power`, `test_parser::test_negative_exponent`, `test_parser::test_power_is_right_associative`
- **Hint 1:** Print parse('2^3^2') and look at the shape of the tree.
- **Hint 2:** The right-hand side of '^' is parsed with the wrong grammar rule, inside a loop.

### Bug 5 - Medium
- **Symptom:** 8/4/2 gives 4 instead of 1.
- **Failing tests:** `test_calculator::test_evaluate`, `test_calculator::test_failed_evaluation_is_not_recorded`, `test_cli::test_errors_are_reported_not_raised`, `test_cli::test_expressions` (+13 more)
- **Hint 1:** Does 6*7 work? Does 8/4/2? Why the difference?
- **Hint 2:** Look at the argument order when the Binary node is built in term().

### Bug 6 - Easy
- **Symptom:** '(2+3' evaluates to 5 instead of raising ParseError.
- **Failing tests:** `test_parser::test_missing_closing_paren`
- **Hint 1:** Compare how this branch closes a parenthesis with how function calls do it.
- **Hint 2:** One line uses advance() where a checked method is needed.

## evaluator.py

### Bug 7 - Easy
- **Symptom:** '5%0' crashes with ZeroDivisionError instead of a friendly EvalError.
- **Failing tests:** `test_evaluator::test_modulo_by_zero`
- **Hint 1:** Compare the '/' branch with the '%' branch.
- **Hint 2:** A guard clause is missing.

### Bug 8 - Easy
- **Symptom:** '0^0' raises 'Zero cannot be raised to a negative power'; it should be 1.
- **Failing tests:** `test_evaluator::test_zero_to_the_zero_is_one`
- **Hint 1:** Test 0^0, 0^1 and 0^-1 separately.
- **Hint 2:** A comparison operator includes the boundary value when it should not.

### Bug 9 - Medium
- **Symptom:** sqrt(1,2) crashes with a raw TypeError instead of an EvalError.
- **Failing tests:** `test_evaluator::test_too_many_arguments`
- **Hint 1:** Which exception type do you see, and which layer should have caught the problem?
- **Hint 2:** Look at the upper bound in the argument-count check.

## functions.py

### Bug 10 - Medium
- **Symptom:** round(2.5) gives 2, round(1.005, 2) gives 1.0.
- **Failing tests:** `test_functions::test_round_half_up`
- **Hint 1:** Try round(0.5), round(1.5), round(2.5) in the CLI. Do you see a pattern?
- **Hint 2:** The built-in round() is not the rounding rule a calculator user expects.

### Bug 11 - Easy
- **Symptom:** fact(0) raises an error; it should be 1.
- **Failing tests:** `test_functions::test_factorial`
- **Hint 1:** Check the boundary: which smallest input should be valid?
- **Hint 2:** A lower-bound comparison is off by one.

### Bug 12 - Medium
- **Symptom:** lcm(-4, 6) returns -12.
- **Failing tests:** `test_functions::test_lcm`
- **Hint 1:** Does lcm work with negative inputs?
- **Hint 2:** One function call is missing around the product.

### Bug 13 - Easy
- **Symptom:** log(8, 2) gives 0.333... instead of 3.
- **Failing tests:** `test_functions::test_log_with_base`
- **Hint 1:** Plug small numbers into the formula by hand: log base 2 of 8.
- **Hint 2:** Numerator and denominator are the wrong way round.

### Bug 14 - Medium
- **Symptom:** In degree mode sin(90) is wrong; in radian mode sin(pi/2) is wrong.
- **Failing tests:** `test_cli::test_mode`, `test_functions::test_degrees`, `test_functions::test_floating_point_dust_is_cleaned`, `test_functions::test_radians_by_default` (+1 more)
- **Hint 1:** Check sin(pi/2) in default mode, then after 'mode deg'.
- **Hint 2:** A string in a condition is the wrong one of the two modes.

### Bug 15 - Medium
- **Symptom:** In degree mode asin(1) gives 90.0457 instead of 90.
- **Failing tests:** `test_functions::test_inverse_trig_in_degrees`
- **Hint 1:** The answer is close but not exact. What would cause a small, consistent error?
- **Hint 2:** Look for a hard-coded number that should come from the math module.

### Bug 16 - Medium
- **Symptom:** tan(90) in degree mode returns 1.6e16 instead of an error.
- **Failing tests:** `test_functions::test_tan_undefined`
- **Hint 1:** What does tan(90) print? Is that a sensible answer?
- **Hint 2:** A validity check in f_tan() was deleted.

## memory.py

### Bug 17 - Easy
- **Symptom:** store 10, subtract 3 -> memory is -7 instead of 7.
- **Failing tests:** `test_cli::test_memory_commands`, `test_memory::test_subtract`
- **Hint 1:** Do the arithmetic by hand with 10 and 3.
- **Hint 2:** The operands of the subtraction are reversed.

### Bug 18 - Easy
- **Symptom:** After mc, mr still shows the old value.
- **Failing tests:** `test_cli::test_memory_commands`, `test_memory::test_clear`
- **Hint 1:** Does the value change after calling clear()?
- **Hint 2:** The body of clear() does not do anything.

## history.py

### Bug 19 - Medium
- **Symptom:** recent(0) returns the whole history.
- **Failing tests:** `test_history::test_recent_zero_and_negative`
- **Hint 1:** What does [1, 2, 3][-0:] evaluate to?
- **Hint 2:** A guard clause for non-positive n was removed.

### Bug 20 - Medium
- **Symptom:** History(3) keeps 4 entries.
- **Failing tests:** `test_calculator::test_history_size_is_configurable`, `test_history::test_capacity_is_respected`, `test_history::test_load_respects_max_size_keeping_newest`
- **Hint 1:** Count how many entries survive after adding more than max_size.
- **Hint 2:** An off-by-one in the constructor.

### Bug 21 - Easy
- **Symptom:** find('SQRT') misses 'sqrt(4)'.
- **Failing tests:** `test_history::test_find_is_case_insensitive`
- **Hint 1:** Search with different capitalisation.
- **Hint 2:** The normalisation of the text being compared was removed.

### Bug 22 - Medium
- **Symptom:** After save() then load(), the order of entries is reversed.
- **Failing tests:** `test_history::test_load_respects_max_size_keeping_newest`, `test_history::test_save_and_load_roundtrip`
- **Hint 1:** Compare history before saving and after loading.
- **Hint 2:** A loop iterates over the data backwards.

## converter.py

### Bug 23 - Medium
- **Symptom:** convert(212, 'f', 'c') gives about 173 instead of 100.
- **Failing tests:** `test_converter::test_celsius_fahrenheit`
- **Hint 1:** Check the formula against 32F = 0C and 212F = 100C.
- **Hint 2:** A fraction is upside down.

### Bug 24 - Medium
- **Symptom:** convert(1, 'mi', 'km') gives 1.60934 (tiny error).
- **Failing tests:** `test_converter::test_miles`
- **Hint 1:** The answer looks right but fails an exact test; check the data, not the logic.
- **Hint 2:** A number in a lookup table is truncated.

### Bug 25 - Medium
- **Symptom:** convert(0, 'k', 'c') raises 'below absolute zero'.
- **Failing tests:** `test_converter::test_absolute_zero_is_allowed`
- **Hint 1:** Test exactly at the boundary value.
- **Hint 2:** A comparison operator includes the boundary.

### Bug 26 - Hard
- **Symptom:** convert(1, 'km', 'kg') crashes with KeyError instead of UnitError.
- **Failing tests:** `test_cli::test_convert_errors`, `test_converter::test_mismatched_categories`
- **Hint 1:** Read the traceback: which exception, and on which line? What should have stopped it before that line?
- **Hint 2:** A validation step between category lookup and arithmetic is missing.

## bases.py

### Bug 27 - Easy
- **Symptom:** to_base(10, 2) gives '0101'.
- **Failing tests:** `test_bases::test_roundtrip`, `test_bases::test_common_values`, `test_cli::test_base_commands`
- **Hint 1:** Work through 10 in binary by hand and watch the order of the remainders.
- **Hint 2:** The digits are assembled in the order they were produced.

### Bug 28 - Medium
- **Symptom:** from_base('2', 2) returns 2 instead of raising an error.
- **Failing tests:** `test_bases::test_invalid_digit_for_base`, `test_cli::test_frombase`
- **Hint 1:** Try digit 2 in base 2, digit 8 in base 8.
- **Hint 2:** A comparison is off by one at the upper boundary.

## stats.py

### Bug 29 - Medium
- **Symptom:** median([1,2,3,4]) gives 3.5; median([1,2]) raises IndexError.
- **Failing tests:** `test_cli::test_stats`, `test_stats::test_median_odd_even_unsorted`
- **Hint 1:** Write out the sorted list and mark the two middle positions.
- **Hint 2:** Both indexes in the average are shifted by one.

### Bug 30 - Medium
- **Symptom:** Population variance of [2,4,4,4,5,5,7,9] is not 4.
- **Failing tests:** `test_cli::test_stats`, `test_stats::test_population_variance_and_stdev`, `test_stats::test_sample_variance`, `test_stats::test_sample_variance_needs_two_values`
- **Hint 1:** Compute the expected value by hand for the classic data set 2,4,4,4,5,5,7,9.
- **Hint 2:** The conditional expression picks the wrong divisor for each mode.

### Bug 31 - Medium
- **Symptom:** mode([1,2,3]) returns [1,2,3] instead of [].
- **Failing tests:** `test_cli::test_stats`, `test_stats::test_mode_with_no_repeats`
- **Hint 1:** What are the counts for [1,2,3]? What should the result be?
- **Hint 2:** A special case for 'nothing repeats' was removed.

## calculator.py

### Bug 32 - Easy
- **Symptom:** 1/3 prints 0.33; 2^0.5 prints 1.41.
- **Failing tests:** `test_calculator::test_evaluate`, `test_calculator::test_decimals_use_ten_significant_digits`, `test_calculator::test_huge_floats_use_scientific_notation`, `test_cli::test_convert` (+2 more)
- **Hint 1:** Print 1/3 and 1/3000.
- **Hint 2:** Look at the format specifier in the f-string.

### Bug 33 - Medium
- **Symptom:** 'X = 5' then 'x*2' -> Unknown variable 'x'.
- **Failing tests:** `test_calculator::test_variable_names_are_case_insensitive`
- **Hint 1:** Which name is stored, and which name is looked up?
- **Hint 2:** One side of the assignment is not normalised.

## cli.py

### Bug 34 - Easy
- **Symptom:** 'history' prints '0. 1+1 = 2'.
- **Failing tests:** `test_cli::test_history_numbering`
- **Hint 1:** Look at the first line of the history output.
- **Hint 2:** A missing second argument to enumerate().

### Bug 35 - Medium
- **Symptom:** 'hex -255' prints '0x-ff' instead of '-0xff'.
- **Failing tests:** `test_cli::test_negative_base_output`
- **Hint 1:** Run hex with a negative number and read the output carefully.
- **Hint 2:** The helper no longer treats negative digit strings differently.

### Bug 36 - Easy
- **Symptom:** 'convert 1 km m' prints '1 km = 0.001 m'.
- **Failing tests:** `test_cli::test_convert`
- **Hint 1:** Convert something where you know the answer, e.g. 1 km to m.
- **Hint 2:** Compare the call with the function's signature.
