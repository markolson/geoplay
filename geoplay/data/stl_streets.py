from geoplay.shapefile import Shapefile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

class StlStreets(Shapefile):
  NAME = 'St. Louis Streets'
  URL = 'https://www.stlouis-mo.gov/data/upload/data-files/streets.zip'
  DEST = Path('data/stl-streets.zip')
  SHP = Path('data/stl-streets/TgrGeoCd.shp')
  PROJ4 = "+init=epsg:26796"

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)