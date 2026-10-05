"""Independent full reports, finite method controls and native admission boundaries."""

import ast
import copy
import json
from pathlib import Path
import subprocess  # nosec B404 -- fixed local interpreter tests, no shell or case commands
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from redirectlab import Invalid, evaluate, parse
from redirectlab import contracts, report
from redirectlab import __main__ as cli

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((ROOT / "fixtures/expected.json").read_text(encoding="utf-8"))
ERRORS = json.loads((ROOT / "fixtures/errors.json").read_text(encoding="utf-8"))


def one(index=0):
    return {"version": 1, "cases": [copy.deepcopy(CASES["cases"][index])]}


class ModelTests(unittest.TestCase):
    def test_frozen_labels(self):
        result = evaluate(parse((ROOT / "fixtures/cases.json").read_bytes()))
        for actual, expected in zip(result["results"], EXPECTED["results"], strict=True):
            with self.subTest(case=actual["id"]):
                self.assertEqual(actual, expected)
        self.assertEqual(result, EXPECTED)
        self.assertEqual(sum(r["status"] == "UNSUPPORTED" for r in result["results"]), 14)

    def test_frozen_errors(self):
        for item in ERRORS:
            with self.subTest(case=item["id"]), self.assertRaises(Invalid) as raised:
                if item["kind"] == "bytes":
                    parse(item["raw"].encode("utf-8"))
                else:
                    evaluate(item["value"])
            self.assertEqual(str(raised.exception), item["code"])

    def test_independent_method_table(self):
        # Independent explicit matrix, not model helpers: 7 methods x5 codes x3 choices.
        methods = ("GET", "HEAD", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
        fixed = {301: methods, 302: methods,
                 303: ("GET", "HEAD", "GET", "GET", "GET", "GET", "GET"),
                 307: methods, 308: methods}
        for status, expected_methods in fixed.items():
            for position, method in enumerate(methods):
                for choice in ("get", "preserve", "unknown"):
                    case = one()["cases"][0]
                    case.update(response_status=status, method=method)
                    case["policy"]["post_301_302"] = choice
                    expected = expected_methods[position]
                    if status in (301, 302) and method == "POST":
                        expected = {"get": "GET", "preserve": "POST", "unknown": None}[choice]
                    row = evaluate({"version": 1, "cases": [case]})["results"][0]
                    with self.subTest(status=status, method=method, choice=choice):
                        self.assertEqual(row["proposed_method"], expected)
                        self.assertEqual(row["unknowns"], ["UNKNOWN_METHOD_POLICY"] if expected is None else [])
                        self.assertEqual(row["body_action"], None if expected is None else (
                            "DROP" if status == 303 or expected != method else "ABSENT"))
                        self.assertEqual(row["policy_decision"], "UNRESOLVED" if expected is None else "WOULD_FOLLOW_ASSUMPTIONS")

    def test_whole_input_validation_and_shortcut_controls(self):
        for index in (22, 34, 35, 37):
            document = one(index)
            late = one()["cases"][0]
            late.update(id="late", method="lowercase")
            document["cases"].append(late)
            with self.assertRaisesRegex(Invalid, "^METHOD$"):
                evaluate(document)
        for status in (200, 204):
            document = one(36)
            document["cases"][0]["response_status"] = status
            row = evaluate(document)["results"][0]
            self.assertEqual((row["rule"], row["policy_decision"], row["next_step"]),
                             ("NOT_FOLLOW_PROFILE", "NOT_APPLICABLE", None))

    def test_immutable_and_independent_copies(self):
        document = one(25)
        snapshot = copy.deepcopy(document)
        result = evaluate(document)
        result["results"][0]["declaration"]["policy"]["follow"] = "changed"
        self.assertEqual(document, snapshot)
        self.assertEqual(evaluate(document)["results"][0], EXPECTED["results"][25])

    def test_tree_bytes_and_schema_boundaries(self):
        for raw, code in ((b"\xff", "INVALID_JSON"), (b"x"*65537, "INPUT_LIMIT")):
            with self.assertRaisesRegex(Invalid, "^"+code+"$"):
                parse(raw)
        for value, code in ((1.1, "TREE_TYPE"), (10**10, "INTEGER_TOKEN_BOUND"),
                            ("x"*257, "TEXT_TYPE_OR_LIMIT"), ("\x00", "TEXT_CONTROL"),
                            ("\ud800", "INVALID_UNICODE"), ([0]*101, "CONTAINER_LIMIT")):
            with self.assertRaisesRegex(Invalid, "^"+code+"$"):
                evaluate(value)
        nested = None
        for _ in range(8):
            nested = [nested]
        contracts._walk(nested, 1, [0], set())
        with self.assertRaisesRegex(Invalid, "^TREE_DEPTH$"):
            contracts._walk([nested], 1, [0], set())
        cyclic = []; cyclic.append(cyclic)
        with self.assertRaisesRegex(Invalid, "^TREE_CYCLE$"):
            evaluate(cyclic)
        repeated = [[0]*100]*50
        with self.assertRaisesRegex(Invalid, "^NODE_LIMIT$"):
            evaluate(repeated)
        # Within node/string/container caps but beyond compact UTF8 byte admission.
        with self.assertRaisesRegex(Invalid, "^INPUT_LIMIT$"):
            evaluate([["x"*256]*100]*3)
        document = one(); document["cases"] *= 41
        with self.assertRaisesRegex(Invalid, "^CASE_COUNT$"):
            evaluate(document)

    def test_identity_guards_never_call_native_hooks(self):
        calls = []
        def hook(*_args):
            calls.append("called")
            raise AssertionError("native hook")
        class Meta(type):
            __eq__ = __hash__ = hook
        class Exotic(metaclass=Meta):
            pass
        class Key(str):
            __hash__ = str.__hash__
            __eq__ = hook
        class Text(str):
            encode = __len__ = __iter__ = hook
        class Number(int):
            __eq__ = __lt__ = __gt__ = hook
        class Sequence(list):
            __iter__ = __len__ = hook
        class Mapping(dict):
            items = __iter__ = __len__ = hook
        values = [Exotic(), Exotic, Key("x"), Text("x"), Number(1), Sequence(), Mapping(), iter([])]
        for value in values:
            with self.assertRaisesRegex(Invalid, "^TREE_TYPE$"):
                evaluate(value)
        bad_key = {Key("x"): 1}
        calls.clear()
        with self.assertRaisesRegex(Invalid, "^TREE_TYPE$"):
            evaluate(bad_key)
        document = one(); document["cases"][0]["method"] = Text("GET")
        with self.assertRaisesRegex(Invalid, "^TREE_TYPE$"):
            evaluate(document)
        self.assertEqual(calls, [])

    def test_parse_identity_aliases_and_schema_limits(self):
        calls = []
        class Raw(bytes):
            def __len__(self):
                calls.append("length")
                return 0
            def decode(self, *_args):
                calls.append("decode")
                return "{}"
        with self.assertRaisesRegex(Invalid, "^INPUT_LIMIT$"):
            parse(Raw(b"{}"))
        self.assertEqual(calls, [])
        document = one()
        other = one()["cases"][0]; other["id"] = "alias"
        other["policy"] = document["cases"][0]["policy"]
        document["cases"].append(other)
        result = evaluate(document)
        self.assertEqual(len(result["results"]), 2)
        self.assertIsNot(result["results"][0]["declaration"]["policy"],
                         result["results"][1]["declaration"]["policy"])
        for field, value, code in (("followed", -1, "FOLLOWED"),
                                   ("followed", 9, "FOLLOWED"),
                                   ("maximum", 9, "MAXIMUM")):
            document = one(); document["cases"][0]["policy"][field] = value
            with self.assertRaisesRegex(Invalid, "^"+code+"$"):
                evaluate(document)
        document = one(); document["cases"][0]["unsupported_features"] = ["a"]*9
        with self.assertRaisesRegex(Invalid, "^FEATURE_COUNT$"):
            evaluate(document)

    def test_stress_admitted_shape_and_cap_seam(self):
        records = []
        for name, index in (("all-gates", 25), ("maximum-features", 37)):
            cases = []
            for position in range(40):
                case = one(index)["cases"][0]
                case["id"] = f"case-{position:02}-" + "x"*56
                if name == "maximum-features":
                    case["method"] = "CUSTOM" + "X"*10
                    case["unsupported_features"] = [chr(97+j)*32 for j in range(8)]
                cases.append(case)
            raw = json.dumps({"version":1, "cases":cases}, separators=(",", ":")).encode()
            self.assertLessEqual(len(raw), contracts.INPUT_BYTES)
            evaluated = evaluate(parse(raw))
            encoded_json = report.encode(evaluated)
            encoded_markdown = report.encode(evaluated, "markdown")
            self.assertLess(len(encoded_markdown), 997376)  # Frozen conservative envelope.
            with patch.object(report, "OUTPUT_BYTES", len(encoded_markdown)-1), self.assertRaisesRegex(Invalid, "^OUTPUT_LIMIT$"):
                report.encode(evaluated, "markdown")
            records.append(dict(name=name, optimized=not __debug__, cases=40,
                                input_bytes=len(raw), json_bytes=len(encoded_json),
                                markdown_bytes=len(encoded_markdown), natural_overflow=False,
                                reduced_cap_seam_rejected=True))
        print("STRESS_RECORD " + json.dumps(records))

    def test_capability_inventory(self):
        names = set()
        for path in (ROOT / "redirectlab").glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    names.update(item.name.split(".")[0] for item in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    names.add(node.module.split(".")[0])
        self.assertEqual(names, {"argparse", "copy", "json", "os", "re", "sys"})


def child(arguments):
    return subprocess.run([sys.executable, *(["-O"] if not __debug__ else []),
                           "-m", "redirectlab", *arguments], cwd=ROOT, capture_output=True,
                          timeout=15, check=False)  # nosec B603


def barrier_child(arguments, close_stdout=False, close_stderr=False, dirty=False):
    wrapper = ("import json,sys;from redirectlab.__main__ import main;sys.stdin.buffer.read(1);"
               + ("sys.stdout.close();sys.stderr.close();" if dirty else "")
               + "raise SystemExit(main(json.loads(sys.argv[1])))")
    process = subprocess.Popen([sys.executable, *(["-O"] if not __debug__ else []),
                                "-c", wrapper, json.dumps(arguments)], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)  # nosec B603
    try:
        if close_stdout:
            process.stdout.close()
            process.stdout = None
        if close_stderr:
            process.stderr.close()
            process.stderr = None
        stdout, stderr = process.communicate(input=b"x", timeout=15)
        return process.returncode, stdout or b"", stderr or b""
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None:
                stream.close()


class DeliveryTests(unittest.TestCase):
    def test_reports_inert_and_bounded(self):
        evaluated = evaluate(CASES)
        self.assertEqual(json.loads(report.encode(evaluated)), EXPECTED)
        document = one(25)
        document["cases"][0]["method"] = "`INERT|TEXT`"
        encoded = report.encode(evaluate(document), "markdown")
        self.assertNotIn(b"`INERT|TEXT`", encoded)
        self.assertIn(b"&#96;", encoded)
        self.assertIn(b"&#124;", encoded)
        self.assertEqual(encoded.count(b"## "), 1)
        with patch.object(report, "OUTPUT_BYTES", 10), self.assertRaisesRegex(Invalid, "^OUTPUT_LIMIT$"):
            report.encode(evaluated)
        with self.assertRaisesRegex(Invalid, "^REPORT_FORMAT$"):
            report.encode(evaluated, "html")

    def test_actual_cli_and_fresh_alias_paths(self):
        result = child(["fixtures/cases.json"])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout), EXPECTED)
        self.assertEqual(result.stderr, b"")
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "input.json"
            source.write_text(json.dumps(one(3)), encoding="utf-8")
            target = Path(directory) / "report.json"
            result = child([str(source), "--output", str(target)])
            self.assertEqual(result.returncode, 0)  # Supported hypothetical next step, no request sent.
            saved = target.read_bytes()
            self.assertEqual(json.loads(saved)["results"][0]["policy_decision"], "WOULD_FOLLOW_ASSUMPTIONS")
            result = child([str(source), "--output", str(target)])
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, b"")
            self.assertEqual(result.stderr, b"redirectlab: IO_ERROR\n")
            self.assertEqual(target.read_bytes(), saved)
            original = source.read_bytes()
            result = child([str(source), "--output", str(source)])
            self.assertEqual(result.stderr, b"redirectlab: INPUT_OUTPUT_ALIAS\n")
            self.assertEqual(source.read_bytes(), original)

    def test_actual_empty_output_and_nul(self):
        result = child(["fixtures/cases.json", "--output", ""])
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (1, b"", b"redirectlab: INVALID_OUTPUT_PATH\n"))
        for arguments, code in ((["\x00"], "INVALID_INPUT_PATH"),
                                (["fixtures/cases.json", "--output", "\x00"], "INVALID_OUTPUT_PATH")):
            # NUL is passed through controlled JSON to main, not as impossible OS argv.
            result = barrier_child(arguments)
            self.assertEqual(result, (1, b"", ("redirectlab: " + code + "\n").encode()))

    def test_actual_process_stream_boundaries(self):
        entries = [
            ("missing-stderr", ["inert-missing.json"], False, True, False, 1),
            ("missing-both", ["inert-missing.json"], True, True, False, 1),
            ("usage-both", ["--format", "inert-private-value"], True, True, False, 2),
            ("empty-input-both", [""], True, True, False, 1),
            ("report-stdout", ["fixtures/cases.json"], True, False, False, 1),
            ("report-both", ["fixtures/cases.json"], True, True, False, 1),
            ("help-alive", ["--help"], False, False, False, 0),
            ("help-stdout", ["--help"], True, False, False, 1),
            ("help-both", ["--help"], True, True, False, 1),
            ("dirty-report", ["fixtures/cases.json"], False, False, True, 1),
            ("dirty-missing", ["inert-missing.json"], False, False, True, 1),
            ("dirty-usage", ["--format", "inert-private-value"], False, False, True, 2),
            ("dirty-help", ["--help"], False, False, True, 1),
        ]
        records = []
        for name, args, close_stdout, close_stderr, dirty, expected in entries:
            with self.subTest(name=name):
                code, stdout, stderr = barrier_child(args, close_stdout, close_stderr, dirty)
                self.assertEqual(code, expected)
                self.assertNotIn(b"Traceback", stderr)
                self.assertNotIn(b"Exception ignored", stderr)
                self.assertNotIn(b"inert-private", stderr)
                if name == "help-alive":
                    self.assertIn(b"usage: redirectlab", stdout)
                    self.assertLess(len(stdout), 4096)
                else:
                    self.assertEqual(stdout, b"")
                if name in ("report-stdout", "help-stdout"):
                    self.assertEqual(stderr, b"redirectlab: IO_ERROR\n")
                records.append({"name":name, "kind":"python_stream_close" if dirty else "physical_pipe_barrier",
                                "optimized":not __debug__, "exit_code":code,
                                "stdout_bytes":len(stdout), "stderr_bytes":len(stderr)})
        print("BOUNDARY_RECORDS " + json.dumps(records))

    def test_actual_parse_error_both_closed(self):
        records = []
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "invalid.json"
            source.write_text('{"version":1,"version":1}', encoding="utf-8")
            for dirty in (False, True):
                code, stdout, stderr = barrier_child([str(source)], not dirty, not dirty, dirty)
                self.assertEqual((code, stdout, stderr), (1, b"", b""))
                records.append({"name":"parse-error-both", "kind":"python_stream_close" if dirty else "physical_pipe_barrier",
                                "optimized":not __debug__, "exit_code":code, "stdout_bytes":0, "stderr_bytes":0})
        print("BOUNDARY_RECORDS " + json.dumps(records))

    def test_actual_invalid_and_argument_diagnostics(self):
        result = child(["--format", "inert-private-value"])
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, b"", b"redirectlab: ARGUMENT_ERROR\n"))
        with tempfile.TemporaryDirectory(dir=ROOT / "reports") as directory:
            source = Path(directory) / "invalid.json"
            source.write_text('{"version":1,"version":1}', encoding="utf-8")
            result = child([str(source)])
            self.assertEqual((result.returncode, result.stdout, result.stderr),
                             (1, b"", b"redirectlab: DUPLICATE_KEY\n"))

    def test_checked_stdout_and_diagnostics_seams(self):
        # Labeled dirty-sink seams, separate from actual child process evidence.
        for mode in ("short", "bool", "float", "none", "write", "flush"):
            class Sink:
                @property
                def buffer(self):
                    return self

                def write(self, payload):
                    if mode == "write":
                        raise OSError("inert-native-text")
                    return 0 if mode == "short" else True if mode == "bool" else float(len(payload)) if mode == "float" else None if mode == "none" else len(payload)

                def flush(self):
                    if mode == "flush":
                        raise ValueError("inert-native-text")

                def fileno(self):
                    raise ValueError("unusable")

            sink = Sink()
            with patch.object(cli.sys, "stdout", SimpleNamespace(buffer=sink)), patch.object(cli.sys, "stderr", sink), \
                    patch.object(cli.os, "open", side_effect=OSError("unavailable")):
                self.assertEqual(cli.main(["fixtures/cases.json"]), 1)
                self.assertIsNone(cli.sys.stdout)
                self.assertIsNone(cli.sys.stderr)
            for args, expected in ((["inert-missing.json"], 1), (["--format", "invalid"], 2)):
                with patch.object(cli.sys, "stderr", sink), patch.object(cli.os, "open", side_effect=OSError("unavailable")):
                    self.assertEqual(cli.main(args), expected)
                    self.assertIsNone(cli.sys.stderr)

    def test_checked_help_and_redirection_seams(self):
        sink = SimpleNamespace(write=lambda payload: 0, flush=lambda: None)
        errors = []
        diagnostic = SimpleNamespace(buffer=SimpleNamespace(write=lambda text: errors.append(text) or len(text), flush=lambda: None))
        with patch.object(cli.sys, "stdout", SimpleNamespace(buffer=sink)), patch.object(cli.sys, "stderr", diagnostic), \
                patch.object(cli.os, "open", side_effect=OSError("unavailable")):
            self.assertEqual(cli.main(["--help"]), 1)
            self.assertEqual(errors, [b"redirectlab: STDOUT_WRITE_AND_SILENCE_FAILED\n"])
        stream = SimpleNamespace(fileno=lambda: 1)
        with patch.object(cli.sys, "stdout", stream), patch.object(cli.os, "open", return_value=99), \
                patch.object(cli.os, "dup2"), patch.object(cli.os, "close", side_effect=OSError("close failed")):
            self.assertFalse(cli._silence_failed_stream(stream))
            self.assertIsNone(cli.sys.stdout)

    def test_fresh_short_flush_close_cleanup_seams(self):
        for mode in ("short", "bool", "float", "none", "flush", "close"):
            class Stream:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    if mode == "close":
                        raise OSError("close failed")

                def write(self, payload):
                    return 0 if mode == "short" else True if mode == "bool" else float(len(payload)) if mode == "float" else None if mode == "none" else len(payload)

                def flush(self):
                    if mode == "flush":
                        raise ValueError("closed")

            with patch("builtins.open", return_value=Stream()), patch.object(report.os, "unlink") as cleanup:
                with self.assertRaises((OSError, ValueError)):
                    report.write_fresh("owned-new-file", b"x")
                cleanup.assert_called_once_with("owned-new-file")
            with patch("builtins.open", return_value=Stream()), patch.object(report.os, "unlink", side_effect=OSError("cleanup failed")):
                with self.assertRaisesRegex(Invalid, "^OUTPUT_WRITE_AND_CLEANUP_FAILED$"):
                    report.write_fresh("owned-new-file", b"x")


if __name__ == "__main__":
    unittest.main()
