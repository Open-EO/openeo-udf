#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes of the OpenEO Python UDF interface

"""
import os
from typing import Optional, Dict
from openeo_udf.server.config import UdfConfiguration


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class MachineLearnModel(object):
    """This class represents a machine learn model. The model will be loaded
    at construction, based on the machine learn framework.

    The following frameworks are supported:
        - sklearn models that are created with sklearn.externals.joblib
        - pytorch models that are created with torch.save

    >>> from sklearn.ensemble import RandomForestRegressor
    >>> from sklearn.externals import joblib
    >>> model = RandomForestRegressor(n_estimators=10, max_depth=2, verbose=0)
    >>> path = '/tmp/test.pkl.xz'
    >>> dummy = joblib.dump(value=model, filename=path, compress=("xz", 3))
    >>> m = MachineLearnModel(framework="sklearn", name="test",
    ...                       description="Machine learn model", path=path)
    >>> m.get_model()# doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
               max_features='auto', max_leaf_nodes=None,
               min_impurity_decrease=0.0, min_impurity_split=None,
               min_samples_leaf=1, min_samples_split=2,
               min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
               oob_score=False, random_state=None, verbose=0, warm_start=False)
    >>> m.to_dict() # doctest: +ELLIPSIS
    ...             # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Machine learn model', 'name': 'test', 'framework': 'sklearn', 'path': '/tmp/test.pkl.xz'}
    >>> d = {'description': 'Machine learn model', 'name': 'test', 'framework': 'sklearn', 'path': '/tmp/test.pkl.xz'}
    >>> m = MachineLearnModel.from_dict(d)
    >>> m.get_model() # doctest: +ELLIPSIS
    ...               # doctest: +NORMALIZE_WHITESPACE
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
               max_features='auto', max_leaf_nodes=None,
               min_impurity_decrease=0.0, min_impurity_split=None,
               min_samples_leaf=1, min_samples_split=2,
               min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
               oob_score=False, random_state=None, verbose=0, warm_start=False)

    >>> import torch
    >>> import torch.nn as nn
    >>> model = nn.Module
    >>> path = '/tmp/test.pt'
    >>> torch.save(model, path)
    >>> m = MachineLearnModel(framework="pytorch", name="test",
    ...                       description="Machine learn model", path=path)
    >>> m.get_model()# doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    <class 'torch.nn.modules.module.Module'>
    >>> m.to_dict() # doctest: +ELLIPSIS
    ...             # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Machine learn model', 'name': 'test', 'framework': 'pytorch', 'path': '/tmp/test.pt'}
    >>> d = {'description': 'Machine learn model', 'name': 'test', 'framework': 'pytorch', 'path': '/tmp/test.pt'}
    >>> m = MachineLearnModel.from_dict(d)
    >>> m.get_model() # doctest: +ELLIPSIS
    ...               # doctest: +NORMALIZE_WHITESPACE
    <class 'torch.nn.modules.module.Module'>
    """

    def __init__(self, framework: str, name: str, description: str,
                 path: Optional[str] = None, md5_hash: Optional[str] = None):
        """The constructor to create a machine learn model object

        Args:
            framework: The name of the framework, pytroch and sklearn are supported
            name: The name of the model
            description: The description of the model
            path: The path to the pre-trained machine learn model that should be applied
            md5_hash: The md5 hash of the machine learn model that is located in the local storage
        """
        self.framework = framework
        self.name = name
        self.description = description
        self.path = path
        self.md5_hash = md5_hash
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the machine learn model from the path or md5 hash.

        Supported model:
        - sklearn models that are created with sklearn.externals.joblib
        - pytorch models that are created with torch.save

        """

        if self.md5_hash is not None:
            filepath = os.path.join(UdfConfiguration.machine_learn_storage_path, self.md5_hash)
        else:
            filepath = self.path

        if os.path.exists(filepath) and os.path.isfile(filepath):
            if self.framework.lower() in "sklearn":
                from sklearn.externals import joblib
                self.model = joblib.load(filepath)
            if self.framework.lower() in "pytorch":
                import torch
                self.model = torch.load(filepath)
        else:
            raise Exception(f"Unable to find the specified machine learn model at path {filepath}")

    def get_model(self):
        """Get the loaded machine learn model. This function will return None if the model was not loaded

        :return: the loaded model
        """
        return self.model

    def to_dict(self) -> Dict:
        return dict(description=self.description, name=self.name,
                    framework=self.framework, path=self.path, md5_hash=self.md5_hash)

    @staticmethod
    def from_dict(machine_learn_model: Dict):
        description = machine_learn_model["description"]
        name = machine_learn_model["name"]
        framework = machine_learn_model["framework"]

        path = None
        md5_hash = None

        if "path" in machine_learn_model:
            path = machine_learn_model["path"]
        if "md5_hash" in machine_learn_model:
            md5_hash = machine_learn_model["md5_hash"]

        return MachineLearnModel(description=description, name=name,
                                 framework=framework, path=path, md5_hash=md5_hash)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
