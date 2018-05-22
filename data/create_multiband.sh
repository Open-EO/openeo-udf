#!/bin/bash
rm red_nir_1987.tif
rm red_nir_2000.tif
rm red_nir_2002.tif

gdal_merge.py -separate red_1987.tif nir_1987.tif -o red_nir_1987.tif
gdal_merge.py -separate red_2000.tif nir_2000.tif -o red_nir_2000.tif
gdal_merge.py -separate red_2002.tif nir_2002.tif -o red_nir_2002.tif
