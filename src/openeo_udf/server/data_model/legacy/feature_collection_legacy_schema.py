# -*- coding: utf-8 -*-
from typing import Dict, List

from pydantic import BaseModel, Schema

__license__ = "Apache License, Version 2.0"
__author__ = "Soeren Gebbert"
__copyright__ = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

EXAMPLE = {
    "id": "test_data",
    "start_times": ["2001-01-01T00:00:00",
                    "2001-01-02T00:00:00"],
    "end_times": ["2001-01-02T00:00:00",
                  "2001-01-03T00:00:00"],
    "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                           "geometry": {"coordinates": [24.0, 50.0], "type": "Point"}},
                          {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                           "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
             "type": "FeatureCollection"}
}


class FeatureCollectionLegacyModel(BaseModel):
    """Vector data that represents a spatio-temporal
    subset of a spatio-temporal vector dataset."""

    id: str = Schema(..., description="The identifier of this feature collection.", examples=[{"id": "test_data"}])

    data: Dict = Schema(..., description="A GeoJSON FeatureCollection.",
                        examples=[
                            {"data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                                                    "geometry": {"coordinates": [24.0, 50.0], "type": "Point"}},
                                                   {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                                                    "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                                      "type": "FeatureCollection"}}])

    start_time: List[str] = Schema(None, description="The array that contains that start time values for "
                                                     "each vector feature. As date-time string format "
                                                     "ISO 8601 must be supported.",
                                   examples=[{"start_times": ["2001-01-01T00:00:00", "2001-01-02T00:00:00"]}])

    end_time: List[str] = Schema(None,
                                 description="The vector that contains that end time values for each "
                                             "vector feature, in case the "
                                             "the time stamps for all or a subset of slices are intervals. "
                                             "For time instances the from and to time stamps must be equal or empty."
                                             "As date-time string format ISO 8601 must be supported.",
                                 examples=[{"end_times": ["2001-01-02T00:00:00", "2001-01-03T00:00:00"]}])

    class Config:
        schema_extra = {
            'examples': [EXAMPLE]
        }
