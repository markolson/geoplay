from geoplay.shapefile import Shapefile
from shapely.geometry import Point, mapping
import urllib.request
from pathlib import Path
import fiona
import pprint
import csv

class NYFarmersMarket(Shapefile):
  NAME = 'NYC Farmers Markets'
  URL = 'https://data.cityofnewyork.us/api/views/8vwk-6iz2/rows.csv?accessType=DOWNLOAD'
  DEST = Path('data/ny-city-farmers-markets.csv')
  SHP = Path('data/ny-city-farmers-markets/mapped.shp')
  PROJ4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

  def __init__(self):
    Shapefile.__init__(self)

  def fetch_data(self):
    if self.SHP.exists():
      return

    to_lat_lng = lambda row: [row['Latitude'], row['Longitude']]

    self.log("Fetching data...")
    urllib.request.urlretrieve(self.URL, self.DEST)
    self.log("Converting to Shapefile...")
    self.SHP.parent.mkdir(parents=True, exist_ok=True)

    shp = fiona.open(self.SHP, 'w', driver="ESRI Shapefile", crs=self.PROJ4, schema={
      'geometry': 'Point',
      'properties': {
        'MarketName': 'str',
        'Borough': 'str'
      }
    })

    with open(self.DEST) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        point = Point(float(row['Longitude']), float(row['Latitude']))
        shp.write({ 'geometry': mapping(point), 'properties': {
          'MarketName': row['Market Name'],
          'Borough': row['Borough']
        }})

    shp.flush()


