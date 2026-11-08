#!/usr/bin/env python3

import ast
from copy import deepcopy
import os
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(sys.argv[1])
OUTPUT = Path(sys.argv[2])
DATA = Path(sys.argv[3])
REFERENCE = re.compile(r"(\S+\.xml)(?::\d+)?(?=\s|$)")
FIELD = re.compile(r"^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.+)$")
PATH_COMMENT = re.compile(r"^#\. \(itstool\) path: (.+)$")
PLACEHOLDER = re.compile(r"<_:([A-Za-z_][\w.-]*)-(\d+)/>")
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def parse_po(path):
    translations = {}
    ambiguous = set()
    references = set()
    tags = set()
    paths = set()
    entry = {}
    entry_tags = set()
    fuzzy = False
    field = None

    def finish_entry():
        nonlocal entry, entry_tags, fuzzy
        if (
            entry.get("msgid")
            and entry.get("msgstr")
            and not entry.get("msgid_plural")
            and "msgctxt" not in entry
            and not any(key.startswith("msgstr[") for key in entry)
            and not fuzzy
        ):
            for tag in entry_tags:
                key = (tag, entry["msgid"])
                value = entry["msgstr"]
                if key in translations and translations[key] != value:
                    ambiguous.add(key)
                else:
                    translations[key] = value
        entry = {}
        entry_tags = set()
        fuzzy = False

    with path.open(encoding="utf-8") as source:
        for line in source:
            line = line.strip()
            if not line:
                finish_entry()
                field = None
                continue
            if line.startswith("#"):
                if line.startswith("#,") and "fuzzy" in {
                    flag.strip() for flag in line[2:].split(",")
                }:
                    fuzzy = True
                match = PATH_COMMENT.match(line)
                if match:
                    source_path = match.group(1)
                    paths.add(source_path)
                    tag = source_path.rsplit("/", 1)[-1]
                    entry_tags.add(tag)
                    tags.add(tag)
                elif line.startswith("#:"):
                    references.update(REFERENCE.findall(line[2:]))
                continue

            match = FIELD.match(line)
            if match:
                field = match.group(1)
                entry[field] = ast.literal_eval(match.group(2))
            elif line.startswith('"') and field:
                entry[field] += ast.literal_eval(line)
            else:
                raise ValueError(f"Unrecognized PO syntax in {path}: {line}")

    finish_entry()
    for key in ambiguous:
        del translations[key]
        print(f"Ambiguous AppStream translation in {path}: {key[0]}={key[1]}", file=sys.stderr)
    return translations, tags, references, paths


def local_name(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else None


def node_source(element):
    parts = [element.text or ""]
    children = {}
    counts = {}
    for child in element:
        if not isinstance(child.tag, str):
            parts.append(child.tail or "")
            continue
        tag = local_name(child.tag)
        counts[tag] = counts.get(tag, 0) + 1
        placeholder = f"{tag}-{counts[tag]}"
        children[placeholder] = child
        parts.append(f"<_:{placeholder}/>")
        parts.append(child.tail or "")
    return "".join(parts).strip(), children


def translate_node(element, translation, children, translations, add_language=True):
    placeholders = PLACEHOLDER.findall(translation)
    if placeholders:
        actual = set(PLACEHOLDER.findall(translation))
        expected_tokens = {
            (key.rsplit("-", 1)[0], key.rsplit("-", 1)[1]) for key in children
        }
        if actual != expected_tokens or len(placeholders) != len(expected_tokens):
            return None
    elif children:
        return None

    result = deepcopy(element)
    if add_language:
        result.set(XML_LANG, "hr")
    if not children:
        result.text = translation
        return result

    for child in list(result):
        result.remove(child)
    pieces = PLACEHOLDER.split(translation)
    result.text = pieces[0]
    index = 1
    while index < len(pieces):
        key = f"{pieces[index]}-{pieces[index + 1]}"
        child = children.get(key)
        if child is None:
            return None
        clone = deepcopy(child)
        child_source, inline_children = node_source(child)
        child_translation = translations.get((local_name(child.tag), child_source))
        if child_translation:
            clone = translate_node(
                child, child_translation, inline_children, translations, add_language=False
            )
            if clone is None:
                return None
        clone.tail = pieces[index + 2]
        result.append(clone)
        index += 3
    return result


def has_hr_translation(children, start, tag):
    for sibling in children[start + 1:]:
        if local_name(sibling.tag) != tag:
            continue
        if sibling.attrib.get(XML_LANG) == "hr":
            return True
        if XML_LANG not in sibling.attrib:
            return False
    return False


catalogs = {}
references = {}
for po in sorted(ROOT.rglob("*.po")):
    relative_parts = po.relative_to(ROOT).parts
    if "output_mo" in relative_parts or ".git" in relative_parts:
        continue
    content = po.read_text(encoding="utf-8")
    if "#. (itstool) path:" not in content:
        continue
    translations, tags, po_references, paths = parse_po(po)
    if not tags or not po_references:
        continue
    for filename in po_references:
        references.setdefault(Path(filename).name, []).append((po, translations, tags, paths))

templates = {}
for directory in (DATA / "metainfo", DATA / "appdata"):
    if not directory.is_dir():
        continue
    for template in sorted(directory.glob("*.xml")):
        if template.is_file() and not template.is_symlink():
            templates.setdefault(template.name, template)

prepared = 0
for filename, matches in sorted(references.items()):
    template = templates.get(filename)
    if template is None:
        continue

    translations = {}
    ambiguous = set()
    tags = set()
    paths = set()
    for _, catalog, catalog_tags, catalog_paths in matches:
        tags.update(catalog_tags)
        paths.update(catalog_paths)
        for key, value in catalog.items():
            if key in translations and translations[key] != value:
                ambiguous.add(key)
            else:
                translations[key] = value
    for key in ambiguous:
        del translations[key]
        print(f"Ambiguous AppStream translation for {filename}: {key[0]}={key[1]}", file=sys.stderr)
    inline_tags = set()
    for path in paths:
        parent = path.rsplit("/", 1)[0] if "/" in path else ""
        if parent and any(other.endswith(f"/{parent}") or other == parent for other in paths):
            inline_tags.add(path.rsplit("/", 1)[-1])
    tags.difference_update(inline_tags)

    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    tree = ET.parse(template, parser=parser)
    root = tree.getroot()
    changed = False
    for parent in root.iter():
        children = list(parent)
        for index, element in enumerate(children):
            tag = local_name(element.tag)
            if tag not in tags or XML_LANG in element.attrib:
                continue
            source, inline_children = node_source(element)
            translated = translations.get((tag, source))
            if not translated or has_hr_translation(children, index, tag):
                continue
            localized = translate_node(element, translated, inline_children, translations)
            if localized is None:
                print(f"Skipping unsupported inline markup in {template}: {tag}={source}", file=sys.stderr)
                continue
            localized.tail = element.tail
            parent.insert(list(parent).index(element) + 1, localized)
            changed = True

    if not changed:
        continue
    relative = template.relative_to(DATA)
    destination = OUTPUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="utf-8", xml_declaration=True)
    sys.stdout.buffer.write(os.fsencode(str(relative)) + b"\0")
    prepared += 1

print(f"Prepared {prepared} localized AppStream files", file=sys.stderr)
