# RED: U+1F534
# YELLOW: U+1F7E1
# WHITE: U+26AA


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
def return_matrix(matrix):

    # We create an empty array that will hold all our rows
    matrix_print = []
    for row in matrix:
        col = []
        for column in row:
            col.append(str(column))

        # We join up col, and add it to the matrix_print list
        matrix_print.append("\t".join(col))

    # We then join up matrix_print and display it
    final_matrix = "\n".join(matrix_print)

    return final_matrix


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
        return self.status

    # Function for easily changing the status of the tile
    def place(self, game):
        self.status = game.turn


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

        # Current turn, red starts first
        self.turn = "RED"

        # And use create_matrix() to create a matrix filled with tile objects
        self.board = create_matrix(grid_size_y, grid_size_x, self)

    # Function for easily changing the current turn
    def change_turn(self):
        if self.turn == "RED":
            self.turn = "YELLOW"
        else:
            self.turn = "RED"


# Instantiating the game_info class
game = game_info(
                tile_radius=50,
                padding=(100, 100),
                grid_size_x=7,
                grid_size_y=6,
                start_turn="RED")


# THE mainloop amoug us
def take_turn(player_column):

    # Ask the user for input (not sanitised yet lol)
    user_place = player_column

    # If the input is off the grid, declare it invalid
    if user_place > 6 or user_place < 0:
        return (False, None)

    # Placing the piece in the desired column
    placement = place_column(user_place, game)
    if placement[0]:

        # Check for victory if the placement was valid
        victory_check = check_win(game, placement[1])
        if victory_check:
            return "WIN"

        # Change the turn
        game.change_turn()

    # If the placement was invalid, say so
    else:
        return (False, None)

    return (True, game.board)
