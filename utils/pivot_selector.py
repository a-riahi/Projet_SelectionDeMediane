"""
Gestionnaire de sélection de pivots personnalisés pour Quickselect
"""
import random

class PivotSelector:
    """Gère la sélection de pivots personnalisés pour Quickselect"""
    
    def __init__(self, pivot_list=None):
        """
        Initialise le sélecteur de pivots
        
        Args:
            pivot_list: Liste de pivots à utiliser (un par niveau récursif)
        """
        self.pivot_list = pivot_list if pivot_list else []
        self.pivot_index = 0
    
    def reset(self):
        """Réinitialise l'index des pivots"""
        self.pivot_index = 0
    
    def select_pivot(self, current_arr, depth):
        """
        Sélectionne un pivot pour l'étape courante
        
        Args:
            current_arr: Tableau courant
            depth: Profondeur récursive
        
        Returns:
            Pivot sélectionné
        """
        if self.pivot_index < len(self.pivot_list):
            pivot = self.pivot_list[self.pivot_index]
            self.pivot_index += 1
            # Vérifier que le pivot est dans le tableau
            if pivot not in current_arr:
                # Si le pivot n'est pas dans le tableau, utiliser un pivot aléatoire
                return random.choice(current_arr)
            return pivot
        else:
            # Plus de pivots spécifiés, utiliser aléatoire
            return random.choice(current_arr)
    
    def create_selector_function(self):
        """
        Crée une fonction de sélection de pivot compatible avec le modèle
        
        Returns:
            Fonction de sélection de pivot
        """
        def selector(arr, depth):
            return self.select_pivot(arr, depth)
        return selector

