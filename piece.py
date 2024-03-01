import pygame
import cairosvg
from io import BytesIO
import os

GRID_SIZE = 100
CURRENT_DIRECTORY = os.getcwd()

class Piece:
    def __init__(self, name, position):
        svg_file_path = os.path.join(CURRENT_DIRECTORY, "pieces", name+".svg")
        with open(svg_file_path, 'rb') as f:
            svg_data = f.read()
        svg_image =cairosvg.svg2png(file_obj=BytesIO(svg_data))
        image = pygame.image.load(BytesIO(svg_image)).convert_alpha()
        self.image = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
        self.name = name
        self.position = position




