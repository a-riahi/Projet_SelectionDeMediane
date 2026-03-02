class SelectionView:
    def show_result(self, algo_name, result, elapsed, steps):
        print(f"{algo_name:20s} -> médiane = {result}, "
              f"temps = {elapsed:.6f} sec, étapes = {steps}")

    def show_verification(self, exact):
        print(f"Vérification par tri complet : {exact}")
    
    def show_detailed_steps(self, algo_name, detailed_steps, total_steps, result, elapsed):
        """Affiche les étapes détaillées d'un algorithme avec les tableaux"""
        print("\n" + "="*80)
        print(f"  {algo_name.upper()}")
        print("="*80)
        print(f"Résultat: {result} | Temps: {elapsed:.6f}s | Total comparaisons: {total_steps}")
        print("-"*80)
        
        for i, step in enumerate(detailed_steps, 1):
            comparisons_str = f"[{step['comparisons']} comparaisons]" if step['comparisons'] > 0 else ""
            cumulative_str = f"(cumul: {step['cumulative']})"
            print(f"\n  {i:3d}. {step['description']:60s} {comparisons_str:20s} {cumulative_str}")
            
            # Afficher les tableaux si disponibles
            if 'arrays' in step and step['arrays']:
                self._display_arrays_terminal(step['arrays'], indent="      ")
        
        print("\n" + "="*80 + "\n")
    
    def _display_arrays_terminal(self, arrays, indent=""):
        """Affiche les tableaux dans le terminal de manière lisible"""
        for key, value in arrays.items():
            if key == 'pivot':
                print(f"{indent}🎯 Pivot sélectionné: {value}")
            elif key == 'a' or key == 'b':
                print(f"{indent}📍 Borne {key.upper()} = {value}")
            elif key == 'result':
                print(f"{indent}✅ Résultat: {value}")
            elif key == 'direction':
                print(f"{indent}→ Direction: {value}")
            elif isinstance(value, list) and len(value) > 0:
                array_title = key.replace('_', ' ').title()
                print(f"{indent}📊 {array_title} ({len(value)} éléments):")
                
                # Afficher le tableau de manière formatée
                if len(value) <= 30:
                    # Afficher tous les éléments
                    elements_per_line = 15
                    for i in range(0, len(value), elements_per_line):
                        line = value[i:i+elements_per_line]
                        line_str = "  ".join(f"{x:>6}" for x in line)
                        print(f"{indent}   {line_str}")
                elif len(value) <= 100:
                    # Afficher les premiers et derniers
                    print(f"{indent}   Premiers 20: {'  '.join(str(x) for x in value[:20])}")
                    print(f"{indent}   ... ({len(value) - 40} éléments non affichés) ...")
                    print(f"{indent}   Derniers 20: {'  '.join(str(x) for x in value[-20:])}")
                else:
                    # Pour très grands tableaux
                    print(f"{indent}   Premiers 30: {'  '.join(str(x) for x in value[:30])}")
                    print(f"{indent}   ... ({len(value) - 60} éléments non affichés) ...")
                    print(f"{indent}   Derniers 30: {'  '.join(str(x) for x in value[-30:])}")
        
        # Afficher les informations de partition pour Quickselect
        if 'left' in arrays and 'right' in arrays:
            print(f"{indent}📋 Partition:")
            print(f"{indent}   < Pivot: {len(arrays['left'])} éléments", end="")
            if len(arrays['left']) <= 20:
                print(f" → {arrays['left']}")
            else:
                print(f" → {arrays['left'][:10]}...{arrays['left'][-10:]}")
            
            print(f"{indent}   = Pivot: {len(arrays.get('equal', []))} éléments", end="")
            if arrays.get('equal'):
                if len(arrays['equal']) <= 20:
                    print(f" → {arrays['equal']}")
                else:
                    print(f" → {arrays['equal'][:10]}...{arrays['equal'][-10:]}")
            else:
                print()
            
            print(f"{indent}   > Pivot: {len(arrays['right'])} éléments", end="")
            if len(arrays['right']) <= 20:
                print(f" → {arrays['right']}")
            else:
                print(f" → {arrays['right'][:10]}...{arrays['right'][-10:]}")
    
    def show_comparison(self, algo1_name, algo1_steps, algo1_result, algo1_time,
                       algo2_name, algo2_steps, algo2_result, algo2_time):
        """Affiche une comparaison côte à côte des deux algorithmes"""
        print("\n" + "="*100)
        print("  COMPARAISON DES MÉTHODES".center(100))
        print("="*100)
        
        # En-têtes
        print(f"{'MÉTRIQUE':<30} | {algo1_name:30s} | {algo2_name:30s}")
        print("-"*100)
        
        # Résultats
        print(f"{'Résultat':<30} | {str(algo1_result):30s} | {str(algo2_result):30s}")
        print(f"{'Temps (secondes)':<30} | {algo1_time:30.6f} | {algo2_time:30.6f}")
        print(f"{'Total comparaisons':<30} | {algo1_steps:30d} | {algo2_steps:30d}")
        
        # Ratio
        if algo2_steps > 0:
            ratio = algo1_steps / algo2_steps
            print(f"{'Ratio (algo1/algo2)':<30} | {ratio:30.2f}x | {'1.00x':>30s}")
        
        print("="*100 + "\n")