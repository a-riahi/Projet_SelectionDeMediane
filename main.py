import sys
import io

# Configuration de l'encodage pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from controllers.controller import SelectionController

if __name__ == "__main__":
    controller = SelectionController()

    # Démonstrateur graphique avec affichage des tableaux et opérations
    # L'utilisateur peut choisir le tableau, sa taille et les pivots via l'interface
    controller.demonstrate_graphical()  # Lance l'interface de configuration
    
    # Démonstrateur console (op1)
    # print("="*100)
    # print("  DÉMONSTRATEUR DES ÉTAPES DE COMPARAISON DES MÉTHODES".center(100))
    # print("="*100)
    # controller.demonstrate_steps(n=100)

    # Comparaison graphique (op2)
    # tailles = [100, 500, 1000, 2000, 4000, 8000]
    # controller.compare_growth(tailles, repetitions=7)