import requests

class Player:

    def __init__(self, name, symbol, is_human=True):
        self.name = name
        self.symbol = symbol
        self.is_human = is_human
        self.port = None
        self.time_per_move = []

    def request_move(self, server_ip, board, board_width):
        # Send a post requst with a board to check if a valid move is made
        move = requests.post(f'http://{server_ip}:' + str(self.port) + '/api/nextmove',
                             json={
                                 'board': board,
                                 'board_width': board_width
                             })
        move = int(move.json()['response'])

        return move


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
        self.game_message = ""
        self.human_friendly_board = human_friendly_board

        # Setup players
        self.player_1 = player_1
        self.player_2 = player_2
        self.current_player = self.player_1 if self.is_player_1_turn else self.player_2

    def drop_piece(self, column):
        """
        Drop a piece on the board.
        """
        assert self.board[0][column - 1] == self.empty_cell_symbol

        # Reverse the board so that the bottom row is the first row.
        # This makes life easier for inserting the current player's symbol
        reversed_board = list(reversed(self.board))

        # Insert the symbol into the board
        for row in reversed_board:
            if row[column - 1] == self.empty_cell_symbol:
                row[column - 1] = self.current_player.symbol
                break

        # Check if the player has won
        if self.has_won_check(self.board, self.current_player.symbol, self.connections_to_win):
            self.is_game_over = True
            self.game_message = self.print_game_over_player_won()

        # Check if the board is full
        if self.is_board_full(self.board):
            self.is_game_over = True
            self.game_message = self.print_game_over_tie()

        # Switch turns
        self.current_player = self.player_2 if self.current_player == self.player_1 else self.player_1

    def initialize_board(self):
        """ Initialize the board with empty cells """
        board = []
        for rows in range(self.board_height):
            board.append([self.empty_cell_symbol for _ in range(self.board_width)])
        return board

    @staticmethod
    def print_game_over_tie(verbose=True) -> str:
        game_over_tie_message = "It's a tie!"
        if verbose:
            print(game_over_tie_message)
        return game_over_tie_message

    def print_game_over_player_won(self, verbose=True) -> str:
        game_over_player_won_message = "Player " + str(1 if self.is_player_1_turn else 2) + " has won!\n"
        if verbose:
            print(game_over_player_won_message)
        return game_over_player_won_message

    def print_game_over_time_up(self, verbose=True) -> str:
        game_over_time_up_message = "Player " + str(1 if self.is_player_1_turn else 2) + " lost due to time up!\n"
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
