
# The four directions we can ask to move
BATTLE_SNAKE_RESPONSE_MOVE_RIGHT = "right"
BATTLE_SNAKE_RESPONSE_MOVE_LEFT = "left"
BATTLE_SNAKE_RESPONSE_MOVE_UP = "up"
BATTLE_SNAKE_RESPONSE_MOVE_DOWN = "down"


def point_to_tuple(point):
    return int(point["x"]), int(point["y"])


class BattleSnake(object):
    """
    Represents a single snake in the game of Battle Snake
    """
    def __init__(self, snake_state):
        self.id = snake_state["id"]
        self.health = snake_state["health"]
        self.length = snake_state["length"]
        self.taunt = snake_state["taunt"]
        self.name = snake_state["name"]
        self.body = map(point_to_tuple, snake_state["body"]["data"])


class SnakeWorld(object):
    """
    Represents the state of the world as is passed to the move endpoint
    """

    def __init__(self, world_state):
        self.map_height = world_state["height"]
        self.map_width = world_state["width"]
        self.world_id = world_state["id"]
        self.turn = world_state["turn"]
        self.snakes = map(BattleSnake, world_state["snakes"]["data"])
        self.food = map(point_to_tuple, world_state["food"]["data"])
        if "dead_snakes" in world_state:
            self.dead_snakes = map(BattleSnake, world_state["dead_snakes"]["data"])
        self.me = BattleSnake(world_state["you"])
