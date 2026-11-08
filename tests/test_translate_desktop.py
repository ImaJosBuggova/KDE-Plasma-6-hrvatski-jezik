import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "translate_desktop.py"
HEADER = '''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: hr\\n"

'''


class DesktopTranslationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = self.root / "share"
        self.output = self.root / "output"
        self.catalog_root = self.root / "catalogs"

    def catalog(self, project, source, translated):
        path = self.catalog_root / project / f"{project}._desktop_.po"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            HEADER + f'#: {source}:1\nmsgctxt "Name"\n'
            f'msgid "Appearance"\nmsgstr "{translated}"\n',
            encoding="utf-8",
        )

    def template(self, path):
        file = self.data / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(
            "[Desktop Entry]\nName=Appearance\nName[hr]=Staro\nName[de]=Aussehen\n",
            encoding="utf-8",
        )
        return file

    def run_script(self):
        return subprocess.run(
            ["python3", str(SCRIPT), str(self.catalog_root), str(self.output), str(self.data)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def test_context_and_existing_translation_are_handled(self):
        self.catalog("systemsettings", "categories/settings.desktop", "Izgled")
        self.template("systemsettings/categories/settings.desktop")
        self.run_script()
        result = (self.output / "systemsettings/categories/settings.desktop").read_text()
        self.assertIn("Name[hr]=Izgled\n", result)
        self.assertEqual(result.count("Name[hr]="), 1)
        self.assertIn("Name[de]=Aussehen\n", result)

    def test_project_path_disambiguates_shared_basename(self):
        self.catalog("systemsettings", "categories/settings.desktop", "Izgled")
        self.catalog("plasma-settings", "categories/settings.desktop", "Prikaz")
        self.template("systemsettings/categories/settings.desktop")
        self.run_script()
        result = (self.output / "systemsettings/categories/settings.desktop").read_text()
        self.assertIn("Name[hr]=Izgled\n", result)

    def test_unresolved_conflict_is_reported_and_not_written(self):
        self.catalog("first", "src/settings.desktop", "Izgled")
        self.catalog("second", "src/settings.desktop", "Prikaz")
        self.template("applications/settings.desktop")
        result = self.run_script()
        self.assertIn(b"Ambiguous translation", result.stderr)
        self.assertFalse((self.output / "applications/settings.desktop").exists())


if __name__ == "__main__":
    unittest.main()
