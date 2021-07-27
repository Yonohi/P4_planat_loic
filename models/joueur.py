
class Joueur:
    """ Player participating in the tournament"""
    def __init__(self, infos):
        self.nom = infos[0]
        self.prenom = infos[1]
        self.date_naissance = infos[2]
        self.sexe = infos[3]
        self.classement = infos[4]
        self.points = 0
        self.id = None

    def __repr__(self):
        return f"{self.nom.capitalize()} {self.prenom}"

    def enregistrer_index(self, table_players):
        """
        Allows to save the index
        :param table_players: tinydb table of players
        """
        self.id = table_players.all()[-1].doc_id

    def ajout_score(self, score):
        """
        Add the score
        :param score: number of points earned by the player
        """
        self.points += score

    def modifier_classement(self, nouveau_classement):
        """
        Modify the ranking of the player
        :param nouveau_classement: new ranking
        """
        self.classement = nouveau_classement


joueurs_test = [Joueur(["Valjean", "Jean", "12/12/1212", "M", 800]),
                Joueur(["VanGrenier", "Archibald", "10/10/1876", "M", 167]),
                Joueur(["LeGaullois", "Perceval", "09/04/1676", "M", 5000]),
                Joueur(["Potter", "Harry", "07/08/1994", "M", 1000]),
                Joueur(["Tyler", "Bonny", "10/05/1967", "F", 500]),
                Joueur(["Pyrobarbare", "Bob", "06/09/1987", "M", 1200]),
                Joueur(["Hallen", "Barry", "23/09/1982", "M", 3500]),
                Joueur(["Polgar", "Judith", "24/11/1956", "F", 2000])
                ]
