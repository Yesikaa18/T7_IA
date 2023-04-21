import pygame
import sys
import math
import time

# Inicializar Pygame
pygame.init()

# Definir las dimensiones de la ventana
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Definir los colores utilizados en el juego
BG_COLOR = (0, 0, 0)
LINE_COLOR = (201, 94, 255)
CIRCLE_COLOR = (255, 0, 255)  # rosa neón
CROSS_COLOR = (0, 255, 255)


# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Definir el tablero del juego
board = [[None, None, None], [None, None, None], [None, None, None]]

# Dibujar las líneas del tablero
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Dibujar las fichas del juego
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Colocar una ficha en el tablero
def mark_square(row, col, player):
    board[row][col] = player

# Comprobar si una celda está vacía
def is_available(row, col):
    return board[row][col] is None

# Comprobar si el tablero está lleno
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

# Comprobar si alguien ha ganado el juego
def check_win(player):
    # Comprobar filas
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Comprobar columnas
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Comprobar diagonales
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


# Algoritmo minimax


def minimax(player, max_depth=None, depth=0):
    if check_win("O"):
        return -10
    elif check_win("X"):
        return 10
    elif is_board_full():
        return 0
    elif max_depth is not None and depth >= max_depth:
        return 0

    if player == "X":
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax("O", max_depth, depth+1)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax("X", max_depth, depth+1)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score




def computer_move():
    computer_move = minimax("X", max_depth=None)
    best_score = -math.inf
    best_row = None
    best_col = None

   # best_row, best_col = computer_move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = "X"
                score = minimax("O")
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_row = row
                    best_col = col

    mark_square(best_row, best_col, "X")


def draw_board():
    draw_lines()
    draw_figures()


def reset_game():
    global board
    board = [[None, None, None], [None, None, None], [None, None, None]]
    screen.fill(BG_COLOR)
    draw_lines()


# Iniciar el juego
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del ratón
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            # Obtener la fila y columna correspondientes a la celda seleccionada
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            # Comprobar si la celda está disponible y hacer la jugada
            if is_available(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, "O")
                if check_win("O"):
                    print("¡Has ganado!")
                    reset_game()
                elif is_board_full():
                    print("Has perdido")

                else:
                    computer_move()
                    if check_win("X"):
                        print("¡La computadora ha ganado!")
                        reset_game()
                    elif is_board_full():
                        print("Empate")
                        reset_game()

    # Actualizar la pantalla
    draw_board()
    pygame.display.update()