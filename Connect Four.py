import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
pygame.init()  # become britsh


# Function for creating a matrix, given the size
def create_matrix(rows_len, columns_len, game):

    # We first create an empty array
    grid_array = []

    # For the desired length, we create a row
    for row in range(rows_len):
        grid_array.append([])

        # For every desired element in that row, we add in the insert
        for column in range(columns_len):
            grid_array[row].append(tile(y=row, x=column, radius=game.tile_radius, padding=game.padding))

    # We then return the array
    return grid_array


# Function for printing out a matrix in a readable manner. The function takes a matrix (list of lists) as a parameter
def print_matrix(matrix):

    # We create an empty array that will hold all our rows
    matrix_print = []
    for row in matrix:
        col = []
        for column in row:
            col.append(str(column))

        # We join up col, and add it to the matrix_print list
        matrix_print.append(", ".join(col))

    # We then join up matrix_print and display it
    print("\n".join(matrix_print))

    return


class tile():
    def __init__(self, x, y, radius, padding):
        self.x = x
        self.y = y

        self.radius = radius

        # The cube that forms around the circle is equal to the diameter, plus one quarter of the diameter
        self.square_side = ((radius + (radius // 4)) * 2)

        self.gameX = x * self.square_side + padding[0]
        self.gameY = y * self.square_side + padding[1]

        self.status = "NONE"

        self.colours = {"NONE" : (175, 175, 175), "RED" : (179, 45, 45), "YELLOW" : (255, 209, 18)}

    def __str__(self):
        return f"{self.status}, X:{self.x} Y:{self.y}"

    def display(self):
        pygame.draw.circle(game.window, self.colours[self.status], (self.gameX, self.gameY), self.radius)

    def place(self, game):
        self.status = game.turn


def mouse_check(obj, m_x, m_y):
    bounding_box = {
        "x1" : obj.gameX - (obj.square_side / 2),
        "y1" : obj.gameY - (obj.square_side / 2),
        "x2" : obj.gameX + (obj.square_side / 2),
        "y2" : obj.gameY + (obj.square_side / 2)
    }

    mouseover_points = 0
    # If the mouseX is within the width of the object
    if m_x > bounding_box["x1"]:
        mouseover_points += 1
    if m_x < bounding_box["x2"]:
        mouseover_points += 1

    # If the mouseY is within the height of the object
    if m_y > bounding_box["y1"]:
        mouseover_points += 1
    if m_y < bounding_box["y2"]:
        mouseover_points += 1

    # If all conditons are met, return True
    if mouseover_points == 4:
        return True

    # Return False otherwise
    return False


def place_column(tile, game):

    column = tile.x

    for y in range(6):
        tile_status = game.board[y][column].status
        print(game.board[y][column])
        if tile_status != "NONE":
            # place y-1 unless top row
            if y - 1 < 0:
                print("UH OH")
                return False
            game.board[y - 1][column].place(game)
            return True
        if y == 5:
            game.board[y][column].place(game)
            return True
    return True


class game_info():
    def __init__(self, tile_radius, padding, grid_size_x, grid_size_y, start_turn):

        # Variables that determine info about the tiles
        self.tile_radius = tile_radius
        self.padding = padding

        # Variables for the size of the grid (7x6)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        # We use MATHS to find out how big the screen should be
        self.win_width = grid_size_x * ((tile_radius + tile_radius // 4) * 2) + padding[0]
        self.win_height = grid_size_y * ((tile_radius + tile_radius // 4) * 2) + padding[1]

        self.turn = "RED"

        # We then create the screen
        self.window = pygame.display.set_mode((self.win_width, self.win_height))

        # And use create_matrix() to create a matrix filled with tile objects
        self.board = create_matrix(grid_size_y, grid_size_x, self)

    def change_turn(self):
        if self.turn == "RED":
            self.turn = "YELLOW"
        else:
            self.turn = "RED"


game = game_info(
                tile_radius=50,
                padding=(100, 100),
                grid_size_x=7,
                grid_size_y=6,
                start_turn="RED")


running = True
mouse_held = False

# THE mainloop amoug us
while running:
    for y in game.board:
        for x in y:
            x.display()

    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0] and not mouse_held:
        mouseX, mouseY = pygame.mouse.get_pos()

        for y in game.board:
            for x in y:
                if mouse_check(x, mouseX, mouseY):
                    place_column(x, game)
                    game.change_turn()

        mouse_held = True

    elif not mouse_press[0]:
        mouse_held = False

    for event in pygame.event.get():

        # Ye if the user closes the pygmae then close it bruv
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    pygame.display.update()
    game.window.fill((0, 0, 0))
