import math
from io import StringIO


class Latex:
    def __init__(self):
        self._buf = StringIO()
        self._buf.write(
            r"""\documentclass{article}

\usepackage{graphicx}
\usepackage{cprotect}

\begin{document}
"""
        )

    def _finalize(self):
        self._buf.write(r"\end{document}")

    def add_image(self, filename: str, caption: str):
        print(caption)
        self._buf.write(
            rf"""
\begin{{figure}}[ht]
\centering
    \includegraphics{{{filename}}}
\cprotect\caption{{"""
        )
        MAX_LEN = 40
        end = int(math.ceil(len(caption) / MAX_LEN))
        for i in range(end):
            start = MAX_LEN * i
            end = MAX_LEN * (i + 1)
            print(start, end)
            cap = caption[start:end]
            print(i, cap)
            self._buf.write(rf"\verb|{cap}| ")

        # close the caption, end the figure
        self._buf.write(
            r"""}
\end{figure}
"""
        )

    def to_file(self, filename):
        self._finalize()
        with open(filename, "w") as out:
            out.write(self._buf.getvalue())
