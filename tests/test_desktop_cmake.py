import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "translate_desktop.py"


class DesktopCmakeTest(unittest.TestCase):
    def test_application_descriptions_and_menu_categories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            catalogs = root / "catalogs"
            data = root / "share"
            output = root / "output"
            cases = (
                ("spectacle", "desktop/org.kde.spectacle.desktop.cmake",
                 "applications/org.kde.spectacle.desktop",
                 "Screenshot Capture Utility", "Alat za snimanje zaslona",
                 "Take screenshots and screen recordings", "Snimanje zaslonskih slika i videozapisa"),
                ("ark", "app/org.kde.ark.desktop.cmake",
                 "applications/org.kde.ark.desktop",
                 "Archiving Tool", "Alat za arhiviranje",
                 "Work with file archives", "Rad s arhivama datoteka"),
            )
            header = ('msgid ""\nmsgstr ""\n'
                      '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                      '"Language: hr\\n"\n\n')
            for project, source, target, generic, generic_hr, comment, comment_hr in cases:
                catalog = catalogs / project / f"{project}._desktop_.po"
                catalog.parent.mkdir(parents=True)
                catalog.write_text(
                    header
                    + f'#: {source}:1\nmsgctxt "GenericName"\n'
                    + f'msgid "{generic}"\nmsgstr "{generic_hr}"\n\n'
                    + f'#: {source}:2\nmsgctxt "Comment"\n'
                    + f'msgid "{comment}"\nmsgstr "{comment_hr}"\n',
                    encoding="utf-8",
                )
                template = data / target
                template.parent.mkdir(parents=True, exist_ok=True)
                template.write_text(
                    f"[Desktop Entry]\nGenericName={generic}\nGenericName[hr]=Staro\n"
                    f"Comment={comment}\nComment[hr]=Staro\n",
                    encoding="utf-8",
                )

            catalog = catalogs / "plasma-workspace" / "plasma-workspace._desktop_.po"
            catalog.parent.mkdir(parents=True)
            catalog.write_text(
                header + '#: menu/desktop/kf5-help.directory:3\n'
                'msgctxt "Name"\nmsgid "Help"\nmsgstr "Pomoć"\n',
                encoding="utf-8",
            )
            category = data / "desktop-directories" / "kf5-help.directory"
            category.parent.mkdir(parents=True)
            category.write_text("[Desktop Entry]\nName=Help\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(SCRIPT), str(catalogs), str(output), str(data)],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            manifest = set(result.stdout.decode().split("\0"))
            for _, _, target, _, generic_hr, _, comment_hr in cases:
                translated = (output / target).read_text(encoding="utf-8")
                self.assertIn(f"GenericName[hr]={generic_hr}\n", translated)
                self.assertIn(f"Comment[hr]={comment_hr}\n", translated)
                self.assertEqual(translated.count("GenericName[hr]="), 1)
                self.assertEqual(translated.count("Comment[hr]="), 1)
                self.assertIn(target, manifest)
            self.assertIn(
                "Name[hr]=Pomoć\n",
                (output / "desktop-directories/kf5-help.directory").read_text(encoding="utf-8"),
            )
            self.assertIn("desktop-directories/kf5-help.directory", manifest)


if __name__ == "__main__":
    unittest.main()
