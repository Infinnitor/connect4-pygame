import os


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
        matrix_print.append("\t".join(col))

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

        self.colours = {"NONE" : (175, 175, 175), "RED" : (179, 45, 45), "YELLOW" : (255, 209, 18), "GREEN" : (92, 174, 89)}

    def __repr__(self):
        # return f"{self.status}, X:{self.x} Y:{self.y}"
        return self.status

    def place(self, game):
        self.status = game.turn


def place_column(column, game):

    for y in range(6):
        tile_status = game.board[y][column].status
        if tile_status != "NONE":

            # Place y - 1 unless bottom row
            if y - 1 < 0:
                return (False, None)

            game.board[y - 1][column].place(game)
            return (True, game.board[y - 1][column])

        if y == game.grid_size_y - 1:
            game.board[y][column].place(game)
            return (True, game.board[y][column])

    return (False, None)


def check_win(game, tile):
    # do thing

    def check_list_four(list):

        subsequent = 0
        previous = "NONE"
        for item in list:
            if item.status == previous:
                subsequent += 1
            else:
                subsequent = 1

            previous = item.status

            if subsequent == 4 and item.status != "NONE":
                return item.status

        return "NONE"

    row = game.board[tile.y]
    check = check_list_four(row)
    if check != "NONE":
        return check

    column = []
    for i in game.board:
        column.append(i[tile.x])
    check = check_list_four(column)
    if check != "NONE":
        return check

    # Left diagonal
    diag_left = []

    # Find origin of left diagonal

    o_x = tile.x
    o_y = tile.y
    while o_x != 0 and o_y != 0:
        o_x -= 1
        o_y -= 1

    while o_x != 7 and o_y != 6:
        diag_left.append(game.board[o_y][o_x])
        o_x += 1
        o_y += 1

    check = check_list_four(diag_left)
    if check != "NONE":
        return check

    # Right diagonal
    diag_right = []

    # Find origin of left diagonal

    o_x = tile.x
    o_y = tile.y
    while o_x != 6 and o_y != 0:
        o_x += 1
        o_y -= 1

    while o_x != -1 and o_y != 6:
        diag_right.append(game.board[o_y][o_x])
        o_x -= 1
        o_y += 1

    check = check_list_four(diag_right)
    if check != "NONE":
        return check

    return False


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

        # And use create_matrix() to create a matrix filled with tile objects
        self.board = create_matrix(grid_size_y, grid_size_x, self)

        self.hover_colours = {"YELLOW" : (153, 125, 10), "RED" : (77, 19, 19)}

    def change_turn(self):
        if self.turn == "RED":
            self.turn = "YELLOW"
        else:
            self.turn = "RED"


def main():

    game = game_info(
                    tile_radius=50,
                    padding=(100, 100),
                    grid_size_x=7,
                    grid_size_y=6,
                    start_turn="RED")

    running = True

    # THE mainloop amoug us
    while running:

        os.system('cls')
        print_matrix(game.board)

        user_place = int(input("\nWhere do you want to place your piece?  ")) - 1

        if user_place > 6 or user_place < 0:
            input("Invalid placement [enter to continue]  ")
            continue

        placement = place_column(user_place, game)
        if placement[0]:

            victory_check = check_win(game, placement[1])
            if victory_check:
                print(f"{victory_check} wins!")
                quit()

            game.change_turn()

        else:
            input("Invalid placement [enter to continue]  ")


main()
