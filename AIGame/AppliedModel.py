import torch
from AIGame import model
from AIGame import SnakeAIVisual
from AIGame.AgentHelper import get_danger
from AIGame.Agent import convert_to_string
import numpy as np
import pygame


class AppliedModel():
    def __init__(self, current_screen: list[str], current_screen_dimensions: tuple) -> None:
        '''Constructor for applying the model which loads the model, stores a visual AI snake game and logic, and stores the screen of entire application'''
        pygame.init()
        self.screen = current_screen
        self.screen_dimensions = current_screen_dimensions
        self.game = SnakeAIVisual.SnakeAIVisual()
        self.model = model.Linear_QNet(11, 256, 3)
        self.model.load_state_dict(torch.load('model/model.pth'))
        self.model.eval()


    def get_state(self, game: SnakeAIVisual.SnakeAIVisual().state) -> list[int]:
        '''Gets the State of the snake game being played'''
        head = game.snake[-1]
        head_position = head[0]
        head_direction = head[1]
        dangers = get_danger(game)

        state = [
            #Danger Straight, Right, Left
            dangers[0],
            dangers[1],
            dangers[2],


            # Move direction
            head_direction == 'L',
            head_direction == 'R',
            head_direction == 'U',
            head_direction == 'D',

            # Food location
            game.apple[0][0] < head_position[0],  # food left
            game.apple[0][0] > head_position[0],  # food right
            game.apple[0][1] < head_position[1],  # food up
            game.apple[0][1] > head_position[1]  # food down
        ]


        return np.array(state, dtype=int)

    def run(self) -> None:
        '''Runs Model and its visual'''
        done = False

        while not done:

            blank_action = [0,0,0]
            state = self.get_state(self.game.state)
            state = torch.tensor(state, dtype=torch.float)

            action = self.model(torch.unsqueeze(state, 0))
            move = torch.argmax(action).item()
            blank_action[move] = 1
            blank_action = convert_to_string(blank_action, self.game.state.snake[-1][1])

            self.screen[0], done = self.game.play_step_testing(blank_action, self.screen_dimensions)


