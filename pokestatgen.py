import json

# Format: (Pokedex_ID, Name, Type1, Type2, Base_HP, Base_Attack, Base_Defense, Base_SpAtk, Base_SpDef, Base_Speed)
# Base stat values for Generation 1 Pokemon
GEN1_DATA = [
    (1, "Bulbasaur", "GRASS", "POISON", 45, 49, 49, 65, 65, 45),
    (2, "Ivysaur", "GRASS", "POISON", 60, 62, 63, 80, 80, 60),
    (3, "Venusaur", "GRASS", "POISON", 80, 82, 83, 100, 100, 80),
    (4, "Charmander", "FIRE", None, 39, 52, 43, 60, 50, 65),
    (5, "Charmeleon", "FIRE", None, 58, 64, 58, 80, 65, 80),
    (6, "Charizard", "FIRE", "FLYING", 78, 84, 78, 109, 85, 100),
    (7, "Squirtle", "WATER", None, 44, 48, 65, 50, 64, 43),
    (8, "Wartortle", "WATER", None, 59, 63, 80, 65, 80, 58),
    (9, "Blastoise", "WATER", None, 79, 83, 100, 85, 105, 78),
    (10, "Caterpie", "BUG", None, 45, 30, 35, 20, 20, 45),
    (11, "Metapod", "BUG", None, 50, 20, 55, 25, 25, 30),
    (12, "Butterfree", "BUG", "FLYING", 60, 45, 50, 90, 80, 70),
    (13, "Weedle", "BUG", "POISON", 40, 35, 30, 20, 20, 50),
    (14, "Kakuna", "BUG", "POISON", 45, 25, 50, 25, 25, 35),
    (15, "Beedrill", "BUG", "POISON", 65, 90, 40, 45, 80, 75),
    (16, "Pidgey", "NORMAL", "FLYING", 40, 45, 40, 35, 35, 56),
    (17, "Pidgeotto", "NORMAL", "FLYING", 63, 60, 55, 50, 50, 71),
    (18, "Pidgeot", "NORMAL", "FLYING", 83, 80, 75, 70, 70, 101),
    (19, "Rattata", "NORMAL", None, 30, 56, 35, 25, 35, 72),
    (20, "Raticate", "NORMAL", None, 55, 81, 60, 50, 70, 97),
    (21, "Spearow", "NORMAL", "FLYING", 40, 60, 30, 31, 31, 70),
    (22, "Fearow", "NORMAL", "FLYING", 65, 90, 65, 61, 61, 100),
    (23, "Ekans", "POISON", None, 35, 60, 44, 40, 54, 55),
    (24, "Arbok", "POISON", None, 60, 85, 69, 65, 79, 80),
    (25, "Pikachu", "ELECTRIC", None, 35, 55, 40, 50, 50, 90),
    (26, "Raichu", "ELECTRIC", None, 60, 90, 55, 90, 80, 110),
    (27, "Sandshrew", "GROUND", None, 50, 75, 85, 20, 30, 40),
    (28, "Sandslash", "GROUND", None, 75, 100, 110, 45, 55, 65),
    (29, "Nidoran♀", "POISON", None, 55, 47, 52, 40, 40, 41),
    (30, "Nidorina", "POISON", None, 70, 62, 67, 55, 55, 56),
    (31, "Nidoqueen", "POISON", "GROUND", 90, 92, 87, 75, 85, 76),
    (32, "Nidoran♂", "POISON", None, 46, 57, 40, 40, 40, 50),
    (33, "Nidorino", "POISON", None, 61, 72, 57, 55, 55, 65),
    (34, "Nidoking", "POISON", "GROUND", 81, 102, 77, 85, 75, 85),
    (35, "Clefairy", "NORMAL", None, 70, 45, 48, 60, 65, 35),
    (36, "Clefable", "NORMAL", None, 95, 70, 73, 95, 90, 60),
    (37, "Vulpix", "FIRE", None, 38, 41, 40, 50, 65, 65),
    (38, "Ninetales", "FIRE", None, 73, 76, 75, 81, 100, 100),
    (39, "Jigglypuff", "NORMAL", None, 115, 45, 20, 45, 25, 20),
    (40, "Wigglytuff", "NORMAL", None, 140, 70, 45, 85, 50, 45),
    (41, "Zubat", "POISON", "FLYING", 40, 45, 35, 30, 40, 55),
    (42, "Golbat", "POISON", "FLYING", 75, 80, 70, 65, 75, 90),
    (43, "Oddish", "GRASS", "POISON", 45, 50, 55, 75, 65, 30),
    (44, "Gloom", "GRASS", "POISON", 60, 65, 70, 85, 75, 40),
    (45, "Vileplume", "GRASS", "POISON", 75, 80, 85, 110, 90, 50),
    (46, "Paras", "BUG", "GRASS", 35, 70, 55, 45, 55, 25),
    (47, "Parasect", "BUG", "GRASS", 60, 95, 80, 60, 80, 30),
    (48, "Venonat", "BUG", "POISON", 60, 55, 50, 40, 55, 45),
    (49, "Venomoth", "BUG", "POISON", 70, 65, 60, 90, 75, 90),
    (50, "Diglett", "GROUND", None, 10, 55, 25, 35, 45, 95),
    (51, "Dugtrio", "GROUND", None, 35, 80, 50, 50, 70, 120),
    (52, "Meowth", "NORMAL", None, 40, 45, 35, 40, 40, 90),
    (53, "Persian", "NORMAL", None, 65, 70, 60, 65, 65, 115),
    (54, "Psyduck", "WATER", None, 50, 52, 48, 65, 50, 55),
    (55, "Golduck", "WATER", None, 80, 82, 78, 95, 80, 85),
    (56, "Mankey", "FIGHTING", None, 40, 80, 35, 35, 45, 70),
    (57, "Primeape", "FIGHTING", None, 65, 105, 60, 60, 70, 95),
    (58, "Growlithe", "FIRE", None, 55, 70, 45, 70, 50, 60),
    (59, "Arcanine", "FIRE", None, 90, 110, 80, 100, 80, 95),
    (60, "Poliwag", "WATER", None, 40, 50, 40, 40, 40, 90),
    (61, "Poliwhirl", "WATER", None, 65, 65, 65, 50, 50, 90),
    (62, "Poliwrath", "WATER", "FIGHTING", 90, 95, 95, 70, 90, 70),
    (63, "Abra", "PSYCHIC", None, 25, 20, 15, 105, 55, 90),
    (64, "Kadabra", "PSYCHIC", None, 40, 35, 30, 120, 70, 105),
    (65, "Alakazam", "PSYCHIC", None, 55, 50, 45, 135, 95, 120),
    (66, "Machop", "FIGHTING", None, 70, 80, 50, 35, 35, 35),
    (67, "Machoke", "FIGHTING", None, 80, 100, 70, 50, 60, 45),
    (68, "Machamp", "FIGHTING", None, 90, 130, 80, 65, 85, 55),
    (69, "Bellsprout", "GRASS", "POISON", 50, 75, 35, 70, 30, 40),
    (70, "Weepinbell", "GRASS", "POISON", 65, 90, 50, 85, 45, 55),
    (71, "Victreebel", "GRASS", "POISON", 80, 105, 65, 100, 70, 70),
    (72, "Tentacool", "WATER", "POISON", 40, 40, 35, 50, 100, 70),
    (73, "Tentacruel", "WATER", "POISON", 80, 70, 65, 80, 120, 100),
    (74, "Geodude", "ROCK", "GROUND", 40, 80, 100, 30, 30, 20),
    (75, "Graveler", "ROCK", "GROUND", 55, 95, 115, 45, 45, 35),
    (76, "Golem", "ROCK", "GROUND", 80, 120, 130, 55, 65, 45),
    (77, "Ponyta", "FIRE", None, 50, 85, 55, 65, 65, 90),
    (78, "Rapidash", "FIRE", None, 65, 100, 70, 80, 80, 105),
    (79, "Slowpoke", "WATER", "PSYCHIC", 90, 65, 65, 40, 40, 15),
    (80, "Slowbro", "WATER", "PSYCHIC", 95, 75, 110, 100, 80, 30),
    (81, "Magnemite", "ELECTRIC", None, 25, 35, 70, 95, 55, 45),
    (82, "Magneton", "ELECTRIC", None, 50, 60, 95, 120, 70, 70),
    (83, "Farfetch'd", "NORMAL", "FLYING", 52, 65, 55, 58, 62, 60),
    (84, "Doduo", "NORMAL", "FLYING", 35, 85, 45, 35, 35, 75),
    (85, "Dodrio", "NORMAL", "FLYING", 60, 110, 70, 60, 60, 100),
    (86, "Seel", "WATER", None, 65, 45, 55, 45, 70, 45),
    (87, "Dewgong", "WATER", "ICE", 90, 70, 80, 70, 95, 70),
    (88, "Grimer", "POISON", None, 80, 80, 50, 40, 50, 25),
    (89, "Muk", "POISON", None, 105, 105, 75, 65, 100, 50),
    (90, "Shellder", "WATER", None, 30, 65, 100, 45, 25, 40),
    (91, "Cloyster", "WATER", "ICE", 50, 95, 180, 85, 45, 70),
    (92, "Gastly", "GHOST", "POISON", 30, 35, 30, 100, 35, 80),
    (93, "Haunter", "GHOST", "POISON", 45, 50, 45, 115, 55, 95),
    (94, "Gengar", "GHOST", "POISON", 60, 65, 60, 130, 75, 110),
    (95, "Onix", "ROCK", "GROUND", 35, 45, 160, 30, 45, 70),
    (96, "Drowzee", "PSYCHIC", None, 60, 48, 45, 43, 90, 42),
    (97, "Hypno", "PSYCHIC", None, 85, 73, 70, 73, 115, 67),
    (98, "Krabby", "WATER", None, 30, 105, 90, 25, 25, 50),
    (99, "Kingler", "WATER", None, 55, 130, 115, 50, 50, 75),
    (100, "Voltorb", "ELECTRIC", None, 40, 30, 50, 55, 55, 100),
    (101, "Electrode", "ELECTRIC", None, 60, 50, 70, 80, 80, 140),
    (102, "Exeggcute", "GRASS", "PSYCHIC", 60, 40, 80, 60, 45, 40),
    (103, "Exeggutor", "GRASS", "PSYCHIC", 95, 95, 85, 125, 65, 55),
    (104, "Cubone", "GROUND", None, 50, 50, 95, 40, 50, 35),
    (105, "Marowak", "GROUND", None, 60, 80, 110, 50, 80, 45),
    (106, "Hitmonlee", "FIGHTING", None, 50, 120, 53, 35, 110, 87),
    (107, "Hitmonchan", "FIGHTING", None, 50, 105, 79, 35, 110, 76),
    (108, "Lickitung", "NORMAL", None, 90, 55, 75, 60, 75, 30),
    (109, "Koffing", "POISON", None, 40, 65, 95, 60, 45, 35),
    (110, "Weezing", "POISON", None, 65, 90, 120, 85, 70, 60),
    (111, "Rhyhorn", "GROUND", "ROCK", 80, 85, 95, 30, 30, 25),
    (112, "Rhydon", "GROUND", "ROCK", 105, 130, 120, 45, 45, 40),
    (113, "Chansey", "NORMAL", None, 250, 5, 5, 35, 105, 50),
    (114, "Tangela", "GRASS", None, 65, 55, 115, 100, 40, 60),
    (115, "Kangaskhan", "NORMAL", None, 105, 95, 80, 40, 80, 90),
    (116, "Horsea", "WATER", None, 30, 40, 70, 70, 25, 60),
    (117, "Seadra", "WATER", None, 55, 65, 95, 95, 45, 85),
    (118, "Goldeen", "WATER", None, 45, 67, 60, 35, 50, 63),
    (119, "Seaking", "WATER", None, 80, 92, 65, 65, 80, 68),
    (120, "Staryu", "WATER", None, 30, 45, 55, 70, 55, 85),
    (121, "Starmie", "WATER", "PSYCHIC", 60, 75, 85, 100, 85, 115),
    (122, "Mr. Mime", "PSYCHIC", None, 40, 45, 65, 100, 120, 90),
    (123, "Scyther", "BUG", "FLYING", 70, 110, 80, 55, 80, 105),
    (124, "Jynx", "ICE", "PSYCHIC", 65, 50, 35, 115, 95, 95),
    (125, "Electabuzz", "ELECTRIC", None, 65, 83, 57, 95, 85, 105),
    (126, "Magmar", "FIRE", None, 65, 95, 57, 100, 85, 93),
    (127, "Pinsir", "BUG", None, 65, 125, 100, 55, 70, 85),
    (128, "Tauros", "NORMAL", None, 75, 100, 95, 40, 70, 110),
    (129, "Magikarp", "WATER", None, 20, 10, 55, 15, 20, 80),
    (130, "Gyarados", "WATER", "FLYING", 95, 125, 79, 60, 100, 81),
    (131, "Lapras", "WATER", "ICE", 130, 85, 80, 85, 95, 60),
    (132, "Ditto", "NORMAL", None, 48, 48, 48, 48, 48, 48),
    (133, "Eevee", "NORMAL", None, 55, 55, 50, 45, 65, 55),
    (134, "Vaporeon", "WATER", None, 130, 65, 60, 110, 95, 65),
    (135, "Jolteon", "ELECTRIC", None, 65, 65, 60, 110, 95, 130),
    (136, "Flareon", "FIRE", None, 65, 130, 60, 95, 110, 65),
    (137, "Porygon", "NORMAL", None, 65, 60, 70, 85, 75, 40),
    (138, "Omanyte", "ROCK", "WATER", 35, 40, 100, 90, 55, 35),
    (139, "Omastar", "ROCK", "WATER", 70, 60, 125, 115, 70, 55),
    (140, "Kabuto", "ROCK", "WATER", 30, 80, 90, 55, 45, 55),
    (141, "Kabutops", "ROCK", "WATER", 60, 115, 105, 65, 70, 80),
    (142, "Aerodactyl", "ROCK", "FLYING", 80, 105, 65, 60, 75, 130),
    (143, "Snorlax", "NORMAL", None, 160, 110, 65, 65, 110, 30),
    (144, "Articuno", "ICE", "FLYING", 90, 85, 100, 95, 125, 85),
    (145, "Zapdos", "ELECTRIC", "FLYING", 90, 90, 85, 125, 90, 100),
    (146, "Moltres", "FIRE", "FLYING", 90, 100, 90, 125, 85, 90),
    (147, "Dratini", "DRAGON", None, 41, 64, 45, 50, 50, 50),
    (148, "Dragonair", "DRAGON", None, 61, 84, 65, 70, 70, 70),
    (149, "Dragonite", "DRAGON", "FLYING", 91, 134, 95, 100, 100, 80),
    (150, "Mewtwo", "PSYCHIC", None, 106, 110, 90, 154, 90, 130),
    (151, "Mew", "PSYCHIC", None, 100, 100, 100, 100, 100, 100)
]

