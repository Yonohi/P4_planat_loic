import random
import re


class Vue:
    """ Class allowing exchanges with the user"""
    @staticmethod
    def demander_info_tournoi():
        """
        Retrieves the various tournament information
        :return: information to create a tournament instance
        """
        print("-------------------------\n"
              "Veuillez rentrer les informations du Tournoi.")
        while True:
            try:
                nom = input("Nom : ")
                if not nom:
                    raise ValueError
                lieu = input("Lieu : ")
                if not lieu:
                    raise ValueError
                date_debut = input("Date JJ/MM/AAAA: ")
                regex = r"^\d{2}/\d{2}/\d{4}$"
                if re.match(regex, date_debut) is None:
                    raise ValueError
                description = input("Description : ")
                break
            except ValueError:
                print("La donnée rentrée n'est pas correct."
                      " Veuillez tout ressaisir.")
        return nom, lieu, date_debut, description

    @staticmethod
    def demander_info_joueur(numero):
        """
        Retrieves player information
        :param numero: number of the player
        :return: information to create player instances
        """
        while True:
            try:
                print("-------------------------\n"
                      f"Veuillez rentrer les informations du Joueur {numero}.")
                nom = input("Nom : ")
                if not nom:
                    raise ValueError
                prenom = input("Prénom : ")
                if not prenom:
                    raise ValueError
                date_naissance = input("Date de naissance JJ/MM/AAAA: ")
                regex = r"^\d{2}/\d{2}/\d{4}$"
                if re.match(regex, date_naissance) is None:
                    raise ValueError
                sexe = input("Sexe M/F: ").upper()
                if sexe not in ["M", "F"]:
                    raise ValueError
                classement = int(input("Classement : "))
                if classement < 0:
                    raise ValueError
                return nom, prenom, date_naissance, sexe, classement
            except ValueError:
                print("La donnée rentrée n'est pas correct."
                      " Veuillez ressaisir l'intégralité des informations")

    @staticmethod
    def demander_type():
        """
        Retrieves information about the type of chess
        :return: number chosen by the user
        """
        print("\nQuel sera le type d'échec de ce tournoi?\n"
              "\t1. Blitz\n"
              "\t2. Bullet\n"
              "\t3. Speed\n")
        while True:
            try:
                choix = int(input("Votre choix : "))
                if choix not in [1, 2, 3]:
                    raise ValueError
                break
            except ValueError:
                print("Choix invalide, veuillez ressaisir votre choix.\n")

        return choix

    @staticmethod
    def demander_binomes(liste_joueurs, nombre_joueurs):
        """
        In the case of a problem with the algorithm
        Asks the user to select the meetings themselves
        :param liste_joueurs: player list of the tournament
        :param nombre_joueurs: total number of players
        :return: list of pairs
        """
        liste_binomes = []
        liste_selection = []
        print("Suite à un problème lié à l'algorithme, "
              "impossible de trouver des binomes valides.\n"
              "Veuillez inscrire les binomes.\n"
              "Liste des participants:")
        for i in range(nombre_joueurs):
            print(f"{i + 1}. {liste_joueurs[i]}, "
                  f"Score : {liste_joueurs[i].points}")
        nb_binomes = 0
        while nb_binomes < nombre_joueurs / 2:
            try:
                first = int(input("Sélectionnez un participant : "))
                second = int(input("Son adversaire : "))
                if first not in range(nombre_joueurs + 1) \
                        or second not in range(nombre_joueurs + 1):
                    raise ValueError
                first_player = liste_joueurs[first-1]
                second_player = liste_joueurs[second-1]
            except ValueError:
                print("Vous n'avez pas saisi un nombre valide.\n"
                      "Veuillez redéfinir tous les participants.")
                nb_binomes = 0
                continue
            liste_binomes.append((first_player, second_player))
            liste_selection.extend((first_player, second_player))
            nb_binomes += 1
            if nb_binomes == 4:
                for joueur in liste_joueurs:
                    if liste_selection.count(joueur) > 1:
                        print("Vous avez sélectionné plusieurs fois "
                              "le même joueur.\n"
                              "Veuillez resaisir les matchs.")
                        liste_binomes = []
                        nb_binomes = 0
                        break

        return liste_binomes

    def afficher_match(self, binomes):
        """
        Show the meetings
        :param binomes: list of pairs
        """
        print("\nLe tour verra s'affronter les joueurs:")
        for binome in binomes:
            print(f"\t{binome[0].nom} {binome[0].prenom} "
                  f"VS {binome[1].nom} {binome[1].prenom}")
            self.tirage_au_sort(binome)

    @staticmethod
    def tirage_au_sort(binome):
        """
        Choose which player will play with white
        and which one will play with the blacks
        :param binome: list of pairs
        """
        index = random.randint(0, 1)
        print(f"Le joueur {binome[index]} aura les blancs.")
        print(f"Le joueur {binome[index-1]} aura les noirs.\n")

    @staticmethod
    def entree_resultats(joueur):
        """
        Retrieves a player's results
        :param joueur: player instance
        :return: score of the player
        """
        while True:
            try:
                score = input(f"Score {joueur.nom} {joueur.prenom} "
                              f"(0, 1/2, 1): ")
                if score == "1/2":
                    score = 0.5
                    break
                score = float(score)
                if score not in [0, 0.5, 1]:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("\nVous n'avez pas rentré de valeurs correctes."
                      "\n\tVeuillez ressaisir le score.\n")

        return score

    @staticmethod
    def erreur_score():
        """ Error message when score written by the user are not good"""
        print("Vous n'avez pas rentré des scores corrects par match.\n"
              "Veuillez recommencer.")

    @staticmethod
    def afficher_resultats(binomes):
        """
        Displays the results of the matches of the just finished round
        :param binomes: list of pairs
        """
        print("\n\tRésumé des résultats:")
        for binome in binomes:
            for joueur in binome:
                print(f"{joueur.nom} {joueur.prenom}" 
                      f" a {joueur.points} points.")

    @staticmethod
    def message_bienvenue():
        """ Simple welcome message """
        print("Bienvenue".center(50),
              "\n\nVous venez de rentrer dans le programme d'échecs "
              "en tournoi suisse.\n"
              "-------------------------\n")

    @staticmethod
    def menu_principal():
        """
        Menu offering different actions to the user
        :return: number chosen by the user
        """
        print("\nQue souhaitez-vous faire?\n"
              "\t1. Créer un nouveau Tournoi\n"
              "\t2. Reprendre un Tournoi\n"
              "\t3. Avoir un rapport sur ...\n"
              "\t4. Quitter le programme\n"
              )
        while True:
            try:
                choix_principal = int(input("Votre choix: "))
                if choix_principal == 1:
                    print("\nCommençons ce nouveau Tournoi!\n")
                    return choix_principal
                elif choix_principal == 2:
                    print("\nReprenons un Tournoi où nous l'avons laissé.\n")
                    return choix_principal
                elif choix_principal == 3:
                    print("\nNous allons rechercher les informations.")
                    return choix_principal
                elif choix_principal == 4:
                    print("A bientôt!")
                    return choix_principal
                else:
                    raise ValueError
            except ValueError:
                print("\nVous n'avez pas rentré un choix valide, "
                      "veuillez recommencer.\n")

    @staticmethod
    def menu_reprendre_tournoi(liste_tournois):
        """
        Menu offering the various unfinished tournaments
        :param liste_tournois: list of tournaments
        :return: number chosen by the user
        """
        print("Veuillez sélectionner le Tournois non terminé "
              "de la liste suivante:")
        i = 1
        for tournoi in liste_tournois:
            print(f"\t{i}. {tournoi['nom']}")
            i += 1
        while True:
            try:
                choix = int(input("\nVotre choix: "))
                if choix not in range(1, i+1):
                    raise ValueError
                break
            except ValueError:
                print("Vous n'avez pas rentré un choix valide, "
                      "veuillez recommencer.")
        return choix

    @staticmethod
    def menu_rapport():
        """
        Menu displaying the various accessible reports
        :return: number chosen by the user
        """
        print("-------------------------\n"
              "Quel rapport souhaitez-vous?\n"
              "\t1. Liste des joueurs ayant participé à au moins un Tournoi\n"
              "\t2. Liste des joueurs d'un Tournoi en particulier\n"
              "\t3. Liste de tous les Tournois\n"
              "\t4. Liste de tous les tours d'un Tournoi\n"
              "\t5. Liste de tous les matchs d'un Tournoi\n"
              )
        while True:
            try:
                choix = int(input("Votre choix : "))
                if choix not in [1, 2, 3, 4, 5]:
                    raise ValueError
                break
            except ValueError:
                print("Vous n'avez pas saisi un nombre correct, "
                      "veuillez redonner votre choix.")
        return choix

    # Choix 1
    @staticmethod
    def afficher_all_participants(table_players, choix_ordre):
        """
        Method displaying all participants registered in the database
        :param table_players: tinydb table of players
        :param choix_ordre: type of sort 1. alphabetical 2. by ranking
        """
        print(f"Nombre total: {len(table_players)}")
        joueurs_tries = []
        for joueur in table_players:
            joueurs_tries.append([joueur['nom'],
                                  joueur['prenom'],
                                  joueur['classement']])
        if choix_ordre == 1:
            for joueur_trie in sorted(joueurs_tries):
                print(f"\t{joueur_trie[0]} {joueur_trie[1]}")
        if choix_ordre == 2:
            for joueur_trie in sorted(joueurs_tries,
                                      key=lambda x: x[2],
                                      reverse=True):
                print(f"\tClassement {joueur_trie[2]} "
                      f"{joueur_trie[0]} {joueur_trie[1]}")

    # Choice 1 et 2
    @staticmethod
    def choisir_ordre():
        """
        Used to define the display criterion:
        alphabetical or by classification
        :return: number chosen by the user
        """
        print("\nDans quel ordre souhaitez-vous afficher les joueurs?"
              "\n\t1. Alphabetique"
              "\n\t2. Classement\n")
        while True:
            try:
                choix = int(input("Votre choix : "))
                if choix not in [1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Vous n'avez pas saisi un nombre correct, "
                      "veuillez ressaisir votre choix.")
        return choix

    # Choice 2, 4 and 5
    @staticmethod
    def selection_tournoi(table_tournaments):
        """
        List of all registered tournaments and ask to select one
        :param table_tournaments: tinydb table of tournaments
        :return: number chosen by the user
        """
        print("Veuillez sélectionner un tournoi dans la liste suivante:")
        liste_id = []
        for tournoi in table_tournaments:
            print(f"\t{tournoi['id']}. {tournoi['nom']}")
            liste_id.append(tournoi['id'])
        while True:
            try:
                choix = int(input("\nVotre choix: "))
                if choix not in liste_id:
                    raise ValueError
                break
            except ValueError:
                print("Vous n'avez pas saisi un nombre correct, "
                      "veuillez ressaisir votre choix.")
        return choix

    # Choice 2
    @staticmethod
    def afficher_joueurs_tournoi(tournoi, choix_ordre):
        """
        List of players from a specified tournament
        :param tournoi: tournament instance
        :param choix_ordre: type of sort 1. alphabetical 2. by ranking
        """
        print(f"\nTournoi : {tournoi.nom}\n"
              "Liste des participants:")
        if choix_ordre == 1:
            for joueur in sorted(tournoi.joueurs, key=lambda x: x.nom):
                print(f"\t{joueur}")
        elif choix_ordre == 2:
            for joueur in sorted(tournoi.joueurs,
                                 key=lambda x: x.classement,
                                 reverse=True):
                print(f"\tClassement {joueur.classement} {joueur}")

    # Choice 3
    @staticmethod
    def afficher_tournois(liste_tournois):
        """
        List of all tournaments
        :param liste_tournois: list of all tournaments
        """
        print("Liste des tournois:")
        for tournoi in liste_tournois:
            print(f"\t{tournoi['nom']} ")

    # Choice 4
    @staticmethod
    def afficher_tours(tournoi):
        """
        List of rounds for a specific tournament
        :param tournoi: tournament instance
        """
        print("\nListe des tours du tournoi: \n"
              f"{tournoi}")
        for tour in tournoi.tours:
            print(f"\t{tour}")

    # Choice 5
    @staticmethod
    def afficher_matchs_tournoi(tournoi):
        """
        List of matches for a specific tournament
        :param tournoi: tournament instance
        """
        print(f"\nListe des matchs du tournoi: {tournoi}")
        for match in tournoi.matchs_tournoi:
            print(f"\t{match[0][0]}, Score: {match[0][1]} "
                  f"\tVS\t {match[1][0]}, Score: {match[1][1]}")

    @staticmethod
    def menu_tournoi(number, tour_en_cours=False):
        """
        Menu allowing:
        - the start and end of turns
        - the display of rankings
        - modification of rankings
        - the end of the tournament
        :param number: number of the round
        :param tour_en_cours: True if a round is in progress
        :return: number chosen by the user
        """
        print("-------------------------\n"
              "Que souhaitez-vous faire à présent?"
              )
        if not tour_en_cours:
            print(f"\t1. Lancer le Tour {number}")
        else:
            print(f"\t1. Fin du Tour {number}, inscrire les scores")
        print("\t2. Afficher le classement des joueurs en compétition\n"
              "\t3. Modifier le classement des joueurs en compétition\n"
              "\t4. Arrêter le tournoi\n"
              )
        while True:
            try:
                choix_tournoi = int(input("Votre choix: "))
                if choix_tournoi not in [1, 2, 3, 4]:
                    raise ValueError
                break
            except ValueError:
                print("Vous n'avez pas fais un choix valide, "
                      "veuillez redonner votre choix.")
        return choix_tournoi

    def choix_classement(self, liste_joueurs, nombre_joueurs):
        """
        List of tournament players and selection
        :param liste_joueurs: list of players
        :param nombre_joueurs: total number of players
        :return: number chosen by the user
        """
        print("De quel joueur souhaitez-vous modifier le classement?\n")
        for i in range(nombre_joueurs):
            print(f"{i + 1}. {liste_joueurs[i]}")
        choix = int(input("Votre choix : "))
        if choix not in range(nombre_joueurs + 1):
            print("Vous n'avez pas saisi un nombre valide.\n"
                  "Veuillez redéfinir votre choix.")
            self.choix_classement(liste_joueurs, nombre_joueurs)
        choix_joueur = liste_joueurs[choix - 1]
        return choix_joueur

    @staticmethod
    def nouveau_classement(joueur):
        """
        Allows to modify a player's ranking
        :param joueur: player instance
        :return: new ranking of the player
        """
        print(f"Le classement actuel de {joueur} est {joueur.classement}.\n"
              "Quel est son nouveau classement?\n")
        while True:
            try:
                classement = int(input("Classement : "))
                if classement < 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Vous n'avez pas saisi un nombre correct, "
                      "veuillez recommencer.")
        return classement

    @staticmethod
    def classement_joueur(joueurs):
        """
        Display of a player's ranking
        :param joueurs: player instance
        """
        for joueur in joueurs:
            print(f"Classement actuel de {joueur}: {joueur.classement}")

    @staticmethod
    def fin_tournoi():
        """ End of tournament message"""
        print("\n\tFin du tournoi !"
              "\nMerci aux participants.\n")
