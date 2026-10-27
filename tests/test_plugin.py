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

"""Regressions for the Claude plugin marketplace published from this repository."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_plugin.py"
PLUGIN = ROOT / "plugins" / "harness2"


class PluginMarketplaceTests(unittest.TestCase):
    def test_marketplace_and_plugin_validate(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER)], capture_output=True, text=True, cwd=ROOT
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_marketplace_lives_where_claude_looks(self):
        self.assertTrue((ROOT / ".claude-plugin" / "marketplace.json").is_file())

    def test_plugin_dir_holds_only_the_manifest(self):
        manifest_dir = PLUGIN / ".claude-plugin"
        self.assertEqual(sorted(p.name for p in manifest_dir.iterdir()), ["plugin.json"])

    def test_component_dirs_sit_at_the_plugin_root(self):
        for name in ("skills", "commands", "agents"):
            self.assertTrue((PLUGIN / name).is_dir(), name)
        self.assertFalse((PLUGIN / "bin").exists(), "bin/ blocks claude.ai installs")

    def test_skills_are_directories_with_skill_md(self):
        skills = sorted(p.name for p in (PLUGIN / "skills").iterdir())
        self.assertIn("harness-refine", skills)
        for name in skills:
            self.assertTrue((PLUGIN / "skills" / name / "SKILL.md").is_file(), name)


if __name__ == "__main__":
    unittest.main()
