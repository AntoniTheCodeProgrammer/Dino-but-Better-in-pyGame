import pygame
import json

from scripts.map_scripts.objects import Gate, Level, Shop

def load_map(game, path):
    with open(path, 'r') as file:
        data = json.load(file)

    tile_size = data['tile_size']
    
    blocks = []
    gates = []
    interactables = []

    background = data['layers']['background']
    
    for block in data['layers']['blocks']:
        x = block['pos'][0] * tile_size
        y = block['pos'][1] * tile_size
        rect = pygame.Rect(x, y, tile_size, tile_size)
        blocks.append({'rect': rect, 'asset': block['asset']})

    for object in data['layers']['objects']:
        match object['type']:
            case 'gate':
                px_x = object['pos'][0] * tile_size
                px_y = object['pos'][1] * tile_size
                gates.append(Gate(game, pos=[px_x, px_y], id=object['id']))

            case 'level': 
                px_x = object['pos'][0] * tile_size
                px_y = object['pos'][1] * tile_size
                interactables.append(Level(game, pos=[px_x, px_y], id=object['id'], lv=object['lv']))

            case 'shop': 
                px_x = object['pos'][0] * tile_size
                px_y = object['pos'][1] * tile_size
                interactables.append(Shop(game, pos=[px_x, px_y], id=object['id']))
        
    spawn_x = data['spawn'][0] * tile_size
    spawn_y = data['spawn'][1] * tile_size
    game.player.pos = [spawn_x, spawn_y]
    
    return  background, blocks, gates, interactables