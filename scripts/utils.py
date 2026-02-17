import os
import pygame
import sys

def resource_path(relative_path):
    """ Pomaga odnaleźć pliki wewnątrz spakowanej aplikacji """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

BASE_IMG_PATH = resource_path('data/images/')

def load_image(path, colorkey=False):
    # Używamy os.path.join, żeby nie martwić się o ukośniki
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert_alpha()
    if colorkey:
        img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert()
        img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=False):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, path)
    
    # List comprehension - skraca kod do jednej pętli
    # Sortujemy, aby klatki animacji (np. 0.png, 1.png) były w dobrej kolejności
    for img_name in sorted(os.listdir(full_path)):
        if img_name.endswith('.png'):
            # Łączymy ścieżkę relatywną dla load_image
            images.append(load_image(os.path.join(path, img_name), colorkey=colorkey))
    return images

def load_spritesheet(path, frame_width, frame_height, scale=1, colorkey=False):
    full_sheet = load_image(path, colorkey=colorkey) # Używamy już istniejącej funkcji!
    sheet_width = full_sheet.get_width()
    num_frames = sheet_width // frame_width
    
    frames = []
    for i in range(num_frames):
        # Wycinamy fragment (subsurface nie kopiuje danych, więc jest szybkie)
        frame = full_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        
        if scale != 1:
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
        
    return frames

def invert_surface_colors(img):
    # 1. Tworzymy białą powierzchnię (bazę)
    inv = pygame.Surface(img.get_rect().size).convert()
    inv.fill((255, 255, 255))
    
    # 2. Odejmujemy od bieli nasz obrazek (255 - kolor = negatyw)
    # Używamy BLEND_RGB_SUB (odejmowanie kolorów)
    inv.blit(img, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
    
    # 3. Jeśli Twoje litery były CZARNE na BIAŁYM tle:
    # Teraz są BIAŁE na CZARNYM tle.
    # Musimy usunąć czarne tło:
    inv.set_colorkey((0, 0, 0))
    
    return inv

def scale_images(images, scale_factor):
    scaled_list = []
    for img in images:
        width = int(img.get_width() * scale_factor)
        height = int(img.get_height() * scale_factor)
        # Skalowanie obrazka
        scaled_img = pygame.transform.scale(img, (width, height))
        scaled_list.append(scaled_img)
    return scaled_list

def rotate_images(images, angle):
    new_images = []
    for img in images:
        rotated_img = pygame.transform.rotate(img, angle)
        new_images.append(rotated_img)
    return new_images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]