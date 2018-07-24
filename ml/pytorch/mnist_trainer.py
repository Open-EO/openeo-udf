# -*- coding: utf-8 -*-
import torch
from torchvision import datasets, transforms

kwargs = {'num_workers': 1, 'pin_memory': True}
trans = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
train = torch.utils.data.DataLoader(datasets.MNIST('data',
                                                   train=True,
                                                   download=True,
                                                   transform=trans),
                                    batch_size=64, shuffle=True, **kwargs)

test = torch.utils.data.DataLoader(datasets.MNIST('data',
                                                  train=False,
                                                  download=True,
                                                  transform=trans),
                                   batch_size=64, shuffle=True, **kwargs)

