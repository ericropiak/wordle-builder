from flask import g

def login_player(player):

	g.current_player = player