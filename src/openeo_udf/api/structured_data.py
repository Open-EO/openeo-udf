#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

from typing import Dict


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class StructuredData:
    """This class represents structured data that is produced by an UDF and can not be represented
    as a RasterCollectionTile or FeatureCollectionTile. For example the result of a statistical
    computation. The data is self descriptive and supports the basic types dict/map, list and table.

    The data field contains the UDF specific values (argument or return) as dict, list or table:

        * A dict can be as complex as required by the UDF
        * A list must contain simple data types example {\"list\": [1,2,3,4]}
        * A table is a list of lists with a header, example {\"table\": [[\"id\",\"value\"],
                                                                           [1,     10],
                                                                           [2,     23],
                                                                           [3,     4]]}

    >>> table = [("col_1", "col_2"), (1, 2), (2, 3)]
    >>> st = StructuredData(description="Table output", data=table, type="table")
    >>> st.to_dict() # doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Table output', 'data': [('col_1', 'col_2'), (1, 2), (2, 3)], 'type': 'table'}

    >>> values = [1,2,3,4]
    >>> st = StructuredData(description="List output", data=values, type="list")
    >>> st.to_dict() # doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    {'description': 'List output', 'data': [1, 2, 3, 4], 'type': 'list'}

    >>> key_value_store = dict(a=1, b=2, c=3)
    >>> st = StructuredData(description="Key-value output", data=key_value_store, type="dict")
    >>> st.to_dict() # doctest: +ELLIPSIS
    ...              # doctest: +NORMALIZE_WHITESPACE
    {'description': 'Key-value output', 'data': {'a': 1, 'b': 2, 'c': 3}, 'type': 'dict'}

    """

    def __init__(self, description, data, type):
        self.description = description
        self.data = data
        self.type = type

    def to_dict(self) -> Dict:
        return dict(description=self.description, data=self.data, type=self.type)

    @staticmethod
    def from_dict(structured_data: Dict):
        description = structured_data["description"]
        data = structured_data["data"]
        type = structured_data["type"]
        return StructuredData(description=description, data=data, type=type)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
