from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from ConnectFourGame import ConnectFourGame


def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)

    game = ConnectFourGame()

    @app.route('/')
    def index():
        return render_template("game/lobby.html")

    # route to reset the board and start a new game
    @app.route('/start', methods=['GET'])
    def start():
        game = ConnectFourGame()
        game.initialize_board()
        game_message = "New Game! - Player 1's turn" if game.current_player == game.player_1 else "New Game! - Player 2's turn"
        return render_template("game/game.html", board=game.board, message=game_message)

    # route to move the piece for the player one to the desired column number,
    # if the column is invalid return invalid else the move is valid,
    # if there are four connecting pieces return Winner
    @app.route('/move/<col>', methods=['GET', 'POST'])
    def move(col):
        col = int(col)
        if (col < 0 or col > game.board_width):
            return render_template("game/game.html", board=game.board, message="Invalid Column!")
        else:
            game.drop_piece(col)

            # Check if winner is found
            if game.is_game_over:
                return render_template("game/game_over.html", board=game.board, message=game.game_message)
            else:
                game_message = "Player 1's turn" if game.current_player == game.player_1 else "Player 2's turn"
                return render_template("game/game.html", board=game.board, message=game_message)

    return app
