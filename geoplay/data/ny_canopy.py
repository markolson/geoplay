import urllib.request
from zipfile import ZipFile
from pathlib import Path
from geoplay.raster import Raster

class NYCanopy(Raster):
  NAME = 'NYC 3Ft Canopy'

  URL = 'https://data.cityofnewyork.us/api/views/9auy-76zt/files/mn9_hD2f5PJkYhHA_ebIDk7wCDXbFEBEWtMc05-3B1U?filename=Land%20Cover%202010.zip'
  DEST = Path('data/ny-canopy.zip')
  RASTER = Path('data/ny-canopy/landcover_2010_nyc_3ft.img')

  PROJ4 = "+init=esri:102718"

  def __init__(self):
    Raster.__init__(self)
    pass

  def fetch_data(self):
    if not self.DEST.exists():
      self.log("Fetching data...")
      urllib.request.urlretrieve(self.URL, self.DEST)

    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.SHP.parent)