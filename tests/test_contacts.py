import unittest
from models import AddressBook, Record


class TestContacts(unittest.TestCase):

    def setUp(self):
        self.book = AddressBook()
        self.record = Record("John Smith")
        self.record.add_phone("7045550199")
        self.book.add_record(self.record)

    def test_add_contact(self):
        self.assertEqual(len(self.book), 1)
        self.assertEqual(self.record.name.value, "John Smith")

    def test_find_contact(self):
        self.assertEqual(self.book.find("John Smith"), self.record)

    def test_delete_contact(self):
        self.book.delete("John Smith")
        self.assertIsNone(self.book.find("John Smith"))

    def test_rename_contact(self):
        self.book.rename("John Smith", "John Brown")
        self.assertIsNone(self.book.find("John Smith"))
        self.assertEqual(self.book.find("John Brown"), self.record)

    def test_add_phone(self):
        self.record.add_phone("7045550123")
        self.assertEqual(len(self.record.phones), 2)

    def test_edit_phone(self):
        self.record.edit_phone("7045550199", "7045550123")
        self.assertEqual(self.record.phones[0].value, "7045550123")

    def test_remove_phone(self):
        self.record.remove_phone("7045550199")
        self.assertEqual(len(self.record.phones), 0)

    def test_set_email(self):
        self.record.set_email("john@gmail.com")
        self.assertEqual(self.record.email.value, "john@gmail.com")

    def test_set_address(self):
        self.record.set_address("100 Main Street")
        self.assertEqual(self.record.address.value, "100 Main Street")

    def test_add_birthday(self):
        self.record.add_birthday("15.05.1995")
        self.assertEqual(str(self.record.birthday), "15.05.1995")

    def test_search_by_name(self):
        self.assertEqual(self.book.search_contacts("john"), [self.record])

    def test_search_by_phone(self):
        self.assertEqual(
            self.book.search_contacts("7045550199"), [self.record]
        )

    def test_search_by_email(self):
        self.record.set_email("john@gmail.com")
        self.assertEqual(
            self.book.search_contacts("john@gmail.com"), [self.record]
        )


if __name__ == "__main__":
    unittest.main()
