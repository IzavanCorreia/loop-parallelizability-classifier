"""Compiles the TikZ figures of this folder (standalone LaTeX files sharing figstyle.tex) with the local TinyTeX."""

import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# pdflatex (with the pgf, standalone and dejavu packages) is taken from the folder in TEX_BIN or from the PATH
TEX_BIN = os.environ.get("TEX_BIN", "")


def pdflatex():
    found = shutil.which("pdflatex", path=TEX_BIN or None)
    if not found:
        raise RuntimeError("pdflatex not found: add it to the PATH or set TEX_BIN to its folder")
    return found


def compile_tikz(name, extra=None):
    """Compiles HERE/<name>.tex in a temporary folder, together with figstyle.tex and the files in `extra`
    ({file name: text}), and returns the path of the PDF. Text that does not fit its box (overfull lines)
    is an error."""
    tmp = tempfile.mkdtemp()
    for f in (name + ".tex", "figstyle.tex"):
        shutil.copy(os.path.join(HERE, f), tmp)
    for f, text in (extra or {}).items():
        with open(os.path.join(tmp, f), "w", encoding="utf-8") as fh:
            fh.write(text)
    run = subprocess.run([pdflatex(), "-interaction=nonstopmode", "-halt-on-error", name + ".tex"], cwd=tmp,
                         capture_output=True, text=True, errors="replace")
    log = open(os.path.join(tmp, name + ".log"), encoding="latin-1").read()
    problems = re.findall(r"^(?:!.*|Overfull.*)$", log, re.M)
    if run.returncode or problems:
        raise RuntimeError(f"{name}.tex: " + "; ".join(problems or ["pdflatex failed, see " + tmp]))
    return os.path.join(tmp, name + ".pdf")


def save(pdf, *targets):
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copy(pdf, t)
