import random
import math

class SelectionModel:
    def __init__(self):
        self.steps = 0  # compteur d'étapes
        self.detailed_steps = []  # liste des étapes détaillées avec comparaisons
        self.pivot_selector = None  # fonction pour choisir le pivot (None = aléatoire)

    def reset_steps(self):
        self.steps = 0
        self.detailed_steps = []
    
    def add_step(self, description, comparisons=0, arrays=None):
        """Ajoute une étape détaillée avec le nombre de comparaisons et les tableaux"""
        step_data = {
            'description': description,
            'comparisons': comparisons,
            'cumulative': self.steps + comparisons
        }
        if arrays:
            step_data['arrays'] = arrays
        self.detailed_steps.append(step_data)
        self.steps += comparisons

    # --------------------
    # Quickselect
    # --------------------
    def quickselect(self, arr, k, depth=0):
        # Afficher le tableau au début de chaque appel récursif
        self.add_step(f"Appel récursif (profondeur {depth}) - Tableau de taille {len(arr)}, k={k}", 
                     1, arrays={'current': arr.copy()})
        
        if len(arr) == 1:
            self.add_step(f"Cas de base: tableau de taille 1, retour {arr[0]}", 
                        0, arrays={'current': arr.copy(), 'result': arr[0]})
            return arr[0]

        # Utiliser la fonction de sélection de pivot si fournie, sinon aléatoire
        if self.pivot_selector and callable(self.pivot_selector):
            pivot = self.pivot_selector(arr, depth)
        else:
            pivot = random.choice(arr)
        self.add_step(f"Sélection du pivot: {pivot}", 
                    0, arrays={'current': arr.copy(), 'pivot': pivot})
        
        ppp, pgp, pivots = [], [], []
        comparisons = 0
        
        for el in arr:
            comparisons += 1
            if el < pivot:
                ppp.append(el)
            elif el > pivot:
                pgp.append(el)
            else:
                pivots.append(el)
        
        self.add_step(f"Partition: {len(ppp)} < pivot, {len(pivots)} = pivot, {len(pgp)} > pivot", 
                     comparisons, arrays={'original': arr.copy(), 'pivot': pivot, 'left': ppp.copy(), 
                                         'equal': pivots.copy(), 'right': pgp.copy()})
        
        if k < len(ppp):
            self.add_step(f"k={k} < {len(ppp)}, recherche dans la partie gauche", 
                        1, arrays={'next_array': ppp.copy(), 'direction': 'gauche'})
            return self.quickselect(ppp, k, depth + 1)
        elif k < len(ppp) + len(pivots):
            self.add_step(f"k={k} dans la plage des pivots, résultat: {pivots[0]}", 
                        1, arrays={'result': pivots[0], 'pivots': pivots.copy()})
            return pivots[0]
        else:
            self.add_step(f"k={k} >= {len(ppp) + len(pivots)}, recherche dans la partie droite", 
                        1, arrays={'next_array': pgp.copy(), 'direction': 'droite'})
            return self.quickselect(pgp, k - len(ppp) - len(pivots), depth + 1)


    # --------------------
    # Médiane Probabiliste
    # --------------------
    def mediane_probabiliste(self, arr, k):
        """
        Algorithme probabiliste pour le calcul de la médiane
        Entrées: Un ensemble arr constitué de n éléments et k (position recherchée)
        Sorties: le k-ième élément de arr ou ECHEC
        """
        n = len(arr)
        self.add_step(f"Début - Tableau de taille n={n}, k={k}", 
                    1, arrays={'original': arr.copy()})
        
        # Étape 1: Soit R un ensemble de n^(3/4) éléments de arr tirés aléatoirement avec remise
        taille_R = int(n ** (3/4))
        self.add_step(f"Étape 1: Échantillonnage de R (taille {taille_R} = n^(3/4))", taille_R,
                     arrays={'original': arr.copy()})
        R = [random.choice(arr) for _ in range(taille_R)]
        self.detailed_steps[-1]['arrays']['R'] = R.copy()
        
        # Étape 2: Trier R et trouver a et b
        comparisons_tri_R = int(taille_R * math.log2(taille_R)) if taille_R > 1 else taille_R
        self.add_step(f"Étape 2: Tri de R ({taille_R} éléments)", comparisons_tri_R,
                     arrays={'R': R.copy()})
        R_trie = sorted(R)
        self.detailed_steps[-1]['arrays']['R_sorted'] = R_trie.copy()
        
        rang_R = taille_R // 2
        delta = int(math.sqrt(n))
        
        # rang_R(a) = max(1, ⌊|R|/2⌋ - √n)
        rang_a_R = max(1, rang_R - delta)
        # rang_R(b) = min(|R|, ⌊|R|/2⌋ + √n)
        rang_b_R = min(taille_R, rang_R + delta)
        
        a = R_trie[rang_a_R - 1]  # -1 pour l'indexation à 0
        b = R_trie[rang_b_R - 1]
        self.add_step(f"Étape 2: Calcul de a={a} et b={b} (delta=sqrt(n)={delta})", 0)
        
        # Étape 3: Parcourir arr pour calculer rang_arr(a), rang_arr(b), P = {x ∈ arr | a ≤ x < b}, Card(P)
        comparisons_parcours = 0
        rang_arr_a = 0
        rang_arr_b = 0
        P = []
        
        for x in arr:
            comparisons_parcours += 2  # deux comparaisons: x < a et x < b
            if x < a:
                rang_arr_a += 1
                rang_arr_b += 1
            elif x < b:  # a ≤ x < b
                rang_arr_b += 1
                P.append(x)
        
        card_P = len(P)
        self.add_step(f"Étape 3: Parcours de arr - rang(a)={rang_arr_a}, rang(b)={rang_arr_b}, |P|={card_P}", 
                     comparisons_parcours, arrays={'original': arr.copy(), 'a': a, 'b': b, 'P': P.copy()})
        
        # Étape 4: Si rang_arr(a) > k retourner ECHEC
        self.add_step(f"Étape 4: Vérification rang(a)={rang_arr_a} > k={k}?", 1)
        if rang_arr_a > k:
            self.add_step("ÉCHEC: rang(a) > k", 0)
            return "ECHEC"
        
        # Étape 5: Si rang_arr(b) < k retourner ECHEC
        self.add_step(f"Étape 5: Vérification rang(b)={rang_arr_b} < k={k}?", 1)
        if rang_arr_b < k:
            self.add_step("ÉCHEC: rang(b) < k", 0)
            return "ECHEC"
        
        # Étape 6: Si Card(P) > 4n^(3/4) retourner ECHEC
        limite_P = int(4 * (n ** (3/4)))
        self.add_step(f"Étape 6: Vérification |P|={card_P} > 4n^(3/4)={limite_P}?", 1)
        if card_P > limite_P:
            self.add_step("ÉCHEC: |P| trop grand", 0)
            return "ECHEC"
        
        # Étape 7: Trier P
        comparisons_tri_P = int(card_P * math.log2(card_P)) if card_P > 1 else card_P
        self.add_step(f"Étape 7: Tri de P ({card_P} éléments)", comparisons_tri_P,
                     arrays={'P': P.copy()})
        P_trie = sorted(P)
        self.detailed_steps[-1]['arrays']['P_sorted'] = P_trie.copy()
        
        # Étape 8: Retourner c tel que rang_P(c) = k - rang_arr(a) + 1
        rang_cible_P = k - rang_arr_a + 1
        self.add_step(f"Étape 8: Calcul rang_cible_P = k - rang(a) + 1 = {rang_cible_P}", 1)
        
        if rang_cible_P < 1 or rang_cible_P > len(P_trie):
            self.add_step("ÉCHEC: rang_cible_P hors limites", 0)
            return "ECHEC"
        
        c = P_trie[rang_cible_P - 1]  # -1 pour l'indexation à 0
        self.add_step(f"SUCCÈS: Résultat c={c}", 0)
        
        return c
