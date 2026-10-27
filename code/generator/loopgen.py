"""Decodes a genome (a vector of integer genes) into a minimal pair of Python loop samples.

Every genome yields two programs that share the same skeleton: wrapper (function or script),
names, data literals, iteration form, expressions and distractor statements. The two programs
differ only in the statement(s) that decide whether a value flows between iterations, so the
Parallelizable and Undefined variants have the same surface vocabulary.

Loop families (P = Parallelizable variant, U = Undefined variant):

A  private temporary vs. accumulator      P: t = e(x); t += c     U: t += e(x); t += c
B  read neighbour of input vs. of output  P: r[i] = s[i] + s[i-1] U: r[i] = r[i-1] + s[i]
C  factor from invariant vs. from itself  P: t = k * c            U: t = t * c
D  constant reference vs. previous value  P: d = d * c           U: prev = cur
E  index-based vs. counter-based label    P: num = i + 1          U: num = num + 1
F  direct vs. indirect element write      P: r[i] += x % k        U: r[x % k] += 1
G  clamp vs. running extreme              P: best = x             U: lim = x
H  skip vs. early exit                    P: continue             U: break
I  unique vs. shared dictionary keys      P: d[i * k // k] = ...  U: d[i // k * k] = ...
"""

import random

N_GENES = 20
GENE_MAX = 1000

FAMILIES = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
# iteration forms: plain list, range(len()) with indexing, enumerate, range(N), zip of two lists
FORMS = {
    "A": ["list", "rangelen", "enumerate", "rangeN", "zip"],
    "B": ["rangelen1"],
    "C": ["list", "rangelen", "enumerate", "rangeN", "zip"],
    "D": ["list", "rangelen", "enumerate", "rangeN"],
    "E": ["enumerate"],
    "F": ["enumerate", "rangelen"],
    "G": ["list", "rangelen", "enumerate", "rangeN", "zip"],
    "H": ["list", "rangelen", "enumerate", "rangeN", "zip"],
    "I": ["enumerate"],
}

# (pt list name, en list name, pt item, en item, kind, value generator id)
DOMAINS = [
    ("temperaturas", "temperatures", "temp", "temp", "float", (10, 40)),
    ("precos", "prices", "preco", "price", "float", (1, 500)),
    ("vendas", "sales", "venda", "sale", "int", (0, 1000)),
    ("notas", "grades", "nota", "grade", "float", (0, 10)),
    ("leituras", "readings", "leitura", "reading", "float", (0, 100)),
    ("distancias", "distances", "distancia", "distance", "int", (1, 300)),
    ("salarios", "salaries", "salario", "salary", "int", (1000, 9000)),
    ("idades", "ages", "idade", "age", "int", (1, 90)),
    ("valores", "values", "valor", "value", "int", (-50, 200)),
    ("pesos", "weights", "peso", "weight", "float", (0.5, 120)),
    ("pontos", "scores", "ponto", "score", "int", (0, 100)),
    ("medidas", "measures", "medida", "measure", "float", (0, 50)),
    ("palavras", "words", "palavra", "word", "str", "words"),
    ("nomes", "names", "nome", "name", "str", "names"),
    ("arquivos", "files", "arquivo", "file_name", "str", "files"),
    ("cidades", "cities", "cidade", "city", "str", "cities"),
    ("codigos", "codes", "codigo", "code", "str", "codes"),
]
STR_POOLS = {
    "words": ["python", "codigo", "laco", "dados", "vetor", "matriz", "texto", "parallel", "thread",
              "kernel", "cache", "memoria", "tarefa", "fila", "pilha", "grafo"],
    "names": ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fabio", "Gabi", "Hugo", "Iris", "Joao",
              "Karen", "Lucas", "Marta", "Nina", "Otavio", "Paula"],
    "files": ["relatorio.pdf", "imagem.jpg", "planilha.xlsx", "notas.txt", "dados.csv", "foto.png",
              "backup.zip", "script.py", "tabela.ods", "audio.mp3", "video.mp4", "config.json"],
    "cities": ["Recife", "Olinda", "Natal", "Salvador", "Fortaleza", "Maceio", "Belem", "Manaus",
               "Curitiba", "Porto Alegre", "Goiania", "Vitoria", "Teresina", "Aracaju"],
    "codes": ["A12", "B07", "C33", "D41", "E05", "F18", "G27", "H09", "J14", "K22", "L30", "M11"],
}

