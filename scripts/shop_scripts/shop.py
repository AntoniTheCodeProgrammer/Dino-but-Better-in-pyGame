from scripts.config import ITEMS

def has_item(game, item_id):
    return item_id in game.inventory.items

def buy_item(game, item_id):
    if item_id in ITEMS:
        price = ITEMS[item_id]["price"]
        if game.inventory.coins >= price and not has_item(game, item_id):
            game.inventory.coins -= price
            game.inventory.items.append(item_id)
            game.save_manager.save()
            return True
    return False
