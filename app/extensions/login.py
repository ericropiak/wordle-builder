from flask import g


def login_user(player):

    g.current_user = player
