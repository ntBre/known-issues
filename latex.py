import math
from io import StringIO


class Latex:
    def __init__(self):
        self._num_images = 0
        self._buf = StringIO()
        self._buf.write(
            r"""\documentclass{article}

\usepackage{graphicx}
\usepackage[margin=1in]{geometry}

\begin{document}
"""
        )

    def _finalize(self):
        self._buf.write(r"\end{document}")

    def add_image(self, filename: str, caption: str):
        self._num_images += 1
        self._buf.write(
            rf"""
\begin{{figure}}[ht]
\centering
    \includegraphics{{{filename}}}
\end{{figure}}
"""
        )
        MAX_LEN = 40
        end = int(math.ceil(len(caption) / MAX_LEN))
        for i in range(end):
            start = MAX_LEN * i
            end = MAX_LEN * (i + 1)
            cap = caption[start:end]
            self._buf.write(rf"\verb|{cap}|\n")

        if self._num_images % 20 != 0:
            self._buf.write(r"\clearpage")

    def to_file(self, filename):
        self._finalize()
        with open(filename, "w") as out:
            out.write(self._buf.getvalue())
