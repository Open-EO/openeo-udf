from unittest import TestCase

from openeo_udf.api.tools import create_datacube
from openeo_udf.api.udf_data import UdfData


class TestWrapper(TestCase):


    def test_timeseries_wrapper(self):

        temp = create_datacube(name="temp", value=1, shape=(3, 3, 3))
        udf_data = UdfData(proj={"EPSG": 4326}, datacube_list=[temp])

        from openeo_udf.api.udf_wrapper import apply_timeseries_generic
        rcts = udf_data.get_datacube_list
        apply_timeseries_generic(udf_data)

        self.assertEqual(rcts,udf_data.get_datacube_list)