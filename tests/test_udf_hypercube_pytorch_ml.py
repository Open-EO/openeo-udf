# -*- coding: utf-8 -*-
from typing import Tuple

import numpy
import torch
import torch.nn as nn
import torch.nn.functional as F
import xarray
from openeo_udf.api.machine_learn_model import MachineLearnModel

from openeo_udf.api.hypercube import HyperCube
from torch.autograd import Variable
import torch.optim as optim
from pprint import pprint
import os
import pprint
import unittest

from openeo_udf.api.tools import create_hypercube
from openeo_udf.api.udf_data import UdfData
from openeo_udf.server.main import app
from starlette.testclient import TestClient
from openeo_udf.server.endpoints import create_storage_directory
from openeo_udf.server.udf_schemas import UdfCodeModel, UdfRequestModel
import openeo_udf.functions


__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

class SimpleNetwork(nn.Module):

    def __init__(self):
        super(SimpleNetwork, self).__init__()
        self.lin1 = nn.Linear(2, 2)
        self.lin2 = nn.Linear(2, 2)

    def forward(self, x):
        x = F.relu(self.lin1(x))
        x = self.lin2(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num = 1
        for i in size:
            num *= i
        return num


class MachineLearningPytorchTestCase(unittest.TestCase):
    create_storage_directory()

    def setUp(self):
        self.app = TestClient(app=app)

    @staticmethod
    def train_pytorch_model(model):
        """Train an arbitrary pytroch model with two features

        Args:
            model: The machine learn model to be used for training

        Returns:
            str:
            The filename of the resulting

        """
        model_path = '/tmp/simple_linear_nn_pytorch.pt'
        criterion = nn.MSELoss()
        a = numpy.random.randint(1, 4, 10)
        a = a.reshape([5, 2])
        input = Variable(torch.Tensor(a))
        target = Variable(torch.Tensor(a))
        for i in range(200):
            output = model(input)
            loss = criterion(output, target)
            model.zero_grad()
            loss.backward()
            optimizer = optim.SGD(model.parameters(), lr=0.1)
            optimizer.step()
        torch.save(model, model_path)

    def test_pytorch_linear_nn(self):
        """Test linear pytorch model training and UDF application"""

        model = SimpleNetwork()

        MachineLearningPytorchTestCase.train_pytorch_model(model=model)

        dir = os.path.dirname(openeo_udf.functions.__file__)
        file_name = os.path.join(dir, "hypercube_pytorch_ml.py")
        udf_code = UdfCodeModel(language="python", source=open(file_name, "r").read())

        temp = create_hypercube(name="temp", value=1, dims=("x", "y"), shape=(2, 2))

        ml = MachineLearnModel(framework="pytorch", name="linear_model",
                               description="A pytorch model that adds two numbers in range of [1,1]",
                               path="/tmp/simple_linear_nn_pytorch.pt")
        udf_data = UdfData(proj={"EPSG":4326}, hypercube_list=[temp], ml_model_list=[ml])
        print(udf_data.to_dict())

        udf_request = UdfRequestModel(data=udf_data.to_dict(), code=udf_code)
        response = self.app.post('/udf', json=udf_request.dict())
        result = response.json()
        pprint.pprint(result)
        self.assertEqual(response.status_code, 200)
        result = response.json()

        pprint.pprint(result)


if __name__ == "__main__":
    unittest.main()
