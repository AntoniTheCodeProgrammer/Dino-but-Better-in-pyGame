# scripts/loops/shop_loop.py
import pygame
import sys

from scripts.config import ITEMS
from scripts.shop_scripts.shop import buy_item, has_item

def shop_loop(game):    
    # Konfiguracja siatki
    ITEM_SIZE_X = 90
    ITEM_SIZE_Y = 50
    GAP = 10
    COLS = 3

    # Matematyka centrowania
    grid_width = (ITEM_SIZE_X * COLS) + (GAP * (COLS - 1))
    START_X = (game.display.get_width() - grid_width) // 2
    START_Y = 55 

    while game.state == 'shop':
        game.display.fill((50, 50, 100))

        # Obsługa myszki
        mouse_pos = pygame.mouse.get_pos()
        scale_x = game.display.get_width() / game.screen.get_width()
        scale_y = game.display.get_height() / game.screen.get_height()
        game_mouse = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)

        # --- Rysowanie Interfejsu ---
        title_img = game.font1.render('SHOP', True, (255, 185, 165))
        text_rect = title_img.get_rect(center=(game.display.get_width() // 2, 25))
        game.display.blit(title_img, text_rect)

        # Monety
        ui_padding = 8 
        coin_img = game.assets['coin']
        game.display.blit(coin_img, (ui_padding, ui_padding))
        coin_text = game.font2.render(f'{int(game.inventory.coins)}', True, (255, 255, 255))
        game.display.blit(coin_text, (ui_padding + coin_img.get_width() + 5, ui_padding + 2))

        # Serca
        heart_img = game.assets['heart']
        heart_y = ui_padding + 20 
        game.display.blit(heart_img, (ui_padding, heart_y))
        life_text = game.font2.render(f'{game.stats.health}', True, (255, 255, 255))
        game.display.blit(life_text, (ui_padding + heart_img.get_width() + 5, heart_y + 2))

        items_in_shop = ['double_jump', 'normal_walk', 'flamethrower', 'extra_life', 'fast_boots', 'more hearts']

        # --- Rysowanie Przedmiotów ---
        for i, item_id in enumerate(items_in_shop):
            row = i // COLS
            col = i % COLS
            x = START_X + col * (ITEM_SIZE_X + GAP)
            y = START_Y + row * (ITEM_SIZE_Y + GAP)

            item_rect = pygame.Rect(x, y, ITEM_SIZE_X, ITEM_SIZE_Y)

            # Hover (podświetlenie)
            if item_rect.collidepoint(game_mouse):
                pygame.draw.rect(game.display, (255, 255, 255), item_rect)
                text_color = (50, 50, 100)
            else:
                pygame.draw.rect(game.display, (50, 50, 50), item_rect)
                text_color = (255, 255, 255)

            is_bought = has_item(game, item_id)
            # Kolor nazwy (Kupiony / Stać / Nie stać)
            if is_bought:
                name_color = (255, 80, 80)
            elif game.inventory.coins >= ITEMS[item_id]['price']:
                name_color = (80, 255, 80)
            else:
                name_color = (150, 150, 150)

            # Renderowanie tekstów
            name_img = game.font2.render(ITEMS[item_id]['name'], True, name_color)
            game.display.blit(name_img, (x + 5, y + 5))
            
            price_text = "SOLD" if is_bought else str(ITEMS[item_id]['price'])
            price_img = game.font2.render(price_text, True, text_color)
            game.display.blit(price_img, (x + 5, y + 25))

        # Wyświetlanie na ekran
        game.screen.blit(pygame.transform.scale(game.display, game.screen.get_size()), (0,0))
        pygame.display.update()
        
        # --- Eventy ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Wyjście ze sklepu
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                    game.state = 'game'
                
                # Kupowanie klawiszami 1-9
                key_index = event.key - 49 
                buy_item(game, key_index)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # LPM
                    for i, item_id in enumerate(items_in_shop):
                        row = i // COLS
                        col = i % COLS
                        x = START_X + col * (ITEM_SIZE_X + GAP)
                        y = START_Y + row * (ITEM_SIZE_Y + GAP)
                        item_rect = pygame.Rect(x, y, ITEM_SIZE_X, ITEM_SIZE_Y)
                        
                        if item_rect.collidepoint(game_mouse):
                            buy_item(game, item_id)
                    
        game.clock.tick(60)