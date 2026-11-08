#!/usr/bin/env python3

import gettext
import io
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(sys.argv[1])
OUTPUT = Path(sys.argv[2])
DATA = Path(sys.argv[3])
REFERENCE = re.compile(r"(\S+\.desktop)(?::\d+)?(?=\s|$)")
KEY = re.compile(r"^([^=\[\]]+)(?:\[([^]]+)\])?=(.*)$")
ESCAPES = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\"}


def unescape(value):
    return re.sub(r"\\([sntr\\])", lambda m: ESCAPES[m.group(1)], value)


def escape(value):
    return (value.replace("\\", "\\\\").replace("\n", "\\n")
            .replace("\t", "\\t").replace("\r", "\\r"))


references = {}
for po in sorted(ROOT.rglob("*._desktop_.po")):
    if "output_mo" in po.relative_to(ROOT).parts or ".git" in po.relative_to(ROOT).parts:
        continue
    with po.open(encoding="utf-8") as source:
        for line in source:
            if line.startswith("#:"):
                for source_path in REFERENCE.findall(line):
                    references.setdefault(Path(source_path).name, set()).add((po, source_path))

catalogs = {}
for template in sorted(DATA.rglob("*.desktop")):
    matches = references.get(template.name, ())
    if not matches or not template.is_file() or template.is_symlink():
        continue
    installed_parts = template.relative_to(DATA).parts[:-1]
    project_matches = [
        match for match in matches
        if match[0].relative_to(ROOT).parts[0] in installed_parts
    ]
    if project_matches:
        matches = project_matches
    lines = template.read_text(encoding="utf-8").splitlines(keepends=True)
    translations = {}
    conflicts = set()
    for po, source_path in sorted(matches):
        catalog_key = (po, source_path)
        if catalog_key not in catalogs:
            filtered = subprocess.run(
                ["msggrep", "-N", source_path, str(po)],
                check=True, stdout=subprocess.PIPE,
            ).stdout
            mo = subprocess.run(
                ["msgfmt", "-o", "-", "-"],
                input=filtered, check=True, stdout=subprocess.PIPE,
            ).stdout
            catalogs[catalog_key] = gettext.GNUTranslations(io.BytesIO(mo))
        catalog = catalogs[catalog_key]
        for line in lines:
            match = KEY.match(line.rstrip("\r\n"))
            if not match or match.group(2):
                continue
            key, _, value = match.groups()
            original = unescape(value)
            translated = catalog.pgettext(key, original)
            if translated == original:
                continue
            identity = (key, value)
            if identity in translations and translations[identity] != translated:
                conflicts.add(identity)
            else:
                translations[identity] = translated

    for identity in conflicts:
        del translations[identity]
        print(f"Ambiguous translation for {template}: {identity[0]}={identity[1]}", file=sys.stderr)
    if not translations:
        continue

    result = []
    replaced = set()
    section = 0
    keys = {}
    for line in lines:
        if line.startswith("[") and line.rstrip().endswith("]"):
            section += 1
        match = KEY.match(line.rstrip("\r\n"))
        if match and not match.group(2):
            key, _, value = match.groups()
            keys[(section, key)] = value
    section = 0
    for line in lines:
        if line.startswith("[") and line.rstrip().endswith("]"):
            section += 1
        match = KEY.match(line.rstrip("\r\n"))
        if match:
            key, language, value = match.groups()
            if language == "hr":
                identity = (key, keys.get((section, key)))
                if identity in translations:
                    continue
            elif language is None and (key, value) in translations:
                result.append(line if line.endswith("\n") else line + "\n")
                result.append(f"{key}[hr]={escape(translations[(key, value)])}\n")
                replaced.add((section, key))
                continue
        result.append(line)
    if replaced:
        relative = template.relative_to(DATA)
        destination = OUTPUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("".join(result), encoding="utf-8")
        sys.stdout.buffer.write(os.fsencode(str(relative)) + b"\0")
