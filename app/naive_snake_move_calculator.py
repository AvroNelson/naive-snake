from collections import namedtuple

from app.battle_snake_world_state import BATTLE_SNAKE_RESPONSE_MOVE_RIGHT, BATTLE_SNAKE_RESPONSE_MOVE_LEFT, \
    BATTLE_SNAKE_RESPONSE_MOVE_DOWN, BATTLE_SNAKE_RESPONSE_MOVE_UP
from pypaths import astar

FoodOption = namedtuple("FoodOption", "distance first_step")


class NaiveSnakeMoveCalculator(object):

    def __init__(self, world_state):
        self.world_state = world_state
        self.all_snake_points = self.get_all_snake_points()
        self.food_options = self.get_food_options()

    def get_all_snake_points(self):
        all_snake_bodies = map(lambda snake: snake.body, self.world_state.snakes)
        return reduce(lambda a, b: a + b, all_snake_bodies)

    def get_food_options(self):
        path_finder = astar.pathfinder(neighbors=self.get_neighbors)
        my_head = self.world_state.me.body[0]

        # Calculate the path to each piece of food on the map
        food_paths = map(lambda food: path_finder(my_head, food), self.world_state.food)

        # All we care about is how long is this path and
        # what is my first step on it
        # Notice we are not passing the first point returned, that is the head of our snake
        return map(lambda path: FoodOption(distance=path[0], first_step=path[1][1]), food_paths)

    def get_neighbors(self, point):

        # Create a list of all four points directly beside us
        neighbor_list = [(point[0], point[1] + 1),
                         (point[0], point[1] - 1),
                         (point[0] + 1, point[1]),
                         (point[0] - 1, point[1])]

        # Remove invalid locations
        return filter(self.is_valid_neighbor, neighbor_list)

    def is_valid_neighbor(self, point):

        # We will never path into another snake or ourself
        if point in self.all_snake_points:
            return False

        # Note: does teh grid start at 0?

        if 0 > point[0] >= self.world_state.map_width:
            return False

        if 0 > point[1] >= self.world_state.map_height:
            return False

        # Point looks good to me
        return True

    def get_nearest_food(self):
        # Sort our food by distance
        self.food_options.sort(key=lambda option: option.distance)
        return self.food_options[0]

    def get_direction_to_point(self, destination):
        """
        If you were to travel to this point, what direction would you go?
        This code assumes that we are looking at a point directly beside us
        """

        # Split our tuples into x/y coordinates
        next_x, next_y = destination
        head_x, head_y = self.world_state.me.body[0]

        if head_x < next_x:
            return BATTLE_SNAKE_RESPONSE_MOVE_RIGHT

        if head_x > next_x:
            return BATTLE_SNAKE_RESPONSE_MOVE_LEFT

        if head_y < next_y:
            return BATTLE_SNAKE_RESPONSE_MOVE_DOWN

        return BATTLE_SNAKE_RESPONSE_MOVE_UP

    def get_next_move(self):
        nearest_food_option = self.get_nearest_food()
        print nearest_food_option

        return self.get_direction_to_point(nearest_food_option.first_step)
