from geoplay.shapefile import Shapefile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

class NyBikes(Shapefile):
  NAME = 'NY Bike Lanes'
  URL = 'https://data.cityofnewyork.us/api/geospatial/7vsa-caz7?method=export&format=Shapefile'
  DEST = Path('data/ny-bikes.zip')
  SHP = Path('data/ny-bikes/geo_export_49b8bffd-19fd-4612-809f-c4c73298d4ba.shp')
  PROJ4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)

