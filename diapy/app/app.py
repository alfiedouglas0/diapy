import npyscreen
from .forms.MainMenuForm import MainMenuForm
from .forms.CreateNewCBForm import CreateNewCBForm
from .forms.EntriesListForm import EntriesListForm
from .forms.EditEntryForm import EditEntryForm


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.db = None

        self.addForm("MAIN", MainMenuForm, name='CONNECT')
        self.addForm("NewDB", CreateNewCBForm, name='CREATE NEW DATABASE')
        self.addForm("EntriesList", EntriesListForm, name='ENTRIES')
        self.addFormClass("EntryEdit", EditEntryForm, name='EDIT ENTRY')
