from AIGame import SnakeAIVisual
import torch
import random
import numpy as np
from collections import deque
from AIGame.model import Linear_QNet, QTrainer
from AIGame.AgentHelper import plot, get_danger
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self) -> None:
        '''Constructor for Agent objects which essentially store a model, games played, and a trainer to train said model'''

        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: SnakeAIVisual.SnakeAIVisual().state) -> None:
        '''
        gets state in form of
        [
        Danger-Straight, Danger-Right, Danger-Left,     0 or 1 for each
        Moving-Left, Moving-Right, Moving-Up, Moving-Down   0 or 1 for each
        Food-Left, Food-Right, Food-Up, Food-Down    0 or 1 for each
        ]
        and returns this state
        '''
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

    def remember(self, state: list[int], action: list[int], reward: int, next_state: list[int], done: bool) -> None:
        '''
        Adds the states,actions,rewards and if the game is over to memory
        self.memory is a deque so if maximum memory exceeded, the left-most index gets removed to allow for new data
        '''
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self) -> None:
        '''
        Gets a batch of memory to train longer term memory (A.K.A the model being fit to an entire game rather than individual actions)
        '''
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state: list[int], action: list[int], reward: int, next_state: list[int], done: bool) -> None:
        '''
        Gets a single moves before-state,after-state,reward,and if the game is over values and trains the model on it
        '''
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state: list[int]) -> list[int]:
        '''Randomly creates an action if randomness permits, otherwise uses the model to predict the action (also random depending on how trained the model)'''
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def convert_to_string(action: list[int], direction: str) -> str:
    '''

    :param action: a list of integers representing direction of which to turn
    :param direction: the current direction of the snake
    :return: string representing the new direction of the snake
    '''

    if action == [0,1,0]:
        if direction == 'R':
            return 'R'
        elif direction == 'U':
            return 'U'
        elif direction == 'D':
            return 'D'
        else:
            return 'L'
    elif action == [1,0,0]:
        if direction == 'R':
            return 'U'
        elif direction == 'U':
            return 'L'
        elif direction == 'D':
            return 'R'
        else:
            return 'D'
    else:
        if direction == 'R':
            return 'D'
        elif direction == 'U':
            return 'R'
        elif direction == 'D':
            return 'L'
        else:
            return 'U'

def train() -> None:
    '''Trains the model'''

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeAIVisual.SnakeAIVisual()
    epochs = 100
    while agent.n_games < epochs:


        state_old = agent.get_state(game.state)

        final_move = agent.get_action(state_old)
        final_move_string = convert_to_string(final_move,game.state.snake[-1][1])

        reward, done, score = game.play_step(final_move_string)

        state_new = agent.get_state(game.state)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:

            game.state.reset()
            agent.n_games += 1
            agent.train_long_memory()


            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)



if __name__ == '__main__':
    train()
