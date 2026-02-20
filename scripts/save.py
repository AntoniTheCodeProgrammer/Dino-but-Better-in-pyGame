import json
import os
from scripts.config import DEFAULT_STATE


class SaveManager:
    def __init__(self, game, filename="saves/savegame.json"):
        self.game = game
        self.filename = filename

    def save(self):
        data = {
            "coins": self.game.coins,
            "inventory": self.game.inventory,
            "unlocked_gates": self.game.unlocked_gates,
            "stats": self.game.stats,
        }

        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
            print("Gra zapisana!")
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    def load(self):
        if not os.path.exists(self.filename):
            print("Brak pliku zapisu, nowa gra.")
            self.apply_state(DEFAULT_STATE)
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            self.apply_state(data)
            print("Gra wczytana!")
        except Exception as e:
            print(f"Błąd wczytywania (plik uszkodzony?): {e}")
            self.apply_state(DEFAULT_STATE)

    def apply_state(self, data):
        self.game.coins = data.get("coins", 0)
        self.game.inventory = data.get("inventory", [])
        self.game.unlocked_gates = data.get("unlocked_gates", [])
        self.game.stats = data.get("stats", {"lives": 1, "damage": 1})

    
