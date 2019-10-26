from geoplay.shapefile import Shapefile
import urllib.request
from zipfile import ZipFile
from pathlib import Path

class NyZips(Shapefile):
  NAME = 'NY Zip Boundaries'

  URL = 'https://data.cityofnewyork.us/api/views/i8iw-xf4u/files/YObIR0MbpUVA0EpQzZSq5x55FzKGM2ejSeahdvjqR20?filename=ZIP_CODE_040114.zip'
  DEST = Path('data/ny-zips.zip')
  SHP = Path('data/ny-zips/ZIP_CODE_040114.shp')

  PROJ4 = ' +proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 no_defs'

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    if not self.DEST.exists():
      self.log("Fetching data...")
      urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)

  def filter(self, property='', values=[]):
    pass

  def filterTo(self, zipCodes=[]):
    self.log("Limiting ZIP Codes to " + ', '.join(map(str, zipCodes)))
    zipList = list(map(str, zipCodes))
    return list(filter(lambda r: r['properties']['ZIPCODE'] in zipList, self.shapefile()))