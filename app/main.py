import bottle
import os
from app.battle_snake_world_state import SnakeWorld
from app.naive_snake_move_calculator import NaiveSnakeMoveCalculator
from pypaths import astar



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00FF00',
        'taunt': "Gosh gee golly, I sure hope this all works out!",
        'head_url': head_url,
        'name': 'Naive Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    world_state = SnakeWorld(data)

    calc = NaiveSnakeMoveCalculator(world_state)
    next_move = calc.get_next_move()
    return {
        'move': next_move,
        'taunt': 'I Sure Hope This Works Out!'
    }


@bottle.get('/')
def index():
    return "Naive Snake - 1.0"

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application,
               host=os.getenv('IP', '0.0.0.0'),
               port=os.getenv('PORT', '8081'))
