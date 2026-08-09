# sinh(x) Calculator — SOEN 6011 (F3)

A from-scratch implementation of the hyperbolic sine function with a
Tkinter graphical user interface, PEP-8 conformance, static analysis,
and a unit test suite.

**Course:** SOEN 6011 — Software Engineering Processes, Summer 2026,
Concordia University
**Author:** Ramprasad Giriraj (40298904)
**Function:** F3 — sinh(x)
**Version:** 3.0.0 (Semantic Versioning)

## What it does

Computes sinh(x) = (e^x − e^−x)/2 for any real x, using only
`+ − × ÷` — no `math` module and no built-in mathematical library
functions, per the project's "from scratch" constraint. The
computation uses the Maclaurin series

```
sinh(x) = x + x^3/3! + x^5/5! + ...
```

with each term built from the previous one (no factorials or powers
are ever computed), odd-symmetry argument reduction, and a
divide-before-multiply term recurrence so that intermediate values
never overflow before the true mathematical limit (about |x| ≈ 710).

## Files

```
sinh_d3.py     — current version (3.0.0): computation core, custom
                 exceptions, Tkinter GUI. PEP-8 clean, Pylint 10.00/10.
test_sinh.py   — PyUnit test suite (20 tests)
sinh_gui.py    — previous version (2.0.0), kept for history
README.md      — this file
```

## Requirements

- Python 3.8+ with Tkinter (included in standard CPython installers;
  on Debian/Ubuntu: `sudo apt install python3-tk`)
- No third-party packages required to run. No IDE required.
- For the checks below: `pip install flake8 pylint`

## Run

```
python3 sinh_d3.py
```

Type a real number, press **Compute** (or Enter). **Clear** resets,
**Quit** exits.

## Tests

```
python3 -m unittest -v test_sinh
```

20 tests covering: accuracy against reference values, odd symmetry,
overflow behaviour, input parsing, and the from-scratch `_absolute`
helper. Boundary cases are explicit — `sinh(710.4)` must compute,
`sinh(800)` must raise `SinhOverflowError`.

## Style and static analysis

```
flake8 sinh_d3.py     # no output — fully PEP-8 compliant
pylint sinh_d3.py     # rated 10.00/10
```

Improvements made to reach 10.00/10 (from 8.83): f-string formatting,
explicit exception chaining (`raise ... from exc`), and consistent
continuation-line indentation.

## Error handling

Custom exception classes provide helpful, user-oriented messages:

| Situation | Class | Message shown |
|---|---|---|
| Non-numeric input (e.g. `hello`, empty) | `SinhInputError` | "'hello' is not a real number. Please enter a value like 2, -0.5, or 3.14." |
| Result exceeds double range (\|x\| ≳ 710) | `SinhOverflowError` | "sinh(x) is too large to represent on this computer. Try a value between about -710 and 710." |

Both derive from a common `SinhError` base, so the GUI handles all
calculator errors uniformly.

## Accessibility and UI design

Large readable font, high-contrast result text, keyboard support
(Enter computes, Tab moves focus), clear labels, and errors conveyed
by text rather than colour alone.

## Accuracy

Verified against reference values: relative error ≤ 3 × 10⁻¹⁵ across
the full representable range, including the overflow boundary
(x = 710.4 computes correctly; x = 712 raises a clean overflow error).

## Versioning

Semantic Versioning (`MAJOR.MINOR.PATCH`):

- `1.0.0` — D1: series core with a textual interface
- `2.0.0` — D2: from-scratch rebuild, custom exceptions, Tkinter GUI
- `3.0.0` — D3: PEP-8 conformance, static analysis, unit test suite

## Design notes

- **Subordinate functions** identified for the from-scratch build:
  `_absolute(v)` (avoids built-in `abs`) and the in-loop term
  recurrence (avoids factorial/power functions).
- The multiply/divide order in the recurrence is deliberate:
  `term / (2n) * v * (v / (2n+1))` keeps intermediates bounded, where
  the naive `term * v * v / ((2n)(2n+1))` overflows transiently near
  x ≈ 709 even though the final answer is representable.
