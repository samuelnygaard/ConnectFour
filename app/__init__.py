from flask import Flask, render_template, request
from ConnectFourGame import ConnectFourGame, Player
import requests

server_ip = '20.223.236.119'
# server_ip = '127.0.0.1'


def connect_player(player: Player, port, game: ConnectFourGame):
    port = int(port)
    assert 1 < port < 65535, "Port must be between 1 and 65535"

    # Send a get request to the api to check if a name is send
    name = requests.get(f'http://{server_ip}:' + str(port) + '/api/getAgentName')
    name = name.json()['response']
    assert name != "", "Name must not be empty"

    # Set player properties
    player.name = name
    player.port = port
    player.is_human = False

    # Send a post requst with a board to check if a valid move is made
    move = requests.post(f'http://{server_ip}:' + str(port) + '/api/nextMove',
                         json={'board': [["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"]],
                               'player_symbol': player.symbol
                               })
    move = int(move.json()['response'])
    assert 0 <= move <= game.board_width - 1, "Move must be between 0 and {}".format(game.board_width - 1)

    return True


def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)
    game = ConnectFourGame()
    validated_ports = {
        'port1': False,
        'port2': False,
    }

    @app.route('/check', methods=['GET', 'POST'])
    def check():
        game_message = ""
        if request.method == 'POST':

            if 'portnumber1' in request.form:
                portnumber1 = request.form['portnumber1']
                try:
                    connect_player(game.player_1, portnumber1, game)
                    validated_ports['port1'] = True

                except Exception as err:
                    game_message = f"Couldn't connect player 1\n{err}"

            if 'portnumber2' in request.form:
                portnumber2 = request.form['portnumber2']
                try:
                    connect_player(game.player_2, portnumber2, game)
                    validated_ports['port2'] = True
                except Exception as err:
                    game_message = f"Couldn't connect player 2\n{err}"

        return render_template("game/lobby.html",
                               game=game,
                               port1_valid=validated_ports['port1'],
                               port2_valid=validated_ports['port2'],
                               message=game_message)

    @app.route('/')
    def lobby():

        # Set validated ports to False
        validated_ports['port1'] = False
        validated_ports['port2'] = False

        game.reset()

        return render_template("game/lobby.html", game=game, port1_valid=validated_ports['port1'], port2_valid=validated_ports['port2'])

    # route to reset the board and start a new game
    @app.route('/start', methods=['GET', 'POST'])
    def start():
        game.board = game.initialize_board()

        game_message = "Player 1's turn" if game.current_player == game.player_1 else "Player 2's turn"

        return render_template("game/game.html", game=game, message=game_message)

    # route to move the piece for the player one to the desired column number,
    # if the column is invalid return invalid else the move is valid,
    # if there are four connecting pieces return Winner
    @app.route('/move/<col>', methods=['GET', 'POST'])
    def move(col):
        if game.current_player.is_human:
            game.current_player.end_turn()
            col = int(col)
        else:
            game.current_player.start_turn()
            col = game.current_player.request_move(server_ip, game.board, game.board_width)
            game.current_player.end_turn()

        if (col < 0 or col > game.board_width):
            return render_template("game/game.html", game=game, message="Invalid Column!")
        else:
            game.drop_piece(col)

            if game.current_player.is_human:
                game.current_player.start_turn()

            # Check if winner is found
            if game.is_game_over:
                return render_template("game/game_over.html", game=game, message=game.game_message)
            else:
                game_message = "Player 1's turn" if game.current_player == game.player_1 else "Player 2's turn"
                return render_template("game/game.html", game=game, message=game_message)

    return app
