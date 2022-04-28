def initialize_board(board_width: 7, board_height: 6) -> list:
    """ Initialize the board with all '0' """
    # board = [["0"] * board_width] * board_height
    board = []
    for rows in range(board_height):
        board.append(["0" for _ in range(board_width)])
    return board


def print_board(board: list, human_friendly=False) -> None:
    """ Print the board in a human friendly way or in a compact way. """

    if human_friendly:
        print_board_human_friendly(board)
    else:
        for row in board:
            for col in row:
                print(col, end="")
            print()


def print_board_human_friendly(board: list) -> None:
    """ Prints the board in a human friendly way. """

    # Print column numbers
    column_numbers = "    1   2   3   4   5   6   7  "
    divider = "  +---------------------------+"
    print(column_numbers)

    for row_idx, row in enumerate(board):

        current_row_number = abs(row_idx - 6)
        coloumn_as_str = str(current_row_number) + " |"

        for col_idx, col in enumerate(row):
            coloumn_as_str += " " + str(col) + " |"

        print(divider)
        print(coloumn_as_str)

    # Print row divider
    print(divider)


def print_game_over(is_player_1_turn: bool) -> None:
    print()
    print("#######################################")
    print("            Player " + str(1 if is_player_1_turn else 2) + " has won!")
    print("#######################################")
    print()

def is_board_full(board: list) -> bool:
    """
    Returns True if the board is full, meaning it contains a single '0' and False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == "0":
                return False
    return True


def horizontal_win(board: list, player_symbol: str, required_in_a_row=4) -> bool:
    """
    Returns True if the player has won horizontally, False otherwise.
    """
    # Check for horizontal win
    for row in board:
        in_a_row = 0

        # Check how many cells are in a row with the current player's symbol
        for cell in row:
            if cell == player_symbol:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == required_in_a_row:
                return True


def vertical_win(board: list, player_symbol: str, required_in_a_row=4) -> bool:
    # Check for vertical win
    for col_idx in range(BOARD_WIDTH):

        # Get all the cells in the current column
        col = [row[col_idx] for row in board]
        in_a_row = 0

        # Check how many cells are in a row with the current player's symbol
        for cell in col:
            if cell == player_symbol:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == required_in_a_row:
                return True


def diagonal_win(board: list, player_symbol: str, required_in_a_row=4, top_left_to_bottom_right=True) -> bool:
    """
    Returns True if the player has won diagonally, False otherwise.
    """
    # Check for diagonal win (top left to bottom right)
    reversed_board = list(reversed(board))

    if top_left_to_bottom_right:
        for row_idx in range(BOARD_HEIGHT):
            in_a_row = 0
            for col_idx in range(BOARD_WIDTH):

                if reversed_board[row_idx][col_idx] == player_symbol:
                    in_a_row += 1
                else:
                    in_a_row = 0
                if in_a_row == required_in_a_row:
                    return True

    # Check for diagonal win (bottom left to top right)
    else:
        for row_idx in range(BOARD_HEIGHT):
            in_a_row = 0
            for col_idx in range(BOARD_WIDTH):
                if row_idx + col_idx == 0:
                    if reversed_board[row_idx][col_idx] == player_symbol:
                        in_a_row += 1
                    else:
                        in_a_row = 0
                    if in_a_row == required_in_a_row:
                        return True


def has_won_check(board: list, player_symbol: str, required_in_a_row=4) -> bool:
    # Check for horizontal win
    if horizontal_win(board, player_symbol, required_in_a_row):
        return True

    # Check for vertical win
    if vertical_win(board, player_symbol, required_in_a_row):
        return True

    # Check for diagonal win (top left to bottom right)
    if diagonal_win(board, player_symbol, required_in_a_row, top_left_to_bottom_right=True):
        return True

    # Check for diagonal win (top right to bottom left)
    if diagonal_win(board, player_symbol, required_in_a_row, top_left_to_bottom_right=False):
        return True


if __name__ == '__main__':

    # Define player symbols
    player_1_symbol = "*"
    player_2_symbol = "%"

    # initialize the board
    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6
    board = initialize_board(BOARD_WIDTH, BOARD_HEIGHT)

    # Print the initial board
    print_human_friendly = True
    print_board(board, print_human_friendly)

    is_player_1_turn = True
    a_player_has_won = False

    # Main game loop. Continue until a player has won or the board is full
    while not a_player_has_won and not is_board_full(board):

        # Determine which player's turn it is and get their symbol
        if is_player_1_turn:
            print("Player 1's turn")
            concurrent_player_symbol = player_1_symbol
        else:
            print("Player 2's turn")
            concurrent_player_symbol = player_2_symbol

        try:
            # Prompt the user for their move 1 - 7
            column_number = int(input("Enter a column number: "))
            print()
            assert 1 <= column_number <= 7

            # Check if column is full
            assert board[0][column_number - 1] == "0"

            # Reverse the board so that the bottom row is the first row. This makes life easier for inserting the symbol
            reversed_board = list(reversed(board))

            # Insert the symbol into the board
            for row in reversed_board:
                if row[column_number - 1] == "0":
                    row[column_number - 1] = concurrent_player_symbol
                    break

            # Print the board
            print_board(board, print_human_friendly)

            # Check if the player has won
            if has_won_check(board, concurrent_player_symbol):
                a_player_has_won = True
                print_game_over(is_player_1_turn)
                break

            # Switch turns
            is_player_1_turn = not is_player_1_turn
            print()

        except Exception:
            print("Invalid input. Should be an integer value from 1 to 7")
            continue
