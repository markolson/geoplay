#

from geoplay.shapefile import Shapefile
import urllib.request
from zipfile import ZipFile
from pathlib import Path

class PhlZips(Shapefile):
  NAME = 'PHL Zip Boundaries'

  URL = 'http://data.phl.opendata.arcgis.com/datasets/b54ec5210cee41c3a884c9086f7af1be_0.zip'
  DEST = Path('data/phl-zips.zip')
  SHP = Path('data/phl-zips/Zipcodes_Poly.shp')

  PROJ4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

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
    return list(filter(lambda r: r['properties']['CODE'] in zipList, self.shapefile()))