from flask import Blueprint, render_template

mod = Blueprint('game', __name__, url_prefix='/')


@mod.route('/', methods=['GET'])
def index():
    board = [['-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', 'O', '-'],
             ['-', 'X', '-', '-', '-', 'O', '-'],
             ['O', 'X', '-', 'O', '-', 'X', '-'],
             ['X', 'O', '-', 'X', 'X', 'O', 'X']]

    return render_template('game/index.html', board=board)


@mod.route('/play', methods=['GET'])
def play():
    example_board_1 = [['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', 'O', '-'],
                       ['-', 'X', '-', '-', '-', 'O', '-'],
                       ['O', 'X', '-', 'O', '-', 'X', '-'],
                       ['X', 'O', '-', 'X', 'X', 'O', 'X']]

    example_board_2 = [['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-']]

    return render_template('game/play.html', board=example_board_2)
