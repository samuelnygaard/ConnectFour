from flask import Flask, render_template, request
from ConnectFourGame import ConnectFourGame
import requests

server_ip = '127.0.0.1'


def check_port(port, game: ConnectFourGame):

    port = int(port)
    assert 1 < port < 65535, "Port must be between 1 and 65535"

    # Send a get request to the api to check if a name is send
    name = requests.get(f'http://{server_ip}:' + str(port) + '/api/getname')
    name = name.json()['response']
    print("Name: " + name)
    assert name != "", "Name must not be empty"

    # Send a post requst with a board to check if a valid move is made
    move = requests.post(f'http://{server_ip}:' + str(port) + '/api/nextmove',
                         json={'board': [["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"],
                                         ["-", "-", "-", "-", "-", "-", "-"]],
                               'board_width': game.board_width,
                               })
    move = int(move.json()['response'])
    print("Move: " + str(move))
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

        if request.method == 'POST':

            if 'portnumber1' or 'portnumber2' in request.form:
                if 'portnumber1' in request.form:
                    portnumber = request.form['portnumber1']
                else:
                    portnumber = request.form['portnumber2']

                try:
                    if check_port(portnumber, game):
                        if 'portnumber1' in request.form:
                            validated_ports['port1'] = True
                            game.player_1.is_human = False
                            game.player_1.port = int(portnumber)
                        else:
                            validated_ports['port2'] = True
                            game.player_2.is_human = False
                            game.player_2.port = int(portnumber)
                except Exception as e:
                    print(e)

        return render_template("game/lobby.html", port1_valid=validated_ports['port1'],
                               port2_valid=validated_ports['port2'])

    @app.route('/')
    def lobby():

        # Set validated ports to False
        validated_ports['port1'] = False
        validated_ports['port2'] = False

        return render_template("game/lobby.html", port1_valid=validated_ports['port1'],
                               port2_valid=validated_ports['port2'])

    # route to reset the board and start a new game
    @app.route('/start', methods=['GET', 'POST'])
    def start():
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
        else:
            col = game.current_player.request_move(server_ip, game.board, game.board_width)

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
