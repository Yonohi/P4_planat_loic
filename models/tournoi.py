from models.tour import Tour


class Tournoi:
    """ Chess tournament """
    def __init__(self, infos_tournoi):
        self.nom = infos_tournoi[0]
        self.lieu = infos_tournoi[1]
        self.date_debut = infos_tournoi[2]
        self.nombre_tours_prevus = 4
        self.joueurs = []
        self.joueurs_id = []
        self.tours = []
        self.tours_db = []
        self.nb_tour_en_cours = 0
        self.en_cours = True
        self.matchs_tournoi = []
        self.description = infos_tournoi[3]
        self.type = None
        self.id = None

    def __repr__(self):
        return f"{self.nom}"

    def enregistrer_index(self, table_tournaments):
        """
        Allows to save the index
        :param table_tournaments: tinydb table for tournaments
        """
        self.id = table_tournaments.all()[-1].doc_id

    def enregistrer_type(self, choix):
        """
        Save the type of chess
        :param choix: number chosen by user
        """
        dict_type = {1: "Blitz", 2: "Bullet", 3: "Speed"}
        self.type = dict_type[choix]

    def enregistrer_joueur(self, joueur):
        """
        Add a player to the list of players
        :param joueur: player instance
        """
        self.joueurs.append(joueur)

    def enregistrer_joueurs_id(self):
        """ Add a player's ID to the list"""
        self.joueurs_id = [joueur.id for joueur in self.joueurs]

    def creer_un_tour(self, number):
        """
        Creation of a round
        :param number: number of the round
        :return: round instance
        """
        tour = Tour(number)
        self.tours.append(tour)
        self.tours_db.append({"nom": tour.nom,
                              "date_debut": tour.date_debut,
                              "heure_debut": tour.heure_debut,
                              "date_fin": tour.date_fin,
                              "heure_fin": tour.heure_fin,
                              "matchs_id": tour.matchs_id,
                              "en_cours": tour.en_cours,
                              "fini": tour.fini})
        return tour

    def maj_tours_db(self, key, value):
        """
        Update the contents of a key with a new value
        :param key: a key in the dictionnary tours_db
        :param value: a value in the dictionnary tours_db
        """
        self.tours_db[-1][key] = value

    def enregistrer_matchs_tournoi(self, number_tour):
        """
        Recording of matches of a specific round
        :param number_tour: round number
        """
        self.matchs_tournoi.extend(self.tours[number_tour - 1].matchs)
