
PIXEL = {
    "proj": "EPSG:4326",
    "raster_collection_tiles": [
        {
            "id": "RED",
            "wavelength": 420,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": [[[5, 4]],
                     [[9, 10]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        },
        {
            "id": "NIR",
            "wavelength": 670,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": [[[3, 4]],
                     [[9, 8]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        }
    ]
}

FEATURE = {
    "proj": "EPSG:4326",
    "feature_collection_tiles": [
        {
            "id": "test_data",
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": {"features": [{"id": "0", "type": "Feature", "properties": {"a": 1, "b": "a"},
                                   "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}},
                                  {"id": "1", "type": "Feature", "properties": {"a": 2, "b": "b"},
                                   "geometry": {"coordinates": [30.0, 53.0], "type": "Point"}}],
                     "type": "FeatureCollection"}
        }
    ]
}

PIXEL_FEATURE = {
    "proj": "EPSG:4326",
    "raster_collection_tiles": [

        {
            "id": "RED",
            "wavelength": 420,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00"],
            "data": [[[5, 4],
                      [3, 2]],
                     [[9, 10],
                      [8, 9]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        },
        {
            "id": "NIR",
            "wavelength": 670,
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00",
                            "2001-01-03T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00",
                          "2001-01-04T00:00:00"],
            "data": [[[2, 1],
                      [4, 3]],
                     [[7, 8],
                      [6, 7]],
                     [[1, 0],
                      [1, 0]]],
            "extent": {
                "top": 53,
                "bottom": 51,
                "right": 30,
                "left": 28,
                "height": 1,
                "width": 1
            }
        }
    ],
    "feature_collection_tiles": [
        {
            "id": "test_data",
            "start_times": ["2001-01-01T00:00:00",
                            "2001-01-02T00:00:00",
                            "2001-01-03T00:00:00"],
            "end_times": ["2001-01-02T00:00:00",
                          "2001-01-03T00:00:00",
                          "2001-01-04T00:00:00"],
            "data": {"features": [{"id": "0", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [28.5, 51.5], "type": "Point"}},
                                  {"id": "1", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [29.5, 52.5], "type": "Point"}},
                                  {"id": "2", "type": "Feature", "properties": {},
                                   "geometry": {"coordinates": [25, 55], "type": "Point"}}],
                     "type": "FeatureCollection"}
        }
    ]
}