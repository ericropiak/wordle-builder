from functools import wraps

from app.web_sockets import forceRefresh

def game_action(action_func):

    @wraps(action_func)
    def inner(*action_args, **action_kwargs):
        game_id = action_kwargs['game_id']
        trigger_fresh, action_response = action_func(*action_args, **action_kwargs)
        if trigger_fresh:
            forceRefresh(game_id)
        return action_response
        # return action_func(*action_args, **action_kwargs)

    return inner

