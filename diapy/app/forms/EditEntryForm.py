import npyscreen
import os
import datetime

from ...db.db import DB, DB_Entry, DB_Entry_Body
from ..widgets.MultiLineEditBox import MultiLineEditBox

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000"


class EditEntryForm(npyscreen.FormBaseNew):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentApp.unsavedChanges = True
        if self.parentApp.selectedEntry == None:
            self.entry, self.entry_body = self.parentApp.db.new_entry_body_pair()
        else:
            self.entry = self.parentApp.selectedEntry
            self.entry_body = self.parentApp.db.get_entry_body(
                self.entry.entry_body_id)

        self.load_values()

    def create(self):
        self.date_widget = self.add(npyscreen.DateCombo,
                                    relx=3, rely=2, max_width=15, max_height=5)
        self.title_widget = self.add(npyscreen.TitleText, name="Title:",
                                     use_two_lines=False,
                                     relx=20, rely=2, max_height=5)
        self.body_widget = self.add(MultiLineEditBox, name='BODY', relx=3, rely=5,
                                    max_width=os.get_terminal_size()[0] - 6,
                                    max_height=os.get_terminal_size()[1] - 9)

        self.add(npyscreen.ButtonPress, name="Exit", relx=3, rely=-3,
                 when_pressed_function=self.exit)
        self.add(npyscreen.ButtonPress, name="Cancel", relx=-25, rely=-3,
                 when_pressed_function=self.cancel)
        self.add(npyscreen.ButtonPress, name="Save", relx=-15, rely=-3,
                 when_pressed_function=self.save)

    def load_values(self):
        self.date_widget.value = self.entry.entry_date
        self.title_widget.value = self.entry.title
        self.body_widget.value = value = self.entry_body.body

    def exit(self):
        notify_result = npyscreen.notify_ok_cancel(
            "Any unsaved changed will be lost", title='Are you sure?')

        if notify_result:
            self.parentApp.switchForm(None)

    def cancel(self):
        notify_result = npyscreen.notify_ok_cancel(
            "Any unsaved changed will be lost", title='Are you sure?')

        if notify_result:
            self.parentApp.switchFormPrevious()

    def save(self):
        try:
            self.entry_body.body = self.body_widget.value
            self.parentApp.db.insert_or_update_entry_body(self.entry_body)

            self.entry.entry_date = self.date_widget.value
            self.entry.title = self.title_widget.value
            self.entry.entry_body_id = self.entry_body.id
            self.parentApp.db.insert_or_update_entry(self.entry)

            self.parentApp.notify_db_changed()
            self.parentApp.switchFormPrevious()
        except Exception as e:
            npyscreen.notify_confirm("Error: {}".format(str(e)), title='Error')
