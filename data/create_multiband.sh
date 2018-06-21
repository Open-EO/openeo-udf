#!/bin/bash
rm red_nir_1987.tif
rm red_nir_2000.tif
rm red_nir_2002.tif

gdal_merge.py -separate red_1987.tif nir_1987.tif -o red_nir_1987.tif
gdal_merge.py -separate red_2000.tif nir_2000.tif -o red_nir_2000.tif
gdal_merge.py -separate red_2002.tif nir_2002.tif -o red_nir_2002.tif

# Within the GRASS GIS north carolina location in the landsat mapset
r.out.gdal input=lsat7_2002_10 output=lsat7_2002_10.tif
r.out.gdal input=lsat7_2002_20 output=lsat7_2002_20.tif
r.out.gdal input=lsat7_2002_30 output=lsat7_2002_30.tif
r.out.gdal input=lsat7_2002_40 output=lsat7_2002_40.tif
r.out.gdal input=lsat7_2002_50 output=lsat7_2002_50.tif
r.out.gdal input=lsat7_2002_60 output=lsat7_2002_60.tif
r.out.gdal input=lsat7_2002_70 output=lsat7_2002_70.tif
r.out.gdal input=lsat7_2002_80 output=lsat7_2002_80.tif

# Merge the tiffs into a multiband tiff
gdal_merge.py -separate lsat7_2002_10.tif lsat7_2002_20.tif lsat7_2002_30.tif lsat7_2002_40.tif lsat7_2002_50.tif lsat7_2002_70.tif lsat7_2002_80.tif -o lsat7_2002.tif

# Create GRASS GIS scikit learn model based on north carolina landsat data
i.group group=lsat7_2002 input=lsat7_2002_10,lsat7_2002_20,lsat7_2002_30,lsat7_2002_40,lsat7_2002_50,lsat7_2002_70,lsat7_2002_80

# Perform the training and save the trained data
g.region raster=landclass96 -p
r.random input=landclass96 npoints=100 raster=landclass96_roi --o
# Run the scikit-learn module and store the trained model
r.learn.ml group=lsat7_2002 trainingmap=landclass96_roi save_model=lsat7_2002_class.model.gz \
           classifier=RandomForestClassifier n_estimators=100 max_depth=3 output=lsat7_2002_class -b --o

r.category lsat7_2002_class raster=landclass96
# copy color scheme from landclass training map to result
r.colors lsat7_2002_class raster=landclass96
r.category lsat7_2002_class

r.out.gdal input=lsat7_2002_class output=lsat7_2002_class.tif --o
r.out.gdal input=landclass96 output=landclass96.tif --o
