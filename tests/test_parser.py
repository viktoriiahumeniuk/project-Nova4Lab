import unittest
from utils import parse_input, suggest_command


class TestParser(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(parse_input(""), ("", []))

    def test_hello_command(self):
        self.assertEqual(parse_input("hello"), ("hello", []))

    def test_uppercase_command(self):
        self.assertEqual(parse_input("HELP"), ("help", []))

    def test_full_name(self):
        self.assertEqual(
            parse_input("add-user John Smith"),
            ("add-user", ["John Smith"])
        )

    def test_add_contact(self):
        self.assertEqual(
            parse_input("add-contact John Smith, 7045550199"),
            ("add-contact", ["John Smith", "7045550199"])
        )

    def test_quoted_name(self):
        self.assertEqual(
            parse_input('add-user "John Smith"'),
            ("add-user", ["John Smith"])
        )

    def test_change_phone(self):
        self.assertEqual(
            parse_input("change John Smith, 7045550199, 7045550123"),
            ("change", ["John Smith", "7045550199", "7045550123"])
        )

    def test_set_email(self):
        self.assertEqual(
            parse_input("set-email John Smith, john@gmail.com"),
            ("set-email", ["John Smith", "john@gmail.com"])
        )

    def test_set_address(self):
        self.assertEqual(
            parse_input("set-address John Smith, 100 Main St, Charlotte, NC"),
            ("set-address", ["John Smith", "100 Main St, Charlotte, NC"])
        )

    def test_add_note(self):
        self.assertEqual(
            parse_input("add-note Buy groceries tomorrow"),
            ("add-note", ["Buy groceries tomorrow"])
        )

    def test_quoted_note(self):
        self.assertEqual(
            parse_input('add-note "Buy groceries tomorrow"'),
            ("add-note", ["Buy groceries tomorrow"])
        )

    def test_edit_note(self):
        self.assertEqual(
            parse_input("edit-note 1, Buy groceries tomorrow"),
            ("edit-note", ["1", "Buy groceries tomorrow"])
        )

    def test_add_tag(self):
        self.assertEqual(
            parse_input("add-tag 1 shopping"),
            ("add-tag", ["1", "shopping"])
        )

    def test_invalid_quotes(self):
        with self.assertRaises(ValueError):
            parse_input('add-note "Buy groceries')

    def test_missing_address(self):
        with self.assertRaises(ValueError):
            parse_input("set-address John Smith")

    def test_suggest_command(self):
        commands = ("hello", "help", "exit")
        self.assertEqual(
            suggest_command("hlep", commands), "help"
        )

    def test_suggest_phrase(self):
        commands = ("search-contact", "search-note")
        self.assertEqual(
            suggest_command("find a contact", commands),
            "search-contact"
        )

    def test_unknown_command(self):
        commands = ("hello", "help", "exit")
        self.assertIsNone(
            suggest_command("xyz123", commands)
        )


if __name__ == "__main__":
    unittest.main()
