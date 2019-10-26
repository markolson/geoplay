#

import urllib.request
from zipfile import ZipFile
from pathlib import Path
from geoplay.raster import Raster

class PhlCanopy(Raster):
  NAME = 'PHL 10Ft Canopy'

  URL = 'ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhiladelphiaLandCoverRaster2008.zip'
  DEST = Path('data/phl-canopy.zip')
  RASTER = Path('data/phl-canopy/Land Cover Raster/land_2008/hdr.adf')

  PROJ4 = '+proj=lcc +lat_1=40.96666666666667 +lat_2=39.93333333333333 +lat_0=39.33333333333334 +lon_0=-77.75 +x_0=600000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs '

  def __init__(self):
    Raster.__init__(self)
    pass

  def fetch_data(self):
    if not self.DEST.exists():
      self.log("Fetching data...")
      urllib.request.urlretrieve(self.URL, self.DEST)

    self.log("Extracting data...")
    with ZipFile(self.DEST, 'r') as z:
      z.extractall(self.DEST.parent)