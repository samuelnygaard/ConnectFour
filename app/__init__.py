from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


def create_app():
    """For to use dynamic environment"""
    app = Flask(__name__)

    # Import a module / component using its blueprint handler variable
    from app.modules.game.controllers import mod as game_module

    # Register blueprint(s)
    app.register_blueprint(game_module)

    return app
