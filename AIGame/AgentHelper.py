import matplotlib.pyplot as plt
from IPython import display
from AIGame import SnakeAI
from copy import deepcopy

plt.ion()

def plot(scores: int, mean_scores: float) -> None:
    '''plots the scores and mean scores by Number of Games'''
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


def _check_danger_wall(game: SnakeAI) -> list[int]:
    '''Checks the Danger Position of Snake and if it is near a wall in front, left, or to its right'''
    snake_head = game.snake[-1]
    head_position = snake_head[0]
    head_direction = snake_head[1]
    board_dimensions = (len(game.board),len(game.board[0]))

    # Danger straight
    wall_checks = [1 if head_direction == 'R' and head_position[1] == board_dimensions[1] - 1 or
    head_direction == 'U' and head_position[0] == 0 or
    head_direction == 'D' and head_position[0] == board_dimensions[0] - 1 or
    head_direction == 'L' and head_position[1] == 0 else 0,

    # Danger right
    1 if head_direction == 'R' and head_position[0] == board_dimensions[0] - 1 or
    head_direction == 'U' and head_position[1] == board_dimensions[1] - 1 or
    head_direction == 'D' and head_position[1] == 0 or
    head_direction == 'L' and head_position[0] == 0 else 0,

    # Danger left
    1 if head_direction == 'R' and head_position[0] == 0 or
    head_direction == 'U' and head_position[1] == 0 or
    head_direction == 'D' and head_position[1] == board_dimensions[1] - 1 or
    head_direction == 'L' and head_position[0] == board_dimensions[0] - 1 else 0,
]
    return wall_checks

def _check_danger_self(game: SnakeAI) -> list[int]:
    '''Checks the Danger Position of Snake and if it is near itself in front, left, or to its right'''
    new_game_straight = deepcopy(game)
    new_game_right = deepcopy(game)
    new_game_left = deepcopy(game)

    #Danger straight
    snake_head = new_game_straight.snake[-1]
    head_position = snake_head[0]
    head_direction = snake_head[1]
    new_game_straight.shift_snake_directions(head_direction)
    new_game_straight.shift_snake_positions()
    danger_straight = int(new_game_straight.check_snake_collision())

    #Danger right
    snake_head = new_game_right.snake[-1]
    head_position = snake_head[0]
    head_direction = snake_head[1]
    new_head_direction = 'R' if head_direction == 'U' else 'D' if head_direction == 'R' else 'L' if head_direction == 'D' else 'U'
    new_game_right.shift_snake_directions(new_head_direction)
    new_game_right.shift_snake_positions()
    danger_right = int(new_game_right.check_snake_collision())

    # Danger left
    snake_head = new_game_left.snake[-1]
    head_position = snake_head[0]
    head_direction = snake_head[1]
    new_head_direction = 'R' if head_direction == 'D' else 'D' if head_direction == 'L' else 'L' if head_direction == 'U' else 'U'
    new_game_left.shift_snake_directions(new_head_direction)
    new_game_left.shift_snake_positions()
    danger_left = int(new_game_left.check_snake_collision())

    return [danger_straight,danger_right,danger_left]


def get_danger(game: SnakeAI) -> list[int]:
    '''Checks the Danger Position of Snake and if it is near a wall or itself in front, left, or to its right'''

    collisions_wall = _check_danger_wall(game)
    collisions_self = _check_danger_self(game)
    overall_collisions = [0,0,0]

    for collision in range(len(collisions_wall)):
        if collisions_wall[collision] == 1 or collisions_self[collision] == 1:
            overall_collisions[collision] = 1

    return overall_collisions



