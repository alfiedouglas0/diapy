import npyscreen
from .forms.MainMenuForm import MainMenuForm
from .forms.CreateNewCBForm import CreateNewCBForm
from .forms.EntriesListForm import EntriesListForm
from .forms.EditEntryForm import EditEntryForm


class App(npyscreen.NPSAppManaged):
    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, val):
        self._db = val
        self.notify_db_changed()

    @property
    def selectedEntry(self):
        return self._selectedEntry

    @selectedEntry.setter
    def selectedEntry(self, val):
        self._selectedEntry = val

    def onStart(self):
        self._db = None
        self._selectedEntry = None
        self.unsavedChanges = False
        self._db_listeners = []

        self.main_form = self.addForm("MAIN", MainMenuForm, name='CONNECT')
        self.newdb_form = self.addForm(
            "NewDB", CreateNewCBForm, name='CREATE NEW DATABASE')
        self.enties_form = self.addForm(
            "EntriesList", EntriesListForm, name='ENTRIES')
        self.addFormClass("EntryEdit", EditEntryForm, name='EDIT ENTRY')

    def onCleanExit(self):
        if self.db != None and self.unsavedChanges:
            save = npyscreen.notify_yes_no("Would you like to save changes?",
                                           title="Unsaved Changes")
            if save:
                self.db.save()

    def addDBListener(self, callback):
        self._db_listeners.append(callback)

    def notify_db_changed(self):
        for callback in self._db_listeners:
            callback(self.db)
