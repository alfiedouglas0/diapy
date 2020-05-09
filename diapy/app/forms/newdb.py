import npyscreen
from os.path import join, abspath, dirname, basename

from ...config import Config
from ...db.dbsetup import create_db
from ...db.db import DB
from ...utils import does_file_exist


class CreateNewCBForm(npyscreen.ActionPopup):
    def create(self):
        self.db_path = self.add(npyscreen.TitleText, name="Database path:",
                                use_two_lines=False, value=Config.singleton.get_db_path())
        self.password = self.add(npyscreen.TitlePassword, name="Password:",
                                 use_two_lines=False, value="")

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def on_ok(self):
        if self.db_path.value == "":
            npyscreen.notify_confirm(
                "Please enter a path for the database".format(
                    self.db_path.value),
                title='Error')
            return
        if does_file_exist(self.db_path.value):
            npyscreen.notify_confirm(
                "The database path '{}' already exists".format(
                    self.db_path.value),
                title='Error')
            return

        try:
            path = abspath(join(Config.get_root_path(), self.db_path.value))
            create_db(path, self.password.value)

            Config.singleton.store_path = dirname(path)
            Config.singleton.db_name = basename(path)
            Config.singleton.save_config()
            db = DB(path, self.password.value)
        except Exception as e:
            npyscreen.notify_confirm("Error: {}".format(str(e)), title='Error')
