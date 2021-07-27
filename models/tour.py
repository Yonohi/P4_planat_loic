import time


class Tour:
    """ Round class"""
    def __init__(self, number):
        self.nom = f"Round {number}"
        self.date_debut = None
        self.heure_debut = None
        self.date_fin = None
        self.heure_fin = None
        self.matchs = []
        self.matchs_id = []
        self.en_cours = False
        self.fini = False

    def __repr__(self):
        return f"{self.nom}"

    def enregistrer_matchs_tour(self, binomes):
        """
        Logging of matches in a round
        :param binomes: list of pairs
        """
        for binome in binomes:
            match = ([binome[0], binome[0].points],
                     [binome[1], binome[1].points])
            match_id = ([binome[0].id, binome[0].points],
                        [binome[1].id, binome[1].points])
            self.matchs.append(match)
            self.matchs_id.append(match_id)

    def enregistrer_temps_debut(self):
        """ Method which collect time at the start of a round"""
        self.date_debut = time.strftime("%d/%m/%Y")
        self.heure_debut = time.strftime("%I:%M:%S %p")

    def enregistrer_temps_fin(self):
        """ Method which collect time at the end of a round"""
        self.date_fin = time.strftime("%d/%m/%Y")
        self.heure_fin = time.strftime("%I:%M:%S %p")
