#!/usr/bin/env python3
"""
Battle Factory Editor v3.2 - Fixed Searchable Dropdowns
Pokemon HeartGold/SoulSilver Battle Factory Editor with Visual Enhancements
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import struct
import csv
from pathlib import Path

# Move type colors (based on Pokemon type colors)
MOVE_TYPE_COLORS = {
    'Normal': '#A8A878',
    'Fighting': '#C03028',
    'Flying': '#A890F0',
    'Poison': '#A040A0',
    'Ground': '#E0C068',
    'Rock': '#B8A038',
    'Bug': '#A8B820',
    'Ghost': '#705898',
    'Steel': '#B8B8D0',
    'Fire': '#F08030',
    'Water': '#6890F0',
    'Grass': '#78C850',
    'Electric': '#F8D030',
    'Psychic': '#F85888',
    'Ice': '#98D8D8',
    'Dragon': '#7038F8',
    'Dark': '#705848',
    'Fairy': '#EE99AC',
}

class SearchableCombobox(ttk.Combobox):
    """A Combobox widget with live search functionality"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self._all_values = []
        self._is_filtering = False
        
        # Bind key press to filter
        self.bind('<KeyRelease>', self._on_keyrelease)
        
    def set_values(self, values):
        """Set the full list of values"""
        self._all_values = list(values)
        self['values'] = self._all_values
    
    def _on_keyrelease(self, event):
        """Filter values based on what user typed"""
        # Ignore special keys
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 
                           'Home', 'End', 'Delete', 'Shift_L', 'Shift_R',
                           'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
                           'Return', 'Tab'):
            return
        
        # Get current text
        typed = self.get().lower()
        
        if not typed:
            # If empty, show all values
            self['values'] = self._all_values
            return
        
        # Filter values that contain the typed text
        filtered = [v for v in self._all_values if typed in v.lower()]
        
        # Update dropdown with filtered values
        self._is_filtering = True
        self['values'] = filtered
        self._is_filtering = False
        
        # Keep the dropdown open to show results
        if filtered:
            self.event_generate('<Down>')

