from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from ConnectFourGame import ConnectFourGame
import requests


def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)

    game = ConnectFourGame()
    server_ip = '0.0.0.0'
    port1_valid = False
    port2_valid = True

    # @app.route('/check', methods=['GET', 'POST'])
    # def check():
    #     if request.method == 'POST':
    #         if 'portnumber1' in request.form:
    #             portnumber = request.form['portnumber1']
    #             port1_valid = True
    #             return render_template("game/lobby.html", port1_valid=port1_valid, port2_valid=port2_valid)
    #         elif 'portnumber2' in request.form:
    #             portnumber = request.form['portnumber2']
    #             port2_valid = True
    #             return render_template("game/lobby.html", port1_valid=port1_valid, port2_valid=port2_valid)
    #         else:
    #
    #         # send request to server ip and portnumber
    #
    #         # get response from server
    #         # get_name = server_ip + ':' + portnumber + '/api/get_name'
    #         # name = requests.get(get_name)
    #
    #     return render_template("game/lobby.html", port1_valid=port1_valid, port2_valid=port2_valid)

    @app.route('/')
    def lobby():
        return render_template("game/lobby.html", port1_valid=port1_valid, port2_valid=port2_valid)

    # route to reset the board and start a new game
    @app.route('/start', methods=['GET', 'POST'])
    def start():
        if request.method == 'POST':
            portnumber1 = request.form['portnumber1']
            portnumber2 = request.form['portnumber2']
            print(portnumber1, portnumber2)

        game.board = game.initialize_board()
        game_message = "New Game! - Player 1's turn" if game.current_player == game.player_1 else "New Game! - Player 2's turn"
        return render_template("game/game.html", board=game.board, message=game_message)

    # route to move the piece for the player one to the desired column number,
    # if the column is invalid return invalid else the move is valid,
    # if there are four connecting pieces return Winner
    @app.route('/move/<col>', methods=['GET', 'POST'])
    def move(col):

        if game.current_player.is_human:
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
