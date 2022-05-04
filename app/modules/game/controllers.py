from flask import Blueprint, render_template

mod = Blueprint('game', __name__, url_prefix='/')


@mod.route('/', methods=['GET'])
def play():
    board = [['-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', 'O', '-'],
             ['-', 'X', '-', '-', '-', 'O', '-'],
             ['O', 'X', '-', 'O', '-', 'X', '-'],
             ['X', 'O', '-', 'X', 'X', 'O', 'X']]

    return render_template('index.html', board=board)