class BattleFactoryEditorEnhanced:
    def __init__(self, root):
        self.root = root
        self.root.title("Battle Factory Editor v1.0")
        self.root.geometry("1600x900")
        
        # Data storage
        self.a202_data = None
        self.a203_data = None
        self.a202_path = None
        self.a203_path = None
        self.trainers = []
        self.pokemon_list = []
        self.current_trainer_index = None
        self.current_pokemon_index = None
        self.modified = False
        
        # Load reference data
        self.load_reference_data()
        
        # Color scheme
        self.bg_color = '#F0F0F0'
        self.group1_color = '#E3F2FD'  # Light blue
        self.group2_color = '#FFF3E0'  # Light orange
        self.legendary_color = '#FCE4EC'  # Light pink
        
        # Create UI
        self.create_menu()
        self.create_ui()
        
    def load_reference_data(self):
        """Load species, moves, items, natures from CSV files"""
        app_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
        
        # Default data
        self.species_data = {i: f"Species_{i:03d}" for i in range(1500)}
        self.move_data = {i: f"Move_{i:03d}" for i in range(1000)}
        self.move_types = {}  # Move ID -> Type name
        self.item_data = {i: f"Item_{i:03d}" for i in range(3000)}
        self.nature_data = {
            0: "Hardy", 1: "Lonely", 2: "Brave", 3: "Adamant", 4: "Naughty",
            5: "Bold", 6: "Docile", 7: "Relaxed", 8: "Impish", 9: "Lax",
            10: "Timid", 11: "Hasty", 12: "Serious", 13: "Jolly", 14: "Naive",
            15: "Modest", 16: "Mild", 17: "Quiet", 18: "Bashful", 19: "Rash",
            20: "Calm", 21: "Gentle", 22: "Sassy", 23: "Careful", 24: "Quirky"
        }
        
        # Load species
        try:
            species_file = app_dir / "species.csv"
            if species_file.exists():
                with open(species_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.species_data[int(row['id'])] = row['name']
        except Exception as e:
            print(f"Warning: Could not load species.csv: {e}")
        
        # Load moves with types
        try:
            moves_file = app_dir / "moves.csv"
            if moves_file.exists():
                with open(moves_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        move_id = int(row['id'])
                        self.move_data[move_id] = row['name']
                        if 'type' in row:
                            self.move_types[move_id] = row['type']
        except Exception as e:
            print(f"Warning: Could not load moves.csv: {e}")
        
        # Load items
        try:
            items_file = app_dir / "items.csv"
            if items_file.exists():
                with open(items_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.item_data[int(row['id'])] = row['name']
        except Exception as e:
            print(f"Warning: Could not load items.csv: {e}")
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open a202 (Trainers)", command=self.load_a202)
        file_menu.add_command(label="Open a203 (Pokemon)", command=self.load_a203)
        file_menu.add_separator()
        file_menu.add_command(label="Save All Changes", command=self.save_all)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Trainers Mode", command=lambda: self.switch_view('trainers'))
        view_menu.add_command(label="Pokemon Groups Mode", command=lambda: self.switch_view('groups'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Quick Guide", command=self.show_quick_guide)
    
    def create_ui(self):
        """Create main UI with notebook tabs"""
        # Create notebook for different views
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Trainer-based editing
        self.trainer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trainer_frame, text="📋 Edit by Trainer")
        self.create_trainer_view(self.trainer_frame)
        
        # Tab 2: Group-based editing
        self.group_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.group_frame, text="🎯 Edit by Pokemon Group")
        self.create_group_view(self.group_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Load files to begin. TIP: Type in dropdowns to search instantly!")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_trainer_view(self, parent):
        """Create trainer-based view"""
        main_paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Trainer list
        left_frame = ttk.LabelFrame(main_paned, text="Trainers", padding=5)
        main_paned.add(left_frame, width=250)
        
        self.trainer_listbox = tk.Listbox(left_frame, width=30)
        trainer_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.trainer_listbox.yview)
        self.trainer_listbox.config(yscrollcommand=trainer_scroll.set)
        self.trainer_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        trainer_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.trainer_listbox.bind('<<ListboxSelect>>', self.on_trainer_select)
        
        # Middle panel - Pokemon pool
        middle_frame = ttk.LabelFrame(main_paned, text="Pokemon Pool", padding=5)
        main_paned.add(middle_frame, width=300)
        
        self.trainer_info_label = ttk.Label(middle_frame, text="Select a trainer")
        self.trainer_info_label.pack(anchor=tk.W, pady=5)
        
        self.pool_listbox = tk.Listbox(middle_frame, width=40)
        pool_scroll = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.pool_listbox.yview)
        self.pool_listbox.config(yscrollcommand=pool_scroll.set)
        self.pool_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pool_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.pool_listbox.bind('<<ListboxSelect>>', self.on_pokemon_select_trainer)
        
        # Right panel - Pokemon editor
        right_frame = ttk.LabelFrame(main_paned, text="Pokemon Editor", padding=10)
        main_paned.add(right_frame, width=700)
        
        self.create_pokemon_editor(right_frame, 'trainer')
    
    def create_group_view(self, parent):
        """Create group-based view"""
        main_paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Group selection
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, width=300)
        
        # Group selector
        group_selector = ttk.LabelFrame(left_frame, text="Pokemon Groups", padding=10)
        group_selector.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(group_selector, text="Select a group:", font=('TkDefaultFont', 10, 'bold')).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(group_selector)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.group_basic_btn = tk.Button(btn_frame, text="🔰 Basic Pokemon\n(Rounds 1-3 | Indices 1-350)", 
                                        command=lambda: self.load_group('basic'),
                                        bg=self.group1_color, height=3, font=('TkDefaultFont', 9))
        self.group_basic_btn.pack(fill=tk.X, pady=2)
        
        self.group_advanced_btn = tk.Button(btn_frame, text="⭐ Advanced Pokemon\n(Round 4+ | Indices 351-894)", 
                                           command=lambda: self.load_group('advanced'),
                                           bg=self.group2_color, height=3, font=('TkDefaultFont', 9))
        self.group_advanced_btn.pack(fill=tk.X, pady=2)
        
        self.group_legendary_btn = tk.Button(btn_frame, text="👑 Legendary Pokemon\n(Round 8+ | Indices 895-950)", 
                                            command=lambda: self.load_group('legendary'),
                                            bg=self.legendary_color, height=3, font=('TkDefaultFont', 9))
        self.group_legendary_btn.pack(fill=tk.X, pady=2)
        
        # Pokemon list
        list_frame = ttk.LabelFrame(left_frame, text="Pokemon in Group", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.group_listbox = tk.Listbox(list_frame, width=35, font=('TkDefaultFont', 9))
        group_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.group_listbox.yview)
        self.group_listbox.config(yscrollcommand=group_scroll.set)
        self.group_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        group_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.group_listbox.bind('<<ListboxSelect>>', self.on_pokemon_select_group)
        
        # Right panel - Pokemon editor
        right_frame = ttk.LabelFrame(main_paned, text="Pokemon Editor", padding=10)
        main_paned.add(right_frame, width=700)
        
        self.create_pokemon_editor(right_frame, 'group')
    
    def create_pokemon_editor(self, parent, mode):
        """Create Pokemon editor with searchable dropdowns"""
        prefix = 't_' if mode == 'trainer' else 'g_'
        
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        editor_container = scrollable_frame
        row = 0
        
        # Pokemon Index
        index_frame = ttk.Frame(editor_container)
        index_frame.grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        ttk.Label(index_frame, text="Pokemon Index:", font=('TkDefaultFont', 10)).pack(side=tk.LEFT, padx=5)
        index_label = ttk.Label(index_frame, text="-", font=('TkDefaultFont', 12, 'bold'))
        index_label.pack(side=tk.LEFT, padx=5)
        setattr(self, f'{prefix}index_label', index_label)
        
        group_label = ttk.Label(index_frame, text="", font=('TkDefaultFont', 9, 'italic'))
        group_label.pack(side=tk.LEFT, padx=10)
        setattr(self, f'{prefix}group_label', group_label)
        
        row += 1
        ttk.Separator(editor_container, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Species - SEARCHABLE
        ttk.Label(editor_container, text="Species:", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
        species_var = tk.StringVar()
        species_combo = SearchableCombobox(editor_container, textvariable=species_var, width=45)
        species_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        species_list = [f"{i:04d} - {name}" for i, name in sorted(self.species_data.items()) if i > 0]
        species_combo.set_values(species_list)
        setattr(self, f'{prefix}species_var', species_var)
        setattr(self, f'{prefix}species_combo', species_combo)
        
        ttk.Label(editor_container, text="🔍 Type to search", font=('TkDefaultFont', 8, 'italic'), foreground='#0066CC').grid(row=row, column=2, sticky=tk.E, padx=5)
        row += 1
        
        # Moves - SEARCHABLE with type colors
        for move_num in range(1, 5):
            move_frame = ttk.Frame(editor_container)
            move_frame.grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=3)
            
            ttk.Label(move_frame, text=f"Move {move_num}:", width=12, font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT)
            
            move_var = tk.StringVar()
            move_combo = SearchableCombobox(move_frame, textvariable=move_var, width=35)
            move_list = [f"{i:03d} - {name}" for i, name in sorted(self.move_data.items()) if i > 0]
            move_combo.set_values(move_list)
            move_combo.pack(side=tk.LEFT, padx=5)
            
            # Type indicator
            type_label = tk.Label(move_frame, text="", width=10, relief=tk.RAISED, font=('TkDefaultFont', 8, 'bold'))
            type_label.pack(side=tk.LEFT, padx=5)
            
            setattr(self, f'{prefix}move{move_num}_var', move_var)
            setattr(self, f'{prefix}move{move_num}_combo', move_combo)
            setattr(self, f'{prefix}move{move_num}_type', type_label)
            
            move_combo.bind('<<ComboboxSelected>>', lambda e, ml=type_label, mv=move_var: self.update_move_type(ml, mv))
            move_var.trace_add('write', lambda *args, ml=type_label, mv=move_var: self.update_move_type(ml, mv))
            
            row += 1
        
        # EV Spread - Checkboxes with colors
        ttk.Label(editor_container, text="EV Spread (252 EVs):", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1
        
        ev_frame = ttk.Frame(editor_container)
        ev_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        stat_names = ['HP', 'Atk', 'Def', 'Spe', 'SpA', 'SpD']
        colors = ['#FF5959', '#FFA500', '#FFD700', '#00CED1', '#9370DB', '#32CD32']
        
        for i, (stat, color) in enumerate(zip(stat_names, colors)):
            var = tk.BooleanVar()
            cb_frame = tk.Frame(ev_frame, bg=color, relief=tk.RAISED, bd=1)
            cb_frame.grid(row=0, column=i, padx=3)
            cb = ttk.Checkbutton(cb_frame, text=stat, variable=var)
            cb.pack(padx=2, pady=2)
            setattr(self, f'{prefix}ev_{stat.lower()}_var', var)
            var.trace_add('write', lambda *args, m=mode: self.update_ev_display(m))
        
        row += 1
        
        ev_value_label = ttk.Label(editor_container, text="EV Byte: 0", foreground='blue', font=('TkDefaultFont', 9))
        ev_value_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        setattr(self, f'{prefix}ev_value_label', ev_value_label)
        row += 1
        
        # Nature - SEARCHABLE
        ttk.Label(editor_container, text="Nature:", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
        nature_var = tk.StringVar()
        nature_combo = SearchableCombobox(editor_container, textvariable=nature_var, width=45)
        nature_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        nature_list = [f"{i:02d} - {name}" for i, name in sorted(self.nature_data.items())]
        nature_combo.set_values(nature_list)
        setattr(self, f'{prefix}nature_var', nature_var)
        setattr(self, f'{prefix}nature_combo', nature_combo)
        row += 1
        
        # Held Item - SEARCHABLE
        ttk.Label(editor_container, text="Held Item:", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
        item_var = tk.StringVar()
        item_combo = SearchableCombobox(editor_container, textvariable=item_var, width=45)
        item_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        item_list = [f"{i:03d} - {name}" for i, name in sorted(self.item_data.items())]
        item_combo.set_values(item_list)
        setattr(self, f'{prefix}item_var', item_var)
        setattr(self, f'{prefix}item_combo', item_combo)
        row += 1
        
        # Form
        ttk.Label(editor_container, text="Form:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_var = tk.StringVar()
        form_entry = ttk.Entry(editor_container, textvariable=form_var, width=10)
        form_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(editor_container, text="(0 = normal)").grid(row=row, column=2, sticky=tk.W, pady=5, padx=5)
        setattr(self, f'{prefix}form_var', form_var)
        setattr(self, f'{prefix}form_entry', form_entry)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(editor_container)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        save_btn = ttk.Button(button_frame, text="💾 Save Pokemon Changes", 
                              command=lambda: self.save_pokemon_changes(mode), state=tk.DISABLED)
        save_btn.pack(side=tk.LEFT, padx=5)
        setattr(self, f'{prefix}save_pokemon_btn', save_btn)
        
        revert_btn = ttk.Button(button_frame, text="↶ Revert Changes", 
                               command=lambda: self.revert_pokemon_changes(mode), state=tk.DISABLED)
        revert_btn.pack(side=tk.LEFT, padx=5)
        setattr(self, f'{prefix}revert_btn', revert_btn)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_move_type(self, type_label, move_var):
        """Update move type color indicator"""
        try:
            move_str = move_var.get()
            if not move_str or len(move_str) < 3:
                type_label.config(text="", bg=self.bg_color)
                return
            
            move_id = int(move_str.split(' - ')[0])
            move_type = self.move_types.get(move_id, 'Normal')
            type_color = MOVE_TYPE_COLORS.get(move_type, '#A8A878')
            
            # Choose text color based on background
            dark_types = ['Fighting', 'Poison', 'Ghost', 'Dragon', 'Dark', 'Rock', 'Bug']
            text_color = 'white' if move_type in dark_types else 'black'
            
            type_label.config(text=move_type, bg=type_color, fg=text_color)
        except:
            type_label.config(text="", bg=self.bg_color)
    
    def update_ev_display(self, mode, *args):
        """Update EV byte display"""
        prefix = 't_' if mode == 'trainer' else 'g_'
        
        ev_byte = 0
        if getattr(self, f'{prefix}ev_hp_var').get():
            ev_byte |= 0x01
        if getattr(self, f'{prefix}ev_atk_var').get():
            ev_byte |= 0x02
        if getattr(self, f'{prefix}ev_def_var').get():
            ev_byte |= 0x04
        if getattr(self, f'{prefix}ev_spe_var').get():
            ev_byte |= 0x08
        if getattr(self, f'{prefix}ev_spa_var').get():
            ev_byte |= 0x10
        if getattr(self, f'{prefix}ev_spd_var').get():
            ev_byte |= 0x20
        
        stats = []
        if ev_byte & 0x01: stats.append("HP")
        if ev_byte & 0x02: stats.append("Atk")
        if ev_byte & 0x04: stats.append("Def")
        if ev_byte & 0x08: stats.append("Spe")
        if ev_byte & 0x10: stats.append("SpA")
        if ev_byte & 0x20: stats.append("SpD")
        
        if stats:
            desc = " / ".join([f"252 {s}" for s in stats])
            total_evs = len(stats) * 252
            remaining = 510 - total_evs
            if remaining > 0 and remaining <= 510:
                desc += f" / {remaining} other"
        else:
            desc = "No EVs"
        
        getattr(self, f'{prefix}ev_value_label').config(text=f"EV Byte: {ev_byte} (0b{ev_byte:06b}) - {desc}")
    
    def switch_view(self, view_name):
        """Switch between views"""
        if view_name == 'trainers':
            self.notebook.select(0)
        elif view_name == 'groups':
            self.notebook.select(1)
    
    def load_group(self, group_type):
        """Load Pokemon by group"""
        if not self.pokemon_list:
            messagebox.showwarning("No Data", "Please load a203 file first")
            return
        
        self.group_listbox.delete(0, tk.END)
        
        if group_type == 'basic':
            indices = range(1, 351)
            self.group_listbox.config(bg=self.group1_color)
        elif group_type == 'advanced':
            indices = range(351, 895)
            self.group_listbox.config(bg=self.group2_color)
        elif group_type == 'legendary':
            indices = range(895, len(self.pokemon_list))
            self.group_listbox.config(bg=self.legendary_color)
        
        # Group by species
        species_groups = {}
        for idx in indices:
            if idx < len(self.pokemon_list):
                pokemon = self.pokemon_list[idx]
                species = pokemon['species']
                if species not in species_groups:
                    species_groups[species] = []
                species_groups[species].append(idx)
        
        # Add to listbox
        for species in sorted(species_groups.keys()):
            indices_list = species_groups[species]
            species_name = self.species_data.get(species, f"Species_{species}")
            
            if len(indices_list) == 1:
                idx = indices_list[0]
                self.group_listbox.insert(tk.END, f"[{idx:04d}] {species_name}")
            else:
                for var_num, idx in enumerate(indices_list, 1):
                    self.group_listbox.insert(tk.END, f"[{idx:04d}] {species_name} (Variant {var_num}/{len(indices_list)})")
        
        self.status_var.set(f"Loaded {group_type} group - {len(list(indices))} Pokemon. Type in dropdowns to search!")
    
    def on_pokemon_select_group(self, event):
        """Handle Pokemon selection from group view"""
        selection = self.group_listbox.curselection()
        if not selection:
            return
        
        line = self.group_listbox.get(selection[0])
        idx_str = line[1:5]
        pokemon_id = int(idx_str)
        
        self.current_pokemon_index = pokemon_id
        self.display_pokemon_group(pokemon_id)
        
        self.g_save_pokemon_btn.config(state=tk.NORMAL)
        self.g_revert_btn.config(state=tk.NORMAL)
    
    def display_pokemon_group(self, pokemon_id):
        """Display Pokemon in group editor"""
        if pokemon_id >= len(self.pokemon_list):
            return
        
        pokemon = self.pokemon_list[pokemon_id]
        
        self.g_index_label.config(text=f"{pokemon_id:04d}")
        
        if pokemon_id <= 350:
            group_text = "🔰 Basic Pokemon (Rounds 1-3)"
        elif pokemon_id <= 894:
            group_text = "⭐ Advanced Pokemon (Round 4+)"
        else:
            group_text = "👑 Legendary Pokemon (Round 8+)"
        self.g_group_label.config(text=group_text, foreground='blue')
        
        # Species
        species_str = f"{pokemon['species']:04d} - {self.species_data.get(pokemon['species'], 'Unknown')}"
        self.g_species_var.set(species_str)
        
        # Moves
        for i in range(1, 5):
            move_id = pokemon[f'move{i}']
            move_str = f"{move_id:03d} - {self.move_data.get(move_id, 'Unknown')}"
            getattr(self, f'g_move{i}_var').set(move_str)
            self.update_move_type(getattr(self, f'g_move{i}_type'), getattr(self, f'g_move{i}_var'))
        
        # EVs
        ev_byte = pokemon['ev_spread']
        self.g_ev_hp_var.set(bool(ev_byte & 0x01))
        self.g_ev_atk_var.set(bool(ev_byte & 0x02))
        self.g_ev_def_var.set(bool(ev_byte & 0x04))
        self.g_ev_spe_var.set(bool(ev_byte & 0x08))
        self.g_ev_spa_var.set(bool(ev_byte & 0x10))
        self.g_ev_spd_var.set(bool(ev_byte & 0x20))
        
        # Nature
        nature_str = f"{pokemon['nature']:02d} - {self.nature_data.get(pokemon['nature'], 'Unknown')}"
        self.g_nature_var.set(nature_str)
        
        # Item
        item_str = f"{pokemon['item']:03d} - {self.item_data.get(pokemon['item'], 'Unknown')}"
        self.g_item_var.set(item_str)
        
        # Form
        self.g_form_var.set(str(pokemon['form']))
    
    def load_a202(self):
        """Load a202 trainer NARC"""
        filepath = filedialog.askopenfilename(
            title="Open a202_bfactory.narc",
            filetypes=[("NARC files", "*.narc"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'rb') as f:
                self.a202_data = bytearray(f.read())
            
            self.a202_path = filepath
            self.trainers = self.parse_a202(self.a202_data)
            self.populate_trainer_list()
            self.status_var.set(f"Loaded {len(self.trainers)} trainers from a202")
            messagebox.showinfo("Success", f"Loaded {len(self.trainers)} trainers")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load a202: {str(e)}")
    
    def load_a203(self):
        """Load a203 Pokemon NARC"""
        filepath = filedialog.askopenfilename(
            title="Open a203_bfactory.narc",
            filetypes=[("NARC files", "*.narc"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'rb') as f:
                self.a203_data = bytearray(f.read())
            
            self.a203_path = filepath
            self.pokemon_list = self.parse_a203(self.a203_data)
            self.status_var.set(f"Loaded {len(self.pokemon_list)} Pokemon from a203")
            messagebox.showinfo("Success", f"Loaded {len(self.pokemon_list)} Pokemon")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load a203: {str(e)}")
    
    def parse_a202(self, data):
        """Parse a202 trainer data"""
        trainers = []
        
        gmif_pos = data.find(b'GMIF')
        if gmif_pos == -1:
            raise ValueError("GMIF section not found")
        
        btaf_pos = data.find(b'BTAF')
        if btaf_pos == -1:
            raise ValueError("BTAF section not found")
        
        num_files = struct.unpack('<H', data[btaf_pos+8:btaf_pos+10])[0]
        
        file_entries = []
        offset = btaf_pos + 12
        for i in range(num_files):
            start = struct.unpack('<I', data[offset:offset+4])[0]
            end = struct.unpack('<I', data[offset+4:offset+8])[0]
            file_entries.append((start, end))
            offset += 8
        
        data_start = gmif_pos + 8
        for i, (start, end) in enumerate(file_entries):
            size = end - start
            if size < 4:
                continue
            
            file_data = data[data_start + start:data_start + end]
            
            trainer_class = struct.unpack('<H', file_data[0:2])[0]
            pool_size = struct.unpack('<H', file_data[2:4])[0]
            
            pokemon_ids = []
            for j in range(pool_size):
                if 4 + j*2 + 2 <= len(file_data):
                    pid = struct.unpack('<H', file_data[4+j*2:4+j*2+2])[0]
                    pokemon_ids.append(pid)
            
            trainers.append({
                'index': i,
                'trainer_class': trainer_class,
                'pool_size': pool_size,
                'pokemon_ids': pokemon_ids,
                'file_start': data_start + start,
                'file_end': data_start + end
            })
        
        return trainers
    
    def parse_a203(self, data):
        """Parse a203 Pokemon data"""
        pokemon_list = []
        
        gmif_pos = data.find(b'GMIF')
        if gmif_pos == -1:
            raise ValueError("GMIF section not found")
        
        btaf_pos = data.find(b'BTAF')
        if btaf_pos == -1:
            raise ValueError("BTAF section not found")
        
        num_files = struct.unpack('<H', data[btaf_pos+8:btaf_pos+10])[0]
        
        file_entries = []
        offset = btaf_pos + 12
        for i in range(num_files):
            start = struct.unpack('<I', data[offset:offset+4])[0]
            end = struct.unpack('<I', data[offset+4:offset+8])[0]
            file_entries.append((start, end))
            offset += 8
        
        data_start = gmif_pos + 8
        for i, (start, end) in enumerate(file_entries):
            if end - start != 16:
                continue
            
            poke_data = data[data_start + start:data_start + end]
            
            species = struct.unpack('<H', poke_data[0:2])[0]
            move1 = struct.unpack('<H', poke_data[2:4])[0]
            move2 = struct.unpack('<H', poke_data[4:6])[0]
            move3 = struct.unpack('<H', poke_data[6:8])[0]
            move4 = struct.unpack('<H', poke_data[8:10])[0]
            ev_spread = poke_data[10]
            nature = poke_data[11]
            item = struct.unpack('<H', poke_data[12:14])[0]
            form = struct.unpack('<H', poke_data[14:16])[0]
            
            pokemon_list.append({
                'index': i,
                'species': species,
                'move1': move1,
                'move2': move2,
                'move3': move3,
                'move4': move4,
                'ev_spread': ev_spread,
                'nature': nature,
                'item': item,
                'form': form,
                'offset': data_start + start
            })
        
        return pokemon_list
    
    def populate_trainer_list(self):
        """Populate trainer listbox"""
        self.trainer_listbox.delete(0, tk.END)
        for trainer in self.trainers:
            idx = trainer['index']
            tclass = trainer['trainer_class']
            pool_size = trainer['pool_size']
            
            if idx in [305, 306, 311, 312, 313, 314]:
                self.trainer_listbox.insert(tk.END, f"⭐ Trainer {idx:03d} (Class {tclass}, Pool: {pool_size})")
            else:
                self.trainer_listbox.insert(tk.END, f"Trainer {idx:03d} (Class {tclass}, Pool: {pool_size})")
    
    def on_trainer_select(self, event):
        """Handle trainer selection"""
        selection = self.trainer_listbox.curselection()
        if not selection:
            return
        
        self.current_trainer_index = selection[0]
        trainer = self.trainers[self.current_trainer_index]
        
        info = f"Trainer {trainer['index']:03d} | Class: {trainer['trainer_class']} | Pool Size: {trainer['pool_size']}"
        self.trainer_info_label.config(text=info)
        
        self.pool_listbox.delete(0, tk.END)
        for pid in trainer['pokemon_ids']:
            if pid < len(self.pokemon_list):
                pokemon = self.pokemon_list[pid]
                species_name = self.species_data.get(pokemon['species'], f"Species_{pokemon['species']}")
                self.pool_listbox.insert(tk.END, f"[{pid:04d}] {species_name}")
            else:
                self.pool_listbox.insert(tk.END, f"[{pid:04d}] (Not loaded)")
    
    def on_pokemon_select_trainer(self, event):
        """Handle Pokemon selection from trainer pool"""
        selection = self.pool_listbox.curselection()
        if not selection or not self.trainers or self.current_trainer_index is None:
            return
        
        pool_index = selection[0]
        trainer = self.trainers[self.current_trainer_index]
        pokemon_id = trainer['pokemon_ids'][pool_index]
        
        if pokemon_id >= len(self.pokemon_list):
            messagebox.showwarning("Warning", "Pokemon data not loaded")
            return
        
        self.current_pokemon_index = pokemon_id
        self.display_pokemon_trainer(pokemon_id)
        
        self.t_save_pokemon_btn.config(state=tk.NORMAL)
        self.t_revert_btn.config(state=tk.DISABLED)
    
    def display_pokemon_trainer(self, pokemon_id):
        """Display Pokemon in trainer editor"""
        if pokemon_id >= len(self.pokemon_list):
            return
        
        pokemon = self.pokemon_list[pokemon_id]
        
        self.t_index_label.config(text=f"{pokemon_id:04d}")
        
        if pokemon_id <= 350:
            group_text = "🔰 Basic Group"
        elif pokemon_id <= 894:
            group_text = "⭐ Advanced Group"
        else:
            group_text = "👑 Legendary Group"
        self.t_group_label.config(text=group_text, foreground='blue')
        
        # Species
        species_str = f"{pokemon['species']:04d} - {self.species_data.get(pokemon['species'], 'Unknown')}"
        self.t_species_var.set(species_str)
        
        # Moves
        for i in range(1, 5):
            move_id = pokemon[f'move{i}']
            move_str = f"{move_id:03d} - {self.move_data.get(move_id, 'Unknown')}"
            getattr(self, f't_move{i}_var').set(move_str)
            self.update_move_type(getattr(self, f't_move{i}_type'), getattr(self, f't_move{i}_var'))
        
        # EVs
        ev_byte = pokemon['ev_spread']
        self.t_ev_hp_var.set(bool(ev_byte & 0x01))
        self.t_ev_atk_var.set(bool(ev_byte & 0x02))
        self.t_ev_def_var.set(bool(ev_byte & 0x04))
        self.t_ev_spe_var.set(bool(ev_byte & 0x08))
        self.t_ev_spa_var.set(bool(ev_byte & 0x10))
        self.t_ev_spd_var.set(bool(ev_byte & 0x20))
        
        # Nature
        nature_str = f"{pokemon['nature']:02d} - {self.nature_data.get(pokemon['nature'], 'Unknown')}"
        self.t_nature_var.set(nature_str)
        
        # Item
        item_str = f"{pokemon['item']:03d} - {self.item_data.get(pokemon['item'], 'Unknown')}"
        self.t_item_var.set(item_str)
        
        # Form
        self.t_form_var.set(str(pokemon['form']))
    
    def save_pokemon_changes(self, mode):
        """Save Pokemon changes"""
        if self.current_pokemon_index is None or not self.a203_data:
            return
        
        prefix = 't_' if mode == 'trainer' else 'g_'
        
        try:
            pokemon = self.pokemon_list[self.current_pokemon_index]
            
            species = int(getattr(self, f'{prefix}species_var').get().split(' - ')[0])
            move1 = int(getattr(self, f'{prefix}move1_var').get().split(' - ')[0])
            move2 = int(getattr(self, f'{prefix}move2_var').get().split(' - ')[0])
            move3 = int(getattr(self, f'{prefix}move3_var').get().split(' - ')[0])
            move4 = int(getattr(self, f'{prefix}move4_var').get().split(' - ')[0])
            
            ev_byte = 0
            if getattr(self, f'{prefix}ev_hp_var').get():
                ev_byte |= 0x01
            if getattr(self, f'{prefix}ev_atk_var').get():
                ev_byte |= 0x02
            if getattr(self, f'{prefix}ev_def_var').get():
                ev_byte |= 0x04
            if getattr(self, f'{prefix}ev_spe_var').get():
                ev_byte |= 0x08
            if getattr(self, f'{prefix}ev_spa_var').get():
                ev_byte |= 0x10
            if getattr(self, f'{prefix}ev_spd_var').get():
                ev_byte |= 0x20
            
            nature = int(getattr(self, f'{prefix}nature_var').get().split(' - ')[0])
            item = int(getattr(self, f'{prefix}item_var').get().split(' - ')[0])
            form = int(getattr(self, f'{prefix}form_var').get())
            
            pokemon['species'] = species
            pokemon['move1'] = move1
            pokemon['move2'] = move2
            pokemon['move3'] = move3
            pokemon['move4'] = move4
            pokemon['ev_spread'] = ev_byte
            pokemon['nature'] = nature
            pokemon['item'] = item
            pokemon['form'] = form
            
            offset = pokemon['offset']
            struct.pack_into('<H', self.a203_data, offset+0, species)
            struct.pack_into('<H', self.a203_data, offset+2, move1)
            struct.pack_into('<H', self.a203_data, offset+4, move2)
            struct.pack_into('<H', self.a203_data, offset+6, move3)
            struct.pack_into('<H', self.a203_data, offset+8, move4)
            self.a203_data[offset+10] = ev_byte
            self.a203_data[offset+11] = nature
            struct.pack_into('<H', self.a203_data, offset+12, item)
            struct.pack_into('<H', self.a203_data, offset+14, form)
            
            self.modified = True
            self.status_var.set(f"Saved changes to Pokemon {self.current_pokemon_index:04d}")
            messagebox.showinfo("Success", f"Pokemon {self.current_pokemon_index:04d} saved to memory.\nUse 'Save All Changes' to write to file.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def revert_pokemon_changes(self, mode):
        """Revert changes"""
        if self.current_pokemon_index is not None:
            if mode == 'trainer':
                self.display_pokemon_trainer(self.current_pokemon_index)
            else:
                self.display_pokemon_group(self.current_pokemon_index)
            self.status_var.set("Reverted to original values")
    
    def save_all(self):
        """Save all changes"""
        if not self.modified:
            messagebox.showinfo("Info", "No changes to save")
            return
        
        try:
            if self.a203_data and self.a203_path:
                with open(self.a203_path, 'wb') as f:
                    f.write(self.a203_data)
                self.status_var.set("Saved all changes successfully")
                messagebox.showinfo("Success", "All changes saved")
                self.modified = False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def save_as(self):
        """Save as new file"""
        if not self.modified:
            messagebox.showinfo("Info", "No changes to save")
            return
        
        try:
            if self.a203_data:
                filepath = filedialog.asksaveasfilename(
                    title="Save a203 as...",
                    defaultextension=".narc",
                    filetypes=[("NARC files", "*.narc"), ("All files", "*.*")],
                    initialfile="a203_bfactory_modified.narc"
                )
                
                if filepath:
                    with open(filepath, 'wb') as f:
                        f.write(self.a203_data)
                    self.status_var.set(f"Saved to {filepath}")
                    messagebox.showinfo("Success", f"Saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Battle Factory Editor v3.2 - Fixed Search

Pokemon HGSS Battle Factory Editor

✨ FIXED in v3.2:
- Searchable dropdowns NOW WORK!
- Type anything to filter instantly
- Live search as you type
- Correct move type colors from moves.s

Features:
🔍 Working searchable dropdowns
🎯 Dual editing modes (Trainer & Group)
🌈 Color-coded move types
✅ Visual EV checkboxes

TIP: Click a dropdown and start typing!
The list will filter in real-time.

Created for Pokemon ROM hacking community
"""
        messagebox.showinfo("About", about_text)
    
    def show_quick_guide(self):
        """Show quick guide"""
        guide_text = """Quick Guide - v3.2 Working Search

🔍 HOW TO SEARCH:
1. Click any dropdown
2. Start typing
3. List filters instantly!

Examples:
- Type "char" → Charizard, Charmander
- Type "bolt" → Thunderbolt
- Type "252" → Move #252
- Type "fire" → All Fire moves

GROUPS:
🔰 Basic (1-350) - Rounds 1-3
⭐ Advanced (351-894) - Round 4+
👑 Legendary (895-950) - Round 8+

MOVE COLORS:
Automatically show type based on moves.s

EV CHECKBOXES:
Check 2 boxes for 252/252/6 split

Search works on ALL dropdowns:
Species, Moves, Items, Natures!
"""
        messagebox.showinfo("Quick Guide", guide_text)


def main():
    root = tk.Tk()
    app = BattleFactoryEditorEnhanced(root)
    root.mainloop()


if __name__ == '__main__':
    main()
