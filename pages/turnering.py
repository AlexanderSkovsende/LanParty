from PyQt4 import QtGui
import random
import html

class Turnering:

    def __init__(self, parent):
        self.ui = parent.ui
        self.settings = parent.settings
        self.parent = parent

        self.ui.comboTurnering.currentIndexChanged.connect(self.update_turnering)
        self.ui.btnDelTurnering.clicked.connect(self.slet_turnering)
        self.ui.btnAddTeam.clicked.connect(self.add_team)
        self.ui.txtTeamName.returnPressed.connect(self.add_team) # Press ENTER
        self.ui.btnStartTurnering.clicked.connect(self.start_turnering)
        self.ui.tabsTurneringer.setEnabled(False)
        self.current = -1

        self.turneringer = self.settings.turneringer

        self.buttons = [[], []]

        self.update_choices()

    def update_choices(self):
        """Opdatér listen af turneringer"""

        self.ui.comboTurnering.clear()

        # Gør combo boxen usynlig, når der ikke er nogen åbne turneringer
        if len(self.turneringer) == 0:
            self.ui.comboTurnering.hide()
        else:
            self.ui.comboTurnering.show()

        names = [i['name'] for i in self.turneringer]
        for i in range(len(self.turneringer)):

            # Hvis navnet er der flere gange i listen, print typen også så man kan kende forskel
            if names.count(self.turneringer[i]['name']) > 1:
                self.ui.comboTurnering.addItem("{} ({})".format(self.turneringer[i]['name'], self.turneringer[i]['type']))
            else:
                self.ui.comboTurnering.addItem(self.turneringer[i]['name'])

    def update_turnering(self, idx):
        """Opdatér siden for den valgte turnering"""

        if idx != -1: # Hvis man har valgt en turnering

            self.ui.tabsTurneringer.setEnabled(True)

            # Indlæs og escape HTML (XSS)
            name = html.escape(self.turneringer[idx]['name'])
            ttype = html.escape(self.turneringer[idx]['type'])
            teams = html.escape(", ".join(self.turneringer[idx]['teams']))
            datetime = html.escape(self.turneringer[idx]['datetime'].toString())
            vinder = "<b>Vinder:</b> {}".format(html.escape(self.turneringer[idx]['vinder'])) if self.turneringer[idx]['vinder'] else ""

            self.ui.lblTurneringOversigt.setHtml(
                "<b>Turnering:</b> {0}<br>"
                "<b>Turneringstype:</b> {1}<br>"
                "<b>Start-tidspunkt:</b> {2}<br><br>"
                "<b>Hold:</b><br>{3}<br><br>{4}".format(name, ttype, datetime, teams, vinder))


            # Fjern alle knapper, så de kan indsættes senere.
            for i in reversed(range(self.ui.layoutKampeLeft.count())):
                self.ui.layoutKampeLeft.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.ui.layoutKampeRight.count())):
                self.ui.layoutKampeRight.itemAt(i).widget().setParent(None)

            self.buttons = [[], []]

            if "kampe" in self.turneringer[idx]:
                # Tegn kampe op

                kampe = self.turneringer[idx]["kampe"]

                for i in range(len(kampe)):
                    if kampe[i][2] == None:
                        self.buttons[0].append(KampButton(self, i, 0, kampe))
                        self.buttons[1].append(KampButton(self, i, 1, kampe))

                        self.buttons[0][i].setText(kampe[i][0])
                        self.ui.layoutKampeLeft.addWidget(self.buttons[0][i])

                        self.buttons[1][i].setText(kampe[i][1])
                        self.ui.layoutKampeRight.addWidget(self.buttons[1][i])
                    else:
                        self.buttons[0].append(KampButton(self, i, 0, kampe))
                        self.buttons[1].append(KampButton(self, i, 1, kampe))

                        self.buttons[0][i].setText(kampe[i][0])
                        self.buttons[0][i].setEnabled(False)
                        self.ui.layoutKampeLeft.addWidget(self.buttons[0][i])

                        self.buttons[1][i].setText(kampe[i][1])
                        self.buttons[1][i].setEnabled(False)
                        self.ui.layoutKampeRight.addWidget(self.buttons[1][i])

                        self.buttons[kampe[i][2]][i].setStyleSheet("color: green;")

        else: # Hvis listen af turneringer er tom
            self.ui.lblTurneringOversigt.setHtml("")
            self.ui.tabsTurneringer.setEnabled(False)

        if self.current != idx:
            self.ui.tabsTurneringer.setCurrentIndex(0)
        self.current = idx




    def add_team(self):
        """Tilføj hold til turnering"""

        name = self.ui.txtTeamName.text()

        # Validér holdnavnet: Må ikke findes allerede og må ikke indeholde komma (forvirrende)
        if len(name) > 0 and name.lower() not in [i.lower() for i in self.turneringer[self.current]['teams']] and ',' not in name:
            self.turneringer[self.current]['teams'].append(name)
            self.ui.txtTeamName.setText("")

        # Sortér listen af hold (case-insensitive)
        self.turneringer[self.current]['teams'] = sorted(self.turneringer[self.current]['teams'], key=lambda x: x.lower())

        self.update_turnering(self.current)

    def slet_turnering(self):
        """Slet turnering og opdatér"""

        del self.turneringer[self.current]

        self.update_choices()

    def start_turnering(self):
        """Sætter kampene op for den valgte turnering med de nuværende hold"""

        hold = self.turneringer[self.current]['teams']

        random.shuffle(hold)

        kampe = []

        while len(hold) > 1:
            kampe.append([hold[-1], hold[-2], None])
            hold = hold[:-2]

        self.turneringer[self.current]['afventer'] = None if not hold else hold[0]
        self.turneringer[self.current]['kampe'] = kampe

        self.turneringer[self.current]['fought'] = len(self.turneringer[self.current]['teams']) - 1

        self.update_turnering(self.current)

    def ny_vinder(self, vinder):
        """Sætter vinder af en kamp og/eller vinder af hele turneringen"""

        afventer = self.turneringer[self.current]['afventer']

        if afventer: # Hvis et hold afventer modstander
            self.turneringer[self.current]['kampe'].append([afventer, vinder, None])
            self.turneringer[self.current]['afventer'] = None
        else:
            self.turneringer[self.current]['afventer'] = vinder

        self.turneringer[self.current]['fought'] -= 1

        # Hvis turneringen er færdig
        if self.turneringer[self.current]['fought'] == 0:
            self.turneringer[self.current]['vinder'] = vinder

        self.update_turnering(self.current)


class KampButton(QtGui.QPushButton):
    def __init__(self, parent, i, x, kampe):
        super().__init__()
        self.i = i
        self.x = x
        self.parent = parent
        self.kampe = kampe

        self.clicked.connect(self.click)

    def click(self):

        self.kampe[self.i][2] = self.x
        self.parent.ny_vinder(self.kampe[self.i][self.x])
