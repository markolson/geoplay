from geoplay.shapefile import Shapefile
import urllib.request
from pathlib import Path
from zipfile import ZipFile


class StlParks(Shapefile):
  NAME = 'St. Louis Parks'
  URL = 'https://www.stlouis-mo.gov/data/upload/data-files/parks.zip'
  DEST = Path('data/stl-parks.zip')
  SHP = Path('data/stl-parks/parks.shp')

  PROJ4 = '+proj=tmerc +lat_0=35.83333333333334 +lon_0=-90.5 +k=0.9999333333333333 +x_0=250000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs'

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)