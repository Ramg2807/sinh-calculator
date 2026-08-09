"""SOEN 6011 - Deliverable 2 - F3: sinh(x).

From-scratch implementation of the hyperbolic sine with a Tkinter GUI.

"From scratch" (per the project description): apart from input, output,
arithmetic, and user-interface functions, no built-in or library
functions are used. In particular, the math module is NOT imported.
The computation uses only +, -, *, / and comparisons.

Design:
    sinh(x) = x + x^3/3! + x^5/5! + ...   (Maclaurin series)

    Subordinate functions identified and implemented from scratch:
        _absolute(v)   -- absolute value (|v|), since abs() is avoided
        _next_term(..) -- builds term n+1 from term n without factorials

Exception handling uses custom exception classes so the GUI can show
helpful, user-oriented messages (traceable to persona frustrations).

Author : Ramprasad Giriraj (40298904)
Course : SOEN 6011, Summer 2026
Version: 3.0.0
"""

import tkinter as tk  # pylint: disable=import-error

# Largest finite double; used to detect overflow without the math module.
_MAX_DOUBLE = 1.7976931348623157e308

__version__ = "3.0.0"


# ---------------------------------------------------------------------------
# Custom exceptions (Problem 5: exception handling with helpful messages)
# ---------------------------------------------------------------------------

class SinhError(Exception):
    """Base class for all sinh calculator errors."""


class SinhInputError(SinhError):
    """Raised when the user's input cannot be read as a real number."""

    def __init__(self, raw):
        super().__init__(
            f"'{raw}' is not a real number. Please enter a value like "
            "2, -0.5, or 3.14."
        )


class SinhOverflowError(SinhError):
    """Raised when |sinh(x)| exceeds the largest representable double."""

    def __init__(self, x):
        super().__init__(
            f"sinh({x}) is too large to represent on this computer. "
            "Try a value between about -710 and 710."
        )


# ---------------------------------------------------------------------------
# From-scratch computation (Problem 5)
# ---------------------------------------------------------------------------

def _absolute(v):
    """Return |v| using only comparison and negation (no abs())."""
    if v < 0:
        return -v
    return v


def sinh(x, tol=1e-16, max_terms=800):
    """Return sinh(x) via its Maclaurin series, using only arithmetic.

    Args:
        x: real input value.
        tol: relative tolerance for convergence.
        max_terms: safety cap on iterations.

    Returns:
        float approximation of sinh(x).

    Raises:
        SinhOverflowError: if the result exceeds double-precision range.
    """
    # Odd symmetry: sinh(-x) = -sinh(x). Work with |x|, restore sign.
    sign = 1.0
    v = x
    if v < 0:
        sign = -1.0
        v = -v

    term = v          # first series term is x itself
    total = term
    n = 1
    while n < max_terms:
        # Subordinate step: next odd term from the previous one,
        # term_{n} = term_{n-1} * v^2 / ((2n)(2n+1)). The multiply and
        # divide are interleaved so intermediates never overflow.
        term = (term / (2.0 * n) * v) * (v / (2.0 * n + 1.0))
        total = total + term
        if total > _MAX_DOUBLE:
            raise SinhOverflowError(x)
        if _absolute(term) < tol * _absolute(total):
            break
        n = n + 1

    if total > _MAX_DOUBLE:
        raise SinhOverflowError(x)
    return sign * total


def parse_real(raw):
    """Convert raw user text to a float, raising SinhInputError if invalid.

    float() is treated as an input function (permitted); the validation
    and messaging around it are what the persona-driven requirements ask.
    """
    cleaned = raw.strip()
    if cleaned == "":
        raise SinhInputError("(empty)")
    try:
        return float(cleaned)
    except ValueError as exc:
        raise SinhInputError(cleaned) from exc


# ---------------------------------------------------------------------------
# Tkinter GUI (Problem 5: graphical user interface)
# ---------------------------------------------------------------------------

class SinhApp:
    """A small Tkinter application to evaluate sinh(x)."""

    def __init__(self, root):
        self.root = root
        root.title("sinh(x) Calculator  v" + __version__)
        root.resizable(False, False)

        pad = {"padx": 10, "pady": 6}

        tk.Label(root, text="Hyperbolic Sine Calculator",
                 font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, columnspan=3, **pad)

        tk.Label(root, text="x =").grid(row=1, column=0, sticky="e", **pad)

        self.entry = tk.Entry(root, width=24, font=("Helvetica", 12))
        self.entry.grid(row=1, column=1, **pad)
        self.entry.focus_set()
        # Usability: pressing Enter computes (FR-9).
        self.entry.bind("<Return>", lambda event: self.compute())

        tk.Button(root, text="Compute", command=self.compute).grid(
            row=1, column=2, **pad)

        self.result = tk.Label(root, text="Enter a real number and press "
                                          "Compute.",
                               font=("Helvetica", 12), fg="#0F4C5C",
                               wraplength=360, justify="left")
        self.result.grid(row=2, column=0, columnspan=3, **pad)

        tk.Button(root, text="Clear", command=self.clear).grid(
            row=3, column=0, **pad)
        tk.Button(root, text="Quit", command=root.destroy).grid(
            row=3, column=2, **pad)

    def compute(self):
        """Read the entry, evaluate sinh, and display result or error."""
        raw = self.entry.get()
        try:
            x = parse_real(raw)
            value = sinh(x)
        except SinhError as err:
            # Helpful, non-technical message (NFR-2).
            self.result.config(text="Error: " + str(err), fg="#B00020")
            return
        self.result.config(text=f"sinh({x}) = {value}",
                           fg="#0F4C5C")

    def clear(self):
        """Reset the input and the result area (FR-10)."""
        self.entry.delete(0, tk.END)
        self.result.config(text="Enter a real number and press Compute.",
                           fg="#0F4C5C")


def main():
    """Launch the GUI. Runs with plain python3; no IDE required."""
    root = tk.Tk()
    SinhApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
