from geoplay.shapefile import Shapefile
import urllib.request
from zipfile import ZipFile
from pathlib import Path

class PreciseZCTA(Shapefile):
  NAME = 'Better ZCTA'

  URL = 'https://www2.census.gov/geo/tiger/TIGER2019/ZCTA5/tl_2019_us_zcta510.zip'
  DEST = Path('data/precise-zcta.zip')
  SHP = Path('data/precise-zcta/tl_2019_us_zcta510.shp')

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
    return list(filter(lambda r: r['properties']['GEOID10'] in zipList, self.shapefile()))