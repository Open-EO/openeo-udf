#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenEO Python UDF interface"""

import numpy
import xarray
from typing import Dict, List
import json


__license__ = "Apache License, Version 2.0"
__author__     = "Soeren Gebbert"
__copyright__  = "Copyright 2018, Soeren Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__      = "soerengebbert@googlemail.com"


class DataCube:
    """This class is a hypercube representation of multi-dimensional data
    that stores an xarray and provides methods to convert the xarray into
    the HyperCube JSON representation


    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)), coords={'x': [1, 2], 'y': [1, 2, 3]}, dims=('x', 'y'))
    >>> array.attrs["description"] = "This is an xarray with two dimensions"
    >>> array.name = "testdata"
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    'testdata'
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> d["description"]
    'This is an xarray with two dimensions'

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    'testdata'
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> d["description"]
    'This is an xarray with two dimensions'

    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)), coords={'x': [1, 2], 'y': [1, 2, 3]}, dims=('x', 'y'))
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> "description" not in d
    True

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    [{'name': 'x', 'coordinates': [1, 2]}, {'name': 'y', 'coordinates': [1, 2, 3]}]
    >>> "description" not in d
    True

    >>> array = xarray.DataArray(numpy.zeros(shape=(2, 3)))
    >>> h = DataCube(array=array)
    >>> d = h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    []
    >>> "description" not in d
    True

    >>> new_h = DataCube.from_dict(d)
    >>> d = new_h.to_dict()
    >>> d["id"]
    >>> d["data"]
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> d["dimensions"]
    []
    >>> "description" not in d
    True

    """

    def __init__(self, array: xarray.DataArray):

        self.set_array(array)

    def __str__(self):
        return "id: %(id)s\n" \
               "data: %(data)s"%{"id":self.id, "data":self.array}

    def get_array(self) -> xarray.DataArray:
        """Return the xarray.DataArray that contains the data and dimension definition

        Returns:
            xarray.DataArray: that contains the data and dimension definition

        """
        return self._array

    def set_array(self, array: xarray.DataArray):
        """Set the xarray.DataArray that contains the data and dimension definition

        This function will check if the provided data is a geopandas.GeoDataFrame and raises
        an Exception

        Args:
            array: xarray.DataArray that contains the data and dimension definition

        """
        if isinstance(array, xarray.DataArray) is False:
            raise Exception("Argument data must be of type xarray.DataArray")

        self._array = array

    @property
    def id(self):
        return self._array.name

    array = property(fget=get_array, fset=set_array)

    def to_dict(self) -> Dict:
        """Convert this hypercube into a dictionary that can be converted into
        a valid JSON representation

        Returns:
            dict:
            HyperCube as a dictionary

        >>> example = {
        ...     "id": "test_data",
        ...     "data": [
        ...         [
        ...             [0.0, 0.1],
        ...             [0.2, 0.3]
        ...         ],
        ...         [
        ...             [0.0, 0.1],
        ...             [0.2, 0.3]
        ...         ]
        ...     ],
        ...     "dimension": [{"name": "time", "unit": "ISO:8601", "coordinates":["2001-01-01", "2001-01-02"]},
        ...                   {"name": "X", "unit": "degree", "coordinates":[50.0, 60.0]},
        ...                   {"name": "Y", "unit": "degree"},
        ...                  ]
        ... }
        
        """

        d = {"id":"", "data": "", "dimensions":[]}
        if self._array is not None:
            xd = self._array.to_dict()

            if "name" in xd:
                d["id"] = xd["name"]

            if "data" in xd:
                d["data"] = xd["data"]

            if "attrs" in xd:
                if "description" in xd["attrs"]:
                    d["description"] = xd["attrs"]["description"]

            if "dims" in xd and "coords" in xd:
                for dim in xd["dims"]:
                    if dim in xd["coords"]:
                        if "data" in xd["coords"][dim]:
                            d["dimensions"].append({"name": dim, "coordinates": xd["coords"][dim]["data"]})
                        else:
                            d["dimensions"].append({"name": dim})

        return d

    @staticmethod
    def from_dict(hc_dict: Dict) -> "DataCube":
        """Create a hypercube from a python dictionary that was created from
        the JSON definition of the HyperCube

        Args:
            hc_dict (dict): The dictionary that contains the hypercube definition

        Returns:
            HyperCube

        """

        if "id" not in hc_dict:
            raise Exception("Missing id in dictionary")

        if "data" not in hc_dict:
            raise Exception("Missing data in dictionary")

        coords = {}
        dims = list()

        if "dimensions" in hc_dict:
            for dim in hc_dict["dimensions"]:
                dims.append(dim["name"])
                if "coordinates" in dim:
                    coords[dim["name"]] = dim["coordinates"]

        if dims and coords:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]), coords=coords, dims=dims)
        elif dims:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]), dims=dims)
        else:
            data = xarray.DataArray(numpy.asarray(hc_dict["data"]))

        if "id" in hc_dict:
            data.name = hc_dict["id"]
        if "description" in hc_dict:
            data.attrs["description"] = hc_dict["description"]

        hc = DataCube(array=data)

        return hc

    def to_data_collection(self):
        pass

    @staticmethod
    def from_data_collection(data_collection: 'openeo_udf.server.data_model.data_collection_schema.DataCollectionModel') -> List['DataCube']:
        """Create data cubes from a data collection

        Args:
            data_collection:

        Returns:
            A list of data cubes

        """

        dc_list = []

        data_cubes = data_collection.object_collections.data_cubes
        variables_collections = data_collection.variables_collections

        for cube in data_cubes:
            variable_collection = variables_collections[cube.variable_collection]

            # Read the one dimensional array and reshape it
            coords = {}
            for key in cube.dimensions.keys():
                d = cube.dimensions[key]
                if d.values:
                    coords[key] = d.values
                else:
                    l = d.number_of_cells
                    if l != 0 and d.extent:
                        stepsize = (d.extent[1] - d.extent[0])/l
                        values = []
                        predecessor = d.extent[0]
                        for i in range(l):
                            value = predecessor + stepsize/2.0
                            values.append(value)
                            predecessor = predecessor + stepsize
                        coords[key] = values

            for variable in variable_collection.variables:
                array = numpy.asarray(variable.values)
                array = array.reshape(variable_collection.size)

                data = xarray.DataArray(array, dims=cube.dim, coords=coords)
                data.name = variable.name

                dc = DataCube(array=data)
                dc_list.append(dc)

        return dc_list


    @staticmethod
    def from_file(filename, fmt='netcdf') -> "DataCube":
        if fmt.lower()=='netcdf':
            return DataCube(DataCube._load_DataArray_from_NetCDF(filename))
        if fmt.lower()=='json':
            return DataCube(DataCube._load_DataArray_from_JSON(filename))
    
    
    def to_file(self, filename, fmt='netcdf'):
        if fmt.lower()=='netcdf':
            return DataCube._save_DataArray_to_NetCDF(filename, self.get_array())
        if fmt.lower()=='json':
            return DataCube._save_DataArray_to_JSON(filename, self.get_array())
    
    
    @staticmethod
    def _load_DataArray_from_JSON(filename) -> xarray.DataArray:
        with open(filename) as f:
            # get the deserialized json
            d=json.load(f)
            d['data']=numpy.array(d['data'],dtype=numpy.dtype(d['attrs']['dtype']))
            for k,v in d['coords'].items():
                # prepare coordinate 
                d['coords'][k]['data']=numpy.array(v['data'],dtype=v['attrs']['dtype'])
                # remove dtype and shape, because that is included for helping the user
                if d['coords'][k].get('attrs',None) is not None:
                    d['coords'][k]['attrs'].pop('dtype',None)
                    d['coords'][k]['attrs'].pop('shape',None)
            
            # remove dtype and shape, because that is included for helping the user
            if d.get('attrs',None) is not None:
                d['attrs'].pop('dtype',None)
                d['attrs'].pop('shape',None)
            # vonvert to xarray
            r=xarray.DataArray.from_dict(d)
            del d
        # build dimension list in proper order
        dims=list(filter(lambda i: i!='t' and i!='bands' and i!='x' and i!='y',r.dims))
        if 't' in r.dims: dims+=['t']
        if 'bands' in r.dims: dims+=['bands']
        if 'x' in r.dims: dims+=['x']
        if 'y' in r.dims: dims+=['y']
        # return the resulting data array
        return r.transpose(*dims)
    
    
    @staticmethod
    def _load_DataArray_from_NetCDF(filename) -> xarray.DataArray:
        # load the dataset and convert to data array
        ds=xarray.open_dataset(filename, engine='h5netcdf')
        r=ds.to_array(dim='bands')
        # build dimension list in proper order
        dims=list(filter(lambda i: i!='t' and i!='bands' and i!='x' and i!='y',r.dims))
        if 't' in r.dims: dims+=['t']
        if 'bands' in r.dims: dims+=['bands']
        if 'x' in r.dims: dims+=['x']
        if 'y' in r.dims: dims+=['y']
        # return the resulting data array
        return r.transpose(*dims)
    
    
    @staticmethod
    def _save_DataArray_to_JSON(filename, array: xarray.DataArray):
        # to deserialized json
        jsonarray=array.to_dict()
        # add attributes that needed for re-creating xarray from json
        jsonarray['attrs']['dtype']=str(array.values.dtype)
        jsonarray['attrs']['shape']=list(array.values.shape)
        for i in array.coords.values():
            jsonarray['coords'][i.name]['attrs']['dtype']=str(i.dtype)
            jsonarray['coords'][i.name]['attrs']['shape']=list(i.shape)
        # custom print so resulting json file is humanly easy to read
        with open(filename,'w') as f:
            def custom_print(data_structure, indent=1):
                f.write("{\n")
                needs_comma=False
                for key, value in data_structure.items():
                    if needs_comma: 
                        f.write(',\n')
                    needs_comma=True
                    f.write('  '*indent+json.dumps(key)+':')
                    if isinstance(value, dict): 
                        custom_print(value, indent+1)
                    else: 
                        json.dump(value,f,default=str,separators=(',',':'))
                f.write('\n'+'  '*(indent-1)+"}")
                
            custom_print(jsonarray)
    
    
    @staticmethod
    def _save_DataArray_to_NetCDF(filename, array: xarray.DataArray):
        # temp reference to avoid modifying the original array
        result=array
        # rearrange in a basic way because older xarray versions have a bug and ellipsis don't work in xarray.transpose()
        if result.dims[-2]=='x' and result.dims[-1]=='y':
            l=list(result.dims[:-2])
            result=result.transpose(*(l+['y','x']))
        # turn it into a dataset where each band becomes a variable
        if not 'bands' in result.dims:
            result=result.expand_dims(dim={'bands':['band_0']})
        else:
            if not 'bands' in result.coords:
                labels=['band_'+str(i) for i in range(result.shape[result.dims.index('bands')])]
                result=result.assign_coords(bands=labels)
        result=result.to_dataset('bands')
        result.to_netcdf(filename, engine='h5netcdf')

    def plot(
            self,
            title=None, 
            limits=None,
            show_bandnames=True,
            show_dates=True,
            fontsize=10,
            oversample=1,
            cmap='RdYlBu_r', 
            cbartext:str=None,
            to_file:str=None,
            to_show=True
        ):

        from matplotlib import pyplot
        
        data=self.get_array()
        if limits is None:
            vmin=data.min()
            vmax=data.max()
        else: 
            vmin=limits[0]
            vmax=limits[1]
        nrow=data.shape[0]
        ncol=data.shape[1]
        data=data.transpose('t','bands','y','x')
        dpi=100
        xres=len(data.x)/dpi
        yres=len(data.y)/dpi
        fs=fontsize/oversample
        frame=0.33
    
        fig = pyplot.figure(figsize=((ncol+frame)*xres*1.1,(nrow+frame)*yres),dpi=int(dpi*oversample)) 
        gs = pyplot.GridSpec(nrow,ncol,wspace=0.,hspace=0.,top=nrow/(nrow+frame),bottom=0.,left=frame/(ncol+frame),right=1.) 
         
        for i in range(nrow):
            for j in range(ncol):
                im = data[i,j]
                ax= pyplot.subplot(gs[i,j])
                ax.set_axis_off()
                img=ax.imshow(im[::-1,:],vmin=vmin,vmax=vmax,cmap=cmap)
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                if show_bandnames:
                    if i==0: ax.text(0.5,1.08, data.bands.values[j]+" ("+str(data.dtype)+")", size=fs, va="center", ha="center", transform=ax.transAxes)
                if show_dates:
                    if j==0: ax.text(-0.08,0.5, data.t.dt.strftime("%Y-%m-%d").values[i], size=fs, va="center", ha="center", rotation=90,  transform=ax.transAxes)
    
        if title is not None:
            fig.text(0.,1.,title.split('/')[-1], size=fs, va="top", ha="left",weight='bold')
    
        cbar_ax = fig.add_axes([0.01, 0.1, 0.04, 0.5])
        if cbartext is not None:
            fig.text(0.06,0.62,cbartext, size=fs, va="bottom", ha="center")
        cbar=fig.colorbar(img, cax=cbar_ax)
        cbar.ax.tick_params(labelsize=fs)
        cbar.outline.set_visible(False)
        cbar.ax.tick_params(size=0)
        cbar.ax.yaxis.set_tick_params(pad=0)
        
        if to_file is not None: pyplot.savefig(to_file)
        if to_show: pyplot.show()
    
        pyplot.close()



if __name__ == "__main__":
    import doctest
    doctest.testmod()
