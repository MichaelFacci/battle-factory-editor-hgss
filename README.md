# Battle Factory Editor v3.0 - Enhanced Edition 🎨

## What's New in v3.0

### Dual Editing Modes
- **Edit by Trainer** - Original workflow, select trainer then edit their Pokemon
- **Edit by Pokemon Group** - New! Browse Pokemon by difficulty tier

### Visuals
- **Color-coded groups**: Basic (blue), Advanced (orange), Legendary (pink)
- **Move type indicators**: Each move shows its type with Pokemon-style colors
- **EV stat colors**: HP (red), Atk (orange), Def (yellow), Spe (cyan), SpA (purple), SpD (green)
- **Variant labeling**: See "Variant 1/4", "Variant 2/4" etc. for easy identification

### Pokemon Groups
- **🔰 Basic Pokemon** (Indices 1-350): Rounds 1-3, simpler builds
- **⭐ Advanced Pokemon** (Indices 351-894): Round 4+, competitive sets
- **👑 Legendary Pokemon** (Indices 895-950): Round 8+, legendary Pokemon

### Quality of Life
- Group indicators on every Pokemon
- Frontier Brain trainers highlighted (⭐)
- Real-time EV calculation

## Screenshots

<img width="1321" height="1041" alt="image" src="https://github.com/user-attachments/assets/9f0a3dd5-d376-472b-bc3a-3ede6520ea4d" />

<img width="992" height="1046" alt="image" src="https://github.com/user-attachments/assets/8680f9f5-0725-4c25-9df1-53075ddcb078" />





### Edit by Trainer Tab
```
┌─────────────────────────────────────────────────────────────┐
│ [Trainers]      [Pokemon Pool]       [Pokemon Editor]       │
│                                                               │
│ Trainer 001     [0001] Bulbasaur     Index: 0001 🔰 Basic   │
│ Trainer 002     [0002] Charmander    Species: Bulbasaur     │
│ ...             [0003] Squirtle      Move 1: [Tackle] Normal│
│ ⭐ Trainer 305                        Move 2: [Vine Whip] 🌱 │
│                                       EVs: [✓]HP [✓]Atk      │
│                                       Nature: Adamant        │
└─────────────────────────────────────────────────────────────┘
```

### Edit by Pokemon Group Tab
```
┌─────────────────────────────────────────────────────────────┐
│ [Group Selection]         [Pokemon Editor]                   │
│                                                               │
│ ┌─ 🔰 Basic Pokemon ─┐   Index: 0351 ⭐ Advanced            │
│ │   (Rounds 1-3)     │   Species: Venusaur                  │
│ └────────────────────┘   Move 1: [Solar Beam] 🌱 Grass      │
│                           Move 2: [Sludge Bomb] ☠️ Poison    │
│ ┌─ ⭐ Advanced ───────┐   Move 3: [Earthquake] 🏔️ Ground     │
│ │   (Round 4+)       │   Move 4: [Sleep Powder] 🌱 Grass    │
│ └────────────────────┘                                       │
│                           EVs: [✓]HP  [ ]Atk  [ ]Def        │
│ ┌─ 👑 Legendary ──────┐        [ ]Spe [✓]SpA  [✓]SpD        │
│ │   (Round 8+)       │                                       │
│ └────────────────────┘   Nature: Bold                       │
│                           Item: Leftovers                     │
│ [0351] Venusaur (1/4)                                        │
│ [0487] Venusaur (2/4)                                        │
│ [0623] Venusaur (3/4)                                        │
│ [0759] Venusaur (4/4)                                        │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Option 1: Run Python Script
```bash
python battle_factory_editor_v3.py
```

Requirements:
- Python 3.6+
- tkinter (included in most Python installations)

### Option 2: Build Windows Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="BattleFactoryEditor_v3" battle_factory_editor_v3.py
```

Place these files with the .exe:
- `species.csv`
- `moves.csv` (with type column)
- `items.csv`

## Quick Start Guide

### Step 1: Load Files
1. **File → Open a202 (Trainers)**
2. **File → Open a203 (Pokemon)**

### Step 2: Choose Your Workflow

#### Option A: Edit by Trainer
1. Click "Edit by Trainer" tab
2. Select a trainer from the left panel
3. Select a Pokemon from their pool
4. Edit in the right panel

#### Option B: Edit by Pokemon Group
1. Click "Edit by Pokemon Group" tab
2. Click a group button (Basic/Advanced/Legendary)
3. Browse Pokemon with variant labels
4. Edit directly

