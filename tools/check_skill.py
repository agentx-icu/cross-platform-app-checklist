#!/usr/bin/env python3
"""Consistency check for the skill: frontmatter, checklist IDs, links, hygiene.

Run from the repository root: python3 tools/check_skill.py
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
REFS = ROOT / "references"
CATALOG = REFS / "checklist.md"
STABLE_IDS = {f"{prefix}{number}" for prefix, count in
              (("L", 8), ("D", 7), ("I", 9), ("B", 8), ("P", 9),
               ("M", 8), ("W", 4), ("F", 3), ("X", 9))
              for number in range(1, count + 1)}

ID_IN_CHECKLIST = re.compile(r"^- \*\*([A-Z]\d+[a-z]?) ", re.M)
ID_HEADING = re.compile(r"^## ([A-Z]\d+[a-z]?) ", re.M)
SECTION = re.compile(r"^### .*?\]\(([\w.-]+\.md)\)", re.M)
LINK = re.compile(r"\]\(([^)#\s]*)(?:#([^)\s]*))?\)")
HEADING = re.compile(r"^#{1,6} (.+?)\s*$", re.M)
FORBIDDEN = [
    (re.compile(r"\b10\.\d+\.\d+\.\d+\b"), "private IPv4 address"),
    (re.compile(r"\b172\.(1[6-9]|2\d|3[01])\.\d+\.\d+\b"), "private IPv4 address"),
    (re.compile(r"\b192\.168\.\d+\.\d+\b"), "private IPv4 address"),
    (re.compile(r"\b100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+\b"), "CGNAT address"),
    (re.compile(r"\b[\w-]+\.(?:internal|corp|intranet|lan)\b"), "internal hostname"),
    (re.compile(r"/Users/[\w.-]+"), "absolute macOS home path"),
    (re.compile(r"/home/[\w.-]+"), "absolute Linux home path"),
]

errors = []


def err(msg):
    errors.append(msg)


def check_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        err("SKILL.md: missing YAML frontmatter")
        return
    try:
        fields = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        err(f"SKILL.md: frontmatter is not valid YAML: {e}")
        return
    if not isinstance(fields, dict):
        err("SKILL.md: frontmatter must be a mapping")
        return
    name, desc = fields.get("name"), fields.get("description")
    if not isinstance(name, str) or not isinstance(desc, str):
        err("SKILL.md: name and description must be strings")
        return
    desc = desc.strip()
    if name != ROOT.name and name != "cross-platform-app-checklist":
        err(f"SKILL.md: frontmatter name {name!r} does not match the skill")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        err("SKILL.md: name must be lowercase letters, digits and hyphens")
    if not desc or len(desc) > 1024:
        err("SKILL.md: description must be 1-1024 characters")
    if fields.get("license") != "MIT-0":
        err("SKILL.md: license must be MIT-0")
    metadata = fields.get("metadata")
    version = metadata.get("version") if isinstance(metadata, dict) else None
    version_file = ROOT / "VERSION"
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        err("SKILL.md: metadata.version must be a semantic version string")
    elif not version_file.exists() or version_file.read_text().strip() != version:
        err("SKILL.md: metadata.version differs from VERSION")


def check_ids(text):
    listed_all = ID_IN_CHECKLIST.findall(text)
    if set(listed_all) != STABLE_IDS or len(listed_all) != len(STABLE_IDS):
        err("references/checklist.md: stable ID set must contain all 65 IDs exactly once")
    # Map each checklist section to its reference file, then compare IDs.
    sections = list(SECTION.finditer(text))
    if len(sections) != 9:
        err("references/checklist.md: expected nine linked area sections")
    for i, sec in enumerate(sections):
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        listed = ID_IN_CHECKLIST.findall(text[sec.end():end])
        ref = REFS / sec.group(1)
        if not ref.exists():
            err(f"references/checklist.md: section links to missing {sec.group(1)}")
            continue
        defined = ID_HEADING.findall(ref.read_text(encoding="utf-8"))
        for missing in sorted(set(listed) - set(defined)):
            err(f"{sec.group(1)}: no '## {missing} ...' heading for a catalog item")
        for extra in sorted(set(defined) - set(listed)):
            err(f"references/checklist.md: {extra} is defined in {sec.group(1)} but not listed")
        for dup in sorted({x for x in listed if listed.count(x) > 1}):
            err(f"references/checklist.md: {dup} listed twice")


def anchors(path):
    # GitHub heading slugs: lowercase, drop punctuation, spaces to hyphens.
    out = set()
    for h in HEADING.findall(path.read_text(encoding="utf-8")):
        h = re.sub(r"\]\([^)]*\)", "]", h)
        h = re.sub(r"[`*\[\]]", "", h).lower()
        out.add(re.sub(r"[^\w\- ]", "", h).replace(" ", "-"))
    return out


def check_file(path):
    raw = path.read_bytes()
    rel = path.relative_to(ROOT)
    if b"\r\n" in raw:
        err(f"{rel}: CRLF line endings")
    text = raw.decode("utf-8")
    for target, frag in LINK.findall(text):
        if re.match(r"[a-z]+:", target):
            continue
        dest = (path.parent / target).resolve() if target else path
        if not dest.exists():
            err(f"{rel}: broken link {target}")
        elif frag and dest.suffix == ".md" and frag not in anchors(dest):
            err(f"{rel}: broken anchor {target}#{frag}")
    for pattern, what in FORBIDDEN:
        for m in pattern.finditer(text):
            err(f"{rel}: {what}: {m.group(0)}")


def main():
    errors.clear()
    text = SKILL.read_text(encoding="utf-8")
    check_frontmatter(text)
    if CATALOG.exists():
        check_ids(CATALOG.read_text(encoding="utf-8"))
    else:
        err("references/checklist.md: missing catalog")
    paths = [p for p in sorted(ROOT.rglob("*.md")) if ".git" not in p.relative_to(ROOT).parts]
    for path in paths:
        check_file(path)
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
