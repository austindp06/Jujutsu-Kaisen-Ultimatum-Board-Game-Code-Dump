import random
from typing import List, Dict, Optional
# ======================
# === Initial Setup ===
# ======================

special_grade_deck: List[str] = [
    "Toji (SG)", "Seance Toji (SG)", "Mahito (SG)", "Awakened Mahito (SG)",
    "Hanami (SG)", "Jogo (SG)", "Cursed Womb Dagon (SG)", "Evolved Dagon (SG)",
    "Sukuna (SG)", "Gojo (SG)", "Todo (SG)", "Megumi (SG)", "Last Leg Megumi (SG)",
    "Yuji (SG)", "Inumaki (SG)", "Geto (SG)", "Teen Geto (SG)"
]

xp_drops: Dict[str, int] = {
    "G4": 1, "G3": 1, "G2": 3, "G1": 5, "FB": 8,
    "Toji (SG)": 20, "Seance Toji (SG)": 19, "Mahito (SG)": 19,
    "Awakened Mahito (SG)": 18, "Hanami (SG)": 20, "Jogo (SG)": 17,
    "Cursed Womb Dagon (SG)": 15, "Evolved Dagon (SG)": 19, "Sukuna (SG)": 22,
    "Gojo (SG)": 22, "Todo (SG)": 17, "Megumi (SG)": 18, "Last Leg Megumi (SG)": 17,
    "Yuji (SG)": 16, "Inumaki (SG)": 17, "Geto (SG)": 16, "Teen Geto (SG)": 15
}

sg_damage_tracker: Dict[str, Dict[str, int]] = {}
previewed_cards: List[str] = []

binding_vow_deck: List[str] = [
    "Binding Vow of Violence", "Binding Vow of Resilience", "Binding Vow of Swiftness",
    "Binding Vow of Recall", "Binding Vow of Luck", "Binding Vow of Recursion",
    "Binding Vow of Cleansing", "Binding Vow of Substitution",
    "Binding Vow of the Black Flash", "Binding Vow of Cursed Flow",
    "Binding Vow of the Stone Soul", "Binding Vow of Transferral",
    "Binding Vow of Uneasy Peace", "Binding Vow of Leverage"
]

skill_card_deck: List[str] = [
    "Sixth Sense", "Soul Guard", "Bodily Purge", "Reverse Curse Technique",
    "Simple Domain", "Flighty", "Mobile", "Transferral", "Precision",
    "Sudden Reversal", "Hazard Cleanse", "Cursed Surge", "Hasten",
    "Companionship", "Adrenaline Surge"
]

encounter_card_deck: List[str] = [
    "Hidden Shrine", "Meditative State", "Rally Point", "Stealthy Withdrawal",
    "Assistant Draw", "Reassessment", "All-out", "Flyhead Swarm",
    "Prison Realm", "Hostile Rush", "Grade 4 Rush", "Special Grade Strike"
]

rush_cards: Dict[str, str | List[str]] = {
    "G4 Rush": "G4s move 1 tile. Attack if on same space as sorcerer",
    "G3 Rush": "G3s move 1 space. Attack if on same space as sorcerer",
    "G2 Rush": [
        "G2s move 1 space. Attack if in range of sorcerer",
        "G2s move 1 space. Attack if in range of sorcerer",
        "G2s move 1 space. Attack if in range of sorcerer",
        "G2s move 1 space. Attack if in range of sorcerer. Spawn 2 G2s",
        "G2s move 1 space. Attack if in range of sorcerer. Spawn 3 G2s"
    ],
    "G1 Rush": [
        "Redraw", "Redraw",
        "G1s move 1 space. Attack if on same space as sorcerer",
        "G1s move 1 space. Attack if on same space as sorcerer. Spawn 1 G1",
        "G1s move 1 space. Attack if on same space as sorcerer. Spawn 1 G1"
    ],
    "SG Rush": [
        "Redraw", "Redraw", "Redraw",
        "SGs move 1 space. Attack if in range of sorcerer",
        "SGs move 1 space. Attack if in range of sorcerer. Spawn 1 SG"
    ],
    "SG Ambush": "Spawn 1 SG 2 tiles away from highest HP sorcerer",
    "Finger Bearer Rush": "Finger bearers move 1 space. Attack if in range of sorcerer",
    "Finger Bearer Ambush": "Spawn 1 Finger Bearer 2 tiles away from highest HP sorcerer",
    "Horde": "Multiply previous card's spawn rate by 1.5x"
}

squadron_cards: Dict[str, List[str]] = {
    "G4 Squadron": ["4 G4s", "5 G4s", "6 G4s", "7 G4s", "8 G4s"],
    "G3 Squadron": ["3 G3s", "4 G3s", "5 G3s", "6 G3s", "8 G3s"],
    "G2 Squadron": ["2 G2", "3 G2s", "4 G2s", "4 G2s", "5 G2s"],
    "G1 Squadron": ["1 G1", "1 G1", "1 G1", "2 G1s", "2 G1s"],
    "Finger Bearer Squadron": ["Redraw", "1 FB", "1 FB", "2 FB", "2 FB"],
    "SG Squadron": ["Redraw", "50/50 1SG", "1 SG", "1 SG", "2 SGs"]
}

enemy_spawn_deck: List[str] = list(squadron_cards.keys()) + list(rush_cards.keys())
master_enemy_deck = enemy_spawn_deck.copy()

assistant_deck: List[str] = [
    "Shoko", "Yaga", "Granny + Grandson Ogami", "Mechamaru",
    "Kusakabe", "Arata", "Ijichi", "Utahime"
]

assistant_abilities: Dict[str, str] = {
    "Shoko": "Trade 10 CE for 1 HP (5-turn cooldown)",
    "Yaga": "Spawns 3 cursed corpses: next 3 damage absorbed, +1DMG bonus per set of 3 cursed corpses (7-turn cooldown)",
    "Granny + Grandson Ogami": "Revives sorcerer with 25% HP if not killed in a domain.",
    "Mechamaru": "Grants 2 rerolls of actions per turn (3-turn cooldown)",
    "Kusakabe": "Casts simple domain to protect from domain expansions (6-turn cooldown)",
    "Arata": "Protects from environmental/tick damage (always active, no cooldown)",
    "Ijichi": "Casts veil (0/1 tile radius) for 2 turns or until deactivated (5-turn cooldown)",
    "Utahime": "Grants +15 CE regen/turn and +50 CE max (always active, no cooldown)"
}

def refill_special_grade_deck() -> List[str]:
    return special_grade_deck.copy()

def refill_encounter_card_deck() -> List[str]:
    return encounter_card_deck.copy()

current_sg_deck: List[str] = refill_special_grade_deck()
current_encounter_card_deck: List[str] = refill_encounter_card_deck()
sorcerer_pool: List['Sorcerer'] = []

def draw_enemy_card(is_preview: bool = False) -> str:
    global previewed_cards
    global enemy_spawn_deck
    if not enemy_spawn_deck:
        print("Enemy spawn deck is empty. Repopulating deck...")
        enemy_spawn_deck = master_enemy_deck.copy()
        print(f"Deck refilled with {len(enemy_spawn_deck)} cards: {enemy_spawn_deck}")
    # Initialize card to draw
    card = None
    if previewed_cards and not is_preview:
        card_info = previewed_cards.pop(0)
        if "|" in card_info:
            card, sg = card_info.split("|")
            if card not in enemy_spawn_deck:
                print(f"Error: Previewed card {card} not in deck. Drawing randomly.")
                card = random.choice(enemy_spawn_deck)
            else:
                print(f"[Enemy Card Drawn from Preview]: {card}")
                if card in ["SG Rush", "Grade 1"]:
                    print(f"[SG Spawned from Preview]: {sg}")
        else:
            card = card_info
            if card not in enemy_spawn_deck:
                print(f"Error: Previewed card {card} not in deck. Drawing randomly.")
                card = random.choice(enemy_spawn_deck)
            else:
                print(f"[Enemy Card Drawn from Preview]: {card}")
    else:
        card = random.choice(enemy_spawn_deck)
        print(f"\n[{'Preview ' if is_preview else ''}Enemy Card Drawn]: {card}")
    # Remove card from deck if not a preview
    if not is_preview and card in enemy_spawn_deck:
        enemy_spawn_deck.remove(card)
        print(f"((Removed {card} from deck. {len(enemy_spawn_deck)} cards remain.))")
    elif not is_preview:
        print(f"Warning: {card} not found in deck for removal. Deck: {enemy_spawn_deck}")
    # Process card effects
    if card in squadron_cards:
        for line in squadron_cards[card]:
            print(line)
        if card == "Grade 1":
            special_grade_draw(1, is_preview)
    elif card in rush_cards:
        if isinstance(rush_cards[card], list):
            for line in rush_cards[card]:
                print(line)
        else:
            print(rush_cards[card])
        if card == "SG Rush":
            special_grade_draw(1, is_preview)
    return card

def special_grade_draw(count: int = 1, is_preview: bool = False) -> Optional[str]:
    global current_sg_deck
    try:
        for _ in range(count):
            if not current_sg_deck:
                current_sg_deck = refill_special_grade_deck()
            sg = random.choice(current_sg_deck)
            if not is_preview:
                current_sg_deck.remove(sg)
            print(f"[{'Preview ' if is_preview else ''}SG Spawned]: {sg}")
            return sg
    except ValueError:
        print("Invalid input. Enter a number.")
        return None

# ========================
# === Sorcerer Data ===
# ========================


