from unittest import TestCase
from udf_data import PIXEL

class TestWrapper(TestCase):

    def test_timeseries_wrapper(self):
        from openeo_udf.api.udf_data import UdfData
        udf_data = UdfData.from_dict(PIXEL)
        from openeo_udf.api.udf_wrapper import apply_timeseries_generic
        rcts = udf_data.raster_collection_tiles
        apply_timeseries_generic(udf_data)

        self.assertEqual(rcts,udf_data.raster_collection_tiles)