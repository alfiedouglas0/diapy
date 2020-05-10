import npyscreen
import os
import datetime

from ...db.db import DB
from ..widgets.MultiLineEditBox import MultiLineEditBox

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000%z"


class EditEntryForm(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.DateCombo, value=datetime.datetime.now(),
                 relx=3, rely=2, max_width=15, max_height=5)
        self.db_path = self.add(npyscreen.TitleText, name="Title:",
                                use_two_lines=False, value="",
                                relx=20, rely=2, max_height=5)
        self.add(MultiLineEditBox, name='BODY', relx=3, rely=5,
                 max_width=os.get_terminal_size()[0] - 6,
                 max_height=os.get_terminal_size()[1] - 15)

        self.add(npyscreen.ButtonPress, name="Exit", relx=3, rely=-3,
                 when_pressed_function=self.exit)
        self.add(npyscreen.ButtonPress, name="Cancel", relx=-25, rely=-3,
                 when_pressed_function=self.cancel)
        self.add(npyscreen.ButtonPress, name="Save", relx=-15, rely=-3,
                 when_pressed_function=self.save)

    def exit(self):
        notify_result = npyscreen.notify_ok_cancel(
            "Any unsaved changed will be lost", title='Are you sure?')

        if notify_result:
            exit()

    def cancel(self):
        notify_result = npyscreen.notify_ok_cancel(
            "Any unsaved changed will be lost", title='Are you sure?')

        if notify_result:
            self.parentApp.switchFormPrevious()

    def save(self):
        pass