# Compute min/max stats across the entire generation to scale 1-9
min_hp = min(p[4] for p in GEN1_DATA)
max_hp = max(p[4] for p in GEN1_DATA)

# CP is approximated using Attack + Special Attack + Speed
cp_raw = [(p[5] + p[7] + p[9]) for p in GEN1_DATA]
min_cp, max_cp = min(cp_raw), max(cp_raw)

min_def = min(p[6] for p in GEN1_DATA)
max_def = max(p[6] for p in GEN1_DATA)

def scale_1_to_9(value, min_val, max_val):
    """Maps a raw stat linearly into an integer scale from 1 to 9."""
    if max_val == min_val:
        return 5
    scaled = 1 + round(8 * (value - min_val) / (max_val - min_val))
    return int(max(1, min(9, scaled)))

# Build JSON dictionary
pokemon_list = []
for index, p in enumerate(GEN1_DATA):
    p_id, name, type1, type2, hp, atk, defense, spatk, spdef, speed = p
    
    types = [type1]
    if type2:
        types.append(type2)
        
    cp_value = cp_raw[index]
    
    pokemon_entry = {
        "id": p_id,
        "name": name,
        "types": types,
        "hp": scale_1_to_9(hp, min_hp, max_hp),
        "cp": scale_1_to_9(cp_value, min_cp, max_cp),
        "defense": scale_1_to_9(defense, min_def, max_def)
    }
    pokemon_list.append(pokemon_entry)

# Write out JSON file
output_filepath = "pokemon_gen1.json"
with open(output_filepath, "w", encoding="utf-8") as f:
    json.dump(pokemon_list, f, indent=2)

print(f"Successfully exported {len(pokemon_list)} Pokémon to '{output_filepath}'.")