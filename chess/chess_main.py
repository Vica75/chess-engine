import pygame
import pygame.draw

from chess import chess_engine

pygame.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (44, 80, 160)
LIGHT_YELLOW = (224, 224, 128)


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        # load images to the dictionary
        # can use SQ_SIZE because the actual piece pictures are a bit smaller than the png files themselves
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# This function is used to draw, the board, pieces, move suggestions, highlighting, etc,
def draw_gamestate(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs)


def draw_board(screen):
    colors = [LIGHT_YELLOW, LIGHT_BLUE]
    for row in range(DIMENSION):
        color_idx = row % 2
        for col in range(DIMENSION):
            pygame.draw.rect(screen, colors[color_idx], (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            color_idx = (color_idx + 1) % 2


def draw_pieces(screen, gs):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = gs.board[row][col]
            if piece != "--":
                piece_img = IMAGES[piece]
                screen.blit(piece_img, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game!")
    window.fill(DARK_BLUE)
    game_state = chess_engine.GameState()
    load_images()

    selected_square = ()
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE
                # if the user didn't choose the piece to move yet, we select the current piece
                # if a piece was already selected, we make a move and clear the selected_square tuple
                if selected_square == ():
                    if game_state.board[row][col] != "--":
                        selected_square = (row, col)
                else:
                    destination_square = (row, col)
                    move = chess_engine.Move(selected_square, destination_square, game_state.board)
                    game_state.make_move(move)
                    print(move.get_chess_notation())
                    selected_square = ()
            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    game_state.undo_move()

        draw_gamestate(window, game_state)
        clock.tick(MAX_FPS)
        pygame.display.flip()



if __name__ == "__main__":
    main()
