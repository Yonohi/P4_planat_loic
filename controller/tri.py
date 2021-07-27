from vue.vue import Vue


class Tri:
    """ Class bringing together the different possible sorts """
    def __init__(self):
        self.dict_possiblity = {}

    @staticmethod
    def tri_classement(liste_joueurs, nombre_joueurs):
        """
        First sorting of players
        - We separate into two halves according to the classification
        - The best of the first half is paired with the best of the second
        and so on
        :param liste_joueurs: list of players
        :param nombre_joueurs: total number of players
        :return: list of pairs sorted by ranking
        """
        joueurs_tries = sorted(liste_joueurs,
                               key=lambda joueur: joueur.classement,
                               reverse=True)
        moitie_sup = joueurs_tries[int(nombre_joueurs / 2):]
        moitie_inf = joueurs_tries[0:int(nombre_joueurs / 2)]
        # List comprehension for the list of tuples
        binomes_classement = [(moitie_inf[i], moitie_sup[i])
                              for i in range(int(nombre_joueurs / 2))]
        return binomes_classement

    def tri_points(self, tournoi, liste_joueurs, nombre_joueurs):
        """
        Sorting of our players by points then by ranking and by pairs not met
        :param tournoi: tournament instance
        :param liste_joueurs: list of players
        :param nombre_joueurs: total number of players
        :return: sorted list of pairs
        """
        joueurs_tries = sorted(liste_joueurs,
                               key=lambda joueur: (joueur.points,
                                                   joueur.classement),
                               reverse=True)
        # We get the list of meetings
        liste_rencontres = [(x[0][0], x[1][0]) for x in tournoi.matchs_tournoi]
        binomes_points = []
        # We create our list of tuples (pairs) from our sorted list
        for i in range(0, int(nombre_joueurs), 2):
            a = joueurs_tries[i]
            b = joueurs_tries[i+1]
            binomes_points.append((a, b))
        # Checking pairs by studying the list of tournament matches
        binomes_existants = self.verifier_binomes(binomes_points,
                                                  liste_rencontres)
        # If one or more existing pair(s) detected
        if binomes_existants:
            new_binomes_points = self.tri_si_rencontre(joueurs_tries,
                                                       liste_rencontres,
                                                       nombre_joueurs)
            return new_binomes_points
        # If the competitors have never met
        else:
            return binomes_points

    @staticmethod
    def verifier_binomes(binomes_points, liste_rencontres):
        """
        Method checking if pairs are in a meeting list
        :param binomes_points: list of pairs sorted by score
        :param liste_rencontres: list of pairs already met
        :return: boolean, True if a pairs has already met
        """
        for binome in binomes_points:
            if binome in liste_rencontres \
                    or (binome[1], binome[0]) in liste_rencontres:
                return True
            else:
                return False

    def tri_si_rencontre(self, joueurs_tries, liste_rencontres, nb_joueurs):
        """
        Sorting if a pair is in a meeting list
        :param joueurs_tries: list of players sorted by score and rank
        :param liste_rencontres: list of pairs already met
        :param nb_joueurs: total number of players
        :return: sorted list of pairs
        """
        # We recover the possibilities
        for x in joueurs_tries:
            liste_dict = []
            for y in joueurs_tries:
                if x == y:
                    continue
                if (x, y) in liste_rencontres or (y, x) in liste_rencontres:
                    continue
                else:
                    liste_dict.append(y)
            self.dict_possiblity[x] = liste_dict
        copy_joueurs = list(joueurs_tries)
        liste_finale = []
        nb_tour = 0
        error = False
        while joueurs_tries:
            x = joueurs_tries[0]
            for y in joueurs_tries:
                if nb_tour > nb_joueurs**2:
                    print("Il y a une erreur dans l'algorithme.")
                    error = True
                    break
                if x == y:
                    continue
                if (x, y) in liste_rencontres or (y, x) in liste_rencontres:
                    nb_tour += 1
                    continue
                else:
                    i = 0
                    # we are looking for a unique possibility
                    for key in list(self.dict_possiblity):
                        if len(self.dict_possiblity[key]) == 1:
                            valeur = self.dict_possiblity[key][0]
                            liste_finale.append((key, valeur))
                            liste_rencontres.append((key, valeur))
                            joueurs_tries.remove(key)
                            joueurs_tries.remove(valeur)
                            self.sup_dicti(valeur, key)
                            i += 1
                            break
                    if i > 0:
                        break
                    # we remove both of the possibilities
                    self.sup_dicti(x, y)
                    liste_finale.append((x, y))
                    liste_rencontres.append((x, y))
                    joueurs_tries.remove(y)
                    joueurs_tries.remove(x)
                    break
            if error:
                liste_finale = Vue().demander_binomes(copy_joueurs,
                                                      nb_joueurs)
                return liste_finale
        return liste_finale

    def sup_dicti(self, x, y):
        """
        Removes the x and y values from the dictionary of possibilities
        :param x: player instance
        :param y: player instance
        """
        for key in self.dict_possiblity:
            if x in self.dict_possiblity[key]:
                self.dict_possiblity[key].remove(x)
            if y in self.dict_possiblity[key]:
                self.dict_possiblity[key].remove(y)
        del self.dict_possiblity[y]
        del self.dict_possiblity[x]
