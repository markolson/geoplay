import fiona
import functools
import geopandas as gpd
import tempfile

class Shapefile:
  def __init__(self):
    self._file = None
    if self.SHP.exists():
      return

    self.log("No data found.")
    self.fetch_data()
    self.log("Done")

  def log(self, msg):
    print("[" + self.NAME + "] " + msg)

  def has_data(self):
    return

  def shapefile(self):
    if self._file == None:
      self.log("Loading Shapefile")
      self._file = fiona.open(self.SHP)
    # print("Returning shapefile w/ crs:" + fiona.crs.to_string(self._file.crs))
    return self._file

  @functools.lru_cache()
  def project_to(self, new_projection):
    self.log("Setting Projection")
    rdir = self.SHP.parent / 're-projected'
    rdir.mkdir(parents=True, exist_ok=True)
    new_shp = rdir / self.SHP.name

    # TODO: make sure new_shp is the right projection
    if new_shp.exists():
      self._file = fiona.open(new_shp)
      return self

    f = gpd.GeoDataFrame.from_file(self.SHP)
    f.crs = self.PROJ4
    # f.to_crs(new_projection)
    f['geometry'] = f['geometry'].to_crs(new_projection)
    f.crs = new_projection
    f.to_file(driver = 'ESRI Shapefile', filename=new_shp)
    self.log("Reloading Shapefile")
    self._file = fiona.open(new_shp)
    print("Setting shapefile w/ crs:" + fiona.crs.to_string(self._file.crs))
    return self
