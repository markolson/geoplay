import fiona
import functools

class KShp:
  def __init__(self):
    if self.has_data():
      return

    self.log("No data found.")
    self.fetch_data()
    self.log("Done")

  def log(self, msg):
    print("[" + self.NAME + "] " + msg)

  def has_data(self):
    # self.log("Checking for " + self.SHP.resolve().as_posix())
    return self.SHP.exists()

  @functools.lru_cache()
  def shp(self):
    self.log("Loading Shapefile")
    return fiona.open(self.SHP)

# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon
# def intersect(self, pointList):
#   pass