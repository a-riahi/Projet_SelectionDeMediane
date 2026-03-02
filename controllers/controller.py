import matplotlib.pyplot as plt
from models.model import SelectionModel
from views.view import SelectionView
from views.graphical_view import GraphicalView
from utils.utils import DataGenerator, PerformanceTimer
from utils.pivot_selector import PivotSelector

class SelectionController:
    """
    Contrôleur MVC pour coordonner le modèle et les vues
    Ne contient que la logique de coordination, pas de logique métier
    """
    def __init__(self):
        self.model = SelectionModel()
        self.view = SelectionView()
        self.graphical_view = None
        self.data_generator = DataGenerator()
        self.timer = PerformanceTimer()

    def run_demo(self, n=10001):
        """Démonstration simple avec affichage console"""
        # Génération des données (via utils)
        arr = self.data_generator.generate_random_array(n)
        k = self.data_generator.calculate_median_position(n)

        # Exécution Quickselect
        self.model.reset_steps()
        result, elapsed = self.timer.measure_execution(
            self.model.quickselect, arr[:], k
        )
        self.view.show_result("Quickselect", result, elapsed, self.model.steps)

        # Vérification par tri complet
        exact, _ = self.timer.measure_execution(sorted, arr)
        exact = exact[k]
        self.view.show_result("Tri complet (sorted)", exact, 0, n * (n.bit_length()))
        self.view.show_verification(exact)

    def demonstrate_steps(self, n=100):
        """
        Démonstrateur qui affiche les étapes de comparaison des méthodes (console)
        """
        # Génération des données
        arr = self.data_generator.generate_random_array(n)
        k = self.data_generator.calculate_median_position(n)
        
        print(f"\n{'='*100}")
        print(f"  DÉMONSTRATION DES ÉTAPES DE COMPARAISON".center(100))
        print(f"{'='*100}")
        print(f"Taille du tableau: {n} | Position recherchée (k): {k}")
        print(f"{'='*100}\n")
        
        # Exécution Quickselect
        qs_result = self._execute_quickselect(arr, k)
        self.view.show_detailed_steps("Quickselect", 
                                     qs_result['steps'], qs_result['total_steps'],
                                     qs_result['result'], qs_result['time'])
        
        # Exécution Médiane Probabiliste
        mom_result = self._execute_mediane_probabiliste(arr, k)
        self.view.show_detailed_steps("Médiane Probabiliste",
                                     mom_result['steps'], mom_result['total_steps'],
                                     mom_result['result'], mom_result['time'])
        
        # Comparaison
        self.view.show_comparison(
            "Quickselect", qs_result['total_steps'], qs_result['result'], qs_result['time'],
            "Médiane Probabiliste", mom_result['total_steps'], mom_result['result'], mom_result['time']
        )
        
        # Vérification
        is_correct_qs, expected = self.data_generator.verify_result(arr, k, qs_result['result'])
        is_correct_mom, _ = self.data_generator.verify_result(arr, k, mom_result['result'])
        
        print(f"Vérification: Résultat attendu = {expected}")
        print(f"{'✓' if is_correct_qs else '✗'} Quickselect: {'CORRECT' if is_correct_qs else 'ERREUR'}")
        if mom_result['result'] == "ECHEC":
            print("✗ Médiane Probabiliste: ÉCHEC")
        else:
            print(f"{'✓' if is_correct_mom else '✗'} Médiane Probabiliste: {'CORRECT' if is_correct_mom else 'ERREUR'}")
        print()
    
    def _execute_quickselect(self, arr, k, pivot_selector=None):
        """Exécute Quickselect et retourne les résultats"""
        if pivot_selector:
            self.model.pivot_selector = pivot_selector.create_selector_function()
            pivot_selector.reset()
        else:
            self.model.pivot_selector = None
        
        self.model.reset_steps()
        result, elapsed = self.timer.measure_execution(
            self.model.quickselect, arr[:], k
        )
        return {
            'result': result,
            'time': elapsed,
            'total_steps': self.model.steps,
            'steps': self.model.detailed_steps.copy()
        }
    
    def _execute_mediane_probabiliste(self, arr, k):
        """Exécute la médiane probabiliste avec fallback si nécessaire"""
        self.model.reset_steps()
        result, elapsed = self.timer.measure_execution(
            self.model.mediane_probabiliste, arr[:], k
        )
        steps = self.model.detailed_steps.copy()
        total_steps = self.model.steps
        
        # Fallback si échec
        if result == "ECHEC":
            self.model.reset_steps()
            result, _ = self.timer.measure_execution(
                self.model.quickselect, arr[:], k
            )
            total_steps += self.model.steps
            steps.append({
                'description': "Fallback: Utilisation de Quickselect après échec",
                'comparisons': self.model.steps,
                'cumulative': total_steps
            })
        
        return {
            'result': result,
            'time': elapsed,
            'total_steps': total_steps,
            'steps': steps
        }
    
    def demonstrate_graphical(self, n=50, arr=None, pivots=None, k=None):
        """
        Démonstrateur graphique qui affiche les étapes dans une fenêtre
        """
        import tkinter as tk
        from tkinter import ttk
        
        # Créer la vue graphique
        self.graphical_view = GraphicalView()
        
        # Variables pour stocker les résultats
        self._graphical_results = {
            'qs': None,
            'mom': None,
            'exact': None
        }
        
        def run_demo(size, custom_arr, custom_pivots, custom_k):
            """Fonction appelée quand l'utilisateur lance la démonstration"""
            # Génération/préparation des données (via utils)
            if custom_arr is not None:
                arr = custom_arr
            else:
                arr = self.data_generator.generate_random_array(size)
            
            if custom_k is not None:
                k = custom_k
            else:
                k = self.data_generator.calculate_median_position(len(arr))
            
            # Configuration des pivots
            pivot_selector = None
            if custom_pivots:
                pivot_selector = PivotSelector(custom_pivots)
            
            # Afficher les informations dans le terminal
            print("\n" + "="*80)
            print("  EXÉCUTION DES ALGORITHMES".center(80))
            print("="*80)
            print(f"Taille du tableau: {len(arr)} | Position k: {k}")
            if custom_pivots:
                print(f"Pivots personnalisés: {custom_pivots}")
            if len(arr) <= 30:
                print(f"Tableau: {arr}")
            else:
                print(f"Tableau (premiers 20): {arr[:20]}... (total: {len(arr)})")
            print("="*80)
            
            # Exécution des algorithmes (via méthodes privées)
            qs_result = self._execute_quickselect(arr, k, pivot_selector)
            mom_result = self._execute_mediane_probabiliste(arr, k)
            
            # Vérification
            is_correct, expected = self.data_generator.verify_result(arr, k, qs_result['result'])
            
            # Afficher les résultats dans le terminal
            print("\n" + "-"*80)
            print("  RÉSULTATS DANS LE TERMINAL".center(80))
            print("-"*80)
            
            # Afficher Quickselect
            self.view.show_result("Quickselect", qs_result['result'], 
                                qs_result['time'], qs_result['total_steps'])
            self.view.show_detailed_steps("Quickselect", qs_result['steps'], 
                                        qs_result['total_steps'], 
                                        qs_result['result'], qs_result['time'])
            
            # Afficher Médiane Probabiliste
            self.view.show_result("Médiane Probabiliste", mom_result['result'], 
                                mom_result['time'], mom_result['total_steps'])
            self.view.show_detailed_steps("Médiane Probabiliste", mom_result['steps'], 
                                        mom_result['total_steps'], 
                                        mom_result['result'], mom_result['time'])
            
            # Comparaison
            self.view.show_comparison(
                "Quickselect", qs_result['total_steps'], qs_result['result'], qs_result['time'],
                "Médiane Probabiliste", mom_result['total_steps'], mom_result['result'], mom_result['time']
            )
            
            # Vérification finale
            print("\n" + "-"*80)
            print("  VÉRIFICATION".center(80))
            print("-"*80)
            print(f"Résultat attendu (tri complet): {expected}")
            is_correct_qs = (qs_result['result'] == expected)
            is_correct_mom = (mom_result['result'] == expected) if mom_result['result'] != "ECHEC" else False
            
            print(f"Quickselect: {'✓ CORRECT' if is_correct_qs else '✗ ERREUR'}")
            if mom_result['result'] == "ECHEC":
                print(f"Médiane Probabiliste: ✗ ÉCHEC (fallback utilisé)")
            else:
                print(f"Médiane Probabiliste: {'✓ CORRECT' if is_correct_mom else '✗ ERREUR'}")
            
            print("\n" + "="*80)
            print("  Interface graphique disponible - Naviguez dans les étapes pour voir les détails".center(80))
            print("="*80 + "\n")
            
            # Stocker les résultats
            self._graphical_results['qs'] = qs_result
            self._graphical_results['mom'] = mom_result
            self._graphical_results['exact'] = expected
            
            # Mettre à jour l'interface
            update_menu()
            
            # Charger Quickselect par défaut
            self.graphical_view.load_algorithm(
                "Quickselect", 
                qs_result['steps'], 
                qs_result['result'], 
                qs_result['total_steps'], 
                qs_result['time']
            )
        
        def update_menu():
            """Met à jour le menu avec les résultats"""
            import tkinter as tk
            from tkinter import ttk
            
            # Effacer le menu précédent
            for widget in self.graphical_view.menu_frame.winfo_children():
                widget.destroy()
            
            if self._graphical_results['qs'] is None:
                return
            
            qs = self._graphical_results['qs']
            mom = self._graphical_results['mom']
            exact = self._graphical_results['exact']
            
            ttk.Label(self.graphical_view.menu_frame, text="Sélectionner l'algorithme:", 
                     font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
            
            def load_quickselect():
                self.graphical_view.load_algorithm(
                    "Quickselect", qs['steps'], qs['result'], 
                    qs['total_steps'], qs['time']
                )
            
            def load_mom():
                self.graphical_view.load_algorithm(
                    "Médiane Probabiliste", mom['steps'], mom['result'], 
                    mom['total_steps'], mom['time']
                )
            
            def show_comparison():
                self.graphical_view.show_comparison(
                    "Quickselect", qs['total_steps'], qs['result'], qs['time'],
                    "Médiane Probabiliste", mom['total_steps'], mom['result'], mom['time']
                )
            
            ttk.Button(self.graphical_view.menu_frame, text="Quickselect", 
                      command=load_quickselect).pack(side=tk.LEFT, padx=5)
            ttk.Button(self.graphical_view.menu_frame, text="Médiane Probabiliste", 
                      command=load_mom).pack(side=tk.LEFT, padx=5)
            ttk.Button(self.graphical_view.menu_frame, text="Comparaison", 
                      command=show_comparison).pack(side=tk.LEFT, padx=5)
            
            # Afficher la vérification
            is_correct_qs = (qs['result'] == exact)
            is_correct_mom = (mom['result'] == exact) if mom['result'] != "ECHEC" else False
            
            verification_text = f"Résultat attendu: {exact} | "
            verification_text += f"Quickselect: {'✓' if is_correct_qs else '✗'} | "
            if mom['result'] == "ECHEC":
                verification_text += "Médiane Probabiliste: ✗ (ÉCHEC)"
            else:
                verification_text += f"Médiane Probabiliste: {'✓' if is_correct_mom else '✗'}"
            
            ttk.Label(self.graphical_view.menu_frame, text=verification_text, 
                     font=('Arial', 9)).pack(side=tk.LEFT, padx=10)
        
        # Configurer l'interface de configuration
        self.graphical_view.setup_config_ui(run_demo)
        
        # Si des paramètres sont fournis, lancer automatiquement
        if arr is not None or (n is not None and n > 0):
            if arr is None:
                arr = self.data_generator.generate_random_array(n)
            if k is None:
                k = self.data_generator.calculate_median_position(len(arr))
            run_demo(len(arr), arr, pivots, k)
        
        # Lancer l'interface
        self.graphical_view.run()

    def compare_growth(self, sizes, repetitions=5):
        quick_steps, mom_steps, sort_steps = [], [], []
        quick_times, mom_times = [], []

        for n in sizes:
            k = n // 2

            # Accumulate over repetitions for averaging
            qs_steps_total = 0
            mom_steps_total = 0
            qs_time_total = 0.0
            mom_time_total = 0.0

            for _ in range(repetitions):
                arr = self.data_generator.generate_random_array(n)

                # Quickselect
                self.model.reset_steps()
                _, elapsed = self.timer.measure_execution(
                    self.model.quickselect, arr[:], k
                )
                qs_time_total += elapsed
                qs_steps_total += self.model.steps

                # Médiane Probabiliste
                self.model.reset_steps()
                result, elapsed = self.timer.measure_execution(
                    self.model.mediane_probabiliste, arr[:], k
                )
                mom_time_total += elapsed
                mom_steps_total += self.model.steps
                
                # Si l'algorithme probabiliste échoue, on utilise quickselect comme fallback
                if result == "ECHEC":
                    self.model.reset_steps()
                    self.model.quickselect(arr[:], k)
                    mom_steps_total += self.model.steps

            # Averages
            quick_steps.append(qs_steps_total / repetitions)
            mom_steps.append(mom_steps_total / repetitions)
            quick_times.append(qs_time_total / repetitions)
            mom_times.append(mom_time_total / repetitions)

            # Tri complet (approx n log n comparaisons) comme référence théorique
            sort_steps.append(n * (n.bit_length()))

        # -----------------
        # Tracé graphique (2 sous-graphiques : étapes et temps)
        # -----------------
        fig, axes = plt.subplots(1, 2, figsize=(12,6), facecolor="black")

        # Left subplot: Steps
        ax_steps = axes[0]
        ax_steps.set_facecolor("black")
        ax_steps.plot(sizes, quick_steps, marker="o", label="Quickselect (randomisé)")
        ax_steps.plot(sizes, mom_steps, marker="s", label="Médiane Probabiliste")
        ax_steps.plot(sizes, sort_steps, marker="^", linestyle="--", label="Tri complet (référence)")
        ax_steps.set_xlabel("Taille n", color="white")
        ax_steps.set_ylabel("Nombre d'étapes (moyenne)", color="white")
        ax_steps.set_title("Complexité en étapes", color="white")
        ax_steps.tick_params(colors="white")
        for spine in ax_steps.spines.values():
            spine.set_color("white")
        leg1 = ax_steps.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
        leg1.get_frame().set_facecolor("black")
        leg1.get_frame().set_edgecolor("white")
        for text in leg1.get_texts():
            text.set_color("white")
        ax_steps.grid(True, color="#444444", alpha=0.6)

        # Right subplot: Time
        ax_time = axes[1]
        ax_time.set_facecolor("black")
        ax_time.plot(sizes, quick_times, marker="o", label="Quickselect (moy. temps)")
        ax_time.plot(sizes, mom_times, marker="s", label="Médiane Probabiliste (moy. temps)")
        ax_time.set_xlabel("Taille n", color="white")
        ax_time.set_ylabel("Temps (secondes, moyenne)", color="white")
        ax_time.set_title("Temps d'exécution", color="white")
        ax_time.tick_params(colors="white")
        for spine in ax_time.spines.values():
            spine.set_color("white")
        leg2 = ax_time.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
        leg2.get_frame().set_facecolor("black")
        leg2.get_frame().set_edgecolor("white")
        for text in leg2.get_texts():
            text.set_color("white")
        ax_time.grid(True, color="#444444", alpha=0.6)

        fig.suptitle("Comparaison Quickselect vs Médiane Probabiliste", color="white")
        plt.tight_layout()
        plt.show()
