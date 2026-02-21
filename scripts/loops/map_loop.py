import pygame
import sys

from scripts.player.entities import Player
from scripts.map_scripts.map import load_map

def map_loop(game):
    game.save_manager.save()

    game.stats.reset()
    game.inventory.apply_passives(game)
    # game.upgrades.apply_passives(game)

    player = Player(game, (50,50), (14,14), animation_offset=(-9,-14)) 

    background, blocks, gates, interactables = load_map(game, 'scripts/map_scripts/map.json')

    game.movement = [0,0]
    game.dead = 0
    game.transition = -30

    scroll = [0, 0]

    while game.state == 'map':
        game.display.fill((0,0,0,0))
        game.display.blit(game.assets[background], (0,0))

        # Scroll
        target_x = player.pos[0] + (player.size[0] / 2) - (game.display.get_width() / 2)
        target_y = player.pos[1] + (player.size[1] / 2) - (game.display.get_height() / 2)
        scroll[0] += (target_x - scroll[0]) / 10
        scroll[1] += (target_y - scroll[1]) / 10
        render_scroll = (int(scroll[0]), int(scroll[1]))

        # BLOKI
        for block in blocks:
            img = game.assets[block['asset']]
            render_x = block['rect'].x - render_scroll[0]
            render_y = block['rect'].y - render_scroll[1]
            game.display.blit(img, (render_x, render_y))

        rects_gates = []
        # Objects
        for gate in gates:
            gate.render(game.display, render_scroll)
            if not gate.unlocked:
                rects_gates.append(gate.rect)

        for object in interactables:
            object.update()
            object.render(game.display, render_scroll)


        # Ruch gracza
        if not game.dead:
            rects_mapy = [block['rect'] for block in blocks]
            rects_mapy.extend(rects_gates)
            move_speed = (game.movement[1]-game.movement[0])
            player.update(movement=[move_speed, 0], colliders=rects_mapy)
        
        player.render(game.display, scroll=render_scroll)

        # decorations


        # --- UI (User Interface) ---
        ui_padding = 8 
        
        # Monety
        coin_img = game.assets['coin']
        game.display.blit(coin_img, (ui_padding, ui_padding))
        coin_text = game.font2.render(f'{int(game.inventory.coins)}', True, (255, 255, 255))
        game.display.blit(coin_text, (ui_padding + coin_img.get_width() + 5, ui_padding + 2))

        # Życia
        heart_img = game.assets['heart']
        heart_y = ui_padding + 20 
        game.display.blit(heart_img, (ui_padding, heart_y))
        life_text = game.font2.render(f'{game.stats.health}', True, (255, 255, 255))
        game.display.blit(life_text, (ui_padding + heart_img.get_width() + 5, heart_y + 2))


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
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP: 
                    player.jump()
                
                if event.key == pygame.K_ESCAPE:
                    game.state = 'start'

                if event.key == pygame.K_e:
                    player_rect = player.rect()
                    for object in interactables:
                        if player_rect.colliderect(object.rect):
                            object.use(game)
                            break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT: 
                    game.movement[0] = False
                if event.key == pygame.K_RIGHT: 
                    game.movement[1] = False

        game.clock.tick(60)