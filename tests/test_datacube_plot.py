'''
Created on Aug 25, 2020

@author: banyait
'''
import unittest
import numpy
from openeo_udf.api.datacube import DataCube
import xarray
from tempfile import TemporaryDirectory
import os
import matplotlib.pyplot as plt
import tempfile


class TestDataCubePlotter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmpdir=TemporaryDirectory()
        cls.tmpdir=str(cls._tmpdir.name)

    def buildData(self):
        a=numpy.zeros((3,2,100,100),numpy.int32)
        for t in range(a.shape[0]):
            for b in range(a.shape[1]):
                for x in range(a.shape[2]):
                    for y in range(a.shape[3]):
                        a[t,b,x,y]=(t*b+1)/(t+b+1)*(x*y+1)/(x+y+1)
        return DataCube(
            xarray.DataArray(
                a, 
                dims=['t','bands','x','y'],
                coords={
                    't':[numpy.datetime64('2020-08-01'),numpy.datetime64('2020-08-11'),numpy.datetime64('2020-08-21')],
                    'bands':['bandzero','bandone'],
                    'x':[10.+float(i) for i in range(a.shape[2])],
                    'y':[20.+float(i) for i in range(a.shape[3])]
                }
            )
        )

    def testPlot(self):
        refpng=plt.imread(os.path.join(os.path.dirname(__file__),'test_datacube_plot_reference_image.png'))
        tmpfile=os.path.join(self.tmpdir,'test.png')
        d=self.buildData()
        d.plot("title", oversample=1.5, cbartext="some\nvalue", to_file=tmpfile, to_show=False)
        respng=plt.imread(tmpfile)
        numpy.testing.assert_array_equal(refpng,respng)