NAMES = {
    "res": (["resultados", "saida", "convertidos", "ajustados", "historico", "processados",
             "lista_final", "valores_finais", "registros", "saidas"],
            ["results", "output", "converted", "adjusted", "history", "processed", "final_list",
             "final_values", "records", "outputs"]),
    # every scalar role draws from this single pool: a name never reveals its role
    "scalar": (["total", "acumulado", "soma", "parcial", "fator", "escala", "taxa", "coef", "ajuste",
                "anterior", "atual", "referencia", "delta", "diferenca", "contador", "numero",
                "posicao", "limite", "melhor", "maximo", "corrente", "base", "nivel", "valor_ref"],
               ["total", "running", "acc", "partial", "factor", "scale", "rate", "coef", "adj",
                "prev", "current", "reference", "delta", "diff", "counter", "number", "position",
                "limit", "best", "max_value", "level", "base", "threshold", "ref_value"]),
    "dict": (["grupos", "contagem", "mapa", "totais", "agrupado"],
             ["groups", "counts", "mapping", "totals", "grouped"]),
    "idx": (["i", "idx", "pos", "k"], ["i", "idx", "pos", "j"]),
    "other": (["outros", "auxiliar", "extras", "segunda_lista"], ["others", "aux", "extras", "second_list"]),
}
VERBS = (["calcular", "processar", "gerar", "converter", "ajustar", "normalizar", "analisar",
          "agrupar", "filtrar", "transformar", "montar", "atualizar"],
         ["compute", "process", "build", "convert", "adjust", "normalize", "analyze", "group",
          "filter", "transform", "prepare", "update"])
PREFIXES = (["item", "registro", "linha", "entrada"], ["item", "record", "row", "entry"])
COMMENTS = (["# percorre os dados de entrada", "# processa cada elemento", "# monta a lista de saida",
             "# laco principal"],
            ["# iterate over the input data", "# process each element", "# build the output list",
             "# main loop"])

NUM_EXPR = ["{x} * {c}", "{x} + {c}", "{x} - {c}", "round({x} / {c}, 2)", "{x} ** 2",
            "abs({x} - {c})", "round(math.sqrt(abs({x})), 2)", "max({x}, {c})", "min({x}, {c})",
            "round({x} * {c}, 1)", "{x} // {c}"]
STR_EXPR = ["{x}.upper()", "{x}.lower()", "{x}[::-1]", "{x} + \"_ok\"", "f\"{{{x}}}_{c}\"",
            "{x}.capitalize()", "{x}.replace(\"a\", \"o\")", "{x}[:3]"]
NUM_COND = ["{x} < {c}", "{x} > {c}", "{x} == {c}", "{x} % 2 == 0"]
STR_COND = ["len({x}) < {c}", "{x}.startswith(\"a\")", "len({x}) > {c}", "\"a\" not in {x}"]
CONSTS = [1, 2, 3, 4, 5, 10, 0.5, 1.5, 2.5, 7, 12]
SMALL_K = [2, 3, 4]
OPS = ["+", "-"]


def _pick(gene, options):
    return options[gene % len(options)]


class _Names:
    """Hands out distinct identifiers for one sample."""

    def __init__(self, lang, genes_offset):
        self.lang = lang
        self.used = set()
        self.offset = genes_offset

    def get(self, role, gene):
        pool = NAMES[role][self.lang]
        for j in range(len(pool)):
            name = pool[(gene + j) % len(pool)]
            if name not in self.used:
                self.used.add(name)
                return name
        name = f"{pool[gene % len(pool)]}_{len(self.used)}"
        self.used.add(name)
        return name

    def take(self, name):
        if name in self.used:
            name = f"{name}_v"
        self.used.add(name)
        return name


def _values(rng, dom, length, unique=False):
    kind, spec = dom[4], dom[5]
    if kind == "str":
        pool = STR_POOLS[spec]
        return rng.sample(pool, min(length, len(pool)))
    lo, hi = spec
    out = []
    while len(out) < length:
        v = rng.randint(int(lo), int(hi)) if kind == "int" else round(rng.uniform(lo, hi), 1)
        if unique and v in out:
            continue
        out.append(v)
    return out


def _lit(v):
    return repr(v)


