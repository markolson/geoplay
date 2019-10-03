sfrom geoplay.shapefile import Shapefile
from shapely.geometry import Point, mapping
import urllib.request
from pathlib import Path
import fiona
import pprint
import csv

class NYTrees(Shapefile):
  NAME = 'NYC Trees'

  URL = 'https://data.cityofnewyork.us/api/views/uvpi-gqnh/rows.csv?accessType=DOWNLOAD'
  DEST = Path('data/NYTrees.csv')
  SHP = Path('data/ny-trees/mapped.shp')

  PROJ4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    if self.SHP.exists():
      return

    if not self.DEST.exists():
      self.log("Fetching data...")
      urllib.request.urlretrieve(self.URL, self.DEST)

    self.log("Converting to Shapefile...")
    self.SHP.parent.mkdir(parents=True, exist_ok=True)

    shp = fiona.open(self.SHP, 'w', driver="ESRI Shapefile", crs=self.PROJ4, schema={
      'geometry': 'Point',
      'properties': {
        'spc_latin': 'str'
      }
    })

    with open(self.DEST) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        point = Point(float(row['longitude']), float(row['latitude']))
        shp.write({ 'geometry': mapping(point), 'properties': {
          'spc_latin': row['spc_latin']
        }})

    shp.flush()
