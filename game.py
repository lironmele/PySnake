import snake, pygame, sys
from pygame.locals import *
import colors

def draw_board(screen, dimensions):
    w, h = screen.get_size()
    dw, dh = dimensions
    for x in range(w//dw, w, w//dw):
        pygame.draw.line(screen, colors.WHITE, (x, 0), (x, h))
    for y in range(h//dh, h, h//dh):
        pygame.draw.line(screen, colors.WHITE, (0, y), (w, y))

def draw_snake(screen, board, x_step, y_step):
    x, y = 0, 0
    for row in board.split("\n"):
        for c in row:
            if c == " ":
                pass
            elif c == "+":
                # draw head
                pygame.draw.rect(screen, colors.GREEN, (x+x_step*0.25, y+y_step*0.25, x_step*0.5, y_step*0.5), 5)
            elif c == "-":
                # draw body
                pygame.draw.rect(screen, colors.GREEN, (x+x_step*0.25, y+y_step*0.25, x_step*0.5, y_step*0.5))
            elif c == "o":
                # draw cherry
                pygame.draw.rect(screen, colors.CHERRY_RED, (x+x_step*0.25, y+y_step*0.25, x_step*0.5, y_step*0.5))
            x += x_step
        x = 0
        y += y_step

board = snake.Board([10,10])
screen_size = (900,900)
x_step, y_step = [screen_size[0]//board.dimensions[0], screen_size[1]//board.dimensions[1]]

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
tick = 0
key = ""

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_UP]:
                key = "w"
            elif event.key in [pygame.K_a, pygame.K_LEFT]:
                key = "a"
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                key = "s"
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                key = "d"
    if tick == 15:
        board.update(user_input=key)
        key = ""
        tick = 0
    else:
        tick += 1

    screen.fill(colors.BLACK)
    draw_board(screen, board.dimensions)
    draw_snake(screen, str(board), x_step, y_step)

    if board.game_ended:
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, colors.WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, (text_x, text_y))

    pygame.display.update()
    clock.tick(30)
