#!/usr/bin/env python3
"""
humanize.py - strip the machine fingerprint out of a draft.

What it changes automatically (safe, meaning-preserving fixes only):

  1. INVISIBLE   delete or normalise the characters a human keyboard never
                 produces: zero-width joiners, word joiners, soft hyphens,
                 BOMs, Unicode tag characters, non-breaking and narrow spaces.
  2. TYPOGRAPHIC en dash -> hyphen, hyphen look-alikes (non-breaking hyphen,
                 minus sign) -> hyphen, curly quotes -> straight,
                 ellipsis -> three dots, bullet -> hyphen.

What it only FLAGS, with the line it sits on (needs judgement, so the writer
or the model rewrites it):

  3. EM DASHES   an em dash can become a comma, a full stop, a colon or a pair
                 of brackets depending on the sentence. Swapping it blindly for
                 a comma creates comma splices, so it is flagged, not replaced.
  4. LEXICAL     slop words and phrases from slop.json, each with a suggested
                 plain alternative. A one-for-one word swap does not read the
                 sentence ("leverage synergy" -> "use overlap"), so the default
                 is to flag. --swap-words restores the old automatic swap.
  5. STRUCTURAL  rule-of-three, "not just X, it's Y", hashtag walls and the rest.

Usage
  python3 humanize.py draft.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py draft.txt --json
  python3 humanize.py draft.txt -o clean.txt
  python3 humanize.py draft.txt --report --swap-words --fix-dashes   # old behaviour
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Swap URLs for placeholders so no pass rewrites inside a link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Delete or space-normalise invisible characters. Returns (text, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Any remaining Cf (format) character is invisible by definition.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "other invisible format chars", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def _line_of(text, idx, width=70):
    """The line containing position idx, trimmed for a report."""
    start = text.rfind("\n", 0, idx) + 1
    end = text.find("\n", idx)
    line = text[start:end if end != -1 else len(text)].strip()
    line = re.sub("\x00URL\\d+\x00", "<link>", line)
    return line if len(line) <= width else line[: width - 3] + "..."


def flag_em_dashes(text):
    """Report each em dash with its line. Does not change the text."""
    flags = []
    for m in re.finditer("—", text):
        flags.append(_line_of(text, m.start()))
    return flags


def pass_typographic(text, lex, fix_dashes=False):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        if ch == "—" and not fix_dashes:
            continue  # flagged separately; rewriting it needs judgement
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(space)"})
        if ch == "—":
            # " word — word " and "word—word" both collapse to a comma + space.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # used as em dash
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # A comma inserted before existing punctuation reads wrong.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _lex_pattern(find):
    return re.compile(r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b",
                      re.IGNORECASE)


def flag_lexical(text, lex):
    """Find slop words and phrases, longest first, without changing the text.
    A word inside an already-flagged phrase is not flagged twice."""
    hits, taken = [], []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        lines = []
        for m in _lex_pattern(entry["find"]).finditer(text):
            if any(a <= m.start() < b for a, b in taken):
                continue
            taken.append((m.start(), m.end()))
            lines.append(_line_of(text, m.start()))
        if lines:
            hits.append({"find": entry["find"], "replace": entry["replace"] or "(cut it)",
                         "count": len(lines), "family": entry["family"], "lines": lines})
    return hits


def pass_lexical(text, lex):
    """Old behaviour, behind --swap-words: replace slop words and phrases."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = _lex_pattern(find)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(deleted)",
                     "count": len(found), "family": entry["family"], "lines": []})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Clean up after deletions.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*([,.;:])\s*", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # An em dash that became a comma, followed by a sentence connective, leaves
    # a splice ("is important, also, it's proof"). Promote it to a full stop.
    text = re.sub(r",\s*(also|so|still|basically|in the end)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Sentence-length uniformity is structural too.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Uniform sentence length (variation {cv:.2f})",
                "count": len(lens),
                "fix": "Break one sentence in half. Let another run long. Machines write even.",
            })
    return flags


def humanize(text, lex, swap_words=False, fix_dashes=False):
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex, fix_dashes=fix_dashes)
    dashes = flag_em_dashes(text)
    if swap_words:
        text, lexi = pass_lexical(text, lex)
    else:
        lexi = flag_lexical(text, lex)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "em_dashes": dashes,
        "lexical": lexi,
        "lexical_swapped": swap_words,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    swapped = report.get("lexical_swapped")
    fixed = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + (sum(h["count"] for h in report["lexical"]) if swapped else 0)
    to_rewrite = len(report["em_dashes"]) + len(report["structures"]) \
        + (0 if swapped else sum(h["count"] for h in report["lexical"]))

    head("HUMANIZE REPORT")
    print(f"{fixed} characters cleaned automatically, "
          f"{to_rewrite} items flagged for a by-hand rewrite", file=out)

    if report["invisible"]:
        head("1. INVISIBLE CHARACTERS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TYPOGRAPHY")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["em_dashes"]:
        head("3. EM DASHES  (rewrite: comma, full stop, colon or brackets - pick by sentence)")
        for line in report["em_dashes"]:
            print(f"        {line}", file=out)
    if report["lexical"]:
        if swapped:
            head("4. SLOP LEXICON  (swapped automatically - re-read these sentences)")
        else:
            head("4. SLOP LEXICON  (not changed - rewrite the sentence, the suggestion is a hint)")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> try: {h['replace']}   [{h['family']}]", file=out)
            for line in h["lines"][:3]:
                print(f"        {line}", file=out)
    if report["structures"]:
        head("5. STRUCTURAL TELLS  (not auto-fixed - rewrite these yourself)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report[k] for k in ("invisible", "typographic", "em_dashes", "lexical", "structures")):
        head("CLEAN")
        print("  Nothing to strip.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Strip the machine fingerprint out of a draft.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("-o", "--out", help="write cleaned text here instead of stdout")
    ap.add_argument("--report", action="store_true", help="print what changed, to stderr")
    ap.add_argument("--json", action="store_true", help="emit {text, report} as JSON")
    ap.add_argument("--lexicon", default=LEX, help="path to slop.json")
    ap.add_argument("--swap-words", action="store_true",
                    help="auto-replace slop words (old behaviour; re-read the result)")
    ap.add_argument("--fix-dashes", action="store_true",
                    help="auto-replace em dashes with commas (old behaviour; can create splices)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, swap_words=args.swap_words, fix_dashes=args.fix_dashes)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
