from flask import Blueprint, render_template
from ConnectFourGame import ConnectFourGame

mod = Blueprint('game', __name__, url_prefix='/')


@mod.route('/', methods=['GET'])
def lobby():
    return render_template('game/lobby.html')


@mod.route('/start', methods=['GET'])
def start():

    connectFourGame = ConnectFourGame()

    example_board_1 = [['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', 'O', '-'],
                       ['-', 'X', '-', '-', '-', 'O', '-'],
                       ['O', 'X', '-', 'O', '-', 'X', '-'],
                       ['X', 'O', '-', 'X', 'X', 'O', 'X']]


    return render_template('game/start.html', game=connectFourGame)
