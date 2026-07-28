# sinh(x) Calculator — SOEN 6011 (F3)

A from-scratch implementation of the hyperbolic sine function with a
Tkinter graphical user interface.

**Course:** SOEN 6011 — Software Engineering Processes, Summer 2026,
Concordia University
**Author:** Ramprasad Giriraj (40298904)
**Function:** F3 — sinh(x)
**Version:** 2.0.0

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

## Requirements

- Python 3.8+ with Tkinter (included in standard CPython installers;
  on Debian/Ubuntu: `sudo apt install python3-tk`)
- No third-party packages. No IDE required.

## Run

```
python3 sinh_gui.py
```

Type a real number, press **Compute** (or Enter). **Clear** resets,
**Quit** exits.

## Error handling

Custom exception classes provide helpful, user-oriented messages:

| Situation | Class | Message shown |
|---|---|---|
| Non-numeric input (e.g. `hello`, empty) | `SinhInputError` | "'hello' is not a real number. Please enter a value like 2, -0.5, or 3.14." |
| Result exceeds double range (|x| ≳ 710) | `SinhOverflowError` | "sinh(x) is too large to represent on this computer. Try a value between about -710 and 710." |

## Accuracy

Verified against reference values: relative error ≤ 3 × 10⁻¹⁵ across
the full representable range, including the overflow boundary
(x = 710.4 computes correctly; x = 712 raises a clean overflow error).

## Project structure

```
sinh_gui.py    — computation core, custom exceptions, Tkinter GUI
README.md      — this file
```

## Design notes

- **Subordinate functions** identified for the from-scratch build:
  `_absolute(v)` (avoids built-in `abs`) and the in-loop term
  recurrence (avoids factorial/power functions).
- The multiply/divide order in the recurrence is deliberate:
  `term / (2n) * v * (v / (2n+1))` keeps intermediates bounded, where
  the naive `term * v * v / ((2n)(2n+1))` overflows transiently near
  x ≈ 709 even though the final answer is representable.
- Exceptions derive from a common `SinhError` base so the GUI handles
  all calculator errors uniformly.
