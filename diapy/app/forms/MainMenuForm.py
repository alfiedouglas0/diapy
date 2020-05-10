import npyscreen
from os.path import join, abspath, dirname, basename

from ...config import Config
from ...db.db import DB
from ...utils import does_file_exist


class MainMenuForm(npyscreen.FormBaseNew):
    def create(self):
        self.db_path = self.add(npyscreen.TitleText, name="Database path:",
                                use_two_lines=False, value=Config.singleton.get_db_path())
        self.password = self.add(npyscreen.TitlePassword, name="Password:",
                                 use_two_lines=False, value="")

        self.add(npyscreen.ButtonPress, name="Exit", relx=12, rely=-3,
                 when_pressed_function=lambda: exit())
        self.add(npyscreen.ButtonPress,
                 name="Create new db", relx=-40, rely=-3,
                 when_pressed_function=self.go_to_new_db)
        self.add(npyscreen.ButtonPress, name="Connect", relx=-15, rely=-3,
                 when_pressed_function=self.connect_to_db)

    def go_to_new_db(self):
        self.parentApp.switchForm("NewDB")

    def connect_to_db(self):
        if self.db_path.value == "":
            npyscreen.notify_confirm(
                "Please enter a path for the database".format(
                    self.db_path.value),
                title='Error')
            return
        if not does_file_exist(self.db_path.value):
            npyscreen.notify_confirm(
                "The database path '{}' does not exist".format(
                    self.db_path.value),
                title='Error')
            return

        try:
            path = abspath(join(Config.get_root_path(), self.db_path.value))
            db = DB(path, self.password.value)
            Config.singleton.store_path = dirname(path)
            Config.singleton.db_name = basename(path)
            Config.singleton.save_config()
            self.parentApp.db = db
            self.parentApp.switchForm("EntriesList")
        except Exception as e:
            self.parentApp.db = None
            npyscreen.notify_confirm("Error: {}".format(str(e)), title='Error')
