from kbrgeo.kshp import KShp
import urllib.request
from pathlib import Path

# extract
from zipfile import ZipFile

# transform
import geopandas as gpd
import tempfile
import fiona
import functools

class StlParks(KShp):
  NAME = 'St. Louis Parks'
  URL = 'https://www.stlouis-mo.gov/data/upload/data-files/parks.zip'
  DEST = Path('data/stl-parks.zip')
  SHP = Path('data/stl-parks/parks.shp')
  # no crs is set in the shp file, so we dug it out of the landuse xml file
  # https://spatialreference.org/ref/esri/102696/
  # NAD_1983_StatePlane_Missouri_East_FIPS_2401_Feet

  def __init__(self):
    KShp.__init__(self)

  def fetch_data(self):
    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)

  @functools.lru_cache()
  def shp(self):
    # TODO: move this from the shp() call
    # shp should just return `open_shp || process_shp()`
    # processed_file(self) -> self.SHP || override
    self.log("Re-Projecting to WGS84")
    rdir = self.SHP.parent / 're-projected'
    rdir.mkdir(parents=True, exist_ok=True)
    new_shp = rdir / 'stl-parks.shp'

    tmp = gpd.GeoDataFrame.from_file(self.SHP)
    tmp.crs = '+proj=tmerc +lat_0=35.83333333333334 +lon_0=-90.5 +k=0.9999333333333333 +x_0=250000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs'
    tmp.to_crs('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    tmp.to_file(driver = 'ESRI Shapefile', filename=new_shp)
    return fiona.open(new_shp)