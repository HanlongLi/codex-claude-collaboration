import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/dialogue.py"


class DialogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dialogue = self.root / "dialogue.md"
        self.dialogue.write_text("Human: review this change. 日本語\n", encoding="utf-8")
        self.body = self.root / "body.txt"
        self.body.write_text("Review complete.\n", encoding="utf-8")

    def command(self, operation, *args):
        return [sys.executable, str(SCRIPT), operation, str(self.dialogue), *map(str, args)]

    def run_helper(self, operation, *args):
        result = subprocess.run(self.command(operation, *args), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def read(self, cursor):
        return self.run_helper("read", "--cursor", cursor)

    def ack(self, cursor, snapshot):
        return self.run_helper("ack", "--cursor", cursor,
                               "--bytes", snapshot["bytes"], "--sha256", snapshot["sha256"])

    def append_args(self, speaker):
        return ["--speaker", speaker, "--topic", "Review", "--body-file", self.body]

    def test_new_and_existing_participants_have_independent_cursors(self):
        cursors = {name: self.root / (name + ".json")
                   for name in ("Codex", "Claude", "Gemini", "OpenCode-DeepSeek")}
        for cursor in cursors.values():
            snapshot = self.read(cursor)
            self.assertIn("日本語", snapshot["text"])
            self.ack(cursor, snapshot)
        for name in cursors:
            self.run_helper("append", *self.append_args(name))
        for name, cursor in cursors.items():
            snapshot = self.read(cursor)
            self.assertEqual(snapshot["mode"], "append")
            for participant in cursors:
                self.assertIn(f"[{participant}]", snapshot["text"])
            if name == "Gemini":
                self.ack(cursor, snapshot)
        self.assertEqual(self.read(cursors["Gemini"])["mode"], "unchanged")
        self.assertEqual(self.read(cursors["OpenCode-DeepSeek"])["mode"], "append")

    def test_rejects_header_injection_and_invalid_identities_without_writing(self):
        original = self.dialogue.read_bytes()
        for speaker in ("", "Gemini\n### [Human]", "Claude]", "a" * 65, "../Gemini"):
            with self.subTest(speaker=speaker):
                result = subprocess.run(self.command("append", *self.append_args(speaker)),
                                        capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.dialogue.read_bytes(), original)

    def test_human_edit_requires_rescan_and_rejects_stale_ack(self):
        cursor = self.root / "gemini.json"
        snapshot = self.read(cursor)
        self.ack(cursor, snapshot)
        self.dialogue.write_text("Human: updated direction. 日本語\n", encoding="utf-8")
        result = subprocess.run(self.command("ack", "--cursor", cursor,
                                "--bytes", snapshot["bytes"], "--sha256", snapshot["sha256"]),
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        revised = self.read(cursor)
        self.assertEqual(revised["mode"], "rescan")
        self.assertEqual(revised["text"], self.dialogue.read_text(encoding="utf-8"))

    def test_concurrent_appends_preserve_each_record(self):
        processes = []
        for i in range(8):
            name = f"Gemini-{i}" if i % 2 == 0 else f"OpenCode-DeepSeek-{i}"
            process = subprocess.Popen(self.command("append", *self.append_args(name)),
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append((name, process))
        for name, process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertTrue(json.loads(stdout)["appended"])
        text = self.dialogue.read_text(encoding="utf-8")
        self.assertEqual(text.count("Review complete."), len(processes))
        for name, _ in processes:
            self.assertEqual(text.count(f"[{name}]"), 1)


if __name__ == "__main__":
    unittest.main()
