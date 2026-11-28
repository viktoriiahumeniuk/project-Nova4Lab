import unittest
from models import NoteBook


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.notebook = NoteBook()
        self.note = self.notebook.add("Buy groceries")

    def test_add_note(self):
        self.assertEqual(self.note.id, 1)
        self.assertEqual(self.note.text, "Buy groceries")

    def test_get_note(self):
        self.assertEqual(self.notebook.get("1"), self.note)

    def test_edit_note(self):
        self.note.edit("Buy groceries tomorrow")
        self.assertEqual(self.note.text, "Buy groceries tomorrow")

    def test_delete_note(self):
        self.notebook.delete("1")
        self.assertEqual(len(self.notebook.notes), 0)

    def test_list_notes(self):
        second_note = self.notebook.add("Call John")
        self.assertEqual(
            self.notebook.list_notes(), [self.note, second_note]
        )

    def test_search_note(self):
        self.assertEqual(
            self.notebook.search("groceries"), [self.note]
        )

    def test_pin_note(self):
        self.note.pinned = True
        self.assertTrue(self.note.pinned)

    def test_unpin_note(self):
        self.note.pinned = True
        self.note.pinned = False
        self.assertFalse(self.note.pinned)

    def test_pinned_notes_first(self):
        second_note = self.notebook.add("Call John")
        second_note.pinned = True
        self.assertEqual(
            self.notebook.list_notes(), [second_note, self.note]
        )

    def test_add_tag(self):
        self.note.add_tag("shopping")
        self.assertIn("shopping", self.note.tags)

    def test_duplicate_tag(self):
        self.note.add_tag("shopping")
        self.note.add_tag("shopping")
        self.assertEqual(len(self.note.tags), 1)

    def test_search_by_tag(self):
        self.note.add_tag("shopping")
        self.assertEqual(
            self.notebook.search_by_tag("shopping"), [self.note]
        )

    def test_sort_by_tags(self):
        self.note.add_tag("shopping")
        second_note = self.notebook.add("Call John")
        second_note.add_tag("personal")
        self.assertEqual(
            self.notebook.sort_by_tags(), [second_note, self.note]
        )


if __name__ == "__main__":
    unittest.main()
