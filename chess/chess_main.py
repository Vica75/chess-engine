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
def draw_gamestate(screen, gs, legal_moves, selected_square):
    draw_board(screen)
    draw_pieces(screen, gs)
    if selected_square:
        draw_selected(screen, selected_square)
    # draw_legal_moves(screen, legal_moves)


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


def draw_legal_moves(screen, legal_moves):
    sq_width = sq_height = 10
    for move in legal_moves:
        x = move.end_col * SQ_SIZE + SQ_SIZE/2 - 5
        y = move.end_row * SQ_SIZE + SQ_SIZE / 2 - 5
        pygame.draw.rect(screen, DARK_BLUE, (x, y, sq_width, sq_height))


def draw_selected(screen, pos):
    x = pos[1] * SQ_SIZE
    y = pos[0] * SQ_SIZE
    pygame.draw.rect(screen, DARK_BLUE, (x, y, SQ_SIZE, SQ_SIZE), 3)


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game!")
    window.fill(DARK_BLUE)
    game_state = chess_engine.GameState()
    load_images()

    selected_square = ()
    valid_moves = game_state.get_legal_moves()
    # valid_moves = [chess_engine.Move((1, 0), (2, 0), game_state.board)]  # test code
    move_made = False

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
                # we only allow to choose a black piece if it's black's move, the same with white
                if (not selected_square and game_state.board[row][col] != "--" and
                        (game_state.white_to_move and game_state.board[row][col][0] == "w" or
                         not game_state.white_to_move and game_state.board[row][col][0] == "b")):
                    selected_square = (row, col)
                    print(selected_square)
                elif selected_square:
                    destination_square = (row, col)
                    move = chess_engine.Move(selected_square, destination_square, game_state.board)
                    if move in valid_moves:
                        game_state.make_move(move)
                        print(move.get_chess_notation())
                        selected_square = ()
                        move_made = True
                    else:
                        selected_square = ()

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    game_state.undo_move()
                    move_made = True

        # we want to generate new moves only when a new move was made
        # otherwise the legal moves stay the same
        if move_made:
            valid_moves = game_state.get_legal_moves()

        draw_gamestate(window, game_state, valid_moves, selected_square)

        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