sorcerer_data: Dict[str, Dict] = {
    "Yuji": {
        "hp": 100,
        "move_points": 2,
        "attack_points": 4,
        "dodge_requirement": "3+",
        "grades": {
            "G4": {
                "ce_max": 125,
                "ce_regen": 50,
                "attacks": {"Divergent Fist": 25},  # Damage via IRL dice rolls
                "perks": ["Resilient", "Duelist Strike"]
            },
            "G3": {
                "ce_max": 150,
                "ce_regen": 60,
                "attacks": {"Divergent Fist": 25},  # Damage via IRL dice rolls
                "perks": ["Resilient", "Duelist Strike"]
            },
            "G2": {
                "ce_max": 200,
                "ce_regen": 70,
                "attacks": {"Divergent Fist": 25, "Black Flash": 40},  # Damage via IRL dice rolls
                "perks": ["Resilient", "Duelist Strike"]
            },
            "G1": {
                "ce_max": 250,
                "ce_regen": 85,
                "attacks": {"Divergent Fist": 25, "Black Flash": 40, "Divergent Fist+": 50},  # Damage via IRL dice rolls
                "perks": ["Resilient", "Duelist Strike"]
            },
            "SG": {
                "ce_max": 300,
                "ce_regen": 100,
                "attacks": {
                    "Divergent Fist": 25,
                    "Black Flash": 40,
                    "Divergent Fist+": 50,
                    "Black Flash+": 70
                },  # Damage via IRL dice rolls
                "perks": ["Resilient", "Duelist Strike", "In The Zone"]
            }
        }
    },
    "Nanami": {
            "hp": 100,
            "move_points": 3,
            "attack_points": 4,
            "dodge_requirement": "3+",
            "grades": {
                "G4": {
                    "ce_max": 125,
                    "ce_regen": 50,
                    "attacks": {"Overhead Bash": 25},
                    "perks": ["Duelist Strike"]
                },
                "G3": {
                    "ce_max": 150,
                    "ce_regen": 60,
                    "attacks": {"Overhead Bash": 25, "Forced Weakness": 55},
                    "perks": ["Duelist Strike"]
                },
                "G2": {
                    "ce_max": 200,
                    "ce_regen": 70,
                    "attacks": {"Overhead Bash": 25, "Forced Weakness": 55, "Crippling Blow": 85},
                    "perks": ["Duelist Strike"]
                },
                "G1": {
                    "ce_max": 250,
                    "ce_regen": 85,
                    "attacks": {"Overhead Bash": 25, "Forced Weakness": 55, "Crippling Blow": 85, "Overhead Bash+": 35},
                    "perks": ["Duelist Strike"]
                },
                "SG": {
                    "ce_max": 300,
                    "ce_regen": 100,
                    "attacks": {"Overhead Bash": 25, "Forced Weakness": 55, "Crippling Blow": 85, "Overhead Bash+": 35, "Overtime": 150},
                    "perks": ["Duelist Strike"]
                }
            }
        },
    "Todo": {
        "hp": 100,
        "move_points": 2,
        "attack_points": 4,
        "dodge_requirement": "2+",
        "grades": {
            "G4": {
                "ce_max": 110,
                "ce_regen": 25,
                "attacks": {"Crippling Kick": 25},  # Damage via IRL dice rolls
                "perks": ["Disruptor Defense"]
            },
            "G3": {
                "ce_max": 200,
                "ce_regen": 45,
                "attacks": {"Crippling Kick": 25, "Boogie Woogie": 55},  # Damage via IRL dice rolls
                "perks": ["Disruptor Defense"]
            },
            "G2": {
                "ce_max": 250,
                "ce_regen": 85,
                "attacks": {
                    "Crippling Kick": 25,
                    "Boogie Woogie": 55,
                    "Stone Strike": 60
                },  # Damage via IRL dice rolls
                "perks": ["Disruptor Defense", "Reflex Boogie"]
            },
            "G1": {
                "ce_max": 300,
                "ce_regen": 100,
                "attacks": {
                    "CRippling Kick": 25,
                    "Boogie Woogie": 55,
                    "Stone Strike": 60,
                    "Boogie Woogie+": 55
                },  # Damage via IRL dice rolls
                "perks": ["Disruptor Defense", "Reflex Boogie"]
            },
            "SG": {
                "ce_max": 400,
                "ce_regen": 130,
                "attacks": {
                    "Crippling Kick": 20,
                    "Boogie Woogie": 45,
                    "Stone Strike": 60,
                    "Boogie Woogie+": 50,
                    "530,000 IQ": 275
                },  # Damage via IRL dice rolls
                "perks": ["Disruptor Defense", "Reflex Boogie", "530,000 IQ", "Teleport Support"]
            }
        }
    },
    "Gojo": {
            "hp": 100,
            "move_points": 2,
            "attack_points": 4,
            "dodge_requirement": "2+",
            "grades": {
                "G4": {
                    "ce_max": 110,
                    "ce_regen": 25,
                    "attacks": {"Lapse Blue": 30},
                    "perks": ["Disruptor Defense"]
                },
                "G3": {
                    "ce_max": 200,
                    "ce_regen": 45,
                    "attacks": {"Lapse Blue": 30, "Reversal Red": 50},
                    "perks": ["Disruptor Defense"]
                },
                "G2": {
                    "ce_max": 250,
                    "ce_regen": 85,
                    "attacks": {"Lapse Blue": 30, "Reversal Red": 50, "Hollow Purple": 130},
                    "perks": ["Disruptor Defense"]
                },
                "G1": {
                    "ce_max": 300,
                    "ce_regen": 100,
                    "attacks": {"Lapse Blue": 30, "Reversal Red": 50, "Hollow Purple": 130},
                    "perks": ["Disruptor Defense"]
                },
                "SG": {
                    "ce_max": 400,
                    "ce_regen": 130,
                    "attacks": {"Lapse Blue": 30, "Reversal Red": 50, "Hollow Purple": 130, "Infinite Void": 300},
                    "perks": ["Disruptor Defense", "Infinity"]
                }
            }
        },
    "Panda": {
        "hp": 60,
        "move_points": 2,
        "attack_points": 2,
        "dodge_requirement": "6",
        "grades": {
            "G4": {
                "ce_max": 80,
                "ce_regen": 25,
                "attacks": {"Heavy Blow": 25},  # Damage via IRL dice rolls
                "perks": ["Soul Siblings", "Tank Evade"]  # Corrected perks
            },
            "G3": {
                "ce_max": 120,
                "ce_regen": 35,
                "attacks": {"Heavy Blow": 25, "Fastball": 30},  # Damage via IRL dice rolls
                "perks": ["Soul Siblings", "Tank Evade"]  # Corrected perks
            },
            "G2": {
                "ce_max": 140,
                "ce_regen": 50,
                "attacks": {"Heavy Blow": 25, "Fastball": 30, "Heavy Blow+": 25},  # Damage via IRL dice rolls
                "perks": ["Soul Siblings", "Tank Evade", "Blast Entry"]  # Corrected perks
            },
            "G1": {
                "ce_max": 170,
                "ce_regen": 60,
                "attacks": {
                    "Heavy Blow": 25,
                    "Fastball": 30,
                    "Heavy Blow+": 25,
                    "Leaping Smash": 40
                },  # Damage via IRL dice rolls
                "perks": ["Soul Siblings", "Tank Evade", "Blast Entry"]  # Corrected perks
            },
            "SG": {
                "ce_max": 200,
                "ce_regen": 70,
                "attacks": {
                    "Heavy Blow": 25,
                    "Fastball": 30,
                    "Heavy Blow+": 25,
                    "Leaping Smash": 40
                },  # Damage via IRL dice rolls
                "perks": ["Soul Siblings", "Tank Evade", "Blast Entry"]  # Corrected perks
            }
        }
    },
    "Megumi": {
        "hp": 80,
        "move_points": 2,
        "attack_points": 2,
        "dodge_requirement": "4+",
        "grades": {
            "G4": {
                "ce_max": 120,
                "ce_regen": 35,
                "attacks": {
                    "Jet Black Shadow Sword": 25  # Damage via IRL dice rolls, +2 per Divine Dog
                },
                "perks": ["Summoner Dodge"]
            },
            "G3": {
                "ce_max": 160,
                "ce_regen": 65,
                "attacks": {
                    "Jet Black Shadow Sword": 25,  # Damage via IRL dice rolls, +2 per Divine Dog
                    "Shikigami Summon": 50  # Minimum CE cost (Rabbit Escape)
                },
                "perks": ["Summoner Dodge", "Rabbit Escape", "Nue"]
            },
            "G2": {
                "ce_max": 190,
                "ce_regen": 65,
                "attacks": {
                    "Jet Black Shadow Sword": 25,  # Damage via IRL dice rolls, +2 per Divine Dog
                    "Shikigami Summon": 50,
                    "Shikigami Summon+": 50
                },
                "perks": ["Summoner Dodge", "Rabbit Escape", "Nue", "Toad Ensare", "Divine Dogs"]
            },
            "G1": {
                "ce_max": 230,
                "ce_regen": 75,
                "attacks": {
                    "Jet Black Shadow Sword": 25,  # Damage via IRL dice rolls, +2 per Divine Dog
                    "Shikigami Summon": 50,
                    "Shikigami Summon+": 50,
                    "Subjugation Ritual": 200
                },
                "perks": ["Summoner Dodge", "Rabbit Escape", "Nue", "Toad Ensare", "Divine Dogs"]
            },
            "SG": {
                "ce_max": 325,
                "ce_regen": 90,
                "attacks": {
                    "Jet Black Shadow Sword": 25,  # Damage via IRL dice rolls, +2 per Divine Dog
                    "Shikigami Summon": 50,
                    "Shikigami Summon+": 50,
                    "Subjugation Ritual": 200,
                    "Chimera Shadow Garden": 275
                },
                "perks": ["Summoner Dodge", "Rabbit Escape", "Nue", "Toad Ensare", "Divine Dogs"]
            }
        }
    },
    "Jogo": {
        "hp": 75,
        "move_points": 3,
        "attack_points": 3,
        "dodge_requirement": "4+",
        "grades": {
            "G4": {
                "ce_max": 150,
                "ce_regen": 50,
                "attacks": {
                    "Disaster Flames": 25,  # Damage via IRL dice rolls
                },
                "perks": ["Ranger Rotation", "Controlled Burn"]
            },
            "G3": {
                "ce_max": 180,
                "ce_regen": 60,
                "attacks": {
                    "Disaster Flames": 25,  # Damage via IRL dice rolls
                    "Volcano": 50  # 3 damage to anyone stepping on volcano
                },
                "perks": ["Ranger Rotation", "Controlled Burn"]
            },
            "G2": {
                "ce_max": 210,
                "ce_regen": 70,
                "attacks": {
                    "Disaster Flames": 25,  # Damage via IRL dice rolls
                    "Volcano": 50,  # 3 damage to anyone stepping on volcano
                    "Maximum Meteor": 200  # Damage via IRL dice rolls
                },
                "perks": ["Ranger Rotation", "Controlled Burn"]
            },
            "G1": {
                "ce_max": 250,
                "ce_regen": 80,
                "attacks": {
                    "Disaster Flames": 25,  # Damage via IRL dice rolls
                    "Volcano": 50,  # 3 damage to anyone stepping on volcano
                    "Maximum Meteor": 200  # Damage via IRL dice rolls
                },
                "perks": ["Ranger Rotation", "Controlled Burn"]
            },
            "SG": {
                "ce_max": 300,
                "ce_regen": 100,
                "attacks": {
                    "Disaster Flames": 25,  # Damage via IRL dice rolls
                    "Volcano": 50,  # 3 damage to anyone stepping on volcano
                    "Maximum Meteor": 200,  # Damage via IRL dice rolls
                    "Coffin of the Iron Mountain": 250  # Damage via IRL dice rolls
                },
                "perks": ["Ranger Rotation", "Controlled Burn"]
            }
        }
    },
    "Dagon": {
        "hp": 90,
        "move_points": 2,
        "attack_points": 3,
        "dodge_requirement": "3+",
        "grades": {
            "G4": {
                "ce_max": 120,
                "ce_regen": 30,
                "attacks": {"Disaster Tides": 30},  # Damage via IRL dice rolls
                "perks": []
            },
            "G3": {
                "ce_max": 175,
                "ce_regen": 45,
                "attacks": {"Disaster Tides": 30},  # Damage via IRL dice rolls
                "perks": ["Disaster Metabolism"]
            },
            "G2": {
                "ce_max": 215,
                "ce_regen": 65,
                "attacks": {"Disaster Tides": 30, "Evasive Strike": 65},  # Damage via IRL dice rolls
                "perks": ["Disaster Metabolism"]
            },
            "G1": {
                "ce_max": 250,
                "ce_regen": 85,
                "attacks": {"Disaster Tides": 30, "Evasive Strike": 65, "Slam Combo": 80},  # Damage via IRL dice rolls
                "perks": ["Disaster Metabolism"]
            },
            "SG": {
                "ce_max": 350,
                "ce_regen": 100,
                "attacks": {
                    "Disaster Tides": 30,
                    "Evasive Strike": 65,
                    "Slam Combo": 80,
                    "Horizon of the Captivating Skandha": 300
                },  # Damage via IRL dice rolls
                "perks": ["Disaster Metabolism", "Death Swarm"]  # Death Swarm: Piranhas (1 damage/hit), Eels (1 damage/hit), Giant Isopod (3 damage/hit)
            }
        }
    },
    "Sukuna": {
        "hp": 100,
        "move_points": 2,
        "attack_points": 3,
        "dodge_requirement": "3+",
        "grades": {
            "G4": {
                "ce_max": 120,
                "ce_regen": 30,
                "attacks": {"Dismantle": 30},
                "perks": ["Butcher Budgeting"]
            },
            "G3": {
                "ce_max": 175,
                "ce_regen": 45,
                "attacks": {"Dismantle": 30, "Cleave": 60},
                "perks": ["Butcher Budgeting"]
            },
            "G2": {
                "ce_max": 215,
                "ce_regen": 65,
                "attacks": {"Dismantle": 30, "Cleave": 60, "Dismantle+": 50},
                "perks": ["Butcher Budgeting"]
            },
            "G1": {
                "ce_max": 250,
                "ce_regen": 85,
                "attacks": {"Dismantle": 30, "Cleave": 60, "Dismantle+": 50, "Divine Flame": 100},
                "perks": ["Butcher Budgeting"]
            },
            "SG": {
                "ce_max": 350,
                "ce_regen": 100,
                "attacks": {
                    "Dismantle": 30,
                    "Cleave": 60,
                    "Dismantle+": 50,
                    "Divine Flame": 100,
                    "Malevolent Shrine": 150
                },
                "perks": ["Butcher Budgeting"]
            }
        }
    },
    "Baghead": {
            "hp": 100,
            "move_points": 2,
            "attack_points": 1,
            "dodge_requirement": "4+",
            "grades": {
                "G4": {
                    "ce_max": 120,
                    "ce_regen": 35,
                    "attacks": {
                        "Hand-to-Hand Combat": 15
                    },
                    "perks": ["Summoner Dodge", "Clone Pooling"]
                },
                "G3": {
                    "ce_max": 160,
                    "ce_regen": 50,
                    "attacks": {
                        "Hand-to-Hand Combat": 15,
                        "Clone I": 40
                    },
                    "perks": ["Summoner Dodge", "Clone Pooling"]
                },
                "G2": {
                    "ce_max": 190,
                    "ce_regen": 65,
                    "attacks": {
                        "Hand-to-Hand Combat": 15,
                        "Clone I": 40,
                        "Clone II": 50
                    },
                    "perks": ["Summoner Dodge", "Clone Pooling"]
                },
                "G1": {
                    "ce_max": 230,
                    "ce_regen": 75,
                    "attacks": {
                        "Hand-to-Hand Combat": 15,
                        "Clone I": 40,
                        "Clone II": 50,
                        "Clone III": 60
                    },
                    "perks": ["Summoner Dodge", "Clone Pooling"]
                },
                "SG": {
                    "ce_max": 325,
                    "ce_regen": 90,
                    "attacks": {
                        "Hand-to-Hand Combat": 15,
                        "Clone I": 40,
                        "Clone II": 50,
                        "Clone III": 60,
                        "Clone Maximum": 160
                    },
                    "perks": ["Summoner Dodge", "Clone Pooling"]
                }
            }
        },
    "Choso": {
            "hp": 70,
            "move_points": 3,
            "attack_points": 3,
            "dodge_requirement": "2+",
            "grades": {
                "G4": {
                    "ce_max": 130,
                    "ce_regen": 30,
                    "attacks": {"Piercing Blood": 30},
                    "perks": ["Ranger Rotation"]
                },
                "G3": {
                    "ce_max": 150,
                    "ce_regen": 40,
                    "attacks": {
                        "Piercing Blood": 30,
                        "Blood Meteor": 40
                    },
                    "perks": ["Ranger Rotation"]
                },
                "G2": {
                    "ce_max": 200,
                    "ce_regen": 50,
                    "attacks": {
                        "Piercing Blood": 30,
                        "Blood Meteor": 40,
                        "Piercing Blood+": 45
                    },
                    "perks": ["Ranger Rotation"]
                },
                "G1": {
                    "ce_max": 250,
                    "ce_regen": 60,
                    "attacks": {
                        "Piercing Blood": 30,
                        "Blood Meteor": 40,
                        "Piercing Blood+": 45
                    },
                    "perks": ["Ranger Rotation"]
                },
                "SG": {
                    "ce_max": 300,
                    "ce_regen": 90,
                    "attacks": {
                        "Piercing Blood": 30,
                        "Blood Meteor": 40,
                        "Piercing Blood+": 45,
                        "Blood Rain": 80
                    },
                    "perks": ["Ranger Rotation", "Coagulated Armor"]
                }
            }
        },
    "Hanami": {
            "hp": 130,
            "move_points": 2,
            "attack_points": 2,
            "dodge_requirement": "5+",
            "grades": {
                "G4": {
                    "ce_max": 80,
                    "ce_regen": 25,
                    "attacks": {"Cursed Roots": 20},
                    "perks": ["Tank Evade"]
                },
                "G3": {
                    "ce_max": 120,
                    "ce_regen": 35,
                    "attacks": {
                        "Cursed Roots": 20,
                        "Wooden Wall": 40
                    },
                    "perks": ["Tank Evade"]
                },
                "G2": {
                    "ce_max": 140,
                    "ce_regen": 50,
                    "attacks": {
                        "Cursed Roots": 20,
                        "Wooden Wall": 40,
                        "Root Bridge": 40
                    },
                    "perks": ["Tank Evade"]
                },
                "G1": {
                    "ce_max": 170,
                    "ce_regen": 60,
                    "attacks": {
                        "Cursed Roots": 20,
                        "Wooden Wall": 40,
                        "Root Bridge": 40,
                        "Life Force Beam": 80
                    },
                    "perks": ["Tank Evade"]
                },
                "SG": {
                    "ce_max": 200,
                    "ce_regen": 70,
                    "attacks": {
                        "Cursed Roots": 20,
                        "Wooden Wall": 40,
                        "Root Bridge": 40,
                        "Life Force Beam": 80,
                        "Ceremonial Sea of Light": 200
                    },
                    "perks": ["Tank Evade"]
                }
            }
        },
    "Mahito": {
        "hp": 60,
        "move_points": 3,
        "attack_points": 2,
        "dodge_requirement": "4+",
        "grades": {
            "G4": {
                "ce_max": 120,
                "ce_regen": 35,
                "attacks": {"Transfigured Human": 20},
                "perks": ["Summoner Dodge"]
            },
            "G3": {
                "ce_max": 160,
                "ce_regen": 50,
                "attacks": {
                    "Transfigured Human": 20,
                    "Swift Slash": 50
                },
                "perks": ["Summoner Dodge"]
            },
            "G2": {
                "ce_max": 190,
                "ce_regen": 65,
                "attacks": {
                    "Transfigured Human": 20,
                    "Swift Slash": 50,
                    "Polymorphic Soul Isomer": 50
                },
                "perks": ["Summoner Dodge", "Shape of the Soul"]
            },
            "G1": {
                "ce_max": 230,
                "ce_regen": 75,
                "attacks": {
                    "Transfigured Human": 20,
                    "Swift Slash": 50,
                    "Polymorphic Soul Isomer": 50,
                    "Idle Transfiguration": 100
                },
                "perks": ["Summoner Dodge", "Shape of the Soul"]
            },
            "SG": {
                "ce_max": 325,
                "ce_regen": 90,
                "attacks": {
                    "Transfigured Human": 20,
                    "Swift Slash": 50,
                    "Polymorphic Soul Isomer": 50,
                    "Idle Transfiguration": 100,
                    "Domain Expansion: Self-Embodiment of Perfection": 275
                },
                "perks": ["Summoner Dodge", "Shape of the Soul"]
            }
        }
    },
    "Kamo": {
        "hp": 75,
        "move_points": 3,
        "attack_points": 3,
        "dodge_requirement": "2+",
        "grades": {
            "G4": {
                "ce_max": 130,
                "ce_regen": 30,
                "attacks": {"Blood-Dipped Arrows": 20},
                "perks": ["Ranger Rotation"]
            },
            "G3": {
                "ce_max": 150,
                "ce_regen": 40,
                "attacks": {"Blood-Dipped Arrows": 20},
                "perks": ["Ranger Rotation"]
            },
            "G2": {
                "ce_max": 200,
                "ce_regen": 50,
                "attacks": {
                    "Blood-Dipped Arrows": 20,
                    "Crimson Binding": 55
                },
                "perks": ["Ranger Rotation"]
            },
            "G1": {
                "ce_max": 250,
                "ce_regen": 60,
                "attacks": {
                    "Blood-Dipped Arrows": 20,
                    "Crimson Binding": 55,
                    "Slicing Exorcism": 175
                },
                "perks": ["Ranger Rotation", "Overwatch"]
            },
            "SG": {
                "ce_max": 300,
                "ce_regen": 90,
                "attacks": {
                    "Blood-Dipped Arrows": 20,
                    "Crimson Binding": 55,
                    "Slicing Exorcism": 175,
                    "Flowing Red Scale": 250
                },
                "perks": ["Ranger Rotation", "Overwatch"]
            }
        }
    },
    "default": {
        "hp": 100,
        "move_points": 2,
        "attack_points": 2,
        "dodge_requirement": "3+",
        "grades": {
            "G4": {"ce_max": 100, "ce_regen": 10, "attacks": {}, "perks": []},
            "G3": {"ce_max": 100, "ce_regen": 10, "attacks": {}, "perks": []},
            "G2": {"ce_max": 100, "ce_regen": 10, "attacks": {}, "perks": []},
            "G1": {"ce_max": 100, "ce_regen": 10, "attacks": {}, "perks": []},
            "SG": {"ce_max": 100, "ce_regen": 10, "attacks": {}, "perks": []}
        }
    }
}

