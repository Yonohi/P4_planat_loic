
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


joueurs_test = [Joueur(["So", "Wesley", "12/12/1212", "M", 800]),
                Joueur(["Aronian", "Levon", "10/10/1876", "M", 1400]),
                Joueur(["Carlsen", "Magnus", "09/04/1676", "M", 5000]),
                Joueur(["Kasparov", "Garry", "07/08/1994", "M", 1000]),
                Joueur(["Yifan", "Hou", "10/05/1967", "F", 1500]),
                Joueur(["Caruana", "Fabiano", "06/09/1987", "M", 1200]),
                Joueur(["Nakamura", "Hikaru", "23/09/1982", "M", 3500]),
                Joueur(["Polgar", "Judith", "24/11/1956", "F", 2000])
                ]
