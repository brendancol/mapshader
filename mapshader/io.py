import rioxarray
import xarray as xr
import datashader as ds
import geopandas as gpd
import numpy as np
from affine import Affine

from os.path import expanduser

from datashader.utils import calc_res


def load_raster(file_path, xmin=None, ymin=None,
                xmax=None, ymax=None, chunks=None):

    if file_path.endswith('.tif'):

        arr = xr.open_rasterio(expanduser(file_path),
                               chunks={'y': 512, 'x': 512})

        if hasattr(arr, 'nodatavals'):

            if np.issubdtype(arr.data.dtype, np.integer):
                arr.data = arr.data.astype('f8')

            for val in arr.nodatavals:
                arr.data[arr.data == val] = np.nan

        arr.name = file_path

    elif file_path.endswith('.nc'):
        # TODO: add chunk parameter to config
        arr = xr.open_dataset(file_path, chunks={'x': 512, 'y': 512})['data']
        arr['name'] = file_path

    else:
        raise TypeError(f"Unable to load raster {file_path}")

    return arr


def load_vector(filepath: str):
    return gpd.read_file(filepath)
