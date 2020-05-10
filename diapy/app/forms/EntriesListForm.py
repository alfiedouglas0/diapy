import npyscreen
from os.path import join, abspath, dirname, basename

from ...config import Config
from ...db.dbsetup import create_db
from ...db.db import DB
from ...utils import does_file_exist

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000%z"


class EntriesListForm(npyscreen.FormBaseNew):
    def create(self):
        self.entries = []
        self.entries_widget = self.add(EntriesListGrid, hidden=True,
                                       max_height=self.lines - 30)
        # self.entries_empty_widget = self.add(npyscreen.FixedText,
        #  relx=self.lines // 4,
        #  rely=self.columns // 4,
        #  value="No entries")

        self.add(npyscreen.ButtonPress, name="Exit", relx=12, rely=-3,
                 when_pressed_function=lambda: exit())
        self.add(npyscreen.ButtonPress, name="New Entry", relx=-20, rely=-3,
                 when_pressed_function=self.new_entry)

        self.refresh()

    def get_entries(self):
        if self.parentApp.db != None:
            self.entries = self.parentApp.db.get_all_entries()
        else:
            self.entries = []

    def refresh(self, *args, **kwargs):
        self.get_entries()
        self.entries_widget.values = self.entries

        # if(len(self.entries) == 0):
        #     self.entries_empty_widget.hidden = False
        #     self.entries_widget.hidden = True
        # else:
        #     self.entries_empty_widget.hidden = True
        #     self.entries_widget.hidden = False

        super().refresh(*args, **kwargs)

    def new_entry(self):
        self.parentApp.switchForm("EntryEdit")


class EntriesListGrid(npyscreen.GridColTitles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = []
        self.select_whole_line = True
        self.default_column_number = 1

    def display_value(self, vl):
        return "{}\t{}".format(vl.entry_date.strftime(DATE_TIME_FORMAT),
                               vl.title)
