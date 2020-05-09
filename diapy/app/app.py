import npyscreen
from .forms.mainmenu import MainMenuForm
from .forms.newdb import CreateNewCBForm


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenuForm, name='Connect',
                     minimum_lines=15, minimum_columns=30)
        self.addForm("NewDB", CreateNewCBForm, name='Create New Database',
                     minimum_lines=15, minimum_columns=30)