# ========================
# === Sorcerer Class ===
# ========================

class Sorcerer:
    def __init__(self, name: str):
        self.name = name
        data = sorcerer_data.get(name, sorcerer_data["default"])
        self.hp: int = data["hp"]
        self.hp_max: int = data["hp"]
        self.default_move_points: int = data["move_points"]
        self.move_points: int = data["move_points"]
        self.default_attack_points: int = data["attack_points"]
        self.attack_points: int = data["attack_points"]
        self.attack_points_current: int = self.attack_points
        self.dodge_requirement: str = data["dodge_requirement"]
        self.grade: str = "G4"
        self.ce_max: int = data["grades"]["G4"]["ce_max"]
        self.ce_regen: int = data["grades"]["G4"]["ce_regen"]
        self.attacks: Dict[str, int] = data["grades"]["G4"]["attacks"]
        self.perks: List[str] = data["grades"]["G4"]["perks"]
        self.skill_cards: List[str] = []
        self.binding_vows: List[str] = []  # Can hold up to 2 Binding Vows
        self.assistant: Optional[str] = None
        self.xp: int = 0
        self.ce: int = 0
        self.shoko_cooldown: int = 0
        self.cursed_flow_turns: int = 0
        self.cursed_corpses: int = 0
        self.yaga_cooldown: int = 0
        self.mechamaru_rerolls: int = 0
        self.mechamaru_cooldown: int = 0
        self.kusakabe_cooldown: int = 0
        self.ijichi_veil_turns: int = 0
        self.ijichi_cooldown: int = 0
        self.lives_remaining: int = 3 if name == "Panda" else 1
        self.is_knocked_out: bool = False
        self.clones = [{"hp": self.hp}] if self.name == "Baghead" else []  # Track Baghead clones
        # Gojo-specific attributes
        self.infinite_void_turns: int = 0
        # Nanami-specific attributes
        self.overtime_turns: int = 0
        # Megumi-specific attributes
        self.active_shikigami: List[Dict[str, any]] = []
        self.dead_shikigami: List[str] = []
        self.mahoraga_active: bool = False
        self.domain_active: bool = False
        self.domain_turns: int = 0
        # Jogo-specific attributes
        self.volcano_active: bool = False
        self.volcano_turns: int = 0
        self.jogo_domain_active: bool = False
        self.jogo_domain_turns: int = 0
        # Dagon-specific attributes
        self.dagon_domain_active: bool = False
        self.dagon_domain_turns: int = 0
        self.death_swarm_shikigami: List[Dict[str, any]] = []
        # Mahito-specific attributes
        self.mahito_domain_turns: int = 0  # Tracks turns remaining for Mahito’s Domain Expansion HP gain
        # Kamo-specific attributes
        self.kamo_red_scale_turns: int = 0  # Tracks turns remaining for Flowing Red Scale
        self.kamo_red_scale_cooldown: int = 0  # Tracks cooldown for Flowing Red Scale

    def use_ranger_rotation(self) -> None:
        """Converts AP to MP at a 1:1 ratio for Rangers with the Ranger Rotation perk."""
        if "Ranger Rotation" not in self.perks:
            print(f"{self.name} does not have Ranger Rotation.")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.attack_points_current < 1:
            print(f"{self.name} has no attack points to convert.")
            return
        try:
            ap_to_convert = int(input(f"{self.name}: How many AP to convert to MP (1-{self.attack_points_current})? "))
            if ap_to_convert < 1 or ap_to_convert > self.attack_points_current:
                print(f"Invalid amount. Enter a number between 1 and {self.attack_points_current}.")
                return
            self.attack_points_current -= ap_to_convert
            self.move_points += ap_to_convert
            print(f"{self.name}: Ranger Rotation -{ap_to_convert} AP (current: {self.attack_points_current}/{self.attack_points}), "
                  f"+{ap_to_convert} MP (current: {self.move_points}).")
        except ValueError:
            print("Invalid input. Enter a number.")

    def use_butcher_budgeting(self) -> None:
        """Converts MP to AP at a 1:1 ratio for Sukuna with the Butcher Budgeting perk."""
        if "Butcher Budgeting" not in self.perks:
            print(f"{self.name} does not have Butcher Budgeting.")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.move_points < 1:
            print(f"{self.name} has no move points to convert.")
            return
        try:
            mp_to_convert = int(input(f"{self.name}: How many MP to convert to AP (1-{self.move_points})? "))
            if mp_to_convert < 1 or mp_to_convert > self.move_points:
                print(f"Invalid amount. Enter a number between 1 and {self.move_points}.")
                return
            self.move_points -= mp_to_convert
            self.attack_points_current += mp_to_convert
            print(f"{self.name}: Butcher Budgeting -{mp_to_convert} MP (current: {self.move_points}), "
                  f"+{mp_to_convert} AP (current: {self.attack_points_current}/{self.attack_points}).")
        except ValueError:
            print("Invalid input. Enter a number.")

    def can_add_skill_card(self) -> bool:
        return len(self.skill_cards) < 2

    def can_add_binding_vow(self, vow: str) -> bool:
        if len(self.binding_vows) >= 1:
            return False
        if vow == "Binding Vow of Recall" and self.name != "Megumi":
            return False
        if vow == "Binding Vow of Luck" and self.name != "Hakari":
            return False
        return True


    def remove_ce(self) -> None:
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot lose CE this turn.")
            return
        print(f"{self.name}’s Current CE: {self.ce}/{self.ce_max}")
        try:
            amount = int(input("Enter CE to remove (or 0 to cancel): "))
            if amount == 0:
                print("CE removal cancelled.")
                return
            if amount < 0:
                print("CE amount must be non-negative.")
                return
            if amount > self.ce:
                print(f"Cannot remove {amount} CE (only have {self.ce} CE).")
                return
            self.ce -= amount
            print(f"Removed {amount} CE from {self.name}. New CE: {self.ce}/{self.ce_max}")
        except ValueError:
            print("Invalid input. Enter a number.")

    def perform_attack  (self) -> None:
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if not self.attacks:
            print(f"{self.name} has no attacks available.")
            return
        if self.attack_points_current <= 0 and not (self.name == "Megumi" and self.domain_turns > 0):
            print(f"{self.name} has no attack points remaining this turn.")
            return
        available_attacks = self.attacks
        if self.name == "Megumi" and "Binding Vow of Recall" in self.binding_vows:
            print(f"{self.name} cannot use non-shikigami attacks due to Binding Vow of Recall.")
            available_attacks = {k: v for k, v in self.attacks.items() if k in ["Shikigami Summon", "Shikigami Summon+"]}
        if not available_attacks:
            print(f"{self.name} has no valid attacks available.")
            return
        print(f"\n{self.name}’s Attacks (Current CE: {self.ce}/{self.ce_max}, "
              f"Attack Points: {self.attack_points_current}/{self.attack_points}):")
        for i, (attack, cost) in enumerate(available_attacks.items(), 1):
            print(f"{i}) {attack} ({cost} CE)")
        if self.name == "Dagon" and self.dagon_domain_active and "Death Swarm" in self.perks:
            print(f"{len(available_attacks) + 1}) Death Swarm (40/60/100 CE)")
        try:
            choice = int(input("Select an attack (or 0 to cancel): ")) - 1
            if choice == -1:
                print("Attack cancelled.")
                return
            if self.name == "Dagon" and choice == len(available_attacks) and self.dagon_domain_active:
                self.spawn_death_swarm()
                return
            if 0 <= choice < len(available_attacks):
                attack, base_cost = list(available_attacks.items())[choice]
                cost = base_cost
                if self.name == "Megumi" and self.domain_turns > 0 and attack in ["Shikigami Summon",
                                                                                  "Shikigami Summon+"]:
                    cost = cost // 2
                    print(f"Chimera Shadow Garden: Shikigami summon cost halved to {cost} CE.")
                if self.ce < cost:
                    print(f"Not enough CE to perform {attack} (need {cost}, have {self.ce}).")
                    return
                if attack == "Coffin of the Iron Mountain":
                    if self.name != "Jogo" or self.grade != "SG":
                        print(f"{self.name} cannot use Coffin of the Iron Mountain (requires Jogo at Special Grade).")
                        return
                    if self.is_knocked_out:
                        print(f"{self.name} is knocked out and cannot act this turn.")
                        return
                    if self.jogo_domain_active:
                        print(f"{self.name}’s Coffin of the Iron Mountain is already active.")
                        return
                    cost = sorcerer_data[self.name]["grades"][self.grade]["attacks"]["Coffin of the Iron Mountain"]
                    if self.ce < cost:
                        print(f"Not enough CE to use Coffin of the Iron Mountain (need {cost}, have {self.ce}).")
                        return
                    self.ce -= cost
                    self.jogo_domain_active = True
                    self.jogo_domain_turns = 3
                    self.attack_points_current -= 1
                    print(
                        f"{self.name} uses Coffin of the Iron Mountain! -{cost} CE (current: {self.ce}/{self.ce_max}), "
                        f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                    print("Domain active for 3 turns: 2 damage to all enemies in 1-tile radius on opening, "
                          "2 damage per enemy movement or attack, +1 damage to Jogo’s attacks and residual fire. "
                          "Allies exempt from negative effects.")
                    return
                if attack == "Horizon of the Captivating Skandha":
                    if self.name != "Dagon" or self.grade != "SG":
                        print(
                            f"{self.name} cannot use Horizon of the Captivating Skandha (requires Dagon at Special Grade).")
                        return
                    if self.is_knocked_out:
                        print(f"{self.name} is knocked out and cannot act this turn.")
                        return
                    if self.dagon_domain_active:
                        print(f"{self.name}’s Horizon of the Captivating Skandha is already active.")
                        return
                    cost = sorcerer_data[self.name]["grades"][self.grade]["attacks"][
                        "Horizon of the Captivating Skandha"]
                    if self.ce < cost:
                        print(f"Not enough CE to use Horizon of the Captivating Skandha (need {cost}, have {self.ce}).")
                        return
                    self.ce -= cost
                    self.dagon_domain_active = True
                    self.dagon_domain_turns = 4
                    self.attack_points_current -= 1
                    self.ce = self.ce_max  # Set CE to max after cost deduction
                    print(
                        f"{self.name} uses Horizon of the Captivating Skandha! -{cost} CE, CE reset to max (current: {self.ce}/{self.ce_max}), "
                        f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                    print("Domain active for 4 turns: CE at max, dodge requirement lowered to 2+, "
                          "Death Swarm available, Disaster Metabolism deactivated. Closes if CE dips below 40.")
                    return
                if attack in ["Clone I", "Clone II", "Clone III", "Clone Maximum"] and self.name == "Baghead":
                    clone_counts = {"Clone I": 2, "Clone II": 3, "Clone III": 4, "Clone Maximum": 5}
                    target_count = clone_counts[attack]
                    if len(self.clones) >= target_count:
                        print(f"{self.name} already has {len(self.clones)} clones, cannot spawn more.")
                        return
                    self.ce -= cost
                    self.attack_points_current -= 1
                    self.add_clone(target_count)
                    print(f"-{cost} CE (current: {self.ce}/{self.ce_max}), "
                          f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                    return
                if attack in ["Shikigami Summon", "Shikigami Summon+"]:
                    max_shikigami = 2 if self.grade in ["G2", "G1", "SG"] else 1
                    active_shikigami = len([s for s in self.active_shikigami if s["name"] not in ["Rabbit Escape", "Nue", "Mahoraga"]])
                    if active_shikigami >= max_shikigami and not (self.domain_turns > 0 and self.dead_shikigami):
                        print(f"{self.name} has reached the shikigami limit ({max_shikigami}).")
                        return
                    available_shikigami = []
                    shikigami_costs = []
                    shikigami_hp = []
                    if "Rabbit Escape" in self.perks:
                        available_shikigami.append("Rabbit Escape")
                        shikigami_costs.append(50)
                        shikigami_hp.append(0)  # Despawns, no HP
                    if "Nue" in self.perks:
                        available_shikigami.append("Nue")
                        shikigami_costs.append(70)
                        shikigami_hp.append(0)  # Despawns, no HP
                    if "Toad Ensare" in self.perks and "Toad Ensare" not in self.dead_shikigami:
                        available_shikigami.append("Toad Ensare")
                        shikigami_costs.append(60)
                        shikigami_hp.append(8)
                    if "Divine Dogs" in self.perks and not all(d in self.dead_shikigami for d in ["Divine Dog 1", "Divine Dog 2"]):
                        available_shikigami.append("Divine Dogs")
                        shikigami_costs.append(110)
                        shikigami_hp.append(5)  # Per dog
                    if self.domain_turns > 0 and self.dead_shikigami:
                        for dead in self.dead_shikigami:
                            if dead == "Toad Ensare" or (dead in ["Divine Dog 1", "Divine Dog 2"] and not all(d in self.dead_shikigami for d in ["Divine Dog 1", "Divine Dog 2"])):
                                if dead not in available_shikigami:
                                    available_shikigami.append(dead)
                                    shikigami_costs.append(60 if dead == "Toad Ensare" else 110)
                                    shikigami_hp.append(8 if dead == "Toad Ensare" else 5)
                    if not available_shikigami:
                        print("No shikigami available to summon.")
                        return
                    print("\nAvailable Shikigami:")
                    for i, (shikigami, shikigami_cost) in enumerate(zip(available_shikigami, shikigami_costs), 1):
                        print(f"{i}) {shikigami} ({shikigami_cost // 2 if self.domain_turns > 0 else shikigami_cost} CE)")
                    shikigami_choice = int(input("Select shikigami (or 0 to cancel): ")) - 1
                    if shikigami_choice == -1:
                        print("Summon cancelled.")
                        return
                    if 0 <= shikigami_choice < len(available_shikigami):
                        shikigami_type = available_shikigami[shikigami_choice]
                        shikigami_cost = shikigami_costs[shikigami_choice] // 2 if self.domain_turns > 0 else shikigami_costs[shikigami_choice]
                        shikigami_hp_value = shikigami_hp[shikigami_choice]
                        if self.ce < shikigami_cost:
                            print(f"Not enough CE to summon {shikigami_type} (need {shikigami_cost}, have {self.ce}).")
                            return
                        self.ce -= shikigami_cost
                        self.attack_points_current -= 1 if not (self.name == "Megumi" and self.domain_turns > 0) else 0
                        if attack == "Infinite Void" and self.name == "Gojo":
                            self.infinite_void_turns = 2
                            print(
                                f"{self.name} activates Infinite Void! Domain active for 2 turns.")
                        elif attack == "Overtime" and self.name == "Nanami":
                            self.overtime_turns = 3
                            print(
                                f"{self.name} activates Overtime! -2 damage taken, +1 dodge requirement for SG enemies (max 6) for 3 turns.")
                        if shikigami_type == "Rabbit Escape":
                            self.move_points = 3
                            self.active_shikigami.append({"name": "Rabbit Escape", "hp": 0, "stun_turns": 0})
                            print(f"{self.name} summons Rabbit Escape! Move points set to 3, allies on tile gain 3 move points, movement unhindered. Despawns at turn end.")
                        elif shikigami_type == "Nue":
                            self.active_shikigami.append({"name": "Nue", "hp": 0, "stun_turns": 0})
                            print(f"{self.name} summons Nue! Roll 1 die IRL for damage to this tile and an adjacent tile. Despawns after attack.")
                        elif shikigami_type == "Toad Ensare":
                            try:
                                stun_turns = int(input("Roll 1 die for Toad Ensare stun duration: "))
                                self.active_shikigami.append({"name": "Toad Ensare", "hp": 8, "stun_turns": stun_turns})
                                if shikigami_type in self.dead_shikigami:
                                    self.dead_shikigami.remove(shikigami_type)
                                print(f"{self.name} summons Toad Ensare! Stuns target for {stun_turns} turns (8 HP).")
                            except ValueError:
                                print("Invalid stun duration. Summon cancelled.")
                                return
                        elif shikigami_type == "Divine Dogs":
                            self.active_shikigami.append({"name": "Divine Dog 1", "hp": 5, "stun_turns": 0})
                            self.active_shikigami.append({"name": "Divine Dog 2", "hp": 5, "stun_turns": 0})
                            if "Divine Dog 1" in self.dead_shikigami:
                                self.dead_shikigami.remove("Divine Dog 1")
                            if "Divine Dog 2" in self.dead_shikigami:
                                self.dead_shikigami.remove("Divine Dog 2")
                            print(f"{self.name} summons Divine Dogs! Two dogs (5 HP each, +4 total damage to Jet Black Shadow Sword).")
                        else:
                            self.active_shikigami.append({"name": shikigami_type, "hp": shikigami_hp_value, "stun_turns": 0})
                            self.dead_shikigami.remove(shikigami_type)
                            print(f"{self.name} revives {shikigami_type} via Chimera Shadow Garden!")
                        print(f"-{shikigami_cost} CE (current: {self.ce}/{self.ce_max})" +
                              (f", -1 attack point (current: {self.attack_points_current}/{self.attack_points})"
                               if self.attack_points_current < self.attack_points else ""))
                    else:
                        print("Invalid shikigami selection.")
                        return
                elif attack == "Subjugation Ritual":
                    if self.grade not in ["G1", "SG"]:
                        print(f"{self.name} must be Grade 1 or higher to use Subjugation Ritual.")
                        return
                    self.active_shikigami.append({"name": "Mahoraga", "hp": 25, "stun_turns": 0})
                    self.mahoraga_active = True
                    self.ce -= cost
                    self.attack_points_current -= 1 if not (self.name == "Megumi" and self.domain_turns > 0) else 0
                    print(f"{self.name} summons Mahoraga via Subjugation Ritual! Attacks G1/SG enemies, then all in line of sight (25 HP, regenerates). -{cost} CE (current: {self.ce}/{self.ce_max})" +
                          (f", -1 attack point (current: {self.attack_points_current}/{self.attack_points})"
                           if self.attack_points_current < self.attack_points else ""))
                elif attack == "Chimera Shadow Garden":
                    if self.grade != "SG":
                        print(f"{self.name} must be Special Grade to use Chimera Shadow Garden.")
                        return
                    self.domain_turns = 2
                    self.domain_active = True
                    self.ce -= cost
                    self.attack_points_current -= 1 if not (self.name == "Megumi" and self.domain_turns > 0) else 0
                    print(f"{self.name} activates Chimera Shadow Garden! Targets in 1-tile radius cannot move for 2 turns, attack limit removed, shikigami costs halved, dead shikigami revived. -{cost} CE (current: {self.ce}/{self.ce_max})" +
                          (f", -1 attack point (current: {self.attack_points_current}/{self.attack_points})"
                           if self.attack_points_current < self.attack_points else ""))
                else:
                    self.ce -= cost
                    self.attack_points_current -= 1 if not (self.name == "Megumi" and self.domain_turns > 0) else 0
                    damage = 0
                    if self.name == "Jogo":
                        if attack == "Disaster Flames":
                            damage = 25
                            if self.jogo_domain_active:
                                damage += 1
                            print(f"{self.name} uses Disaster Flames!, "
                                  f"1 residual fire damage/turn to enemies on tile (allies exempt).")
                        elif attack == "Volcano":
                            self.place_volcano()
                            return
                        elif attack == "Maximum Meteor":
                            damage = 50
                            if self.jogo_domain_active:
                                damage += 1
                            tile = input("Choose target tile for Maximum Meteor: ")
                            print(f"{self.name} uses Maximum Meteor!")
                            return
                    elif self.name == "Dagon":
                        if attack == "Disaster Tides":
                            damage = 25
                            print(f"{self.name} uses Disaster Tides!")
                            if "Disaster Metabolism" in self.perks and not self.dagon_domain_active:
                                try:
                                    curses = int(input("How many G4-G2 curses did Dagon consume? "))
                                    self.use_disaster_metabolism(curses)
                                except ValueError:
                                    print("Invalid input. No curses consumed.")
                        elif attack == "Evasive Strike":
                            damage = 35
                            print(f"{self.name} uses Evasive Strike!")
                        elif attack == "Slam Combo":
                            damage = 40
                            print(f"{self.name} uses Slam Combo!")
                            return
                    elif self.name == "Choso":
                        if attack in ["Piercing Blood", "Blood Meteor", "Piercing Blood+", "Blood Rain"]:
                            print(f"{self.name} uses {attack}!")
                    elif self.name == "Hanami":
                        if attack in ["Cursed Roots", "Wooden Wall", "Root Bridge", "Life Force Beam",
                                      "Ceremonial Sea of Light"]:
                            print(f"{self.name} uses {attack}!")
                    else:
                        damage = cost
                        if self.name == "Megumi" and attack == "Jet Black Shadow Sword" and "Divine Dogs" in self.perks:
                            active_dogs = sum(1 for s in self.active_shikigami if s["name"] in ["Divine Dog 1", "Divine Dog 2"])
                            if active_dogs > 0:
                                print(f"Divine Dogs: +{active_dogs * 2} damage to Jet Black Shadow Sword.")
                        if self.name == "Jogo" and self.jogo_domain_active:
                            damage += 1
                        print(f"{self.name} uses {attack}!")
                    if damage > 0:
                        print(f"-{cost} CE (current: {self.ce}/{self.ce_max}), "
                              f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                        if self.name == "Todo" and attack == "Boogie Woogie+":
                            allies = [s for s in sorcerer_pool if s.name != "Todo" and not s.is_knocked_out]
                            if allies:
                                print("\nSelect an ally to receive a free attack point:")
                                for i, ally in enumerate(allies, 1):
                                    print(
                                        f"{i}) {ally.name} (Current AP: {ally.attack_points_current}/{ally.attack_points})")
                                print(f"{len(allies) + 1}) None")
                                try:
                                    ally_choice = int(input("Choose an ally (or None): ")) - 1
                                    if ally_choice == len(allies):
                                        print("No ally receives the free attack point.")
                                    elif 0 <= ally_choice < len(allies):
                                        target = allies[ally_choice]
                                        can_exceed = target.attack_points_current == target.attack_points
                                        target.attack_points_current += 1
                                        print(
                                            f"{target.name} gains 1 attack point! New AP: {target.attack_points_current}/{target.attack_points}")
                                        if can_exceed and target.attack_points_current > target.attack_points:
                                            print(
                                                f"{target.name}’s attack points exceed maximum due to unused AP this turn.")
                                    else:
                                        print("Invalid selection. No ally receives the free attack point.")
                                except ValueError:
                                    print("Invalid input. No ally receives the free attack point.")
                            else:
                                print("No eligible allies available for the free attack point.")
                if attack == "Transfigured Human":
                    try:
                        num_spawns = int(input(
                            f"How many Transfigured Humans to spawn for {self.name}? (20 CE each, {self.ce} CE available): "))
                        total_cost = 20 * num_spawns
                        if num_spawns < 0:
                            print("Invalid number of spawns. Must be non-negative.")
                            return
                        if total_cost > self.ce:
                            print(
                                f"Not enough CE to spawn {num_spawns} Transfigured Humans ({total_cost} CE needed, {self.ce} available).")
                            return
                        self.ce -= total_cost
                        print(
                            f"{self.name} spawns {num_spawns} Transfigured Humans! -{total_cost} CE (current: {self.ce}/{self.ce_max})")
                    except ValueError:
                        print("Invalid input. Enter a number.")
                        return
                elif attack == "Swift Slash":
                    damage = 50
                    try:
                        hp_heal = int(input(
                            f"How much HP to heal for {self.name} using Swift Slash? (Max {self.hp_max - self.hp}): "))
                        if hp_heal < 0:
                            print("Invalid HP amount. Must be non-negative.")
                            return
                        if hp_heal > self.hp_max - self.hp:
                            print(f"Cannot heal {hp_heal} HP. Max possible is {self.hp_max - self.hp}.")
                            return
                        if self.ce < 50:
                            print(f"Not enough CE for Swift Slash (50 CE needed, {self.ce} available).")
                            return
                        self.hp = min(self.hp + hp_heal, self.hp_max)
                        self.ce -= 50
                        print(
                            f"{self.name} uses Swift Slash, dealing {damage} damage and healing {hp_heal} HP! -50 CE (current: {self.ce}/{self.ce_max})")
                    except ValueError:
                        print("Invalid input. Enter a number.")
                        return
                elif attack == "Domain Expansion: Self-Embodiment of Perfection":
                    if self.ce < 300:
                        print(f"Not enough CE for Domain Expansion (300 CE needed, {self.ce} available).")
                        return
                    self.ce -= 300
                    self.mahito_domain_turns = 2
                    print(
                        f"{self.name} uses Domain Expansion: Self-Embodiment of Perfection! +7 HP for 2 turns. -300 CE (current: {self.ce}/{self.ce_max})")
                if attack == "Blood-Dipped Arrows":
                    try:
                        num_arrows = int(input(
                            f"How many arrows to fire for {self.name}? (1–3, 20 CE each, {self.ce} CE available, 0 to cancel): "))
                        if num_arrows == 0:
                            print("Blood-Dipped Arrows cancelled.")
                            return
                        if num_arrows < 0:
                            print("Invalid number of arrows. Must be non-negative.")
                            return
                        if num_arrows > 3:
                            print("Too many arrows to fire at once. Choose 1–3 arrows.")
                            return
                        total_cost = 20 * num_arrows
                        if total_cost > self.ce:
                            print(
                                f"Not enough CE to fire {num_arrows} arrows ({total_cost} CE needed, {self.ce} available).")
                            return
                        self.ce -= total_cost
                        print(
                            f"{self.name} fires {num_arrows} Blood-Dipped Arrows! -{total_cost} CE (current: {self.ce}/{self.ce_max})")
                    except ValueError:
                        print("Invalid input. Enter a number.")
                        return
                elif attack == "Flowing Red Scale":
                    if self.ce < 250:
                        print(f"Not enough CE for Flowing Red Scale (250 CE needed, {self.ce} available).")
                        return
                    if self.kamo_red_scale_cooldown > 0:
                        print(f"Flowing Red Scale is on cooldown for {self.kamo_red_scale_cooldown} more turns.")
                        return
                    self.ce = self.ce_max
                    self.kamo_red_scale_turns = 2
                    self.kamo_red_scale_cooldown = 5  # 2 turns active + 3 turns cooldown
                    print(
                        f"{self.name} uses Flowing Red Scale! CE restored to max ({self.ce}/{self.ce_max}), active for 2 turns.")
                    print("Reminder: Apply other Flowing Red Scale benefits manually IRL.")
            else:
                print("Invalid attack selection.")
        except ValueError:
            print("Invalid input. Enter a number.")

    def use_blast_entry(self) -> None:
        if self.name != "Panda" or self.grade not in ["G2", "G1", "SG"]:
            print(f"{self.name} cannot use Blast Entry (requires Panda at G2 or higher).")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.ce < 40:
            print(f"Not enough CE to use Blast Entry (need 40, have {self.ce}).")
            return
        self.ce -= 40
        print(f"{self.name} uses Blast Entry! -40 CE (current: {self.ce}/{self.ce_max}).")
        print("Reminder: Create a new permanent path IRL by crashing through a wall.")

    def summon_shikigami(self) -> None:
        if self.name != "Megumi":
            print(f"{self.name} cannot summon shikigami.")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        max_shikigami = 1 if self.grade == "G3" else 3 if self.grade in ["G1", "SG"] else 2
        if len(self.active_shikigami) >= max_shikigami:
            print(f"{self.name} has reached the shikigami limit ({max_shikigami}).")
            return
        available_shikigami = []
        if "Rabbit Escape" in self.perks:
            available_shikigami.append(("Rabbit Escape", 50 if not self.domain_active else 25))
        if "Nue" in self.perks and "Nue" not in self.dead_shikigami:
            available_shikigami.append(("Nue", 70 if not self.domain_active else 35))
        if "Toad Ensnare" in self.perks and "Toad Ensnare" not in self.dead_shikigami:
            available_shikigami.append(("Toad Ensnare", 60 if not self.domain_active else 30))
        if "Divine Dogs" in self.perks and "Divine Dogs" not in self.dead_shikigami:
            available_shikigami.append(("Divine Dogs", 110 if not self.domain_active else 55))
        if not available_shikigami:
            print(f"{self.name} has no available shikigami to summon.")
            return
        print(f"\n{self.name}’s Available Shikigami (Current CE: {self.ce}/{self.ce_max}):")
        for i, (shikigami, cost) in enumerate(available_shikigami, 1):
            print(f"{i}) {shikigami} ({cost} CE)")
        try:
            choice = int(input("Select a shikigami to summon (or 0 to cancel): ")) - 1
            if choice == -1:
                print("Summon cancelled.")
                return
            if 0 <= choice < len(available_shikigami):
                shikigami, cost = available_shikigami[choice]
                if self.ce < cost:
                    print(f"Not enough CE to summon {shikigami} (need {cost}, have {self.ce}).")
                    return
                self.ce -= cost
                if shikigami == "Rabbit Escape":
                    self.active_shikigami.append({"name": "Rabbit Escape", "hp": 0, "stun_turns": 0})
                    self.move_points = 3
                    print(f"{self.name} summons Rabbit Escape! -{cost} CE (current: {self.ce}/{self.ce_max}).")
                    print("MP set to 3 for Megumi and allies on tile. Enemies cannot hinder escape.")
                elif shikigami == "Nue":
                    self.active_shikigami.append({"name": "Nue", "hp": 0, "stun_turns": 0})
                    damage = random.randint(1, 6)
                    tile = input("Choose adjacent tile for Nue’s attack (e.g., north, south): ")
                    print(f"{self.name} summons Nue! -{cost} CE (current: {self.ce}/{self.ce_max}).")
                    print(f"Nue deals {damage} damage to Megumi’s tile and {tile}.")
                elif shikigami == "Toad Ensnare":
                    stun_turns = random.randint(1, 6)
                    self.active_shikigami.append({"name": "Toad Ensnare", "hp": 8, "stun_turns": stun_turns})
                    target = input("Choose target to stun: ")
                    print(f"{self.name} summons Toad Ensnare! -{cost} CE (current: {self.ce}/{self.ce_max}).")
                    print(f"Toad stuns {target} for {stun_turns} turns (8 HP).")
                elif shikigami == "Divine Dogs":
                    self.active_shikigami.append({"name": "Divine Dogs", "hp": 5, "stun_turns": 0})
                    self.active_shikigami.append({"name": "Divine Dogs", "hp": 5, "stun_turns": 0})
                    print(f"{self.name} summons Divine Dogs! -{cost} CE (current: {self.ce}/{self.ce_max}).")
                    print("Two dogs summoned (5 HP each), each adding +2 damage to attacks.")
                if not self.domain_active:
                    self.attack_points_current -= 1
                    print(f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
            else:
                print("Invalid shikigami selection.")
        except ValueError:
            print("Invalid input. Enter a number.")

    def use_subjugation_ritual(self) -> None:
        if self.name != "Megumi" or self.grade not in ["G1", "SG"]:
            print(f"{self.name} cannot use Subjugation Ritual (requires Megumi at G1 or higher).")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.mahoraga_active:
            print(f"{self.name} already has Mahoraga active.")
            return
        if "Binding Vow of Recall" in self.binding_vows:
            print(f"{self.name} cannot summon Mahoraga due to Binding Vow of Recall.")
            return
        cost = 200
        if self.ce < cost:
            print(f"Not enough CE to use Subjugation Ritual (need {cost}, have {self.ce}).")
            return
        self.ce -= cost
        self.mahoraga_active = True
        self.attack_points_current -= 1
        print(f"{self.name} uses Subjugation Ritual! -{cost} CE (current: {self.ce}/{self.ce_max}), "
              f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
        print("Mahoraga summoned (25 HP, 10 damage/hit, 1 AP, 1 MP). Targets G1/SG enemies in 1-tile radius, "
              "then closest G1/SG/sorcerer. Regenerates unless one-shot. Adapts to domain debuffs after 1 turn.")

    def use_chimera_shadow_garden(self) -> None:
        if self.name != "Megumi" or self.grade != "SG":
            print(f"{self.name} cannot use Chimera Shadow Garden (requires Megumi at Special Grade).")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.domain_active:
            print(f"{self.name}’s Chimera Shadow Garden is already active.")
            return
        cost = 275
        if self.ce < cost:
            print(f"Not enough CE to use Chimera Shadow Garden (need {cost}, have {self.ce}).")
            return
        self.ce -= cost
        self.domain_active = True
        self.domain_turns = 2
        self.attack_points_current -= 1
        print(f"{self.name} uses Chimera Shadow Garden! -{cost} CE (current: {self.ce}/{self.ce_max}), "
              f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
        print("Domain active for 2 turns: enemies in 1-tile radius immobilized, allies move freely, "
              "Megumi ignores AP limit, shikigami CE costs halved, dead shikigami available.")

    def place_volcano(self) -> None:
        if self.name != "Jogo" or self.grade not in ["G3", "G2", "G1", "SG"]:
            print(f"{self.name} cannot use Volcano (requires Jogo at G3 or higher).")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        if self.volcano_active:
            print(f"{self.name} already has an active volcano.")
            return
        cost = 50
        print(f"Before Volcano CE deduction: CE = {self.ce}")
        if self.ce < cost:
            print(f"Not enough CE to use Volcano (need {cost}, have {self.ce}).")
            return
        # CE deduction moved to perform_attack to avoid double subtraction
        self.volcano_active = True
        self.volcano_turns = 2
        # AP deduction moved to perform_attack
        tile = input("Choose tile to place Volcano (e.g., current, north): ")
        print(f"{self.name} places Volcano on {tile}! Volcano active for 2 turns, damages enemies that touch the tile.")

    def use_disaster_metabolism(self, curses_consumed: int) -> None:
        if self.name != "Dagon" or self.grade not in ["G3", "G2", "G1", "SG"]:
            print(f"{self.name} cannot use Disaster Metabolism (requires Dagon at G3 or higher).")
            return
        if self.dagon_domain_active:
            print(f"{self.name} cannot use Disaster Metabolism while Horizon of the Captivating Skandha is active.")
            return
        if curses_consumed <= 0:
            print("No curses consumed. Disaster Metabolism not applied.")
            return
        print(f"{self.name} consumed {curses_consumed} G4-G2 curses with Disaster Tides.")
        for _ in range(curses_consumed):
            choice = input("Choose benefit for one curse (hp for +1 HP, ce for +2 CE): ").lower()
            if choice == "hp" and self.hp < self.hp_max:
                self.hp = min(self.hp + 1, self.hp_max)
                print(f"{self.name} gains 1 HP (current: {self.hp}/{self.hp_max}).")
            elif choice == "ce" and self.ce < self.ce_max:
                self.ce = min(self.ce + 2, self.ce_max)
                print(f"{self.name} gains 2 CE (current: {self.ce}/{self.ce_max}).")
            else:
                print(f"Invalid choice or limit reached (HP: {self.hp}/{self.hp_max}, CE: {self.ce}/{self.ce_max}).")

    def spawn_death_swarm(self) -> None:
        if self.name != "Dagon" or not self.dagon_domain_active:
            print(f"{self.name} cannot use Death Swarm (requires Dagon in Horizon of the Captivating Skandha).")
            return
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        available_shikigami = [
            ("Piranha (3x)", 40, {"type": "Piranha", "hp": 1, "damage": 1, "mp": 1}),
            ("Eel", 60, {"type": "Eel", "hp": 2, "damage": 1, "mp": 2}),
            ("Giant Isopod", 100, {"type": "Giant Isopod", "hp": 8, "damage": 3, "mp": 1})
        ]
        print(f"\n{self.name}’s Death Swarm Options (Current CE: {self.ce}/{self.ce_max}):")
        for i, (name, cost, _) in enumerate(available_shikigami, 1):
            print(f"{i}) {name} ({cost} CE)")
        try:
            choice = int(input("Select shikigami to spawn (or 0 to cancel): ")) - 1
            if choice == -1:
                print("Spawn cancelled.")
                return
            if 0 <= choice < len(available_shikigami):
                name, cost, shikigami_base = available_shikigami[choice]
                if self.ce < cost:
                    print(f"Not enough CE to spawn {name} (need {cost}, have {self.ce}).")
                    return
                self.ce -= cost
                self.attack_points_current -= 1
                tile = input("Choose tile in domain for spawning (not SG enemy tile unless SG in Dagon’s tile): ")
                if name.startswith("Piranha"):
                    for _ in range(3):
                        self.death_swarm_shikigami.append({**shikigami_base, "tile": tile})
                    print(f"{self.name} spawns 3 Piranhas (1 HP, 1 damage, 1 MP each) on {tile}! "
                          f"-{cost} CE (current: {self.ce}/{self.ce_max}), "
                          f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                else:
                    self.death_swarm_shikigami.append({**shikigami_base, "tile": tile})
                    print(f"{self.name} spawns {name} ({shikigami_base['hp']} HP, {shikigami_base['damage']} damage, "
                          f"{shikigami_base['mp']} MP) on {tile}! -{cost} CE (current: {self.ce}/{self.ce_max}), "
                          f"-1 attack point (current: {self.attack_points_current}/{self.attack_points}).")
                print("Enemy dodge requirements raised to 5+ in domain.")
            else:
                print("Invalid shikigami selection.")
        except ValueError:
            print("Invalid input. Enter a number.")

    def adjust_clone_hp(self, new_clone_count):
        if self.name != "Baghead" or "Clone Pooling" not in self.perks:
            return
        total_hp = sum(clone["hp"] for clone in self.clones)
        target_hp = {2: 50, 3: 33, 4: 25, 5: 20}.get(new_clone_count, 100)
        # Distribute HP to approach target_hp without healing
        desired_total = min(total_hp, 100)  # Cap at 100
        base_hp = desired_total // new_clone_count
        remainder = desired_total % new_clone_count
        new_hp_values = [base_hp + (1 if i < remainder else 0) for i in range(new_clone_count)]
        # Assign HP, only reducing to prevent healing
        for clone, new_hp in zip(self.clones, new_hp_values):
            clone["hp"] = min(clone["hp"], new_hp)
        # Ensure total HP <= 100
        total_hp = sum(clone["hp"] for clone in self.clones)
        if total_hp > 100:
            excess = total_hp - 100
            sorted_clones = sorted(self.clones, key=lambda x: x["hp"], reverse=True)
            for clone in sorted_clones:
                reduction = min(clone["hp"], excess)
                clone["hp"] -= reduction
                excess -= reduction
                if excess <= 0:
                    break
        print(f"Clone HP adjusted: {[clone['hp'] for clone in self.clones]}")

    def add_clone(self, clone_count):
        if self.name != "Baghead" or "Clone Pooling" not in self.perks:
            return
        current_clones = len(self.clones)
        if current_clones >= clone_count:
            print(f"Cannot spawn clone: Already at {current_clones} clones.")
            return
        target_hp = {2: 50, 3: 33, 4: 25, 5: 20}.get(clone_count, 100)
        for _ in range(current_clones, clone_count):
            self.clones.append({"hp": target_hp})  # Initialize with target HP
            self.move_points += 1
            self.attack_points += 1
            self.attack_points_current += 1
        self.adjust_clone_hp(clone_count)
        print(f"{self.name} spawns clone(s). Total clones: {len(self.clones)}, "
              f"MP: {self.move_points}, AP: {self.attack_points_current}/{self.attack_points}")

    def remove_clone(self):
        if self.name != "Baghead" or not self.clones:
            return
        self.clones.pop()
        self.move_points = max(1, self.move_points - 1)
        self.attack_points = max(1, self.attack_points - 1)
        self.attack_points_current = max(1, self.attack_points_current - 1)
        self.adjust_clone_hp(len(self.clones))
        print(f"Clone removed. Total clones: {len(self.clones)}, "f"MP: {self.move_points}, AP: {self.attack_points_current}/{self.attack_points}")

    def reset_attack_points(self) -> None:
        self.attack_points_current = self.attack_points
        if self.name == "Megumi":
            # Despawn Rabbit Escape at turn end
            self.active_shikigami = [s for s in self.active_shikigami if s["name"] != "Rabbit Escape"]
            # Update stun turns for Toad Ensnare
            for shikigami in self.active_shikigami:
                if shikigami["name"] == "Toad Ensnare" and shikigami["stun_turns"] > 0:
                    shikigami["stun_turns"] -= 1
                    if shikigami["stun_turns"] == 0:
                        print(f"{self.name}’s Toad Ensnare stun effect has ended.")
            # Manage Chimera Shadow Garden duration
            if self.domain_active:
                self.domain_turns -= 1
                if self.domain_turns <= 0:
                    self.domain_active = False
                    print(f"{self.name}’s Chimera Shadow Garden has closed.")
                    # Revert dead shikigami to unavailable
                    available_shikigami = ["Rabbit Escape", "Nue", "Toad Ensnare", "Divine Dogs"]
                    self.dead_shikigami = [s for s in available_shikigami if s in self.dead_shikigami]
        if self.name == "Jogo":
            # Manage Volcano duration
            if self.volcano_active:
                self.volcano_turns -= 1
                if self.volcano_turns <= 0:
                    self.volcano_active = False
                    print(f"{self.name}’s Volcano has expired.")
            # Manage Coffin of the Iron Mountain duration
            if self.jogo_domain_active:
                self.jogo_domain_turns -= 1
                if self.jogo_domain_turns <= 0:
                    self.jogo_domain_active = False
                    print(f"{self.name}’s Coffin of the Iron Mountain has closed.")
        if self.name == "Dagon":
            # Manage Horizon of the Captivating Skandha duration
            if self.dagon_domain_active:
                if self.ce < 40:
                    self.dagon_domain_active = False
                    self.dagon_domain_turns = 0
                    self.death_swarm_shikigami = []
                    print(f"{self.name}’s Horizon of the Captivating Skandha closes (CE below 40).")
                else:
                    self.dagon_domain_turns -= 1
                    if self.dagon_domain_turns <= 0:
                        self.dagon_domain_active = False
                        self.death_swarm_shikigami = []
                        print(f"{self.name}’s Horizon of the Captivating Skandha has closed.")

    def preview_enemy_turn(self) -> None:
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot act this turn.")
            return
        global previewed_cards
        if self.name != "Todo" or self.grade != "SG":
            print(f"{self.name} cannot use 530,000 IQ (requires Todo at Special Grade).")
            return
        print(f"\n{self.name} uses 530,000 IQ! Previewing next enemy turn (no effects applied):")
        previewed_cards.clear()
        while True:
            card = draw_enemy_card(is_preview=True)
            if card in ["SG Rush", "Grade 1"] and special_grade_deck:
                sg = special_grade_draw(1, is_preview=True)
                if sg:
                    previewed_cards.append(f"{card}|{sg}")
                else:
                    previewed_cards.append(card)
            else:
                previewed_cards.append(card)
            more = input("\nPreview another card? (y/n): ").lower()
            if more != 'y':
                break
        print(f"Previewed cards locked in: {previewed_cards}")

    def take_damage(self, damage: int) -> bool:
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot take damage this turn.")
            return False
        if self.cursed_corpses > 0:
            self.cursed_corpses -= 1
            print(f"{self.name}: Yaga’s cursed corpse absorbs 1 damage!"
                  f"{self.cursed_corpses} corpses remain.")
            print(f"Reminder: Remove +1 DMG bonus for this corpse.")
            return False
        if self.name == "Baghead" and self.clones:
            print("Select clone to take damage:")
            for i, clone in enumerate(self.clones, 1):
                print(f"{i}) Clone {i} (HP: {clone['hp']})")
            try:
                clone_idx = int(input("Choose clone (1-{}): ".format(len(self.clones)))) - 1
                if not 0 <= clone_idx < len(self.clones):
                    print("Invalid clone selection. No damage applied.")
                    return False
                target_clone = self.clones[clone_idx]
                effective_damage = damage
                target_clone["hp"] -= effective_damage
                print(
                    f"{self.name} clone {clone_idx + 1} takes {effective_damage} damage. Clone HP: {target_clone['hp']}")
                if target_clone["hp"] <= 0:
                    self.remove_clone()
                    self.adjust_clone_hp(len(self.clones))  # Only adjust HP after clone removal
                if self.clones:
                    print(f"Clone HP: {[clone['hp'] for clone in self.clones]}")
                if self.assistant == "Arata":
                    print(f"Reminder: Arata protects {self.name} from environmental/tick damage "
                          f"(e.g., cursed buds, fire). Adjust damage if applicable.")
                if not self.clones:
                    print(f"{self.name} has no clones left and is knocked out!")
                    self.is_knocked_out = True
                    if self.assistant == "Granny + Grandson Ogami":
                        domain = input(f"Did {self.name} die in a domain? (y/n): ").lower()
                        if domain == "n":
                            self.clones = [{"hp": 25}]
                            self.hp = 25
                            self.hp_max = 100
                            self.is_knocked_out = False
                            self.assistant = None
                            print(f"{self.name} is revived by Granny + Grandson Ogami with 25 HP (1 clone)!")
                            return False
                    print(f"{self.name} has died!")
                    return True
                return False
            except ValueError:
                print("Invalid input. No damage applied.")
                return False
        self.hp = max(0, self.hp - damage)
        if self.name == "Nanami" and self.overtime_turns > 0:
            print(f"Overtime active ({self.overtime_turns} remain): Subtract 2 from damage taken.")
        print(f"{self.name} takes {damage} damage. New HP: {self.hp}/{self.hp_max}")
        if self.assistant == "Arata":
            print(f"Reminder: Arata protects {self.name} from environmental/tick damage "
                  f"(e.g., cursed buds, fire). Adjust damage if applicable.")
        if self.hp <= 0:
            if self.name == "Panda" and self.lives_remaining > 1:
                self.lives_remaining -= 1
                self.is_knocked_out = True
                self.hp = 50 if self.lives_remaining == 2 else 40
                self.hp_max = self.hp
                print(f"{self.name} is knocked out! Revives next turn with {self.hp} HP "
                      f"({self.lives_remaining} lives remain).")
                return False
            if self.assistant == "Granny + Grandson Ogami":
                domain = input(f"Did {self.name} die in a domain? (y/n): ").lower()
                if domain == "n":
                    self.hp = 25
                    self.hp_max = 100
                    self.assistant = None
                    print(f"{self.name} is revived by Granny + Grandson Ogami with 25 HP!")
                    return False
                print(f"{self.name} has died!")
                return True
        return False

    def gain_ce(self) -> None:
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot gain CE this turn.")
            return
        regen = self.ce_regen
        if self.cursed_flow_turns > 0:
            if self.cursed_flow_turns <= 3:
                regen *= 2
                print(f"{self.name}: Binding Vow of Cursed Flow - Double CE regen ({regen})")
            else:
                regen //= 2
                print(f"{self.name}: Binding Vow of Cursed Flow - Half CE regen ({regen})")
            self.cursed_flow_turns = (self.cursed_flow_turns % 6) + 1
        self.ce = min(self.ce + regen, self.ce_max)

    def level_up(self) -> None:
        """
        Promotes the sorcerer to the next grade if XP thresholds are met, handling multiple promotions.
        """
        thresholds = {"G4": 18, "G3": 54, "G2": 99, "G1": 120}
        grades = ["G4", "G3", "G2", "G1", "SG"]
        while True:
            current_index = grades.index(self.grade)
            next_grade = grades[current_index + 1] if current_index < len(grades) - 1 else None
            if not next_grade or self.xp < thresholds.get(self.grade, float('inf')):
                break
            self.grade = next_grade
            data = sorcerer_data.get(self.name, sorcerer_data["default"])
            self.ce_max = data["grades"][self.grade]["ce_max"]
            self.ce_regen = data["grades"][self.grade]["ce_regen"]
            self.attacks = data["grades"][self.grade]["attacks"]
            self.perks = data["grades"][self.grade]["perks"]
            self.ce = min(self.ce, self.ce_max)
            if self.name == "Panda":
                self.hp_max = 60 if self.lives_remaining == 3 else 50 if self.lives_remaining == 2 else 40
                self.hp = min(self.hp, self.hp_max)
            print(f"{self.name} has been promoted to {self.grade}!")

    def show_info(self) -> None:
        print(f"\n{self.name}’s Status:")
        print(f"Grade: {self.grade}")
        print(f"HP: {self.hp}/{self.hp_max}")
        print(f"CE: {self.ce}/{self.ce_max} (Regen: {self.ce_regen}/turn)")
        print(f"Move Points: {self.move_points}")
        print(f"Attack Points: {self.attack_points_current}/{self.attack_points}")
        print(f"Dodge Requirement: {self.dodge_requirement}")
        print(f"XP: {self.xp}")
        print(f"Attacks: {', '.join(f'{k} ({v} CE)' for k, v in self.attacks.items())}")
        print(f"Perks: {', '.join(self.perks) or 'None'}")
        print(f"Skill Cards: {', '.join(self.skill_cards) or 'None'}")
        print(f"Binding Vows: {', '.join(self.binding_vows) or 'None'}")
        print(f"Assistant: {self.assistant or 'None'}")
        if self.name == "Panda":
            print(f"Lives Remaining: {self.lives_remaining}")
        if self.name == "Megumi":
            print(f"Active Shikigami: {', '.join(s['name'] for s in self.active_shikigami) or 'None'}")
            print(f"Dead Shikigami: {', '.join(self.dead_shikigami) or 'None'}")
            print(f"Mahoraga Active: {self.mahoraga_active}")
            print(f"Chimera Shadow Garden: {'Active' if self.domain_active else 'Inactive'} "
                  f"({self.domain_turns} turns remaining)")
        if self.name == "Jogo":
            print(f"Volcano: {'Active' if self.volcano_active else 'Inactive'} "
                  f"({self.volcano_turns} turns remaining)")
            print(f"Coffin of the Iron Mountain: {'Active' if self.jogo_domain_active else 'Inactive'} "
                  f"({self.jogo_domain_turns} turns remaining)")
        if self.name == "Dagon":
            print(f"Horizon of the Captivating Skandha: {'Active' if self.dagon_domain_active else 'Inactive'} "
                  f"({self.dagon_domain_turns} turns remaining)")
            if self.death_swarm_shikigami:
                print("Death Swarm Shikigami:")
                for s in self.death_swarm_shikigami:
                    print(f"- {s['type']} (HP: {s['hp']}, Damage: {s['damage']}, MP: {s['mp']}, Tile: {s['tile']})")
            else:
                print("Death Swarm Shikigami: None")
        if self.binding_vows:
            vow_conditions = {
                "Binding Vow of Violence": "+1 attack point per turn.",
                "Binding Vow of Resilience": "-1 attack point.",
                "Binding Vow of Swiftness": "+2 movement points, -2 to all dice values for the game.",
                "Binding Vow of Recall": "Megumi cannot attack or open domain.",
                "Binding Vow of Luck": "Jackpot lasts 1 turn, +35 HP instead of 50, +1 reroll.",
                "Binding Vow of Recursion": "1 turn damage immunity on revive, max HP halved, -1 move point.",
                "Binding Vow of Cleansing": "No persistent conditions.",
                "Binding Vow of Substitution": "No persistent conditions.",
                "Binding Vow of the Black Flash": "Damage output x1.5, CE max halved.",
                "Binding Vow of Cursed Flow": "Double CE regen for 3 turns, half for next 3, cycles indefinitely.",
                "Binding Vow of the Stone Soul": "Immune to forced movement, base move points set to 1.",
                "Binding Vow of Transferral": "Allies within 1 tile can deflect damage with consent.",
                "Binding Vow of Uneasy Peace": "No persistent conditions.",
                "Binding Vow of Leverage": "No persistent conditions."
            }
            print(f"Binding Vow Conditions: {vow_conditions[self.binding_vows[0]]}")
        if self.assistant == "Arata":
            print(f"Reminder: Arata protects {self.name} from environmental/tick damage "
                  f"(e.g., cursed buds, fire).")
        if self.assistant == "Granny + Grandson Ogami":
            print(f"Reminder: Revives sorcerer with 25% HP if not killed in a domain.")
        if self.assistant == "Kusakabe":
            print(f"Reminder: Kusakabe’s simple domain protects from domain expansions.")
        if self.assistant == "Ijichi" and self.ijichi_veil_turns > 0:
            print(f"Reminder: Ijichi’s veil is active ({self.ijichi_veil_turns} turns left).")

    def reset_turn_cycle(self) -> None:
        """Reset stats for a new turn cycle (e.g., attack points, move points)."""
        self.attack_points_current = self.default_attack_points
        self.move_points = self.default_move_points
        if "Ranger Rotation" in self.perks:
            print(f"{self.name}: Ranger Rotation reset - {self.attack_points_current} AP, {self.move_points} MP.")


def award_xp() -> None:
    global sg_damage_tracker
    print("\nAward XP for defeated enemies:")
    print("1) G4\n2) G3\n3) G2\n4) G1\n5) Finger Bearer\n6) Special Grade")
    try:
        enemy_type = int(input("Select enemy type: "))
        if enemy_type not in [1, 2, 3, 4, 5, 6]:
            raise ValueError
        if enemy_type <= 5:
            grade = ["G4", "G3", "G2", "G1", "FB"][enemy_type - 1]
            count = int(input(f"How many {grade} enemies defeated? "))
            if count < 1:
                raise ValueError
            print("\nSelect sorcerers to receive XP (equal split):")
            for i, s in enumerate(sorcerer_pool):
                print(f"{i + 1}) {s.name} ({s.grade})")
            choices = input("Enter sorcerer numbers (comma-separated): ").strip()
            if not choices:
                print("No sorcerers selected.")
                return
            indices = [int(i) - 1 for i in choices.split(",") if i.strip()]
            valid_sorcerers = [sorcerer_pool[i] for i in indices if 0 <= i < len(sorcerer_pool)]
            if not valid_sorcerers:
                print("No valid sorcerers selected.")
                return
            xp_per_sorcerer = (xp_drops[grade] * count) // len(valid_sorcerers)
            for s in valid_sorcerers:
                s.xp += xp_per_sorcerer
                print(f"{s.name} gains {xp_per_sorcerer} XP (total: {s.xp})")
                if s.name == "Yuji" and s.grade in ["G4", "G3", "G2", "G1", "SG"]:
                    attacks = int(input(f"How many successful attacks did {s.name} "
                                      f"land on {grade} enemies? "))
                    ce_gain = attacks * 15
                    if ce_gain > 0:
                        s.ce = min(s.ce + ce_gain, s.ce_max)
                        print(f"{s.name} gains {ce_gain} CE from Resilient perk "
                              f"(total: {s.ce}/{s.ce_max})")
                s.level_up()
        else:
            print("\nSelect defeated Special Grade:")
            for i, sg in enumerate(special_grade_deck):
                print(f"{i + 1}) {sg}")
            sg_idx = int(input("SG #: ")) - 1
            sg = special_grade_deck[sg_idx]
            total_xp = xp_drops[sg]
            print(f"\nEnter damage dealt to {sg} by each sorcerer (0 if none):")
            contributions = {}
            total_damage = 0
            for s in sorcerer_pool:
                damage = int(input(f"{s.name} damage dealt: "))
                if damage < 0:
                    raise ValueError
                if damage > 0:
                    contributions[s.name] = damage
                    total_damage += damage
            if total_damage == 0:
                print("No damage recorded. XP not awarded.")
                return
            sg_damage_tracker[sg] = contributions
            for s in sorcerer_pool:
                if s.name == "Yuji" and s.grade in ["G4", "G3", "G2", "G1", "SG"]:
                    attacks = int(input(f"How many successful attacks did {s.name} "
                                      f"land on {sg}? "))
                    ce_gain = attacks * 15
                    if ce_gain > 0:
                        s.ce = min(s.ce + ce_gain, s.ce_max)
                        print(f"{s.name} gains {ce_gain} CE from Resilient perk "
                              f"(total: {s.ce}/{s.ce_max})")
            for s_name, damage in contributions.items():
                sorcerer = next(s for s in sorcerer_pool if s.name == s_name)
                xp_share = round((damage / total_damage) * total_xp)
                is_killer = input(f"Did {s_name} land the killing blow? (y/n): ").lower() == "y"
                if is_killer:
                    xp_share += 4
                sorcerer.xp += xp_share
                print(f"{s_name} gains {xp_share} XP (total: {sorcerer.xp})")
                sorcerer.level_up()
            sg_damage_tracker.pop(sg, None)
    except (ValueError, IndexError):
        print("Invalid input. Try again.")

def manage_sorcerer_pool():
    global sorcerer_pool
    if not sorcerer_pool:
        sorcerer_names = [
            "Yuji", "Hakari", "Nanami", "Gojo", "Todo", "Inumaki",
            "Choso", "Nobara", "Jogo", "Toji", "Dagon", "Panda",
            "Hanami", "Sukuna", "Mahito", "Geto", "Megumi", "Baghead", "Kamo"
        ]
        print("\nAvailable Sorcerers:")
        for i, name in enumerate(sorcerer_names):
            print(f"{i + 1}) {name}")
        while True:
            try:
                choices = input("\nEnter sorcerer numbers separated by commas: ")
                indices = [int(i) for i in choices.split(",")]
                if not all(1 <= i <= len(sorcerer_names) for i in indices):
                    raise ValueError
                sorcerer_pool = [Sorcerer(name) for i, name in enumerate(sorcerer_names) if i + 1 in indices]
                print(f"\nSelected sorcerers: {[s.name for s in sorcerer_pool]}")
                break
            except ValueError:
                print("Invalid input. Enter valid numbers separated by commas.")
    while True:
        print("\nSorcerer Pool Management:")
        for i, s in enumerate(sorcerer_pool):
            status = " (Knocked Out)" if s.is_knocked_out else ""
            print(f"{i + 1}) {s.name} ({s.grade}){status}")
        print(f"{len(sorcerer_pool) + 1}) Return to Main Menu")
        try:
            sub_choice = int(input("Choose a sorcerer to manage (or return): "))
            if sub_choice == len(sorcerer_pool) + 1:
                break
            selected = sorcerer_pool[sub_choice - 1]
            while True:
                if selected.is_knocked_out:
                    print(f"\n{selected.name} is knocked out and cannot act this turn.")
                    print("1) View Info")
                    print("2) Remove CE")
                    print("3) Return")
                    action = input("Select action: ")
                    if action == "1":
                        selected.show_info()
                    elif action == "2":
                        selected.remove_ce()
                    elif action == "3":
                        break
                    else:
                        print("Invalid action.")
                    continue
                print(f"\nManaging {selected.name} ({selected.grade}):")
                print("1) Take Damage")
                print("2) View Info")
                print("3) Manage Assistant")
                print("4) Use Skill Card")
                print("5) Use Binding Vow")
                print("6) Award XP")
                print("7) Perform Attack")
                print("8) Remove CE")
                next_option = 9
                has_todo_sg_action = selected.name == "Todo" and selected.grade == "SG"
                has_todo_teleport = selected.name == "Todo" and selected.grade == "SG" and "Teleport Support" in selected.perks
                has_megumi_unsummon = 1 if selected.name == "Megumi" and len(selected.active_shikigami) > 0 else 0
                has_ranger_rotation = 1 if "Ranger Rotation" in selected.perks else 0
                has_butcher_budgeting = 1 if "Butcher Budgeting" in selected.perks else 0
                if has_todo_sg_action:
                    print(f"{next_option}) Preview Enemy Turn")
                    next_option += 1
                if has_todo_teleport:
                    print(f"{next_option}) Use Teleport Support")
                    next_option += 1
                if has_megumi_unsummon:
                    print(f"{next_option}) Unsummon Shikigami")
                    next_option += 1
                if has_ranger_rotation:
                    print(f"{next_option}) Use Ranger Rotation")
                    next_option += 1
                if has_butcher_budgeting:
                    print(f"{next_option}) Use Butcher Budgeting")
                    next_option += 1
                print(f"{next_option}) Return")
                action = input("Select action: ")
                if action == "1":
                    try:
                        dmg = int(input("Damage taken: "))
                        if selected.take_damage(dmg):
                            sorcerer_pool.remove(selected)
                            break
                    except ValueError:
                        print("Invalid damage value.")
                elif action == "2":
                    selected.show_info()
                elif action == "3":
                    if selected.is_knocked_out:
                        print(f"{selected.name} is knocked out and cannot manage assistants.")
                        continue
                    if not selected.assistant:
                        print(f"{selected.name} has no assistant to manage.")
                        continue
                    print(f"\nManaging {selected.name}’s Assistant ({selected.assistant}):")
                    print("1) Use Assistant")
                    print("2) Give Assistant")
                    print("3) Swap Assistant")
                    print("4) Exit")
                    assistant_action = input("Select assistant action: ")
                    if assistant_action == "1":
                        if selected.assistant == "Shoko":
                            if selected.shoko_cooldown > 0:
                                print(f"Shoko is on cooldown for {selected.shoko_cooldown} more turns.")
                            else:
                                print(f"{selected.name} has {selected.ce} CE.")
                                try:
                                    ce_to_use = int(input("How much CE to trade for HP? (10 CE = 1 HP): "))
                                    if ce_to_use > selected.ce:
                                        print("Not enough CE. Try again.")
                                    else:
                                        selected.ce -= ce_to_use
                                        gained_hp = ce_to_use // 10
                                        selected.hp = min(selected.hp + gained_hp, selected.hp_max)
                                        print(f"{selected.name} gains {gained_hp} HP!")
                                        selected.shoko_cooldown = 5
                                except ValueError:
                                    print("Invalid CE value.")
                        elif selected.assistant == "Yaga":
                            if selected.yaga_cooldown > 0:
                                print(f"Yaga is on cooldown for {selected.yaga_cooldown} more turns.")
                            else:
                                selected.cursed_corpses = 3
                                selected.yaga_cooldown = 7
                                print(f"{selected.name} spawns 3 cursed corpses! 3 corpses active.")
                                print(f"Reminder: Track +1 DMG per set of 3 living corpses manually.")
                        elif selected.assistant == "Mechamaru":
                            if selected.mechamaru_cooldown > 0:
                                print(f"Mechamaru is on cooldown for {selected.mechamaru_cooldown} more turns.")
                            elif selected.mechamaru_rerolls == 0:
                                print("No rerolls remaining. Mechamaru is on cooldown.")
                            else:
                                use_reroll = input("Use 1 reroll? (y/n): ").lower()
                                if use_reroll == "y":
                                    selected.mechamaru_rerolls -= 1
                                    print(
                                        f"{selected.name} uses a Mechamaru reroll! {selected.mechamaru_rerolls} rerolls left.")
                                    if selected.mechamaru_rerolls == 0:
                                        selected.mechamaru_cooldown = 3
                        elif selected.assistant == "Kusakabe":
                            if selected.kusakabe_cooldown > 0:
                                print(f"Kusakabe is on cooldown for {selected.kusakabe_cooldown} more turns.")
                            else:
                                selected.kusakabe_cooldown = 6
                                print(f"{selected.name} activates Kusakabe’s simple domain!")
                                print(
                                    f"Reminder: Protects from domain expansions for sorcerer and allies on same tile.")
                        elif selected.assistant == "Ijichi":
                            if selected.ijichi_cooldown > 0:
                                print(f"Ijichi is on cooldown for {selected.ijichi_cooldown} more turns.")
                            elif selected.ijichi_veil_turns > 0:
                                close_veil = input("Close Ijichi’s veil early? (y/n): ").lower()
                                if close_veil == "y":
                                    selected.ijichi_veil_turns = 0
                                    print(f"{selected.name}: Ijichi’s veil has been closed.")
                                else:
                                    print(f"Ijichi’s veil is active ({selected.ijichi_veil_turns} turns left).")
                            else:
                                try:
                                    radius = int(input("Enter veil radius (0 or 1): "))
                                    if radius not in [0, 1]:
                                        raise ValueError
                                    selected.ijichi_veil_turns = 2
                                    selected.ijichi_cooldown = 5
                                    print(f"{selected.name} activates Ijichi’s veil (radius {radius}) for 2 turns!")
                                    print(f"Reminder: Blocks hostiles from entering.")
                                except ValueError:
                                    print("Invalid radius. Enter 0 or 1.")
                        else:
                            print(
                                f"{selected.assistant}’s ability is applied or always active: {assistant_abilities[selected.assistant]}")
                    elif assistant_action == "2":
                        other_sorcerers = [s for s in sorcerer_pool if s != selected]
                        if not other_sorcerers:
                            print("No other sorcerers available to receive the assistant.")
                            continue
                        print("\nSelect a sorcerer to receive the assistant:")
                        for i, s in enumerate(other_sorcerers, 1):
                            status = f" (has {s.assistant})" if s.assistant else ""
                            print(f"{i}) {s.name}{status}")
                        try:
                            choice = int(input("Choose a sorcerer (or 0 to cancel): ")) - 1
                            if choice == -1:
                                print("Give assistant cancelled.")
                                continue
                            if 0 <= choice < len(other_sorcerers):
                                target = other_sorcerers[choice]
                                assistant = selected.assistant
                                shoko_cooldown = getattr(selected, 'shoko_cooldown', 0)
                                yaga_cooldown = getattr(selected, 'yaga_cooldown', 0)
                                cursed_corpses = getattr(selected, 'cursed_corpses', 0)
                                mechamaru_cooldown = getattr(selected, 'mechamaru_cooldown', 0)
                                mechamaru_rerolls = getattr(selected, 'mechamaru_rerolls', 0)
                                kusakabe_cooldown = getattr(selected, 'kusakabe_cooldown', 0)
                                ijichi_cooldown = getattr(selected, 'ijichi_cooldown', 0)
                                ijichi_veil_turns = getattr(selected, 'ijichi_veil_turns', 0)
                                target.assistant = assistant
                                if assistant == "Shoko":
                                    target.shoko_cooldown = shoko_cooldown
                                elif assistant == "Yaga":
                                    target.yaga_cooldown = yaga_cooldown
                                    target.cursed_corpses = cursed_corpses
                                elif assistant == "Mechamaru":
                                    target.mechamaru_cooldown = mechamaru_cooldown
                                    target.mechamaru_rerolls = mechamaru_rerolls
                                elif assistant == "Kusakabe":
                                    target.kusakabe_cooldown = kusakabe_cooldown
                                elif assistant == "Ijichi":
                                    target.ijichi_cooldown = ijichi_cooldown
                                    target.ijichi_veil_turns = ijichi_veil_turns
                                selected.assistant = None
                                for attr in ['shoko_cooldown', 'yaga_cooldown', 'cursed_corpses',
                                             'mechamaru_cooldown', 'mechamaru_rerolls', 'kusakabe_cooldown',
                                             'ijichi_cooldown', 'ijichi_veil_turns']:
                                    if hasattr(selected, attr):
                                        setattr(selected, attr, 0)
                                print(f"{selected.name} gave {assistant} to {target.name}.")
                            else:
                                print("Invalid sorcerer selection.")
                        except ValueError:
                            print("Invalid input. Enter a number.")
                    elif assistant_action == "3":
                        other_sorcerers = [s for s in sorcerer_pool if s != selected and s.assistant]
                        if not other_sorcerers:
                            print("No other sorcerers with assistants available to swap.")
                            continue
                        print("\nSelect a sorcerer to swap assistants with:")
                        for i, s in enumerate(other_sorcerers, 1):
                            print(f"{i}) {s.name} ({s.assistant})")
                        try:
                            choice = int(input("Choose a sorcerer (or 0 to cancel): ")) - 1
                            if choice == -1:
                                print("Swap assistant cancelled.")
                                continue
                            if 0 <= choice < len(other_sorcerers):
                                target = other_sorcerers[choice]
                                selected_assistant = selected.assistant
                                selected_shoko_cooldown = getattr(selected, 'shoko_cooldown', 0)
                                selected_yaga_cooldown = getattr(selected, 'yaga_cooldown', 0)
                                selected_cursed_corpses = getattr(selected, 'cursed_corpses', 0)
                                selected_mechamaru_cooldown = getattr(selected, 'mechamaru_cooldown', 0)
                                selected_mechamaru_rerolls = getattr(selected, 'mechamaru_rerolls', 0)
                                selected_kusakabe_cooldown = getattr(selected, 'kusakabe_cooldown', 0)
                                selected_ijichi_cooldown = getattr(selected, 'ijichi_cooldown', 0)
                                selected_ijichi_veil_turns = getattr(selected, 'ijichi_veil_turns', 0)
                                target_assistant = target.assistant
                                target_shoko_cooldown = getattr(target, 'shoko_cooldown', 0)
                                target_yaga_cooldown = getattr(target, 'yaga_cooldown', 0)
                                target_cursed_corpses = getattr(target, 'cursed_corpses', 0)
                                target_mechamaru_cooldown = getattr(target, 'mechamaru_cooldown', 0)
                                target_mechamaru_rerolls = getattr(target, 'mechamaru_rerolls', 0)
                                target_kusakabe_cooldown = getattr(target, 'kusakabe_cooldown', 0)
                                target_ijichi_cooldown = getattr(target, 'ijichi_cooldown', 0)
                                target_ijichi_veil_turns = getattr(target, 'ijichi_veil_turns', 0)
                                selected.assistant = target_assistant
                                target.assistant = selected_assistant
                                if target_assistant == "Shoko":
                                    selected.shoko_cooldown = target_shoko_cooldown
                                elif target_assistant == "Yaga":
                                    selected.yaga_cooldown = target_yaga_cooldown
                                    selected.cursed_corpses = target_cursed_corpses
                                elif target_assistant == "Mechamaru":
                                    selected.mechamaru_cooldown = target_mechamaru_cooldown
                                    selected.mechamaru_rerolls = target_mechamaru_rerolls
                                elif target_assistant == "Kusakabe":
                                    selected.kusakabe_cooldown = target_kusakabe_cooldown
                                elif target_assistant == "Ijichi":
                                    selected.ijichi_cooldown = target_ijichi_cooldown
                                    selected.ijichi_veil_turns = target_ijichi_veil_turns
                                if selected_assistant == "Shoko":
                                    target.shoko_cooldown = selected_shoko_cooldown
                                elif selected_assistant == "Yaga":
                                    target.yaga_cooldown = selected_yaga_cooldown
                                    target.cursed_corpses = selected_cursed_corpses
                                elif selected_assistant == "Mechamaru":
                                    target.mechamaru_cooldown = selected_mechamaru_cooldown
                                    target.mechamaru_rerolls = selected_mechamaru_rerolls
                                elif selected_assistant == "Kusakabe":
                                    target.kusakabe_cooldown = selected_kusakabe_cooldown
                                elif selected_assistant == "Ijichi":
                                    target.ijichi_cooldown = selected_ijichi_cooldown
                                    target.ijichi_veil_turns = selected_ijichi_veil_turns
                                for attr in ['shoko_cooldown', 'yaga_cooldown', 'cursed_corpses',
                                             'mechamaru_cooldown', 'mechamaru_rerolls', 'kusakabe_cooldown',
                                             'ijichi_cooldown', 'ijichi_veil_turns']:
                                    if hasattr(selected, attr) and not (
                                            selected.assistant == "Shoko" and attr == 'shoko_cooldown' or
                                            selected.assistant == "Yaga" and attr in ['yaga_cooldown',
                                                                                      'cursed_corpses'] or
                                            selected.assistant == "Mechamaru" and attr in ['mechamaru_cooldown',
                                                                                           'mechamaru_rerolls'] or
                                            selected.assistant == "Kusakabe" and attr == 'kusakabe_cooldown' or
                                            selected.assistant == "Ijichi" and attr in ['ijichi_cooldown',
                                                                                        'ijichi_veil_turns']):
                                        setattr(selected, attr, 0)
                                    if hasattr(target, attr) and not (
                                            target.assistant == "Shoko" and attr == 'shoko_cooldown' or
                                            target.assistant == "Yaga" and attr in ['yaga_cooldown',
                                                                                    'cursed_corpses'] or
                                            target.assistant == "Mechamaru" and attr in ['mechamaru_cooldown',
                                                                                         'mechamaru_rerolls'] or
                                            target.assistant == "Kusakabe" and attr == 'kusakabe_cooldown' or
                                            target.assistant == "Ijichi" and attr in ['ijichi_cooldown',
                                                                                      'ijichi_veil_turns']):
                                        setattr(target, attr, 0)
                                print(
                                    f"{selected.name} and {target.name} swapped assistants: {selected_assistant} <-> {target_assistant}.")
                            else:
                                print("Invalid sorcerer selection.")
                        except ValueError:
                            print("Invalid input. Enter a number.")
                    elif assistant_action == "4":
                        continue
                    else:
                        print("Invalid action.")
                elif action == "4":
                    if not selected.skill_cards:
                        print("No skill cards to use.")
                    else:
                        print(f"\n{selected.name}’s Skill Cards:")
                        for i, card in enumerate(selected.skill_cards):
                            print(f"{i + 1}) {card}")
                        try:
                            card_choice = int(input("Select a skill card to use: ")) - 1
                            if 0 <= card_choice < len(selected.skill_cards):
                                card = selected.skill_cards.pop(card_choice)
                                skill_card_deck.append(card)
                                print(f"\nUsing {card}...")
                                if card == "Reverse Curse Technique":
                                    selected.hp = selected.hp_max
                                    print(f"Reverse Curse Technique used! Restored to full HP ({selected.hp_max}).")
                                elif card == "Cursed Surge":
                                    selected.ce += 150
                                    print(f"Cursed Surge used! Gained +150 CE (current: {selected.ce}).")
                                elif card == "Hasten":
                                    if selected.assistant in ["Shoko", "Yaga", "Mechamaru", "Kusakabe", "Ijichi"]:
                                        if selected.assistant == "Shoko" and selected.shoko_cooldown > 0:
                                            selected.shoko_cooldown = 0
                                            print(f"Hasten used! Shoko’s cooldown reset.")
                                        elif selected.assistant == "Yaga" and selected.yaga_cooldown > 0:
                                            selected.yaga_cooldown = 0
                                            print(f"Hasten used! Yaga’s cooldown reset.")
                                        elif selected.assistant == "Mechamaru" and selected.mechamaru_cooldown > 0:
                                            selected.mechamaru_cooldown = 0
                                            print(f"Hasten used! Mechamaru’s cooldown reset.")
                                        elif selected.assistant == "Kusakabe" and selected.kusakabe_cooldown > 0:
                                            selected.kusakabe_cooldown = 0
                                            print(f"Hasten used! Kusakabe’s cooldown reset.")
                                        elif selected.assistant == "Ijichi" and selected.ijichi_cooldown > 0:
                                            selected.ijichi_cooldown = 0
                                            print(f"Hasten used! Ijichi’s cooldown reset.")
                                        else:
                                            print(
                                                f"Hasten has no effect; {selected.assistant}’s ability is not on cooldown.")
                                    else:
                                        print(
                                            f"Hasten has no effect; {selected.assistant}’s ability does not use cooldowns.")
                                else:
                                    print(f"{card} used! Apply its effect manually.")
                            else:
                                print("Invalid skill card selection.")
                        except ValueError:
                            print("Invalid input. Enter a number.")
                elif action == "5":
                    if len(selected.binding_vows) >= 2:
                        print(f"{selected.name} already has maximum binding vows: {', '.join(selected.binding_vows)}")
                    else:
                        if not binding_vow_deck:
                            print("No binding vows available.")
                        else:
                            available_vows = [vow for vow in binding_vow_deck if selected.can_add_binding_vow(vow)]
                            if not available_vows:
                                print(f"No compatible binding vows available for {selected.name}.")
                            else:
                                print(f"\nAvailable Binding Vows for {selected.name}:")
                                for i, vow in enumerate(available_vows, 1):
                                    print(f"{i}) {vow}")
                                try:
                                    vow_choice = int(input("Select a binding vow to add (or 0 to cancel): ")) - 1
                                    if vow_choice == -1:
                                        print("Binding vow selection cancelled.")
                                    elif 0 <= vow_choice < len(available_vows):
                                        vow = available_vows[vow_choice]
                                        selected.binding_vows.append(vow)
                                        binding_vow_deck.remove(vow)
                                        print(f"{selected.name} has taken the {vow} binding vow!")
                                        print(f"Reminder: Apply {vow}’s effects manually.")
                                    else:
                                        print("Invalid binding vow selection.")
                                except ValueError:
                                    print("Invalid input. Enter a number.")
                elif action == "6":
                    try:
                        award_xp()
                    except ValueError:
                        print("Invalid XP value.")
                elif action == "7":
                    selected.perform_attack()
                elif action == "8":
                    selected.remove_ce()
                elif action == str(9) and has_todo_sg_action:
                    print("Previewing Enemy Turn...")
                elif action == str(9 + int(has_todo_teleport)) and has_todo_teleport:
                    if selected.ce < 40:
                        print(f"Not enough CE for Teleport Support (40 CE needed, {selected.ce} available).")
                    else:
                        selected.ce -= 40
                        print(
                            f"{selected.name} uses Teleport Support! -40 CE (current: {selected.ce}/{selected.ce_max})")
                        print("Reminder: Apply teleport and bonus damage manually IRL.")
                elif action == str(9 + int(has_todo_sg_action)) and has_megumi_unsummon:
                    print(f"\n{selected.name}’s Active Shikigami:")
                    for i, shikigami in enumerate(selected.active_shikigami, 1):
                        print(f"{i}) {shikigami['name']} (HP: {shikigami['hp']})")
                    try:
                        choice = int(input("Select shikigami to unsummon (or 0 to cancel): ")) - 1
                        if choice == -1:
                            print("Unsummon cancelled.")
                        elif 0 <= choice < len(selected.active_shikigami):
                            shikigami = selected.active_shikigami.pop(choice)
                            print(f"{shikigami['name']} unsummoned.")
                        else:
                            print("Invalid shikigami selection.")
                    except ValueError:
                        print("Invalid input. Enter a number.")
                elif action == str(9 + int(has_todo_sg_action) + int(has_todo_teleport)) and has_megumi_unsummon:
                    print(f"\n{selected.name}’s Active Shikigami:")
                    for i, shikigami in enumerate(selected.active_shikigami, 1):
                        print(f"{i}) {shikigami['name']} (HP: {shikigami['hp']})")
                    try:
                        choice = int(input("Select shikigami to unsummon (or 0 to cancel): ")) - 1
                        if choice == -1:
                            print("Unsummon cancelled.")
                        elif 0 <= choice < len(selected.active_shikigami):
                            shikigami = selected.active_shikigami.pop(choice)
                            print(f"{shikigami['name']} unsummoned.")
                        else:
                            print("Invalid shikigami selection.")
                    except ValueError:
                        print("Invalid input. Enter a number.")
                elif action == str(9 + int(has_todo_sg_action) + int(has_todo_teleport) + int(
                        has_megumi_unsummon)) and has_ranger_rotation:
                    selected.use_ranger_rotation()
                elif action == str(
                        9 + int(has_todo_sg_action) + int(has_todo_teleport) + int(has_megumi_unsummon) + int(
                                has_ranger_rotation)) and has_butcher_budgeting:
                    selected.use_butcher_budgeting()
                elif action == str(
                        9 + int(has_todo_sg_action) + int(has_todo_teleport) + int(has_megumi_unsummon) + int(
                                has_ranger_rotation) + int(has_butcher_budgeting)):
                    break
                else:
                    print("Invalid action.")
        except ValueError:
            print("Invalid input. Enter a number.")

def assistant_menu(selected_sorcerer: Optional[Sorcerer] = None) -> None:
    global assistant_deck
    if not assistant_deck:
        print("\nNo assistants left in the deck!")
        return
    print("\nDrawing assistant...")
    assistant = random.choice(assistant_deck)
    print(f"You drew: {assistant}")
    print(f"Ability: {assistant_abilities[assistant]}")
    if selected_sorcerer and selected_sorcerer.assistant:
        print(f"{selected_sorcerer.name} already has an assistant.")
        choice = input("Discard assistant or leave on square? (discard/leave): ").lower()
        if choice == "discard":
            assistant_deck.remove(assistant)
            print(f"{assistant} discarded.")
        else:
            print(f"{assistant} left on square, risks death.")
        return
    print("Assign this assistant to a sorcerer:")
    if selected_sorcerer:
        target = selected_sorcerer
    else:
        for i, s in enumerate(sorcerer_pool):
            print(f"{i + 1}) {s.name} ({s.grade})")
        try:
            assign_index = int(input("Sorcerer #: ")) - 1
            target = sorcerer_pool[assign_index]
        except (ValueError, IndexError):
            print("Invalid sorcerer selection.")
            return
    target.assistant = assistant
    if assistant == "Mechamaru":
        target.mechamaru_rerolls = 2
        print(f"{target.name} gains 2 rerolls from Mechamaru!")
    elif assistant == "Utahime":
        target.ce_max += 50
        target.ce_regen += 15
        target.ce = min(target.ce, target.ce_max)
        print(f"{target.name} gains +50 CE max and +15 CE regen from Utahime!")
    assistant_deck.remove(assistant)
    print(f"{assistant} assigned to {target.name}!")

def skill_card_menu(selected_sorcerer: Optional[Sorcerer] = None) -> None:
    global skill_card_deck
    if not skill_card_deck:
        print("\nNo skill cards left in the deck!")
        return
    print("\nDrawing skill card...")
    card = random.choice(skill_card_deck)
    print(f"You drew: {card}")
    print("Assign this skill card to a sorcerer:")
    valid_sorcerers = ([selected_sorcerer] if selected_sorcerer
                       else [s for s in sorcerer_pool if s.can_add_skill_card()])
    if not valid_sorcerers:
        print("No sorcerers can receive a skill card (all have 2 cards).")
        return
    for i, s in enumerate(valid_sorcerers):
        print(f"{i + 1}) {s.name} ({s.grade}, {len(s.skill_cards)}/2 cards)")
    try:
        assign_index = 0 if selected_sorcerer else int(input("Sorcerer #: ")) - 1
        target = valid_sorcerers[assign_index]
        target.skill_cards.append(card)
        skill_card_deck.remove(card)
        print(f"{card} assigned to {target.name}!")
    except (ValueError, IndexError):
        print("Invalid sorcerer selection.")

def binding_vow_menu() -> None:
    global binding_vow_deck
    if not binding_vow_deck:
        print("\nNo binding vows left in the deck!")
        return
    print("\nDrawing 5 binding vows...")
    import random
    drawn_vows = random.sample(binding_vow_deck, min(5, len(binding_vow_deck)))
    print("Available Binding Vows:")
    for i, vow in enumerate(drawn_vows, 1):
        print(f"{i}) {vow}")
    try:
        vow_choice = int(input("Select a binding vow to assign (or 0 to pass): ")) - 1
        if vow_choice == -1:
            print("Binding vow assignment passed.")
            return
        if 0 <= vow_choice < len(drawn_vows):
            selected_vow = drawn_vows[vow_choice]
            print(f"\nAssign {selected_vow} to a sorcerer:")
            valid_sorcerers = [s for s in sorcerer_pool if s.can_add_binding_vow(selected_vow) and len(s.binding_vows) < 2]
            if not valid_sorcerers:
                print("No sorcerers can receive this binding vow (all at capacity or ineligible).")
                return
            for i, s in enumerate(valid_sorcerers, 1):
                print(f"{i}) {s.name} ({s.grade}, {len(s.binding_vows)}/2 vows)")
            try:
                assign_index = int(input("Sorcerer #: ")) - 1
                if 0 <= assign_index < len(valid_sorcerers):
                    target = valid_sorcerers[assign_index]
                    target.binding_vows.append(selected_vow)
                    binding_vow_deck.remove(selected_vow)
                    print(f"{selected_vow} assigned to {target.name}!")
                    print(f"Reminder: Apply {selected_vow}’s effects manually.")
                else:
                    print("Invalid sorcerer selection.")
            except (ValueError, IndexError):
                print("Invalid sorcerer selection.")
        else:
            print("Invalid binding vow selection.")
    except ValueError:
        print("Invalid input. Enter a number.")

def encounter_card_menu() -> None:
    global current_encounter_card_deck
    if not current_encounter_card_deck:
        print("\nEncounter card deck is empty, refilling...")
        current_encounter_card_deck = refill_encounter_card_deck()
    print("\nDrawing encounter card...")
    card = random.choice(current_encounter_card_deck)
    print(f"You drew: {card}")
    current_encounter_card_deck.remove(card)
    if card in ["Meditative State", "Stealthy Withdrawal", "Assistant Draw",
               "Reassessment", "All-out", "Flyhead Swarm", "Prison Realm", "Hostile Rush"]:
        print("Select a sorcerer:")
        for i, s in enumerate(sorcerer_pool):
            print(f"{i + 1}) {s.name} ({s.grade})")
        try:
            sorcerer_idx = int(input("Sorcerer #: ")) - 1
            selected = sorcerer_pool[sorcerer_idx]
        except (ValueError, IndexError):
            print("Invalid sorcerer selection.")
            return
    if card == "Hidden Shrine":
        print("Hidden Shrine used! Drew from binding vow deck.")
        binding_vow_menu()
    elif card == "Meditative State":
        print(f"Meditative State used! {selected.name} removes all debuffs.")
    elif card == "Rally Point":
        print("Select the sorcerer who drew the card:")
        for i, s in enumerate(sorcerer_pool):
            print(f"{i + 1}) {s.name} ({s.grade})")
        try:
            owner_idx = int(input("Sorcerer #: ")) - 1
            owner = sorcerer_pool[owner_idx]
            movers = []
            for s in sorcerer_pool:
                if s != owner:
                    move = input(f"Move {s.name} to {owner.name}’s tile? (y/n): ").lower()
                    if move == "y":
                        movers.append(s.name)
            print(f"Rally Point used! {', '.join(movers) or 'No one'} move to "
                  f"{owner.name}’s tile without CE/move cost.")
        except (ValueError, IndexError):
            print("Invalid sorcerer selection.")
    elif card == "Stealthy Withdrawal":
        print(f"Stealthy Withdrawal used! {selected.name} can pass hostiles without CE tax.")
    elif card == "Assistant Draw":
        print(f"Assistant Draw used! Drawing from assistant deck for {selected.name}.")
        assistant_menu(selected)
    elif card == "Reassessment":
        if not selected.skill_cards:
            print("No skill cards to discard. Reassessment failed.")
        else:
            print(f"\n{selected.name}’s Skill Cards:")
            for i, sc in enumerate(selected.skill_cards):
                print(f"{i + 1}) {sc}")
            try:
                discard_idx = int(input("Select skill card to discard: ")) - 1
                discarded = selected.skill_cards.pop(discard_idx)
                print(f"Reassessment used! Discarded {discarded}, drawing new skill card.")
                skill_card_menu(selected)
            except (ValueError, IndexError):
                print("Invalid selection.")
    elif card == "All-out":
        if selected.hp == selected.hp_max:
            print("HP is at max. All-out failed.")
        else:
            print(f"All-out used! {selected.name} gains +1 action point, +1 move point.")
    elif card == "Flyhead Swarm":
        print(f"Flyhead Swarm used! {selected.name} ends turn, immune to non-domain "
              f"attacks until next turn.")
    elif card == "Prison Realm":
        print(f"Prison Realm used! {selected.name} is trapped, needs another sorcerer "
              f"to roll 3+ attack points to free.")
    elif card == "Hostile Rush":
        print(f"Hostile Rush used! Enemies in adjacent tiles move to {selected.name}’s tile, "
              f"ranged curses fall back 1 tile.")
    elif card == "Grade 4 Rush":
        print("Grade 4 Rush used! New batch of G4 curses spawns.")
    elif card == "Special Grade Strike":
        print("Special Grade Strike used! Extra SG curse spawned.")
        special_grade_draw(1)

# =========================
# === Main Menu System ===
# =========================

while True:
    print("\n=== MAIN MENU (Player Turn) ===\n"
          "1) Enemy Spawning (Enemy Turn)\n"
          "2) Sorcerer Pool Management\n"
          "3) Assistant Deck\n"
          "4) Skill Card Deck\n"
          "5) Binding Vow Deck\n"
          "6) Encounter Card Deck\n"
          "7) Exit")
    try:
        choice = input("Choose an option: ")
        if choice == "1":
            print("\n=== Enemy Turn ===")
            # Reset enemy_spawn_deck if empty
            if not enemy_spawn_deck:
                enemy_spawn_deck = master_enemy_deck.copy()
            for sorcerer in sorcerer_pool:
                sorcerer.reset_attack_points()
                sorcerer.gain_ce()
                if sorcerer.shoko_cooldown > 0:
                    sorcerer.shoko_cooldown -= 1
                if sorcerer.yaga_cooldown > 0:
                    sorcerer.yaga_cooldown -= 1
                if sorcerer.mechamaru_cooldown > 0:
                    sorcerer.mechamaru_cooldown -= 1
                if sorcerer.kusakabe_cooldown > 0:
                    sorcerer.kusakabe_cooldown -= 1
                if sorcerer.ijichi_cooldown > 0:
                    sorcerer.ijichi_cooldown -= 1
                if sorcerer.ijichi_veil_turns > 0:
                    sorcerer.ijichi_veil_turns -= 1
                    if sorcerer.ijichi_veil_turns == 0:
                        print(f"{sorcerer.name}: Ijichi’s veil has ended.")
                if sorcerer.name == "Nanami" and sorcerer.overtime_turns > 0:
                    sorcerer.overtime_turns -= 1
                    if sorcerer.name.overtime_turns == 0:
                        print(f"{sorcerer.name}’s Overtime effect ends.")
                elif sorcerer.name == "Gojo" and sorcerer.infinite_void_turns > 0:
                    sorcerer.infinite_void_turns -= 1
                    if sorcerer.infinite_void_turns == 0:
                        print(f"{sorcerer.name}’s Infinite Void ends.")
            while True:
                draw_enemy_card()
                more = input("\nDraw another card? (y/n): ").lower()
                if more != 'y':
                    break
            previewed_cards.clear()
        elif choice == "2":
            manage_sorcerer_pool()
        elif choice == "3":
            assistant_menu()
        elif choice == "4":
            skill_card_menu()
        elif choice == "5":
            binding_vow_menu()
        elif choice == "6":
            encounter_card_menu()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
    except ValueError:
        print("Invalid input. Try again.")