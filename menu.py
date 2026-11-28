def show_help():
    print(
        """
========================================================
                 NOVA4LAB ASSISTANT
========================================================

CONTACT COMMANDS

add-user name
add-contact name, phone
change name, old_phone, new_phone
remove-phone name, phone
phone name
set-address name, address
set-email name, email
rename-contact old_name, new_name
delete-contact name
show-contact name
search-contact query
all
favorite name
unfavorite name
favorites
add-birthday name, DD.MM.YYYY
show-birthday name
birthdays [days]

NOTE COMMANDS

add-note text
list-notes
search-note text
edit-note id, new_text
delete-note id
pin-note id
unpin-note id
add-tag id tag
search-tag tag
sort-notes-by-tag

SYSTEM COMMANDS

hello       - Greeting
help        - Show available commands
exit        - Save data and exit
close       - Save data and exit

Separate arguments with commas where indicated.
Double quotation marks are optional.

========================================================
"""
    )
