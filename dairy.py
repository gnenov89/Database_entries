import datetime
from peewee import *
import os
from collections import OrderedDict
import sys
#Creting database
db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

#Initializing db and creating tables
def initialize():
    """Create the database and the table if they don't exsists"""
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()
def add_entry():
    """Add entry"""
    print("Press ctrl+d when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Yn] ').lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully")

def view_entries(search_query=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        clear()
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq]').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entries(entry)


def delete_entries(entry):
    """Delete an entry"""
    if input("Are you sure? [yN]").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")


def search_entries():
    """Search for a string"""
    view_entries(input('Search quiery: '))

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()