"""Dynamic dependence oracle for single Python loops.

The oracle executes the target loop of a code sample iteration by iteration and records, for
every iteration, which variables and which container elements are read and written. A loop is
labelled Parallelizable when no value flows between iterations, and Undefined otherwise. The
analysis follows the usual definition of loop-carried dependences used by dynamic dependence
profilers:

* a scalar read in iteration k before being written in k, and written in an earlier iteration,
  is a loop-carried flow dependence;
* a scalar written in the loop and read after it is a live-out (output) dependence;
* a container element written in one iteration and read or written in another one is a
  cross-iteration conflict;
* a list that is appended to and also read inside the loop carries state between iterations;
* ``break``/``return`` inside the loop body and ``while`` loops make the iteration space depend
  on computed state.

Appending to a result list that is not read inside the loop (the *map* pattern) is accepted as
Parallelizable, which is the convention used to annotate the real-world samples.
"""

import ast
import builtins
import contextlib
import io
import multiprocessing as mp
import random

PARALLELIZABLE = "Parallelizable"
UNDEFINED = "Undefined"

MAX_ITERATIONS = 200
ALLOWED_MODULES = {
    "math", "random", "string", "hashlib", "uuid", "datetime", "statistics", "itertools",
    "functools", "collections", "re", "json", "decimal", "fractions", "numpy", "time",
    "operator", "copy", "heapq", "bisect",
}
PARAM_DEFAULTS = (10, list(range(1, 11)), "texto", 1.5)


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class _Recorder:
    """Collects the per-iteration access log of one loop execution."""

    def __init__(self):
        self.iteration = -1
        self.active = False
        self.scalar_writes = {}       # name -> set of iterations
        self.exposed_reads = {}       # name -> set of iterations (read before written in it)
        self.written_now = set()
        self.elem_writes = {}         # (cid, key) -> set of iterations
        self.elem_reads = {}          # (cid, key) -> set of iterations
        self.appends = {}             # cid -> set of iterations
        self.whole_reads = {}         # cid -> set of iterations (len, iteration, slicing...)

    def start_iteration(self, k):
        self.iteration = k
        self.written_now = set()

    def _add(self, table, key):
        if self.active:
            table.setdefault(key, set()).add(self.iteration)


class LoggingNamespace(dict):
    """Local namespace that logs name reads and writes during the loop body."""

    def __init__(self, recorder, *args, **kw):
        super().__init__(*args, **kw)
        self.rec = recorder

    def __getitem__(self, name):
        value = super().__getitem__(name)
        rec = self.rec
        if rec.active and name not in rec.written_now:
            rec._add(rec.exposed_reads, name)
        return value

    def __setitem__(self, name, value):
        rec = self.rec
        if rec.active:
            rec._add(rec.scalar_writes, name)
            rec.written_now.add(name)
        super().__setitem__(name, value)


def _norm_index(key, length):
    if isinstance(key, int) and key < 0:
        return key + length
    return key


