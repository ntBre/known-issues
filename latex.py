import math
from io import StringIO


class Latex:
    def __init__(self):
        self._buf = StringIO()
        self._buf.write(
            r"""\documentclass{beamer}

\usepackage{graphicx}

\setbeamertemplate{navigation symbols}{}

\begin{document}
"""
        )

    def _finalize(self):
        self._buf.write(r"\end{document}")

    def add_image(self, filename: str, caption: str):
        self._buf.write(r"\begin{frame}[fragile]" + "\n")

        MAX_LEN = 40
        end = int(math.ceil(len(caption) / MAX_LEN))
        for i in range(end):
            cap = caption[MAX_LEN * i : MAX_LEN * (i + 1)]
            self._buf.write(rf"\verb|{cap}|" + "\n")

        self._buf.write(
            rf"""
\begin{{figure}}
    \includegraphics[width=0.7\textwidth,height=0.7\textheight,keepaspectratio]{{{filename}}}
\end{{figure}}
"""
        )
        self._buf.write(r"\end{frame}" + "\n")

    def to_file(self, filename):
        self._finalize()
        with open(filename, "w") as out:
            out.write(self._buf.getvalue())
