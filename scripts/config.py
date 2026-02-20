ITEMS = {
    'double_jump': {'name': 'Double Jump', 'price': 3, 'desc': 'Jump twice!'},
    'normal_walk': {'name': 'Normal Walk', 'price': 1, 'desc': 'End of saffering'},
    'flamethrower': {'name': 'Flamethrower', 'price': 7, 'desc': 'Burn enemies!'},
    'extra_life': {'name': 'Extra Life', 'price': 5, 'desc': '+1 Heart'},
    'magic_boots': {'name': 'Fast Boots', 'price': 4, 'desc': 'Run faster'},
    'more hearts': {'name': 'More Hearts', 'price': 10, 'desc': '??? <3 ???'},
}

DEFAULT_STATE = {
    'coins': 0,
    'inventory': [],
    'unlocked_gates': [],
    'current_level': 0
}

BOSSES = {
    0: {'name': 'zoroar', 'hp': 5, 'asset': 'boss_1'},
    1: {'name': 'arrator', 'hp': 10, 'asset': 'boss_2'},
}

LEVELS = {
    0: {'name': 'garden', 'ground': 'grass', 'length': 100, 'boss': 0, 'bg': 'bg_0'},
    1: {'name': 'forest', 'ground': 'dirt', 'length': 5000, 'boss': -1, 'bg': 'bg_1'},
    2: {'name': 'cave', 'ground': 'stone', 'length': 3000, 'boss': 1, 'bg': 'bg_2'},
}