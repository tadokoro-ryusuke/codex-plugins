#!/usr/bin/env python3
"""Independent behavioral assertions for the execution smoke fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import types
import unittest


COMPLETION_PREFIX = "EXECUTION_SMOKE_COMPLETION="


def load_candidate(directory: Path):
    source = directory / "totals.py"
    source_bytes = source.read_bytes()
    module = types.ModuleType("execution_smoke_candidate")
    module.__file__ = str(source)
    code = compile(source_bytes, str(source), "exec")
    exec(code, module.__dict__)
    return module


def make_suite(candidate) -> unittest.TestSuite:
    class IndependentTotalCentsTests(unittest.TestCase):
        def test_quantity_multiplies_unit_price(self):
            self.assertEqual(
                candidate.total_cents(
                    [
                        {"unit_price_cents": 125, "quantity": 3},
                        {"unit_price_cents": 40, "quantity": 2},
                    ]
                ),
                455,
            )

        def test_missing_quantity_defaults_to_one(self):
            self.assertEqual(candidate.total_cents([{"unit_price_cents": 321}]), 321)

        def test_empty_iterable_totals_zero(self):
            self.assertEqual(candidate.total_cents(iter(())), 0)

        def test_generator_input_is_supported(self):
            lines = (
                line
                for line in [
                    {"unit_price_cents": 90, "quantity": 2},
                    {"unit_price_cents": 20},
                ]
            )
            self.assertEqual(candidate.total_cents(lines), 200)

        def test_invalid_quantities_raise_value_error(self):
            for quantity in (0, -1, True, False, 1.5, "2", None, [], {}):
                with self.subTest(quantity=quantity):
                    with self.assertRaises(ValueError):
                        candidate.total_cents(
                            [{"unit_price_cents": 100, "quantity": quantity}]
                        )

    return unittest.defaultTestLoader.loadTestsFromTestCase(IndependentTotalCentsTests)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True, type=Path)
    args = parser.parse_args()
    candidate = load_candidate(args.directory.resolve())
    suite = make_suite(candidate)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    completion = {
        "schema_version": 1,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
    }
    print(COMPLETION_PREFIX + json.dumps(completion, sort_keys=True), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
