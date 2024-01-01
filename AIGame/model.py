import numpy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):

    def __init__(self, input_size: int, hidden_size: int, output_size: int) -> None:
        '''Constructor for Neural Network Architecture Object'''
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x: float) -> float:
        '''Function performs activation function'''
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth') -> None:
        '''Saves Model'''
        model_folder_path = '../model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model: Linear_QNet(), lr: float, gamma: float) -> None:
        '''Constructor for Trainer Objects where the model, loss, and optimizers are defined'''
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state: list or tuple[list], action: list or tuple[list], reward: int or tuple[int], next_state: list or tuple[list], done: bool or tuple[bool]) -> None:
        '''Trains model for a step by running data through the model to enhance performance. State Data can be of dimensions (1,11) or (n,11) '''

        if type(state) is tuple:
            state = numpy.array(torch.tensor(state))
            state = torch.tensor(state, dtype=torch.float)

        else:
            state = torch.tensor(state, dtype=torch.float)

        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)


        pred = self.model(state)


        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()