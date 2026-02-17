

def buy_item(game, index):
    if 0 <= index < len(game.items):
        item = game.items[index]
            
        # Główny warunek kupna
        if game.coins >= item['price'] and not item['bought']:
            game.coins -= item['price']
            item['bought'] = True
                
            # --- Aplikowanie efektów ---
            if index == 0: 
                game.double_jump = True
            elif index == 1: 
                game.normal_walk = 1
            elif index == 2: 
                game.flametrower = True
            elif index == 3: 
                game.lives += 1
            elif index == 4: 
                game.fast_boots = 1.5
            elif index == 5: 
                game.hearts_count = 128
