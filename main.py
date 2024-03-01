import pygame
from board import Board

# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 100
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE, BLACK = (232, 235, 239), (125, 135, 150)

# The Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)


# Function to draw the checkered board
def draw_board():
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            text_surface = font.render(f"{(7-row)*8+(7-col)}", True, text_color)
            screen.blit(text_surface, (col*GRID_SIZE, row*GRID_SIZE))


def drawDragging(pieceLocal, mainBoardLocal, screenLocal):
    if pieceLocal is not None:
        mainBoardLocal.drawPossibleMoves(screen, mainBoardLocal.findPossibleMovesforClickedPiece())
        x, y = mainBoardLocal.bitBoardPos2Coords(pieceLocal.position)
        green_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(green_surface, GREEN, green_surface.get_rect())
        screenLocal.blit(green_surface, (y, x))
        screenLocal.blit(piece.image, (event.pos[0] - GRID_SIZE / 2, event.pos[1] - GRID_SIZE / 2))


# Initialize the screen
pygame.display.set_caption("Chess")
mainBoard = Board()
dragging = False
piece = None
GREEN = (0, 255, 0, 128)
# Game loop
while True:
    draw_board()
    mainBoard.drawBoardState(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            piece = mainBoard.pieceOnCoords(event=event)
            dragging = True
            drawDragging(piece, mainBoard, screen)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mainBoard.dropPiece(event=event)
            dragging = False
            piece = None
        elif dragging:
            drawDragging(piece, mainBoard, screen)
    if piece is not None:
        drawDragging(piece, mainBoard, screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
