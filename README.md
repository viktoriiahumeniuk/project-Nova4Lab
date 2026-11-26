# Nova Lab Personal Assistant

A Python command-line assistant for managing contacts and notes. This is the final team project for Neoversity's Python Programming course.

## Project status

The starter bot supports contacts, phone numbers, and birthdays. The team plans to add email and address fields, contact search, and note management.

## Run the starter bot

Use Python 3.10 or later. The starter bot uses only the Python standard library.

```bash
git clone https://github.com/viktoriiahumeniuk/project-Nova4Lab.git
cd project-Nova4Lab
python3 main.py
```

Run `python3 main.py` once `main.py` is available on `main`. If the starter bot is still under review, switch to `feature/initial-bot` after that branch is published.

## Starter commands

| Command | Description |
| --- | --- |
| `add Anna 7045550123` | Create a contact or add a phone number |
| `change Anna 7045550123 7045550199` | Replace an existing phone number |
| `phone Anna` | Show a contact's phone numbers |
| `all` | Show all contacts |
| `add-birthday Anna 03.12.1998` | Save a birthday in `DD.MM.YYYY` format |
| `show-birthday Anna` | Show a contact's birthday |
| `birthdays` | Show upcoming birthdays from today through seven days from now |
| `exit` or `close` | Save contacts and exit |

The starter bot accepts single-word names and 10-digit phone numbers. It saves contacts to `addressbook.pkl` in the directory where you run it. Keep that file local.

## Team workflow

1. Pick a Trello card and create a branch from `main`.
2. Open a pull request and link the Trello card.
3. Request a review before merging.
4. Keep the link to your merged pull request for the course submission.