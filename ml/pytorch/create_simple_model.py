# -*- coding: utf-8 -*-
# A simple pytorch model to train a neuronal network
# with arbitrary data

import numpy
import pandas
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
import torchvision
from pprint import pprint
import os


class SimpleNetwork(nn.Module):

    def __init__(self):
        super(SimpleNetwork, self).__init__()
        # Put 10 features in and expect 10 features out
        self.lin1 = nn.Linear(10, 10)
        # Put the output of lin1 in the input of lin2, be aware that the
        # number of lin1 output features is equal to the numner of lin2 input features
        self.lin2 = nn.Linear(10, 10)

    def forward(self, x):
        # Simple activation function, rectified linear unit
        x = F.relu(self.lin1(x))
        x = self.lin2(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:] # Without bias
        num = 1
        for i in size:
            num *= i
        return num

net = SimpleNetwork()

# Load the network if it was trained alredy
model_path = '/tmp/simple_linear_nn_pytorch.pt'
if os.path.exists(model_path):
    net = torch.load(model_path)

criterion = nn.MSELoss()

pprint(net)

x = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
input = Variable(torch.Tensor([x for _ in range(10)]))
y = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
target = Variable(torch.Tensor([y for _ in range(10)]))

for i in range(100):

    # Compute the output
    output = net(input)
    # Compute the MSE based loss
    loss = criterion(output, target)

    print(i, loss.tolist())
    if loss.tolist() < 0.000001:
        print("Break at", i)
        break
    # Reset the gradient
    net.zero_grad()
    loss.backward()
    # Stochastik gradient descent
    optimizer = optim.SGD(net.parameters(), lr=0.1)
    # Perform the next step
    optimizer.step()

# Store the network
torch.save(net, model_path)