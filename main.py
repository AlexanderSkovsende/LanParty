import sys
from PyQt4 import QtCore, QtGui
from gui.main import Ui_MainWindow
from gui.turnering import Ui_Dialog

from pages import mad, turnering, settings, tilmeld, rapport


class StartQt4(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = settings.Settings(self)
        self.mad = mad.Mad(self)
        self.turnering = turnering.Turnering(self)
        self.tilmeld = tilmeld.Tilmeld(self)
        self.rapport = rapport.Rapport(self)

        self.turnering.dialog = TurneringDialog(self.turnering)
        self.ui.btnNewTurnering.clicked.connect(self.turnering.dialog.new)
        self.ui.btnEditTurnering.clicked.connect(self.turnering.dialog.edit)

        self.ui.btnTilmeld.clicked.connect(lambda: self.goto(1))
        self.ui.btnMad.clicked.connect(lambda: self.goto(2))
        self.ui.btnTurnering.clicked.connect(lambda: self.goto(3))
        self.ui.btnSettings.clicked.connect(lambda: self.goto(4))
        self.ui.btnRapport.clicked.connect(lambda: self.goto(5))
        self.ui.btnBack.clicked.connect(self.goto_menu)

        # Fix headers
        self.ui.tblTilmelding.horizontalHeader().setVisible(True)
        self.ui.tblMad.horizontalHeader().setVisible(True)

        self.goto_menu()

    def keyReleaseEvent(self, e):
        """Gå til menuen, når man trykker Escape"""

        if e.key() == 16777216:
            self.goto_menu()


    def goto_menu(self):
        """Gå til menuen og fjern back knappen"""

        self.ui.btnBack.hide()
        self.ui.stackedWidget.setCurrentIndex(0)

    def goto(self, id):
        """Gå til den n'de side"""

        self.ui.btnBack.show()
        self.ui.stackedWidget.setCurrentIndex(id)

    def closeEvent(self, event):
        """Gem indstillinger og data"""

        self.settings.saveToFile()





class TurneringDialog(QtGui.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.turneringer = parent.turneringer

        self.current = -1

        self.ui.btnSave.clicked.connect(self.save)


    def save(self):
        """Gem ændringer i turnering"""

        if len(self.ui.txtName.text()) > 0:

            if self.current == -1: # Hvis det er en ny turnering, tilføj til listen
                self.turneringer.append({'name': self.ui.txtName.text(), 'type': self.ui.txtType.text(), 'datetime': self.ui.dateTurnering.dateTime(), 'teams': [], 'vinder': None})
            else:
                self.turneringer[self.current]['name'] = self.ui.txtName.text()
                self.turneringer[self.current]['type'] = self.ui.txtType.text()
                self.turneringer[self.current]['datetime'] = self.ui.dateTurnering.dateTime()

            # Opdatér valg og sæt brugeren til rigtigt valg og forside
            self.parent.update_choices()
            if self.current == -1: self.parent.ui.comboTurnering.setCurrentIndex(len(self.turneringer) - 1)
            else: self.parent.ui.comboTurnering.setCurrentIndex(self.current)
            self.parent.ui.tabsTurneringer.setCurrentIndex(0)
            self.hide()

    def new(self):
        """Åbn vinduet for ny turnering"""

        self.current = -1
        self.ui.txtName.setText("")
        self.ui.txtType.setText("")
        self.ui.dateTurnering.setDate(QtCore.QDate.currentDate())

        self.show()


    def edit(self):
        """Edit turnering"""

        self.current = self.parent.ui.comboTurnering.currentIndex()
        self.ui.txtName.setText(self.turneringer[self.current]['name'])
        self.ui.txtType.setText(str(self.turneringer[self.current]['type']))
        self.ui.dateTurnering.setDateTime(self.turneringer[self.current]['datetime'])

        self.show()

    def showEvent(self, event):
        self.parent.parent.setEnabled(False)

    def hideEvent(self, event):
        self.parent.parent.setEnabled(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = StartQt4()
    ex.show()
    sys.exit(app.exec_())
