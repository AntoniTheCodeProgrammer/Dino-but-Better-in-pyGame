import pygame
import sys

from scripts.map_scripts.objects import Gate
from scripts.map_scripts.map import load_map

def map_loop(game):
    game.save_manager.save()

    blocks = load_map(game, 'scripts/map_scripts/map.json')

    while game.state == 'map':
        game.display.fill((0,0,0,0))
        game.display_2.blit(game.assets[map_data['background']], (0,0))

        scroll = [game.player.pos[0] - (game.display.get_width() / 2), game.player.pos[1] - (game.display.get_height() / 1.5)]

        for block in blocks:
            img = game.assets[block['asset']]

            render_x = block['rect'].x - scroll[0]
            render_y = block['rect'].y - scroll[1]

            game.display.blit(img, (render_x, render_y))

        # --- SKALOWANIE I UPDATE ---
        game.screen.blit(pygame.transform.scale(game.display, game.screen.get_size()), (0,0))
        pygame.display.update()
        
        # --- EVENTY ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    game.movement[0] = True
                if event.key == pygame.K_RIGHT: 
                    game.movement[1] = True
                if event.key == pygame.K_SPACE: 
                    game.player.jump()
                
                if event.key == pygame.K_ESCAPE:
                    game.state = 'start'

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: 
                    game.movement[0] = False
                if event.key == pygame.K_RIGHT: 
                    game.movement[1] = False

        game.clock.tick(60)