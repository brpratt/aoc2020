import unittest

from day02 import *

class TestParseOldRecord(unittest.TestCase):
    def test_returns_policy_and_password(self):
        tests = [
            ("1-3 a: abcde", OldPolicy(1, 3, 'a'), "abcde"),
            ("1-3 b: cdefg", OldPolicy(1, 3, 'b'), "cdefg"),
            ("2-9 c: ccccccccc", OldPolicy(2, 9, 'c'), "ccccccccc")
        ]

        for (record, expected_policy, expected_password) in tests:
            (policy, password) = parse_old_record(record)
            self.assertEqual(expected_policy, policy)
            self.assertEqual(expected_password, password)

class TestPassesOldPolicy(unittest.TestCase):
    def test_returns_correct_value(self):
        tests = [
            (OldPolicy(1, 3, 'a'), "abcde", True),
            (OldPolicy(1, 3, 'b'), "cdefg", False),
            (OldPolicy(2, 9, 'c'), "ccccccccc", True)
        ]

        for (policy, password, passes) in tests:
            self.assertEqual(passes, passes_old_policy(policy, password))

class TestSolvePart1(unittest.TestCase):
    def test_returns_valid_password_count(self):
        records = [
            "1-3 a: abcde",
            "1-3 b: cdefg",
            "2-9 c: ccccccccc"
        ]

        self.assertEqual(2, solve_part_1(records))

class TestParseNewRecord(unittest.TestCase):
    def test_returns_policy_and_password(self):
        tests = [
            ("1-3 a: abcde", NewPolicy(1, 3, 'a'), "abcde"),
            ("1-3 b: cdefg", NewPolicy(1, 3, 'b'), "cdefg"),
            ("2-9 c: ccccccccc", NewPolicy(2, 9, 'c'), "ccccccccc")
        ]

        for (record, expected_policy, expected_password) in tests:
            (policy, password) = parse_old_record(record)
            self.assertEqual(expected_policy, policy)
            self.assertEqual(expected_password, password)

class TestPassesNewPolicy(unittest.TestCase):
    def test_returns_correct_value(self):
        tests = [
            (NewPolicy(1, 3, 'a'), "abcde", True),
            (NewPolicy(1, 3, 'b'), "cdefg", False),
            (NewPolicy(2, 9, 'c'), "ccccccccc", False),
            (NewPolicy(5, 7, 'a'), "abc", False),
            (NewPolicy(5, 7, 'a'), "bcdeag", True)
        ]

        for (policy, password, passes) in tests:
            self.assertEqual(passes, passes_new_policy(policy, password))

class TestSolvePart2(unittest.TestCase):
    def test_returns_valid_password_count(self):
        records = [
            "1-3 a: abcde",
            "1-3 b: cdefg",
            "2-9 c: ccccccccc"
        ]

        self.assertEqual(1, solve_part_2(records))
