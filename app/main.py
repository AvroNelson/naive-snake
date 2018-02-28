import bottle
import os
from pypaths import astar

RIGHT_MOVE = "right"
LEFT_MOVE = "left"
UP_MOVE = "up"
DOWN_MOVE = "down"


def get_distance(point_a, point_b):
    distance_x = int(point_a["x"]) - int(point_b["x"])
    distance_y = int(point_a["y"]) - int(point_b["y"])
    return distance_x, distance_y


def point_to_tuple(point):
    return int(point["x"]), int(point["y"])


class MoveCalculator(object):

    def __init__(self, data):
        self.game_state = data
        self.snake_head = point_to_tuple(self.game_state["you"]["body"]["data"][0])
        self.map_height = self.game_state["height"]
        self.map_width = self.game_state["width"]
        self.all_snake_points = map(lambda s: point_to_tuple(s["body"]["data"]), self.game_state["snakes"]["data"])

    def get_distance_to_location(self, location):
        distance_x, distance_y = get_distance(self.snake_head, location)
        total = abs(distance_x) + abs(distance_y)
        return total

    def get_nearest_food(self):
        all_food = map(self.get_distance_to_location, self.game_state["food"]["data"])
        smallest = min(all_food)
        food_index = all_food.index(smallest)
        return point_to_tuple(self.game_state["food"]["data"][food_index])

    def get_neighbors(self, coord):
        neighbor_list = [(coord[0], coord[1] + 1),
                         (coord[0], coord[1] - 1),
                         (coord[0] + 1, coord[1]),
                         (coord[0] - 1, coord[1])]

        values = [c for c in neighbor_list
                  if c != coord
                  and c not in self.all_snake_points
                  and 0 <= c[0] < self.map_width
                  and 0 <= c[1] < self.map_height]
        return values

    def get_next_move(self):

        finder = astar.pathfinder(neighbors=self.get_neighbors)

        # ToDo: Cycle through foods until we find the nearest one we can reach.
        search_start = self.snake_head
        search_end = self.get_nearest_food()

        total_moves, path = finder(search_start, search_end)

        next_x, next_y = path[1]
        head_x, head_y = search_start

        if head_x < next_x:
            return RIGHT_MOVE

        if head_x > next_x:
            return LEFT_MOVE

        if head_y < next_y:
            return DOWN_MOVE

        if head_y > next_y:
            return UP_MOVE

        # Don't know where we are going, choose a direction
        return UP_MOVE

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
        'taunt': "Nom Nom Nom",
        'head_url': head_url,
        'name': 'Naive Snake'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    calc = MoveCalculator(data)
    next_move = calc.get_next_move()
    return {
        'move': next_move,
        'taunt': 'I Sure Hope This Works Out!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application,
               host=os.getenv('IP', '10.4.19.129'),
               port=os.getenv('PORT', '8082'))
