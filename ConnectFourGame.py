import random
import time


class Player:

    def __init__(self, name, symbol, is_human=True):
        self.name = name
        self.symbol = symbol
        self.is_human = is_human
        self.time_per_move = []

    def next_move(self, board):
        if self.is_human:
            return int(input(f"{self.name}, enter your move: "))
        else:
            return random.randint(0, len(board[0]) - 1)


class ConnectFourGame:

    def __init__(self, board_size=(7, 6),
                 turn_time_sec=10,
                 connections_to_win=4,
                 player_1_starts=True,
                 human_friendly_board=True,
                 player_1=Player("Gary", "X", True),
                 player_2=Player("Magnus", "O", True)
                 ):

        # Board settings
        self.board_width = board_size[0]
        self.board_height = board_size[1]
        self.empty_cell_symbol = "-"
        self.board = self.initialize_board()

        # Game settings
        self.turn_time_sec = turn_time_sec  # Seconds
        self.connections_to_win = connections_to_win  # Number of connections to win
        self.is_player_1_turn = player_1_starts
        self.is_game_over = False
        self.human_friendly_board = human_friendly_board

        # Setup players
        self.player_1 = player_1
        self.player_2 = player_2

    def play(self):
        """ Start the game. """

        # Initialize the board
        self.board = self.initialize_board()
        self.print_start_game_message()

        input("Press Enter to start the game...")

        # Print the board
        self.print_board(self.board, self.human_friendly_board)

        # Play the game
        # Main game loop. Continue until a player has won or the board is full
        while not self.is_game_over:

            # Start this turn's time counter
            turn_start_time = time.time()

            # Determine which player's turn it is and get their symbol
            if self.is_player_1_turn:
                print("Player 1's turn")
                concurrent_player_symbol = self.player_1.symbol
            else:
                print("Player 2's turn")
                concurrent_player_symbol = self.player_2.symbol

            valid_move = False
            while not valid_move:

                try:
                    # Prompt the user for their move
                    column_number = int(input("Enter a column number: "))
                    print()
                    assert 1 <= column_number <= self.board_width

                    # Check if column is full
                    assert self.board[0][column_number - 1] == self.empty_cell_symbol

                    # Check if the move was made in time
                    move_time_sec = round(time.time() - turn_start_time, 2)
                    if move_time_sec > self.turn_time_sec:
                        self.print_game_over_time_up()
                        self.is_game_over = True
                        break

                    # Add move time to player's time list
                    if self.is_player_1_turn:
                        self.player_1.time_per_move.append(move_time_sec)
                    else:
                        self.player_2.time_per_move.append(move_time_sec)

                    # If move was made in time and passed the asserts, then the move is valid
                    valid_move = True

                    # Reverse the board so that the bottom row is the first row.
                    # This makes life easier for inserting the current player's symbol
                    reversed_board = list(reversed(self.board))

                    # Insert the symbol into the board
                    for row in reversed_board:
                        if row[column_number - 1] == self.empty_cell_symbol:
                            row[column_number - 1] = concurrent_player_symbol
                            break

                    # Print the board and the player's used time
                    self.print_board(self.board, self.human_friendly_board)
                    self.print_players_total_turn_time()

                    # Check if the player has won
                    if self.has_won_check(self.board, concurrent_player_symbol, self.connections_to_win):
                        self.print_game_over_player_won()
                        self.is_game_over = True
                        break

                    # Switch turns
                    self.is_player_1_turn = not self.is_player_1_turn
                    print()

                    # Check if the board is full
                    if self.is_board_full(self.board):
                        self.print_game_over_tie()
                        self.is_game_over = True
                        break

                except Exception:

                    seconds_elapsed = time.time() - turn_start_time
                    seconds_remaining = round(self.turn_time_sec - seconds_elapsed, 2)

                    if seconds_remaining < 0:
                        self.print_game_over_time_up()
                        break
                    else:
                        print(f"Invalid input. Should be an integer value from 1 to 7. "
                              f"You have {seconds_remaining} seconds left to make a move.")
                        continue

    def initialize_board(self) -> list:
        """ Initialize the board with empty cells """
        board = []
        for rows in range(self.board_height):
            board.append([self.empty_cell_symbol for _ in range(self.board_width)])
        return board

    def print_board(self, board, human_friendly=False) -> None:
        """ Print the board in a human friendly way or in a compact way. """

        if human_friendly:
            self.print_board_human_friendly(board)
        else:
            for row in board:
                for col in row:
                    print(col, end="")
                print()

    def print_board_human_friendly(self, board) -> None:
        """ Prints the board in a human friendly way. """

        # Print column numbers
        column_numbers = "    1   2   3   4   5   6   7  "
        divider = "  +---------------------------+"
        print(column_numbers)

        for row_idx, row in enumerate(board):

            current_row_number = abs(row_idx - (self.board_width - 1))
            coloumn_as_str = str(current_row_number) + " |"

            for col_idx, col in enumerate(row):
                coloumn_as_str += " " + str(col) + " |"

            print(divider)
            print(coloumn_as_str)

        # Print row divider
        print(divider)

    def print_players_total_turn_time(self, verbose=True) -> str:
        """ Prints the total time of the players """

        player_total_turn_time_msg = f"{self.player_1.name} has used {round(sum(self.player_1.time_per_move), 2)} seconds in total" + "\n"
        player_total_turn_time_msg += f"{self.player_2.name} has used {round(sum(self.player_2.time_per_move), 2)} minutes in total" + "\n"

        if verbose:
            print(player_total_turn_time_msg)

        return player_total_turn_time_msg

    def print_start_game_message(self, verbose=True) -> str:
        start_games_message = "Welcome to Connect Four!\n"
        start_games_message += "Board size: " + str(self.board_width) + " X " + str(self.board_height) + "\n"
        start_games_message += "Time per turn: " + str(self.turn_time_sec) + " seconds" + "\n\n"
        start_games_message += "Player 1: " + self.player_1.name + " (" + self.player_1.symbol + f") is a {'human' if self.player_1.is_human else 'computer'} player" + "\n"
        start_games_message += "Player 2: " + self.player_2.name + " (" + self.player_2.symbol + f") is a {'human' if self.player_2.is_human else 'computer'} player" + "\n\n"
        start_games_message += f"{self.player_1.name if self.is_player_1_turn else self.player_2.name} starts the game!" + "\n"
        if verbose:
            print(start_games_message)
        return start_games_message

    @staticmethod
    def print_game_over_tie(verbose=True) -> str:
        game_over_tie_message = "#########################################\n"
        game_over_tie_message += "        It's a tie!\n"
        game_over_tie_message += "#########################################\n"
        if verbose:
            print(game_over_tie_message)
        return game_over_tie_message

    def print_game_over_player_won(self, verbose=True) -> str:
        game_over_player_won_message = "#########################################\n"
        game_over_player_won_message += "         Player " + str(1 if self.is_player_1_turn else 2) + " has won!\n"
        game_over_player_won_message += "#########################################\n"
        if verbose:
            print(game_over_player_won_message)
        return game_over_player_won_message

    def print_game_over_time_up(self, verbose=True) -> str:
        game_over_time_up_message = "#########################################\n"
        game_over_time_up_message += "    Player " + str(1 if self.is_player_1_turn else 2) + " lost due to time up!\n"
        game_over_time_up_message += "#########################################\n"
        if verbose:
            print(game_over_time_up_message)
        return game_over_time_up_message

    def is_board_full(self, board: list) -> bool:
        """
        Returns True if the board is full, meaning it contains a single '0' and False otherwise.
        """
        for row in board:
            for cell in row:
                if cell == self.empty_cell_symbol:
                    return False
        return True

    def horizontal_win(self, board: list, player_symbol: str, required_in_a_row=4) -> bool:
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

    def vertical_win(self, board: list, player_symbol: str, required_in_a_row=4) -> bool:
        # Check for vertical win
        for col_idx in range(self.board_width):

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

    def diagonal_win(self, board: list, player_symbol: str, required_in_a_row=4, top_left_to_bottom_right=True) -> bool:
        """
        Returns True if the player has won diagonally, False otherwise.
        """
        # Check for diagonal win (top left to bottom right)
        if top_left_to_bottom_right:
            for row_idx in range(self.board_height):
                in_a_row = 0
                for col_idx in range(self.board_width):

                    while row_idx < self.board_height and col_idx < self.board_width:
                        if board[row_idx][col_idx] == player_symbol:
                            in_a_row += 1
                        else:
                            in_a_row = 0

                        if in_a_row == required_in_a_row:
                            return True

                        row_idx += 1
                        col_idx += 1

        # Check for diagonal win (bottom left to top right)
        else:
            for row_idx in range(self.board_height):
                in_a_row = 0
                for col_idx in range(self.board_width):

                    while row_idx >= 0 and col_idx < self.board_width:
                        if board[row_idx][col_idx] == player_symbol:
                            in_a_row += 1
                        else:
                            in_a_row = 0

                        if in_a_row == required_in_a_row:
                            return True

                        row_idx -= 1
                        col_idx += 1

    def has_won_check(self, board: list, player_symbol: str, required_in_a_row=4) -> bool:
        # Check for horizontal win
        if self.horizontal_win(board, player_symbol, required_in_a_row):
            return True

        # Check for vertical win
        if self.vertical_win(board, player_symbol, required_in_a_row):
            return True

        # Check for diagonal win (top left to bottom right)
        if self.diagonal_win(board, player_symbol, required_in_a_row, top_left_to_bottom_right=True):
            return True

        # Check for diagonal win (top right to bottom left)
        if self.diagonal_win(board, player_symbol, required_in_a_row, top_left_to_bottom_right=False):
            return True


if __name__ == '__main__':
    # Initialize the game
    game = ConnectFourGame(human_friendly_board=False)

    game.play()
