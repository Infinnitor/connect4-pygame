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


# Class for each tile in the game, represents both a space on the grid and one in the Pygame window
class tile():
    def __init__(self, x, y, radius, padding):

        # Position of the tile on the grid
        self.x = x
        self.y = y

        # Radius that the tile will be drawn at
        self.radius = radius

        # The cube that forms around the circle is equal to the diameter, plus one quarter of the diameter
        self.square_side = ((radius + (radius // 4)) * 2)

        # Position on the Pygame window, based off of grid position
        self.gameX = x * self.square_side + padding[0]
        self.gameY = y * self.square_side + padding[1]

        # Status of the tile (either NONE, RED, or YELLOW)
        self.status = "NONE"

        # Easily accessible dictionary of the colours that the tile can drawn in
        self.colours = {"NONE" : (175, 175, 175), "RED" : (179, 45, 45), "YELLOW" : (255, 209, 18), "GREEN" : (92, 174, 89)}

    # Represents the class when printed
    def __repr__(self):
        return f"{self.status}, X:{self.x} Y:{self.y}"

    # Function for drawing the tile on the Pygame window
    def display(self):
        pygame.draw.circle(game.window, self.colours[self.status], (self.gameX, self.gameY), self.radius)

    # Function for easily changing the status of the tile
    def place(self, game):
        self.status = game.turn

    # Debugging function for highlighting the tile on the Pygame window
    def highlight(self):
        self.status = "GREEN"


# Function for checking if the mouse is over a given square, based off of a tile's position and square side
def mouse_check(obj, m_x, m_y):

    # Map that forms a bounding box for area that is being checked for mouse collision
    bounding_box = {
        "x1" : obj.gameX - (obj.square_side / 2),
        "y1" : obj.gameY - (obj.square_side / 2),
        "x2" : obj.gameX + (obj.square_side / 2),
        "y2" : obj.gameY + (obj.square_side / 2)
    }

    # A points system is used to check if the mouse satisfies all given requirements for intersection
    mouseover_points = 0
    # If the mouseX is within the width of the object
    if m_x > bounding_box["x1"]:
        mouseover_points += 1
    if m_x <= bounding_box["x2"]:
        mouseover_points += 1

    # If the mouseY is within the height of the object
    if m_y > bounding_box["y1"]:
        mouseover_points += 1
    if m_y <= bounding_box["y2"]:
        mouseover_points += 1

    # If all conditons are met, return True
    if mouseover_points == 4:
        return True

    # Return False otherwise
    return False


# Function for calculating the where to place a new piece, taking gravity into account
def place_column(column, game):

    # Iterate down through the given column
    for y in range(game.grid_size_y):
        tile_status = game.board[y][column].status

        # If it hits something, then place above
        if tile_status != "NONE":

            # If it's at the very top, then return False because column is thus full
            if y - 1 < 0:
                return (False, None)

            # Place it and return True to indicate that it was successful
            game.board[y - 1][column].place(game)
            return (True, game.board[y - 1][column])

        # If it's at the bottom, then place at the bottom and return True
        if y == game.grid_size_y - 1:
            game.board[y][column].place(game)
            return (True, game.board[y][column])

    # Safety clause
    return (False, None)


# Function for checking for a win in every possible direction
def check_win(game, tile):

    # Nested function that checks a list to see if there are four in a row of anything in it
    def check_list_four(list):

        # Define variables for tracking the number of subsequent tiles
        subsequent = 0
        previous = "NONE"

        # Loop through every item in the list
        for item in list:

            # Increase the counter if the item that you are currently on is the same as the last one
            if item.status == previous:
                subsequent += 1

            # Decrease it if the streak is broken
            else:
                subsequent = 1

            # Once you have checked the current item, set the previous variable to it for the next cycle
            previous = item.status

            # If there was a four in a row and it wasn't comprised of NONE, the return it
            if subsequent == 4 and item.status != "NONE":
                return item.status

        # Safety clause that returns NONE if there were no valid four-in-a-rows
        return "NONE"

    # Create a list for the horizontal, based on the Y position of the target piece
    row = game.board[tile.y]

    # Check the horizontal with check_list_four()
    check = check_list_four(row)

    # If it returned a valid four-in-a-row, return the winning item
    if check != "NONE":
        return check

    # For column, we have to use a for loop to get every item in the grid at a given X
    column = []
    for i in game.board:
        column.append(i[tile.x])

    # Same logic for checking applies
    check = check_list_four(column)
    if check != "NONE":
        return check

    # Diagonals are fucked up
    # First, we define a list for the left diagonal
    diag_left = []

    # Then we find the origin of left diagonal
    o_x = tile.x
    o_y = tile.y

    # Decreasing the potential origin X and Y until all wall is hit
    while o_x != 0 and o_y != 0:
        o_x -= 1
        o_y -= 1

    # We then go from the origin to the other wall, building the list as we go
    while o_x != 7 and o_y != 6:
        diag_left.append(game.board[o_y][o_x])
        o_x += 1
        o_y += 1

    # The list is then in a form where it can be checked by the check_list_four() function
    check = check_list_four(diag_left)
    if check != "NONE":
        return check

    # Right diagonal is even worse
    diag_right = []

    # We find the origin by going up and right
    o_x = tile.x
    o_y = tile.y
    while o_x != 6 and o_y != 0:
        o_x += 1
        o_y -= 1

    # We then decrease, but we have to be fucking careful because of order of events and shit, or else we get an incomplete list
    while o_x != -1 and o_y != 6:
        diag_right.append(game.board[o_y][o_x])
        o_x -= 1
        o_y += 1

    # And it can be checked by the function
    check = check_list_four(diag_right)
    if check != "NONE":
        return check

    # Safety clause
    return False


# Epic class that we use for all important game info, can be passed around easily
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

        # Current turn, red starts first
        self.turn = "RED"

        # We then create the screen
        self.window = pygame.display.set_mode((self.win_width, self.win_height))

        # And use create_matrix() to create a matrix filled with tile objects
        self.board = create_matrix(grid_size_y, grid_size_x, self)

        # Different colours that the bg will change to when hovered over
        self.hover_colours = {"YELLOW" : (153, 125, 10), "RED" : (77, 19, 19)}

    # Function for easily changing the current turn
    def change_turn(self):
        if self.turn == "RED":
            self.turn = "YELLOW"
        else:
            self.turn = "RED"


# Instantiating the class
game = game_info(
                tile_radius=50,
                padding=(100, 100),
                grid_size_x=7,
                grid_size_y=6,
                start_turn="RED")


# Is the gmae running??!??!?!?!
running = True
mouse_held = False

# THE mainloop amoug us
while running:

    # User input variables about whether the mouse was pressed, and where
    mouse_press = pygame.mouse.get_pressed()
    mouseX, mouseY = pygame.mouse.get_pos()

    hover_column = False

    # Set hover column to something valid by doing collision checks on every item on the board
    for y in game.board:
        for x in y:
            if mouse_check(x, mouseX, mouseY):
                hover_column = x

    # If there is an actual valid position for hover column, then draw a rectangle where it should be
    if hover_column:
        pygame.draw.rect(game.window, game.hover_colours[game.turn], (hover_column.gameX - (hover_column.square_side / 2), 0, hover_column.square_side, game.win_height))

        # If the mouse is pressed, and was not held down last loop
        if mouse_press[0] and not mouse_held:

            # Then try to place in the given
            placement = place_column(hover_column.x, game)

            # If the placement was successful, then check for victory
            if placement[0]:
                victory_check = check_win(game, placement[1])

                # If someone won, then print the winner and quit
                if victory_check:
                    print(victory_check)

                    # We have not made a nice win screen yet lol
                    pygame.quit()
                    quit()

                # If it wasn't a victory that turn, give control over to the next player
                else:
                    game.change_turn()

            mouse_held = True

        # If the mouse is not pressed, then allow it to be pressed in the next loop
        elif not mouse_press[0]:
            mouse_held = False

    # Display EVERYTHING
    for y in game.board:
        for x in y:
            x.display()

    # Update the window, the fill it for the next loop
    pygame.display.update()
    game.window.fill((0, 0, 0))

    # Check if the window is being closed
    for event in pygame.event.get():

        # Ye if the user closes the pygmae then close it bruv
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
