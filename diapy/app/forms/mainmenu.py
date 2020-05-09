import npyscreen

from ...config import Config


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
        pass
