import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import functools
import geopandas as gpd
import tempfile

class Raster:
  def __init__(self):
    self._file = None
    if self.RASTER.exists():
      return

    self.log("No data found.")
    self.fetch_data()
    self.log("Done")

  def log(self, msg):
    print("[" + self.NAME + "] " + msg)

  def has_data(self):
    return

  def image(self):
    if self._file == None:
      self.log("Loading Shapefile")
      self._file = rasterio.open(self.RASTER)
    return self._file

  @functools.lru_cache()
  def project_to(self, new_projection):
    return self
