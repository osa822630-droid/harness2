#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Validate the Claude plugin marketplace that ships with this repository.

Checks the layout Claude reads when a marketplace is added from a Git repository:
`.claude-plugin/marketplace.json` at the root, one plugin folder per entry, a
manifest, discovered skills/commands, and the README and license that the plugin
directory requires. Stdlib only, so it runs without the package installed.
"""

import json
import re
import sys
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_MARKETPLACE = ("name", "owner", "plugins")
REQUIRED_ENTRY = ("name", "source")
REQUIRED_PLUGIN = ("name", "version", "description", "license")
README_WORDS = 40


def _fail(failures, message):
    failures.append(message)


def _frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("'\"")
    return fields, text[end + 4 :]


def check_plugin(root, plugin_dir, entry, failures, label):
    """Check one plugin folder; returns the count of skills and commands found."""

    name = entry["name"]
    if not NAME.match(name):
        _fail(failures, f"{label}: name {name!r} is not kebab-case")
    if name.startswith(("claude-", "anthropic-")):
        _fail(failures, f"{label}: name {name!r} may not start with claude-/anthropic-")
    if not plugin_dir.is_dir():
        _fail(failures, f"{label}: source {entry['source']!r} does not exist")
        return 0, 0

    if (plugin_dir / "bin").is_dir():
        _fail(failures, f"{label}: a top-level bin/ stops claude.ai from installing the plugin")

    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = {}
    if not manifest_path.is_file():
        _fail(failures, f"{label}: missing .claude-plugin/plugin.json")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except ValueError as exc:
            _fail(failures, f"{label}: plugin.json is not valid JSON ({exc})")
        for field in REQUIRED_PLUGIN:
            if not manifest.get(field):
                _fail(failures, f"{label}: plugin.json is missing {field!r}")
        if manifest.get("name") and manifest["name"] != name:
            _fail(
                failures,
                f"{label}: marketplace entry name {name!r} != plugin.json name "
                f"{manifest['name']!r}",
            )

    readme = plugin_dir / "README.md"
    if not readme.is_file():
        _fail(failures, f"{label}: missing README.md")
    else:
        body = re.sub(r"```.*?```", "", readme.read_text(encoding="utf-8"), flags=re.S)
        words = len(re.findall(r"[A-Za-z0-9²-]+", body))
        if words < README_WORDS:
            _fail(failures, f"{label}: README.md has {words} words, needs {README_WORDS}")

    if not (plugin_dir / "LICENSE").is_file() and not manifest.get("license"):
        _fail(failures, f"{label}: no LICENSE file and no license field")

    skills_dir = plugin_dir / "skills"
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    for skill_dir in skills:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            _fail(failures, f"{label}/{skill_dir.name}: missing SKILL.md")
            continue
        fields, _ = _frontmatter(skill_md)
        if fields is None:
            _fail(failures, f"{label}/{skill_dir.name}: SKILL.md has no YAML frontmatter")
            continue
        if not fields.get("description"):
            _fail(failures, f"{label}/{skill_dir.name}: SKILL.md has no description")
        elif len(fields["description"]) > 1024:
            _fail(failures, f"{label}/{skill_dir.name}: description exceeds 1024 characters")
        if not NAME.match(skill_dir.name):
            _fail(failures, f"{label}/{skill_dir.name}: skill folder must be kebab-case")
        if fields.get("name") and fields["name"] != skill_dir.name:
            _fail(
                failures,
                f"{label}/{skill_dir.name}: skill name {fields['name']!r} != folder name",
            )

    commands_dir = plugin_dir / "commands"
    commands = sorted(commands_dir.glob("*.md")) if commands_dir.is_dir() else []
    for command in commands:
        fields, _ = _frontmatter(command)
        if not fields or not fields.get("description"):
            _fail(failures, f"{label}/commands/{command.name}: no description frontmatter")

    for agent in sorted((plugin_dir / "agents").glob("*.md")):
        fields, _ = _frontmatter(agent)
        if not fields or not fields.get("description"):
            _fail(failures, f"{label}/agents/{agent.name}: no description frontmatter")

    if not skills and not commands:
        _fail(failures, f"{label}: no skills/ or commands/, so the plugin does nothing")
    return len(skills), len(commands)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = Path(argv[0]).resolve() if argv else Path(__file__).resolve().parents[1]
    failures = []

    market_path = root / ".claude-plugin" / "marketplace.json"
    if not market_path.is_file():
        print("Plugin check failed: missing .claude-plugin/marketplace.json")
        return 1
    try:
        market = json.loads(market_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"Plugin check failed: marketplace.json is not valid JSON ({exc})")
        return 1

    for field in REQUIRED_MARKETPLACE:
        if not market.get(field):
            _fail(failures, f"marketplace.json: missing {field!r}")

    if not NAME.match(market.get("name", "")):
        _fail(failures, "marketplace.json: name must be kebab-case")
    owner = market.get("owner") or {}
    if isinstance(owner, dict) and not owner.get("name"):
        _fail(failures, "marketplace.json: owner needs a name")

    total_skills = total_commands = 0
    seen = set()
    for entry in market.get("plugins") or []:
        for field in REQUIRED_ENTRY:
            if not entry.get(field):
                _fail(failures, f"marketplace.json: a plugin entry is missing {field!r}")
        name = entry.get("name", "<unnamed>")
        if name in seen:
            _fail(failures, f"marketplace.json: duplicate plugin name {name!r}")
        seen.add(name)

        source = entry.get("source")
        if not isinstance(source, str):
            _fail(failures, f"marketplace.json: {name}: source must be a relative path")
            continue
        if not source.startswith("./"):
            _fail(failures, f"marketplace.json: {name}: source must start with './'")
        plugin_dir = (root / source).resolve()
        if root not in plugin_dir.parents:
            _fail(failures, f"marketplace.json: {name}: source escapes the repository")
            continue
        skills, commands = check_plugin(root, plugin_dir, entry, failures, name)
        total_skills += skills
        total_commands += commands

    if not market.get("plugins"):
        _fail(failures, "marketplace.json: plugins array is empty")

    if failures:
        print("Plugin check failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(
        f"PASS: marketplace {market['name']!r} "
        f"({len(market['plugins'])} plugin(s), {total_skills} skill(s), "
        f"{total_commands} command(s))"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