### Step 3: Edit Pokemon
- **Species**: Choose from dropdown
- **Moves**: Select 4 moves (types shown in color)
- **EVs**: Check boxes for 252 EVs (typically 2 boxes)
- **Nature**: Choose from dropdown
- **Item**: Choose from dropdown
- **Form**: Usually 0 (for regional forms, select species directly)

### Step 4: Save
1. Click "💾 Save Pokemon Changes" (saves to memory)
2. Click "File → Save All Changes" (writes to file)

## Understanding the Groups

### 🔰 Basic Pokemon (1-350)
**When Used**: Rounds 1-3 in Level 50 mode
**Characteristics**:
- 1-2 variants per species
- Simpler movesets
- Early-stage and mid-stage evolutions

### ⭐ Advanced Pokemon (351-894)
**When Used**: Round 4+ in Level 50, Round 1+ in Open Level
**Characteristics**:
- Exactly 4 variants per species
- Competitive movesets
- Fully-evolved Pokemon
- 136 index spacing between variants

**Example**:
- Venusaur variant 1 (Index 351) - Physical
- Venusaur variant 2 (Index 487) - Special
- Venusaur variant 3 (Index 623) - Mixed
- Venusaur variant 4 (Index 759) - Support

### 👑 Legendary Pokemon (895-950)
**When Used**: Round 8+ in Level 50, Round 5+ in Open Level
**Characteristics**:
- Legendary and mythical Pokemon
- 4 variants each
- Highest difficulty
- Top-tier competitive sets

**Example**:
- Articuno (4 variants)
- Zapdos (4 variants)
- Moltres (4 variants)

## Move Type Colors

Moves are color-coded by type for easy team building:

| Type      | Color          | Example Moves          |
|-----------|----------------|------------------------|
| Normal    | Gray           | Tackle, Hyper Beam     |
| Fire      | Orange-Red     | Flamethrower, Fire Blast |
| Water     | Blue           | Surf, Hydro Pump       |
| Grass     | Green          | Solar Beam, Leaf Blade |
| Electric  | Yellow         | Thunderbolt, Thunder   |
| Ice       | Cyan           | Ice Beam, Blizzard     |
| Fighting  | Red-Brown      | Close Combat, Brick Break |
| Poison    | Purple         | Sludge Bomb, Toxic     |
| Ground    | Brown          | Earthquake, Earth Power |
| Flying    | Light Blue     | Brave Bird, Aerial Ace |
| Psychic   | Pink           | Psychic, Psyshock      |
| Bug       | Yellow-Green   | X-Scissor, U-turn      |
| Rock      | Brown-Gray     | Stone Edge, Rock Slide |
| Ghost     | Purple-Gray    | Shadow Ball, Shadow Claw |
| Dragon    | Indigo         | Dragon Claw, Outrage   |
| Dark      | Dark Brown     | Crunch, Dark Pulse     |
| Steel     | Silver-Gray    | Iron Head, Flash Cannon |
| Fairy     | Pink           | Moonblast, Play Rough  |

## EV Checkbox Colors

Each stat has its own color for easy recognition:

| Stat  | Color  | 
|-------|--------|
| HP    | Red    |
| Atk   | Orange |
| Def   | Yellow |
| Spe   | Cyan   |
| SpA   | Purple |
| SpD   | Green  |

**Tip**: Check 2 boxes for the standard 252/252/6 EV split!

## Special Features

### Frontier Brain Highlighting
Trainers 305, 306, 311, 312, 313, 314 are marked with ⭐

These are:
- **Palmer** (305, 306) - Battle Tower
- **Dahlia** (311, 312) - Battle Arcade  
- **Darach** (313, 314) - Battle Castle

### Variant Tracking
In Group Mode, Pokemon with multiple variants show:
```
[0351] Venusaur (Variant 1/4)
[0487] Venusaur (Variant 2/4)
[0623] Venusaur (Variant 3/4)
[0759] Venusaur (Variant 4/4)
```

## Keyboard Shortcuts

- **Ctrl+1**: Switch to Trainer view
- **Ctrl+2**: Switch to Group view
- **Ctrl+S**: Save all changes
- **Ctrl+Q**: Quit

## Credits

Created for the Pokemon ROM hacking community.

Special thanks to:
- HG-Engine developers


---

**Version**: 3.0 Enhanced  
**Date**: December 2024  
**Compatibility**: Pokemon HGSS, HG-Engine
