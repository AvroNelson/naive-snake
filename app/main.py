import random

import bottle
import os
from app.battle_snake_world_state import SnakeWorld
from app.naive_snake_move_calculator import NaiveSnakeMoveCalculator


HAPPY_SNAKE_TAUNTS = [
    "Today sure looks like a nice day!",
    "Stay positive and happy",
    "Keep your face in the sunshine",
    "I am a successful snake, and I can do it!",
    "Work hard and stay positive!",
    "I Sure Hope This Works Out!",
    "Hard work pays off!"
]


def get_next_taunt():
    taunt_index = random.randint(0, len(HAPPY_SNAKE_TAUNTS) - 1)
    return HAPPY_SNAKE_TAUNTS[taunt_index]


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
        'taunt': get_next_taunt(),
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
        'taunt': get_next_taunt()
    }


@bottle.get('/')
def index():
    return "Naive Snake - 1.2"

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application,
               host=os.getenv('IP', '0.0.0.0'),
               port=os.getenv('PORT', '8080'))
