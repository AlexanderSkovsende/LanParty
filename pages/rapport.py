class Rapport:

    def __init__(self, parent):
        self.ui = parent.ui
        self.settings = parent.settings
        self.parent = parent
        self.turneringer = self.parent.turnering.turneringer

        self.ui.btnLavRapport.clicked.connect(self.lav_rapport)



    def lav_rapport(self):
        # Indsamler data om Lan.
        deltagere = self.ui.tblTilmelding.rowCount()

        bord_lille = 0
        bord_stor = 0
        for row in range(deltagere):
            if self.ui.tblTilmelding.item(row, 2).text() == "Lille bord":
                bord_lille += 1
            else:
                bord_stor += 1

        power = 0
        for row in range(deltagere):
            power += int(self.ui.tblTilmelding.item(row, 3).text())



        mad_rows_ialt = self.ui.tblMad.rowCount() - 1
        pizza_count = self.ui.tblMad.item(mad_rows_ialt, 1).text()
        burger_count = self.ui.tblMad.item(mad_rows_ialt, 2).text()
        cola_count = self.ui.tblMad.item(mad_rows_ialt, 3).text()

        penge_indtjent = int(self.ui.tblMad.item(mad_rows_ialt, 4).text()[:-2])
        for row in range(deltagere):
            penge_indtjent += int(self.ui.tblTilmelding.item(row, 4).text()[:-2])



        antal_turneringer = len(self.turneringer)
        antal_hold, antal_kampe = 0, 0
        for turnering in self.turneringer:
            antal_hold += len(turnering["teams"])
            if "kampe" in turnering:
                antal_kampe += len(turnering["kampe"])

        with open('gui/rapport.html', 'r') as f:
            text = f.read()

        # Printer data om Lan.
        self.ui.txtRapport.setHtml(
            text.format(deltagere, bord_lille, bord_stor, power,
                    antal_turneringer, antal_hold, antal_kampe,
                    mad_rows_ialt, pizza_count, burger_count, cola_count, penge_indtjent))
