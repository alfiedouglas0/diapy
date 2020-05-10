import npyscreen
import curses
from os.path import join, abspath, dirname, basename

from ...config import Config
from ...db.dbsetup import create_db
from ...db.db import DB
from ...utils import does_file_exist

DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000"


class EntriesListForm(npyscreen.FormBaseNew):
    def create(self):
        self.value = []
        self.entries_widget = self.add(EntriesListGrid, hidden=False,
                                       max_height=self.lines - 30,
                                       callback=self.item_selected_callback,
                                       values=[])
        # self.entries_empty_widget = self.add(npyscreen.FixedText,
        #  relx=self.lines // 4,
        #  rely=self.columns // 4,
        #  value="No entries")

        self.add(npyscreen.ButtonPress, name="Exit", relx=12, rely=-3,
                 when_pressed_function=lambda: self.parentApp.switchForm(None))
        self.add(npyscreen.ButtonPress, name="New Entry", relx=-20, rely=-3,
                 when_pressed_function=self.new_entry)

        self.parentApp.addDBListener(
            lambda db: self.set_value(db.get_all_entries() if db != None else []))

    def get_entries(self):
        if self.parentApp.db != None:
            self.entries = self.parentApp.db.get_all_entries()
        else:
            self.entries = []
        return self.entries

    def item_selected_callback(self, item):
        self.parentApp.selectedEntry = item
        self.parentApp.switchForm("EntryEdit")

    def new_entry(self):
        self.parentApp.selectedEntry = None
        self.parentApp.switchForm("EntryEdit")


class EntriesListGrid(npyscreen.GridColTitles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.select_whole_line = True
        self.default_column_number = 1
        self.item_selected_callback = kwargs['callback'] if 'callback' in kwargs else None
        self.add_handlers({curses.KEY_ENTER: self.item_selected})
        self.add_handlers({curses.ascii.NL: self.item_selected})

    def display_value(self, vl):
        return "{}\t\t{}".format(vl.entry_date.strftime(DATE_FORMAT),
                                 vl.title)

    def item_selected(self, input):
        if(self.item_selected_callback != None):
            self.item_selected_callback(self.values[self.edit_cell[0]][0])

    def when_parent_changes_value(self):
        self.values = [[v] for v in self.parent.value]
        # self.set_grid_values_from_flat_list([v for v in self.parent.value])
