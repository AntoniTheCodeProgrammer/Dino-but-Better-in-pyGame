# scripts/loops/menu_loop.py
import pygame
import sys

def start_loop(game):
    while game.state == 'start':
        game.display.fill((0, 0, 0)) 
        
        title_text = game.font1.render("CAT RUN", True, (255, 255, 255))
        start_text = game.font2.render("Press SPACE to Start", True, (200, 200, 200))
        
        game.display.blit(title_text, (120, 50))
        game.display.blit(start_text, (100, 100))

        game.screen.blit(pygame.transform.scale(game.display, game.screen.get_size()), (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.state = 'game'
        
        game.clock.tick(60)