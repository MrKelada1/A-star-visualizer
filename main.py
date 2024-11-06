import pygame
import cell
import math, heapq

# initialize pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 10
COLS = 10
CELL_SIZE = SCREEN_HEIGHT / ROWS
screen = pygame.display.set_mode(((SCREEN_WIDTH, SCREEN_HEIGHT)))


# create grid of cells, some of them aren't walkable
def draw_grid(cells_mat, cell_size):
    # draw cells
    for row in range(ROWS):
        for col in range(COLS):
            c = cells_mat[row][col]
            rect = pygame.Rect(c.x * cell_size, c.y * cell_size, cell_size, cell_size)
            rect.scale_by_ip(0.9, 0.9)
            pygame.draw.rect(screen, c.color, rect)


def mouse_click_handler():
    """
    Handles mouse clicks.
    left click sets a cell to currently chosen state, right click clears it.
    setting start and goal states clears the old start/goal.
    """
    global mat
    # get which mouse data
    (l_click, m_click, r_click) = pygame.mouse.get_pressed(3)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # position to matrix indices
    x, y = math.floor(mouse_x / CELL_SIZE), math.floor(mouse_y / CELL_SIZE)
    if l_click:
        # clear old start/goal if needed and set the current start/goal xy
        if fill_state == "start":
            mat[cell.start.y][cell.start.x].set_state("clear")
            cell.start.x = x
            cell.start.y = y
        elif fill_state == "goal":
            mat[cell.goal.y][cell.goal.x].set_state("clear")
            cell.goal.x = x
            cell.goal.y = y
        # set state for current cell
        mat[y][x].set_state(fill_state)
    # clear cell on mouse right click
    elif r_click:
        mat[y][x].set_state("clear")


def update_neighbors(start_cell):
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = start_cell.x + j
            y = start_cell.y + i
            if 0 <= x <= COLS - 1 and 0 <= y <= ROWS - 1:
                neighbour = mat[y][x]
                if neighbour.state != "unwalkable" and neighbour not in closed_set:
                    mat[y][x].calc_f(start_cell)
                    heapq.heappush(open_set, mat[y][x])


def find_next_cell(cur_cell):
    """
    Moves to the next optimal cell in matrix.
    if the next cell is the goal, add it to path and return, then add each one previous one and return.
    if there's nowhere to advance, and the goal wasn't reached,
    :param cur_cell: current cell
    :return:
    """

    # add cell to the closed set
    heapq.heappush(closed_set, cur_cell)
    # mat[cur_cell.y][cur_cell.x].set_state("closed")
    # break condition. reached goal
    if cur_cell.h == 0:
        path.append(cur_cell)
        return True
    # haven't reached goal yet:
    # update neighbors values, add them to the open set.
    update_neighbors(cur_cell)
    # next cell is the one with the smallest f
    if open_set:
        next_cell = heapq.heappop(open_set)
    else:
        return False

    found_path = find_next_cell(next_cell)

    if found_path:
        path.append(cur_cell)
        if not (cur_cell.state == "start"):
            mat[cur_cell.y][cur_cell.x].set_state("path")
        return True
    return False


def find_path():
    global path, open_set,closed_set, mat
    mat[cell.start.y][cell.start.x].calc_f(cell.start)

    found_path = find_next_cell(mat[cell.start.y][cell.start.x])
    return found_path


# start grid
# init cells matrix
mat = [[cell.Cell(col, row) for col in range(COLS)] for row in range(ROWS)]
path = []
open_set = []
closed_set = []

# main loop
run = True
setup_phase = True
fill_state = "clear"
while run:
    # delete last frame
    draw_grid(mat, CELL_SIZE)
    # check for event
    for event in pygame.event.get():
        # if in setup stage and mouse click or key press:
        if setup_phase:
            # if keyboard is pressed, update fill state
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_s:
                        fill_state = "start"
                    case pygame.K_g:
                        fill_state = "goal"
                    case pygame.K_u:
                        fill_state = "unwalkable"
                    case pygame.K_SPACE:
                        # start a* algorithm
                        setup_phase = False
                        # for cell in path:
                            # mat[cell.y][cell.x].set_state("clear")
                    case _:
                        fill_state = "clear"

            # if left msb is clicked, set cell state
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_handler()
        # quit event
        if event.type == pygame.QUIT:
            run = 0
    # main algorithm loop:
    if not setup_phase:
        success=find_path()
        if success:
            print("Found Path!")
        else:
            print("Path not found!")

        setup_phase = True
    # update display
    pygame.display.update()

# quit app
pygame.quit()