class TrackedList(list):
    def __init__(self, data, recorder):
        super().__init__(data)
        self._rec = recorder

    def __getitem__(self, key):
        rec = self._rec
        if isinstance(key, slice):
            rec._add(rec.whole_reads, id(self))
        else:
            rec._add(rec.elem_reads, (id(self), _norm_index(key, list.__len__(self))))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        rec = self._rec
        if isinstance(key, slice):
            rec._add(rec.whole_reads, id(self))
            rec._add(rec.elem_writes, (id(self), "slice"))
        else:
            rec._add(rec.elem_writes, (id(self), _norm_index(key, list.__len__(self))))
        super().__setitem__(key, value)

    def append(self, value):
        self._rec._add(self._rec.appends, id(self))
        super().append(value)

    def extend(self, values):
        self._rec._add(self._rec.appends, id(self))
        super().extend(values)

    def insert(self, i, value):
        self._rec._add(self._rec.whole_reads, id(self))
        self._rec._add(self._rec.appends, id(self))
        super().insert(i, value)

    def pop(self, *a):
        self._rec._add(self._rec.whole_reads, id(self))
        self._rec._add(self._rec.appends, id(self))
        return super().pop(*a)

    def remove(self, v):
        self._rec._add(self._rec.whole_reads, id(self))
        self._rec._add(self._rec.appends, id(self))
        super().remove(v)

    def __len__(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().__len__()

    def __iter__(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().__iter__()

    def __contains__(self, v):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().__contains__(v)

    def copy(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return list(super().__iter__())

    def sort(self, *a, **k):
        self._rec._add(self._rec.whole_reads, id(self))
        self._rec._add(self._rec.elem_writes, (id(self), "slice"))
        super().sort(*a, **k)

    def reverse(self):
        self._rec._add(self._rec.whole_reads, id(self))
        self._rec._add(self._rec.elem_writes, (id(self), "slice"))
        super().reverse()

    def count(self, v):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().count(v)

    def index(self, *a):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().index(*a)


class TrackedDict(dict):
    def __init__(self, data, recorder):
        super().__init__(data)
        self._rec = recorder

    def __getitem__(self, key):
        self._rec._add(self._rec.elem_reads, (id(self), key))
        return super().__getitem__(key)

    def get(self, key, default=None):
        self._rec._add(self._rec.elem_reads, (id(self), key))
        return super().get(key, default)

    def __setitem__(self, key, value):
        self._rec._add(self._rec.elem_writes, (id(self), key))
        super().__setitem__(key, value)

    def setdefault(self, key, default=None):
        self._rec._add(self._rec.elem_reads, (id(self), key))
        self._rec._add(self._rec.elem_writes, (id(self), key))
        return super().setdefault(key, default)

    def __contains__(self, key):
        self._rec._add(self._rec.elem_reads, (id(self), key))
        return super().__contains__(key)

    def __len__(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().__len__()

    def __iter__(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().__iter__()

    def keys(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().keys()

    def values(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().values()

    def items(self):
        self._rec._add(self._rec.whole_reads, id(self))
        return super().items()

    def update(self, *a, **k):
        self._rec._add(self._rec.elem_writes, (id(self), "update"))
        super().update(*a, **k)


class TrackedSet(set):
    """Sets are tracked as a whole: membership/size/iteration are reads, additions are writes."""

    def __init__(self, data, recorder):
        super().__init__(data)
        self._rec = recorder

    def _read(self):
        self._rec._add(self._rec.whole_reads, id(self))

    def _write(self):
        self._rec._add(self._rec.elem_writes, (id(self), "update"))

    def __contains__(self, v):
        self._read()
        return super().__contains__(v)

    def __len__(self):
        self._read()
        return super().__len__()

    def __iter__(self):
        self._read()
        return super().__iter__()

    def add(self, v):
        self._write()
        super().add(v)

    def update(self, *a):
        self._write()
        super().update(*a)

    def discard(self, v):
        self._write()
        super().discard(v)

    def remove(self, v):
        self._write()
        super().remove(v)

    def __ior__(self, other):
        self._write()
        return super().__ior__(other)


def _track(value, recorder, seen=None):
    """Recursively wraps lists and dicts created before the loop."""
    seen = {} if seen is None else seen
    if id(value) in seen:
        return seen[id(value)]
    if isinstance(value, list) and not isinstance(value, TrackedList):
        out = TrackedList([], recorder)
        seen[id(value)] = out
        list.extend(out, [_track(v, recorder, seen) for v in value])
        return out
    if isinstance(value, set) and not isinstance(value, TrackedSet):
        out = TrackedSet(value, recorder)
        seen[id(value)] = out
        return out
    if isinstance(value, dict) and not isinstance(value, (TrackedDict, LoggingNamespace)):
        out = TrackedDict({}, recorder)
        seen[id(value)] = out
        for k, v in value.items():
            dict.__setitem__(out, k, _track(v, recorder, seen))
        return out
    return value


class _EarlyExitRewriter(ast.NodeTransformer):
    """Turns break/continue/return of the target loop into exceptions (not inside nested loops)."""

    def __init__(self):
        self.has_break = False
        self.has_return = False

    def visit_For(self, node):
        return node      # break/continue of nested loops belong to them

    visit_While = visit_For
    visit_AsyncFor = visit_For

    def visit_FunctionDef(self, node):
        return node

    visit_Lambda = visit_FunctionDef

    def visit_Break(self, node):
        self.has_break = True
        return ast.copy_location(ast.Raise(exc=ast.Name("_Break", ast.Load()), cause=None), node)

    def visit_Continue(self, node):
        return ast.copy_location(ast.Raise(exc=ast.Name("_Continue", ast.Load()), cause=None), node)

    def visit_Return(self, node):
        self.has_return = True
        return ast.copy_location(ast.Raise(exc=ast.Name("_Break", ast.Load()), cause=None), node)


def _imports_allowed(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            mods = [(node.module or "").split(".")[0]]
        else:
            continue
        if any(m not in ALLOWED_MODULES for m in mods):
            return False
    return True


def _find_target(tree):
    """Returns (scope_statements, loop_index, function_node or None)."""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for i, st in enumerate(node.body):
                if isinstance(st, (ast.For, ast.While)):
                    return node.body, i, node
    for i, st in enumerate(tree.body):
        if isinstance(st, (ast.For, ast.While)):
            return tree.body, i, None
    return None, None, None


def _comprehension_as_loop(tree):
    """Rewrites the first single-generator list/generator comprehension of a statement in a
    function (``return [e for x in xs if c]`` or ``ys = [...]``) as the equivalent explicit loop
    that appends to a fresh list, so the oracle can analyse comprehension-only samples."""
    scopes = [n.body for n in tree.body if isinstance(n, ast.FunctionDef)] + [tree.body]
    for body in scopes:
        for i, st in enumerate(body):
            value = st.value if isinstance(st, (ast.Return, ast.Assign, ast.Expr)) else None
            comp = None
            for n in ast.walk(value) if value is not None else []:
                if isinstance(n, (ast.ListComp, ast.GeneratorExp)) and len(n.generators) == 1 \
                        and not n.generators[0].is_async:
                    comp = n
                    break
            if comp is None:
                continue
            gen = comp.generators[0]
            append = ast.Expr(ast.Call(ast.Attribute(ast.Name("_oracle_out", ast.Load()), "append", ast.Load()),
                                       [comp.elt], []))
            inner = append
            for cond in reversed(gen.ifs):
                inner = ast.If(test=cond, body=[inner], orelse=[])
            init = ast.Assign(targets=[ast.Name("_oracle_out", ast.Store())], value=ast.List([], ast.Load()))
            loop = ast.For(target=gen.target, iter=gen.iter, body=[inner], orelse=[])
            body[i:i + 1] = [init, loop]
            return ast.fix_missing_locations(tree)
    return None


class _Globals(dict):
    """Globals seen by nested scopes (generator expressions, lambdas) inside the loop body:
    names missing here are looked up in the logged local namespace."""

    def __init__(self, base, ns):
        super().__init__(base)
        self._ns = ns

    def __missing__(self, key):
        return self._ns[key]


def _module(stmts):
    return compile(ast.fix_missing_locations(ast.Module(body=stmts, type_ignores=[])), "<oracle>", "exec")


def _names_loaded(stmts):
    out = set()
    for st in stmts:
        for n in ast.walk(st):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                out.add(n.id)
    return out


def _names_stored(stmts):
    out = set()
    for st in stmts:
        for n in ast.walk(st):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                out.add(n.id)
    return out


def _target_names(target):
    return {n.id for n in ast.walk(target) if isinstance(n, ast.Name)}


def analyze(code):
    """Analyses the first top-level loop of ``code``.

    Returns a dict with ``label`` (Parallelizable, Undefined or None when the sample cannot be
    analysed) and ``reason``. Function parameters are bound to a few default values in turn until
    one of them executes without a runtime error.
    """
    result = None
    for value in PARAM_DEFAULTS:
        result = _analyze(code, value)
        if not result["reason"].startswith("runtime error"):
            return result
    return result


def _analyze(code, param_value):
    random.seed(0)
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"label": None, "reason": f"syntax error: {e.msg}"}
    if not _imports_allowed(tree):
        return {"label": None, "reason": "imports outside the allow-list"}
    scope, idx, func = _find_target(tree)
    if scope is None and _comprehension_as_loop(tree) is not None:
        scope, idx, func = _find_target(tree)
    if scope is None:
        return {"label": None, "reason": "no top-level loop"}
    loop = scope[idx]
    if isinstance(loop, ast.While):
        return {"label": UNDEFINED, "reason": "while loop: iteration space depends on state"}
    pre, post = scope[:idx], scope[idx + 1:]

    rewriter = _EarlyExitRewriter()
    body = [rewriter.visit(st) for st in loop.body]
    if rewriter.has_break or rewriter.has_return:
        return {"label": UNDEFINED, "reason": "early exit (break/return) inside the loop"}

    loop_vars = _target_names(loop.target)
    live_out = (_names_stored(loop.body) - loop_vars) & _names_loaded(post)
    if live_out:
        return {"label": UNDEFINED, "reason": f"live-out scalar(s): {sorted(live_out)}"}

    rec = _Recorder()
    sink = io.StringIO()
    # math/random/string are preloaded because several snippets use them without importing
    g = {"__builtins__": builtins, "_Break": _Break, "_Continue": _Continue,
         "math": __import__("math"), "random": random, "string": __import__("string")}
    try:
        with contextlib.redirect_stdout(sink):
            # module-level definitions and imports (not the loop itself when it is at module level)
            if func is not None:
                exec(_module([n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign))]), g)
            ns = LoggingNamespace(rec)
            for k, v in g.items():
                if k != "__builtins__":
                    dict.__setitem__(ns, k, v)
            if func is not None:
                params = [a.arg for a in func.args.args]
                defaults = list(func.args.defaults)
                values = {}
                for p in params:
                    values[p] = param_value
                if defaults:
                    for p, d in zip(params[-len(defaults):], defaults):
                        values[p] = eval(compile(ast.Expression(d), "<d>", "eval"), g)
                for p, v in values.items():
                    dict.__setitem__(ns, p, v)
            exec(_module(pre), g, ns)
            for k in list(ns.keys()):
                dict.__setitem__(ns, k, _track(dict.__getitem__(ns, k), rec))
            iterable = eval(compile(ast.Expression(loop.iter), "<iter>", "eval"), g, ns)
            items = []
            for n, item in enumerate(iterable):
                if n >= MAX_ITERATIONS:
                    break
                items.append(item)
            assign_target = _module([ast.Assign(targets=[loop.target], value=ast.Name("_oracle_item", ast.Load()))])
            body_code = _module(body)
            for k, item in enumerate(items):
                rec.start_iteration(k)
                dict.__setitem__(ns, "_oracle_item", item)
                exec(assign_target, g, ns)
                rec.active = True
                gk = _Globals(g, ns)               # nested scopes (genexprs, lambdas) see current locals
                try:
                    exec(body_code, gk, ns)
                except _Continue:
                    pass
                finally:
                    rec.active = False
    except _Break:
        return {"label": UNDEFINED, "reason": "early exit"}
    except Exception as e:  # noqa: BLE001 - any runtime failure makes the sample non-analysable
        return {"label": None, "reason": f"runtime error: {type(e).__name__}: {e}"}

    if len(items) < 2:
        return {"label": None, "reason": "fewer than two iterations executed"}

    ignore = loop_vars | {"_oracle_item"}
    for name, reads in rec.exposed_reads.items():
        if name in ignore:
            continue
        writes = rec.scalar_writes.get(name, set())
        if writes and any(any(w < r for w in writes) for r in reads):
            return {"label": UNDEFINED, "reason": f"loop-carried scalar '{name}'"}

    verdict = _container_verdict(rec)
    if verdict:
        return {"label": UNDEFINED, "reason": verdict}
    return {"label": PARALLELIZABLE, "reason": "no cross-iteration dependence observed"}


def _container_verdict(rec):
    """Returns the reason of a cross-iteration conflict on containers, or None."""
    containers = {cid for cid, _ in rec.elem_writes} | {cid for cid, _ in rec.elem_reads} | \
        set(rec.appends) | set(rec.whole_reads)
    for cid in containers:
        writes = {key: its for (c, key), its in rec.elem_writes.items() if c == cid}
        reads = {key: its for (c, key), its in rec.elem_reads.items() if c == cid}
        appended = rec.appends.get(cid, set())
        whole = rec.whole_reads.get(cid, set())
        if not writes and not appended:
            continue                                   # read-only inside the loop
        whole_writes = set().union(*[its for key, its in writes.items() if key in ("slice", "update")]) \
            if any(key in ("slice", "update") for key in writes) else set()
        all_reads = set().union(whole, *reads.values()) if (whole or reads) else set()
        if whole_writes and len(whole_writes | all_reads) > 1:
            return "whole-container update inside the loop"
        for key, w_iters in writes.items():
            if key in ("slice", "update"):
                continue
            if len(w_iters) > 1:
                return "the same container element is written by different iterations"
            if reads.get(key, set()) - w_iters:
                return "container element written in one iteration and read in another"
            if whole - w_iters:
                return "container written by index and read as a whole in another iteration"
        if appended and all_reads:
            return "list appended to and read inside the loop"
        if appended and writes:
            return "list appended to and written by index inside the loop"
    return None


def _worker(code, q):
    q.put(analyze(code))


def analyze_isolated(code, timeout=5.0):
    """Runs :func:`analyze` in a separate process with a time limit (for untrusted samples)."""
    q = mp.Queue()
    p = mp.Process(target=_worker, args=(code, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return {"label": None, "reason": "timeout"}
    return q.get() if not q.empty() else {"label": None, "reason": "crashed"}
