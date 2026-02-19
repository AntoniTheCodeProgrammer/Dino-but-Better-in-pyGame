# scripts/loops/game_loop.py
import pygame
import sys

from scripts.run_scripts.level import load_level, gen_obstacle, gen_platform
from scripts.run_scripts.ground import Ground
from scripts.config import LEVELS

def game_loop(game):
    load_level(game)   
    boss_fight = False
    
    invincibility = 0
    health = game.full_HP

    while game.state == 'game':
        # 1. Rysowanie Tła i Podłogi
        game.display.fill((0,0,0,0))
        game.display_2.blit(game.assets['background'], (0,0))
        game.ground = Ground(game, 164, LEVELS[game.level]['ground'])
        game.ground.render(game.display)
        
        # Efekt przejścia (kółko na starcie)
        if game.transition < 0:
            game.transition += 1

        # --- EKRAN ŚMIERCI ---
        if game.dead:
            text_img = game.font1.render('YOU LOST', True, (255, 225, 205))
            text_rect = text_img.get_rect(center=(game.display.get_width() // 2, 45))
            game.display.blit(text_img, text_rect)
            
            text_img = game.font1.render(f'Points: {int(game.points)}', True, (255, 255, 255))
            text_rect = text_img.get_rect(center=(game.display.get_width() // 2, 70))
            game.display.blit(text_img, text_rect)
            
            text_img = game.font2.render('press space to restart', True, (55, 155, 255))
            text_rect = text_img.get_rect(center=(game.display.get_width() // 2, 100))
            game.display.blit(text_img, text_rect)
            
            text_img = game.font2.render('press s to go shopping', True, (55, 155, 255))
            text_rect = text_img.get_rect(center=(game.display.get_width() // 2, 120))
            game.display.blit(text_img, text_rect)              
                    
        # Tło serduszek
        game.hearts.update()
        game.hearts.render(game.display_2)
        
        # --- GENEROWANIE PRZESZKÓD LUB PLATFORM ---
        if boss_fight:
            gen_platform(game)
        else:
            gen_obstacle(game)

        # Licznik nieśmiertelności
        if invincibility > 0:
            invincibility -= 1

        # --- UPDATE PRZESZKÓD ---
        for obstacle in game.obstacles.copy():
            obstacle.update(alive=game.dead, speed=game.level)
            
            # Usuwanie poza ekranem
            if obstacle.pos[0] < -50:
                game.obstacles.remove(obstacle)
            
            # Kolizje (tylko jak nie jest nieśmiertelny)
            if invincibility == 0:
                if game.player.rect().colliderect(obstacle.rect):
                    if health > 1:
                        health -= 1
                        invincibility = 120 # 2 sekundy ochrony
                    elif health == 1:
                        health = 0
                        game.dead = 1

            # Renderowanie (miganie przy obrażeniach)
            if invincibility > 0:
                if invincibility % 10 < 5:
                    obstacle.render(game.display)
            else:
                obstacle.render(game.display)

        # --- UPDATE PLATFORM ---
        for platform in game.platforms.copy():
            platform.update(alive=game.dead, speed=game.level)
            
            # Usuwanie poza ekranem
            if platform.pos[0] < -50:
                game.platforms.remove(platform)

            platform.render(game.display)

        # --- UPDATE MONET ---
        for coin in game.coinsObjects.copy():
            coin.update(alive=game.dead, speed=game.level)
            if coin.pos[0] < -50:
                game.coinsObjects.remove(coin)
            if game.player.rect().colliderect(coin.rect):
                game.coinsObjects.remove(coin)
                game.coins += 1
            coin.render(game.display)

        # --- UPDATE GRACZA ---
        if not game.dead:
            # Obliczanie prędkości ruchu tła / game.fast_boots * game.normal_walk
            move_speed = (game.movement[1]-game.movement[0]) / 2
            game.player.update(movement=[move_speed, 0])
            
            game.points += 0.03
            # game.player.update_flamethrower()
        
        game.player.render(game.display)

        if not boss_fight and game.points >= LEVELS[game.level]['length']:
            if LEVELS[game.level]['boss'] == -1:
                game.state = 'map'
            else:
                boss_fight = True

        # --- UI (User Interface) ---
        ui_padding = 8 
        
        # Monety
        coin_img = game.assets['coin']
        game.display.blit(coin_img, (ui_padding, ui_padding))
        coin_text = game.font2.render(f'{int(game.coins)}', True, (255, 255, 255))
        game.display.blit(coin_text, (ui_padding + coin_img.get_width() + 5, ui_padding + 2))

        # Życia
        heart_img = game.assets['heart']
        heart_y = ui_padding + 20 
        game.display.blit(heart_img, (ui_padding, heart_y))
        life_text = game.font2.render(f'{health}', True, (255, 255, 255))
        game.display.blit(life_text, (ui_padding + heart_img.get_width() + 5, heart_y + 2))

        # Punkty
        score_text = game.font2.render(f'Score: {int(game.points)}', True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(game.display.get_width() - ui_padding, ui_padding))
        game.display.blit(score_text, score_rect)

        # Ramka (Winieta)
        display_mask = pygame.mask.from_surface(game.display)
        display_sillhouette = display_mask.to_surface(setcolor=(0,0,0,100), unsetcolor=(0,0,0,0))
        for offset in [(-1,0), (1,0), (0,-1), (0,1)]:
            game.display_2.blit(display_sillhouette, offset)
        
        # --- STEROWANIE ---
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
                    if not game.dead:
                        game.player.jump()
                    else:
                        health = game.full_HP
                        load_level(game)      
                if event.key == pygame.K_r:
                    health = max(1, health)
                    load_level(game)
                    game.transition = -30
                if event.key == pygame.K_ESCAPE:
                    game.state = 'map'
                # if event.key == pygame.K_f and 'flamethrower' in game.inventory:
                #    if not game.dead:
                #         game.player.active_flametrower()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    game.movement[1] = False
                    
        # --- RYSOWANIE KOŃCOWE ---
        # Efekt wejścia (kółko)
        if game.transition:
            transition_surf = pygame.Surface(game.display.get_size())
            pygame.draw.circle(transition_surf, (255, 255, 255), (game.display.get_width() // 2, game.display.get_height() // 2), (30 - abs(game.transition)) * 8)
            transition_surf.set_colorkey((255, 255, 255))
            game.display.blit(transition_surf, (0, 0))
        
        # Skalowanie na cały ekran
        game.display_2.blit(game.display, (0,0))
        game.screen.blit(pygame.transform.scale(game.display_2, game.screen.get_size()), (game.screenshake, game.screenshake))
        pygame.display.update()
        game.clock.tick(60)