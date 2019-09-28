from kbrgeo.kshp import KShp
import urllib.request
from zipfile import ZipFile
from pathlib import Path
"""
Expose a

"""
class ZCTA(KShp):
  NAME = 'ZCTA'
  URL = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_zcta510_500k.zip'
  DEST = Path('data/zcta.zip')
  SHP = Path('data/zcta/cb_2018_us_zcta510_500k.shp')

  def __init__(self):
    KShp.__init__(self)

  def fetch_data(self):
    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Extracting data...")
    with ZipFile('data/zcta.zip', 'r') as z:
      z.extractall('data/zcta')

  def filterTo(self, zipCodes=[]):
    zipList = list(map(str, zipCodes))
    return list(filter(lambda r: r['properties']['GEOID10'] in zipList, self.shp()))