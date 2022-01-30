import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch import save, tensor, float, unsqueeze, argmax
from os import path, makedirs

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not path.exists(model_folder_path):
            makedirs(model_folder_path)
        
        file_name = path.join(model_folder_path, file_name)
        save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr =lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = tensor(state, dtype=float)
        next_state = tensor(next_state, dtype=float)
        action = tensor(action, dtype=float)
        reward = tensor(reward, dtype=float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = unsqueeze(state, 0)
            next_state = unsqueeze(next_state, 0)
            action = unsqueeze(action, 0)
            reward = unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * max(self.model(next_state[idx]))
            
            target[idx][argmax(action).item()] = Q_new


        # 2: Q_new = r + y * max(next_predicted Q value) --> ionly if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()