from PyQt4 import QtGui

class Tilmeld:

    def __init__(self, parent):
        self.ui = parent.ui
        self.settings = parent.settings
        self.ui.btnAddTilmeld.clicked.connect(self.tilmeld)
        self.ui.tblTilmelding.keyReleaseEvent = lambda e: self.remove_row(e) # Detect Key Press


    def remove_row(self,e):
        """Fjern valgte rows"""

        if e.key() == 16777223: # Delete knappen

            # Fjern valgte indices fra højest til lavest (vigtigt)
            indices = sorted([index.row() for index in self.ui.tblTilmelding.selectedIndexes()], reverse=True)

            for i in indices:
                self.ui.tblTilmelding.removeRow(i)

    def tilmeld(self):
        """Tilføj tilmelding"""

        if len(self.ui.txtNameTilmeld.text()) > 2:

            tilmeldArray = []
            tilmeldArray.append(self.ui.txtNameTilmeld.text())
            tilmeldArray.append(self.ui.txtKlasse.text())
            tilmeldArray.append(self.ui.comboBord.currentText())
            tilmeldArray.append(self.ui.spinPower.value())
            rowPosition = self.ui.tblTilmelding.rowCount()
            self.ui.tblTilmelding.insertRow(rowPosition)
            for x in range(0,4):
                self.ui.tblTilmelding.setItem(rowPosition, x, QtGui.QTableWidgetItem(str(tilmeldArray[x])))

            if tilmeldArray[2] == "Stort bord":
                self.ui.tblTilmelding.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(self.settings.stor_pris) + ",-"))
            else:
                self.ui.tblTilmelding.setItem(rowPosition, 4, QtGui.QTableWidgetItem(str(self.settings.lille_pris) + ",-"))
