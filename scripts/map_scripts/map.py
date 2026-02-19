import pygame
import json

def load_map(game, path):
    with open(path, 'r') as file:
        data = json.load(file)

    tile_size = data['tile_size']
    blocks = []
    gates = []
    
    for block in data['layers']['blocks']:
        x = block['pos'][0] * tile_size
        y = block['pos'][1] * tile_size
        rect = pygame.Rect(x, y, tile_size, tile_size)
        blocks.append({'rect': rect, 'asset': block['asset']})
        
    spawn_x = data['layers']['spawn'][0] * tile_size
    spawn_y = data['layers']['spawn'][1] * tile_size
    game.player.pos = [spawn_x, spawn_y]
    
    return blocks