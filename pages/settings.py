import pickle
from PyQt4 import QtGui

class Settings:

    def __init__(self, parent):
        self.ui = parent.ui
        self.parent = parent

        self.ui.btnGem.clicked.connect(self.save)
        self.ui.btnDefault.clicked.connect(self.setDefault)
        self.ui.btnResetAll.clicked.connect(self.reset_all)

        # Set Default settings
        self.setDefault()

        # Load fil og overwrite settings
        self.load()

        self.set_ui_values()

    def set_ui_values(self):
        """Set værdierne i UI'en"""

        self.ui.spinPizzaPris.setValue(self.pizza_pris)
        self.ui.spinBurgerPris.setValue(self.burger_pris)
        self.ui.spinColaPris.setValue(self.cola_pris)
        self.ui.spinLilleBord.setValue(self.lille_pris)
        self.ui.spinStortBord.setValue(self.stor_pris)

        try:
            self.parent.mad.get_sum()
        except AttributeError:
            pass

    def setDefault(self):
        """Sætter standardindstillinger"""

        self.pizza_pris = 55
        self.burger_pris = 45
        self.cola_pris = 12
        self.lille_pris = 60
        self.stor_pris = 90

        try: # Hvis self.turneringer allerede findes (Når man trykker på Nulstil indstillinger:
            self.turneringer.clear()
        except AttributeError:
            self.turneringer = []

        self.set_ui_values()



    def save(self):
        """Gem indstillinger"""

        self.pizza_pris = self.ui.spinPizzaPris.value()
        self.burger_pris = self.ui.spinBurgerPris.value()
        self.cola_pris = self.ui.spinColaPris.value()
        self.parent.mad.get_sum()

        self.lille_pris = self.ui.spinLilleBord.value()
        self.stor_pris = self.ui.spinStortBord.value()

        self.saveToFile()

    def saveToFile(self):
        """Gemmer alt data til en fil"""

        #Gem tilmeldings-table
        w, h = 5, self.ui.tblTilmelding.rowCount()
        tilmeldingMatrix = [[0 for x in range(w)] for y in range(h)]
        for i in range(h):
            for j in range(w):
                tilmeldingMatrix[i][j] = str(self.ui.tblTilmelding.item(i, j).text())

        # Gem mad-table
        w2, h2 = 5, self.ui.tblMad.rowCount()
        madMatrix = [[0 for x in range(w2)] for y in range(h2)]
        for i in range(h2):
            for j in range(w2):
                madMatrix[i][j] = str(self.ui.tblMad.item(i, j).text())

        save_array = [self.pizza_pris, self.burger_pris, self.cola_pris, self.lille_pris, self.stor_pris, tilmeldingMatrix, madMatrix, self.turneringer]
        pickle.dump(save_array, open("save.dat", "wb"))


    def load(self):
        """Åbner save.dat, hvis den findes"""

        try:
            savefile = pickle.load(open("save.dat", 'rb'))
            self.pizza_pris = savefile[0]
            self.burger_pris = savefile[1]
            self.cola_pris = savefile[2]
            self.lille_pris = savefile[3]
            self.stor_pris = savefile[4]

            # Load QTableWidgets
            h = len(savefile[5])
            for i in range(h):
                self.ui.tblTilmelding.insertRow(i)
                for j in range(5):
                    self.ui.tblTilmelding.setItem(i, j, QtGui.QTableWidgetItem(savefile[5][i][j]))

            h = len(savefile[6])
            for i in range(h):
                self.ui.tblMad.insertRow(i)
                for j in range(5):
                    self.ui.tblMad.setItem(i, j, QtGui.QTableWidgetItem(savefile[6][i][j]))

            # Load turnering
            self.turneringer = savefile[7]

        except Exception:
            pass  # Der findes ingen indstillinger endnu


    def reset_all(self):
        """Nulstiller alle værdier fra LanPartyet"""

        self.ui.tblTilmelding.setRowCount(0)

        self.ui.tblMad.setRowCount(0)
        self.ui.tblMad.insertRow(0)
        self.ui.tblMad.setItem(0, 0, QtGui.QTableWidgetItem("Samlet"))
        for i in range(1, 4):
            self.ui.tblMad.setItem(0, i, QtGui.QTableWidgetItem("0"))
        self.ui.tblMad.setItem(0, 4, QtGui.QTableWidgetItem("0,-"))
        self.parent.mad.total = [0]*4

        self.turneringer.clear()
        self.parent.turnering.update_choices()
        self.parent.turnering.update_turnering(-1)

        self.ui.txtRapport.setHtml("")

