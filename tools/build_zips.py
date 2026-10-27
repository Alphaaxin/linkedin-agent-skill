#!/usr/bin/env python3
"""
Build one ZIP per skill in dist/, ready to upload in the Claude app
(Customize > Skills > + > Create skill > Upload a skill).

    python3 tools/build_zips.py

Skills that use the 21 hook formulas get their own copy of hooks.json, so each
ZIP works on its own.
"""

import glob
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
HOOKS = os.path.join(ROOT, "skills", "li-post", "hooks.json")
NEEDS_HOOKS = {"li-plan", "li-audit", "li-repurpose"}

os.makedirs(DIST, exist_ok=True)
for old in glob.glob(os.path.join(DIST, "*.zip")):
    os.remove(old)

for folder in sorted(glob.glob(os.path.join(ROOT, "skills", "li-*"))):
    name = os.path.basename(folder)
    out = os.path.join(DIST, f"{name}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(glob.glob(os.path.join(folder, "*"))):
            if os.path.isfile(path) and not path.endswith(".pyc"):
                z.write(path, f"{name}/{os.path.basename(path)}")
        if name in NEEDS_HOOKS:
            z.write(HOOKS, f"{name}/hooks.json")
    print(f"built dist/{name}.zip")
