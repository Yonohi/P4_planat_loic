from models.joueur import Joueur
from models.tournoi import Tournoi
from models.tour import Tour
from vue.vue import Vue
from controller.tri import Tri
import time
import copy
from tinydb import TinyDB, Query

NOMBRE_JOUEURS = 8

db = TinyDB("db.json")
table_players = db.table("Players")
table_tournaments = db.table("Tournaments")
print(time.strftime("%d/%m/%Y"))
print(time.strftime("%I:%M:%S %p"))


class ControleurPrincipal:
    """ Class interacting between View and Model"""
    def __init__(self):
        self.vue = Vue()
        self.tri = Tri()

    def obtenir_joueurs(self, tournoi):
        """
        Method for creating player entities
        according to the number of players
        :param tournoi: tournament instance where players will be saved
        """
        i = 1
        for x in range(0, NOMBRE_JOUEURS):
            # collect player via view
            infos = self.vue.demander_info_joueur(i)
            joueur = Joueur(infos)
            # add to the list of players
            tournoi.enregistrer_joueur(joueur)
            i += 1

    def resultat_match(self, binomes):
        """
        Get the results and display the results of the different matches
        :param binomes: list of pairs
        """
        for binome in binomes:
            while True:
                score_un = self.vue.entree_resultats(binome[0])
                score_deux = self.vue.entree_resultats(binome[1])
                if score_un + score_deux != 1:
                    self.vue.erreur_score()
                    continue
                else:
                    binome[0].ajout_score(score_un)
                    binome[1].ajout_score(score_deux)
                    table_players.update({"score": binome[0].points},
                                         doc_ids=[binome[0].id])
                    table_players.update({"score": binome[1].points},
                                         doc_ids=[binome[1].id])
                    break
        self.vue.afficher_resultats(binomes)

    # DataBase
    @staticmethod
    def serialisation_tournoi(tournoi):
        """
        Dictionary of a tournament
        :param tournoi: tournament instance
        :return: serialized tournament
        """
        serialized_tournoi = {
            "nom": tournoi.nom,
            "lieu": tournoi.lieu,
            "dates": tournoi.dates,
            "nb tours prevus": tournoi.nombre_tours_prevus,
            "id_participants": tournoi.joueurs_id,
            "tours_effectues": tournoi.nb_tour_en_cours,
            "tours_db": tournoi.tours_db,
            "description": tournoi.description,
            "type": tournoi.type,
            "id": tournoi.id,
            "en_cours": tournoi.en_cours
        }
        return serialized_tournoi

    def deserialisation_tournoi(self, tournoi_serialise):
        """
        Resetting to Tournament Instance
        :param tournoi_serialise: serialized tournament
        :return: deserialized tournament
        """
        infos = [tournoi_serialise['nom'],
                 tournoi_serialise['lieu'],
                 tournoi_serialise['dates'],
                 tournoi_serialise['description']]
        tournoi = Tournoi(infos)
        tournoi.nombre_tours = tournoi_serialise["nb tours prevus"]
        tournoi.joueurs_id = tournoi_serialise["id_participants"]
        tournoi.nb_tour_en_cours = tournoi_serialise["tours_effectues"]
        tournoi.tours_db = tournoi_serialise["tours_db"]
        tournoi.matchs_tournoi = \
            copy.deepcopy([match for tour in tournoi_serialise["tours_db"]
                           for match in tour["matchs_id"]])
        tournoi.type = tournoi_serialise["type"]
        tournoi.id = tournoi_serialise["id"]
        tournoi.en_cours = tournoi_serialise["en_cours"]
        query = Query()
        # We take the player IDs to retrieve the stored players
        for index in tournoi.joueurs_id:
            joueur_serialise = table_players.search(query.id == int(index))[0]
            joueur_deserialise = self.deserialisation_joueur(joueur_serialise)
            tournoi.joueurs.append(joueur_deserialise)
        # We recover the different matches that took place
        for binome in tournoi.matchs_tournoi:
            for joueur_id in binome:
                for joueur in tournoi.joueurs:
                    if joueur.id == joueur_id[0]:
                        joueur_id[0] = joueur
        # We recreate rounds instances
        for index, tour_db in enumerate(tournoi.tours_db):
            tour = Tour(index + 1)
            tour.date_debut = tour_db["date_debut"]
            tour.heure_debut = tour_db["heure_debut"]
            tour.date_fin = tour_db["date_fin"]
            tour.heure_fin = tour_db["heure_fin"]
            tour.matchs_id = tour_db["matchs_id"]
            tour.en_cours = tour_db["en_cours"]
            tour.fini = tour_db["fini"]
            tour.matchs = tournoi.matchs_tournoi[index]
            tournoi.tours.append(tour)
        return tournoi

    @staticmethod
    def serialisation_joueur(joueur):
        """
        Dictionary of a player
        :param joueur: player instance
        :return: serialized player
        """
        serialized_player = {"nom": joueur.nom,
                             "prenom": joueur.prenom,
                             "date_naissance": joueur.date_naissance,
                             "sexe": joueur.sexe,
                             "classement": joueur.classement,
                             "score": joueur.points,
                             "id": joueur.id
                             }
        return serialized_player

    @staticmethod
    def deserialisation_joueur(joueur_serialise):
        """
        Reset to Player instance status
        :param joueur_serialise: serialized player
        :return: player instance
        """
        infos = [joueur_serialise['nom'],
                 joueur_serialise['prenom'],
                 joueur_serialise['date_naissance'],
                 joueur_serialise['sexe'],
                 joueur_serialise['classement']]
        joueur = Joueur(infos)
        joueur.points = joueur_serialise['score']
        joueur.id = joueur_serialise['id']
        return joueur

    @staticmethod
    def enregistrer_donnees(table, donnees):
        """
        Single or multiple data storage
        :param table: tinydb table
        :param donnees: information to insert in the table
        """
        if type(donnees) == list:
            table.insert_multiple(donnees)
        else:
            table.insert(donnees)

    # the methods organizing the whole code
    def lancement_tours(self, tournoi, nb=1, reprise=False):
        """
        Method for the launch of rounds
        :param tournoi: tournament instance
        :param nb: round number to access
        :param reprise: True if tournament resomption
        """
        i = nb
        stop = False
        # We create our pairs by ranking
        binomes_classement = \
            self.tri.tri_classement(tournoi.joueurs, NOMBRE_JOUEURS)
        binomes_points = []
        # We launch the loop of the tournament
        # stopping at the number of rounds planned (4)
        while tournoi.en_cours and not stop:
            # We create a round instance and its loop
            if tournoi.tours and reprise and tournoi.tours[-1].en_cours:
                reprise = False
                tour = tournoi.tours[-1]
            else:
                tour = tournoi.creer_un_tour(i)
            # Used to set the nb_tour_en_cours attribute to 1
            if i == 1 and tournoi.nb_tour_en_cours == 0:
                tournoi.nb_tour_en_cours += 1
            table_tournaments.update(
                {"tours_effectues": tournoi.nb_tour_en_cours},
                doc_ids=[tournoi.id])
            # Loop of the round
            while tour.fini is False and not stop:
                choix_tournoi = \
                    self.vue.menu_tournoi(i, tour_en_cours=tour.en_cours)
                # Choice 1 and no round started
                if choix_tournoi == 1 and not tour.en_cours:
                    # Launch of the round
                    tour.en_cours = True
                    # data logging
                    tour.enregistrer_temps_debut()
                    tournoi.maj_tours_db("en_cours", tour.en_cours)
                    tournoi.maj_tours_db("date_debut", tour.date_debut)
                    tournoi.maj_tours_db("heure_debut", tour.heure_debut)
                    table_tournaments.update({"tours_db": tournoi.tours_db},
                                             doc_ids=[tournoi.id])
                    # Show matches
                    if i == 1:
                        # matches sorted by ranking for 1st round
                        self.vue.afficher_match(binomes_classement)
                        tour.enregistrer_matchs_tour(binomes_classement)
                    else:
                        # matches sorted by points and rankings
                        binomes_points = self.tri.tri_points(tournoi,
                                                             tournoi.joueurs,
                                                             NOMBRE_JOUEURS)
                        self.vue.afficher_match(binomes_points)
                        tour.enregistrer_matchs_tour(binomes_points)
                    # Match logging
                    tournoi.enregistrer_matchs_tournoi(i)
                    tournoi.maj_tours_db("matchs_id", tour.matchs_id)
                    table_tournaments.update({"tours_db": tournoi.tours_db},
                                             doc_ids=[tournoi.id])
                # Choice 1 and round launched
                elif choix_tournoi == 1 and tour.en_cours:
                    tour.en_cours = False
                    tour.enregistrer_temps_fin()
                    if i == 1:
                        self.resultat_match(binomes_classement)
                    else:
                        self.resultat_match(binomes_points)
                    tour.fini = True
                    # Data logging
                    tournoi.maj_tours_db("en_cours", tour.en_cours)
                    tournoi.maj_tours_db("date_fin", tour.date_fin)
                    tournoi.maj_tours_db("heure_fin", tour.heure_fin)
                    tournoi.maj_tours_db("fini", tour.fini)
                    table_tournaments.update({"tours_db": tournoi.tours_db},
                                             doc_ids=[tournoi.id])
                    tournoi.nb_tour_en_cours += 1
                    i += 1
                # Display the ranking of participants
                elif choix_tournoi == 2:
                    self.vue.classement_joueur(tournoi.joueurs)
                # Modify a participant's ranking
                elif choix_tournoi == 3:
                    choix_joueur = self.vue.choix_classement(tournoi.joueurs,
                                                             NOMBRE_JOUEURS)
                    classement = self.vue.nouveau_classement(choix_joueur)
                    choix_joueur.modifier_classement(classement)
                # Choice of stopping the tournament
                elif choix_tournoi == 4:
                    stop = True
            # End of tournament
            if i == (tournoi.nombre_tours_prevus + 1):
                tournoi.en_cours = False
                table_tournaments.update({"en_cours": tournoi.en_cours},
                                         doc_ids=[tournoi.id])
        self.vue.fin_tournoi()

    def enregistrement_joueurs(self, tournoi):
        """
        Allow to save players in the database
        :param tournoi: tournament instance
        """
        self.obtenir_joueurs(tournoi)
        # Line for registered players (add joueurs_test to import)
        # tournoi.joueurs = joueurs_test
        for joueur in tournoi.joueurs:
            joueur_serialise = self.serialisation_joueur(joueur)
            query = Query()
            condition = query.nom == f"{joueur.nom}"
            doublon = False
            if table_players.contains(condition):
                existants = table_players.search(condition)
                for existant in existants:
                    if existant["prenom"] == joueur.prenom:
                        doublon = True
                        joueur.id = existant["id"]
                        if existant["classement"] != joueur.classement:
                            table_players.update(
                                {"classement": joueur.classement},
                                doc_ids=[existant["id"]])
            if not doublon:
                self.enregistrer_donnees(table_players, joueur_serialise)
                joueur.enregistrer_index(table_players)
                table_players.update({"id": joueur.id}, doc_ids=[joueur.id])

    def lancement_tournoi(self):
        """
        Method for the launch of the tournament
        :return: tournament instance
        """
        # Information gathering
        infos_tournoi = self.vue.demander_info_tournoi()
        tournoi = Tournoi(infos_tournoi)
        choix_type = self.vue.demander_type()
        tournoi.enregistrer_type(choix_type)
        tournoi_serialise = self.serialisation_tournoi(tournoi)
        self.enregistrer_donnees(table_tournaments, tournoi_serialise)
        tournoi.enregistrer_index(table_tournaments)
        table_tournaments.update({"id": tournoi.id}, doc_ids=[tournoi.id])
        self.enregistrement_joueurs(tournoi)
        tournoi.enregistrer_joueurs_id()
        table_tournaments.update({"id_participants": tournoi.joueurs_id},
                                 doc_ids=[tournoi.id])
        return tournoi

    def lancer_programme(self):
        """ Method for the launch of the program"""
        quitter = False
        self.vue.message_bienvenue()
        while not quitter:
            choix_principal = self.vue.menu_principal()
            # Choice of creating a new Tournament
            if choix_principal == 1:
                tournoi = self.lancement_tournoi()
                self.lancement_tours(tournoi)
            # Choice to resume a tournament
            elif choix_principal == 2:
                q = Query()
                # We are looking for current tournaments
                tournois = table_tournaments.search(q.en_cours == bool(True))
                if not tournois:
                    print("Il n'y a apparement pas de tournoi en cours.")
                else:
                    # Selection of the desired tournament
                    choix_reprise = self.vue.menu_reprendre_tournoi(tournois)
                    tournoi_reprise = tournois[choix_reprise - 1]
                    tournoi = self.deserialisation_tournoi(tournoi_reprise)
                    if len(tournoi.joueurs) < NOMBRE_JOUEURS:
                        self.enregistrement_joueurs(tournoi)
                        tournoi.enregistrer_joueurs_id()
                        table_tournaments.update(
                            {"id_participants": tournoi.joueurs_id},
                            doc_ids=[tournoi.id])
                    if tournoi.nb_tour_en_cours == 0:
                        self.lancement_tours(tournoi, reprise=True)
                    else:
                        self.lancement_tours(tournoi,
                                             nb=tournoi.nb_tour_en_cours,
                                             reprise=True)
            # Choice to have a report on ...
            elif choix_principal == 3:
                choix_rapport = self.vue.menu_rapport()
                # List of all players in the database
                if choix_rapport == 1:
                    ordre = self.vue.choisir_ordre()
                    self.vue.afficher_all_participants(table_players, ordre)
                # List of players in a particular Tournament
                if choix_rapport == 2:
                    q = Query()
                    id_tournoi = self.vue.selection_tournoi(table_tournaments)
                    ordre = self.vue.choisir_ordre()
                    tournoi_serialise = table_tournaments.search(
                        q.id == int(id_tournoi))[0]
                    tournoi = self.deserialisation_tournoi(tournoi_serialise)
                    self.vue.afficher_joueurs_tournoi(tournoi, ordre)
                # List of all Tournaments
                if choix_rapport == 3:
                    list_tournaments = table_tournaments.all()
                    self.vue.afficher_tournois(list_tournaments)
                # List of all rounds in a Tournament
                if choix_rapport == 4:
                    q = Query()
                    id_tournoi = self.vue.selection_tournoi(table_tournaments)
                    tournoi_serialise = table_tournaments.search(
                        q.id == int(id_tournoi))[0]
                    tournoi = self.deserialisation_tournoi(tournoi_serialise)
                    self.vue.afficher_tours(tournoi)
                # List of all matches in a Tournament
                if choix_rapport == 5:
                    q = Query()
                    id_tournoi = self.vue.selection_tournoi(table_tournaments)
                    tournoi_serialise = table_tournaments.search(
                        q.id == int(id_tournoi))[0]
                    tournoi = self.deserialisation_tournoi(tournoi_serialise)
                    self.vue.afficher_matchs_tournoi(tournoi)
            # Choice to stop the program
            elif choix_principal == 4:
                quitter = True
