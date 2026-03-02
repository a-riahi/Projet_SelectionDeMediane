#!/usr/bin/env python3
"""
Fichier de test complet pour le projet SelectionMediane
Teste les algorithmes de sélection : Quickselect et Médiane Probabiliste
Utilise l'architecture MVC du projet
"""

import random
import sys
from models.model import SelectionModel
from controllers.controller import SelectionController
from utils.utils import DataGenerator, PerformanceTimer
from utils.pivot_selector import PivotSelector

class TestSuite:
    """Suite de tests complète pour valider le projet"""
    
    def __init__(self):
        self.model = SelectionModel()
        self.controller = SelectionController()
        self.data_generator = DataGenerator()
        self.timer = PerformanceTimer()
        self.stats = {
            'total_tests': 0,
            'quickselect_success': 0,
            'probabiliste_success': 0,
            'probabiliste_failures': 0,
            'errors': 0
        }
        
    def run_single_test(self, arr, k, test_name, pivot_selector=None):
        """
        Exécute un test unique et retourne les résultats
        
        Args:
            arr: Tableau à tester
            k: Position recherchée
            test_name: Nom du test
            pivot_selector: Sélecteur de pivot personnalisé (optionnel)
        """
        self.stats['total_tests'] += 1
        
        print(f"\n{'='*70}")
        print(f"TEST: {test_name}")
        print(f"{'='*70}")
        print(f"Taille: {len(arr)} | k: {k} | Médiane attendue: {sorted(arr)[k] if k < len(arr) else 'N/A'}")
        if len(arr) <= 20:
            print(f"Tableau: {arr}")
        else:
            print(f"Tableau (premiers 10): {arr[:10]}... (total: {len(arr)})")
        
        results = {}
        
        # Test Quickselect
        try:
            if pivot_selector:
                self.model.pivot_selector = pivot_selector.create_selector_function()
                pivot_selector.reset()
            else:
                self.model.pivot_selector = None
            
            self.model.reset_steps()
            result, elapsed = self.timer.measure_execution(
                self.model.quickselect, arr[:], k
            )
            
            expected = sorted(arr)[k]
            is_correct = (result == expected)
            
            results['quickselect'] = {
                'result': result,
                'expected': expected,
                'time': elapsed,
                'steps': self.model.steps,
                'success': True,
                'correct': is_correct
            }
            
            if is_correct:
                self.stats['quickselect_success'] += 1
            else:
                self.stats['errors'] += 1
                
        except Exception as e:
            results['quickselect'] = {
                'result': None,
                'time': 0,
                'steps': 0,
                'success': False,
                'error': str(e),
                'correct': False
            }
            self.stats['errors'] += 1
        
        # Test Médiane Probabiliste
        try:
            self.model.reset_steps()
            result, elapsed = self.timer.measure_execution(
                self.model.mediane_probabiliste, arr[:], k
            )
            
            expected = sorted(arr)[k]
            is_correct = (result == expected) if result != "ECHEC" else False
            
            results['probabiliste'] = {
                'result': result,
                'expected': expected,
                'time': elapsed,
                'steps': self.model.steps,
                'success': True,
                'correct': is_correct,
                'failed': (result == "ECHEC")
            }
            
            if result == "ECHEC":
                self.stats['probabiliste_failures'] += 1
            elif is_correct:
                self.stats['probabiliste_success'] += 1
            else:
                self.stats['errors'] += 1
                
        except Exception as e:
            results['probabiliste'] = {
                'result': None,
                'time': 0,
                'steps': 0,
                'success': False,
                'error': str(e),
                'correct': False,
                'failed': False
            }
            self.stats['errors'] += 1
        
        # Vérification par tri complet
        sorted_arr, _ = self.timer.measure_execution(sorted, arr)
        exact_result = sorted_arr[k]
        
        # Affichage des résultats
        print(f"\n{'RÉSULTATS':^70}")
        print("-" * 70)
        
        qs = results['quickselect']
        prob = results['probabiliste']
        
        qs_status = "✓" if qs.get('correct', False) else "✗"
        prob_status = "✓" if prob.get('correct', False) else ("ECHEC" if prob.get('failed', False) else "✗")
        
        print(f"Quickselect:     {qs_status} Résultat: {qs['result']:8} | "
              f"Temps: {qs['time']:.6f}s | Étapes: {qs['steps']:6}")
        print(f"Probabiliste:    {prob_status:6} Résultat: {str(prob['result']):8} | "
              f"Temps: {prob['time']:.6f}s | Étapes: {prob['steps']:6}")
        print(f"Résultat exact:  {exact_result:8} (vérification)")
        
        if not qs.get('correct', False) and qs.get('success', False):
            print(f"⚠️  ERREUR: Quickselect incorrect! (obtenu {qs['result']}, attendu {exact_result})")
        if prob.get('failed', False):
            print(f"ℹ️  INFO: Médiane Probabiliste a échoué (ECHEC)")
        elif not prob.get('correct', False) and prob.get('success', False):
            print(f"⚠️  ERREUR: Probabiliste incorrect! (obtenu {prob['result']}, attendu {exact_result})")
        
        return results
    
    def test_small_arrays(self):
        """Test avec de petits arrays"""
        print(f"\n{'='*80}")
        print("TESTS AVEC PETITS ARRAYS (1-20 éléments)")
        print(f"{'='*80}")
        
        test_cases = [
            ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 5, "Array de 10 éléments"),
            ([1, 2, 3, 4, 5], 2, "Array trié de 5 éléments"),
            ([5, 4, 3, 2, 1], 2, "Array inversé de 5 éléments"),
            ([42], 0, "Array d'un seul élément"),
            ([1, 1, 1, 1, 1], 2, "Array avec doublons"),
            ([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 5, "Array ordonné"),
        ]
        
        for arr, k, name in test_cases:
            self.run_single_test(arr, k, name)
    
    def test_medium_arrays(self):
        """Test avec des arrays moyens"""
        print(f"\n{'='*80}")
        print("TESTS AVEC ARRAYS MOYENS (50-500 éléments)")
        print(f"{'='*80}")
        
        sizes = [50, 100, 200, 500]
        
        for size in sizes:
            arr = self.data_generator.generate_random_array(size)
            k = self.data_generator.calculate_median_position(size)
            self.run_single_test(arr, k, f"Array aléatoire de {size} éléments")
    
    def test_large_arrays(self):
        """Test avec de grands arrays"""
        print(f"\n{'='*80}")
        print("TESTS AVEC GRANDS ARRAYS (1000-5000 éléments)")
        print(f"{'='*80}")
        
        sizes = [1000, 2000, 5000]
        
        for size in sizes:
            arr = self.data_generator.generate_random_array(size)
            k = self.data_generator.calculate_median_position(size)
            self.run_single_test(arr, k, f"Array aléatoire de {size} éléments")
    
    def test_edge_cases(self):
        """Test des cas limites"""
        print(f"\n{'='*80}")
        print("TESTS DES CAS LIMITES")
        print(f"{'='*80}")
        
        edge_cases = [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, "Premier élément (k=0)"),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9, "Dernier élément (k=9)"),
            ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 5, "Tous les éléments identiques"),
            ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 5, "Array décroissant"),
            ([1, 3, 5, 7, 9, 2, 4, 6, 8, 10], 5, "Array avec pattern alterné"),
        ]
        
        for arr, k, name in edge_cases:
            self.run_single_test(arr, k, name)
    
    def test_custom_pivots(self):
        """Test avec pivots personnalisés"""
        print(f"\n{'='*80}")
        print("TESTS AVEC PIVOTS PERSONNALISÉS")
        print(f"{'='*80}")
        
        arr = [10, 5, 8, 3, 1, 9, 2, 7, 4, 6]
        k = 5
        
        # Test avec pivots spécifiques
        pivots = [5, 3, 1]
        pivot_selector = PivotSelector(pivots)
        
        self.run_single_test(arr, k, "Array avec pivots personnalisés [5, 3, 1]", pivot_selector)
    
    def performance_comparison(self):
        """Comparaison de performance détaillée"""
        print(f"\n{'='*80}")
        print("COMPARAISON DE PERFORMANCE")
        print(f"{'='*80}")
        
        sizes = [100, 500, 1000, 2000]
        repetitions = 5
        
        print(f"\n{'Taille':<8} {'Quickselect':<20} {'Probabiliste':<20} {'Ratio':<10}")
        print(f"{'':8} {'Temps (s)':<10} {'Étapes':<9} {'Temps (s)':<10} {'Étapes':<9} {'QS/Prob':<10}")
        print("-" * 80)
        
        for size in sizes:
            qs_times, qs_steps = [], []
            prob_times, prob_steps = [], []
            prob_failures = 0
            
            for _ in range(repetitions):
                arr = self.data_generator.generate_random_array(size)
                k = self.data_generator.calculate_median_position(size)
                
                # Quickselect
                self.model.reset_steps()
                _, elapsed = self.timer.measure_execution(
                    self.model.quickselect, arr[:], k
                )
                qs_times.append(elapsed)
                qs_steps.append(self.model.steps)
                
                # Probabiliste
                self.model.reset_steps()
                result, elapsed = self.timer.measure_execution(
                    self.model.mediane_probabiliste, arr[:], k
                )
                prob_times.append(elapsed)
                prob_steps.append(self.model.steps)
                
                if result == "ECHEC":
                    prob_failures += 1
            
            # Moyennes
            qs_time_avg = sum(qs_times) / len(qs_times)
            qs_steps_avg = sum(qs_steps) / len(qs_steps)
            prob_time_avg = sum(prob_times) / len(prob_times)
            prob_steps_avg = sum(prob_steps) / len(prob_steps)
            
            ratio = qs_steps_avg / prob_steps_avg if prob_steps_avg > 0 else 0
            
            print(f"{size:<8} {qs_time_avg:<10.6f} {qs_steps_avg:<9.0f} {prob_time_avg:<10.6f} "
                  f"{prob_steps_avg:<9.0f} {ratio:<10.2f}")
            
            if prob_failures > 0:
                print(f"         ⚠️  {prob_failures}/{repetitions} échecs pour Probabiliste")
    
    def print_statistics(self):
        """Affiche les statistiques finales"""
        print(f"\n{'='*80}")
        print("STATISTIQUES FINALES")
        print(f"{'='*80}")
        
        total = self.stats['total_tests']
        qs_success_rate = (self.stats['quickselect_success'] / total * 100) if total > 0 else 0
        prob_success_rate = (self.stats['probabiliste_success'] / total * 100) if total > 0 else 0
        prob_failure_rate = (self.stats['probabiliste_failures'] / total * 100) if total > 0 else 0
        
        print(f"Total de tests: {total}")
        print(f"\nQuickselect:")
        print(f"  ✓ Succès: {self.stats['quickselect_success']}/{total} ({qs_success_rate:.1f}%)")
        print(f"\nMédiane Probabiliste:")
        print(f"  ✓ Succès: {self.stats['probabiliste_success']}/{total} ({prob_success_rate:.1f}%)")
        print(f"  ✗ Échecs (ECHEC): {self.stats['probabiliste_failures']}/{total} ({prob_failure_rate:.1f}%)")
        print(f"\nErreurs totales: {self.stats['errors']}")
        
        if self.stats['errors'] == 0:
            print("\n✅ Tous les tests sont passés avec succès!")
        else:
            print(f"\n⚠️  {self.stats['errors']} erreur(s) détectée(s)")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("\n" + "="*80)
        print("DÉMARRAGE DES TESTS - PROJET SELECTIONDEMEDIANE")
        print("="*80)
        
        try:
            self.test_small_arrays()
            self.test_medium_arrays()
            self.test_large_arrays()
            self.test_edge_cases()
            self.test_custom_pivots()
            self.performance_comparison()
            self.print_statistics()
            
            print(f"\n{'='*80}")
            print("TOUS LES TESTS TERMINÉS!")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ ERREUR LORS DES TESTS: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

def main():
    """Fonction principale pour exécuter les tests"""
    print("\n" + "="*80)
    print("SUITE DE TESTS - PROJET SELECTIONDEMEDIANE")
    print("="*80)
    print("Ce script teste tous les algorithmes et fonctionnalités du projet")
    print("="*80)
    
    # Initialisation du générateur aléatoire pour des résultats reproductibles
    random.seed(42)
    
    # Création et exécution des tests
    test_suite = TestSuite()
    test_suite.run_all_tests()
    
    print("\n" + "="*80)
    print("RÉSUMÉ")
    print("="*80)
    print("✓ Tests sur petits arrays: Terminés")
    print("✓ Tests sur arrays moyens: Terminés") 
    print("✓ Tests sur grands arrays: Terminés")
    print("✓ Tests des cas limites: Terminés")
    print("✓ Tests avec pivots personnalisés: Terminés")
    print("✓ Comparaison de performance: Terminée")
    print("\n💡 Pour voir l'interface graphique, exécutez: python main.py")
    print("="*80)

if __name__ == "__main__":
    main()
