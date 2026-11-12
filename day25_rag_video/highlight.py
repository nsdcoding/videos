"""Turn a Python file into VS Code Dark+ style HTML lines -> src/code_<name>.js"""
import html, io, json, keyword, sys, tokenize

CTRL = {"import", "from", "for", "if", "elif", "else", "return", "continue", "with", "as",
        "try", "except", "in", "while", "break", "pass", "raise", "not", "is", "and", "or"}
BLUE = {"def", "class", "None", "True", "False", "lambda"}
BUILTIN = {"print", "len", "open", "sorted", "range", "enumerate", "round", "str", "int", "list", "dict"}
MODULES = {"os", "re"}


def highlight(path):
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    out = [[] for _ in lines]          # per line list of (col_start, col_end, cls)
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    sig = [t for t in toks if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                             tokenize.DEDENT, tokenize.COMMENT, tokenize.ENDMARKER)]
    nxt = {id(t): (sig[i + 1] if i + 1 < len(sig) else None) for i, t in enumerate(sig)}
    prv = {id(t): (sig[i - 1] if i > 0 else None) for i, t in enumerate(sig)}
    for t in toks:
        ty = t.type
        if ty == tokenize.COMMENT:
            cls = "cm"
        elif ty == tokenize.STRING or ty in (getattr(tokenize, "FSTRING_START", -1),
                                             getattr(tokenize, "FSTRING_MIDDLE", -1),
                                             getattr(tokenize, "FSTRING_END", -1)):
            cls = "st"
        elif ty == tokenize.NUMBER:
            cls = "nu"
        elif ty == tokenize.NAME:
            n, p = nxt.get(id(t)), prv.get(id(t))
            if t.string in CTRL:
                cls = "kc"
            elif t.string in BLUE:
                cls = "kb"
            elif p is not None and p.string in ("def",):
                cls = "fn"
            elif n is not None and n.string == "(":
                cls = "cl" if t.string[:1].isupper() else "fn"
            elif t.string in MODULES or t.string[:1].isupper() and not t.string.isupper():
                cls = "cl"
            elif t.string.isupper() and len(t.string) > 1:
                cls = "co"
            else:
                cls = "va"
        elif ty == tokenize.OP:
            cls = "op"
        else:
            continue
        (sr, sc), (er, ec) = t.start, t.end
        for r in range(sr, er + 1):
            a = sc if r == sr else 0
            b = ec if r == er else len(lines[r - 1])
            if b > a:
                out[r - 1].append((a, b, cls))
    res = []
    for i, line in enumerate(lines):
        spans = sorted(out[i])
        h, col = "", 0
        for a, b, cls in spans:
            if a < col:
                continue
            h += html.escape(line[col:a])
            h += f'<span class="{cls}">{html.escape(line[a:b])}</span>'
            col = b
        h += html.escape(line[col:])
        res.append(h)
    return res, lines


if __name__ == "__main__":
    for name in sys.argv[1:]:
        res, raw = highlight(f"assets/{name}.py")
        with open(f"src/code_{name}.js", "w") as f:
            f.write(f"window.CODE=window.CODE||{{}};CODE[{json.dumps(name)}]={json.dumps(res)};\n")
            f.write(f"window.RAW=window.RAW||{{}};RAW[{json.dumps(name)}]={json.dumps(raw)};\n")
        print(name, len(res))
