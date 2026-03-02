#!/usr/bin/env python3
"""
Module de visualisation graphique pour comparer les algorithmes de sélection
Affiche des graphiques comparant Quickselect et Médiane Probabiliste
en termes de nombre de pas et de complexité asymptotique
"""

import matplotlib.pyplot as plt
import math
from controllers.controller import SelectionController
from utils.utils import DataGenerator


class GrapheComparaison:
    """
    Classe pour générer des graphiques de comparaison des algorithmes
    """
    
    def __init__(self):
        """Initialise le graphe avec le contrôleur"""
        self.controller = SelectionController()
        self.data_generator = DataGenerator()
    
    def generer_donnees(self, tailles, repetitions=5):
        """
        Génère les données de comparaison pour différentes tailles
        
        Args:
            tailles: Liste des tailles de tableaux à tester
            repetitions: Nombre de répétitions pour chaque taille (pour moyenne)
        
        Returns:
            Dictionnaire contenant les données pour chaque algorithme
        """
        quickselect_pas = []
        probabiliste_pas = []
        
        print("Génération des données de comparaison...")
        print(f"Tailles testées: {tailles}")
        print(f"Répétitions par taille: {repetitions}\n")
        
        for i, n in enumerate(tailles, 1):
            print(f"[{i}/{len(tailles)}] Test avec n={n}...", end=" ", flush=True)
            k = n // 2  # Position médiane
            
            # Accumulateurs pour les moyennes
            qs_pas_total = 0
            mom_pas_total = 0
            
            for rep in range(repetitions):
                # Générer un nouveau tableau pour chaque répétition
                arr = self.data_generator.generate_random_array(n)
                
                # Test Quickselect
                self.controller.model.reset_steps()
                self.controller.model.quickselect(arr[:], k)
                qs_pas_total += self.controller.model.steps
                
                # Test Médiane Probabiliste
                self.controller.model.reset_steps()
                result = self.controller.model.mediane_probabiliste(arr[:], k)
                mom_pas_total += self.controller.model.steps
                
                # Si échec, utiliser Quickselect comme fallback
                if result == "ECHEC":
                    self.controller.model.reset_steps()
                    self.controller.model.quickselect(arr[:], k)
                    mom_pas_total += self.controller.model.steps
            
            # Calculer les moyennes
            quickselect_pas.append(qs_pas_total / repetitions)
            probabiliste_pas.append(mom_pas_total / repetitions)
            
            print(f"✓ (QS: {int(quickselect_pas[-1])} pas, "
                  f"MOM: {int(probabiliste_pas[-1])} pas)")
        
        print("\n✓ Génération des données terminée!\n")
        
        return {
            'tailles': tailles,
            'quickselect_pas': quickselect_pas,
            'probabiliste_pas': probabiliste_pas
        }
    
    def tracer_graphiques(self, donnees):
        """
        Trace les graphiques de comparaison du nombre de pas et de la complexité
        
        Args:
            donnees: Dictionnaire contenant les données générées
        """
        tailles = donnees['tailles']
        qs_pas = donnees['quickselect_pas']
        mom_pas = donnees['probabiliste_pas']
        
        # Calculer les courbes théoriques pour référence
        # O(n) pour Quickselect et Médiane Probabiliste
        if tailles[0] > 0:
            facteur = qs_pas[0] / tailles[0]
        else:
            facteur = 1
        reference_lin = [n * facteur for n in tailles]
        
        # O(n log n) pour référence (tri complet)
        if tailles[0] > 1:
            facteur_nlogn = qs_pas[0] / (tailles[0] * math.log2(tailles[0]))
        else:
            facteur_nlogn = 1
        reference_nlogn = [n * math.log2(n) * facteur_nlogn if n > 1 else 0 for n in tailles]
        
        # Créer la figure avec 2 sous-graphiques
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Comparaison des Algorithmes : Nombre de Pas et Complexité',
                     fontsize=16, fontweight='bold')
        
        # ========== Graphique 1: Nombre de pas (linéaire) ==========
        ax1 = axes[0]
        ax1.plot(tailles, qs_pas, 'o-', linewidth=2.5, markersize=9, 
                label='Quickselect', color='#2E86AB', alpha=0.9)
        ax1.plot(tailles, mom_pas, 's-', linewidth=2.5, markersize=9, 
                label='Médiane Probabiliste', color='#A23B72', alpha=0.9)
        ax1.plot(tailles, reference_lin, '--', linewidth=2, 
                label='Référence O(n)', color='gray', alpha=0.7)
        ax1.set_xlabel('Taille du tableau (n)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Nombre de pas (comparaisons)', fontsize=12, fontweight='bold')
        ax1.set_title('Nombre de Pas - Échelle Linéaire', 
                     fontsize=13, fontweight='bold')
        ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_facecolor('#FAFAFA')
        
        # ========== Graphique 2: Complexité (log-log) ==========
        ax2 = axes[1]
        ax2.loglog(tailles, qs_pas, 'o-', linewidth=2.5, markersize=9, 
                  label='Quickselect', color='#2E86AB', alpha=0.9)
        ax2.loglog(tailles, mom_pas, 's-', linewidth=2.5, markersize=9, 
                  label='Médiane Probabiliste', color='#A23B72', alpha=0.9)
        ax2.loglog(tailles, reference_lin, '--', linewidth=2, 
                  label='Référence O(n)', color='gray', alpha=0.7)
        ax2.loglog(tailles, reference_nlogn, ':', linewidth=2, 
                  label='Référence O(n log n)', color='darkgray', alpha=0.7)
        ax2.set_xlabel('Taille du tableau (n)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Nombre de pas (comparaisons)', fontsize=12, fontweight='bold')
        ax2.set_title('Complexité Asymptotique - Échelle Log-Log', 
                     fontsize=13, fontweight='bold')
        ax2.legend(loc='upper left', fontsize=11, framealpha=0.9)
        ax2.grid(True, alpha=0.3, linestyle='--', which='both')
        ax2.set_facecolor('#FAFAFA')
        
        # Ajuster l'espacement
        plt.tight_layout()
        
        # Afficher la fenêtre
        plt.show()
    
    def comparer(self, tailles=None, repetitions=5):
        """
        Méthode principale pour générer et afficher les graphiques
        
        Args:
            tailles: Liste des tailles à tester (par défaut: [50, 100, 200, 500, 1000, 2000])
            repetitions: Nombre de répétitions pour chaque taille
        """
        if tailles is None:
            tailles = [50, 100, 200, 500, 1000, 2000]
        
        # Générer les données
        donnees = self.generer_donnees(tailles, repetitions)
        
        # Tracer les graphiques
        self.tracer_graphiques(donnees)


def main():
    """Point d'entrée principal pour exécuter les graphiques"""
    print("=" * 80)
    print("  GÉNÉRATION DE GRAPHIQUES DE COMPARAISON DES ALGORITHMES".center(80))
    print("=" * 80)
    print()
    
    # Créer l'instance de graphe
    graphe = GrapheComparaison()
    
    # Définir les tailles à tester
    # Vous pouvez modifier ces valeurs selon vos besoins
    tailles = [50, 100, 200, 500, 1000, 2000]
    repetitions = 5  # Nombre de répétitions pour calculer la moyenne
    
    print(f"Configuration:")
    print(f"  - Tailles testées: {tailles}")
    print(f"  - Répétitions par taille: {repetitions}")
    print(f"  - Total d'exécutions: {len(tailles) * repetitions * 2} algorithmes")
    print(f"  - Métriques: Nombre de pas et complexité")
    print()
    
    # Générer et afficher les graphiques
    graphe.comparer(tailles, repetitions)
    
    print("\n" + "=" * 80)
    print("Graphiques générés avec succès!")
    print("=" * 80)


if __name__ == "__main__":
    main()

