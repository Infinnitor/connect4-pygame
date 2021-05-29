import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
pygame.init()  # become britsh


# Function for creating a matrix, given the size
def create_matrix(rows_len, columns_len):

    # We first create an empty array
    grid_array = []

    # For the desired length, we create a row
    for row in range(rows_len):
        grid_array.append([])

        # For every desired element in that row, we add in the insert
        for column in range(columns_len):
            grid_array[row].append(tile(y=row, x=column, radius=tile_radius, padding=padding))

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
        return self.status

    def display(self):
        pygame.draw.circle(window, self.colours[self.status], (self.gameX, self.gameY), self.radius)

    def place(self, turn):
        self.status = turn


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


def place_column(column):
    global turn
    # find the lowest empty space in the column
    for x in board:
        for y in board:
            if x.x == column:
                # if its not empty
                #    place in the one above
                # if its in the bottom row
                #    place in itself
                if x.status != "NONE":
                    board[x.y - 1][x.x].place(turn)
                elif x.y == 5:
                    x.place(turn)
                else:
                    return False

                if turn == "RED":
                    turn = "YELLOW"
                else:
                    turn = "RED"
                return True


# Variables that determine info about the tiles
tile_radius = 50
padding = (100, 100)

# Variables for the size of the grid (7x6)
grid_size_x = 7
grid_size_y = 6

# We use MATHS to find out how big the screen should be
win_width = grid_size_x * ((tile_radius + tile_radius // 4) * 2) + padding[0]
win_height = grid_size_y * ((tile_radius + tile_radius // 4) * 2) + padding[1]

# We then create the screen
window = pygame.display.set_mode((win_width, win_height))

# And use create_matrix() to create a matrix filled with tile objects
board = create_matrix(grid_size_y, grid_size_x)

# THE mainloop amoug us

turn = "RED"
running = True
while running:
    for y in board:
        for x in y:
            x.display()

    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0]:
        mouseX, mouseY = pygame.mouse.get_pos()

        # for i in range(7):
        #     if mouseX > (win_height / 6) * i and mouseX < (win_height / 6) * (i + 1):
        #         pygame.draw.rect(window, (155, 155, 155), (((win_height - padding) / 6) * i, 0, (win_height - padding) / 7, win_height))
        #         print(i)

        for y in board:
            for x in y:
                if mouse_check(x, mouseX, mouseY):
                    x.place(turn)

    for event in pygame.event.get():

        # Ye if the user closes the pygmae then close it bruv
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    pygame.display.update()
    window.fill((0, 0, 0))
