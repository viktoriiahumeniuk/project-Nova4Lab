import unittest
from models import Name, Phone, Email, Address, Birthday, Note, NoteBook


class TestValidation(unittest.TestCase):

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Name("")

    def test_short_phone(self):
        with self.assertRaises(ValueError):
            Phone("12345")

    def test_long_phone(self):
        with self.assertRaises(ValueError):
            Phone("12345678901")

    def test_phone_with_letters(self):
        with self.assertRaises(ValueError):
            Phone("704555abcd")

    def test_empty_phone(self):
        with self.assertRaises(ValueError):
            Phone("")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Email("john.gmail.com")

    def test_email_without_domain(self):
        with self.assertRaises(ValueError):
            Email("john@")

    def test_empty_email(self):
        with self.assertRaises(ValueError):
            Email("")

    def test_empty_address(self):
        with self.assertRaises(ValueError):
            Address("")

    def test_invalid_birthday_format(self):
        with self.assertRaises(ValueError):
            Birthday("1995-05-15")

    def test_invalid_birthday_date(self):
        with self.assertRaises(ValueError):
            Birthday("31.02.1995")

    def test_empty_birthday(self):
        with self.assertRaises(ValueError):
            Birthday("")

    def test_empty_note(self):
        with self.assertRaises(ValueError):
            Note(1, "")

    def test_empty_tag(self):
        note = Note(1, "Buy groceries")
        with self.assertRaises(ValueError):
            note.add_tag("")

    def test_tag_with_spaces(self):
        note = Note(1, "Buy groceries")
        with self.assertRaises(ValueError):
            note.add_tag("shopping list")

    def test_invalid_note_id(self):
        notebook = NoteBook()
        with self.assertRaises(ValueError):
            notebook.get("abc")

    def test_missing_note(self):
        notebook = NoteBook()
        with self.assertRaises(ValueError):
            notebook.get("99")


if __name__ == "__main__":
    unittest.main()
