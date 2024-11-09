import sys

import pygame
from pygame.locals import *
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


def reset_cells():
    global mat, path, open_set, closed_set
    mat = [[cell.Cell(col, row) for col in range(COLS)] for row in range(ROWS)]
    path.clear()
    open_set.clear()
    closed_set.clear()
    cell.start = cell.Cell(-1, -1)
    cell.goal = cell.Cell(-1, -1)


def get_fill_state(key) -> str:
    match key:
        case pygame.K_s:
            state = "start"
        case pygame.K_g:
            state = "goal"
        case pygame.K_u:
            state = "unwalkable"
        case _:
            state = "clear"
    return state


def setup_simulation():
    global fill_state
    reset_cells()
    while True:
        # delete last frame
        draw_grid(mat, CELL_SIZE)
        # update display
        pygame.display.update()
        # check for event
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # check for space to start simulation
                if event.key == pygame.K_SPACE:
                    if cell.start.x >= 0 and cell.goal.x >= 0:
                        # finish setup
                        print("finished setup")
                        return
                    else:
                        print("invalid start/goal!")

                # update fill state when appropriate button is pressed
                fill_state = get_fill_state(event.key)

            # if left msb is clicked, set cell state
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_handler()
            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def run_simulation():
    print("running simulation")
    success = find_path()
    if success:
        print("Found Path!")
    else:
        print("Path not found!")


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


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                return


def update_neighbors(start_cell):
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = start_cell.x + j
            y = start_cell.y + i
            if 0 <= x <= COLS - 1 and 0 <= y <= ROWS - 1:
                neighbour = mat[y][x]
                if neighbour.state != "unwalkable" and neighbour not in closed_set:
                    mat[y][x].calc_f(start_cell)
                    mat[y][x].parent = start_cell
                    heapq.heappush(open_set, mat[y][x])
                    if neighbour.state != "goal":
                        mat[y][x].set_state("open")


def append_to_path(cur_cell):
    x = cur_cell.x
    y = cur_cell.y

    if cur_cell == cell.start:
        path.append(cur_cell)
        mat[y][x].set_state("path")
        return
    append_to_path(cur_cell.parent)
    path.append(cur_cell)
    mat[y][x].set_state("path")
    return


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
    mat[cur_cell.y][cur_cell.x].set_state("closed")
    # break condition. reached goal
    if cur_cell.h == 0:
        append_to_path(cur_cell)
        return True
    # haven't reached goal yet:
    # update neighbors values, add them to the open set.
    update_neighbors(cur_cell)
    # next cell is the one with the smallest f
    if open_set:
        next_cell = heapq.heappop(open_set)
    else:
        return False

    # redraw cells
    draw_grid(mat, CELL_SIZE)
    pygame.display.update()

    # wait for keypress
    wait()

    found_path = find_next_cell(next_cell)

    if found_path:
        return True
    return False


def find_path():
    global path, open_set, closed_set, mat
    mat[cell.start.y][cell.start.x].calc_f(cell.start)

    found_path = find_next_cell(mat[cell.start.y][cell.start.x])
    draw_grid(mat, CELL_SIZE)
    pygame.display.update()
    return found_path


# start grid
# init cells matrix

mat = [[cell.Cell(col, row) for col in range(COLS)] for row in range(ROWS)]
path = []
open_set = []
closed_set = []
# main loop
fill_state = "clear"
while True:
    setup_simulation()
    # main algorithm loop:
    run_simulation()
    wait()