def decode(genome):
    """Returns {"P": code, "U": code, "meta": {...}} or raises ValueError for invalid genomes."""
    g = [int(x) % GENE_MAX for x in genome]
    fam = _pick(g[0], FAMILIES)
    form = _pick(g[1], FORMS[fam])
    is_func = (g[2] % 10) < 8
    param = g[3] % 3 if is_func else 0
    dom = _pick(g[4], DOMAINS)
    if fam == "B" and dom[4] == "str":            # neighbour arithmetic needs numbers
        dom = _pick(g[4], [d for d in DOMAINS if d[4] != "str"])
    lang = 0 if (g[5] % 10) < 7 else 1
    rng = random.Random(g[19] * 7919 + g[15])
    kind = dom[4]
    is_str = kind == "str"
    if is_str and form in ("rangeN", "zip"):
        form = "list"
    names = _Names(lang, 0)

    lst = names.take(dom[lang])
    item = names.take(dom[2 + lang])
    res = names.get("res", g[6])
    idx = names.get("idx", g[18])
    c = _pick(g[12], CONSTS)
    c2 = _pick(g[13], CONSTS)
    op = _pick(g[14], OPS)
    length = 5 + g[15] % 6
    extras = g[16]
    k_mod = _pick(g[17], SMALL_K)
    uses_math = False

    values = _values(rng, dom, length, unique=(fam == "I"))
    length = len(values)
    pre, header, xexpr = [], None, item

    # ----- iteration form ---------------------------------------------------------------------
    n_bound = None
    if form == "list":
        header = f"for {item} in {lst}:"
    elif form == "rangelen":
        header = f"for {idx} in range(len({lst})):"
        xexpr = f"{lst}[{idx}]"
    elif form == "rangelen1":
        header = f"for {idx} in range(1, len({lst})):"
        xexpr = f"{lst}[{idx}]"
    elif form == "enumerate":
        header = f"for {idx}, {item} in enumerate({lst}):"
    elif form == "rangeN":
        n_bound = "n" if (is_func and param == 2) else str(length)
        header = f"for {idx} in range({n_bound}):"
        xexpr = _pick(g[11], [f"{idx} * {c}", f"{idx} + {c}", f"{idx} * 0.5", f"{idx} ** 2"])
    elif form == "zip":
        other = names.get("other", g[7] + 3)
        item2 = names.take(dom[2 + lang] + "_2")
        pre.append(f"{other} = {_lit(_values(rng, dom, length))}")
        header = f"for {item}, {item2} in zip({lst}, {other}):"
        xexpr = _pick(g[11], [f"{item} * {item2}", f"{item} + {item2}", f"{item} - {item2}"])
    needs_list = form != "rangeN"
    if needs_list:
        pre.insert(0, f"{lst} = {_lit(values)}")

    numx = f"len({xexpr})" if is_str else xexpr

    def num_expr(x, gene=g[11]):
        nonlocal uses_math
        e = _pick(gene, NUM_EXPR)
        if "math." in e:
            uses_math = True
        return e.format(x=x, c=c)

    def str_expr(x, gene=g[11]):
        return _pick(gene, STR_EXPR).format(x=x, c=c)

    def val_expr(x):
        return str_expr(x) if is_str else num_expr(x)

    # ----- family-specific statements ---------------------------------------------------------
    body_p, body_u = [], []
    ret = res
    if fam == "A":
        acc = names.get("scalar", g[7])
        init = '""' if is_str else ("1" if op == "*" else "0")
        pre.append(f"{acc} = {init}")
        pre.append(f"{res} = []")
        suffix = _pick(g[13], ["_ok", "_v1", "_fim", "_novo", "_x"])
        tail = f'{acc} += "{suffix}"' if is_str else f"{acc} {op}= {c2}"
        body_p = [f"{acc} = {val_expr(xexpr)}", tail, f"{res}.append({acc})"]
        body_u = [f"{acc} += {val_expr(xexpr)}", tail, f"{res}.append({acc})"]
    elif fam == "B":
        pre.append(f"{res} = [0] * len({lst})")
        body_p = [f"{res}[{idx}] = {lst}[{idx}] {op} {lst}[{idx} - 1]"]
        body_u = [f"{res}[{idx}] = {res}[{idx} - 1] {op} {lst}[{idx}]"]
    elif fam == "C":
        k = names.get("scalar", g[7])
        t = names.get("scalar", g[8])
        pre.append(f"{k} = {c}")
        pre.append(f"{t} = 1")
        pre.append(f"{res} = []")
        body_p = [f"{t} = {k} * {c2}", f"{res}.append(round({numx} * {t}, 2))"]
        body_u = [f"{t} = {t} * {c2}", f"{res}.append(round({numx} * {t}, 2))"]
    elif fam == "D":
        prev = names.get("scalar", g[7])
        cur = names.get("scalar", g[8])
        diff = names.get("scalar", g[17])
        pre.append(f"{prev} = {c}")
        pre.append(f"{res} = []")
        head = [f"{cur} = {numx}", f"{diff} = {cur} - {prev}"]
        body_p = head + [f"{diff} = {diff} * {c2}", f"{res}.append({diff})"]
        body_u = head + [f"{prev} = {cur}", f"{res}.append({diff})"]
    elif fam == "E":
        num = names.get("scalar", g[7])
        prefix = _pick(g[17], PREFIXES[lang])
        pre.append(f"{num} = 0")
        pre.append(f"{res} = []")
        label = f'f"{prefix} {{{num}}}: {{{item}}}"'
        body_p = [f"{num} = {idx} + 1", f"{res}.append({label})"]
        body_u = [f"{num} = {num} + 1", f"{res}.append({label})"]
    elif fam == "F":
        key = f"len({xexpr})" if is_str else f"int({xexpr})"
        pre.append(f"{res} = [0] * len({lst})")
        body_p = [f"{res}[{idx}] += {key} % {k_mod}"]
        body_u = [f"{res}[{key} % {k_mod}] += 1"]
    elif fam == "G":
        lim = names.get("scalar", g[7])
        best = names.get("scalar", g[8])
        # the reference starts in the lower third of the data so that it is exceeded and updated
        lim_value = 4 if is_str else (1 if form == "rangeN" else sorted(values)[len(values) // 3])
        pre.append(f"{lim} = {_lit(lim_value)}")
        pre.append(f"{res} = []")
        body_p = [f"{best} = {lim}", f"if {numx} > {best}:", f"    {best} = {numx}", f"{res}.append({best})"]
        body_u = [f"{best} = {lim}", f"if {numx} > {best}:", f"    {lim} = {numx}", f"{res}.append({best})"]
    elif fam == "H":
        cond = _pick(g[17], STR_COND if is_str else NUM_COND).format(x=xexpr, c=c if not is_str else 5)
        pre.append(f"{res} = []")
        body_p = [f"if {cond}:", "    continue", f"{res}.append({val_expr(xexpr)})"]
        body_u = [f"if {cond}:", "    break", f"{res}.append({val_expr(xexpr)})"]
    elif fam == "I":
        dname = names.get("dict", g[7])
        value = f"len({item})" if is_str else num_expr(item)
        pre.append(f"{dname} = {{}}")
        # idx * k // k == idx never repeats a key; idx // k * k makes consecutive iterations share keys
        pkey, ukey = f"{idx} * {k_mod} // {k_mod}", f"{idx} // {k_mod} * {k_mod}"
        body_p = [f"{dname}[{pkey}] = {dname}.get({pkey}, 0) + {value}"]
        body_u = [f"{dname}[{ukey}] = {dname}.get({ukey}, 0) + {value}"]
        ret = dname

    # ----- shared distractors -----------------------------------------------------------------
    if extras & 2 and needs_list:
        qtd = names.take("quantidade" if lang == 0 else "count_items")
        pre.append(f"{qtd} = len({lst})")
    comment = [_pick(g[9], COMMENTS[lang])] if extras & 1 else []
    post_extra = []
    if extras & 4:
        tot = names.take("tamanho" if lang == 0 else "size")
        post_extra = [f"{tot} = len({ret})"]

    imports = []
    if uses_math:
        imports.append("import math")
    if extras & 8:
        imports.append(_pick(g[13], ["import random", "import string", "import math", "import time"]))

    def render(body):
        loop = [header] + ["    " + b for b in body]
        if is_func:
            verb = _pick(g[9], VERBS[lang])
            fname = f"{verb}_{dom[lang]}"
            args = "n" if param in (1, 2) else ""
            inner = pre + comment + loop + post_extra + [f"return {ret}"]
            lines = imports + ([""] if imports else []) + [f"def {fname}({args}):"] + ["    " + s for s in inner]
        else:
            msg = _pick(g[9], ["Resultado", "Saida", "Valores", "Final"] if lang == 0 else
                        ["Result", "Output", "Values", "Final"])
            lines = imports + ([""] if imports else []) + pre + comment + loop + post_extra + \
                [f'print("{msg}:", {ret})']
        return "\n".join(lines) + "\n"

    meta = {"family": fam, "form": form, "wrapper": "function" if is_func else "script",
            "domain": dom[0], "kind": kind, "lang": "pt" if lang == 0 else "en"}
    return {"P": render(body_p), "U": render(body_u), "meta": meta}


def random_genome(rng):
    return [rng.randrange(GENE_MAX) for _ in range(N_GENES)]


if __name__ == "__main__":
    r = random.Random(1)
    for _ in range(9):
        try:
            d = decode(random_genome(r))
        except ValueError:
            continue
        print("#", d["meta"])
        print("--- P ---")
        print(d["P"])
        print("--- U ---")
        print(d["U"])
