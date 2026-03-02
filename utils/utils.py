"""
Utilitaires pour la génération de données et opérations communes
"""
import random
import time

class DataGenerator:
    """Générateur de données pour les algorithmes"""
    
    @staticmethod
    def generate_random_array(size, min_val=1, max_multiplier=10):
        """
        Génère un tableau aléatoire de taille donnée
        
        Args:
            size: Taille du tableau
            min_val: Valeur minimale
            max_multiplier: Multiplicateur pour la valeur maximale (max = size * max_multiplier)
        
        Returns:
            Liste d'entiers uniques
        """
        if size <= 0:
            return []
        max_val = size * max_multiplier
        return random.sample(range(min_val, max_val), size)
    
    @staticmethod
    def parse_array(array_str):
        """
        Parse une chaîne de caractères en tableau d'entiers
        
        Args:
            array_str: Chaîne au format "1,2,3" ou "1 2 3"
        
        Returns:
            Liste d'entiers
        """
        if not array_str or not array_str.strip():
            return []
        # Supprimer les virgules et séparer par espaces
        array_str = array_str.replace(',', ' ')
        return [int(x.strip()) for x in array_str.split() if x.strip()]
    
    @staticmethod
    def parse_pivots(pivot_str):
        """
        Parse une chaîne de pivots en liste d'entiers
        
        Args:
            pivot_str: Chaîne au format "pivot1,pivot2,..."
        
        Returns:
            Liste d'entiers
        """
        if not pivot_str or not pivot_str.strip():
            return []
        pivot_str = pivot_str.replace(',', ' ')
        return [int(x.strip()) for x in pivot_str.split() if x.strip()]
    
    @staticmethod
    def calculate_median_position(size):
        """Calcule la position de la médiane (k)"""
        return size // 2
    
    @staticmethod
    def verify_result(arr, k, result):
        """
        Vérifie si le résultat est correct en comparant avec le tri complet
        
        Args:
            arr: Tableau original
            k: Position recherchée
            result: Résultat obtenu
        
        Returns:
            Tuple (is_correct, expected_value)
        """
        sorted_arr = sorted(arr)
        expected = sorted_arr[k] if k < len(sorted_arr) else None
        is_correct = (result == expected) if expected is not None else False
        return is_correct, expected


class PerformanceTimer:
    """Utilitaire pour mesurer les performances"""
    
    @staticmethod
    def measure_execution(func, *args, **kwargs):
        """
        Mesure le temps d'exécution d'une fonction
        
        Args:
            func: Fonction à exécuter
            *args, **kwargs: Arguments de la fonction
        
        Returns:
            Tuple (result, elapsed_time)
        """
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end - start

