#!/usr/bin/env python3
"""
Checks that the pack is intact and the humanizer behaves as documented.

    python3 tests/run_tests.py

No packages needed. Exits non-zero if anything fails.
"""

import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUMAN = os.path.join(ROOT, "skills", "li-human")
HUMANIZE = os.path.join(HUMAN, "humanize.py")
DETECT = os.path.join(HUMAN, "detect.py")

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def run(script, text, *args):
    p = subprocess.run([sys.executable, "-I", script, "-", *args],
                       input=text, capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def humanize(text, *args):
    code, out, err = run(HUMANIZE, text, "--json", *args)
    if code != 0:
        raise RuntimeError(err)
    return json.loads(out)


def verdict(text):
    code, out, err = run(DETECT, text, "--json")
    if code != 0:
        raise RuntimeError(err)
    data = json.loads(out)
    return data.get("verdict"), data.get("overall")


# 1. Pack structure ---------------------------------------------------------

skills = sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")))
check("11 skills present", len(skills) == 11, f"found {len(skills)}")
for path in skills:
    folder = os.path.basename(os.path.dirname(path))
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    name = re.search(r"^name:\s*(\S+)", m.group(1), re.M) if m else None
    check(f"{folder}: header valid", m and name and name.group(1) == folder)
    check(f"{folder}: has description", m and "description:" in m.group(1))

for rel in ["skills/li-post/hooks.json", "skills/li-human/slop.json",
            "skills/li-profile/rubric.json", ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json"]:
    try:
        json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
        check(f"{rel} is valid JSON", True)
    except Exception as e:  # noqa: BLE001
        check(f"{rel} is valid JSON", False, str(e))

hooks = json.load(open(os.path.join(ROOT, "skills/li-post/hooks.json"), encoding="utf-8"))
check("21 hook formulas", len(hooks["hooks"]) == 21, f"found {len(hooks['hooks'])}")
rubric = json.load(open(os.path.join(ROOT, "skills/li-profile/rubric.json"), encoding="utf-8"))
total = sum(i["points"] for i in rubric["items"])
check("profile rubric adds up to 100", total == 100, f"adds up to {total}")
check("voice template ships inside li-post",
      os.path.exists(os.path.join(ROOT, "skills/li-post/voice-template.md")))

# Every /li-xxx a skill mentions must exist.
names = {os.path.basename(os.path.dirname(p)) for p in skills}
for path in skills:
    for ref in set(re.findall(r"/(li-[a-z]+)", open(path, encoding="utf-8").read())):
        check(f"{os.path.basename(os.path.dirname(path))} -> /{ref} exists", ref in names)

# 2. humanize.py ------------------------------------------------------------

r = humanize("Hello​ world again.")
check("deletes zero-width space", "​" not in r["text"])
check("normalises non-breaking space", " " not in r["text"])

r = humanize("It’s a “good” fast‑paced week…")
check("curly quotes and ellipsis straightened",
      r["text"].strip() == 'It\'s a "good" fast-paced week...', r["text"])

r = humanize("We shipped it — finally.")
check("em dash kept, not swapped", "—" in r["text"])
check("em dash flagged with its line", r["report"]["em_dashes"] == ["We shipped it — finally."])

r = humanize("We leverage synergy to delve in.")
check("slop words kept by default", r["text"].strip() == "We leverage synergy to delve in.")
check("slop words flagged", {h["find"] for h in r["report"]["lexical"]} >= {"leverage", "synergy", "delve"})

r = humanize("In today's fast-paced world we win.")
found = [h["find"] for h in r["report"]["lexical"]]
check("phrase flagged once, not also its words", found == ["in today's fast-paced world"], str(found))

r = humanize("We leverage it.", "--swap-words")
check("--swap-words still replaces", r["text"].strip() == "We use it.", r["text"])

r = humanize("Read https://example.com/leverage—guide now.")
check("URLs never touched", "https://example.com/leverage—guide" in r["text"], r["text"])

r = humanize("")
check("empty input does not crash", r["text"] == "\n")

r = humanize("It's not just a tool, it's a mindset. Thoughts?")
check("structural tells flagged", len(r["report"]["structures"]) >= 2)

# 3. detect.py --------------------------------------------------------------

AI = ("In today's fast-paced world, it's crucial to leverage synergy — let's delve in.​\n\n"
      "It's not just a tool, it's a mindset. The result? A robust, seamless, scalable workflow.\n\nThoughts?\n")
HUMAN_POST = ("Last March a client walked away from a “signed” deal. We had no contract.\n\n"
              "It cost us $18,000 and two months of payroll for Priya and Sam. I still think about the email. "
              "Four words, sent at 11pm on a Sunday.\n\nNow every job gets a one-page agreement before we write "
              "a line of code. It takes me nine minutes. Clients don’t push back, they’re relieved.\n\n"
              "What’s the cheapest thing you’ve skipped that cost you the most?\n")
v, score = verdict(AI)
check("AI-pattern draft is FLAGGED", v == "FLAGGED", f"{v} {score}")
v, score = verdict(HUMAN_POST)
check("specific human post PASSES (curly quotes allowed)", v == "PASS", f"{v} {score}")

# Report --------------------------------------------------------------------

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   ({detail})" if detail and not ok else ""))
print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
sys.exit(1 if failed else 0)
