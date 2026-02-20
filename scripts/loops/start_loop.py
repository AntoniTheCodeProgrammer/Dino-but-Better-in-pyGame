import pygame
import sys

from scripts.save import SaveManager
from scripts.config import DEFAULT_STATE

def start_loop(game):
    menu_mode = 'main'

    while game.state == 'start':
        game.display.fill((0, 0, 0)) 

        # Obsługa myszki
        mouse_pos = pygame.mouse.get_pos()
        scale_x = game.display.get_width() / game.screen.get_width()
        scale_y = game.display.get_height() / game.screen.get_height()
        game_mouse = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_mode = 'main'

        # --- Rysowanie Interfejsu ---
        title_img = game.font1.render('CAT RUN', True, (255, 185, 165))
        text_rect = title_img.get_rect(center=(game.display.get_width() // 2, 25))
        game.display.blit(title_img, text_rect)

        def draw_button(text, y_pos):
            img = game.font1.render(text, True, (255, 255, 255))
            rect = img.get_rect(center=(game.display.get_width() // 2, y_pos))
            # Podświetlenie po najechaniu
            if rect.collidepoint(game_mouse):
                img = game.font1.render(text, True, (255, 0, 0)) 
                if mouse_click: 
                    return True
            game.display.blit(img, rect)
            return False

        if menu_mode == 'main':
            if draw_button('Nowa Gra', 70):
                menu_mode = 'new_game'
            if draw_button('Wczytaj Gre', 100):
                menu_mode = 'load_game'
                
        else:
            # Ekran wyboru slotu zapisu
            info_text = 'Nadpisz zapis:' if menu_mode == 'new_game' else 'Wczytaj zapis:'
            info_img = game.font1.render(info_text, True, (200, 200, 200))
            game.display.blit(info_img, info_img.get_rect(center=(game.display.get_width() // 2, 55)))

            for i in range(1, 4):
                if draw_button(f'Slot {i}', 70 + (i * 20)):
                    save_slot = "saves/gameslot" + str(i) + ".json"
                    game.save_manager = SaveManager(game, filename=save_slot)
                    
                    if menu_mode == 'new_game':
                        game.save_manager.apply_state(DEFAULT_STATE)
                        game.save()
                        pass
                    
                    game.save_manager.load()
                    game.state = 'game'

        

        game.screen.blit(pygame.transform.scale(game.display, game.screen.get_size()), (0,0))
        pygame.display.update()
        
        game.clock.tick(60)