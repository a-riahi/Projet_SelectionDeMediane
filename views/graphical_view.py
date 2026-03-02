import tkinter as tk
from tkinter import ttk
import time

class GraphicalView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Démonstrateur - Comparaison des Méthodes de Sélection")
        self.root.geometry("1600x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_algo = None
        self.current_step = 0
        self.steps_data = []
        self.result = None
        self.total_steps = 0
        self.elapsed_time = 0.0
        self.displayed_steps = []  # Liste des indices d'étapes déjà affichées
        self.step_widgets = {}  # Dictionnaire pour stocker les widgets de chaque étape
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame pour le menu (sera rempli par le contrôleur)
        self.menu_frame = ttk.Frame(self.root, padding="5")
        self.menu_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Frame pour la configuration (tableau et pivots)
        self.config_frame = ttk.LabelFrame(self.root, text="Configuration", padding="10")
        self.config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        self.config_frame.columnconfigure(1, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Démonstrateur des Étapes de Comparaison", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Frame gauche - Informations et contrôles
        left_frame = ttk.LabelFrame(main_frame, text="Informations", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        # Limiter la largeur minimale du frame gauche pour laisser plus d'espace à droite
        main_frame.columnconfigure(0, weight=0, minsize=300)
        
        # Algorithme sélectionné
        self.algo_label = ttk.Label(left_frame, text="Algorithme: -", font=('Arial', 12, 'bold'))
        self.algo_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        
        # Résultat
        self.result_label = ttk.Label(left_frame, text="Résultat: -", font=('Arial', 11))
        self.result_label.grid(row=1, column=0, pady=5, sticky=tk.W)
        
        # Statistiques
        stats_frame = ttk.Frame(left_frame)
        stats_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.steps_label = ttk.Label(stats_frame, text="Comparaisons: 0")
        self.steps_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(stats_frame, text="Temps: 0.000s")
        self.time_label.grid(row=1, column=0, sticky=tk.W)
        
        # Contrôles de navigation
        control_frame = ttk.LabelFrame(left_frame, text="Navigation", padding="10")
        control_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        control_frame.columnconfigure(0, weight=1)
        
        self.step_label = ttk.Label(control_frame, text="Étape: 0 / 0")
        self.step_label.grid(row=0, column=0, pady=5)
        
        nav_frame = ttk.Frame(control_frame)
        nav_frame.grid(row=1, column=0, pady=5)
        
        self.prev_btn = ttk.Button(nav_frame, text="◀ Précédent", command=self.prev_step, state=tk.DISABLED)
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        self.next_btn = ttk.Button(nav_frame, text="Suivant ▶", command=self.next_step, state=tk.DISABLED)
        self.next_btn.grid(row=0, column=1, padx=5)
        
        self.auto_btn = ttk.Button(nav_frame, text="▶▶ Auto", command=self.toggle_auto)
        self.auto_btn.grid(row=0, column=2, padx=5)
        
        # Frame droite - Affichage des étapes et tableaux
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Description de l'étape
        self.desc_label = ttk.Label(right_frame, text="Sélectionnez un algorithme pour commencer", 
                                    font=('Arial', 11), wraplength=1000)
        self.desc_label.grid(row=0, column=0, pady=10, sticky=tk.W)
        
        # Zone d'affichage des tableaux
        canvas_frame = ttk.Frame(right_frame)
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        # Canvas avec scrollbar
        canvas = tk.Canvas(canvas_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Fonction pour mettre à jour la largeur du scrollable_frame
        def configure_scrollable_frame(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            self.scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scrollable_frame)
        canvas.bind("<Configure>", configure_canvas)
        
        # Configurer les colonnes du scrollable_frame pour utiliser toute la largeur
        self.scrollable_frame.columnconfigure(0, weight=1)
        
        self.canvas = canvas
        self.content_frame = self.scrollable_frame
        
        # S'assurer que le content_frame utilise toute la largeur disponible
        self.content_frame.columnconfigure(0, weight=1)
        
        # Auto-play
        self.auto_playing = False
        self.auto_interval = 2000  # 2 secondes
    
    def load_algorithm(self, algo_name, steps_data, result, total_steps, elapsed_time):
        """Charge les données d'un algorithme"""
        self.current_algo = algo_name
        self.steps_data = steps_data
        self.result = result
        self.total_steps = total_steps
        self.elapsed_time = elapsed_time
        self.current_step = 0
        self.displayed_steps = []
        self.step_widgets = {}
        
        # Effacer le contenu précédent
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mettre à jour les labels
        self.algo_label.config(text=f"Algorithme: {algo_name}")
        self.result_label.config(text=f"Résultat: {result}")
        self.steps_label.config(text=f"Comparaisons: {total_steps}")
        self.time_label.config(text=f"Temps: {elapsed_time:.6f}s")
        
        # Activer les boutons
        self.next_btn.config(state=tk.NORMAL)
        if len(steps_data) > 0:
            self.prev_btn.config(state=tk.DISABLED)
        
        # Afficher la première étape
        self.display_step(0)
    
    def display_step(self, step_index):
        """Affiche une étape spécifique et garde les étapes précédentes visibles"""
        if step_index < 0 or step_index >= len(self.steps_data):
            return
        
        self.current_step = step_index
        step = self.steps_data[step_index]
        
        # Mettre à jour la description
        desc = f"Étape {step_index + 1}/{len(self.steps_data)}: {step['description']}"
        if step['comparisons'] > 0:
            desc += f" [{step['comparisons']} comparaisons]"
        self.desc_label.config(text=desc)
        
        # Mettre à jour le label d'étape
        self.step_label.config(text=f"Étape: {step_index + 1} / {len(self.steps_data)}")
        
        # Mettre à jour les boutons
        self.prev_btn.config(state=tk.NORMAL if step_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if step_index < len(self.steps_data) - 1 else tk.DISABLED)
        
        # Si l'étape n'a pas encore été affichée, l'ajouter
        if step_index not in self.displayed_steps:
            self.displayed_steps.append(step_index)
            self.displayed_steps.sort()
            self.add_step_widget(step_index)
        
        # Mettre en évidence l'étape courante
        self.highlight_current_step(step_index)
        
        # Faire défiler jusqu'à l'étape courante
        if step_index in self.step_widgets:
            self.root.after(100, lambda: self.scroll_to_step(step_index))
    
    def scroll_to_step(self, step_index):
        """Fait défiler jusqu'à une étape spécifique"""
        if step_index not in self.step_widgets:
            return
        
        frame = self.step_widgets[step_index]['frame']
        frame.update_idletasks()
        self.canvas.update_idletasks()
        
        # Obtenir la position du frame dans le canvas
        try:
            # Calculer la position relative dans le contenu
            frame_y = frame.winfo_y()
            content_height = self.content_frame.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            
            if content_height > canvas_height:
                # Calculer la position de défilement (0.0 à 1.0)
                scroll_pos = max(0.0, min(1.0, (frame_y - 50) / max(1, content_height - canvas_height)))
                self.canvas.yview_moveto(scroll_pos)
        except:
            pass
    
    def add_step_widget(self, step_index):
        """Ajoute un widget pour une étape"""
        step = self.steps_data[step_index]
        
        # Créer un frame pour cette étape
        step_frame = ttk.LabelFrame(self.content_frame, 
                                   text=f"Étape {step_index + 1}: {step['description']}", 
                                   padding="15")
        step_frame.grid(row=step_index, column=0, pady=8, sticky=(tk.W, tk.E), padx=15)
        step_frame.columnconfigure(0, weight=1)
        
        # Frame pour les informations de l'étape avec style amélioré
        info_frame = tk.Frame(step_frame, bg='#F5F5F5', relief=tk.FLAT)
        info_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        info_text = f"Comparaisons: {step['comparisons']} | Cumul: {step['cumulative']}"
        info_label = tk.Label(info_frame, text=info_text, font=('Arial', 10, 'bold'), 
                             foreground='#555555', bg='#F5F5F5', padx=10, pady=5)
        info_label.pack(side=tk.LEFT)
        
        # Afficher les tableaux si disponibles
        if 'arrays' in step and step['arrays']:
            self.display_arrays_in_frame(step['arrays'], step_frame)
        
        # Stocker la référence
        self.step_widgets[step_index] = {
            'frame': step_frame,
            'info': info_label
        }
    
    def highlight_current_step(self, step_index):
        """Met en évidence l'étape courante"""
        style = ttk.Style()
        style.configure('Current.TLabelframe', borderwidth=3, relief=tk.RAISED)
        style.configure('Normal.TLabelframe', borderwidth=1, relief=tk.FLAT)
        
        for idx, widget_data in self.step_widgets.items():
            frame = widget_data['frame']
            info_label = widget_data['info']
            if idx == step_index:
                # Mettre en évidence l'étape courante
                frame.configure(style='Current.TLabelframe')
                # Changer la couleur de fond du frame d'info
                if hasattr(info_label, 'master'):
                    info_frame = info_label.master
                    info_frame.configure(bg='#E3F2FD')
                    info_label.configure(bg='#E3F2FD', foreground='#1976D2')
            else:
                # Réinitialiser les autres étapes
                frame.configure(style='Normal.TLabelframe')
                if hasattr(info_label, 'master'):
                    info_frame = info_label.master
                    info_frame.configure(bg='#F5F5F5')
                    info_label.configure(bg='#F5F5F5', foreground='#555555')
    
    def display_arrays_in_frame(self, arrays, parent_frame):
        """Affiche les tableaux dans un frame parent donné avec un affichage amélioré"""
        # Afficher chaque tableau
        for key, value in arrays.items():
            if key == 'pivot':
                # Afficher le pivot séparément avec style
                pivot_frame = ttk.LabelFrame(parent_frame, text="🎯 Pivot Sélectionné", padding="10")
                pivot_frame.pack(fill=tk.X, pady=8, padx=5)
                pivot_label = tk.Label(pivot_frame, text=f"{value}", 
                                      font=('Arial', 18, 'bold'), 
                                      foreground='#0066CC', 
                                      bg='#E6F2FF',
                                      relief=tk.RAISED,
                                      borderwidth=2,
                                      padx=30,
                                      pady=15)
                pivot_label.pack()
                
            elif key == 'a' or key == 'b':
                # Afficher les bornes avec style
                color = '#00AA00' if key == 'a' else '#AA6600'
                bound_frame = ttk.LabelFrame(parent_frame, text=f"Borne {key.upper()}", padding="8")
                bound_frame.pack(fill=tk.X, pady=5, padx=5)
                bound_label = tk.Label(bound_frame, text=f"{key.upper()} = {value}", 
                                      font=('Arial', 13, 'bold'), 
                                      foreground=color,
                                      bg='#F0F8F0',
                                      relief=tk.RAISED,
                                      borderwidth=1,
                                      padx=20,
                                      pady=8)
                bound_label.pack()
            elif key == 'result':
                # Afficher le résultat
                result_frame = ttk.LabelFrame(parent_frame, text="✅ Résultat", padding="10")
                result_frame.pack(fill=tk.X, pady=8, padx=5)
                result_label = tk.Label(result_frame, text=f"Résultat: {value}", 
                                       font=('Arial', 16, 'bold'), 
                                       foreground='#006600',
                                       bg='#E6FFE6',
                                       relief=tk.RAISED,
                                       borderwidth=2,
                                       padx=25,
                                       pady=12)
                result_label.pack()
            elif key == 'direction':
                # Afficher la direction de recherche
                dir_frame = ttk.LabelFrame(parent_frame, text="Direction", padding="5")
                dir_frame.pack(fill=tk.X, pady=2, padx=5)
                dir_label = tk.Label(dir_frame, text=f"→ Recherche dans la partie {value}", 
                                    font=('Arial', 10, 'italic'), 
                                    foreground='#666666')
                dir_label.pack()
                
            elif isinstance(value, list) and len(value) > 0:
                # Afficher le tableau avec un affichage amélioré
                array_title = key.replace('_', ' ').title()
                array_frame = ttk.LabelFrame(parent_frame, text=f"📊 {array_title} ({len(value)} éléments)", padding="10")
                array_frame.pack(fill=tk.BOTH, expand=True, pady=8, padx=5)
                array_frame.columnconfigure(0, weight=1)
                
                # Créer un canvas avec scrollbar pour les grands tableaux
                canvas_container = tk.Frame(array_frame)
                canvas_container.pack(fill=tk.BOTH, expand=True)
                canvas_container.columnconfigure(0, weight=1)
                canvas_container.rowconfigure(0, weight=1)
                
                canvas = tk.Canvas(canvas_container, bg='#FAFAFA', height=200, highlightthickness=1, highlightbackground='#E0E0E0')
                scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg='#FAFAFA')
                
                def update_scrollregion(event):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                
                scrollable_frame.bind("<Configure>", update_scrollregion)
                
                canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                
                def configure_canvas_width(event):
                    canvas_width = event.width
                    canvas.itemconfig(canvas_window, width=canvas_width)
                
                canvas.bind("<Configure>", configure_canvas_width)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Afficher les éléments du tableau dans une grille colorée
                max_per_row = 25
                row = 0
                col = 0
                
                # Déterminer quels éléments afficher
                if len(value) > 100:
                    # Pour très grands tableaux, afficher seulement les premiers et derniers
                    display_items = value[:50] + [("...", len(value) - 100)] + value[-50:]
                    show_all = False
                elif len(value) > 50:
                    # Pour grands tableaux, afficher avec troncature
                    display_items = value[:30] + [("...", len(value) - 60)] + value[-30:]
                    show_all = False
                else:
                    display_items = value
                    show_all = True
                
                for idx, item in enumerate(display_items):
                    if isinstance(item, tuple) and item[0] == "...":
                        # Afficher l'indicateur de troncature
                        ellipsis_label = tk.Label(scrollable_frame, 
                                                 text=f"... ({item[1]} éléments non affichés) ...",
                                                 font=('Arial', 9, 'italic'),
                                                 fg='gray',
                                                 bg='white')
                        ellipsis_label.grid(row=row, column=0, columnspan=max_per_row, pady=5, padx=5)
                        row += 1
                        col = 0
                    else:
                        # Afficher l'élément avec style et couleurs selon le type
                        bg_color = '#E8F4F8' if idx % 2 == 0 else '#F0F8FF'
                        if key == 'original' or key == 'current':
                            bg_color = '#FFF4E6'  # Orange clair pour tableau original/courant
                        elif key == 'left' or key == 'next_array':
                            bg_color = '#FFE6E6'  # Rouge clair pour partie gauche
                        elif key == 'right':
                            bg_color = '#E6F2FF'  # Bleu clair pour partie droite
                        elif key == 'equal':
                            bg_color = '#E6FFE6'  # Vert clair pour égal
                        elif key == 'R' or key == 'R_sorted':
                            bg_color = '#F0E6FF'  # Violet clair pour échantillon R
                        elif key == 'P' or key == 'P_sorted':
                            bg_color = '#E6F0FF'  # Bleu très clair pour partition P
                        
                        element_label = tk.Label(scrollable_frame,
                                                text=str(item),
                                                font=('Courier', 11, 'bold'),
                                                bg=bg_color,
                                                relief=tk.RAISED,
                                                borderwidth=1,
                                                padx=10,
                                                pady=5,
                                                width=8,
                                                anchor='center')
                        element_label.grid(row=row, column=col, padx=3, pady=3, sticky='ew')
                        
                        col += 1
                        if col >= max_per_row:
                            col = 0
                            row += 1
                
                # Configurer les colonnes pour qu'elles s'étendent uniformément
                for i in range(max_per_row):
                    scrollable_frame.columnconfigure(i, weight=1, uniform="equal")
                
                canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
                
                # Afficher la taille si le tableau est tronqué
                if not show_all:
                    size_label = tk.Label(array_frame, 
                                         text=f"⚠ Affichage limité: {len(value)} éléments au total",
                                         font=('Arial', 8, 'italic'),
                                         fg='gray',
                                         bg='white')
                    size_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Afficher les informations de partition pour Quickselect avec style
        if 'left' in arrays and 'right' in arrays:
            partition_frame = ttk.LabelFrame(parent_frame, text="📋 Résultat de la Partition", padding="10")
            partition_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Créer une grille pour les statistiques
            stats_frame = tk.Frame(partition_frame, bg='white')
            stats_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Éléments < pivot
            left_frame = tk.Frame(stats_frame, bg='#FFE6E6', relief=tk.RAISED, borderwidth=2)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            tk.Label(left_frame, text="< Pivot", font=('Arial', 9, 'bold'), bg='#FFE6E6').pack()
            tk.Label(left_frame, text=f"{len(arrays['left'])}", 
                    font=('Arial', 14, 'bold'), bg='#FFE6E6', fg='#CC0000').pack()
            
            # Éléments = pivot
            equal_frame = tk.Frame(stats_frame, bg='#E6FFE6', relief=tk.RAISED, borderwidth=2)
            equal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            tk.Label(equal_frame, text="= Pivot", font=('Arial', 9, 'bold'), bg='#E6FFE6').pack()
            tk.Label(equal_frame, text=f"{len(arrays.get('equal', []))}", 
                    font=('Arial', 14, 'bold'), bg='#E6FFE6', fg='#00AA00').pack()
            
            # Éléments > pivot
            right_frame = tk.Frame(stats_frame, bg='#E6F2FF', relief=tk.RAISED, borderwidth=2)
            right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            tk.Label(right_frame, text="> Pivot", font=('Arial', 9, 'bold'), bg='#E6F2FF').pack()
            tk.Label(right_frame, text=f"{len(arrays['right'])}", 
                    font=('Arial', 14, 'bold'), bg='#E6F2FF', fg='#0066CC').pack()
            
            # Afficher les tableaux de partition si pas trop grands
            if len(arrays.get('left', [])) <= 30:
                self._display_partition_array(partition_frame, arrays.get('left', []), "Éléments < Pivot", '#FFE6E6')
            if len(arrays.get('equal', [])) <= 30:
                self._display_partition_array(partition_frame, arrays.get('equal', []), "Éléments = Pivot", '#E6FFE6')
            if len(arrays.get('right', [])) <= 30:
                self._display_partition_array(partition_frame, arrays.get('right', []), "Éléments > Pivot", '#E6F2FF')
    
    def _display_partition_array(self, parent, arr, title, bg_color):
        """Affiche un tableau de partition avec style"""
        if not arr:
            return
        
        part_frame = ttk.LabelFrame(parent, text=title, padding="5")
        part_frame.pack(fill=tk.X, pady=3, padx=5)
        
        array_text = "  ".join(f"[{x}]" for x in arr)
        text_widget = tk.Text(part_frame, height=2, wrap=tk.WORD, 
                            font=('Courier', 9), bg=bg_color, relief=tk.FLAT)
        text_widget.insert('1.0', array_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.X, padx=5, pady=2)
    
    
    def prev_step(self):
        """Étape précédente"""
        if self.current_step > 0:
            self.display_step(self.current_step - 1)
    
    def next_step(self):
        """Étape suivante"""
        if self.current_step < len(self.steps_data) - 1:
            self.display_step(self.current_step + 1)
    
    def toggle_auto(self):
        """Active/désactive le mode auto"""
        self.auto_playing = not self.auto_playing
        if self.auto_playing:
            self.auto_btn.config(text="⏸ Pause")
            self.auto_play()
        else:
            self.auto_btn.config(text="▶▶ Auto")
    
    def auto_play(self):
        """Joue automatiquement les étapes"""
        if not self.auto_playing:
            return
        
        if self.current_step < len(self.steps_data) - 1:
            self.next_step()
            self.root.after(self.auto_interval, self.auto_play)
        else:
            self.auto_playing = False
            self.auto_btn.config(text="▶▶ Auto")
    
    def show_comparison(self, algo1_name, algo1_steps, algo1_result, algo1_time,
                       algo2_name, algo2_steps, algo2_result, algo2_time):
        """Affiche une fenêtre de comparaison"""
        comp_window = tk.Toplevel(self.root)
        comp_window.title("Comparaison des Méthodes")
        comp_window.geometry("600x300")
        
        # Titre
        ttk.Label(comp_window, text="Comparaison des Méthodes", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Tableau de comparaison
        frame = ttk.Frame(comp_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # En-têtes
        ttk.Label(frame, text="Métrique", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Label(frame, text=algo1_name, font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame, text=algo2_name, font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        
        # Lignes
        metrics = [
            ("Résultat", str(algo1_result), str(algo2_result)),
            ("Temps (s)", f"{algo1_time:.6f}", f"{algo2_time:.6f}"),
            ("Comparaisons", str(algo1_steps), str(algo2_steps))
        ]
        
        for i, (metric, val1, val2) in enumerate(metrics, 1):
            ttk.Label(frame, text=metric).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Label(frame, text=val1).grid(row=i, column=1, padx=10, pady=5)
            ttk.Label(frame, text=val2).grid(row=i, column=2, padx=10, pady=5)
        
        # Ratio
        if algo2_steps > 0:
            ratio = algo1_steps / algo2_steps
            ttk.Label(frame, text="Ratio", font=('Arial', 9, 'italic')).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Label(frame, text=f"{ratio:.2f}x", font=('Arial', 9, 'italic')).grid(row=4, column=1, padx=10, pady=5)
            ttk.Label(frame, text="1.00x", font=('Arial', 9, 'italic')).grid(row=4, column=2, padx=10, pady=5)
        
        # Bouton fermer
        ttk.Button(comp_window, text="Fermer", command=comp_window.destroy).pack(pady=10)
    
    def setup_config_ui(self, on_run_callback):
        """Configure l'interface de configuration du tableau et des pivots"""
        # Effacer le contenu précédent
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        
        # Taille du tableau
        ttk.Label(self.config_frame, text="Taille du tableau:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        size_var = tk.StringVar(value="50")
        size_entry = ttk.Entry(self.config_frame, textvariable=size_var, width=10)
        size_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Tableau manuel ou aléatoire
        ttk.Label(self.config_frame, text="Tableau:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        array_mode = tk.StringVar(value="random")
        
        def toggle_array_input():
            if array_mode.get() == "manual":
                array_entry.config(state=tk.NORMAL)
                generate_btn.config(state=tk.DISABLED)
            else:
                array_entry.config(state=tk.DISABLED)
                generate_btn.config(state=tk.NORMAL)
        
        ttk.Radiobutton(self.config_frame, text="Aléatoire", variable=array_mode, 
                       value="random", command=toggle_array_input).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.config_frame, text="Manuel", variable=array_mode, 
                       value="manual", command=toggle_array_input).grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Champ pour entrer le tableau manuellement
        array_var = tk.StringVar()
        array_entry = ttk.Entry(self.config_frame, textvariable=array_var, width=40, state=tk.DISABLED)
        array_entry.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Label(self.config_frame, text="Format: 1,2,3,4,5 ou 1 2 3 4 5", 
                 font=('Arial', 8), foreground='gray').grid(row=3, column=0, columnspan=3, padx=5, sticky=tk.W)
        
        # Bouton pour générer un tableau aléatoire
        generate_btn = ttk.Button(self.config_frame, text="Générer", state=tk.NORMAL)
        generate_btn.grid(row=2, column=3, padx=5, pady=5)
        
        # Configuration des pivots (pour Quickselect)
        ttk.Label(self.config_frame, text="Pivots (Quickselect):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        pivot_mode = tk.StringVar(value="random")
        
        def toggle_pivot_input():
            if pivot_mode.get() == "manual":
                pivot_entry.config(state=tk.NORMAL)
            else:
                pivot_entry.config(state=tk.DISABLED)
        
        ttk.Radiobutton(self.config_frame, text="Aléatoire", variable=pivot_mode, 
                       value="random", command=toggle_pivot_input).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.config_frame, text="Manuel", variable=pivot_mode, 
                       value="manual", command=toggle_pivot_input).grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Champ pour entrer les pivots manuellement
        pivot_var = tk.StringVar()
        pivot_entry = ttk.Entry(self.config_frame, textvariable=pivot_var, width=40, state=tk.DISABLED)
        pivot_entry.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Label(self.config_frame, text="Format: pivot1,pivot2,... (un par niveau récursif)", 
                 font=('Arial', 8), foreground='gray').grid(row=6, column=0, columnspan=3, padx=5, sticky=tk.W)
        
        # Position k
        ttk.Label(self.config_frame, text="Position k (médiane si vide):").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        k_var = tk.StringVar()
        k_entry = ttk.Entry(self.config_frame, textvariable=k_var, width=10)
        k_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Bouton pour lancer la démonstration
        def run_demo():
            try:
                # Récupérer la taille
                size = int(size_var.get())
                if size < 1 or size > 1000:
                    raise ValueError("La taille doit être entre 1 et 1000")
                
                # Récupérer le tableau
                if array_mode.get() == "manual":
                    # Vérifier si on a un tableau généré stocké
                    if hasattr(array_entry, 'arr_data') and array_entry.arr_data is not None:
                        arr = array_entry.arr_data
                        if len(arr) != size:
                            # Régénérer si la taille a changé
                            import random
                            arr = random.sample(range(1, size * 10), size)
                    else:
                        array_str = array_var.get().strip()
                        if not array_str:
                            raise ValueError("Veuillez entrer un tableau")
                        # Parser le tableau (supporter les deux formats)
                        array_str = array_str.replace(',', ' ')
                        arr = [int(x.strip()) for x in array_str.split() if x.strip()]
                        if len(arr) != size:
                            raise ValueError(f"Le tableau doit contenir {size} éléments")
                else:
                    arr = None  # Sera généré aléatoirement
                
                # Récupérer les pivots
                pivots = None
                if pivot_mode.get() == "manual":
                    pivot_str = pivot_var.get().strip()
                    if pivot_str:
                        pivot_str = pivot_str.replace(',', ' ')
                        pivots = [int(x.strip()) for x in pivot_str.split() if x.strip()]
                
                # Récupérer k
                k = None
                if k_var.get().strip():
                    k = int(k_var.get())
                    if k < 0:
                        raise ValueError("k doit être >= 0")
                
                # Appeler le callback avec les paramètres
                on_run_callback(size, arr, pivots, k)
                
            except ValueError as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", str(e))
            except Exception as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        
        run_btn = ttk.Button(self.config_frame, text="▶ Lancer la démonstration", command=run_demo)
        run_btn.grid(row=8, column=0, columnspan=4, padx=5, pady=10)
        
        # Stocker les références pour y accéder depuis l'extérieur
        self.config_vars = {
            'size': size_var,
            'array_mode': array_mode,
            'array': array_var,
            'array_entry': array_entry,
            'pivot_mode': pivot_mode,
            'pivot': pivot_var,
            'pivot_entry': pivot_entry,
            'k': k_var,
            'generate_btn': generate_btn
        }
        
        # Fonction pour générer un tableau aléatoire et l'afficher
        def generate_random_array():
            try:
                size = int(size_var.get())
                if size < 1 or size > 1000:
                    raise ValueError("La taille doit être entre 1 et 1000")
                import random
                arr = random.sample(range(1, size * 10), size)
                # Stocker le tableau complet
                array_entry.arr_data = arr
                # Afficher le tableau avec des espaces pour la lisibilité
                if size <= 20:
                    array_var.set(", ".join(map(str, arr)))
                else:
                    # Pour les grands tableaux, afficher seulement les premiers et derniers
                    preview = ", ".join(map(str, arr[:10])) + f", ... ({size-20} éléments), " + ", ".join(map(str, arr[-10:]))
                    array_var.set(preview)
                # Passer en mode manuel pour afficher le tableau généré
                array_mode.set("manual")
                toggle_array_input()
            except ValueError as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", str(e))
        
        generate_btn.config(command=generate_random_array)
        
        # Stocker une référence au tableau généré
        array_entry.arr_data = None
    
    def run(self):
        """Lance l'interface graphique"""
        self.root.mainloop()

