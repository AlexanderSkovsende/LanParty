from PyQt4 import QtGui
import re

class Mad:

    def __init__(self, parent):
        self.ui = parent.ui
        self.settings = parent.settings

        self.ui.btnBestilMad.clicked.connect(self.bestil)

        self.ui.spinPizza.valueChanged.connect(self.get_sum)
        self.ui.spinBurger.valueChanged.connect(self.get_sum)
        self.ui.spinCola.valueChanged.connect(self.get_sum)
        self.ui.tblMad.keyReleaseEvent = lambda e: self.remove_row(e) # Detect Key Press

        if self.ui.tblMad.rowCount() == 0:
            self.ui.tblMad.insertRow(0)
            self.ui.tblMad.setItem(0, 0, QtGui.QTableWidgetItem("Samlet"))
            for i in range(1, 4):
                self.ui.tblMad.setItem(0, i, QtGui.QTableWidgetItem("0"))
            self.ui.tblMad.setItem(0, 4, QtGui.QTableWidgetItem("0,-"))

        self.get_sum()

    def remove_row(self,e):
        """Fjern valgte rows"""

        if e.key() == 16777223: # Delete knappen

            # Fjern valgte indices fra højest til lavest (vigtigt)
            indices = sorted([index.row() for index in self.ui.tblMad.selectedIndexes()], reverse=True)

            for i in indices:
                if i < self.ui.tblMad.rowCount()-1:
                    row_pos = self.ui.tblMad.rowCount() - 1

                    # Opdater total
                    for j in range(1, 4):
                        t = int(self.ui.tblMad.item(row_pos, j).text()) - int(self.ui.tblMad.item(i, j).text())

                        self.ui.tblMad.setItem(row_pos, j, QtGui.QTableWidgetItem(str(t)))

                    t = int(self.ui.tblMad.item(row_pos, 4).text()[:-2]) - int(self.ui.tblMad.item(i, 4).text()[:-2])
                    self.ui.tblMad.setItem(row_pos, 4, QtGui.QTableWidgetItem(str(t) + ",-"))


                    self.ui.tblMad.removeRow(i)

    def bestil(self):
        """Tilføj bestilling"""

        if len(self.ui.txtNameMad.text()) > 2:

            name = self.ui.txtNameMad.text()
            pizza_count = self.ui.spinPizza.value()
            burger_count = self.ui.spinBurger.value()
            cola_count = self.ui.spinCola.value()
            samlet = self.ui.lblSamlet.text()

            if pizza_count + burger_count + cola_count == 0: # Hvis man ikke har bestilt noget
                return

            mad_array = [name, str(pizza_count), str(burger_count), str(cola_count), samlet]

            row_pos = self.ui.tblMad.rowCount()-1

            # Opdater total
            for i in range(1, 4):
                t = int(self.ui.tblMad.item(row_pos, i).text()) + int(mad_array[i])
                self.ui.tblMad.setItem(row_pos, i, QtGui.QTableWidgetItem(str(t)))

            t = int(self.ui.tblMad.item(row_pos, 4).text()[:-2]) + self.get_sum()
            self.ui.tblMad.setItem(row_pos, 4, QtGui.QTableWidgetItem(str(t)+",-"))

            # Indsæt nye tal
            self.ui.tblMad.insertRow(row_pos)

            for i in range(0, 5):
                self.ui.tblMad.setItem(row_pos, i, QtGui.QTableWidgetItem(mad_array[i]))

    def get_sum(self):
        """Find prisen af de valgte madvarer"""

        pizza_count = self.ui.spinPizza.value()
        burger_count = self.ui.spinBurger.value()
        cola_count = self.ui.spinCola.value()

        s = pizza_count*self.settings.pizza_pris + burger_count*self.settings.burger_pris + cola_count*self.settings.cola_pris

        self.ui.lblPizza.setText(str(self.settings.pizza_pris) + ",-")
        self.ui.lblBurger.setText(str(self.settings.burger_pris) + ",-")
        self.ui.lblCola.setText(str(self.settings.cola_pris) + ",-")
        self.ui.lblSamlet.setText(str(s) + ",-")

        return s
